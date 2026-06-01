# Runbook

## Rotating API Keys
1. Generate a new key from the provider portal.
2. Update the value in your secrets manager (or `.env` for local dev).
3. Restart the ingestion service — no code change needed.

## Re-running a Failed DAG
1. Open the Prefect UI (`prefect server start`).
2. Navigate to the failed flow run.
3. Click **Re-run** to replay from the failed task.
4. For a full reprocess, delete the raw partition in `data/raw/` and trigger a new run.

## Refreshing the Warehouse
```bash
dbt run --select staging+ --target prod
dbt test
```

## Restarting the Streamlit Service
```bash
docker restart ftf-tracker
# or on Streamlit Cloud: Manage app → Reboot
```

## Contacts
- Project owner: Rohan
- On-call (weeks 1–2): project owner and lead engineer
- Data provider support: listed per-provider in `.env.example` comments
