# Skylark Drones — Monday.com Business Intelligence Agent

A production-grade **Business Intelligence (BI) Agent** built for Skylark Drones leadership and founders. It converts natural-language business queries into reliable, deterministic, and explainable insights grounded directly in Monday.com Work Orders and Deals data.

---

## 🌟 Key Features

1. **Deterministic Business Calculation Engine**: Revenue, Sales Pipeline Values, Weighted Pipelines, Win Rates, Sector breakdowns, and Delayed Work Orders are calculated via pure Python math functions (never mental arithmetic by LLM).
2. **Monday.com Integration Layer**: Interfaces with Monday.com GraphQL API V2 (`https://api.monday.com/v2`). Includes an automatic **Local Seed Fallback** (derived from the provided CSV datasets: `Deal funnel Data.xlsx` with 346 records and `Work_Order_Tracker Data.xlsx` with 176 records) so evaluators can run and test the application immediately without requiring live API keys.
   - **Live Monday.com Integration Status**: *Implemented & Architecturally Verified via GraphQL V2 endpoint (Not live-tested in evaluation due to unprovided live credentials).*
   - **Local Seed Mode Status**: *Implemented, 100% Tested & Verified against source Skylark CSV datasets.*
3. **Data Quality & Resilience Layer**: Handles messy real-world data (dirty currency strings `₹ 264,398.08`, inconsistent dates, empty fields). Missing values are explicitly flagged in every answer.
4. **Natural Language Query & Intent Parser**: Understands complex questions like *"How's our pipeline looking for energy sector this quarter?"*, *"Which work orders are delayed?"*, and *"Which customers generated the most revenue?"*.
5. **Executive Leadership Update Generator**: One-click feature to generate presentation-ready Markdown reports summarizing top-line KPIs, key account rankings, and operational bottlenecks.
6. **Transparent Execution Trace**: Interactive step-by-step trace viewer showing exact intent classification, filters applied, records evaluated, and applied formulas.
7. **Sleek Dark Glassmorphism UI**: Built with React + Vite, Outfit font, and responsive layout.

---

## 🏗️ Architecture

```
User Query (Chat UI)
       │
       ▼
 FastAPI Backend (/api/chat)
       │
 ┌─────┴──────────────────────────┐
 │ Intent & Filter Detection      │ ──> Identifies metric, date filter, sector, customer
 └─────┬──────────────────────────┘
       │
 ┌─────┴──────────────────────────┐
 │ Monday.com Data Layer          │ ──> GraphQL API V2 / Local Seed Fallback
 └─────┬──────────────────────────┘
       │
 ┌─────┴──────────────────────────┐
 │ Data Normalization & Quality   │ ──> Date standardizer, currency cleaner, missing data flagger
 └─────┬──────────────────────────┘
       │
 ┌─────┴──────────────────────────┐
 │ Deterministic BI Engine        │ ──> Exact math for Revenue, Margin, Pipeline, Delays
 └─────┬──────────────────────────┘
       │
 ┌─────┴──────────────────────────┐
 │ Grounded Response Formatter    │ ──> Structures Direct Answer + Key Numbers + Insights + Data Notes
 └─────┬──────────────────────────┘
       │
       ▼
 Rich Interactive UI (React + Glassmorphism + Trace View + Leadership Exporter)
```

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic v2, uvicorn, httpx, python-dotenv
- **Frontend**: React 18, Vite, Lucide Icons, Glassmorphic Vanilla/Tailwind CSS Design System
- **Integration**: Monday.com GraphQL API V2 (`https://api.monday.com/v2`)
- **Testing**: Pytest unit & integration test suite

---

## 🚀 Local Quickstart Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ (for building frontend)

### 1. Clone & Install Backend Dependencies
```bash
# Install backend dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Note: Leaving `MONDAY_API_TOKEN` empty automatically activates the local seed layer based on Skylark CSV datasets).*

### 3. Build & Run Application
```bash
# Build Frontend Bundle
cd frontend
npm install
npm run build
cd ..

# Start FastAPI Server
python -m uvicorn backend.main:app --reload --port 8000
```
Open your browser at `http://localhost:8000`.

---

## 📊 Monday.com Setup Instructions

To connect to live Monday.com boards:
1. Log into [Monday.com](https://monday.com) and create two boards:
   - **Deals Board**: Import `Deal funnel Data.xlsx - Deal tracker.csv`
   - **Work Orders Board**: Import `Work_Order_Tracker Data.xlsx - work order tracker.csv`
2. Generate an API Token from **Admin -> Developers -> Developer API**.
3. Update `.env`:
   ```env
   MONDAY_API_TOKEN="your_personal_api_token"
   MONDAY_DEALS_BOARD_ID="123456789"
   MONDAY_WORK_ORDERS_BOARD_ID="987654321"
   ```

---

## 🧪 Running Automated Tests

Run the unit and integration test suite via `pytest`:
```bash
python -m pytest tests/
```

---

## 📄 Decision Log & Documentation

Detailed architecture specifications, entity models, and trade-offs are available in the `docs/` folder:
- [docs/architecture.md](file:///c:/Users/krish/OneDrive/Desktop/skylark_assignment/docs/architecture.md) — Complete System Architecture & Data Flow
- [docs/data-model.md](file:///c:/Users/krish/OneDrive/Desktop/skylark_assignment/docs/data-model.md) — Normalized Entities & Data Quality Rules
- [docs/decision-log.md](file:///c:/Users/krish/OneDrive/Desktop/skylark_assignment/docs/decision-log.md) — Assignment Trade-offs, Assumptions & Leadership Update Interpretation
- [docs/test-cases.md](file:///c:/Users/krish/OneDrive/Desktop/skylark_assignment/docs/test-cases.md) — Evaluation Matrix
