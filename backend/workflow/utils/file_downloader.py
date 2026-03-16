#!/usr/bin/env python3
"""Download files from the internet and save them to the output folder."""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


def download_file(url: str, output_dir: Path | None = None, filename: str | None = None) -> Path:
    """
    Download a file from a given URL and save it to the specified directory.
    
    Args:
        url: The URL of the file to download
        output_dir: Directory to save the file (defaults to workflow/output/)
        filename: Custom filename (defaults to the filename from URL)
    
    Returns:
        Path: Path to the downloaded file
    
    Raises:
        ValueError: If URL is invalid
        urllib.error.URLError: If download fails
    """
    # Set default output directory
    if output_dir is None:
        output_dir = Path(__file__).resolve().parent.parent / "output"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine filename
    if filename is None:
        parsed_url = urlparse(url)
        filename = Path(parsed_url.path).name
        if not filename:
            filename = "downloaded_file"
    
    output_path = output_dir / filename
    
    # Download the file
    print(f"Downloading from: {url}")
    print(f"Saving to: {output_path}")
    
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"✓ Download completed: {output_path}")
        return output_path
    except Exception as e:
        print(f"✗ Download failed: {e}", file=sys.stderr)
        raise


def main():
    """CLI entry point for the file downloader utility."""
    parser = argparse.ArgumentParser(
        description="Download files from the internet to workflow/output folder"
    )
    parser.add_argument(
        "url",
        help="URL of the file to download"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output directory (default: workflow/output/)"
    )
    parser.add_argument(
        "-f", "--filename",
        help="Custom filename for the downloaded file"
    )
    
    args = parser.parse_args()
    
    try:
        downloaded_path = download_file(args.url, args.output, args.filename)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
