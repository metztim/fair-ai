#!/usr/bin/env python3
"""
Archive sources to the Wayback Machine.

Reads sources.yaml, finds sources without archive URLs, and submits them
to the Internet Archive's Wayback Machine.

Usage:
    python archive-sources.py <path-to-sources.yaml>
    python archive-sources.py research/investigations/ai-bubble-valuation/sources.yaml

Rate limiting: 5 seconds between requests to avoid blocking.
"""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml

WAYBACK_SAVE_URL = "https://web.archive.org/save/"
WAYBACK_CHECK_URL = "https://web.archive.org/web/"
RATE_LIMIT_SECONDS = 5


def load_sources(yaml_path: Path) -> dict:
    """Load sources.yaml file."""
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)


def save_sources(yaml_path: Path, data: dict) -> None:
    """Save sources.yaml file."""
    with open(yaml_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def archive_url(url: str) -> tuple[str | None, str | None]:
    """
    Submit URL to Wayback Machine and return archive URL.

    Returns:
        Tuple of (archive_url, archive_date) or (None, None) on failure.
    """
    try:
        # Submit to Wayback Machine
        save_url = f"{WAYBACK_SAVE_URL}{url}"
        response = requests.get(save_url, timeout=60)

        if response.status_code == 200:
            # Try to extract the archive URL from response headers or URL
            # The Wayback Machine redirects to the archived version
            if "location" in response.headers:
                archive_url = response.headers["location"]
            elif WAYBACK_CHECK_URL in response.url:
                archive_url = response.url
            else:
                # Construct expected archive URL
                today = datetime.now().strftime("%Y%m%d")
                archive_url = f"{WAYBACK_CHECK_URL}{today}/{url}"

            archive_date = datetime.now().strftime("%Y-%m-%d")
            return archive_url, archive_date
        else:
            print(f"  Failed with status {response.status_code}")
            return None, None

    except requests.exceptions.Timeout:
        print("  Timeout - Wayback Machine may be slow")
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"  Request error: {e}")
        return None, None


def main():
    parser = argparse.ArgumentParser(description="Archive sources to Wayback Machine")
    parser.add_argument("sources_yaml", type=Path, help="Path to sources.yaml file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be archived without doing it")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of sources to archive")
    args = parser.parse_args()

    if not args.sources_yaml.exists():
        print(f"Error: {args.sources_yaml} not found")
        sys.exit(1)

    print(f"Loading {args.sources_yaml}...")
    data = load_sources(args.sources_yaml)

    sources = data.get("sources", [])
    if not sources:
        print("No sources found in file")
        sys.exit(0)

    # Find sources that need archiving
    to_archive = []
    for source in sources:
        archive = source.get("archive", {})
        if archive.get("wayback") is None:
            to_archive.append(source)

    print(f"Found {len(to_archive)} sources without archives (of {len(sources)} total)")

    if args.limit:
        to_archive = to_archive[:args.limit]
        print(f"Limiting to {args.limit} sources")

    if args.dry_run:
        print("\nDry run - would archive:")
        for source in to_archive:
            print(f"  - {source.get('id')}: {source.get('url')}")
        sys.exit(0)

    if not to_archive:
        print("All sources already archived!")
        sys.exit(0)

    # Archive each source
    archived_count = 0
    failed_count = 0

    print(f"\nArchiving {len(to_archive)} sources (rate limited to {RATE_LIMIT_SECONDS}s between requests)...\n")

    for i, source in enumerate(to_archive):
        source_id = source.get("id", "unknown")
        url = source.get("url")

        print(f"[{i+1}/{len(to_archive)}] {source_id}")
        print(f"  URL: {url}")

        archive_url_result, archive_date = archive_url(url)

        if archive_url_result:
            print(f"  Archived: {archive_url_result}")

            # Update source in data
            if "archive" not in source:
                source["archive"] = {}
            source["archive"]["wayback"] = archive_url_result
            source["archive"]["wayback_date"] = archive_date
            archived_count += 1
        else:
            print("  Failed to archive")
            failed_count += 1

        # Rate limit
        if i < len(to_archive) - 1:
            print(f"  Waiting {RATE_LIMIT_SECONDS}s...")
            time.sleep(RATE_LIMIT_SECONDS)

        print()

    # Update metadata
    if "metadata" in data:
        data["metadata"]["archived_count"] = sum(
            1 for s in data["sources"]
            if s.get("archive", {}).get("wayback") is not None
        )
        data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    # Save updated file
    print(f"Saving {args.sources_yaml}...")
    save_sources(args.sources_yaml, data)

    print(f"\nComplete!")
    print(f"  Archived: {archived_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total archived in file: {data['metadata'].get('archived_count', 'unknown')}")


if __name__ == "__main__":
    main()
