"""Re-audit item 1: payload numbers (trend counts, window sizes) never reach the DOM raw.

A scan PR can ship any data/trends.json, and render equality only proves the
page is main's template plus *some* payload. So both ends are hardened:
generate_html coerces trend numbers, and the template escapes every number.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import generate_html as gh
import pytest

EVIL = "<img src=x onerror=alert(1)>"


def _extract(src: str, name: str) -> str:
    start = src.index(f"function {name}(")
    depth = 0
    for i in range(src.index("{", start), len(src)):
        depth += {"{": 1, "}": -1}.get(src[i], 0)
        if depth == 0:
            return src[start : i + 1]
    raise ValueError(name)


def _js(names: list[str], prelude: str, expr: str) -> str:
    if not shutil.which("node"):
        pytest.skip("node not available")
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    script = (
        "\n".join(_extract(src, n) for n in names)
        + "\n"
        + prelude
        + f"\nprocess.stdout.write(JSON.stringify({expr}));"
    )
    out = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=10)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_num_only_ever_yields_digits():
    got = _js(["esc", "num"], "", f"[12, '7', {json.dumps(EVIL)}, null, {{}}, [], 1e30, -3]"
              ".map(num)")  # fmt: skip
    assert got[:2] == ["12", "7"]
    assert all(re.fullmatch(r"-?\d+", g) for g in got)


@pytest.mark.parametrize("field", ["count", "recent"])
def test_trend_rows_with_html_numbers_render_inert(field):
    row = {"tag": "x", "count": 3, "recent": 1, "momentum": 1, field: EVIL}
    prelude = "var TMETA = {}; var DATA = {topics: {}, trends: {t: [" + json.dumps(row) + "]}};"
    html = _js(["esc", "num", "clean", "tname", "tvar", "emergingBlock"], prelude,
               "emergingBlock('t', false)")  # fmt: skip
    assert "<img" not in html and "onerror" not in html
    assert "0 total" in html or "0 recent" in html


def test_template_has_no_raw_payload_numbers():
    """The sweep, pinned: each sink found in the re-audit goes through num()/esc()."""
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    for raw in (
        "' + r.count + '",
        "' + r.recent + '",
        "' + DATA.snapshot_days +",
        "+ DATA.max_age_days + ' days</span>",
        "' + DATA.news_front_page_days + '",
        "' + arch + '",
        "' + since : ",
        "' + c[0] + '",
        "' + c[1] + '",
    ):
        assert raw not in src, raw


# ---------------------------------------------------------------- generate_html side


@pytest.mark.parametrize(
    "bad",
    [
        {"count": EVIL},
        {"recent": EVIL},
        {"momentum": "fast"},
        {"momentum": float("nan")},
        {"momentum": float("inf")},
        {"count": [1]},
        {"count": {"a": 1}},
        {"count": True},
    ],
)
def test_trend_rows_with_bad_numbers_are_dropped(bad):
    good = {"tag": "ok", "count": 3, "recent": 1, "momentum": 2.5}
    assert gh._trend_rows([{**good, "tag": "bad", **bad}, good]) == [good]


def test_trend_numbers_are_coerced_and_other_fields_kept():
    rows = gh._trend_rows([{"tag": "t", "count": "4", "recent": 2.0, "members": [1]}])
    assert rows == [{"tag": "t", "count": 4, "recent": 2, "momentum": 0.0, "members": [1]}]
    assert isinstance(rows[0]["recent"], int) and isinstance(rows[0]["momentum"], float)


@pytest.mark.parametrize("rows", [None, "x", {"a": 1}, [1, "row", None]])
def test_malformed_trend_lists_yield_nothing(rows):
    assert gh._trend_rows(rows) == []


def test_real_trends_survive_unchanged():
    trends = json.loads((gh.c.DATA_DIR / "trends.json").read_text())
    for rows in trends.values():
        if isinstance(rows, list):
            assert gh._trend_rows(rows) == rows


def test_build_payload_ships_only_coerced_trend_rows(sandbox):
    import common
    from test_claims import ledger_of, make_claim

    good = {"topic": "ai-security", "tag": "ok", "count": 3, "recent": 1, "momentum": 1.0}
    bad = {**good, "tag": "bad", "count": EVIL}
    (sandbox / "data" / "trends.json").write_text(json.dumps({"ai-security": [bad, good]}))
    payload = gh.build_payload(ledger_of(make_claim()), common.load_config(), "2026-07-15")
    assert payload["trends"]["ai-security"] == [good]
    assert EVIL not in gh.render(payload, "2026-07-15")
