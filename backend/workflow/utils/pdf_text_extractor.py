#!/usr/bin/env python3
"""Extract text from a PDF file and optionally save it to disk."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _extract_with_pypdf(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""

    reader = PdfReader(str(pdf_path))
    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    return "\n\n".join(page for page in pages if page)


def _extract_with_pypdf2(pdf_path: Path) -> str:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        return ""

    reader = PdfReader(str(pdf_path))
    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    return "\n\n".join(page for page in pages if page)


def _extract_with_pdftotext(pdf_path: Path) -> str:
    if shutil.which("pdftotext") is None:
        return ""

    result = subprocess.run(
        ["pdftotext", str(pdf_path), "-"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF using available backends."""
    extractors = (_extract_with_pypdf, _extract_with_pypdf2, _extract_with_pdftotext)
    for extractor in extractors:
        text = extractor(pdf_path)
        if text:
            return text

    raise RuntimeError(
        "No supported PDF extractor found. Install `pypdf` (recommended), "
        "`PyPDF2`, or ensure `pdftotext` is installed."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf_path", type=Path, help="Path to the input PDF file.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional output text file path. Prints to stdout when omitted.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_path: Path = args.pdf_path

    if not pdf_path.exists():
        print(f"Error: file not found: {pdf_path}", file=sys.stderr)
        return 1
    if pdf_path.suffix.lower() != ".pdf":
        print(f"Error: expected a .pdf file, got: {pdf_path.name}", file=sys.stderr)
        return 1

    try:
        text = extract_text_from_pdf(pdf_path)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"Error while reading PDF: {exc}", file=sys.stderr)
        return 3

    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"Text written to {args.output}")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
