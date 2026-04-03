from __future__ import annotations

from .models import Alert, CompetitorListing, PriceRecommendation, SellerBook
from .pricing import compute_margin_pct


def build_alerts(
    book: SellerBook,
    listings: list[CompetitorListing],
    recommendation: PriceRecommendation,
) -> list[Alert]:
    alerts: list[Alert] = []
    if not listings:
        alerts.append(
            Alert(
                severity="medium",
                sku=book.sku,
                title="Visibility gap",
                message="No equivalent competitor listings were detected for this monitoring cycle.",
            )
        )
        return alerts

    cheapest = min(listings, key=lambda item: item.landed_price)
    current_margin = compute_margin_pct(book, book.current_price)

    if cheapest.landed_price < book.current_price - 25:
        alerts.append(
            Alert(
                severity="high",
                sku=book.sku,
                title="Aggressive competitor pricing",
                message=f"{cheapest.marketplace} is undercutting by {book.current_price - cheapest.landed_price:.2f}.",
            )
        )

    if current_margin < book.target_margin_pct:
        alerts.append(
            Alert(
                severity="high",
                sku=book.sku,
                title="Margin risk",
                message=f"Current margin {current_margin:.1%} is below the target margin of {book.target_margin_pct:.1%}.",
            )
        )

    if recommendation.action == "raise":
        alerts.append(
            Alert(
                severity="low",
                sku=book.sku,
                title="Margin expansion opportunity",
                message="Market headroom suggests price can be increased without losing competitiveness.",
            )
        )

    return alerts
