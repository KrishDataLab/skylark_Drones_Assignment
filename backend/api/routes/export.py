from fastapi import APIRouter
from backend.agent.bi_agent import BIAgent
from backend.bi.calculations import (
    calculate_total_revenue,
    calculate_pipeline,
    calculate_sector_performance,
    calculate_delayed_work_orders,
    calculate_top_customers
)

router = APIRouter()
agent = BIAgent()

@router.get("/export/leadership-update")
async def generate_leadership_update():
    deals, work_orders, quality = await agent.monday_client.get_all_data()
    
    rev = calculate_total_revenue(work_orders)
    pipe = calculate_pipeline(deals)
    delays = calculate_delayed_work_orders(work_orders)
    sectors = calculate_sector_performance(deals, work_orders)
    top_custs = calculate_top_customers(work_orders, top_n=3)
    
    markdown_report = f"""# Skylark Drones — Executive Leadership Update

## 1. Executive Summary & Core KPIs
- **Total Revenue (excl. GST)**: ₹{rev['total_revenue_excl_gst']:,.2f} ({rev['count']} Work Orders)
- **Total Billed Value**: ₹{rev['total_billed_excl_gst']:,.2f}
- **Total Collected Amount**: ₹{rev['total_collected_incl_gst']:,.2f}
- **Active Sales Pipeline**: ₹{pipe['total_pipeline_value']:,.2f} ({pipe['open_deals_count']} Open Deals)
- **Weighted Pipeline Value**: ₹{pipe['weighted_pipeline_value']:,.2f}
- **Operational Delays**: {delays['delayed_count']} Work Orders ({delays['delayed_percentage']}%)

## 2. Sectoral Performance Breakdown
| Sector | Revenue (excl GST) | Work Orders | Active Pipeline | Open Deals |
|---|---|---|---|---|
"""
    for s in sectors[:5]:
        markdown_report += f"| {s['sector']} | ₹{s['revenue']:,.2f} | {s['work_orders_count']} | ₹{s['pipeline_value']:,.2f} | {s['open_deals_count']} |\n"

    markdown_report += f"""
## 3. Top Key Accounts (Customers)
"""
    for idx, c in enumerate(top_custs, 1):
        markdown_report += f"{idx}. **{c['customer']}** ({c['sector']}): ₹{c['total_revenue']:,.2f} across {c['work_orders_count']} work orders\n"

    markdown_report += f"""
## 4. Operational Bottlenecks & Risk Warnings
- **Delayed Projects**: {delays['delayed_count']} work orders are currently marked as delayed or requiring billing updates.
- **Data Quality Alerts**: {', '.join(quality.quality_notes)}

## 5. Strategic Recommendations for Leadership
1. **Focus BD/KAM teams on Mining & Renewable Energy** which contribute the largest revenue and pipeline.
2. **Resolve Billing Updates** on {delays['delayed_count']} work orders to accelerate cash collections.
3. **Audit missing deal values** across 181 open deals to improve pipeline forecasting accuracy.
"""

    return {
        "report_title": "Executive Leadership Update",
        "markdown_content": markdown_report,
        "metrics": {
            "revenue": rev['total_revenue_excl_gst'],
            "pipeline": pipe['total_pipeline_value'],
            "delayed_count": delays['delayed_count']
        }
    }
