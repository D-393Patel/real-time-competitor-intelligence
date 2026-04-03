from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
INVENTORY_PATH = DATA_DIR / "inventory" / "seller_catalog.json"
MARKETPLACE_DIR = DATA_DIR / "marketplaces"
RAW_DIR = DATA_DIR / "raw_marketplaces"


BASE_BOOKS = [
    {
        "sku": "BK-ATOMIC-HABITS-PB",
        "canonical_title": "Atomic Habits",
        "subtitle": "Tiny Changes, Remarkable Results",
        "author": "James Clear",
        "isbn_13": "9781847941831",
        "isbn_10": "1847941834",
        "edition": "Paperback",
        "publisher": "Penguin Random House",
        "format": "paperback",
        "cost_price": 180.0,
        "shipping_cost": 35.0,
        "marketplace_fee_pct": 0.12,
        "current_price": 349.0,
        "target_margin_pct": 0.24,
    },
    {
        "sku": "BK-DEEP-WORK-PB",
        "canonical_title": "Deep Work",
        "subtitle": "Rules for Focused Success in a Distracted World",
        "author": "Cal Newport",
        "isbn_13": "9781455586691",
        "isbn_10": "1455586692",
        "edition": "Paperback",
        "publisher": "Grand Central Publishing",
        "format": "paperback",
        "cost_price": 165.0,
        "shipping_cost": 35.0,
        "marketplace_fee_pct": 0.12,
        "current_price": 325.0,
        "target_margin_pct": 0.22,
    },
    {
        "sku": "BK-PSY-MONEY-HC",
        "canonical_title": "The Psychology of Money",
        "subtitle": "Timeless lessons on wealth, greed, and happiness",
        "author": "Morgan Housel",
        "isbn_13": "9780857197689",
        "isbn_10": "0857197681",
        "edition": "Hardcover",
        "publisher": "Harriman House",
        "format": "hardcover",
        "cost_price": 250.0,
        "shipping_cost": 40.0,
        "marketplace_fee_pct": 0.13,
        "current_price": 499.0,
        "target_margin_pct": 0.25,
    },
]

TITLE_PREFIXES = [
    "Adaptive",
    "Data-Driven",
    "Digital",
    "Modern",
    "Strategic",
    "Competitive",
    "Practical",
    "Smart",
    "Advanced",
    "Lean",
]
TITLE_TOPICS = [
    "Pricing",
    "Selling",
    "Catalog",
    "Commerce",
    "Growth",
    "Analytics",
    "Optimization",
    "Strategy",
    "Operations",
    "Retail",
    "Market",
    "Revenue",
]
TITLE_SUFFIXES = [
    "Playbook",
    "Handbook",
    "Blueprint",
    "Framework",
    "Guide",
    "Manual",
    "System",
    "Method",
    "Toolkit",
    "Engine",
]
AUTHORS_FIRST = [
    "Aarav",
    "Diya",
    "Ishaan",
    "Kavya",
    "Mira",
    "Rohan",
    "Saanvi",
    "Vihaan",
    "Anika",
    "Dev",
]
AUTHORS_LAST = [
    "Kapoor",
    "Reddy",
    "Mehta",
    "Sharma",
    "Iyer",
    "Verma",
    "Nair",
    "Gupta",
    "Patel",
    "Rao",
]
PUBLISHERS = [
    "Penguin Business",
    "Insight Press",
    "MarketMind Publications",
    "RetailWorks Media",
    "Velocity House",
    "SmartSeller Books",
]


