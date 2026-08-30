# Test Cases Matrix — Skylark Drones BI Agent

## Evaluation Query Test Suite

| Test ID | Category | Sample Query | Expected Data Source | Expected Metric / Answer |
|---|---|---|---|---|
| `TC-01` | Overall Business | *"How is our overall business performing?"* | Work Orders + Deals | Total Revenue, Total Pipeline, Delayed Work Order count |
| `TC-02` | Sector Revenue | *"What is our total revenue in mining sector?"* | Work Orders | Total Revenue for Mining sector (Excl GST) |
| `TC-03` | Sector Pipeline | *"How is our pipeline looking for energy sector this quarter?"* | Deals | Pipeline Value for Renewable Energy sector |
| `TC-04` | Operational Delays | *"Which work orders are delayed?"* | Work Orders | List of delayed work orders and percentage |
| `TC-05` | Key Accounts | *"Which customers generated the most revenue?"* | Work Orders | Top 5 customers ranked by revenue |
| `TC-06` | Stage Breakdown | *"Show me pipeline by deal stage"* | Deals | Breakdown of open deals by stage |
| `TC-07` | Ambiguity Handling | *"Show me revenue"* | System Rules | Triggers clarification question asking for dimension |
| `TC-08` | Missing Data Caveats | Any query on incomplete records | Data Flagger | Explicit note regarding missing revenue/deal values |
| `TC-09` | Leadership Export | GET `/api/export/leadership-update` | Export Route | Generated Markdown executive update |
