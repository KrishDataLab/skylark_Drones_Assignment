from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field

class Deal(BaseModel):
    id: str
    deal_name: str
    owner_code: Optional[str] = None
    client_code: Optional[str] = None
    deal_status: Optional[str] = "Open"
    close_date_actual: Optional[str] = None
    closure_probability: Optional[str] = None
    masked_deal_value: Optional[float] = 0.0
    tentative_close_date: Optional[str] = None
    deal_stage: Optional[str] = None
    product_deal: Optional[str] = None
    sector: Optional[str] = "Unspecified"
    created_date: Optional[str] = None
    raw_record: Optional[Dict[str, Any]] = None

class WorkOrder(BaseModel):
    id: str
    deal_name: str
    customer_name_code: Optional[str] = None
    serial_num: Optional[str] = None
    nature_of_work: Optional[str] = None
    execution_status: Optional[str] = "Pending"
    data_delivery_date: Optional[str] = None
    date_of_po_loi: Optional[str] = None
    probable_start_date: Optional[str] = None
    probable_end_date: Optional[str] = None
    owner_code: Optional[str] = None
    sector: Optional[str] = "Unspecified"
    type_of_work: Optional[str] = None
    skylark_software_used: Optional[str] = None
    amount_excl_gst: Optional[float] = 0.0
    amount_incl_gst: Optional[float] = 0.0
    billed_value_excl_gst: Optional[float] = 0.0
    billed_value_incl_gst: Optional[float] = 0.0
    collected_amount_incl_gst: Optional[float] = 0.0
    amount_to_be_billed_excl_gst: Optional[float] = 0.0
    amount_receivable: Optional[float] = 0.0
    invoice_status: Optional[str] = None
    billing_status: Optional[str] = None
    collection_status: Optional[str] = None
    raw_record: Optional[Dict[str, Any]] = None

class DataQualitySummary(BaseModel):
    total_deals: int = 0
    total_work_orders: int = 0
    deals_missing_value: int = 0
    work_orders_missing_amount: int = 0
    work_orders_missing_dates: int = 0
    data_source_mode: str = "seed_data_fallback" # "live_graphql" or "seed_data_fallback"
    quality_notes: List[str] = []

class BIQueryIntent(BaseModel):
    metric: str # revenue, pipeline, margin, work_orders, deals, delayed_work_orders, sector_performance, top_customers, owner_pipeline, etc.
    dimensions: List[str] = [] # sector, customer, owner, stage, month, quarter
    time_filter: Optional[str] = None # Q1, Q2, last_month, this_month, 2025, 2026
    sector_filter: Optional[str] = None
    owner_filter: Optional[str] = None
    customer_filter: Optional[str] = None
    needs_clarification: bool = False
    clarification_question: Optional[str] = None

class BIQueryResult(BaseModel):
    query: str
    direct_answer: str
    intent: BIQueryIntent
    key_numbers: Dict[str, Any]
    insights: List[str]
    data_notes: List[str]
    supporting_data: List[Dict[str, Any]] = []
    execution_trace: List[str] = []
