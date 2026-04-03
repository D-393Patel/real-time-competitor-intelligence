from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .io_utils import DATA_DIR, load_marketplace_listings
from .models import CompetitorListing


@dataclass(slots=True)
class SnapshotPoint:
    captured_at: str
    listing_id: str
    marketplace: str
    landed_price: float


def load_historical_snapshots() -> list[dict]:
    path = DATA_DIR / "marketplaces" / "historical_snapshots.json"
    return json.loads(path.read_text(encoding="utf-8"))


def build_listing_lookup() -> dict[str, CompetitorListing]:
    return {listing.listing_id: listing for listing in load_marketplace_listings()}


def build_listing_history() -> dict[str, list[SnapshotPoint]]:
    lookup = build_listing_lookup()
    snapshots = load_historical_snapshots()
    history: dict[str, list[SnapshotPoint]] = {}

    for snapshot in snapshots:
        captured_at = snapshot["captured_at"]
        for row in snapshot["listings"]:
            listing = lookup.get(row["listing_id"])
            if not listing:
                continue
            history.setdefault(row["listing_id"], []).append(
                SnapshotPoint(
                    captured_at=captured_at,
                    listing_id=row["listing_id"],
                    marketplace=row["marketplace"],
                    landed_price=row["price"] + row["shipping"],
                )
            )
    return history
