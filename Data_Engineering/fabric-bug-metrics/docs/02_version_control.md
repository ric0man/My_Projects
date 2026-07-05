# Version control guide — fabric-bug-metrics

Goal: show clean Git discipline (a graded item). The principle is **one logical
change per commit**, committed in the order the pipeline was built, so a reviewer
can read the history like a story: setup → bronze → silver → gold → docs.

## 0. Repo layout

```
fabric-bug-metrics/
├─ .gitignore
├─ README.md                       <-- to add (approach, assumptions, tradeoffs)
├─ data/
│  └─ brnz_azdo_workitems_current_anonymized.csv.csv
├─ docs/
│  ├─ 01_setup_guide.md
│  └─ 02_version_control.md         <-- this file
└─ notebooks/
   ├─ 01_bronze_ingestion.py
   ├─ 02_silver_cleaning.py
   └─ 03_gold_star_schema.py        <-- PySpark star schema
```

## 1. Initialise and connect (run once)

```bash
cd fabric-bug-metrics
git init
git branch -M main
git remote add origin https://github.com/<your-user>/fabric-bug-metrics.git
```

## 2. Commit in logical slices (recommended history)

```bash
# repo scaffolding + ignore rules
git add .gitignore docs/01_setup_guide.md data/
git commit -m "chore: initial repo structure, raw data and setup guide"

# bronze layer
git add notebooks/01_bronze_ingestion.py
git commit -m "feat(bronze): land raw Azure DevOps export as lossless Delta table"

# silver layer
git add notebooks/02_silver_cleaning.py
git commit -m "feat(silver): type, clean, dedupe work items with quality gates"

# gold layer (PySpark star schema)
git add notebooks/03_gold_star_schema.py
git commit -m "feat(gold): bug star schema (fact_bug, dim_product, dim_date) in PySpark"

# version-control + docs
git add docs/02_version_control.md
git commit -m "docs: add version control guide"

# README last, once content is final
git add README.md
git commit -m "docs: README — approach, assumptions, data quality, modeling, productionization"

git push -u origin main
```

## 3. Going forward

- Commit small and often; use Conventional Commit prefixes (`feat:`, `fix:`, `chore:`, `docs:`).
- Never commit tokens / PATs (the `.gitignore` blocks `.env` and `*.pat`).
- Fabric Git integration syncs workspace items under `/fabric` (see setup guide §4).
  The hand-written `notebooks/*.py` stay the reviewable source of truth; the
  `/fabric` items are the deployed copies. Say this explicitly in the README.

## 4. If the repo already has commits

You only need the Gold change:

```bash
git add notebooks/03_gold_star_schema.py docs/02_version_control.md .gitignore
git commit -m "refactor(gold): rewrite star schema in PySpark for pipeline uniformity"
git push
```
