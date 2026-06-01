"""
USPTO patent ingestion client.
Fetches patent records relevant to pharma molecules from the USPTO API.
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.patentsview.org/patents/query"
API_KEY = os.getenv("USPTO_API_KEY", "")


def fetch_patents_by_molecule(molecule_name: str, limit: int = 25) -> dict:
    """Search USPTO for patents related to a molecule name."""
    payload = {
        "q": {"_text_phrase": {"patent_abstract": molecule_name}},
        "f": ["patent_number", "patent_title", "patent_date", "assignee_organization"],
        "o": {"per_page": limit},
    }
    headers = {"X-Api-Key": API_KEY} if API_KEY else {}

    response = httpx.post(BASE_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = fetch_patents_by_molecule("ibuprofen", limit=3)
    print(f"Fetched {data.get('count', 0)} patents.")
