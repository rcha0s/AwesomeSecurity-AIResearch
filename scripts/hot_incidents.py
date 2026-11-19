#!/usr/bin/env python3
"""
hot_incidents.py - the few incidents everyone in security is talking about, called out
on top of the Briefing with a short summary each. Pure helpers plus a small CLI.

Rohan, 2026-11-18, after NGINX2Root and Java4Shell were not on the site: "They're like
the hottest thing right now in cybersecurity ... I need to be called out as soon as
possible", with "a section for these kind of incident-related things that are really hot
and popular": what the root cause is, the conditions around it, how it can be exploited,
"a summary version of it". And: "you don't want to do this for every advisory item."

THE BAR (one definition, used by the intake fast path, the hourly watch and the
validator of data/hot_incidents.json, and printed on the README, the site and the feed):

    critical      a critical rating (CVSS 9+ or the vendor's "critical"), or unauthenticated
                  remote code execution. "Exploited" alone is not critical: it is one of
                  the reach reasons below, never counted twice.
    and `min_outlets` (3) or more independent outlets (GitHub repos and HN posts do not
    count; one registrable domain is one outlet; a patch roundup or weekly recap copy
    is not an outlet),
    and at least TWO of:
      exploited     exploited in the wild (a CISA KEV listing counts)
      wide-coverage covered by `wide_outlets` (4) or more independent outlets
                    (GitHub repos and HN posts do not count)
      ubiquitous    very common software (config.yaml `hot_incidents.ubiquitous`) named in a
                    copy's headline. Edge appliances that are on CISA KEV most weeks
                    (FortiOS, PAN-OS, Ivanti, NetScaler) are deliberately not on that list:
                    they qualify only as exploited AND widely covered.

So a CISA KEV entry for a niche product, a critical CVE one vendor posts, an exploited
appliance bug two or three outlets write up, or a Patch Tuesday roundup does not
qualify: those stay in the normal lanes. NGINX2Root (critical,
nginx, a dozen outlets) and Java4Shell (critical, Java, eight outlets) do.

data/hot_incidents.json holds the curated entries (`add` validates one; the scan writes
them for candidates the fast path flags). Each entry is a summary, never exploit code:

    id, name, headline, cves[], disclosed, updated, severity, status,
    bar[]           the reasons it clears the bar (two or more of the three above)
    affected, root_cause, conditions, exploitation, impact, fix
    sources[]       {name, url}: at least two independent outlets, https only
    finding_id      optional: the pool entry with the full writeup
    flag            set by `add` for a scan-written entry: the data/_scan_hot.json story id

Usage:
    python scripts/hot_incidents.py validate            # every entry against the bar
    python scripts/hot_incidents.py add FILE.json       # validate one entry and upsert it
    python scripts/hot_incidents.py list                # what the Briefing shows now
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

import common as c

FILE_NAME = "hot_incidents.json"
FEED_NAME = "hot-incidents.md"
JSON_FEED_NAME = "hot-incidents.json"
REACH = ("exploited", "wide-coverage", "ubiquitous")
REASON_LABEL = {
    "exploited": "exploited in the wild",
    "wide-coverage": "widely covered",
    "ubiquitous": "very common software",
}
DEFAULTS = {
    "wide_outlets": 4,  # independent outlets for `wide-coverage` (3 let routine exploited-bug news in)
    "min_outlets": 3,  # never fewer, whatever else holds (2 let weekly KEV news in)
    "min_reach": 2,  # how many REACH reasons it needs
    "show_days": 30,  # the Briefing shows an incident this long after its last update
    "ubiquitous": [],
}
SUMMARY_FIELDS = (
    "headline",
    "severity",
    "status",
    "affected",
    "root_cause",
    "conditions",
    "exploitation",
    "impact",
    "fix",
)
FIELD_LABEL = {
    "affected": "Affected",
    "root_cause": "Root cause",
    "conditions": "Conditions to exploit",
    "exploitation": "How it is exploited",
    "impact": "Impact",
    "fix": "Fix or mitigation",
}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,60}$")
CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Text that would read as working exploit material on a public page. A summary says how
# exploitation works at a high level; payloads and code blocks belong to the vendors.
EXPLOIT_TEXT = re.compile(r"```|<script|\\x[0-9a-f]{2}|/bin/sh|curl\s+-|wget\s+http", re.I)
FIELD_MAX = 700
# Copies that bundle many bugs: never an outlet for one incident, never its markers.
ROUNDUP = re.compile(
    r"patch tuesday|roundup|round-up|recap|week in review|this week in|weekly|newsletter"
    r"|security updates? for (?:\w+ )?(?:january|february|march|april|may|june|july"
    r"|august|september|october|november|december)",
    re.I,
)
NOT_OUTLETS = frozenset({"github.com", "ycombinator.com"})
BAR_NOTE = (
    "Only incidents that are critical, covered by 3+ independent outlets, and clear two "
    "of: exploited in the wild (CISA KEV counts), 4+ outlets, very common software. "
    "Routine advisories and patch roundups never qualify."
)


def settings(conf: c.Config | None = None) -> dict:
    """config.yaml `hot_incidents:` over DEFAULTS; anything malformed reads as the default."""
    raw = getattr(conf, "hot", None) or {}
    if not isinstance(raw, dict):
        raw = {}
    out = dict(DEFAULTS)
    for key in ("wide_outlets", "min_outlets", "min_reach", "show_days"):
        try:
            out[key] = max(1, int(raw.get(key, DEFAULTS[key])))
        except (TypeError, ValueError):
            pass
    names = raw.get("ubiquitous") or []
    out["ubiquitous"] = [str(n).strip() for n in names if isinstance(n, str) and n.strip()]
    return out


# --- the bar -----------------------------------------------------------------------
def is_critical(markers: frozenset[str] | set[str]) -> bool:
    """Critical by newsworthy.py's markers: rated critical, or pre-auth RCE. Exploited
    alone is not (it is a reach reason; "zero-day" and "under attack" set it)."""
    m = set(markers)
    return "critical" in m or {"rce", "unauthenticated"} <= m


def ubiquitous_hit(text: str, names: list[str]) -> str:
    """The first configured very-common-software name in `text` (whole words), or ""."""
    for name in names:
        if re.search(r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])", text, re.I):
            return name
    return ""


def bar_reasons(
    markers: frozenset[str] | set[str],
    outlets: int,
    exploited: bool,
    ubiquitous: bool,
    conf: dict | None = None,
) -> list[str]:
    """Why a story clears the hot bar, or [] when it does not. `outlets` counts
    independent publishers (not GitHub, not HN); `exploited` is a KEV listing or a
    confirmed-exploitation marker."""
    s = conf or DEFAULTS
    if not is_critical(markers) or outlets < s["min_outlets"]:
        return []
    reasons = []
    if exploited or "exploited" in set(markers):
        reasons.append("exploited")
    if outlets >= s["wide_outlets"]:
        reasons.append("wide-coverage")
    if ubiquitous:
        reasons.append("ubiquitous")
    return reasons if len(reasons) >= s["min_reach"] else []


# --- the curated file --------------------------------------------------------------
def path() -> Path:
    return c.DATA_DIR / FILE_NAME


def load() -> list[dict]:
    data = c.load_json(path(), default={"incidents": []}) or {}
    rows = data.get("incidents") if isinstance(data, dict) else None
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def save(rows: list[dict]) -> None:
    ordered = sorted(rows, key=lambda r: (str(r.get("updated") or ""), str(r.get("id"))))
    c.save_json(path(), {"incidents": list(reversed(ordered))})


def _https(url: object) -> bool:
    u = str(url or "")
    parsed = urlparse(u)
    return parsed.scheme == "https" and bool(parsed.netloc) and not re.search(r"[\s<>\"`]", u)


def _host(url: str) -> str:
    """The outlet behind a URL: its registrable domain, as newsworthy.publisher counts."""
    host = (urlparse(url).hostname or "").lower()
    labels = [p for p in host.split(".") if p]
    if (
        len(labels) >= 3
        and labels[-2] in ("co", "com", "org", "net", "ac", "gov")
        and len(labels[-1]) == 2
    ):
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def problems(entry: object, s: dict | None = None) -> list[str]:
    """Everything wrong with one curated entry; [] means it may be published.
    `s` is settings() (config.yaml); DEFAULTS when not given."""
    s = s or DEFAULTS
    if not isinstance(entry, dict):
        return ["entry is not an object"]
    out = []
    eid = str(entry.get("id") or "")
    if not ID_RE.match(eid):
        out.append(f"id {eid!r} must be lowercase letters, digits and dashes")
    tag = eid or "?"
    if not str(entry.get("name") or "").strip():
        out.append(f"{tag}: name is missing")
    for key in ("disclosed", "updated"):
        if not DATE_RE.match(str(entry.get(key) or "")):
            out.append(f"{tag}: {key} must be YYYY-MM-DD")
    cves = entry.get("cves")
    if not isinstance(cves, list) or any(not CVE_RE.match(str(x)) for x in cves):
        out.append(f"{tag}: cves must be a list of CVE-YYYY-NNNN ids (may be empty)")
    for key in SUMMARY_FIELDS:
        text = entry.get(key)
        if not isinstance(text, str) or not text.strip():
            out.append(f"{tag}: {key} is missing")
        elif len(text) > FIELD_MAX:
            out.append(f"{tag}: {key} runs past {FIELD_MAX} characters; keep it a summary")
        elif EXPLOIT_TEXT.search(text):
            out.append(f"{tag}: {key} reads like exploit material; describe it at a high level")
    bar = entry.get("bar")
    if not isinstance(bar, list) or any(b not in REACH for b in bar):
        out.append(f"{tag}: bar must list reasons from {', '.join(REACH)}")
    elif len(set(bar)) < s["min_reach"]:
        out.append(
            f"{tag}: clears {len(set(bar))} of the bar's reasons; a hot incident needs "
            f"{s['min_reach']} ({BAR_NOTE})"
        )
    sources = entry.get("sources")
    if not isinstance(sources, list) or any(
        not isinstance(s, dict) or not _https(s.get("url")) or not str(s.get("name") or "").strip()
        for s in sources
    ):
        out.append(f"{tag}: sources must be {{name, url}} with https urls")
    else:
        hosts = {_host(x["url"]) for x in sources} - NOT_OUTLETS
        if len(hosts) < s["min_outlets"]:
            out.append(f"{tag}: needs at least {s['min_outlets']} independent outlets")
        if "wide-coverage" in (bar or []) and len(hosts) < s["wide_outlets"]:
            out.append(f"{tag}: claims wide coverage but cites {len(hosts)} outlet(s)")
    fid = entry.get("finding_id")
    if fid is not None and not (isinstance(fid, str) and re.match(r"^[a-z0-9-]{1,120}$", fid)):
        out.append(f"{tag}: finding_id must be a pool entry id")
    flag = entry.get("flag")
    if flag is not None and not (isinstance(flag, str) and re.match(r"^[\w.:-]{1,200}$", flag)):
        out.append(f"{tag}: flag must be the flagged story's id")
    if DATE_RE.match(str(entry.get("disclosed") or "")) and DATE_RE.match(
        str(entry.get("updated") or "")
    ):
        if entry["updated"] < entry["disclosed"]:
            out.append(f"{tag}: updated is before disclosed")
    return out


def validate(rows: list[dict], s: dict | None = None) -> list[str]:
    out = [p for row in rows for p in problems(row, s)]
    ids = [str(r.get("id")) for r in rows]
    out += [f"duplicate id {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    return out


def active(rows: list[dict], now: str, show_days: int) -> list[dict]:
    """Entries updated in the last `show_days`, newest update first."""
    cutoff = (date.fromisoformat(now) - timedelta(days=show_days)).isoformat()
    live = [r for r in rows if str(r.get("updated") or "") >= cutoff]
    return sorted(
        live, key=lambda r: (str(r.get("updated")), str(r.get("disclosed"))), reverse=True
    )


def payload_rows(rows: list[dict]) -> list[dict]:
    """The subset the site renders (plain strings, https links only)."""
    keep = ("id", "name", "disclosed", "updated", "finding_id", *SUMMARY_FIELDS)
    out = []
    for row in rows:
        item = {k: str(row.get(k) or "") for k in keep}
        item["cves"] = [str(x) for x in row.get("cves") or [] if CVE_RE.match(str(x))]
        item["bar"] = [b for b in row.get("bar") or [] if b in REACH]
        item["sources"] = [
            {"name": str(s.get("name")), "url": str(s.get("url"))}
            for s in row.get("sources") or []
            if isinstance(s, dict) and _https(s.get("url"))
        ]
        out.append(item)
    return out


# --- rendering ---------------------------------------------------------------------
def _md(text: object) -> str:
    out = " ".join(str(text or "").split())
    return re.sub(r"([\\\[\]<>*_`|])", r"\\\1", out)


def reasons_text(bar: list[str]) -> str:
    return ", ".join(REASON_LABEL[b] for b in REACH if b in bar)


def readme_lines(rows: list[dict], site_url: str, limit: int = 3) -> list[str]:
    """The README's Hot incidents section: one line each, newest first; [] when none."""
    if not rows:
        return []
    out = ["## Hot incidents", "", f"_{BAR_NOTE} [Summaries]({site_url}{FEED_NAME})._", ""]
    for i, row in enumerate(rows[:limit], 1):
        cves = f" · {', '.join(row['cves'][:2])}" if row.get("cves") else ""
        link = f"{site_url}?hot={row['id']}#week"
        out.append(
            f"{i}. **[{_md(row['name'])}: {_md(row['headline'])}]({link})** · "
            f"_{_md(reasons_text(row['bar']))}{cves} · updated {row['updated']}_"
        )
    return out + [""]


