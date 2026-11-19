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
                  remote code execution, or confirmed exploitation in the wild
    and at least TWO of:
      exploited     exploited in the wild (a CISA KEV listing counts)
      wide-coverage covered by `wide_outlets` (4) or more independent outlets
                    (GitHub repos and HN posts do not count)
      ubiquitous    in very common software (config.yaml `hot_incidents.ubiquitous`)

    and never: a single outlet, a patch roundup (Patch Tuesday) or a lone vendor bulletin.

So a CISA KEV entry for a niche product, a critical CVE one vendor posts, or a story two
outlets carry does not qualify: those stay in the normal lanes. NGINX2Root (critical,
nginx, a dozen outlets) and Java4Shell (critical, Java, eight outlets) do.

data/hot_incidents.json holds the curated entries (`add` validates one; the scan writes
them for candidates the fast path flags). Each entry is a summary, never exploit code:

    id, name, headline, cves[], disclosed, updated, severity, status,
    bar[]           the reasons it clears the bar (two or more of the three above)
    affected, root_cause, conditions, exploitation, impact, fix
    sources[]       {name, url}: at least two independent outlets, https only
    finding_id      optional: the pool entry with the full writeup
    flag            `add` only, for a new entry: the data/_scan_hot.json story id (not stored)

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
    "min_outlets": 2,  # never a single outlet, whatever else holds
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
BAR_NOTE = (
    "Only incidents that are critical and clear at least two of: exploited in the wild "
    "(CISA KEV counts), covered by 4+ independent outlets, in very common software. "
    "Routine advisories never qualify."
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
    """Critical by newsworthy.py's markers: rated critical, pre-auth RCE, or exploited."""
    m = set(markers)
    return "critical" in m or "exploited" in m or {"rce", "unauthenticated"} <= m


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
    host = urlparse(url).netloc.lower().split(":")[0]
    return host[4:] if host.startswith("www.") else host


def problems(entry: object) -> list[str]:
    """Everything wrong with one curated entry; [] means it may be published."""
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
    elif len(set(bar)) < DEFAULTS["min_reach"]:
        out.append(
            f"{tag}: clears {len(set(bar))} of the bar's reasons; a hot incident needs "
            f"{DEFAULTS['min_reach']} ({BAR_NOTE})"
        )
    sources = entry.get("sources")
    if not isinstance(sources, list) or any(
        not isinstance(s, dict) or not _https(s.get("url")) or not str(s.get("name") or "").strip()
        for s in sources
    ):
        out.append(f"{tag}: sources must be {{name, url}} with https urls")
    else:
        hosts = {_host(s["url"]) for s in sources}
        if len(hosts) < DEFAULTS["min_outlets"]:
            out.append(f"{tag}: needs at least {DEFAULTS['min_outlets']} independent outlets")
        if "wide-coverage" in (bar or []) and len(hosts) < DEFAULTS["wide_outlets"]:
            out.append(f"{tag}: claims wide coverage but cites {len(hosts)} outlet(s)")
    fid = entry.get("finding_id")
    if fid is not None and not (isinstance(fid, str) and re.match(r"^[a-z0-9-]{1,120}$", fid)):
        out.append(f"{tag}: finding_id must be a pool entry id")
    return out


def validate(rows: list[dict]) -> list[str]:
    out = [p for row in rows for p in problems(row)]
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


def add_problems(entry: dict, rows: list[dict], flags: list[dict]) -> list[str]:
    """`add` is the scan session's only way in (containment denies editing the file), so
    a NEW entry must name the fast-path flag it summarizes (`flag`: the flagged
    candidate id) and claim no reason the code did not find. Updating an entry that is
    already published needs no flag. Hand-curated entries arrive by reviewed PR."""
    if any(r.get("id") == entry.get("id") for r in rows):
        return []
    by_id = {str(f.get("id")): f for f in flags}
    flag = by_id.get(str(entry.get("flag") or ""))
    if flag is None:
        return [
            f"{entry.get('id')}: a new entry needs `flag` set to a story id in "
            "data/_scan_hot.json; the fast path did not flag this one"
        ]
    extra = set(entry.get("bar") or []) - set(flag.get("reasons") or [])
    if extra:
        return [f"{entry.get('id')}: bar claims {sorted(extra)}, which the flag did not find"]
    return []


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
        errs = validate(rows)
        for e in errs:
            print(f"  - {e}")
        print(f"hot incidents: {len(rows)} entries, {len(errs)} problems")
        return 1 if errs else 0
    if args.cmd == "add":
        entry = json.loads(Path(args.file).read_text(encoding="utf-8"))
        errs = problems(entry) or add_problems(entry, rows, scan_flags())
        if errs:
            print("refused:\n" + "\n".join(f"  - {e}" for e in errs))
            return 1
        entry.pop("flag", None)
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
