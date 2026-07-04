#!/usr/bin/env python3
"""Create a standard WeChat article topic workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value:
        value = "wechat-topic"
    return value[:80].strip("-")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("title", help="Topic title or slug seed")
    parser.add_argument("--root", default="docs/content-agent/topics", help="Topics root directory")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Date suffix, YYYY-MM-DD")
    parser.add_argument("--no-date", action="store_true", help="Do not append date suffix")
    args = parser.parse_args()

    slug = slugify(args.title)
    if not args.no_date and not slug.endswith(args.date):
        slug = f"{slug}-{args.date}"

    topic_dir = Path(args.root) / slug
    for child in ["sources", "extracted", "imgs/prompts", "prompts"]:
        (topic_dir / child).mkdir(parents=True, exist_ok=True)

    manifest = {
        "title": args.title,
        "slug": slug,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "directories": {
            "topic": str(topic_dir),
            "sources": str(topic_dir / "sources"),
            "extracted": str(topic_dir / "extracted"),
            "images": str(topic_dir / "imgs"),
            "prompts": str(topic_dir / "prompts"),
        },
    }
    (topic_dir / "topic-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(topic_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
