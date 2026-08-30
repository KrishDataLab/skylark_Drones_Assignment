import os
import json
from typing import List, Tuple
from backend.data.models import Deal, WorkOrder, DataQualitySummary
from backend.data.normalizer import parse_float, parse_date, normalize_sector, normalize_status

def load_seed_data(base_path: str = ".") -> Tuple[List[Deal], List[WorkOrder], DataQualitySummary]:
    deals: List[Deal] = []
    work_orders: List[WorkOrder] = []
    
    # Locate seed_records.json
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "seed_records.json")
    if not os.path.exists(json_path):
        json_path = os.path.join(base_path, "seed_records.json")
    
    raw_deals = []
    raw_wos = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            raw_deals = data.get("deals", [])
            raw_wos = data.get("work_orders", [])
            
    deals_missing_val = 0
    wo_missing_amt = 0
    wo_missing_dates = 0
    
    for idx, row in enumerate(raw_deals):
        val, missing_val = parse_float(row.get("Masked Deal value"))
        if missing_val:
            deals_missing_val += 1
            
        deal = Deal(
            id=f"DEAL-{idx+1:04d}",
            deal_name=row.get("Deal Name", f"Deal {idx+1}").strip(),
            owner_code=row.get("Owner code", "").strip() or None,
            client_code=row.get("Client Code", "").strip() or None,
            deal_status=normalize_status(row.get("Deal Status")),
            close_date_actual=parse_date(row.get("Close Date (A)")),
            closure_probability=row.get("Closure Probability", "").strip() or None,
            masked_deal_value=val or 0.0,
            tentative_close_date=parse_date(row.get("Tentative Close Date")),
            deal_stage=row.get("Deal Stage", "").strip() or None,
            product_deal=row.get("Product deal", "").strip() or None,
            sector=normalize_sector(row.get("Sector/service")),
            created_date=parse_date(row.get("Created Date")),
            raw_record=row
        )
        deals.append(deal)
        
    for idx, row in enumerate(raw_wos):
        amt_excl, missing_amt = parse_float(row.get("Amount in Rupees (Excl of GST) (Masked)"))
        amt_incl, _ = parse_float(row.get("Amount in Rupees (Incl of GST) (Masked)"))
        billed_excl, _ = parse_float(row.get("Billed Value in Rupees (Excl of GST.) (Masked)"))
        billed_incl, _ = parse_float(row.get("Billed Value in Rupees (Incl of GST.) (Masked)"))
        collected_incl, _ = parse_float(row.get("Collected Amount in Rupees (Incl of GST.) (Masked)"))
        to_be_billed, _ = parse_float(row.get("Amount to be billed in Rs. (Exl. of GST) (Masked)"))
        receivable, _ = parse_float(row.get("Amount Receivable (Masked)"))
        
        deliv_date = parse_date(row.get("Data Delivery Date"))
        if missing_amt:
            wo_missing_amt += 1
        if not deliv_date:
            wo_missing_dates += 1
            
        wo = WorkOrder(
            id=f"WO-{idx+1:04d}",
            deal_name=row.get("Deal name masked", f"Work Order {idx+1}").strip(),
            customer_name_code=row.get("Customer Name Code", "").strip() or None,
            serial_num=row.get("Serial #", "").strip() or None,
            nature_of_work=row.get("Nature of Work", "").strip() or None,
            execution_status=normalize_status(row.get("Execution Status")),
            data_delivery_date=deliv_date,
            date_of_po_loi=parse_date(row.get("Date of PO/LOI")),
            probable_start_date=parse_date(row.get("Probable Start Date")),
            probable_end_date=parse_date(row.get("Probable End Date")),
            owner_code=row.get("BD/KAM Personnel code", "").strip() or None,
            sector=normalize_sector(row.get("Sector")),
            type_of_work=row.get("Type of Work", "").strip() or None,
            skylark_software_used=row.get("Is any Skylark software platform part of the client deliverables in this deal?", "").strip() or None,
            amount_excl_gst=amt_excl or 0.0,
            amount_incl_gst=amt_incl or 0.0,
            billed_value_excl_gst=billed_excl or 0.0,
            billed_value_incl_gst=billed_incl or 0.0,
            collected_amount_incl_gst=collected_incl or 0.0,
            amount_to_be_billed_excl_gst=to_be_billed or 0.0,
            amount_receivable=receivable or 0.0,
            invoice_status=row.get("Invoice Status", "").strip() or None,
            billing_status=row.get("Billing Status", "").strip() or None,
            collection_status=row.get("Collection status", "").strip() or None,
            raw_record=row
        )
        work_orders.append(wo)
        
    summary = DataQualitySummary(
        total_deals=len(deals),
        total_work_orders=len(work_orders),
        deals_missing_value=deals_missing_val,
        work_orders_missing_amount=wo_missing_amt,
        work_orders_missing_dates=wo_missing_dates,
        data_source_mode="seed_data_fallback",
        quality_notes=[
            f"Note: {deals_missing_val} out of {len(deals)} deals in the assignment dataset have missing/unstated deal values.",
            f"Note: {wo_missing_amt} out of {len(work_orders)} work orders have unstated base revenue amounts."
        ]
    )
    
    return deals, work_orders, summary
