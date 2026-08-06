#!/usr/bin/env python3
"""
add_news_sources.py — One-shot: (a) backfill track/scope on every source in
the registry, (b) append 15 news-track sources (frontier labs, framework
specs, trust journalism, tldr;sec).

Idempotent. Run twice → adds nothing.

    python scripts/add_news_sources.py --dry-run
    python scripts/add_news_sources.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import common as c  # noqa: E402


NEWS_SOURCES = [
    # Frontier lab announcements (primary)
    ("https://openai.com/blog/rss.xml", "OpenAI Blog",
     ["ai-research", "ai-security"], "ai", "high", "news",
     "First-party OpenAI product/capability/pricing announcements"),
    ("https://www.anthropic.com/news/rss.xml", "Anthropic News",
     ["ai-research", "ai-security"], "ai", "high", "news",
     "Anthropic news + incident disclosures"),
    ("https://deepmind.google/discover/blog/rss.xml", "Google DeepMind Blog",
     ["ai-research"], "ai", "high", "news",
     "DeepMind research + robotics + capability posts"),
    ("https://blog.google/technology/ai/rss/", "Google AI Blog",
     ["ai-research", "ai-security"], "ai", "high", "news",
     "Google-wide AI product / announcement layer"),
    ("https://ai.meta.com/blog/rss/", "Meta AI Blog",
     ["ai-research"], "ai", "high", "news",
     "Llama releases, research previews, product announcements"),
    ("https://mistral.ai/news/rss.xml", "Mistral AI News",
     ["ai-research"], "ai", "high", "news",
     "Mistral model releases and product announcements"),
    ("https://huggingface.co/blog/feed.xml", "Hugging Face Blog",
     ["ai-research", "ai-security"], "ai", "high", "news",
     "Model release ecosystem — includes Kimi/Qwen/Llama mirrors"),

    # Framework / spec / standards
    ("https://github.com/modelcontextprotocol/specification/releases.atom",
     "Model Context Protocol releases",
     ["ai-research", "ai-security"], "ai", "high", "news",
     "MCP spec release feed — every version bump lands here"),
    ("https://blog.langchain.dev/rss/", "LangChain Blog",
     ["ai-research"], "ai", "medium", "news",
     "LangChain framework releases + ecosystem posts"),
    ("https://www.llamaindex.ai/blog/rss.xml", "LlamaIndex Blog",
     ["ai-research"], "ai", "medium", "news",
     "LlamaIndex releases + agent architecture posts"),

    # Incident / trust journalism
    ("https://www.theregister.com/security/headlines.atom",
     "The Register — Security",
     ["product-security", "ai-security"], "both", "medium", "news",
     "Incident and breach coverage; filter via classifier"),
    ("https://feeds.arstechnica.com/arstechnica/security",
     "Ars Technica Security",
     ["product-security", "ai-security"], "both", "medium", "news",
     "Security journalism with technical depth"),
    ("https://www.wired.com/feed/category/security/latest/rss",
     "Wired Security",
     ["product-security", "ai-security"], "both", "medium", "news",
     "Security journalism — must classify on-topic per item"),
    ("https://tldrsec.com/feed", "tldr;sec",
     ["product-security", "ai-security"], "both", "high", "news",
     "Weekly security newsletter by Clint Gibler; high signal"),
]


def scope_from_topics(topics: list[str]) -> str:
    has_ai = any(t.startswith("ai-") for t in topics)
    has_sec = "product-security" in topics
    if has_ai and has_sec:
        return "both"
    return "ai" if has_ai else "security"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src_path = ROOT / "data" / "sources.json"
    sources = json.loads(src_path.read_text(encoding="utf-8"))
    existing_ids = {s["id"] for s in sources}

    # Pass 1 — backfill track/scope on every existing entry.
    track_added = 0
    scope_added = 0
    for s in sources:
        if "track" not in s or s.get("track") is None:
            if s.get("name") == "Trail of Bits":
                s["track"] = "both"
            else:
                s["track"] = "research"
            track_added += 1
        if "scope" not in s or s.get("scope") is None:
            s["scope"] = scope_from_topics(s.get("topics", []))
            scope_added += 1

    # Pass 2 — append the news sources.
    added_news = 0
    skipped_news = 0
    for url, name, topics, scope, tier, track, notes in NEWS_SOURCES:
        sid = f"rss:{c.slugify(url, 48)}"
        if sid in existing_ids:
            skipped_news += 1
            continue
        sources.append({
            "id": sid,
            "type": "rss",
            "handle": url,
            "name": name,
            "url": url,
            "topics": topics,
            "domains": [],
            "tier": tier,
            "track": track,
            "scope": scope,
            "signals": {},
            "stats": {"ingested": 0, "curated": 0},
            "rank": 70.0 if tier == "medium" else 80.0,
            "added": "2026-08-06",
            "active": True,
            "notes": notes,
            "strict": False,
        })
        added_news += 1
        existing_ids.add(sid)

    print(f"Backfilled track on {track_added}, scope on {scope_added}")
    print(f"News sources: {added_news} added, {skipped_news} already present")
    print(f"Total sources after: {len(sources)}")

    if args.dry_run:
        print("[dry-run] no writes.")
        return 0

    src_path.write_text(
        json.dumps(sources, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {src_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
