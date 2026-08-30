import sys
import asyncio
import json

sys.stdout.reconfigure(encoding='utf-8')

from backend.agent.bi_agent import BIAgent

async def run_5_queries():
    agent = BIAgent()
    queries = [
        "1. What is our current sales pipeline?",
        "2. How's our pipeline looking for energy sector this quarter?",
        "3. What is our total revenue in mining sector?",
        "4. Which work orders are delayed?",
        "5. What do you do?"
    ]

    for q in queries:
        raw_q = q.split(". ", 1)[1]
        res = await agent.process_query(raw_q)
        print(f"### {q}")
        print(f"**Answer**: {res.direct_answer}\n")
        if res.insights:
            print("**Key Insights**:")
            for ins in res.insights[:3]:
                print(f"- {ins}")
            print()
        if res.data_notes:
            print("**Data Quality Notes**:")
            for note in res.data_notes[:2]:
                print(f"- ⚠️ {note}")
            print()
        print("---")
        print()

if __name__ == "__main__":
    asyncio.run(run_5_queries())
