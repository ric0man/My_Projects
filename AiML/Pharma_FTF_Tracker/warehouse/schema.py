"""
SQLAlchemy table definitions matching the conceptual data model.
Used to initialize the DuckDB warehouse schema.
"""

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Date, Text, MetaData, Table
)

metadata = MetaData()

company = Table("company", metadata,
    Column("company_id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("country", String),
    Column("market_cap_usd", Float),
    Column("pe", Float),
    Column("pb", Float),
    Column("rd_spend_usd", Float),
    Column("fiscal_year", Integer),
)

molecule = Table("molecule", metadata,
    Column("molecule_id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("inchi_key", String),
    Column("therapeutic_area", String),
)

anda_filing = Table("anda_filing", metadata,
    Column("filing_id", String, primary_key=True),
    Column("molecule_id", String),
    Column("company_id", String),
    Column("filing_date", Date),
    Column("para_cert_type", String),
    Column("status", String),
)

ftf_exclusivity = Table("ftf_exclusivity", metadata,
    Column("exclusivity_id", String, primary_key=True),
    Column("filing_id", String),
    Column("company_id", String),
    Column("start_date", Date),
    Column("end_date", Date),
    Column("exclusivity_type", String),
    Column("shared_flag", Boolean, default=False),
)

patent = Table("patent", metadata,
    Column("patent_id", String, primary_key=True),
    Column("molecule_id", String),
    Column("patent_number", String),
    Column("expiry_date", Date),
    Column("owner", String),
)

revenue_estimate = Table("revenue_estimate", metadata,
    Column("estimate_id", String, primary_key=True),
    Column("molecule_id", String),
    Column("company_id", String),
    Column("year", Integer),
    Column("revenue_usd", Float),
    Column("source", String),
    Column("confidence_score", Float),
)

fda_action = Table("fda_action", metadata,
    Column("action_id", String, primary_key=True),
    Column("company_id", String),
    Column("facility", String),
    Column("action_type", String),
    Column("date", Date),
    Column("details", Text),
)


def init_db(engine):
    """Create all tables in the target database."""
    metadata.create_all(engine)
