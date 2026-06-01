"""
FTF Exclusivity Tracker — Phase 1 Dashboard
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import date, timedelta
from pathlib import Path

from warehouse.exclusivity_logic import flag_risks

DATA_DIR = Path(__file__).parent.parent / "data" / "sample"
TODAY = pd.Timestamp(date.today())
ALERT_DAYS = 60

st.set_page_config(
    page_title="FTF Exclusivity Tracker",
    page_icon="💊",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .risk-red    { color: #e74c3c; font-weight: 600; }
    .risk-yellow { color: #f39c12; font-weight: 600; }
    .risk-green  { color: #27ae60; font-weight: 600; }
    .alert-box {
        background: #fdf2f2; border-left: 4px solid #e74c3c;
        padding: 0.8rem 1rem; border-radius: 4px; margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    filings  = pd.read_csv(DATA_DIR / "anda_filings_sample.csv",  parse_dates=["filing_date"])
    molecules = pd.read_csv(DATA_DIR / "molecules_sample.csv")
    companies = pd.read_csv(DATA_DIR / "companies_sample.csv")

    df = (
        filings
        .merge(molecules, on="molecule_id", how="left")
        .merge(companies, on="company_id",  how="left")
    )
    df.rename(columns={"name_x": "Molecule", "name_y": "Company"}, inplace=True)

    df["exclusivity_start"] = df["filing_date"]
    df["exclusivity_end"]   = df["filing_date"] + pd.Timedelta(days=180)
    df["days_to_expiry"]    = (df["exclusivity_end"] - TODAY).dt.days
    df["expiring_soon"]     = df["days_to_expiry"].between(0, ALERT_DAYS)

    df["risk_flags"] = df.apply(flag_risks, axis=1)
    df["risk_level"] = df["risk_flags"].apply(
        lambda f: "🔴 High" if len(f) >= 2 else ("🟡 Medium" if len(f) == 1 else "🟢 Low")
    )
    return df, companies


df, companies_df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/48/pill.png", width=40)
st.sidebar.title("Filters")

sel_companies = st.sidebar.multiselect(
    "Company", options=df["Company"].unique(), default=df["Company"].unique()
)
sel_areas = st.sidebar.multiselect(
    "Therapeutic Area", options=df["therapeutic_area"].unique(), default=df["therapeutic_area"].unique()
)
sel_statuses = st.sidebar.multiselect(
    "Filing Status", options=df["status"].unique(), default=df["status"].unique()
)
sel_risk = st.sidebar.multiselect(
    "Risk Level", options=df["risk_level"].unique(), default=df["risk_level"].unique()
)

filtered = df[
    df["Company"].isin(sel_companies) &
    df["therapeutic_area"].isin(sel_areas) &
    df["status"].isin(sel_statuses) &
    df["risk_level"].isin(sel_risk)
]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("💊 FTF Exclusivity Tracker — Pharma Sector")
st.caption(f"Data as of {TODAY.date()} · Sample dataset · {len(filtered)} filings shown")

# ── Expiry Alert Banner ───────────────────────────────────────────────────────
expiring = filtered[filtered["expiring_soon"]]
if not expiring.empty:
    st.markdown("### ⚠️ Exclusivity Expiring Within 60 Days")
    for _, row in expiring.iterrows():
        st.markdown(
            f'<div class="alert-box">'
            f'<b>{row["Molecule"]}</b> ({row["Company"]}) — '
            f'Exclusivity ends <b>{row["exclusivity_end"].date()}</b> '
            f'({int(row["days_to_expiry"])} days left) · Status: {row["status"]}'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Filings",      len(filtered))
k2.metric("Unique Molecules",   filtered["molecule_id"].nunique())
k3.metric("Companies",          filtered["Company"].nunique())
k4.metric("Expiring ≤60 days",  int(filtered["expiring_soon"].sum()))
k5.metric("High-Risk Filings",  int((filtered["risk_level"] == "🔴 High").sum()))

st.divider()

# ── Tab layout ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📅 Exclusivity Timeline",
    "📋 Filings Table",
    "🏢 Company Scorecard",
    "🔬 Molecule Drilldown",
])

# ── Tab 1: Gantt timeline ─────────────────────────────────────────────────────
with tab1:
    st.subheader("Exclusivity Windows by Molecule & Company")

    gantt_df = filtered.copy()
    gantt_df["Label"] = gantt_df["Molecule"] + " · " + gantt_df["Company"]

    fig = px.timeline(
        gantt_df,
        x_start="exclusivity_start",
        x_end="exclusivity_end",
        y="Label",
        color="Company",
        hover_data=["status", "para_cert_type", "risk_level", "days_to_expiry"],
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.add_shape(
        type="line", x0=str(TODAY.date()), x1=str(TODAY.date()),
        y0=0, y1=1, yref="paper",
        line=dict(color="red", dash="dash", width=2),
    )
    fig.add_annotation(
        x=str(TODAY.date()), y=1, yref="paper",
        text="Today", showarrow=False,
        font=dict(color="red"), xanchor="left",
    )
    fig.update_layout(
        height=max(350, len(gantt_df) * 38),
        xaxis_title="Date",
        yaxis_title="",
        legend_title="Company",
        margin=dict(l=10, r=10, t=30, b=10),
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Red dashed line = today. Bars ending before today have expired exclusivity.")

# ── Tab 2: Filings table with risk badges + CSV export ───────────────────────
with tab2:
    st.subheader("ANDA Filings & Risk Flags")

    display_cols = [
        "filing_id", "Molecule", "therapeutic_area", "Company",
        "filing_date", "exclusivity_end", "days_to_expiry",
        "para_cert_type", "status", "risk_level",
    ]
    table_df = filtered[display_cols].rename(columns={
        "therapeutic_area": "Area",
        "filing_date": "Filed",
        "exclusivity_end": "Excl. Ends",
        "days_to_expiry": "Days Left",
        "para_cert_type": "Para Cert",
        "risk_level": "Risk",
    }).sort_values("Days Left")

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Days Left": st.column_config.NumberColumn(format="%d days"),
            "Filed": st.column_config.DateColumn(),
            "Excl. Ends": st.column_config.DateColumn(),
        }
    )

    csv = table_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Export to CSV",
        data=csv,
        file_name=f"ftf_filings_{TODAY.date()}.csv",
        mime="text/csv",
    )

# ── Tab 3: Company Scorecard ──────────────────────────────────────────────────
with tab3:
    st.subheader("Company Fundamentals")

    col_a, col_b = st.columns(2)

    with col_a:
        fig_rd = px.bar(
            companies_df.sort_values("rd_spend_usd", ascending=True),
            x="rd_spend_usd", y="name",
            orientation="h",
            title="R&D Spend (USD)",
            color="name",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"rd_spend_usd": "R&D Spend", "name": ""},
        )
        fig_rd.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
        fig_rd.update_xaxes(tickformat="$.2s")
        st.plotly_chart(fig_rd, use_container_width=True)

    with col_b:
        fig_mc = px.bar(
            companies_df.sort_values("market_cap_usd", ascending=True),
            x="market_cap_usd", y="name",
            orientation="h",
            title="Market Cap (USD)",
            color="name",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"market_cap_usd": "Market Cap", "name": ""},
        )
        fig_mc.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
        fig_mc.update_xaxes(tickformat="$.2s")
        st.plotly_chart(fig_mc, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        fig_pe = px.scatter(
            companies_df,
            x="pe", y="pb",
            size="market_cap_usd",
            color="name",
            text="name",
            title="PE vs PB (bubble = market cap)",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"pe": "Price / Earnings", "pb": "Price / Book"},
        )
        fig_pe.update_traces(textposition="top center")
        fig_pe.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_pe, use_container_width=True)

    with col_d:
        ftf_wins = (
            filtered[filtered["status"] == "Approved"]
            .groupby("Company")
            .size()
            .reset_index(name="FTF Wins")
        )
        fig_wins = px.bar(
            ftf_wins.sort_values("FTF Wins"),
            x="FTF Wins", y="Company",
            orientation="h",
            title="Approved ANDA Filings per Company",
            color="Company",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_wins.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_wins, use_container_width=True)

    st.subheader("FDA Inspection Status")
    for _, row in companies_df.iterrows():
        status_icon = "🟢" if row["fda_inspection_status"] == "Satisfactory" else "🔴"
        st.write(f"{status_icon} **{row['name']}** — {row['fda_inspection_status']}")

# ── Tab 4: Molecule Drilldown ─────────────────────────────────────────────────
with tab4:
    st.subheader("Molecule Drilldown")

    mol_options = sorted(filtered["Molecule"].unique())
    selected_mol = st.selectbox("Select a molecule", mol_options)
    mol_df = filtered[filtered["Molecule"] == selected_mol].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Therapeutic Area", mol_df["therapeutic_area"])
    col2.metric("Global Sales (USD)", f"${mol_df['global_sales_usd']:,.0f}")
    col3.metric("Total Filings", len(filtered[filtered["Molecule"] == selected_mol]))

    st.markdown("#### Filers for this molecule")
    mol_filings = filtered[filtered["Molecule"] == selected_mol][[
        "Company", "filing_date", "exclusivity_end", "status", "risk_level"
    ]].rename(columns={
        "filing_date": "Filed",
        "exclusivity_end": "Excl. Ends",
        "risk_level": "Risk",
    })
    st.dataframe(mol_filings, use_container_width=True, hide_index=True)

    st.markdown("#### Exclusivity Timeline")
    fig_mol = px.timeline(
        filtered[filtered["Molecule"] == selected_mol],
        x_start="exclusivity_start",
        x_end="exclusivity_end",
        y="Company",
        color="status",
        hover_data=["risk_level", "days_to_expiry"],
        color_discrete_map={
            "Approved": "#27ae60",
            "Tentatively Approved": "#f39c12",
            "Pending": "#3498db",
        },
    )
    fig_mol.add_shape(
        type="line", x0=str(TODAY.date()), x1=str(TODAY.date()),
        y0=0, y1=1, yref="paper",
        line=dict(color="red", dash="dash", width=2),
    )
    fig_mol.add_annotation(
        x=str(TODAY.date()), y=1, yref="paper",
        text="Today", showarrow=False,
        font=dict(color="red"), xanchor="left",
    )
    fig_mol.update_layout(height=300, margin=dict(l=10, r=10, t=20, b=10))
    fig_mol.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_mol, use_container_width=True)

    risk_flags = filtered[filtered["Molecule"] == selected_mol]["risk_flags"].explode().dropna()
    risk_flags = risk_flags[risk_flags != ""]
    if not risk_flags.empty:
        st.markdown("#### ⚠️ Risk Flags")
        for flag in risk_flags.unique():
            st.warning(flag)
    else:
        st.success("No risk flags for this molecule.")

st.divider()
st.caption("FTF Exclusivity Tracker · Sample data · Connect DuckDB warehouse in load_data() for live feeds.")
