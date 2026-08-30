# Decision Log — Skylark Drones BI Agent

## 1. Key Assumptions Made
1. **Monday.com Integration**: We assume Monday.com boards use standard column naming for Deals and Work Orders. To guarantee that the agent is immediately testable by evaluators without manual Monday API setup, we implemented an automatic fallback to local dataset seed files (`Deal funnel Data.xlsx` and `Work_Order_Tracker Data.xlsx`). When `MONDAY_API_TOKEN` is supplied, the agent automatically switches to live GraphQL API queries.
2. **Revenue Calculation**: Work Order `Amount in Rupees (Excl of GST)` is treated as top-line contract revenue. Billed Value and Collected Amounts are tracked separately to provide visibility into cash flow and receivables.
3. **Pipeline Probability**: Pipeline deal weighting assigns standard probabilities: High = 80%, Medium = 50%, Low = 20%.

## 2. Trade-offs Chosen and Rationale

| Decision Area | Chosen Approach | Alternative Considered | Rationale |
|---|---|---|---|
| **Data Calculation** | Pure Deterministic Python Math | Direct LLM Mental Math | LLMs hallucinate numbers and struggle with large dataset aggregations. Deterministic math ensures 100% accuracy and auditability. |
| **Monday Integration** | Live GraphQL Client + Seed Fallback | Live API Only | Live GraphQL V2 client is fully implemented, but fallback to local seed data ensures zero-friction evaluation when live credentials are not supplied. |
| **Agent Architecture** | Single Intent-Driven BI Agent | Multi-Agent Swarm | A single structured pipeline (Intent -> Retrieval -> Calculation -> Grounding) is faster, less prone to inter-agent handoff failures, and easier to debug. |
| **UI Design** | React Dark Glassmorphic UI + Trace Modal | Plain CLI / Standard Admin Table | Founders require clean, high-impact executive dashboards with instant query chips and full mathematical transparency. |

## 3. Interpretation of "Leadership Updates"
We interpreted "Leadership Updates" as an executive decision-support feature that automatically synthesizes top-line revenue, pipeline health, top key accounts, operational delays, and data quality warnings into a clean, presentation-ready Markdown & PDF report. 

This enables founders and department heads to generate one-click status reports for board meetings or team syncs without manual copying of numbers.

## 4. What We Would Do Differently With More Time
1. **Real-time Webhook Ingestion**: Implement Monday.com Webhooks so that board updates immediately trigger push invalidation of local caches.
2. **Custom DAX/SQL Metric Builder**: Build a visual metric builder allowing founders to save custom formulas (e.g. `Customer Lifetime Value`, `Pilot Utilization Index`).
3. **Multi-board Joins**: Add advanced graph-based joins between Deals and Work Orders using dynamic fuzzy client name matching.
