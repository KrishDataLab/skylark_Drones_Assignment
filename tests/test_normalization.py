from backend.data.normalizer import parse_float, parse_date, normalize_sector, normalize_status

def test_parse_float():
    val, missing = parse_float("₹ 264,398.08")
    assert val == 264398.08
    assert not missing

    val_empty, missing_empty = parse_float("")
    assert val_empty is None
    assert missing_empty

    val_none, missing_none = parse_float(None)
    assert val_none is None
    assert missing_none

def test_parse_date():
    assert parse_date("2025-09-27") == "2025-09-27"
    assert parse_date("27/09/2025") == "2025-09-27"
    assert parse_date("") is None

def test_normalize_sector():
    assert normalize_sector("mining") == "Mining"
    assert normalize_sector("solar project") == "Renewable Energy"
    assert normalize_sector("energy") == "Renewable Energy"
    assert normalize_sector("energy sector") == "Renewable Energy"
    assert normalize_sector("renewables") == "Renewable Energy"
    assert normalize_sector("") == "Unspecified"

def test_normalize_status():
    assert normalize_status("Closed Won") == "Closed Won"
    assert normalize_status("Completed") == "Completed"
    assert normalize_status("in delay") == "Delayed"
