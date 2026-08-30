import re
from datetime import datetime
from typing import Optional, Any, Tuple

def parse_float(val: Any) -> Tuple[Optional[float], bool]:
    """
    Parses numeric strings, currency formats, floats safely.
    Returns (parsed_value, is_missing_flag).
    """
    if val is None or val == "" or str(val).strip() in ["", "-", "nan", "NaN", "null", "None"]:
        return (None, True)
    try:
        if isinstance(val, (int, float)):
            return (float(val), False)
        # Remove currency symbols, commas, spaces
        cleaned = re.sub(r"[^\d.-]", "", str(val))
        if not cleaned or cleaned == "-":
            return (None, True)
        return (float(cleaned), False)
    except Exception:
        return (None, True)

def parse_date(val: Any) -> Optional[str]:
    """
    Parses various date formats to YYYY-MM-DD string.
    """
    if not val or str(val).strip() in ["", "-", "nan", "NaN", "null", "None"]:
        return None
    s = str(val).strip()
    
    # Standard YYYY-MM-DD
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return s
    
    # Formats like YYYY/MM/DD, DD/MM/YYYY, DD-MM-YYYY
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%b %Y", "%B %Y", "%d %b %Y"]:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
            
    return s # return raw if unparseable

def normalize_sector(val: Any) -> str:
    if not val or str(val).strip() in ["", "-", "nan", "NaN", "null", "None"]:
        return "Unspecified"
    s = str(val).strip()
    # Canonical mapping for common sectors
    s_lower = s.lower()
    if "mining" in s_lower:
        return "Mining"
    if "energy" in s_lower or "solar" in s_lower or "renewable" in s_lower or "renewables" in s_lower:
        return "Renewable Energy"
    if "wind" in s_lower:
        return "Wind Energy"
    if "rail" in s_lower:
        return "Railways"
    if "infra" in s_lower or "construction" in s_lower:
        return "Infrastructure"
    if "power" in s_lower or "utility" in s_lower or "transmission" in s_lower:
        return "Power & Utilities"
    if "agriculture" in s_lower:
        return "Agriculture"
    return s.title()

def normalize_status(val: Any) -> str:
    if not val or str(val).strip() in ["", "-", "nan", "NaN", "null", "None"]:
        return "Unknown"
    s = str(val).strip()
    s_lower = s.lower()
    if "won" in s_lower or "closed won" in s_lower or "signed" in s_lower:
        return "Closed Won"
    if "lost" in s_lower or "closed lost" in s_lower:
        return "Closed Lost"
    if "complete" in s_lower:
        return "Completed"
    if "progress" in s_lower or "ongoing" in s_lower:
        return "In Progress"
    if "delay" in s_lower or "hold" in s_lower:
        return "Delayed"
    if "open" in s_lower:
        return "Open"
    return s
