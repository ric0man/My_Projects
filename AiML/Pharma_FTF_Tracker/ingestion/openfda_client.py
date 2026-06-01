"""
OpenFDA ANDA ingestion client.
Fetches drug application records from the OpenFDA API and returns raw JSON.
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.fda.gov/drug/drugsfda.json"
API_KEY = os.getenv("OPENFDA_API_KEY", "")


def fetch_anda_filings(limit: int = 100, skip: int = 0) -> dict:
    """Fetch ANDA filings from OpenFDA. Returns raw API response as dict."""
    params = {
        "search": 'application_number:"ANDA*"',
        "limit": limit,
        "skip": skip,
    }
    if API_KEY:
        params["api_key"] = API_KEY

    response = httpx.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_para_iv_filings(limit: int = 100, skip: int = 0) -> dict:
    """Fetch Para IV certification filings from OpenFDA."""
    params = {
        "search": 'submissions.submission_type:"ORIG" AND submissions.submission_class_code:"PARAGRAPH_IV"',
        "limit": limit,
        "skip": skip,
    }
    if API_KEY:
        params["api_key"] = API_KEY

    response = httpx.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = fetch_anda_filings(limit=5)
    print(f"Fetched {len(data.get('results', []))} records.")
