from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

from .pipeline import SkuInsight, get_data_source_label, get_matcher_label, insights_to_dict


ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports"


def render_markdown_report(insights: list[SkuInsight]) -> str:
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    lines = [
        "# Real-Time Competitor Strategy Tracker Report",
        "",
        f"Generated at: `{generated_at}`",
        "",
        "## Executive Summary",
        "",
    ]

    total_alerts = sum(len(insight.alerts) for insight in insights)
    lower_count = sum(1 for insight in insights if insight.recommendation.action == "lower")
    raise_count = sum(1 for insight in insights if insight.recommendation.action == "raise")

    lines.extend(
        [
            f"- SKUs monitored: {len(insights)}",
            f"- High-priority pricing changes: {lower_count}",
            f"- Margin expansion opportunities: {raise_count}",
            f"- Total alerts triggered: {total_alerts}",
            "",
        ]
    )

    for insight in insights:
        book = insight.book
        recommendation = insight.recommendation
        lines.extend(
            [
                f"## {book.sku} - {book.canonical_title}",
                "",
                f"- Current price: {book.current_price:.2f}",
                f"- Recommended action: **{recommendation.action.upper()}** to {recommendation.recommended_price:.2f}",
                f"- Expected margin: {recommendation.expected_margin_pct:.1%}",
                f"- Matched competitors: {len(insight.matches)}",
                f"- Market trend: {insight.trend.trend_label} ({insight.trend.floor_change:+.2f} vs first snapshot)",
                "",
                "### Why",
                "",
            ]
        )
        lines.extend(f"- {reason}" for reason in recommendation.rationale)
        lines.extend(["", "### Top Matches", ""])

        for listing, candidate in insight.matches[:3]:
            lines.append(
                f"- {listing.marketplace} | {listing.title} | landed price {listing.landed_price:.2f} | confidence {candidate.confidence:.2f}"
            )

        lines.extend(["", "### Alerts", ""])
        if insight.alerts:
            lines.extend(f"- [{alert.severity.upper()}] {alert.title}: {alert.message}" for alert in insight.alerts)
        else:
            lines.append("- No active alerts")
        lines.append("")

    return "\n".join(lines)


def write_reports(insights: list[SkuInsight]) -> tuple[Path, Path]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    markdown_path = REPORTS_DIR / "latest_report.md"
    json_path = REPORTS_DIR / "latest_report.json"
    markdown_path.write_text(render_markdown_report(insights), encoding="utf-8")
    json_path.write_text(json.dumps(insights_to_dict(insights), indent=2), encoding="utf-8")
    return markdown_path, json_path


