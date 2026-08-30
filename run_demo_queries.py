import sys
import asyncio
import json

# Ensure UTF-8 output encoding for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

from backend.agent.bi_agent import BIAgent
from backend.api.routes.export import generate_leadership_update

async def run_all_queries():
    agent = BIAgent()
    queries = [
        "What is our overall business performance?",
        "What is our total revenue in mining sector?",
        "How is our pipeline looking for energy sector this quarter?",
        "Which work orders are delayed?",
        "Which customers generated the most revenue?",
        "Show me pipeline by deal stage",
        "Show me revenue",  # Ambiguity test
        "What is our employee attrition?"  # Unsupported query / Hallucination test
    ]

    print("=" * 80)
    print("      SKYLARK DRONES MONDAY.COM BI AGENT — LIVE DEMO RESULTS")
    print("=" * 80)
    print()

    for idx, q in enumerate(queries, 1):
        print(f"--- QUERY {idx}: '{q}' ---")
        res = await agent.process_query(q)
        print(f"Direct Answer : {res.direct_answer}")
        print(f"Intent Metric : {res.intent.metric} | Filter: {res.intent.sector_filter or 'None'}")
        if res.key_numbers:
            print(f"Key Numbers   : {json.dumps(res.key_numbers)}")
        if res.insights:
            print("Insights      :")
            for ins in res.insights[:3]:
                print(f"  • {ins}")
        if res.data_notes:
            print("Data Notes    :")
            for note in res.data_notes[:2]:
                print(f"  ⚠️ {note}")
        print("Trace Steps   :")
        for step in res.execution_trace:
            print(f"  [TRACE] {step}")
        print("-" * 80)
        print()

    print("=" * 80)
    print("      EXECUTIVE LEADERSHIP UPDATE GENERATOR REPORT")
    print("=" * 80)
    rep = await generate_leadership_update()
    print(rep["markdown_content"])
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_all_queries())
