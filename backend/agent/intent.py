import re
from typing import List, Optional
from backend.data.models import BIQueryIntent

SECTORS = ["Mining", "Renewable Energy", "Wind Energy", "Infrastructure", "Power & Utilities", "Agriculture", "Energy"]

UNSUPPORTED_KEYWORDS = [
    "attrition", "employee", "hr", "turnover", "hiring", "salary", "payroll",
    "ebitda", "p&l", "profit and loss", "net profit", "tax", "balance sheet",
    "cac", "customer acquisition cost", "marketing spend", "ad spend",
    "nps", "csat", "customer satisfaction", "feedback score",
    "drone fleet", "telemetry", "battery", "gps trace", "flight duration", "pilot salary",
    "weather", "joke", "president", "capital", "news", "stock", "python", "program", "code"
]

GREETING_KEYWORDS = [
    "hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "howdy",
    "who are you", "what can you do", "what do you do", "how can you help", "how can you help me", "help", "capabilities"
]

EXPLICIT_OVERVIEW_KEYWORDS = [
    "general summary", "overall summary", "business performance", "company overview",
    "how are we doing", "show me performance", "overall performance", "business overview", "summary", "overview"
]

def parse_query_intent(query: str) -> BIQueryIntent:
    q_lower = query.strip().lower()

    # 1. Check for explicit unsupported keywords first
    for kw in UNSUPPORTED_KEYWORDS:
        if kw in q_lower:
            return BIQueryIntent(metric="unsupported_metric", dimensions=[], needs_clarification=False)

    # 2. Check for greetings & capabilities
    words = re.findall(r'\w+', q_lower)
    if words and words[0] in ["hi", "hello", "hey", "greetings", "howdy"] and len(words) <= 3:
        return BIQueryIntent(metric="greeting", dimensions=[], needs_clarification=False)
    if q_lower in GREETING_KEYWORDS or any(k in q_lower for k in ["what do you do", "what can you do", "how can you help"]):
        return BIQueryIntent(metric="greeting", dimensions=[], needs_clarification=False)

    # 3. Identify Supported Domain Metrics
    metric = None
    if any(k in q_lower for k in ["pipeline", "deals", "funnel", "opportunity", "opportunities", "stage"]):
        metric = "pipeline"
    elif any(k in q_lower for k in ["revenue", "sales", "billed", "amount", "collection", "collected", "money", "income"]):
        metric = "revenue"
    elif any(k in q_lower for k in ["delayed", "delay", "bottleneck", "pending", "overdue", "hold"]):
        metric = "delayed_work_orders"
    elif any(k in q_lower for k in ["customer", "customers", "client", "clients", "account", "accounts"]):
        metric = "top_customers"
    elif any(k in q_lower for k in ["sector", "sectors", "industry", "industries", "service"]):
        metric = "sector_performance"
    elif any(k in q_lower for k in ["owner", "owners", "bd", "kam", "salesperson", "rep"]):
        metric = "owner_performance"
    elif any(k in q_lower for k in ["work order", "work orders", "wo", "execution", "tracker"]):
        metric = "work_orders"
    elif any(k in q_lower for k in EXPLICIT_OVERVIEW_KEYWORDS):
        metric = "general_overview"

    # If no supported domain metric or overview request was found -> Unsupported out-of-domain query
    if not metric:
        return BIQueryIntent(metric="unsupported_metric", dimensions=[], needs_clarification=False)

    # Identify Sector Filter
    sector_filter = None
    if any(k in q_lower for k in ["energy", "renewable", "renewables", "solar"]):
        sector_filter = "Renewable Energy"
    else:
        for sec in SECTORS:
            if sec.lower() in q_lower:
                sector_filter = sec
                break

    if sector_filter:
        from backend.data.normalizer import normalize_sector
        sector_filter = normalize_sector(sector_filter)

    # Identify Time Filter
    time_filter = None
    if "last month" in q_lower:
        time_filter = "last_month"
    elif "this month" in q_lower:
        time_filter = "this_month"
    elif "this quarter" in q_lower or any(q in q_lower for q in ["q1", "q2", "q3", "q4"]):
        time_filter = "this_quarter"
    elif "last year" in q_lower or "2025" in q_lower:
        time_filter = "2025"
    elif "this year" in q_lower or "2026" in q_lower:
        time_filter = "2026"

    # Ambiguity check
    needs_clarification = False
    clarification_q = None
    
    if query.strip().lower() in ["revenue", "show me revenue", "what is revenue", "pipeline", "show me pipeline"]:
        needs_clarification = True
        if "revenue" in q_lower:
            clarification_q = "Would you like to see total revenue, revenue broken down by sector, or top customers?"
        else:
            clarification_q = "Would you like total pipeline value, pipeline by deal stage, or pipeline by owner?"

    return BIQueryIntent(
        metric=metric,
        dimensions=["sector"] if sector_filter else [],
        time_filter=time_filter,
        sector_filter=sector_filter,
        needs_clarification=needs_clarification,
        clarification_question=clarification_q
    )
