from __future__ import annotations

from .models import CompetitorListing, PriceRecommendation, SellerBook


def compute_margin_pct(book: SellerBook, price: float) -> float:
    total_cost = book.cost_price + book.shipping_cost + (price * book.marketplace_fee_pct)
    return (price - total_cost) / price


def recommend_price(book: SellerBook, listings: list[CompetitorListing]) -> PriceRecommendation:
    if not listings:
        current_margin = compute_margin_pct(book, book.current_price)
        return PriceRecommendation(
            sku=book.sku,
            action="hold",
            recommended_price=round(book.current_price, 2),
            expected_margin_pct=round(current_margin, 4),
            competitor_gap=0.0,
            rationale=["No matched competitor listings available"],
        )

    cheapest = min(listings, key=lambda item: item.landed_price)
    market_floor = cheapest.landed_price
    profit_guardrail = (
        book.cost_price + book.shipping_cost
    ) / (1 - book.marketplace_fee_pct - book.target_margin_pct)
    stretch_price = market_floor + 9.0

    if book.current_price > market_floor + 20:
        action = "lower"
        recommended = max(profit_guardrail, market_floor - 1)
        rationale = [
            f"Competitor floor at {market_floor:.2f} is materially below current price",
            "Lower price while protecting target margin",
        ]
    elif book.current_price < market_floor - 12 and compute_margin_pct(book, stretch_price) >= book.target_margin_pct:
        action = "raise"
        recommended = stretch_price
        rationale = [
            "Current price is well below the nearest competitor",
            "There is room to expand margin without losing price competitiveness",
        ]
    else:
        action = "hold"
        recommended = max(book.current_price, profit_guardrail)
        rationale = [
            "Current pricing is competitive",
            "Maintain stable market position and protected margin",
        ]

    recommended = round(recommended, 2)
    return PriceRecommendation(
        sku=book.sku,
        action=action,
        recommended_price=recommended,
        expected_margin_pct=round(compute_margin_pct(book, recommended), 4),
        competitor_gap=round(book.current_price - market_floor, 2),
        rationale=rationale,
    )
