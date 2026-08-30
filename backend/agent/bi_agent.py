from typing import Dict, Any, List
from backend.integrations.monday.client import MondayClient
from backend.agent.intent import parse_query_intent
from backend.data.models import BIQueryResult, BIQueryIntent
from backend.bi.calculations import (
    calculate_total_revenue,
    calculate_pipeline,
    calculate_sector_performance,
    calculate_delayed_work_orders,
    calculate_top_customers
)

class BIAgent:
    def __init__(self):
        self.monday_client = MondayClient()

    async def process_query(self, query: str) -> BIQueryResult:
        trace = []
        trace.append(f"Received User Query: '{query}'")

        # Step 1: Parse Intent
        intent = parse_query_intent(query)
        trace.append(f"Parsed Intent: metric='{intent.metric}', sector_filter='{intent.sector_filter}', time_filter='{intent.time_filter}'")

        # Step 2: Handle Clarification
        if intent.needs_clarification and intent.clarification_question:
            trace.append("Query is ambiguous. Triggering clarification mode.")
            return BIQueryResult(
                query=query,
                direct_answer=intent.clarification_question,
                intent=intent,
                key_numbers={},
                insights=["Please refine your query or choose an option above for more specific insights."],
                data_notes=[],
                execution_trace=trace
            )

        # Step 3: Fetch Data from Monday.com / Seed Layer
        deals, work_orders, quality = await self.monday_client.get_all_data()
        mode_label = "Live Monday.com GraphQL API" if quality.data_source_mode == "live_graphql" else "Local Seed Dataset Fallback"
        trace.append(f"Retrieved Data: {len(deals)} Deals, {len(work_orders)} Work Orders (Data Mode: {mode_label})")

        # Step 4: Execute Deterministic Metric Math
        key_numbers = {}
        insights = []
        direct_answer = ""
        supporting_data = []

        if intent.metric == "revenue":
            rev = calculate_total_revenue(work_orders, sector_filter=intent.sector_filter)
            key_numbers = rev
            sec_str = f" in the {intent.sector_filter} sector" if intent.sector_filter else ""
            direct_answer = (
                f"Total recorded revenue (excl. GST) from work orders{sec_str} is "
                f"₹{rev['total_revenue_excl_gst']:,.2f} across {rev['count']} work orders."
            )
            insights.append(f"Total billed value: ₹{rev['total_billed_excl_gst']:,.2f}.")
            insights.append(f"Total collected amount: ₹{rev['total_collected_incl_gst']:,.2f}.")
            if rev['missing_amount_count'] > 0:
                insights.append(f"Note: {rev['missing_amount_count']} work orders have unstated/missing revenue fields.")

        elif intent.metric == "pipeline":
            pipe = calculate_pipeline(deals, sector_filter=intent.sector_filter)
            key_numbers = pipe
            sec_str = f" for the {intent.sector_filter} sector" if intent.sector_filter else ""
            direct_answer = (
                f"Current active sales pipeline{sec_str} stands at "
                f"₹{pipe['total_pipeline_value']:,.2f} across {pipe['open_deals_count']} open deals "
                f"(Weighted Pipeline: ₹{pipe['weighted_pipeline_value']:,.2f})."
            )
            top_stages = pipe['deals_by_stage'][:3]
            for st in top_stages:
                insights.append(f"Stage '{st['stage']}': {st['count']} deals totaling ₹{st['value']:,.2f}")
            supporting_data = pipe['deals_by_stage']

        elif intent.metric == "delayed_work_orders":
            delays = calculate_delayed_work_orders(work_orders)
            key_numbers = delays
            direct_answer = (
                f"Currently, {delays['delayed_count']} out of {delays['total_work_orders']} work orders "
                f"({delays['delayed_percentage']}%) are delayed or requiring updates."
            )
            for item in delays['sample_delayed'][:4]:
                insights.append(f"WO '{item['deal_name']}' ({item['customer']}) in {item['sector']} sector - Status: {item['status']}")
            supporting_data = delays['sample_delayed']

        elif intent.metric == "top_customers":
            custs = calculate_top_customers(work_orders, top_n=5)
            key_numbers = {"top_customers_count": len(custs)}
            direct_answer = f"Top customer by total work order value is {custs[0]['customer']} with ₹{custs[0]['total_revenue']:,.2f}." if custs else "No customer data available."
            for idx, c in enumerate(custs, 1):
                insights.append(f"#{idx} {c['customer']} ({c['sector']}): ₹{c['total_revenue']:,.2f} across {c['work_orders_count']} work orders")
            supporting_data = custs

        elif intent.metric == "greeting":
            direct_answer = "Hello! I'm Skylark Drones' Business Intelligence Agent. I can help you analyze revenue, sales pipeline, work orders, customers, and sector performance. What would you like to know?"
            key_numbers = {"status": "greeting"}

        elif intent.metric == "unsupported_metric":
            direct_answer = "I can only answer questions based on Skylark Drones' available Monday.com business data, including revenue, sales pipeline, work orders, customers, and sector performance. I don't have data to answer that question."
            key_numbers = {"status": "unsupported_metric"}
            quality.quality_notes.append("Requested metric is outside the available Monday.com Deals and Work Orders datasets.")

        elif intent.metric == "sector_performance":
            sec_perf = calculate_sector_performance(deals, work_orders)
            key_numbers = {"total_sectors": len(sec_perf)}
            top_sec = sec_perf[0] if sec_perf else None
            direct_answer = (
                f"Top performing sector is {top_sec['sector']} with ₹{top_sec['revenue']:,.2f} in revenue "
                f"and ₹{top_sec['pipeline_value']:,.2f} in active pipeline."
            ) if top_sec else "No sector data."
            for s in sec_perf[:5]:
                insights.append(f"{s['sector']}: Revenue ₹{s['revenue']:,.2f} ({s['work_orders_count']} WOs) | Pipeline ₹{s['pipeline_value']:,.2f} ({s['open_deals_count']} open deals)")
            supporting_data = sec_perf

        else: # general_overview
            rev = calculate_total_revenue(work_orders)
            pipe = calculate_pipeline(deals)
            delays = calculate_delayed_work_orders(work_orders)
            key_numbers = {
                "total_revenue_excl_gst": rev['total_revenue_excl_gst'],
                "total_pipeline_value": pipe['total_pipeline_value'],
                "weighted_pipeline_value": pipe['weighted_pipeline_value'],
                "open_deals_count": pipe['open_deals_count'],
                "open_deals": pipe['open_deals_count'],
                "delayed_count": delays['delayed_count'],
                "delayed_work_orders": delays['delayed_count']
            }
            direct_answer = (
                f"Business Performance Summary: Total Work Order Revenue is ₹{rev['total_revenue_excl_gst']:,.2f}, "
                f"Active Sales Pipeline is ₹{pipe['total_pipeline_value']:,.2f} across {pipe['open_deals_count']} open deals, "
                f"and {delays['delayed_count']} work orders are currently delayed or flagged for updates."
            )
            insights.append(f"Total Billed (excl GST): ₹{rev['total_billed_excl_gst']:,.2f}")
            insights.append(f"Total Collected (incl GST): ₹{rev['total_collected_incl_gst']:,.2f}")
            insights.append(f"Weighted Sales Pipeline: ₹{pipe['weighted_pipeline_value']:,.2f}")

        trace.append("Completed deterministic calculations & response formatting.")

        return BIQueryResult(
            query=query,
            direct_answer=direct_answer,
            intent=intent,
            key_numbers=key_numbers,
            insights=insights,
            data_notes=quality.quality_notes,
            supporting_data=supporting_data,
            execution_trace=trace
        )
