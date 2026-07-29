#!/usr/bin/env python3
"""
generate_og.py - Render the social/hero card the README and link unfurls use.

Draws docs/og.png (1200x630) from live data so it refreshes on every run: the
masthead, the week's tallies, and the lead headlines, in the same editorial
house style as the site. No screenshot tooling required (pure Pillow), so it
works in CI.

Usage:
    python scripts/generate_og.py
"""

from __future__ import annotations

from datetime import UTC, datetime

from PIL import Image, ImageDraw, ImageFont

import common as c

import claims as cl

from generate_html import build_payload

W, H, S = 1200, 630, 2  # final size, and supersample factor for crisp text

# House palette (light "paper" theme, matching the site).
PAPER = (244, 242, 236)
CARD = (251, 250, 246)
INK = (27, 26, 23)
INK2 = (74, 71, 64)
INK3 = (114, 109, 98)
RULE = (216, 211, 198)
ACCENT = (122, 32, 22)
TRACK = {
    "ai-security": (154, 59, 46),
    "product-security": (47, 93, 98),
    "ai-research": (75, 63, 122),
}

FONTS = "/usr/share/fonts/truetype"
SERIF_B = f"{FONTS}/crosextra/Caladea-Bold.ttf"
SERIF_I = f"{FONTS}/crosextra/Caladea-Italic.ttf"
MONO = f"{FONTS}/dejavu/DejaVuSansMono.ttf"
MONO_B = f"{FONTS}/dejavu/DejaVuSansMono-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size * S)
    except OSError:
        return ImageFont.truetype(MONO, size * S)


def tw(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> float:
    return draw.textlength(text, font=f)


def fit(draw, text: str, f, max_w: int) -> str:
    """Truncate text with an ellipsis so it fits max_w (device px)."""
    if tw(draw, text, f) <= max_w:
        return text
    while text and tw(draw, text + "...", f) > max_w:
        text = text[:-1]
    return text.rstrip() + "..."


def tracks_present(payload) -> list[str]:
    return payload.get("topic_order") or list(payload.get("topics", {}))


def build_image(payload: dict) -> Image.Image:
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)
    m = 70 * S  # margin
    x0, x1 = m, W * S - m

    findings = payload.get("findings", [])
    claims = payload.get("claims", [])
    fresh = [f for f in findings if f.get("fresh")]
    retired = [c_ for c_ in claims if c_.get("status") in ("superseded", "refuted")]
    live = len(claims) - len(retired)

    def rule(y, weight, color=INK):
        d.rectangle([x0, y, x1, y + weight * S], fill=color)

    # --- Flag line ---
    y = m
    rule(y, 3)
    y += 10 * S
    fmono = font(MONO_B, 13)
    d.text((x0, y), "WEEKLY BRIEFING  /  AI & SECURITY RESEARCH", font=fmono, fill=INK2)
    issue = f"ISSUE {payload.get('generated', '')}"
    d.text((x1 - tw(d, issue, fmono), y), issue, font=fmono, fill=INK2)
    y += 22 * S
    rule(y, 1, RULE)

    # --- Title ---
    y += 26 * S
    ft = font(SERIF_B, 52)
    d.text((x0, y), "Awesome Security", font=ft, fill=INK)
    y += 56 * S
    d.text((x0, y), "& AI Research", font=ft, fill=INK)
    y += 60 * S

    # --- Tagline ---
    fi = font(SERIF_I, 20)
    tag = fit(
        d,
        "A weekly, source-cited briefing. One lesson and one action per finding, filed by field.",
        fi,
        x1 - x0,
    )
    d.text((x0, y), tag, font=fi, fill=INK2)
    y += 36 * S

    # --- Tally strip ---
    rule(y, 1, RULE)
    y += 18 * S
    cells = [
        (str(len(fresh)), "THIS WEEK"),
        (str(len(findings)), "VETTED FINDINGS"),
        (str(live), "STANDING CLAIMS"),
        (str(len(retired)), "REVERSALS"),
    ]
    fn = font(MONO_B, 34)
    fk = font(MONO, 12)
    cw = (x1 - x0) / len(cells)
    for i, (num, key) in enumerate(cells):
        cx = x0 + i * cw
        d.text((cx, y), num, font=fn, fill=INK)
        d.text((cx, y + 40 * S), key, font=fk, fill=INK3)
    y += 70 * S
    rule(y, 3, INK)  # double rule
    rule(y + 5 * S, 1, INK)

    # --- Lead headlines (two), placed above a pinned footer ---
    y += 24 * S
    pool = fresh if fresh else findings
    fh = font(SERIF_B, 19)
    fmeta = font(MONO, 12)
    for f in pool[:2]:
        tcol = TRACK.get(f.get("topic"), INK)
        r = 5 * S
        cy = y + 10 * S
        d.ellipse([x0, cy - r, x0 + 2 * r, cy + r], fill=tcol)
        title = fit(d, f.get("title", ""), fh, x1 - (x0 + 22 * S))
        d.text((x0 + 22 * S, y), title, font=fh, fill=INK)
        y += 30 * S
        meta = "   /   ".join(
            p
            for p in (
                payload["topics"].get(f.get("topic"), {}).get("name", ""),
                f.get("domain", ""),
            )
            if p
        )
        d.text((x0 + 22 * S, y), fit(d, meta, fmeta, x1 - (x0 + 22 * S)), font=fmeta, fill=INK3)
        y += 42 * S

    # --- Footer, pinned to the bottom margin with a divider ---
    fy = H * S - m
    rule(fy - 20 * S, 1, RULE)
    fu = font(MONO_B, 13)
    d.text((x0, fy), "rcha0s.github.io/AwesomeSecurity-AIResearch", font=fu, fill=ACCENT)
    tail = "vetted / source-cited / weekly"
    ftl = font(MONO, 13)
    d.text((x1 - tw(d, tail, ftl), fy), tail, font=ftl, fill=INK3)

    return img.resize((W, H), Image.LANCZOS)


def main() -> int:
    conf = c.load_config()
    ledger = cl.load_ledger()
    now = datetime.now(UTC).strftime("%Y-%m-%d")
    payload = build_payload(ledger, conf, now)
    docs = c.ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    img = build_image(payload)
    img.save(docs / "og.png")
    print(f"og: docs/og.png ({img.width}x{img.height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