def render_feed(rows: list[dict], now: str, site_url: str) -> str:
    """docs/hot-incidents.md: every curated incident in full, for people and harnesses."""
    out = [
        "# Hot incidents",
        "",
        f"_Generated {now} from data/{FILE_NAME} by scripts/generate_html.py. "
        "Generated - do not hand-edit._",
        "",
        BAR_NOTE,
        "",
        f"Site: {site_url}#week · JSON: {site_url}{JSON_FEED_NAME}",
        "",
    ]
    if not rows:
        return "\n".join(out + ["_No hot incidents yet._", ""])
    for row in rows:
        cves = ", ".join(row["cves"]) or "no CVE yet"
        out += [
            f"## {_md(row['name'])}: {_md(row['headline'])}",
            "",
            f"{cves} · disclosed {row['disclosed']} · updated {row['updated']} · "
            f"why hot: {_md(reasons_text(row['bar']))}",
            "",
            f"- **Severity:** {_md(row['severity'])}",
            f"- **Status:** {_md(row['status'])}",
        ]
        out += [f"- **{FIELD_LABEL[k]}:** {_md(row[k])}" for k in FIELD_LABEL]
        links = " · ".join(f"[{_md(s['name'])}]({s['url']})" for s in row["sources"])
        out += [f"- **Sources:** {links}", ""]
    return "\n".join(out)


