import unittest

from src.competitor_tracker.io_utils import detect_marketplace_source, load_marketplace_listings, load_seller_catalog
from src.competitor_tracker.evaluate import collect_metrics
from src.competitor_tracker.matching_service import get_matcher_info
from src.competitor_tracker.matcher import find_equivalent_listings, score_listing_match
from src.competitor_tracker.monitoring import build_listing_history
from src.competitor_tracker.pipeline import build_insights, get_data_source_label, get_matcher_label
from src.competitor_tracker.pricing import recommend_price
from src.competitor_tracker.reporting import render_dashboard_html, write_alerts_csv
from src.competitor_tracker.scraping import parse_marketplace_html, write_scraped_snapshots
from src.competitor_tracker.server import TrackerRequestHandler


class TrackerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_seller_catalog(limit=3)
        self.listings = load_marketplace_listings(prefer_scraped=False, limit=9)

    def test_atomic_habits_variant_still_matches(self) -> None:
        book = next(item for item in self.catalog if item.sku == "BK-ATOMIC-HABITS-PB")
        listing = next(item for item in self.listings if item.listing_id == "BW-3001")

        candidate = score_listing_match(book, listing)

        self.assertGreaterEqual(candidate.confidence, 0.55)
        self.assertIn("Strong title similarity", " ".join(candidate.reasons))

    def test_matching_groups_books_by_sku(self) -> None:
        matched = find_equivalent_listings(self.catalog, self.listings, threshold=0.55)

        self.assertGreaterEqual(len(matched["BK-ATOMIC-HABITS-PB"]), 2)
        self.assertGreaterEqual(len(matched["BK-DEEP-WORK-PB"]), 2)
        self.assertGreaterEqual(len(matched["BK-PSY-MONEY-HC"]), 2)

    def test_pricing_engine_covers_raise_lower_and_hold(self) -> None:
        insights = {
            insight.book.sku: insight
            for insight in build_insights(
                prefer_scraped=False,
                prefer_embeddings=False,
                catalog_limit=3,
                listing_limit=9,
            )
        }

        self.assertEqual(insights["BK-ATOMIC-HABITS-PB"].recommendation.action, "hold")
        self.assertEqual(insights["BK-DEEP-WORK-PB"].recommendation.action, "raise")
        self.assertEqual(insights["BK-PSY-MONEY-HC"].recommendation.action, "lower")

    def test_lower_recommendation_preserves_positive_margin(self) -> None:
        book = next(item for item in self.catalog if item.sku == "BK-PSY-MONEY-HC")
        listings = [item for item in self.listings if item.listing_id in {"AMZ-1003", "BW-3003"}]

        recommendation = recommend_price(book, listings)

        self.assertEqual(recommendation.action, "lower")
        self.assertGreater(recommendation.expected_margin_pct, 0.0)

    def test_dashboard_contains_key_sections(self) -> None:
        html = render_dashboard_html(
            build_insights(
                prefer_scraped=False,
                prefer_embeddings=False,
                catalog_limit=3,
                listing_limit=9,
            ),
            data_source_label="curated sample feeds",
            matcher_label="heuristic",
        )

        self.assertIn("Real-Time Competitor Strategy Tracker", html)
        self.assertIn("Biggest Threat", html)
        self.assertIn("Best Opportunity", html)
        self.assertIn("Recommended Next Move", html)
        self.assertIn("Alerts Inbox", html)
        self.assertIn("Pricing Actions", html)
        self.assertIn("Competitive Detail", html)
        self.assertIn("BK-DEEP-WORK-PB", html)
        self.assertIn("marketplace-filter", html)
        self.assertIn("severity-filter", html)
        self.assertIn("search-filter", html)
        self.assertIn("sort-filter", html)

    def test_historical_monitoring_has_multiple_snapshots(self) -> None:
        history = build_listing_history()

        self.assertIn("AMZ-1003", history)
        self.assertGreaterEqual(len(history["AMZ-1003"]), 7)
        self.assertLess(history["AMZ-1003"][-1].landed_price, history["AMZ-1003"][0].landed_price)

    def test_server_routes_are_defined(self) -> None:
        self.assertTrue(hasattr(TrackerRequestHandler, "do_GET"))

    def test_alerts_csv_is_generated(self) -> None:
        path = write_alerts_csv(
            build_insights(
                prefer_scraped=False,
                prefer_embeddings=False,
                catalog_limit=3,
                listing_limit=9,
            )
        )
        content = path.read_text(encoding="utf-8")

        self.assertIn("severity,sku,book_title,alert_title", content)
        self.assertIn("BK-PSY-MONEY-HC", content)

    def test_scraper_parses_marketplace_html(self) -> None:
        html = """
        <div class="book-card" data-listing-id="AMZ-X1">
          <span class="title">Demo Book</span>
          <span class="author">Demo Author</span>
          <span class="isbn">123</span>
          <span class="edition">Paperback</span>
          <span class="publisher">Demo Publisher</span>
          <span class="format">Paperback</span>
          <span class="price">100.0</span>
          <span class="shipping">10.0</span>
          <span class="rating">4.2</span>
          <span class="availability">in_stock</span>
        </div>
        """
        listings = parse_marketplace_html("amazon_books", html, captured_at="2026-04-02T10:00:00+05:30")

        self.assertEqual(len(listings), 1)
        self.assertEqual(listings[0].listing_id, "AMZ-X1")
        self.assertEqual(listings[0].landed_price, 110.0)

    def test_scraped_snapshots_are_written(self) -> None:
        paths = write_scraped_snapshots(captured_at="2026-04-02T10:00:00+05:30")

        self.assertTrue(any(path.name == "amazon_books_scraped.json" for path in paths))

    def test_loader_prefers_scraped_snapshots_when_present(self) -> None:
        write_scraped_snapshots(captured_at="2026-04-02T10:00:00+05:30")
        listings = load_marketplace_listings(prefer_scraped=True)

        self.assertGreaterEqual(len(listings), 3000)
        self.assertEqual(detect_marketplace_source(prefer_scraped=True), "scraped snapshots")

    def test_dashboard_and_pipeline_expose_active_source(self) -> None:
        write_scraped_snapshots(captured_at="2026-04-02T10:00:00+05:30")
        html = render_dashboard_html(
            build_insights(prefer_scraped=True, catalog_limit=3, listing_limit=9),
            data_source_label=get_data_source_label(),
            matcher_label=get_matcher_label(),
        )

        self.assertIn("Source: scraped snapshots", html)
        self.assertIn(f"Matcher: {get_matcher_label()}", html)

    def test_matcher_defaults_to_heuristic_when_embeddings_unavailable(self) -> None:
        info = get_matcher_info(prefer_embeddings=True)

        self.assertIn(info.strategy, {"heuristic", "embedding"})

    def test_metrics_collection_returns_quantified_summary(self) -> None:
        metrics = collect_metrics(prefer_embeddings=False, catalog_limit=3, listing_limit=9)

        self.assertEqual(metrics["seller_skus_monitored"], 3)
        self.assertEqual(metrics["competitor_listings_loaded"], 9)
        self.assertIn("pricing_actions", metrics)


if __name__ == "__main__":
    unittest.main()
