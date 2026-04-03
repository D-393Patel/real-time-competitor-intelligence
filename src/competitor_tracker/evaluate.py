from __future__ import annotations

import json
from pathlib import Path

from .io_utils import DATA_DIR, detect_marketplace_source, load_marketplace_listings, load_seller_catalog
from .monitoring import build_listing_history, load_historical_snapshots
from .pipeline import build_insights, get_matcher_label


ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports"


def collect_metrics(
    prefer_embeddings: bool = True,
    catalog_limit: int | None = None,
    listing_limit: int | None = None,
) -> dict:
    catalog = load_seller_catalog(limit=catalog_limit)
    listings = load_marketplace_listings(limit=listing_limit)
    insights = build_insights(
        prefer_embeddings=prefer_embeddings,
        catalog_limit=catalog_limit,
        listing_limit=listing_limit,
    )
    history = build_listing_history()
    snapshots = load_historical_snapshots()

    total_matches = sum(len(insight.matches) for insight in insights)
    total_alerts = sum(len(insight.alerts) for insight in insights)
    raise_count = sum(1 for insight in insights if insight.recommendation.action == "raise")
    lower_count = sum(1 for insight in insights if insight.recommendation.action == "lower")
    hold_count = sum(1 for insight in insights if insight.recommendation.action == "hold")
    avg_expected_margin = round(
        sum(insight.recommendation.expected_margin_pct for insight in insights) / max(len(insights), 1),
        4,
    )
    historical_observations = sum(len(points) for points in history.values())

    return {
        "seller_skus_monitored": len(catalog),
        "competitor_listings_loaded": len(listings),
        "equivalent_matches_detected": total_matches,
        "average_matches_per_sku": round(total_matches / max(len(catalog), 1), 2),
        "pricing_actions": {
            "raise": raise_count,
            "lower": lower_count,
            "hold": hold_count,
        },
        "alerts_generated": total_alerts,
        "average_expected_margin_pct": avg_expected_margin,
        "historical_snapshots_replayed": len(snapshots),
        "historical_price_observations": historical_observations,
        "marketplace_input_source": detect_marketplace_source(),
        "matcher_strategy": get_matcher_label(),
        "marketplaces_covered": sorted({listing.marketplace for listing in listings}),
    }


def write_metrics_report() -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / "project_metrics.json"
    path.write_text(json.dumps(collect_metrics(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_metrics_report()
    metrics = json.loads(path.read_text(encoding="utf-8"))
    print("Project metrics summary")
    print("=" * 28)
    for key, value in metrics.items():
        print(f"{key}: {value}")
    print(f"\nMetrics JSON: {path}")


if __name__ == "__main__":
    main()
