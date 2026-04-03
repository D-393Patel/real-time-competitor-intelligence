# Real-Time Competitor Strategy Tracker

Real-Time Competitor Strategy Tracker is an internship-ready e-commerce intelligence project built for online book marketplaces. It solves a real pricing problem: the same book is often listed under inconsistent titles, editions, ISBNs, and publisher formats, which makes direct competitor comparison unreliable. This project combines scraping, semantic product matching, historical monitoring, pricing recommendations, alerts, and dashboard reporting into one end-to-end system.

## Business Problem

Online book sellers frequently face three issues:

- competitor prices change faster than manual teams can track
- equivalent books are hard to identify because metadata is inconsistent across marketplaces
- naive pricing strategies protect competitiveness poorly and often damage margin

This project addresses those issues by identifying equivalent books across noisy listings, monitoring price movement over time, and recommending profit-aware pricing actions through business-friendly outputs.

## Key Capabilities

- Scrapes marketplace-style HTML pages and converts them into structured listing snapshots
- Matches equivalent books across marketplaces using semantic similarity
- Supports an embedding-enabled matcher using SentenceTransformers with offline-safe fallback behavior
- Replays historical price snapshots to simulate real-time monitoring
- Generates `raise`, `hold`, and `lower` pricing recommendations
- Surfaces business alerts for aggressive undercutting, margin pressure, and opportunity signals
- Exposes a live dashboard, local API, and exportable reports for non-technical review

## Benchmark Scale

The current benchmark run supports:

- `1,000` seller SKUs
- `3,000` competitor listings across `3` marketplaces
- `14` historical monitoring snapshots
- `42,000` historical price observations
- `746` generated pricing alerts
- embedding-based semantic matching

You can regenerate the benchmark and metrics locally from the commands below.

## Architecture

```text
Raw Marketplace HTML
        |
        v
Scraping + Ingestion
        |
        v
Normalized Listings
        |
        v
Semantic Matching
        |
        v
Trend Analysis + Pricing Engine
        |
        v
Alerts + Dashboard + API + Reports
```

## Project Structure

```text
.
|-- data/
|   |-- inventory/
|   |-- marketplaces/
|   `-- raw_marketplaces/
|-- docs/
|-- reports/
|-- src/competitor_tracker/
`-- tests/
```

## Quick Start

Run the benchmark data generator:

```powershell
py -m src.competitor_tracker.generate_benchmark_data
```

Convert raw marketplace HTML into scraped JSON snapshots:

```powershell
py -m src.competitor_tracker.ingest
```

Run the end-to-end demo:

```powershell
py -m src.competitor_tracker.demo
```

Generate the quantified metrics report:

```powershell
py -m src.competitor_tracker.evaluate
```

Run the live local app:

```powershell
py -m src.competitor_tracker.server
```

Open:

- `http://127.0.0.1:8000/dashboard`
- `http://127.0.0.1:8000/api/insights`

Run tests:

```powershell
py -m unittest discover -s tests -v
```

## Outputs

The pipeline generates:

- `reports/latest_report.md`
- `reports/latest_report.json`
- `reports/dashboard.html`
- `reports/alerts_inbox.csv`
- `reports/project_metrics.json`

## Current Technical Highlights

- Parser-based scraping layer for Amazon Books, Flipkart Books, and Bookswagon-style inputs
- Automatic preference for scraped marketplace snapshots over curated sample feeds
- Matcher strategy abstraction with embedding-enabled semantic matching
- Interactive dashboard with executive summary, alerts inbox, filters, search, and sorting
- Business-facing exports in Markdown, JSON, CSV, and HTML
- Fast validation mode for tests plus full benchmark mode for large-scale evaluation

## Why This Is a Strong Internship Project

- It solves a practical e-commerce problem with measurable business relevance
- It covers full-stack engineering breadth: ingestion, matching, analytics, reporting, and API design
- It demonstrates both product thinking and system design, not just model experimentation
- It includes reproducible benchmarking and automated tests, which makes the work easier to trust

## Future Improvements

- Replace local HTTP serving with FastAPI and add auth-ready API structure
- Add scheduled jobs and background monitoring execution
- Persist historical prices in a database instead of JSON snapshots
- Add email or Slack notification delivery
- Extend the pricing engine with elasticity or conversion-aware modeling
