from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .matcher import find_equivalent_listings as heuristic_find_equivalent_listings
from .models import CompetitorListing, MatchCandidate, SellerBook


EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@dataclass(slots=True)
class MatcherInfo:
    strategy: str
    detail: str


@lru_cache(maxsize=1)
def _load_embedding_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL_NAME, local_files_only=True)


def get_matcher_info(prefer_embeddings: bool = True) -> MatcherInfo:
    if prefer_embeddings:
        try:
            _load_embedding_model()

            return MatcherInfo(
                strategy="embedding",
                detail=f"SentenceTransformer model loaded ({EMBEDDING_MODEL_NAME})",
            )
        except Exception:
            pass
    return MatcherInfo(
        strategy="heuristic",
        detail="weighted metadata similarity matcher enabled",
    )


def _embedding_find_equivalent_listings(
    catalog: list[SellerBook],
    listings: list[CompetitorListing],
    threshold: float = 0.55,
) -> dict[str, list[tuple[CompetitorListing, MatchCandidate]]]:
    model = _load_embedding_model()
    matches: dict[str, list[tuple[CompetitorListing, MatchCandidate]]] = {book.sku: [] for book in catalog}

    book_texts = [
        " ".join(part for part in [book.canonical_title, book.subtitle, book.author, book.publisher, book.edition] if part)
        for book in catalog
    ]
    listing_texts = [
        " ".join(part for part in [listing.title, listing.author, listing.publisher, listing.edition, listing.format] if part)
        for listing in listings
    ]
    book_embeddings = model.encode(book_texts, normalize_embeddings=True)
    listing_embeddings = model.encode(listing_texts, normalize_embeddings=True)

    for book, book_embedding in zip(catalog, book_embeddings):
        for listing, listing_embedding in zip(listings, listing_embeddings):
            score = float(book_embedding @ listing_embedding)
            if score >= threshold:
                candidate = MatchCandidate(
                    sku=book.sku,
                    listing_id=listing.listing_id,
                    marketplace=listing.marketplace,
                    confidence=min(score, 1.0),
                    reasons=[f"SentenceTransformer cosine similarity ({score:.2f})"],
                )
                matches[book.sku].append((listing, candidate))
        matches[book.sku].sort(key=lambda pair: pair[1].confidence, reverse=True)
        matches[book.sku] = matches[book.sku][:3]
    return matches


def find_equivalent_listings(
    catalog: list[SellerBook],
    listings: list[CompetitorListing],
    threshold: float = 0.55,
    prefer_embeddings: bool = True,
) -> tuple[dict[str, list[tuple[CompetitorListing, MatchCandidate]]], MatcherInfo]:
    info = get_matcher_info(prefer_embeddings=prefer_embeddings)
    if info.strategy == "embedding":
        return _embedding_find_equivalent_listings(catalog, listings, threshold=threshold), info
    heuristic_matches = heuristic_find_equivalent_listings(catalog, listings, threshold=threshold)
    for sku in heuristic_matches:
        heuristic_matches[sku] = heuristic_matches[sku][:3]
    return heuristic_matches, info
