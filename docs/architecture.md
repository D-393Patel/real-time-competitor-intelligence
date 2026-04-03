# Architecture Overview

## Objective

Build a competitor intelligence system for online book sellers that can:

- monitor listings across marketplaces
- identify equivalent books despite noisy metadata
- recommend profit-safe pricing actions
- surface alerts and reports for fast business response

## Pipeline

```text
Marketplace Feeds -> Normalization -> Semantic Matching -> Price Intelligence -> Alerts -> Reports
```

## Key Modules

### `io_utils.py`

Loads seller inventory and marketplace feeds from JSON. This keeps the demo simple while mirroring what a production ingestion layer would hand off downstream.

### `normalization.py`

Standardizes text, ISBNs, formats, and edition labels. This is critical because marketplace metadata is inconsistent even when listings refer to the same physical book.

### `matcher.py`

Computes equivalence confidence using a weighted heuristic:

- ISBN exact match
- title similarity
- author similarity
- publisher similarity
- edition alignment
- format alignment

This is intentionally explainable, which is useful for internship demos and recruiter walkthroughs.

### `pricing.py`

Transforms matched competitor listings into an action:

- `lower` when the market floor threatens competitiveness
- `raise` when margin can improve without giving up the market
- `hold` when current pricing is balanced

Recommendations respect:

- cost price
- shipping cost
- marketplace fee percentage
- target margin percentage

### `monitoring.py` and `analytics.py`

Adds the real-time simulation layer by replaying multiple marketplace snapshots and summarizing:

- market-floor movement over time
- short-term volatility
- rising, stable, or falling competitor pressure

This makes the project feel operational instead of static.

### `alerts.py`

Raises business-facing alerts for:

- aggressive competitor undercutting
- margin risk
- margin expansion opportunities
- missing market visibility

### `reporting.py`

Exports:

- `reports/latest_report.md`
- `reports/latest_report.json`
- `reports/dashboard.html`
- `reports/alerts_inbox.csv`

These outputs mimic automated operational reporting for category managers or sellers.

### `server.py`

Provides a lightweight application layer with:

- `/dashboard` for a live browser view
- `/api/insights` for structured JSON output
- `/health` for a simple readiness check

This is a strong internship touch because it shows how the analytics layer can be consumed as an internal tool.

### `scraping.py` and `ingest.py`

Adds a scraper-style ingestion layer that:

- parses raw marketplace HTML samples
- converts them into structured competitor listings
- writes reusable JSON snapshots for the pricing pipeline

This lets the project truthfully demonstrate scraping and ingestion even when live network access is unavailable during review.
When scraped snapshots are present, the app can prefer them as the active marketplace input source.

### `matching_service.py`

Adds matcher strategy selection:

- heuristic matcher by default
- optional embedding matcher path when `sentence-transformers` is available

This gives the project a realistic upgrade path from explainable heuristics to stronger semantic retrieval without breaking offline demos.

### `evaluate.py`

Produces a quantified metrics snapshot for the current project, including:

- SKUs monitored
- competitor listings loaded
- matched equivalents found
- pricing action distribution
- alerts generated
- margin averages
- historical snapshot coverage

## Why Semantic Matching Matters

Direct field equality fails because online book listings frequently vary by:

- subtitle inclusion
- abbreviations in author names
- publisher shorthand
- edition formatting
- missing or reused ISBN values

The matching layer closes that gap and makes downstream pricing decisions trustworthy.

## Production-Ready Extension Path

The current project is intentionally lightweight, but the architecture is ready to evolve into:

1. Event-driven ingestion from APIs or scrapers
2. Embedding-based record linkage for harder catalog matching
3. FastAPI inference service for dashboard consumption
4. Scheduler plus notification delivery through email or Slack
5. Historical pricing warehouse and elasticity modeling
