#!/usr/bin/env python3
"""Extract text and selected page/crop images from a PDF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_crop(spec: str) -> tuple[str, int, tuple[float, float, float, float]]:
    # name:page:x0,y0,x1,y1 where coords are page fractions.
    name, page, box = spec.split(":", 2)
    coords = tuple(float(x) for x in box.split(","))
    if len(coords) != 4:
        raise ValueError(f"invalid crop box: {spec}")
    return name, int(page), coords  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("--text-out")
    parser.add_argument("--images-dir")
    parser.add_argument("--pages", default="", help="Comma-separated 1-based pages to render")
    parser.add_argument("--crop", action="append", default=[], help="name:page:x0,y0,x1,y1 fraction crop")
    parser.add_argument("--scale", type=float, default=2.5)
    args = parser.parse_args()

    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise SystemExit("PyMuPDF is required: pip install pymupdf") from exc

    pdf = Path(args.pdf).resolve()
    doc = fitz.open(pdf)
    out: dict[str, object] = {"pdf": str(pdf), "pages": len(doc), "images": []}

    if args.text_out:
        chunks = []
        for idx, page in enumerate(doc):
            chunks.append(f"\n\n--- PAGE {idx + 1} ---\n")
            chunks.append(page.get_text("text"))
        Path(args.text_out).write_text("".join(chunks), encoding="utf-8")
        out["text_out"] = args.text_out

    images_dir = Path(args.images_dir) if args.images_dir else None
    if images_dir:
        images_dir.mkdir(parents=True, exist_ok=True)
        matrix = fitz.Matrix(args.scale, args.scale)
        for page_no in [int(p) for p in args.pages.split(",") if p.strip()]:
            page = doc[page_no - 1]
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            target = images_dir / f"page-{page_no:02d}.png"
            pix.save(target)
            out["images"].append(str(target))  # type: ignore[index]

        for crop_spec in args.crop:
            name, page_no, frac = parse_crop(crop_spec)
            page = doc[page_no - 1]
            rect = page.rect
            clip = fitz.Rect(
                rect.x0 + frac[0] * rect.width,
                rect.y0 + frac[1] * rect.height,
                rect.x0 + frac[2] * rect.width,
                rect.y0 + frac[3] * rect.height,
            )
            pix = page.get_pixmap(matrix=matrix, clip=clip, alpha=False)
            target = images_dir / f"{name}.png"
            pix.save(target)
            out["images"].append(str(target))  # type: ignore[index]

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
