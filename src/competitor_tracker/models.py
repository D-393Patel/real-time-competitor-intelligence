from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SellerBook:
    sku: str
    canonical_title: str
    subtitle: str
    author: str
    isbn_13: str
    isbn_10: str
    edition: str
    publisher: str
    format: str
    cost_price: float
    shipping_cost: float
    marketplace_fee_pct: float
    current_price: float
    target_margin_pct: float


@dataclass(slots=True)
class CompetitorListing:
    marketplace: str
    listing_id: str
    title: str
    author: str
    isbn: str
    edition: str
    publisher: str
    format: str
    price: float
    shipping: float
    seller_rating: float
    availability: str
    captured_at: str

    @property
    def landed_price(self) -> float:
        return self.price + self.shipping


@dataclass(slots=True)
class MatchCandidate:
    sku: str
    listing_id: str
    marketplace: str
    confidence: float
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PriceRecommendation:
    sku: str
    action: str
    recommended_price: float
    expected_margin_pct: float
    competitor_gap: float
    rationale: list[str]


@dataclass(slots=True)
class Alert:
    severity: str
    sku: str
    title: str
    message: str
