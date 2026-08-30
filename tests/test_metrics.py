from backend.data.models import Deal, WorkOrder
from backend.bi.calculations import (
    calculate_total_revenue,
    calculate_pipeline,
    calculate_delayed_work_orders,
    calculate_top_customers
)

def test_calculate_total_revenue():
    wos = [
        WorkOrder(id="WO-1", deal_name="D1", amount_excl_gst=100000.0, billed_value_excl_gst=50000.0, sector="Mining"),
        WorkOrder(id="WO-2", deal_name="D2", amount_excl_gst=200000.0, billed_value_excl_gst=200000.0, sector="Solar")
    ]
    res = calculate_total_revenue(wos)
    assert res["count"] == 2
    assert res["total_revenue_excl_gst"] == 300000.0
    assert res["total_billed_excl_gst"] == 250000.0

def test_calculate_pipeline():
    deals = [
        Deal(id="D1", deal_name="D1", masked_deal_value=500000.0, deal_status="Open", closure_probability="High", sector="Mining"),
        Deal(id="D2", deal_name="D2", masked_deal_value=200000.0, deal_status="Open", closure_probability="Low", sector="Mining")
    ]
    res = calculate_pipeline(deals)
    assert res["open_deals_count"] == 2
    assert res["total_pipeline_value"] == 700000.0
    # High (0.8 * 500k) + Low (0.2 * 200k) = 400k + 40k = 440k
    assert res["weighted_pipeline_value"] == 440000.0

def test_calculate_delayed_work_orders():
    wos = [
        WorkOrder(id="WO-1", deal_name="D1", execution_status="Delayed"),
        WorkOrder(id="WO-2", deal_name="D2", execution_status="Completed")
    ]
    res = calculate_delayed_work_orders(wos)
    assert res["delayed_count"] == 1
    assert res["delayed_percentage"] == 50.0
