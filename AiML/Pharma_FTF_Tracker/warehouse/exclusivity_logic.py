"""
Business logic for computing FTF exclusivity windows and revenue attribution.
"""

from datetime import date, timedelta
import pandas as pd


def compute_exclusivity_window(
    approval_date: date,
    shared: bool = False,
) -> tuple[date, date]:
    """
    Returns (start_date, end_date) for a 180-day FTF exclusivity window.
    Per Hatch-Waxman: 180 days from first commercial marketing by FTF filer.
    """
    start = approval_date
    end = start + timedelta(days=180)
    return start, end


def attribute_revenue(
    molecule_global_sales_usd: float,
    company_therapeutic_area_share: float,
    direct_revenue_usd: float | None = None,
    source: str = "proxy",
) -> tuple[float, str, float]:
    """
    Returns (revenue_usd, source, confidence_score).
    Prefers direct company disclosures; falls back to proxy method.
    """
    if direct_revenue_usd is not None:
        return direct_revenue_usd, "disclosure", 0.95

    proxy = molecule_global_sales_usd * company_therapeutic_area_share
    return proxy, "proxy", 0.60


def flag_risks(row: pd.Series) -> list[str]:
    """
    Returns a list of risk flag strings for a molecule/company row.
    Expects columns: active_litigation, form483_count, api_suppliers, regulatory_hold.
    """
    flags = []
    if row.get("active_litigation"):
        flags.append("ACTIVE_LITIGATION")
    if row.get("form483_count", 0) > 0:
        flags.append("FORM_483")
    if row.get("api_suppliers", 2) <= 1:
        flags.append("SINGLE_SOURCE_API")
    if row.get("regulatory_hold"):
        flags.append("REGULATORY_HOLD")
    return flags
