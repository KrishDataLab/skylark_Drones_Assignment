import os
import csv
from typing import List, Tuple
from backend.data.models import Deal, WorkOrder, DataQualitySummary
from backend.data.normalizer import parse_float, parse_date, normalize_sector, normalize_status

DEALS_CSV = "Deal funnel Data.xlsx - Deal tracker.csv"
WORK_ORDERS_CSV = "Work_Order_Tracker Data.xlsx - work order tracker.csv"

def load_seed_data(base_path: str = ".") -> Tuple[List[Deal], List[WorkOrder], DataQualitySummary]:
    deals: List[Deal] = []
    work_orders: List[WorkOrder] = []
    
    deals_missing_val = 0
    wo_missing_amt = 0
    wo_missing_dates = 0
    
    # Load Deals
    deals_path = os.path.join(base_path, DEALS_CSV)
    if os.path.exists(deals_path):
        with open(deals_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
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
                
    # Load Work Orders
    wo_path = os.path.join(base_path, WORK_ORDERS_CSV)
    if os.path.exists(wo_path):
        with open(wo_path, mode="r", encoding="utf-8-sig") as f:
            all_rows = list(csv.reader(f))
            header_idx = 0
            while header_idx < len(all_rows) and not any(all_rows[header_idx]):
                header_idx += 1
            if header_idx < len(all_rows):
                headers = [h.strip() for h in all_rows[header_idx]]
                for idx, row_vals in enumerate(all_rows[header_idx+1:]):
                    if not any(row_vals):
                        continue
                    row = dict(zip(headers, row_vals))
                    amt_excl, missing_amt = parse_float(row.get("Amount in Rupees (Excl of GST) (Masked)"))
                    amt_incl, _ = parse_float(row.get("Amount in Rupees (Incl of GST) (Masked)"))
                    billed_excl, _ = parse_float(row.get("Billed Value in Rupees (Excl of GST.) (Masked)"))
                    billed_incl, _ = parse_float(row.get("Billed Value in Rupees (Incl of GST.) (Masked)"))
                    collected_incl, _ = parse_float(row.get("Collected Amount in Rupees (Incl of GST.) (Masked)"))
                    to_be_billed, _ = parse_float(row.get("Amount to be billed in Rs. (Exl. of GST) (Masked)"))
                    receivable, _ = parse_float(row.get("Amount Receivable (Masked)"))
                    
                    if missing_amt:
                        wo_missing_amt += 1
                    
                    delivery_date = parse_date(row.get("Data Delivery Date"))
                    if not delivery_date:
                        wo_missing_dates += 1
                        
                    wo = WorkOrder(
                        id=f"WO-{idx+1:04d}",
                        deal_name=row.get("Deal name masked", f"WorkOrder {idx+1}").strip(),
                        customer_name_code=row.get("Customer Name Code", "").strip() or None,
                        serial_num=row.get("Serial #", "").strip() or None,
                        nature_of_work=row.get("Nature of Work", "").strip() or None,
                        execution_status=normalize_status(row.get("Execution Status")),
                        data_delivery_date=delivery_date,
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

    notes = []
    if deals_missing_val > 0:
        notes.append(f"{deals_missing_val} deals have missing financial deal values.")
    if wo_missing_amt > 0:
        notes.append(f"{wo_missing_amt} work orders have missing base amount values.")
    if wo_missing_dates > 0:
        notes.append(f"{wo_missing_dates} work orders lack data delivery dates.")

    quality = DataQualitySummary(
        total_deals=len(deals),
        total_work_orders=len(work_orders),
        deals_missing_value=deals_missing_val,
        work_orders_missing_amount=wo_missing_amt,
        work_orders_missing_dates=wo_missing_dates,
        quality_notes=notes
    )

    return deals, work_orders, quality
