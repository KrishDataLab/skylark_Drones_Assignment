# Architectural Specification — Skylark Drones BI Agent

## 1. Overview
The Skylark Drones Business Intelligence Agent is a full-stack decision-support system designed to query Monday.com boards (Work Orders & Deals) and answer founder-level queries deterministically without hallucination.

## 2. Core Design Principles
1. **Source of Truth**: Monday.com GraphQL API V2 is the primary data source (with local dataset seed fallback for evaluation).
2. **Deterministic Calculations**: Math functions for revenue, pipeline values, margin, and delay tracking are strictly isolated from LLM output.
3. **Data Quality Transparency**: Missing or unstated values are explicitly highlighted in every user response.
4. **Explainable Execution**: Every query generates an execution trace detailing the intent, extracted filters, records evaluated, and applied formulas.

## 3. Data Flow Diagram

```
[User Natural Language Query]
          │
          ▼
   [Intent & Filter Extraction]
   - Detects metric (revenue/pipeline/delays/customers/sectors)
   - Extracts filters (Sector: Mining, Time: Q1/Last Month)
   - Ambiguity check (Triggers clarification if intent is vague)
          │
          ▼
   [Monday.com Data Ingestion Layer]
   - GraphQL API V2 / Local Seed Fallback
   - Column Mapping & Schema Matching
          │
          ▼
   [Normalization & Data Quality Pipeline]
   - Cleans dirty numeric strings ("₹ 264,398.08" -> 264398.08)
   - Parses dates into YYYY-MM-DD
   - Standardizes sector & status strings
   - Flags missing values & missing dates
          │
          ▼
   [Deterministic BI Metrics Engine]
   - Revenue (Excl GST, Incl GST, Billed, Collected)
   - Pipeline Value (Gross & Weighted by probability)
   - Delayed Work Order detection
   - Sector & Account Rankings
          │
          ▼
   [Grounded Response Formatter]
   - Direct Answer
   - Key Numbers Widget
   - Contextual Insights & Recommendations
   - Data Quality Caveats
          │
          ▼
[React Dark Glassmorphism Interface + Leadership Export]
```

## 4. Layer Architecture

- `backend/api/`: FastAPI route controllers (`/chat`, `/health`, `/export/leadership-update`).
- `backend/agent/`: Intent parser, BI Agent orchestrator, and prompt templates.
- `backend/integrations/monday/`: GraphQL client for Monday.com API v2 with dynamic board parser and CSV seed engine.
- `backend/data/`: Data normalizer, Pydantic schemas, and quality tracker.
- `backend/bi/`: Pure mathematical calculation functions for financial and operational metrics.
- `frontend/`: React + Vite web dashboard with dark glassmorphic styling, trace inspection, and export options.
