# Setup guide — Fabric workspace, Lakehouse, GitHub

Follow these once, in order. ~20 minutes.

## 1. Fabric workspace

1. Go to https://app.fabric.microsoft.com and sign in (your trial account).
2. Left nav → **Workspaces** → **New workspace**.
3. Name: `ws-bug-metrics`. Under **Advanced**, confirm license mode = **Trial** capacity.
4. Create.

## 2. Lakehouse

1. Inside the workspace → **New item** → **Lakehouse**.
2. Name: `lh_bug_metrics`. Leave "Lakehouse schemas" OFF (keeps table names simple).
3. In the Lakehouse explorer, right-click **Files** → **New subfolder** → name it `raw`.
4. Right-click `raw` → **Upload** → **Upload files** → select
   `brnz_azdo_workitems_current_anonymized.csv.csv` (a copy is in this repo's `data/` folder).
5. Verify the file appears under `Files/raw/`.

Why one Lakehouse, not Lakehouse + Warehouse: a single Lakehouse holds all three
medallion layers as Delta tables, its SQL analytics endpoint is enough for Power BI,
and it keeps the solution small and reviewable — matching the case's
"clear, defensible solution" instruction.

## 3. GitHub repository

1. On GitHub: **New repository** → name `fabric-bug-metrics`, add no files yet.
2. Push this folder:
   ```
   cd fabric-bug-metrics
   git init
   git add .
   git commit -m "chore: initial repo structure, raw data and setup guide"
   git branch -M main
   git remote add origin https://github.com/<your-user>/fabric-bug-metrics.git
   git push -u origin main
   ```
3. Commit small and often — version-control discipline is graded. Suggested style:
   one commit per layer (`feat: bronze ingestion notebook`, `feat: silver cleaning`, ...).

## 4. Connect Fabric workspace to GitHub (Git integration)

1. GitHub → Settings → Developer settings → **Fine-grained personal access token**:
   repo access to `fabric-bug-metrics`, permissions: Contents = Read and write.
2. Fabric: workspace → **Workspace settings** → **Git integration** → provider **GitHub**.
3. Add account with the token, pick repo `fabric-bug-metrics`, branch `main`,
   Git folder: `/fabric` (keeps Fabric-generated items separate from docs).
4. **Connect and sync**. From now on, notebooks created in the workspace are
   committed to the repo from the Source control panel in Fabric.

Note: the repo will then hold BOTH hand-written notebook code in `notebooks/`
(readable .py files, the reviewable source of truth) and Fabric's synced items
under `/fabric`. Say exactly that in the README.

## 5. Create the first notebook

1. Workspace → **New item** → **Notebook**, name `01_bronze_ingestion`.
2. In the notebook's Explorer pane → **Add data items** → select `lh_bug_metrics`
   (attaches the default Lakehouse — required; `Files/...` paths resolve against it).
3. Copy the cells from `notebooks/01_bronze_ingestion.py`
   (each `# CELL ----` block = one notebook cell).
4. Run all. Expected final output: row_count = 500, column count = 40
   (38 source columns + 2 metadata columns).
