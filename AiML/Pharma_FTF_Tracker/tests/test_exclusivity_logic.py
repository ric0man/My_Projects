"""Unit tests for exclusivity window and revenue attribution logic."""

from datetime import date
import pytest
from warehouse.exclusivity_logic import compute_exclusivity_window, attribute_revenue, flag_risks
import pandas as pd


def test_exclusivity_window_180_days():
    start, end = compute_exclusivity_window(date(2024, 1, 1))
    assert (end - start).days == 180


def test_exclusivity_window_shared():
    start, end = compute_exclusivity_window(date(2024, 1, 1), shared=True)
    assert (end - start).days == 180


def test_revenue_prefers_direct():
    rev, source, conf = attribute_revenue(1_000_000, 0.3, direct_revenue_usd=500_000)
    assert rev == 500_000
    assert source == "disclosure"
    assert conf > 0.9


def test_revenue_proxy_fallback():
    rev, source, conf = attribute_revenue(1_000_000, 0.3)
    assert abs(rev - 300_000) < 1
    assert source == "proxy"
    assert conf < 0.9


def test_risk_flags_all():
    row = pd.Series({
        "active_litigation": True,
        "form483_count": 2,
        "api_suppliers": 1,
        "regulatory_hold": True,
    })
    flags = flag_risks(row)
    assert "ACTIVE_LITIGATION" in flags
    assert "FORM_483" in flags
    assert "SINGLE_SOURCE_API" in flags
    assert "REGULATORY_HOLD" in flags


def test_risk_flags_none():
    row = pd.Series({
        "active_litigation": False,
        "form483_count": 0,
        "api_suppliers": 3,
        "regulatory_hold": False,
    })
    assert flag_risks(row) == []