def render_dashboard_html(
    insights: list[SkuInsight],
    data_source_label: str | None = None,
    matcher_label: str | None = None,
) -> str:
    generated_at = datetime.now().astimezone().strftime("%d %b %Y %I:%M:%S %p %Z")
    source_label = data_source_label or get_data_source_label()
    active_matcher = matcher_label or get_matcher_label()
    total_alerts = sum(len(insight.alerts) for insight in insights)
    lower_count = sum(1 for insight in insights if insight.recommendation.action == "lower")
    raise_count = sum(1 for insight in insights if insight.recommendation.action == "raise")
    hold_count = sum(1 for insight in insights if insight.recommendation.action == "hold")
    avg_margin = (
        sum(insight.recommendation.expected_margin_pct for insight in insights) / len(insights) if insights else 0.0
    )
    falling_count = sum(1 for insight in insights if insight.trend.trend_label == "falling")
    marketplaces = sorted({listing.marketplace for insight in insights for listing, _candidate in insight.matches})
    severities = sorted({alert.severity for insight in insights for alert in insight.alerts})
    alert_order = {"high": 0, "medium": 1, "low": 2}
    biggest_threat = max(insights, key=lambda insight: insight.recommendation.competitor_gap, default=None)
    best_opportunity = max(
        insights,
        key=lambda insight: (
            1 if insight.recommendation.action == "raise" else 0,
            insight.recommendation.expected_margin_pct,
        ),
        default=None,
    )
    next_move = max(
        insights,
        key=lambda insight: (
            len([alert for alert in insight.alerts if alert.severity == "high"]),
            insight.recommendation.competitor_gap,
        ),
        default=None,
    )
    all_alerts = sorted(
        [
            (alert, insight.book.canonical_title, insight.recommendation.action)
            for insight in insights
            for alert in insight.alerts
        ],
        key=lambda item: (alert_order.get(item[0].severity, 9), item[0].sku, item[0].title),
    )
    inbox_html = "".join(
        f"""
        <article class="inbox-item {alert.severity}">
          <div class="inbox-top">
            <span class="inbox-pill {alert.severity}">{alert.severity.upper()}</span>
            <span class="inbox-sku">{alert.sku}</span>
          </div>
          <h3>{alert.title}</h3>
          <p>{message}</p>
          <div class="inbox-meta">
            <span>{book_title}</span>
            <span>Recommended action: {action.upper()}</span>
          </div>
        </article>
        """
        for alert, book_title, action in all_alerts
        for message in [alert.message]
    ) or '<div class="empty-state">No alerts triggered in this monitoring cycle.</div>'

    action_cards: list[str] = []
    detail_sections: list[str] = []
    for insight in insights:
        book = insight.book
        recommendation = insight.recommendation
        badge_class = f"badge-{recommendation.action}"
        trend_points = insight.trend.floor_series
        sparkline = build_sparkline_svg([price for _timestamp, price in trend_points])
        marketplace_tokens = "|".join(sorted({listing.marketplace for listing, _candidate in insight.matches}))
        severity_tokens = "|".join(sorted({alert.severity for alert in insight.alerts})) or "none"
        best_confidence = max((candidate.confidence for _listing, candidate in insight.matches), default=0.0)
        alert_html = "".join(
            (
                f'<div class="alert {alert.severity}" data-severity="{alert.severity}">'
                f"<strong>{alert.title}</strong><span>{alert.message}</span></div>"
            )
            for alert in insight.alerts
        ) or '<div class="empty-state">No active alerts for this SKU.</div>'

        match_rows = "".join(
            (
                f'<tr data-marketplace="{listing.marketplace}">'
                f"<td>{listing.marketplace}</td>"
                f"<td>{listing.title}</td>"
                f"<td>{listing.landed_price:.2f}</td>"
                f"<td>{candidate.confidence:.2f}</td>"
                f"<td>{', '.join(candidate.reasons[:3])}</td>"
                "</tr>"
            )
            for listing, candidate in insight.matches[:5]
        ) or '<tr><td colspan="5">No competitor matches found</td></tr>'

        rationale_html = "".join(f"<li>{reason}</li>" for reason in recommendation.rationale)

        action_cards.append(
            f"""
            <article class="sku-card" data-sku="{book.sku}" data-title="{book.canonical_title}" data-action="{recommendation.action}" data-marketplaces="{marketplace_tokens}" data-severities="{severity_tokens}" data-gap="{recommendation.competitor_gap:.2f}" data-margin="{recommendation.expected_margin_pct:.4f}" data-trend-change="{insight.trend.floor_change:.2f}" data-confidence="{best_confidence:.2f}">
              <div class="sku-card-top">
                <div>
                  <p class="eyebrow">{book.sku}</p>
                  <h3>{book.canonical_title}</h3>
                  <p class="meta">{book.author} | {book.format.title()} | Target margin {book.target_margin_pct:.0%}</p>
                </div>
                <span class="action-badge {badge_class}">{recommendation.action.upper()}</span>
              </div>
              <div class="price-grid">
                <div><span>Current</span><strong>{book.current_price:.2f}</strong></div>
                <div><span>Recommended</span><strong>{recommendation.recommended_price:.2f}</strong></div>
                <div><span>Expected margin</span><strong>{recommendation.expected_margin_pct:.1%}</strong></div>
                <div><span>Competitor gap</span><strong>{recommendation.competitor_gap:.2f}</strong></div>
              </div>
              <div class="trend-row">
                <div>
                  <span class="trend-label">Market floor trend</span>
                  <strong>{insight.trend.trend_label.title()}</strong>
                  <em>{insight.trend.floor_change:+.2f} change | volatility {insight.trend.volatility:.2f}</em>
                </div>
                <div class="sparkline">{sparkline}</div>
              </div>
              <ul class="rationale-list">{rationale_html}</ul>
            </article>
            """
        )

        detail_sections.append(
            f"""
            <section class="detail-panel" data-sku="{book.sku}" data-title="{book.canonical_title}" data-action="{recommendation.action}" data-marketplaces="{marketplace_tokens}" data-severities="{severity_tokens}" data-gap="{recommendation.competitor_gap:.2f}" data-margin="{recommendation.expected_margin_pct:.4f}" data-trend-change="{insight.trend.floor_change:.2f}" data-confidence="{best_confidence:.2f}">
              <div class="panel-header">
                <div>
                  <p class="eyebrow">Competitive intelligence</p>
                  <h3>{book.canonical_title}</h3>
                </div>
                <span class="panel-pill">{len(insight.matches)} matched listings</span>
              </div>
              <div class="detail-grid">
                <div>
                  <h4>Alerts</h4>
                  {alert_html}
                </div>
                <div>
                  <h4>Top competitor matches</h4>
                  <div class="table-wrap">
                    <table>
                      <thead>
                        <tr>
                          <th>Marketplace</th>
                          <th>Listing</th>
                          <th>Landed price</th>
                            <th>Confidence</th>
                            <th>Why matched</th>
                          </tr>
                        </thead>
                        <tbody>{match_rows}</tbody>
                    </table>
                  </div>
                </div>
              </div>
            </section>
            """
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Competitor Strategy Tracker Dashboard</title>
  <style>
    :root {{
      --bg: #f4efe7;
      --panel: rgba(255, 250, 244, 0.88);
      --ink: #1d2433;
      --muted: #5b6475;
      --accent: #0f766e;
      --accent-2: #c2410c;
      --hold: #2563eb;
      --raise: #0f766e;
      --lower: #b91c1c;
      --line: rgba(29, 36, 51, 0.12);
      --shadow: 0 24px 60px rgba(36, 31, 24, 0.14);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(15, 118, 110, 0.14), transparent 28%),
        radial-gradient(circle at top right, rgba(194, 65, 12, 0.12), transparent 25%),
        linear-gradient(180deg, #f7f1e8 0%, #efe7db 100%);
    }}
    .shell {{
      width: min(1200px, calc(100% - 32px));
      margin: 32px auto 48px;
    }}
    .hero {{
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 28px;
      background: linear-gradient(135deg, rgba(255,255,255,0.75), rgba(255,247,237,0.92));
      box-shadow: var(--shadow);
    }}
    .hero h1 {{
      margin: 0 0 10px;
      font-size: clamp(2rem, 4vw, 3.4rem);
      line-height: 1.02;
      letter-spacing: -0.04em;
    }}
    .hero p {{
      max-width: 760px;
      color: var(--muted);
      font-size: 1.02rem;
      line-height: 1.6;
      margin: 0;
    }}
    .hero-meta {{
      margin-top: 18px;
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .hero-meta span {{
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.55);
      border-radius: 999px;
      padding: 8px 12px;
      font-size: 0.9rem;
    }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 16px;
      margin-top: 22px;
    }}
    .kpi, .sku-card, .detail-panel {{
      border: 1px solid var(--line);
      background: var(--panel);
      backdrop-filter: blur(10px);
      box-shadow: var(--shadow);
    }}
    .kpi {{
      border-radius: 22px;
      padding: 18px;
    }}
    .kpi span {{
      display: block;
      color: var(--muted);
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
    }}
    .kpi strong {{
      font-size: 2rem;
      letter-spacing: -0.04em;
    }}
    .section-title {{
      margin: 30px 0 14px;
      font-size: 1.45rem;
      letter-spacing: -0.03em;
    }}
    .section-subtitle {{
      margin: 0 0 12px;
      color: var(--muted);
      line-height: 1.6;
    }}
    .filters {{
      margin-top: 20px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 14px;
    }}
    .summary-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-top: 22px;
    }}
    .summary-card {{
      border-radius: 22px;
      padding: 18px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.58);
    }}
    .summary-card strong {{
      display: block;
      margin: 8px 0 6px;
      font-size: 1.15rem;
      letter-spacing: -0.03em;
    }}
    .summary-card p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.55;
    }}
    .filter {{
      display: grid;
      gap: 8px;
      padding: 14px;
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.55);
    }}
    .filter label {{
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }}
    .filter select {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 10px 12px;
      background: #fffdfa;
      color: var(--ink);
      font: inherit;
    }}
    .filter input {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 10px 12px;
      background: #fffdfa;
      color: var(--ink);
      font: inherit;
    }}
    .filter-summary {{
      margin-top: 14px;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
    }}
    .inbox-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
      margin-top: 14px;
    }}
    .inbox-item {{
      border-radius: 22px;
      padding: 18px;
      border: 1px solid var(--line);
      background: var(--panel);
      box-shadow: var(--shadow);
    }}
    .inbox-item h3 {{
      margin: 12px 0 8px;
      font-size: 1.1rem;
    }}
    .inbox-item p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
    }}
    .inbox-top {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
    }}
    .inbox-pill {{
      display: inline-flex;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 0.78rem;
      letter-spacing: 0.08em;
      border: 1px solid transparent;
    }}
    .inbox-pill.high {{ color: var(--lower); background: rgba(185, 28, 28, 0.1); border-color: rgba(185, 28, 28, 0.16); }}
    .inbox-pill.medium {{ color: #a16207; background: rgba(202, 138, 4, 0.1); border-color: rgba(202, 138, 4, 0.16); }}
    .inbox-pill.low {{ color: var(--raise); background: rgba(15, 118, 110, 0.1); border-color: rgba(15, 118, 110, 0.16); }}
    .inbox-sku {{
      font-size: 0.84rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    .inbox-meta {{
      margin-top: 14px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      color: var(--muted);
      font-size: 0.88rem;
    }}
    .sku-card {{
      border-radius: 24px;
      padding: 20px;
    }}
    .sku-card-top, .panel-header, .detail-grid {{
      display: flex;
      gap: 16px;
      justify-content: space-between;
      align-items: flex-start;
    }}
    .eyebrow {{
      margin: 0 0 4px;
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--muted);
    }}
    h3, h4 {{
      margin: 0;
    }}
    .meta {{
      margin: 8px 0 0;
      color: var(--muted);
      line-height: 1.5;
    }}
    .action-badge, .panel-pill {{
      display: inline-flex;
      padding: 8px 12px;
      border-radius: 999px;
      font-size: 0.8rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      border: 1px solid transparent;
      white-space: nowrap;
    }}
    .badge-hold {{ color: var(--hold); background: rgba(37, 99, 235, 0.1); border-color: rgba(37, 99, 235, 0.16); }}
    .badge-raise {{ color: var(--raise); background: rgba(15, 118, 110, 0.1); border-color: rgba(15, 118, 110, 0.16); }}
    .badge-lower {{ color: var(--lower); background: rgba(185, 28, 28, 0.1); border-color: rgba(185, 28, 28, 0.16); }}
    .panel-pill {{ color: var(--accent-2); background: rgba(194, 65, 12, 0.08); border-color: rgba(194, 65, 12, 0.16); }}
    .price-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin: 18px 0;
    }}
    .price-grid div {{
      padding: 14px;
      border-radius: 18px;
      background: rgba(255,255,255,0.55);
      border: 1px solid var(--line);
    }}
    .price-grid span {{
      display: block;
      font-size: 0.82rem;
      color: var(--muted);
      margin-bottom: 8px;
    }}
    .price-grid strong {{
      font-size: 1.5rem;
      letter-spacing: -0.03em;
    }}
    .rationale-list {{
      margin: 0;
      padding-left: 18px;
      line-height: 1.6;
    }}
    .trend-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 14px;
      border-radius: 18px;
      background: rgba(255,255,255,0.55);
      border: 1px solid var(--line);
      margin-bottom: 16px;
    }}
    .trend-label {{
      display: block;
      font-size: 0.82rem;
      color: var(--muted);
      margin-bottom: 6px;
    }}
    .trend-row strong {{
      display: block;
      font-size: 1.2rem;
      margin-bottom: 4px;
    }}
    .trend-row em {{
      color: var(--muted);
      font-style: normal;
      font-size: 0.9rem;
    }}
    .sparkline svg {{
      width: 160px;
      height: 52px;
      display: block;
    }}
    .detail-stack {{
      display: grid;
      gap: 18px;
      margin-top: 18px;
    }}
    .detail-panel {{
      border-radius: 24px;
      padding: 20px;
    }}
    .detail-grid {{
      align-items: stretch;
      margin-top: 18px;
    }}
    .detail-grid > div {{
      flex: 1 1 0;
      min-width: 0;
    }}
    .alert {{
      display: grid;
      gap: 6px;
      padding: 14px;
      border-radius: 16px;
      margin-bottom: 12px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.56);
    }}
    .alert.high {{ border-color: rgba(185, 28, 28, 0.22); background: rgba(254, 242, 242, 0.92); }}
    .alert.medium {{ border-color: rgba(202, 138, 4, 0.22); background: rgba(254, 252, 232, 0.92); }}
    .alert.low {{ border-color: rgba(15, 118, 110, 0.22); background: rgba(240, 253, 250, 0.92); }}
    .empty-state {{
      padding: 14px;
      border-radius: 16px;
      background: rgba(255,255,255,0.55);
      border: 1px dashed var(--line);
      color: var(--muted);
    }}
    .hidden {{
      display: none !important;
    }}
    .table-wrap {{
      overflow: auto;
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.55);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 620px;
    }}
    th, td {{
      padding: 12px 14px;
      text-align: left;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      background: rgba(244, 239, 231, 0.88);
    }}
    td {{
      font-size: 0.95rem;
      line-height: 1.45;
    }}
    @media (max-width: 860px) {{
      .detail-grid {{
        flex-direction: column;
      }}
      .sku-card-top, .panel-header {{
        flex-direction: column;
      }}
      .price-grid {{
        grid-template-columns: 1fr;
      }}
      .trend-row {{
        flex-direction: column;
        align-items: flex-start;
      }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Internship Showcase Project</p>
      <h1>Real-Time Competitor Strategy Tracker</h1>
      <p>Semantic book matching meets profitability-first pricing intelligence. This dashboard turns noisy marketplace listings into seller actions, alerts, and explainable competitor insights.</p>
      <div class="hero-meta">
        <span>Generated: {generated_at}</span>
        <span>Domain: E-commerce books</span>
        <span>Focus: Matching + pricing + alerts</span>
        <span>Source: {source_label}</span>
        <span>Matcher: {active_matcher}</span>
      </div>
      <div class="kpis">
        <div class="kpi"><span>SKUs monitored</span><strong>{len(insights)}</strong></div>
        <div class="kpi"><span>Raise opportunities</span><strong>{raise_count}</strong></div>
        <div class="kpi"><span>Lower now</span><strong>{lower_count}</strong></div>
        <div class="kpi"><span>Hold steady</span><strong>{hold_count}</strong></div>
        <div class="kpi"><span>Falling markets</span><strong>{falling_count}</strong></div>
        <div class="kpi"><span>Total alerts</span><strong>{total_alerts}</strong></div>
        <div class="kpi"><span>Avg expected margin</span><strong>{avg_margin:.1%}</strong></div>
      </div>
      <div class="summary-strip">
        <article class="summary-card">
          <p class="eyebrow">Biggest Threat</p>
          <strong>{biggest_threat.book.canonical_title if biggest_threat else "No active threat"}</strong>
          <p>{f"Competitor pressure is strongest here with a {biggest_threat.recommendation.competitor_gap:.2f} current price gap and action {biggest_threat.recommendation.action.upper()}." if biggest_threat else "No active threat detected."}</p>
        </article>
        <article class="summary-card">
          <p class="eyebrow">Best Opportunity</p>
          <strong>{best_opportunity.book.canonical_title if best_opportunity else "No active opportunity"}</strong>
          <p>{f"This SKU offers the best margin upside with expected margin {best_opportunity.recommendation.expected_margin_pct:.1%} and action {best_opportunity.recommendation.action.upper()}." if best_opportunity else "No active opportunity detected."}</p>
        </article>
        <article class="summary-card">
          <p class="eyebrow">Recommended Next Move</p>
          <strong>{next_move.book.sku if next_move else "No immediate move"}</strong>
          <p>{f"Prioritize {next_move.book.canonical_title} because it combines the most urgent alert pressure with current market movement." if next_move else "No immediate move required."}</p>
        </article>
      </div>
      <div class="filters">
        <div class="filter">
          <label for="search-filter">Search SKU or title</label>
          <input id="search-filter" type="text" placeholder="e.g. Atomic or BK-DEEP" />
        </div>
        <div class="filter">
          <label for="marketplace-filter">Marketplace</label>
          <select id="marketplace-filter">
            <option value="all">All marketplaces</option>
            {''.join(f'<option value="{marketplace}">{marketplace}</option>' for marketplace in marketplaces)}
          </select>
        </div>
        <div class="filter">
          <label for="action-filter">Pricing action</label>
          <select id="action-filter">
            <option value="all">All actions</option>
            <option value="hold">Hold</option>
            <option value="raise">Raise</option>
            <option value="lower">Lower</option>
          </select>
        </div>
        <div class="filter">
          <label for="severity-filter">Alert severity</label>
          <select id="severity-filter">
            <option value="all">All severities</option>
            {''.join(f'<option value="{severity}">{severity.title()}</option>' for severity in severities)}
          </select>
        </div>
        <div class="filter">
          <label for="sort-filter">Sort visible SKUs</label>
          <select id="sort-filter">
            <option value="default">Default order</option>
            <option value="gap_desc">Biggest undercut first</option>
            <option value="margin_desc">Highest margin first</option>
            <option value="trend_asc">Fastest falling market first</option>
            <option value="confidence_desc">Highest match confidence first</option>
            <option value="title_asc">Title A-Z</option>
          </select>
        </div>
      </div>
      <p class="filter-summary"><span id="visible-sku-count">{len(insights)}</span> of {len(insights)} SKUs visible</p>
    </section>

    <h2 class="section-title">Alerts Inbox</h2>
    <p class="section-subtitle">A recruiter-friendly operator view of the highest-priority issues and opportunities from the latest monitoring cycle.</p>
    <section class="inbox-grid">
      {inbox_html}
    </section>

    <h2 class="section-title">Pricing Actions</h2>
    <section class="cards">
      {''.join(action_cards)}
    </section>

    <h2 class="section-title">Competitive Detail</h2>
    <section class="detail-stack">
      {''.join(detail_sections)}
    </section>
  </main>
  <script>
    const searchFilter = document.getElementById("search-filter");
    const marketplaceFilter = document.getElementById("marketplace-filter");
    const actionFilter = document.getElementById("action-filter");
    const severityFilter = document.getElementById("severity-filter");
    const sortFilter = document.getElementById("sort-filter");
    const cards = Array.from(document.querySelectorAll(".sku-card"));
    const panels = Array.from(document.querySelectorAll(".detail-panel"));
    const cardsContainer = document.querySelector(".cards");
    const detailContainer = document.querySelector(".detail-stack");
    const visibleCount = document.getElementById("visible-sku-count");

    function includesToken(rawValue, token) {{
      if (token === "all") return true;
      return (rawValue || "").split("|").includes(token);
    }}

    function textMatches(element) {{
      const query = searchFilter.value.trim().toLowerCase();
      if (!query) return true;
      const haystack = `${{element.dataset.sku || ""}} ${{element.dataset.title || ""}}`.toLowerCase();
      return haystack.includes(query);
    }}

    function matchesFilters(element) {{
      const actionOk = actionFilter.value === "all" || element.dataset.action === actionFilter.value;
      const marketplaceOk = includesToken(element.dataset.marketplaces, marketplaceFilter.value);
      const severityOk = severityFilter.value === "all" || includesToken(element.dataset.severities, severityFilter.value);
      return actionOk && marketplaceOk && severityOk && textMatches(element);
    }}

    function sortValue(element) {{
      switch (sortFilter.value) {{
        case "gap_desc":
          return -Number(element.dataset.gap || 0);
        case "margin_desc":
          return -Number(element.dataset.margin || 0);
        case "trend_asc":
          return Number(element.dataset.trendChange || 0);
        case "confidence_desc":
          return -Number(element.dataset.confidence || 0);
        case "title_asc":
          return String(element.dataset.title || "").toLowerCase();
        default:
          return 0;
      }}
    }}

    function compareElements(left, right) {{
      const leftValue = sortValue(left);
      const rightValue = sortValue(right);
      if (leftValue < rightValue) return -1;
      if (leftValue > rightValue) return 1;
      return 0;
    }}

    function reorderVisibleElements() {{
      cards.sort(compareElements).forEach((card) => cardsContainer.appendChild(card));
      panels.sort(compareElements).forEach((panel) => detailContainer.appendChild(panel));
    }}

    function updatePanelInternals(panel) {{
      const rows = Array.from(panel.querySelectorAll("tbody tr[data-marketplace]"));
      rows.forEach((row) => {{
        const showRow = marketplaceFilter.value === "all" || row.dataset.marketplace === marketplaceFilter.value;
        row.classList.toggle("hidden", !showRow);
      }});

      const alerts = Array.from(panel.querySelectorAll(".alert[data-severity]"));
      alerts.forEach((alert) => {{
        const showAlert = severityFilter.value === "all" || alert.dataset.severity === severityFilter.value;
        alert.classList.toggle("hidden", !showAlert);
      }});
    }}

    function applyFilters() {{
      reorderVisibleElements();
      let count = 0;
      cards.forEach((card) => {{
        const show = matchesFilters(card);
        card.classList.toggle("hidden", !show);
        if (show) count += 1;
      }});
      panels.forEach((panel) => {{
        const show = matchesFilters(panel);
        panel.classList.toggle("hidden", !show);
        if (show) updatePanelInternals(panel);
      }});
      visibleCount.textContent = String(count);
    }}

    [marketplaceFilter, actionFilter, severityFilter, sortFilter].forEach((control) => {{
      control.addEventListener("change", applyFilters);
    }});
    searchFilter.addEventListener("input", applyFilters);

    applyFilters();
  </script>
</body>
</html>
"""


def write_dashboard(
    insights: list[SkuInsight],
    data_source_label: str | None = None,
    matcher_label: str | None = None,
) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    dashboard_path = REPORTS_DIR / "dashboard.html"
    dashboard_path.write_text(
        render_dashboard_html(
            insights,
            data_source_label=data_source_label,
            matcher_label=matcher_label,
        ),
        encoding="utf-8",
    )
    return dashboard_path


def write_alerts_csv(insights: list[SkuInsight]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = REPORTS_DIR / "alerts_inbox.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
      writer = csv.writer(handle)
      writer.writerow(
          [
              "severity",
              "sku",
              "book_title",
              "alert_title",
              "message",
              "recommended_action",
              "recommended_price",
              "expected_margin_pct",
          ]
      )
      for insight in insights:
          for alert in insight.alerts:
              writer.writerow(
                  [
                      alert.severity,
                      alert.sku,
                      insight.book.canonical_title,
                      alert.title,
                      alert.message,
                      insight.recommendation.action,
                      f"{insight.recommendation.recommended_price:.2f}",
                      f"{insight.recommendation.expected_margin_pct:.4f}",
                  ]
              )
    return csv_path


def build_sparkline_svg(values: list[float]) -> str:
    if not values:
        return ""
    width = 160
    height = 52
    min_value = min(values)
    max_value = max(values)
    spread = max(max_value - min_value, 1)
    points = []
    for index, value in enumerate(values):
        x = (width / max(len(values) - 1, 1)) * index
        y = height - (((value - min_value) / spread) * (height - 8)) - 4
        points.append(f"{x:.1f},{y:.1f}")
    polyline = " ".join(points)
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="price trend">'
        f'<polyline fill="none" stroke="#0f766e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="{polyline}" />'
        "</svg>"
    )
