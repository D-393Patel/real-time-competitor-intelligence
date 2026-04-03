# Real-Time Competitor Strategy Tracker Presentation Script

This presentation script is designed to replace or update the current `realtime.pptx` so it matches the actual project in this repository.

## Why the Current PPT Needs Revision

The current deck describes a different implementation than the one in this repo. It references:

- Flask
- BeautifulSoup web scraping
- SBERT embeddings
- TF-IDF retrieval on a 52k+ dataset
- ARIMA forecasting
- 1,000 scraped products and 2,664 trained models

Those claims are not represented in the current codebase. For an internship presentation, it is much better to present a clean, truthful, polished project than an overclaimed one.

## Recommended Slide Flow

### Slide 1: Title

**Real-Time Competitor Strategy Tracker for E-Commerce Books**

Subtitle:
Semantic product matching, pricing intelligence, alerts, and trend-aware monitoring

Presented by:

- Your name
- Roll number
- Department
- Guide name

### Slide 2: Problem Statement

Online book marketplaces often list the same book with:

- different titles
- subtitle variations
- different editions
- missing or inconsistent ISBNs
- inconsistent author and publisher names

This makes direct price comparison unreliable. Sellers are forced to track competitors manually, which is time-consuming, error-prone, and not scalable.

### Slide 3: Objective

Build a system that can:

- monitor competitor book prices across marketplaces
- identify equivalent books using semantic matching logic
- recommend profit-safe pricing actions
- detect market threats and opportunities
- generate automated reports and alerts

### Slide 4: Key Features

- Multi-marketplace listing ingestion
- Semantic book matching across noisy metadata
- Profit-aware pricing recommendation engine
- Historical snapshot replay for real-time simulation
- Trend-aware dashboard with alerts inbox
- CSV, JSON, Markdown, and HTML outputs
- Local web app with browser dashboard and API

### Slide 5: System Workflow

Use this flow:

`Marketplace Data -> Normalization -> Semantic Matching -> Trend Analysis -> Pricing Engine -> Alerts -> Dashboard + Reports`

### Slide 6: Data Model

Mention the two main data sources:

- Seller catalog
- Competitor marketplace listings

Important attributes:

- title
- subtitle
- author
- ISBN
- edition
- format
- publisher
- current price
- cost price
- shipping cost
- marketplace fee
- target margin

### Slide 7: Semantic Matching Logic

Explain that equivalent books are identified using weighted signals:

- exact ISBN match
- title similarity
- author similarity
- publisher similarity
- edition alignment
- format alignment
- canonical title containment

This makes the system robust against noisy metadata.

### Slide 8: Pricing Recommendation Logic

The pricing engine does not simply undercut competitors.

It chooses:

- `LOWER` when market pressure is strong
- `RAISE` when there is margin headroom
- `HOLD` when current pricing is competitive

It protects profitability using:

- cost price
- shipping cost
- marketplace fee percentage
- target margin percentage

### Slide 9: Real-Time Monitoring Simulation

To simulate real-time behavior, the system replays multiple marketplace snapshots over time.

This allows the dashboard to show:

- market floor movement
- short-term volatility
- rising, stable, or falling competitor pressure

### Slide 10: Dashboard Overview

Show the dashboard and point out:

- KPI cards
- executive summary strip
- alerts inbox
- pricing action cards
- trend sparkline
- competitive detail tables
- interactive filters, search, and sorting

### Slide 11: Alerts Inbox

Explain that alerts are grouped by business importance:

- high: aggressive competitor undercutting or margin risk
- medium: visibility or monitoring concern
- low: margin expansion opportunity

Also mention CSV export for business users.

### Slide 12: Live App and API

Routes:

- `/dashboard`
- `/api/insights`
- `/health`

This makes the project feel like an internal product, not just a backend script.

### Slide 13: Example Output

Use the current example results:

- `Atomic Habits` -> `HOLD`
- `Deep Work` -> `RAISE`
- `The Psychology of Money` -> `LOWER`

Then explain why each result happened.

### Slide 14: Reports Generated

The system automatically produces:

- `latest_report.md`
- `latest_report.json`
- `dashboard.html`
- `alerts_inbox.csv`

This supports both technical and business users.

### Slide 15: Testing and Reliability

Mention that the project includes automated tests for:

- semantic matching quality
- pricing engine behavior
- historical monitoring
- dashboard generation
- alert CSV export
- server route availability

### Slide 16: Tech Stack

- Python 3.12
- Standard library HTTP server
- JSON-based datasets
- HTML/CSS/JavaScript dashboard
- Unit tests with `unittest`

### Slide 17: Business Impact

This project helps sellers:

- reduce manual competitor tracking effort
- avoid incorrect product comparisons
- protect margins while staying competitive
- respond faster to market changes
- make data-driven pricing decisions

### Slide 18: Limitations

Current limitations:

- uses curated sample data instead of live marketplace APIs
- uses heuristic semantic matching instead of transformer embeddings
- does not yet persist to a production database
- does not yet send real email or Slack alerts

### Slide 19: Future Enhancements

- FastAPI backend
- React frontend
- live marketplace API integration
- transformer embedding matcher
- database-backed history storage
- scheduled monitoring jobs
- email/Slack alert delivery
- elasticity-based pricing optimization

### Slide 20: Conclusion

This project demonstrates how semantic matching and pricing analytics can solve a real e-commerce problem.

It is internship-ready because it combines:

- software engineering
- data processing
- business logic
- reporting
- product-oriented presentation

### Slide 21: Demo / Questions

End with:

**Thank You**

Then demo:

- dashboard filters
- alerts inbox
- pricing actions
- CSV export

## Suggested 60-Second Project Summary

"Our project solves a real problem in online book selling: the same book appears across marketplaces with inconsistent titles, editions, and ISBN information, so direct price comparison is unreliable. We built a Real-Time Competitor Strategy Tracker that normalizes marketplace data, semantically matches equivalent books, analyzes competitor price movement, and recommends pricing actions like hold, raise, or lower while protecting target margins. On top of that, we built a dashboard, alerts inbox, CSV export, and local API so the project feels like a real internal product rather than just a script."

## Suggested Demo Order

1. Open the live dashboard.
2. Show the executive summary.
3. Open the alerts inbox.
4. Filter by `lower` action.
5. Search for `Deep Work`.
6. Sort by biggest undercut.
7. Show the generated CSV and reports.

## Important Presentation Advice

- Do not present features that are not in the code.
- If asked about machine learning, say the current version uses explainable heuristic semantic matching and is designed to be extended with embeddings later.
- If asked about real-time, explain that the current version uses historical snapshot replay to simulate market monitoring and demonstrate decision logic clearly.
