from __future__ import annotations

from .pipeline import build_insights, get_data_source_label, get_matcher_label
from .reporting import write_alerts_csv, write_dashboard, write_reports


def main() -> None:
    insights = build_insights()
    data_source_label = get_data_source_label()
    matcher_label = get_matcher_label()
    markdown_path, json_path = write_reports(insights)
    dashboard_path = write_dashboard(
        insights,
        data_source_label=data_source_label,
        matcher_label=matcher_label,
    )
    alerts_csv_path = write_alerts_csv(insights)

    print("Real-Time Competitor Strategy Tracker")
    print("=" * 40)
    print(f"Marketplace source: {data_source_label}")
    print(f"Matcher strategy: {matcher_label}")
    action_summary = {
        "raise": sum(1 for insight in insights if insight.recommendation.action == "raise"),
        "lower": sum(1 for insight in insights if insight.recommendation.action == "lower"),
        "hold": sum(1 for insight in insights if insight.recommendation.action == "hold"),
    }
    print(f"SKUs monitored: {len(insights)}")
    print(f"Action summary: {action_summary}")
    print("Top pricing priorities:")

    ranked = sorted(
        insights,
        key=lambda insight: (
            len([alert for alert in insight.alerts if alert.severity == "high"]),
            abs(insight.recommendation.competitor_gap),
        ),
        reverse=True,
    )
    for insight in ranked[:12]:
        rec = insight.recommendation
        print(
            f"{insight.book.sku}: {rec.action.upper()} -> {rec.recommended_price:.2f} "
            f"(expected margin {rec.expected_margin_pct:.1%}, matches {len(insight.matches)})"
        )
        for alert in insight.alerts:
            print(f"  - [{alert.severity.upper()}] {alert.title}: {alert.message}")

    print()
    print(f"Markdown report: {markdown_path}")
    print(f"JSON report: {json_path}")
    print(f"HTML dashboard: {dashboard_path}")
    print(f"Alerts CSV: {alerts_csv_path}")


if __name__ == "__main__":
    main()
