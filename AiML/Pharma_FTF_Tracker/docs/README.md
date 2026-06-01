# FTF Exclusivity Tracker — Pharma Sector

End-to-end data pipeline and interactive dashboard tracking First-to-File (FTF) exclusivity, Paragraph IV filings, ANDA outcomes, and molecule-level revenue impact across global and Indian pharma companies.

## Quickstart

```bash
# 1. Create and activate a virtual environment (Python 3.12)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate       # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and fill in secrets
cp .env.example .env

# 4. Run the dashboard (uses sample data out of the box)
streamlit run dashboard/app.py

# 5. Run tests
pytest tests/ -v
```

## Project Structure

```
ftf-exclusivity-tracker/
  data/sample/          # Mock CSVs for local dev and CI
  ingestion/            # OpenFDA and USPTO API clients
  dbt/models/           # dbt transformation models
  warehouse/            # Schema definitions and business logic
  dashboard/app.py      # Streamlit MVP
  docs/                 # README and runbook
  tests/                # Unit and integration tests
  Dockerfile            # Container for dashboard deployment
  requirements.txt      # Pinned dependencies
  .env.example          # Secret keys template
```

## Data Sources

| Source | What it provides | Access |
|--------|-----------------|--------|
| OpenFDA | ANDA filings, Para IV certifications | Free API, key optional |
| USPTO PatentsView | Patent records and expiry dates | Free API, key optional |
| IQVIA / GlobalData | Molecule sales and market share | Commercial — use mock CSV |
| SEC EDGAR | Company fundamentals | Free |

## Key Business Logic

- **Exclusivity window:** `approval_date` to `approval_date + 180 days` (Hatch-Waxman)
- **Revenue attribution:** prefers company disclosures; falls back to `global_sales × therapeutic_area_share`
- **Risk flags:** ACTIVE_LITIGATION, FORM_483, SINGLE_SOURCE_API, REGULATORY_HOLD

## Deployment

### Docker
```bash
docker build -t ftf-tracker .
docker run -p 8501:8501 --env-file .env ftf-tracker
```

### Streamlit Cloud
Push repo to GitHub → connect at [share.streamlit.io](https://share.streamlit.io) → set secrets in the UI.