def render_json(rows: list[dict], now: str) -> str:
    return json.dumps({"generated": now, "bar": BAR_NOTE, "incidents": rows}, indent=2) + "\n"


def scan_flags() -> list[dict]:
    """data/_scan_hot.json: the stories this run's fast path flagged (select_batch.py)."""
    data = c.load_json(c.DATA_DIR / "_scan_hot.json", [])
    return [f for f in data if isinstance(f, dict)] if isinstance(data, list) else []


def covered(titles: list[str], ids: set[str], rows: list[dict]) -> bool:
    """data/hot_incidents.json already calls this story out: a shared CVE, or an
    incident's name in one of the copies' headlines."""
    for inc in rows:
        if ids & {str(x).lower() for x in inc.get("cves") or []}:
            return True
        name = str(inc.get("name") or "")
        pattern = r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])"
        if name and any(re.search(pattern, t or "", re.I) for t in titles):
            return True
    return False


def _flag_urls(flag: dict) -> set[str]:
    return {_canon(u) for u in [flag.get("url"), *(flag.get("coverage") or [])] if u}


def _canon(url: object) -> str:
    parsed = urlparse(str(url or ""))
    host = (parsed.hostname or "").lower().removeprefix("www.")
    return f"{host}{parsed.path.rstrip('/')}"


