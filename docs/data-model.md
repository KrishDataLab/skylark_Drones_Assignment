# Data Model Specification — Skylark Drones BI Agent

## 1. Normalized Entities

### `Deal` (Sales Pipeline)
| Field | Type | Description | Source Column |
|---|---|---|---|
| `id` | `str` | Unique record ID | Monday Item ID / `DEAL-xxxx` |
| `deal_name` | `str` | Deal / Account Name | `Deal Name` |
| `owner_code` | `Optional[str]` | Owner / BD personnel code | `Owner code` |
| `client_code` | `Optional[str]` | Client identifier | `Client Code` |
| `deal_status` | `str` | Deal status (`Open`, `Closed Won`, `Closed Lost`) | `Deal Status` |
| `close_date_actual` | `Optional[str]` | Actual close date (ISO `YYYY-MM-DD`) | `Close Date (A)` |
| `closure_probability` | `Optional[str]` | Win probability (`High`, `Medium`, `Low`) | `Closure Probability` |
| `masked_deal_value` | `float` | Financial deal value | `Masked Deal value` |
| `tentative_close_date`| `Optional[str]` | Expected close date (ISO `YYYY-MM-DD`) | `Tentative Close Date` |
| `deal_stage` | `Optional[str]` | Funnel stage (e.g., `B. Sales Qualified Leads`) | `Deal Stage` |
| `product_deal` | `Optional[str]` | Product / Service offer | `Product deal` |
| `sector` | `str` | Industry sector (e.g. `Mining`, `Renewable Energy`) | `Sector/service` |
| `created_date` | `Optional[str]` | Deal creation date (ISO `YYYY-MM-DD`) | `Created Date` |

### `WorkOrder` (Project Execution & Billing)
| Field | Type | Description | Source Column |
|---|---|---|---|
| `id` | `str` | Unique work order ID | Monday Item ID / `WO-xxxx` |
| `deal_name` | `str` | Associated deal / project name | `Deal name masked` |
| `customer_name_code` | `Optional[str]` | Customer identifier | `Customer Name Code` |
| `serial_num` | `Optional[str]` | Serial / PO tracker number | `Serial #` |
| `nature_of_work` | `Optional[str]` | Project type (`One time Project`, `Monthly`) | `Nature of Work` |
| `execution_status` | `str` | Operational status (`Completed`, `In Progress`, `Delayed`) | `Execution Status` |
| `data_delivery_date` | `Optional[str]` | Delivery date (ISO `YYYY-MM-DD`) | `Data Delivery Date` |
| `owner_code` | `Optional[str]` | BD/KAM owner code | `BD/KAM Personnel code` |
| `sector` | `str` | Industry sector | `Sector` |
| `amount_excl_gst` | `float` | Base order amount (Excl GST) | `Amount in Rupees (Excl of GST) (Masked)` |
| `amount_incl_gst` | `float` | Gross order amount (Incl GST) | `Amount in Rupees (Incl of GST) (Masked)` |
| `billed_value_excl_gst`| `float` | Billed amount | `Billed Value in Rupees (Excl of GST.) (Masked)` |
| `collected_amount_incl_gst`| `float` | Cash collected | `Collected Amount in Rupees (Incl of GST.) (Masked)` |
| `amount_receivable` | `float` | Accounts Receivable balance | `Amount Receivable (Masked)` |
| `billing_status` | `Optional[str]` | Billing status string | `Billing Status` |

## 2. Data Quality Rules

1. **Numeric Normalization**: All currency strings containing `₹`, commas, or trailing spaces are sanitized to `float`.
2. **Null Preservation**: Missing values are stored as `None` / `0.0` with explicit missing counts reported to users.
3. **Date Canonicalization**: Dates formatted as `YYYY-MM-DD`, `DD/MM/YYYY`, or month names are standardized to `YYYY-MM-DD`.
4. **Sector Grouping**: Variations like `mining`, `Mining`, `solar`, `renewable` are unified into standard categories (`Mining`, `Renewable Energy`, `Infrastructure`, etc.).
