from __future__ import annotations

from dataclasses import asdict, dataclass

from .analytics import TrendSummary, summarize_trend
from .alerts import build_alerts
from .io_utils import detect_marketplace_source, load_marketplace_listings, load_seller_catalog
from .matching_service import find_equivalent_listings, get_matcher_info
from .models import Alert, CompetitorListing, MatchCandidate, PriceRecommendation, SellerBook
from .monitoring import build_listing_history
from .pricing import recommend_price


@dataclass(slots=True)
class SkuInsight:
    book: SellerBook
    matches: list[tuple[CompetitorListing, MatchCandidate]]
    recommendation: PriceRecommendation
    alerts: list[Alert]
    trend: TrendSummary


def build_insights(
    prefer_scraped: bool = True,
    prefer_embeddings: bool = True,
    catalog_limit: int | None = None,
    listing_limit: int | None = None,
) -> list[SkuInsight]:
    catalog = load_seller_catalog(limit=catalog_limit)
    listings = load_marketplace_listings(prefer_scraped=prefer_scraped, limit=listing_limit)
    matched, _matcher_info = find_equivalent_listings(
        catalog,
        listings,
        prefer_embeddings=prefer_embeddings,
    )
    history = build_listing_history()

    insights: list[SkuInsight] = []
    for book in catalog:
        book_matches = matched[book.sku]
        matched_listings = [listing for listing, _candidate in book_matches]
        recommendation = recommend_price(book, matched_listings)
        alerts = build_alerts(book, matched_listings, recommendation)
        trend = summarize_trend(matched_listings, history)
        insights.append(
            SkuInsight(
                book=book,
                matches=book_matches,
                recommendation=recommendation,
                alerts=alerts,
                trend=trend,
            )
        )
    return insights


def get_data_source_label(prefer_scraped: bool = True) -> str:
    return detect_marketplace_source(prefer_scraped=prefer_scraped)


def get_matcher_label(prefer_embeddings: bool = True) -> str:
    return get_matcher_info(prefer_embeddings=prefer_embeddings).strategy


def insights_to_dict(insights: list[SkuInsight]) -> list[dict]:
    payload: list[dict] = []
    for insight in insights:
        payload.append(
            {
                "book": asdict(insight.book),
                "recommendation": asdict(insight.recommendation),
                "alerts": [asdict(alert) for alert in insight.alerts],
                "trend": asdict(insight.trend),
                "matches": [
                    {
                        "listing": asdict(listing),
                        "candidate": asdict(candidate),
                    }
                    for listing, candidate in insight.matches
                ],
            }
        )
    return payload