def add_problems(entry: dict, rows: list[dict], flags: list[dict], today: str) -> list[str]:
    """`add` is the scan session's only way in (containment denies editing the file).

    A NEW entry must name the fast-path flag it summarizes (`flag`: the flagged story's
    id in data/_scan_hot.json), cite at least one of the flagged story's own URLs, claim
    no reason the code did not find, and use a flag no other entry used.

    An UPDATE (same id) keeps its CVEs and disclosure date, and may add a bar reason only
    when a current flag for the same story found it. `updated` is never after today, so
    an entry cannot hold the top of the section by moving its date forward.
    Hand-curated entries arrive by reviewed PR, not through `add`."""
    tag = str(entry.get("id"))
    out = []
    if str(entry.get("updated") or "") > today:
        out.append(f"{tag}: updated is after today ({today})")
    by_id = {str(f.get("id")): f for f in flags}
    flag = by_id.get(str(entry.get("flag") or ""))
    old = next((r for r in rows if r.get("id") == entry.get("id")), None)
    if old is not None:
        if sorted(entry.get("cves") or []) != sorted(old.get("cves") or []) and not flag:
            out.append(f"{tag}: an update keeps the published CVEs unless a current flag backs it")
        if entry.get("disclosed") != old.get("disclosed"):
            out.append(f"{tag}: an update keeps the disclosure date")
        allowed = set(old.get("bar") or []) | set((flag or {}).get("reasons") or [])
        extra = set(entry.get("bar") or []) - allowed
        if extra:
            out.append(f"{tag}: bar adds {sorted(extra)}, which no current flag found")
        return out
    if flag is None:
        return out + [
            f"{tag}: a new entry needs `flag` set to a story id in data/_scan_hot.json; "
            "the fast path did not flag this one"
        ]
    if any(r.get("flag") == flag.get("id") for r in rows):
        out.append(f"{tag}: flag {flag.get('id')} already backs another entry")
    cited = {_canon(x.get("url")) for x in entry.get("sources") or [] if isinstance(x, dict)}
    if not cited & _flag_urls(flag):
        out.append(f"{tag}: cite at least one of the flagged story's own URLs")
    extra = set(entry.get("bar") or []) - set(flag.get("reasons") or [])
    if extra:
        out.append(f"{tag}: bar claims {sorted(extra)}, which the flag did not find")
    return out


# --- CLI ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    add = sub.add_parser("add")
    add.add_argument("file")
    sub.add_parser("list")
    args = parser.parse_args(argv)
    rows = load()
    if args.cmd == "validate":
        errs = validate(rows, settings(c.load_config()))
        for e in errs:
            print(f"  - {e}")
        print(f"hot incidents: {len(rows)} entries, {len(errs)} problems")
        return 1 if errs else 0
    if args.cmd == "add":
        entry = json.loads(Path(args.file).read_text(encoding="utf-8"))
        s = settings(c.load_config())
        today = c.utcnow().strftime("%Y-%m-%d")
        errs = problems(entry, s) or add_problems(entry, rows, scan_flags(), today)
        if errs:
            print("refused:\n" + "\n".join(f"  - {e}" for e in errs))
            return 1
        rows = [r for r in rows if r.get("id") != entry["id"]] + [entry]
        save(rows)
        print(f"hot incidents: upserted {entry['id']} ({len(rows)} entries)")
        return 0
    now = c.utcnow().strftime("%Y-%m-%d")
    for row in active(rows, now, settings(c.load_config())["show_days"]):
        print(f"{row['updated']}  {row['name']}: {row['headline']}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
