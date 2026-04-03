from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev

from .models import CompetitorListing
from .monitoring import SnapshotPoint


@dataclass(slots=True)
class TrendSummary:
    floor_series: list[tuple[str, float]]
    latest_floor: float
    earliest_floor: float
    floor_change: float
    volatility: float
    trend_label: str


def summarize_trend(
    matched_listings: list[CompetitorListing],
    history: dict[str, list[SnapshotPoint]],
) -> TrendSummary:
    timeline: dict[str, list[float]] = {}

    for listing in matched_listings:
        for point in history.get(listing.listing_id, []):
            timeline.setdefault(point.captured_at, []).append(point.landed_price)

    floor_series = sorted((timestamp, min(prices)) for timestamp, prices in timeline.items())
    if not floor_series:
        return TrendSummary([], 0.0, 0.0, 0.0, 0.0, "stable")

    floors = [price for _timestamp, price in floor_series]
    earliest = floors[0]
    latest = floors[-1]
    change = round(latest - earliest, 2)
    volatility = round(pstdev(floors), 2) if len(floors) > 1 else 0.0

    if change <= -10:
        label = "falling"
    elif change >= 10:
        label = "rising"
    else:
        label = "stable"

    return TrendSummary(
        floor_series=floor_series,
        latest_floor=latest,
        earliest_floor=earliest,
        floor_change=change,
        volatility=volatility,
        trend_label=label,
    )


def average_competitor_price(matched_listings: list[CompetitorListing]) -> float:
    if not matched_listings:
        return 0.0
    return round(mean(listing.landed_price for listing in matched_listings), 2)
