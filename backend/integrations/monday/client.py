import httpx
from typing import List, Tuple, Dict, Any, Optional
from backend.config.settings import settings
from backend.data.models import Deal, WorkOrder, DataQualitySummary
from backend.integrations.monday.mock_seed import load_seed_data
from backend.data.normalizer import parse_float, parse_date, normalize_sector, normalize_status

MONDAY_API_URL = "https://api.monday.com/v2"

class MondayClient:
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or settings.monday_api_token
        self.deals_board_id = settings.monday_deals_board_id
        self.work_orders_board_id = settings.monday_work_orders_board_id

    async def fetch_board_items(self, board_id: str) -> List[Dict[str, Any]]:
        if not self.api_token or not board_id:
            return []
        
        query = """
        query ($board_id: [ID!]) {
          boards (ids: $board_id) {
            id
            name
            items_page {
              items {
                id
                name
                column_values {
                  id
                  title
                  text
                  value
                }
              }
            }
          }
        }
        """
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                MONDAY_API_URL,
                headers={
                    "Authorization": self.api_token,
                    "Content-Type": "application/json"
                },
                json={"query": query, "variables": {"board_id": [board_id]}},
                timeout=10.0
            )
            resp.raise_for_status()
            data = resp.json()
            boards = data.get("data", {}).get("boards", [])
            if not boards:
                return []
            items = boards[0].get("items_page", {}).get("items", [])
            return items

    async def get_all_data(self) -> Tuple[List[Deal], List[WorkOrder], DataQualitySummary]:
        # If no credentials set, use local seed data automatically
        if not self.api_token or not self.deals_board_id or not self.work_orders_board_id:
            return load_seed_data()
        
        try:
            raw_deals = await self.fetch_board_items(self.deals_board_id)
            raw_wos = await self.fetch_board_items(self.work_orders_board_id)
            
            if not raw_deals or not raw_wos:
                # Fallback to seed data if Monday API returns empty or board not found
                return load_seed_data()
            
            # Map raw Monday GraphQL items to Deals & Work Orders
            deals: List[Deal] = []
            for item in raw_deals:
                cols = {c.get("title", ""): c.get("text", "") for c in item.get("column_values", [])}
                val, _ = parse_float(cols.get("Masked Deal value") or cols.get("Deal Value"))
                deal = Deal(
                    id=item.get("id"),
                    deal_name=item.get("name"),
                    owner_code=cols.get("Owner code") or cols.get("Owner"),
                    client_code=cols.get("Client Code") or cols.get("Client"),
                    deal_status=normalize_status(cols.get("Deal Status") or cols.get("Status")),
                    close_date_actual=parse_date(cols.get("Close Date (A)")),
                    closure_probability=cols.get("Closure Probability"),
                    masked_deal_value=val or 0.0,
                    tentative_close_date=parse_date(cols.get("Tentative Close Date")),
                    deal_stage=cols.get("Deal Stage") or cols.get("Stage"),
                    product_deal=cols.get("Product deal"),
                    sector=normalize_sector(cols.get("Sector/service") or cols.get("Sector")),
                    created_date=parse_date(cols.get("Created Date"))
                )
                deals.append(deal)
                
            work_orders: List[WorkOrder] = []
            for item in raw_wos:
                cols = {c.get("title", ""): c.get("text", "") for c in item.get("column_values", [])}
                amt_excl, _ = parse_float(cols.get("Amount in Rupees (Excl of GST) (Masked)") or cols.get("Amount"))
                amt_incl, _ = parse_float(cols.get("Amount in Rupees (Incl of GST) (Masked)"))
                billed_excl, _ = parse_float(cols.get("Billed Value in Rupees (Excl of GST.) (Masked)"))
                billed_incl, _ = parse_float(cols.get("Billed Value in Rupees (Incl of GST.) (Masked)"))
                collected_incl, _ = parse_float(cols.get("Collected Amount in Rupees (Incl of GST.) (Masked)"))
                to_be_billed, _ = parse_float(cols.get("Amount to be billed in Rs. (Exl. of GST) (Masked)"))
                receivable, _ = parse_float(cols.get("Amount Receivable (Masked)"))
                
                wo = WorkOrder(
                    id=item.get("id"),
                    deal_name=item.get("name"),
                    customer_name_code=cols.get("Customer Name Code") or cols.get("Customer"),
                    serial_num=cols.get("Serial #"),
                    nature_of_work=cols.get("Nature of Work"),
                    execution_status=normalize_status(cols.get("Execution Status") or cols.get("Status")),
                    data_delivery_date=parse_date(cols.get("Data Delivery Date")),
                    date_of_po_loi=parse_date(cols.get("Date of PO/LOI")),
                    probable_start_date=parse_date(cols.get("Probable Start Date")),
                    probable_end_date=parse_date(cols.get("Probable End Date")),
                    owner_code=cols.get("BD/KAM Personnel code"),
                    sector=normalize_sector(cols.get("Sector")),
                    type_of_work=cols.get("Type of Work"),
                    skylark_software_used=cols.get("Is any Skylark software platform part of the client deliverables in this deal?"),
                    amount_excl_gst=amt_excl or 0.0,
                    amount_incl_gst=amt_incl or 0.0,
                    billed_value_excl_gst=billed_excl or 0.0,
                    billed_value_incl_gst=billed_incl or 0.0,
                    collected_amount_incl_gst=collected_incl or 0.0,
                    amount_to_be_billed_excl_gst=to_be_billed or 0.0,
                    amount_receivable=receivable or 0.0,
                    invoice_status=cols.get("Invoice Status"),
                    billing_status=cols.get("Billing Status"),
                    collection_status=cols.get("Collection status")
                )
                work_orders.append(wo)
                
            return deals, work_orders, DataQualitySummary(
                total_deals=len(deals),
                total_work_orders=len(work_orders),
                data_source_mode="live_graphql",
                quality_notes=["Loaded directly from live Monday.com GraphQL API V2."]
            )
        except Exception as e:
            # On network error or bad API response, safely fallback to seed data
            deals, wos, summary = load_seed_data()
            summary.data_source_mode = "seed_data_fallback"
            summary.quality_notes.append(f"Monday API notice: Could not reach live API ({str(e)}). Active mode: Seed Dataset Fallback.")
            return deals, wos, summary
