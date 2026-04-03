from __future__ import annotations

import json
from pathlib import Path

from .models import CompetitorListing, SellerBook


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"


def _load_listing_files(paths: list[Path], limit: int | None = None) -> list[CompetitorListing]:
    listings: list[CompetitorListing] = []
    per_file_limit = None
    if limit is not None and paths:
        per_file_limit = max(limit // len(paths), 1)
        if limit % len(paths):
            per_file_limit += 1
    for path in paths:
        rows = json.loads(path.read_text(encoding="utf-8"))
        if per_file_limit is not None:
            rows = rows[:per_file_limit]
        listings.extend(CompetitorListing(**row) for row in rows)
        if limit is not None and len(listings) >= limit:
            return listings[:limit]
    return listings


def load_seller_catalog(limit: int | None = None) -> list[SellerBook]:
    path = DATA_DIR / "inventory" / "seller_catalog.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    books = [SellerBook(**row) for row in rows]
    return books[:limit] if limit is not None else books


def load_marketplace_listings(prefer_scraped: bool = True, limit: int | None = None) -> list[CompetitorListing]:
    marketplace_dir = DATA_DIR / "marketplaces"
    scraped_paths = sorted(marketplace_dir.glob("*_scraped.json"))
    curated_paths = [
        path
        for path in sorted(marketplace_dir.glob("*.json"))
        if path.name != "historical_snapshots.json" and not path.name.endswith("_scraped.json")
    ]

    if prefer_scraped and scraped_paths:
        return _load_listing_files(scraped_paths, limit=limit)
    return _load_listing_files(curated_paths, limit=limit)


def detect_marketplace_source(prefer_scraped: bool = True) -> str:
    marketplace_dir = DATA_DIR / "marketplaces"
    scraped_paths = list(marketplace_dir.glob("*_scraped.json"))
    if prefer_scraped and scraped_paths:
        return "scraped snapshots"
    return "curated sample feeds"
