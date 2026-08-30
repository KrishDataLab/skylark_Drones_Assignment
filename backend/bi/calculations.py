from typing import List, Dict, Any, Optional
from collections import defaultdict
from backend.data.models import Deal, WorkOrder
from backend.data.normalizer import normalize_sector

def calculate_total_revenue(
    work_orders: List[WorkOrder],
    sector_filter: Optional[str] = None,
    customer_filter: Optional[str] = None,
    owner_filter: Optional[str] = None
) -> Dict[str, Any]:
    filtered = work_orders
    if sector_filter:
        norm_filter = normalize_sector(sector_filter).lower()
        filtered = [w for w in filtered if w.sector and (normalize_sector(w.sector).lower() == norm_filter or norm_filter in normalize_sector(w.sector).lower())]
    if customer_filter:
        filtered = [w for w in filtered if w.customer_name_code and w.customer_name_code.lower() == customer_filter.lower()]
    if owner_filter:
        filtered = [w for w in filtered if w.owner_code and w.owner_code.lower() == owner_filter.lower()]

    total_amount_excl_gst = sum(w.amount_excl_gst for w in filtered if w.amount_excl_gst)
    total_amount_incl_gst = sum(w.amount_incl_gst for w in filtered if w.amount_incl_gst)
    total_billed_excl_gst = sum(w.billed_value_excl_gst for w in filtered if w.billed_value_excl_gst)
    total_collected_incl_gst = sum(w.collected_amount_incl_gst for w in filtered if w.collected_amount_incl_gst)
    total_receivable = sum(w.amount_receivable for w in filtered if w.amount_receivable)
    
    missing_amount_count = sum(1 for w in filtered if not w.amount_excl_gst)

    return {
        "count": len(filtered),
        "total_revenue_excl_gst": round(total_amount_excl_gst, 2),
        "total_revenue_incl_gst": round(total_amount_incl_gst, 2),
        "total_billed_excl_gst": round(total_billed_excl_gst, 2),
        "total_collected_incl_gst": round(total_collected_incl_gst, 2),
        "total_receivable": round(total_receivable, 2),
        "missing_amount_count": missing_amount_count
    }

def calculate_pipeline(
    deals: List[Deal],
    sector_filter: Optional[str] = None,
    owner_filter: Optional[str] = None,
    stage_filter: Optional[str] = None
) -> Dict[str, Any]:
    filtered = deals
    if sector_filter:
        norm_filter = normalize_sector(sector_filter).lower()
        filtered = [d for d in filtered if d.sector and (normalize_sector(d.sector).lower() == norm_filter or norm_filter in normalize_sector(d.sector).lower())]
    if owner_filter:
        filtered = [d for d in filtered if d.owner_code and d.owner_code.lower() == owner_filter.lower()]
    if stage_filter:
        filtered = [d for d in filtered if d.deal_stage and stage_filter.lower() in d.deal_stage.lower()]

    open_deals = [d for d in filtered if d.deal_status and d.deal_status.lower() == "open"]
    won_deals = [d for d in filtered if d.deal_status and "won" in d.deal_status.lower()]

    total_pipeline_val = sum(d.masked_deal_value for d in open_deals if d.masked_deal_value)
    
    # Probability weights
    prob_weights = {"high": 0.8, "medium": 0.5, "low": 0.2}
    weighted_val = 0.0
    for d in open_deals:
        prob = (d.closure_probability or "medium").lower()
        w = prob_weights.get(prob, 0.5)
        weighted_val += (d.masked_deal_value or 0.0) * w

    # Breakdown by stage
    by_stage = defaultdict(lambda: {"count": 0, "value": 0.0})
    for d in open_deals:
        stage = d.deal_stage or "Unspecified Stage"
        by_stage[stage]["count"] += 1
        by_stage[stage]["value"] += (d.masked_deal_value or 0.0)

    stage_list = [{"stage": k, "count": v["count"], "value": round(v["value"], 2)} for k, v in by_stage.items()]
    stage_list.sort(key=lambda x: x["value"], reverse=True)

    missing_val_count = sum(1 for d in open_deals if not d.masked_deal_value)

    return {
        "total_deals_count": len(filtered),
        "open_deals_count": len(open_deals),
        "won_deals_count": len(won_deals),
        "total_pipeline_value": round(total_pipeline_val, 2),
        "weighted_pipeline_value": round(weighted_val, 2),
        "deals_by_stage": stage_list,
        "missing_value_count": missing_val_count
    }

def calculate_sector_performance(deals: List[Deal], work_orders: List[WorkOrder]) -> List[Dict[str, Any]]:
    sectors = defaultdict(lambda: {"revenue": 0.0, "work_orders_count": 0, "pipeline_value": 0.0, "open_deals_count": 0})

    for w in work_orders:
        sec = w.sector or "Unspecified"
        sectors[sec]["revenue"] += (w.amount_excl_gst or 0.0)
        sectors[sec]["work_orders_count"] += 1

    for d in deals:
        if d.deal_status and d.deal_status.lower() == "open":
            sec = d.sector or "Unspecified"
            sectors[sec]["pipeline_value"] += (d.masked_deal_value or 0.0)
            sectors[sec]["open_deals_count"] += 1

    res = []
    for sec, data in sectors.items():
        res.append({
            "sector": sec,
            "revenue": round(data["revenue"], 2),
            "work_orders_count": data["work_orders_count"],
            "pipeline_value": round(data["pipeline_value"], 2),
            "open_deals_count": data["open_deals_count"]
        })
    res.sort(key=lambda x: x["revenue"] + x["pipeline_value"], reverse=True)
    return res

def calculate_delayed_work_orders(work_orders: List[WorkOrder]) -> Dict[str, Any]:
    delayed = []
    for w in work_orders:
        status_lower = (w.execution_status or "").lower()
        if "delay" in status_lower or "hold" in status_lower:
            delayed.append(w)
        elif status_lower not in ["completed", "closed"]:
            # Check if dates imply delay or bottleneck
            if w.billing_status and "update required" in w.billing_status.lower():
                delayed.append(w)

    return {
        "delayed_count": len(delayed),
        "total_work_orders": len(work_orders),
        "delayed_percentage": round((len(delayed) / len(work_orders) * 100), 1) if work_orders else 0.0,
        "sample_delayed": [
            {
                "id": w.id,
                "deal_name": w.deal_name,
                "customer": w.customer_name_code,
                "status": w.execution_status,
                "amount": w.amount_excl_gst,
                "sector": w.sector,
                "owner": w.owner_code
            }
            for w in delayed[:10]
        ]
    }

def calculate_top_customers(work_orders: List[WorkOrder], top_n: int = 5) -> List[Dict[str, Any]]:
    cust_map = defaultdict(lambda: {"total_revenue": 0.0, "work_orders_count": 0, "sector": "Unspecified"})
    for w in work_orders:
        c = w.customer_name_code or "Unknown Customer"
        cust_map[c]["total_revenue"] += (w.amount_excl_gst or 0.0)
        cust_map[c]["work_orders_count"] += 1
        if w.sector:
            cust_map[c]["sector"] = w.sector

    res = [
        {
            "customer": k,
            "total_revenue": round(v["total_revenue"], 2),
            "work_orders_count": v["work_orders_count"],
            "sector": v["sector"]
        }
        for k, v in cust_map.items()
    ]
    res.sort(key=lambda x: x["total_revenue"], reverse=True)
    return res[:top_n]
