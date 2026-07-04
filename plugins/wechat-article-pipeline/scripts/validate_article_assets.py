#!/usr/bin/env python3
"""Validate article frontmatter, image links, and Baoyu visual artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    block = text[4:end]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("article", help="Markdown article path")
    parser.add_argument("--require-baoyu", action="store_true", help="Require imgs/outline.md and prompt files")
    args = parser.parse_args()

    article = Path(args.article).resolve()
    errors: list[str] = []

    if not article.exists():
        print(f"ERROR: article not found: {article}", file=sys.stderr)
        return 2

    text = article.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if not fm.get("title"):
        errors.append("frontmatter title is missing")

    cover = fm.get("coverImage") or fm.get("cover") or fm.get("image")
    if cover:
        cover_path = (article.parent / cover).resolve()
        if not cover_path.exists():
            errors.append(f"cover image not found: {cover}")
    else:
        errors.append("frontmatter coverImage is missing")

    for match in IMAGE_RE.finditer(text):
        rel = match.group(1).strip()
        if rel.startswith(("http://", "https://")):
            continue
        img_path = (article.parent / rel).resolve()
        if not img_path.exists():
            errors.append(f"markdown image not found: {rel}")

    imgs_dir = article.parent / "imgs"
    has_generated = any(imgs_dir.glob("*.png")) if imgs_dir.exists() else False
    if args.require_baoyu or has_generated:
        outline = imgs_dir / "outline.md"
        prompts = imgs_dir / "prompts"
        if not outline.exists():
            errors.append("Baoyu visual outline missing: imgs/outline.md")
        if not prompts.exists() or not any(prompts.glob("*.md")):
            errors.append("Baoyu visual prompt files missing: imgs/prompts/*.md")
        else:
            for prompt in prompts.glob("*.md"):
                if prompt.name.startswith("00-cover") or "cover" in prompt.name:
                    continue
                body = prompt.read_text(encoding="utf-8")
                required_groups = {
                    "layout": ["LAYOUT", "STRUCTURE"],
                    "colors": ["COLORS", "PALETTE"],
                    "style": ["STYLE"],
                    "aspect": ["ASPECT"],
                }
                missing = [
                    label
                    for label, options in required_groups.items()
                    if not any(option in body for option in options)
                ]
                if missing:
                    errors.append(f"{prompt.name} missing prompt sections: {', '.join(missing)}")
                content_markers = [
                    "LABELS",
                    "NODES",
                    "STEPS",
                    "ZONES",
                    "LEFT SIDE",
                    "RIGHT SIDE",
                    "RELATIONSHIPS",
                ]
                if not any(marker in body for marker in content_markers):
                    errors.append(f"{prompt.name} missing content-specific sections")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {article}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