def synthetic_book(index: int) -> dict:
    prefix = TITLE_PREFIXES[index % len(TITLE_PREFIXES)]
    topic = TITLE_TOPICS[(index // len(TITLE_PREFIXES)) % len(TITLE_TOPICS)]
    suffix = TITLE_SUFFIXES[(index // (len(TITLE_PREFIXES) * 2)) % len(TITLE_SUFFIXES)]
    first = AUTHORS_FIRST[index % len(AUTHORS_FIRST)]
    last = AUTHORS_LAST[(index // len(AUTHORS_FIRST)) % len(AUTHORS_LAST)]
    hardback = index % 5 == 0
    fmt = "hardcover" if hardback else "paperback"
    edition = "Hardcover" if hardback else "Paperback"
    isbn_num = 9781000000000 + index
    isbn13 = str(isbn_num)
    isbn10 = str(1000000000 + index)[-10:]
    cost_price = 150.0 + (index % 9) * 18.0 + (25.0 if hardback else 0.0)
    shipping_cost = 35.0 + (5.0 if hardback else 0.0)
    fee_pct = 0.12 + (0.01 if hardback else 0.0)
    current_price = round(cost_price * 1.82 + shipping_cost + (index % 6) * 7.0, 2)
    target_margin = 0.22 + ((index % 4) * 0.01)
    book_id = index + 1

    return {
        "sku": f"BK-SYN-{book_id:03d}",
        "canonical_title": f"{prefix} {topic} {suffix}",
        "subtitle": f"A practical system for {topic.lower()} performance",
        "author": f"{first} {last}",
        "isbn_13": isbn13,
        "isbn_10": isbn10,
        "edition": edition,
        "publisher": PUBLISHERS[index % len(PUBLISHERS)],
        "format": fmt,
        "cost_price": round(cost_price, 2),
        "shipping_cost": round(shipping_cost, 2),
        "marketplace_fee_pct": round(fee_pct, 2),
        "current_price": round(current_price, 2),
        "target_margin_pct": round(target_margin, 2),
    }


def build_catalog(total_skus: int = 1000) -> list[dict]:
    synthetic_needed = max(total_skus - len(BASE_BOOKS), 0)
    return BASE_BOOKS + [synthetic_book(index) for index in range(synthetic_needed)]


def marketplace_variants(book: dict, market: str, idx: int) -> dict:
    preserved = {
        ("BK-ATOMIC-HABITS-PB", "Amazon Books"): {
            "listing_id": "AMZ-1001",
            "title": "Atomic Habits: Tiny Changes, Remarkable Results",
            "author": "James Clear",
            "isbn": "9781847941831",
            "edition": "Paperback",
            "publisher": "Penguin Random House UK",
            "format": "Paperback",
            "price": 339.0,
            "shipping": 0.0,
            "seller_rating": 4.8,
            "availability": "in_stock",
        },
        ("BK-ATOMIC-HABITS-PB", "Flipkart Books"): {
            "listing_id": "FLP-2001",
            "title": "Atomic Habits",
            "author": "J. Clear",
            "isbn": "1847941834",
            "edition": "1st Paperback Edition",
            "publisher": "Penguin",
            "format": "paper back",
            "price": 345.0,
            "shipping": 20.0,
            "seller_rating": 4.5,
            "availability": "in_stock",
        },
        ("BK-ATOMIC-HABITS-PB", "Bookswagon"): {
            "listing_id": "BW-3001",
            "title": "Atomic Habits (Tiny Changes, Remarkable Results)",
            "author": "James Clear",
            "isbn": "",
            "edition": "Paperback",
            "publisher": "Random House Business",
            "format": "paperback",
            "price": 329.0,
            "shipping": 30.0,
            "seller_rating": 4.3,
            "availability": "in_stock",
        },
        ("BK-DEEP-WORK-PB", "Amazon Books"): {
            "listing_id": "AMZ-1002",
            "title": "Deep Work",
            "author": "Cal Newport",
            "isbn": "9781455586691",
            "edition": "Paperback",
            "publisher": "Grand Central Publishing",
            "format": "Paperback",
            "price": 349.0,
            "shipping": 0.0,
            "seller_rating": 4.7,
            "availability": "in_stock",
        },
        ("BK-DEEP-WORK-PB", "Flipkart Books"): {
            "listing_id": "FLP-2002",
            "title": "Deep Work: Rules for Focused Success in a Distracted World",
            "author": "Calvin Newport",
            "isbn": "",
            "edition": "Paperback",
            "publisher": "Grand Central",
            "format": "PB",
            "price": 338.0,
            "shipping": 25.0,
            "seller_rating": 4.4,
            "availability": "limited_stock",
        },
        ("BK-DEEP-WORK-PB", "Bookswagon"): {
            "listing_id": "BW-3002",
            "title": "Deep Work",
            "author": "Cal Newport",
            "isbn": "1455586692",
            "edition": "Paperback",
            "publisher": "Grand Central Publishing",
            "format": "paperback",
            "price": 356.0,
            "shipping": 0.0,
            "seller_rating": 4.2,
            "availability": "in_stock",
        },
        ("BK-PSY-MONEY-HC", "Amazon Books"): {
            "listing_id": "AMZ-1003",
            "title": "Psychology of Money",
            "author": "Morgan Housel",
            "isbn": "9780857197689",
            "edition": "Hardcover",
            "publisher": "Harriman House",
            "format": "Hardcover",
            "price": 449.0,
            "shipping": 0.0,
            "seller_rating": 4.6,
            "availability": "in_stock",
        },
        ("BK-PSY-MONEY-HC", "Flipkart Books"): {
            "listing_id": "FLP-2003",
            "title": "The Psychology of Money: Timeless lessons on wealth, greed, and happiness",
            "author": "Morgan Housel",
            "isbn": "",
            "edition": "Hard Cover",
            "publisher": "Harriman",
            "format": "Hard Cover",
            "price": 525.0,
            "shipping": 0.0,
            "seller_rating": 4.7,
            "availability": "in_stock",
        },
        ("BK-PSY-MONEY-HC", "Bookswagon"): {
            "listing_id": "BW-3003",
            "title": "Psychology of Money",
            "author": "M. Housel",
            "isbn": "0857197681",
            "edition": "Hardcover Special Edition",
            "publisher": "Harriman House",
            "format": "Hardcover",
            "price": 469.0,
            "shipping": 35.0,
            "seller_rating": 4.4,
            "availability": "in_stock",
        },
    }
    if (book["sku"], market) in preserved:
        return {
            "marketplace": market,
            **preserved[(book["sku"], market)],
            "captured_at": "2026-04-02T10:00:00+05:30",
        }

    bucket = idx % 3
    if bucket == 0:
        amazon_price = round(book["current_price"] - 14, 2)
        flipkart_price = round(book["current_price"] - 6, 2)
        bookswagon_price = round(book["current_price"] - 10, 2)
    elif bucket == 1:
        amazon_price = round(book["current_price"] + 18, 2)
        flipkart_price = round(book["current_price"] + 26, 2)
        bookswagon_price = round(book["current_price"] + 14, 2)
    else:
        amazon_price = round(book["current_price"] + 4, 2)
        flipkart_price = round(book["current_price"] + 6, 2)
        bookswagon_price = round(book["current_price"] - 2, 2)

    if market == "Amazon Books":
        return {
            "marketplace": market,
            "listing_id": f"AMZ-{1000 + idx}",
            "title": f"{book['canonical_title']}: {book['subtitle']}" if idx % 4 != 0 else book["canonical_title"],
            "author": book["author"],
            "isbn": book["isbn_13"],
            "edition": book["edition"],
            "publisher": book["publisher"],
            "format": book["format"].title(),
            "price": amazon_price,
            "shipping": 0.0,
            "seller_rating": round(4.2 + (idx % 7) * 0.1, 1),
            "availability": "in_stock",
            "captured_at": "2026-04-02T10:00:00+05:30",
        }
    if market == "Flipkart Books":
        author_parts = book["author"].split()
        short_author = f"{author_parts[0][0]}. {author_parts[-1]}" if len(author_parts) > 1 else book["author"]
        return {
            "marketplace": market,
            "listing_id": f"FLP-{2000 + idx}",
            "title": book["canonical_title"] if idx % 3 else f"{book['canonical_title']}: {book['subtitle']}",
            "author": short_author,
            "isbn": book["isbn_10"] if idx % 2 == 0 else "",
            "edition": f"1st {book['edition']} Edition" if book["edition"] == "Paperback" else "Hard Cover",
            "publisher": book["publisher"].split()[0],
            "format": "PB" if book["format"] == "paperback" else "Hard Cover",
            "price": flipkart_price,
            "shipping": 20.0 if book["format"] == "paperback" else 0.0,
            "seller_rating": round(4.1 + (idx % 6) * 0.1, 1),
            "availability": "limited_stock" if idx % 5 == 0 else "in_stock",
            "captured_at": "2026-04-02T10:00:00+05:30",
        }
    return {
        "marketplace": market,
        "listing_id": f"BW-{3000 + idx}",
        "title": f"{book['canonical_title']} ({book['subtitle']})" if idx % 4 == 0 else book["canonical_title"],
        "author": book["author"] if idx % 3 else f"{book['author'][0]}. {book['author'].split()[-1]}",
        "isbn": book["isbn_10"] if idx % 2 else "",
        "edition": book["edition"] if book["format"] == "paperback" else "Hardcover Special Edition",
        "publisher": book["publisher"],
        "format": book["format"],
        "price": bookswagon_price,
        "shipping": 30.0 if book["format"] == "paperback" else 35.0,
        "seller_rating": round(4.0 + (idx % 5) * 0.1, 1),
        "availability": "in_stock",
        "captured_at": "2026-04-02T10:00:00+05:30",
    }


def build_marketplaces(catalog: list[dict]) -> dict[str, list[dict]]:
    markets = {
        "amazon_books": [],
        "flipkart_books": [],
        "bookswagon": [],
    }
    for idx, book in enumerate(catalog, start=1):
        markets["amazon_books"].append(marketplace_variants(book, "Amazon Books", idx))
        markets["flipkart_books"].append(marketplace_variants(book, "Flipkart Books", idx))
        markets["bookswagon"].append(marketplace_variants(book, "Bookswagon", idx))
    return markets


def build_historical_snapshots(marketplaces: dict[str, list[dict]], snapshot_count: int = 14) -> list[dict]:
    start = datetime(2026, 3, 31, 8, 0, tzinfo=timezone(timedelta(hours=5, minutes=30)))
    all_listings = [item for items in marketplaces.values() for item in items]
    snapshots = []
    for snap_idx in range(snapshot_count):
        captured_at = (start + timedelta(minutes=30 * snap_idx)).isoformat()
        rows = []
        for listing_idx, listing in enumerate(all_listings):
            preserved_adjustments = {
                "AMZ-1001": [20, 18, 16, 14, 12, 10, 8, 6, 5, 4, 3, 2, 1, 0],
                "FLP-2001": [24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 3, 1, 0],
                "BW-3001": [18, 16, 15, 14, 12, 10, 8, 6, 5, 4, 3, 2, 1, 0],
                "AMZ-1002": [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
                "FLP-2002": [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3],
                "BW-3002": [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1],
                "AMZ-1003": [52, 48, 44, 40, 36, 32, 28, 24, 20, 16, 12, 8, 4, 0],
                "FLP-2003": [26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 0],
                "BW-3003": [30, 27, 24, 21, 18, 15, 12, 10, 8, 6, 4, 3, 1, 0],
            }
            if listing["listing_id"] in preserved_adjustments:
                adjustment = preserved_adjustments[listing["listing_id"]][snap_idx]
            else:
                trend_bucket = listing_idx % 3
                if trend_bucket == 0:
                    adjustment = (snapshot_count - snap_idx - 1) * 4
                elif trend_bucket == 1:
                    adjustment = (snap_idx - (snapshot_count // 2)) * 2
                else:
                    adjustment = snap_idx * 3
            rows.append(
                {
                    "marketplace": listing["marketplace"],
                    "listing_id": listing["listing_id"],
                    "price": round(max(listing["price"] + adjustment, 50.0), 2),
                    "shipping": listing["shipping"],
                }
            )
        snapshots.append({"captured_at": captured_at, "listings": rows})
    return snapshots


def render_raw_html(market_key: str, listings: list[dict]) -> str:
    if market_key == "amazon_books":
        items = "\n".join(
            f"""  <div class="book-card" data-listing-id="{listing['listing_id']}">
    <span class="title">{listing['title']}</span>
    <span class="author">{listing['author']}</span>
    <span class="isbn">{listing['isbn']}</span>
    <span class="edition">{listing['edition']}</span>
    <span class="publisher">{listing['publisher']}</span>
    <span class="format">{listing['format']}</span>
    <span class="price">{listing['price']}</span>
    <span class="shipping">{listing['shipping']}</span>
    <span class="rating">{listing['seller_rating']}</span>
    <span class="availability">{listing['availability']}</span>
  </div>"""
            for listing in listings
        )
    elif market_key == "flipkart_books":
        items = "\n".join(
            f"""  <section class="listing" data-listing-id="{listing['listing_id']}">
    <div class="listing-title">{listing['title']}</div>
    <div class="listing-author">{listing['author']}</div>
    <div class="listing-isbn">{listing['isbn']}</div>
    <div class="listing-edition">{listing['edition']}</div>
    <div class="listing-publisher">{listing['publisher']}</div>
    <div class="listing-format">{listing['format']}</div>
    <div class="listing-price">{listing['price']}</div>
    <div class="listing-shipping">{listing['shipping']}</div>
    <div class="listing-rating">{listing['seller_rating']}</div>
    <div class="listing-availability">{listing['availability']}</div>
  </section>"""
            for listing in listings
        )
    else:
        items = "\n".join(
            f"""  <article class="book-row" data-id="{listing['listing_id']}">
    <p class="book-title">{listing['title']}</p>
    <p class="book-author">{listing['author']}</p>
    <p class="book-isbn">{listing['isbn']}</p>
    <p class="book-edition">{listing['edition']}</p>
    <p class="book-publisher">{listing['publisher']}</p>
    <p class="book-format">{listing['format']}</p>
    <p class="book-price">{listing['price']}</p>
    <p class="book-shipping">{listing['shipping']}</p>
    <p class="book-rating">{listing['seller_rating']}</p>
    <p class="book-availability">{listing['availability']}</p>
  </article>"""
            for listing in listings
        )
    return f"<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n{items}\n</body>\n</html>\n"


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    catalog = build_catalog(total_skus=1000)
    marketplaces = build_marketplaces(catalog)
    snapshots = build_historical_snapshots(marketplaces, snapshot_count=14)

    write_json(INVENTORY_PATH, catalog)
    for market_key, listings in marketplaces.items():
        write_json(MARKETPLACE_DIR / f"{market_key}.json", listings)
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        (RAW_DIR / f"{market_key}.html").write_text(render_raw_html(market_key, listings), encoding="utf-8")
    write_json(MARKETPLACE_DIR / "historical_snapshots.json", snapshots)

    print("Generated benchmark dataset")
    print(f"Seller SKUs: {len(catalog)}")
    print(f"Marketplace listings: {sum(len(items) for items in marketplaces.values())}")
    print(f"Historical snapshots: {len(snapshots)}")


if __name__ == "__main__":
    main()
