from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

from .models import CompetitorListing


ROOT = Path(__file__).resolve().parents[2]
RAW_MARKETPLACE_DIR = ROOT / "data" / "raw_marketplaces"
SNAPSHOT_DIR = ROOT / "data" / "marketplaces"


class StructuredListingParser(HTMLParser):
    def __init__(
        self,
        marketplace: str,
        record_tag: str,
        record_id_attr: str,
        field_map: dict[str, str],
    ) -> None:
        super().__init__()
        self.marketplace = marketplace
        self.record_tag = record_tag
        self.record_id_attr = record_id_attr
        self.field_map = field_map
        self.records: list[dict[str, str]] = []
        self.current_record: dict[str, str] | None = None
        self.current_field: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == self.record_tag and self.record_id_attr in attr_map:
            self.current_record = {"listing_id": attr_map.get(self.record_id_attr, "")}
            return

        if not self.current_record:
            return

        class_name = attr_map.get("class", "")
        for field_name, selector in self.field_map.items():
            if class_name == selector:
                self.current_field = field_name
                break

    def handle_data(self, data: str) -> None:
        if self.current_record is None or self.current_field is None:
            return
        existing = self.current_record.get(self.current_field, "")
        self.current_record[self.current_field] = f"{existing}{data}".strip()

    def handle_endtag(self, tag: str) -> None:
        self.current_field = None
        if tag == self.record_tag and self.current_record:
            self.records.append(self.current_record)
            self.current_record = None


SCRAPER_CONFIG = {
    "amazon_books": {
        "marketplace": "Amazon Books",
        "record_tag": "div",
        "record_id_attr": "data-listing-id",
        "field_map": {
            "title": "title",
            "author": "author",
            "isbn": "isbn",
            "edition": "edition",
            "publisher": "publisher",
            "format": "format",
            "price": "price",
            "shipping": "shipping",
            "seller_rating": "rating",
            "availability": "availability",
        },
    },
    "flipkart_books": {
        "marketplace": "Flipkart Books",
        "record_tag": "section",
        "record_id_attr": "data-listing-id",
        "field_map": {
            "title": "listing-title",
            "author": "listing-author",
            "isbn": "listing-isbn",
            "edition": "listing-edition",
            "publisher": "listing-publisher",
            "format": "listing-format",
            "price": "listing-price",
            "shipping": "listing-shipping",
            "seller_rating": "listing-rating",
            "availability": "listing-availability",
        },
    },
    "bookswagon": {
        "marketplace": "Bookswagon",
        "record_tag": "article",
        "record_id_attr": "data-id",
        "field_map": {
            "title": "book-title",
            "author": "book-author",
            "isbn": "book-isbn",
            "edition": "book-edition",
            "publisher": "book-publisher",
            "format": "book-format",
            "price": "book-price",
            "shipping": "book-shipping",
            "seller_rating": "book-rating",
            "availability": "book-availability",
        },
    },
}


def parse_marketplace_html(source_name: str, html_text: str, captured_at: str | None = None) -> list[CompetitorListing]:
    config = SCRAPER_CONFIG[source_name]
    parser = StructuredListingParser(
        marketplace=config["marketplace"],
        record_tag=config["record_tag"],
        record_id_attr=config["record_id_attr"],
        field_map=config["field_map"],
    )
    parser.feed(html_text)
    timestamp = captured_at or datetime.now().astimezone().isoformat(timespec="seconds")

    listings: list[CompetitorListing] = []
    for row in parser.records:
        if "listing_id" in row and any(key != "listing_id" for key in row):
            listings.append(
                CompetitorListing(
                    marketplace=config["marketplace"],
                    listing_id=row.get("listing_id", ""),
                    title=row.get("title", ""),
                    author=row.get("author", ""),
                    isbn=row.get("isbn", ""),
                    edition=row.get("edition", ""),
                    publisher=row.get("publisher", ""),
                    format=row.get("format", ""),
                    price=float(row.get("price", "0") or 0.0),
                    shipping=float(row.get("shipping", "0") or 0.0),
                    seller_rating=float(row.get("seller_rating", "0") or 0.0),
                    availability=row.get("availability", "unknown"),
                    captured_at=timestamp,
                )
            )
    return listings


def scrape_sample_marketplaces(captured_at: str | None = None) -> dict[str, list[CompetitorListing]]:
    scraped: dict[str, list[CompetitorListing]] = {}
    for source_name in SCRAPER_CONFIG:
        html_path = RAW_MARKETPLACE_DIR / f"{source_name}.html"
        html_text = html_path.read_text(encoding="utf-8")
        scraped[source_name] = parse_marketplace_html(source_name, html_text, captured_at=captured_at)
    return scraped


def write_scraped_snapshots(captured_at: str | None = None) -> list[Path]:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for source_name, listings in scrape_sample_marketplaces(captured_at=captured_at).items():
        path = SNAPSHOT_DIR / f"{source_name}_scraped.json"
        path.write_text(json.dumps([asdict(item) for item in listings], indent=2), encoding="utf-8")
        paths.append(path)
    return paths
