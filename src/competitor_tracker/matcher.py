from __future__ import annotations

from .models import CompetitorListing, MatchCandidate, SellerBook
from .normalization import (
    normalize_edition,
    normalize_format,
    normalize_isbn,
    normalize_text,
    similarity,
    token_overlap,
)


def score_listing_match(book: SellerBook, listing: CompetitorListing) -> MatchCandidate:
    reasons: list[str] = []
    score = 0.0

    book_isbns = {normalize_isbn(book.isbn_10), normalize_isbn(book.isbn_13)}
    listing_isbn = normalize_isbn(listing.isbn)
    if listing_isbn and listing_isbn in book_isbns:
        score += 0.45
        reasons.append("Exact ISBN match")

    title_similarity = max(
        similarity(book.canonical_title, listing.title),
        similarity(f"{book.canonical_title} {book.subtitle}".strip(), listing.title),
        token_overlap(f"{book.canonical_title} {book.subtitle}".strip(), listing.title),
    )
    score += title_similarity * 0.27
    if title_similarity >= 0.7:
        reasons.append(f"Strong title similarity ({title_similarity:.2f})")

    normalized_title = normalize_text(listing.title)
    normalized_canonical = normalize_text(book.canonical_title)
    if normalized_canonical and normalized_canonical in normalized_title:
        score += 0.07
        reasons.append("Canonical title contained in competitor listing")

    author_similarity = max(similarity(book.author, listing.author), token_overlap(book.author, listing.author))
    score += author_similarity * 0.15
    if author_similarity >= 0.6:
        reasons.append(f"Author similarity ({author_similarity:.2f})")

    publisher_similarity = similarity(book.publisher, listing.publisher)
    score += publisher_similarity * 0.08
    if publisher_similarity >= 0.55:
        reasons.append(f"Publisher similarity ({publisher_similarity:.2f})")

    if normalize_format(book.format) == normalize_format(listing.format):
        score += 0.03
        reasons.append("Format aligned")

    if normalize_edition(book.edition) == normalize_edition(listing.edition):
        score += 0.02
        reasons.append("Edition aligned")

    return MatchCandidate(
        sku=book.sku,
        listing_id=listing.listing_id,
        marketplace=listing.marketplace,
        confidence=min(score, 1.0),
        reasons=reasons,
    )


def find_equivalent_listings(
    catalog: list[SellerBook],
    listings: list[CompetitorListing],
    threshold: float = 0.55,
) -> dict[str, list[tuple[CompetitorListing, MatchCandidate]]]:
    matches: dict[str, list[tuple[CompetitorListing, MatchCandidate]]] = {book.sku: [] for book in catalog}
    for book in catalog:
        for listing in listings:
            candidate = score_listing_match(book, listing)
            if candidate.confidence >= threshold:
                matches[book.sku].append((listing, candidate))
        matches[book.sku].sort(key=lambda pair: pair[1].confidence, reverse=True)
    return matches
