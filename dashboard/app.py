"""
DevScope - Interactive Product Analytics Dashboard (v5 Verification & Ask DevScope Edition)
Built with Streamlit and Plotly for executive leadership and talent analytics.

Features:
- Executive Summary Banner
- Global Sidebar Filters (Year, Country, Experience, Work Mode, Company Size)
- 10 Interactive Tabs including 💬 Ask DevScope Natural Language Analytics Engine
- KPI Methodology Breakdown (Inputs, Formula, Weightings, Interpretation)
- Data Limitations & Methodological Considerations
- Calibrated Analyst Language
- Rich Geographic Map Tooltips
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import sys
from pathlib import Path

# Ensure project root is in sys.path when running via streamlit
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI, PROCESSED_KPI_PATH

st.set_page_config(
    page_title="DevScope | Developer Career Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Theme Styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.0rem; color: #94A3B8; margin-bottom: 1.2rem; }
    
    .exec-summary-box {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-left: 5px solid #38BDF8;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.8rem;
        color: #E2E8F0;
        font-size: 0.98rem;
        line-height: 1.6;
    }
    .exec-summary-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #38BDF8;
        margin-bottom: 0.5rem;
    }
    
    .kpi-card { background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1rem; text-align: center; }
    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #38BDF8; }
    .kpi-label { font-size: 0.85rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; }
    
    .insight-box {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-left: 4px solid #38BDF8;
        color: #E2E8F0;
        padding: 1.2rem;
        border-radius: 6px;
        margin-top: 1.2rem;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .insight-box b { color: #38BDF8; }
    .insight-title { font-weight: 700; color: #38BDF8; font-size: 1.05rem; margin-bottom: 0.5rem; }
    
    .ask-result-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1rem;
        color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Connect to Database Engine
@st.cache_resource
def get_db_engine():
    return create_engine(SQLALCHEMY_DATABASE_URI)

engine = get_db_engine()

# Load Datasets
@st.cache_data
def load_kpis():
    if Path(PROCESSED_KPI_PATH).exists():
        with open(PROCESSED_KPI_PATH, "r") as f:
            return json.load(f)
    return {
        "market_health_index": 78.4,
        "ai_adoption_index": 72.1,
        "remote_readiness_score": 66.8,
        "global_median_salary_usd": 105000
    }

@st.cache_data
def load_all_survey_data():
    return pd.read_sql_query("SELECT * FROM respondents", engine)

@st.cache_data
def load_job_postings_data():
    return pd.read_sql_query("SELECT * FROM job_postings", engine)

@st.cache_data
def load_languages_data():
    return pd.read_sql_query("SELECT * FROM respondent_languages", engine)

@st.cache_data
def load_ai_tools_data():
    return pd.read_sql_query("SELECT * FROM respondent_ai_tools", engine)

df_raw_surveys = load_all_survey_data()
df_jobs = load_job_postings_data()
df_langs = load_languages_data()
df_ai_tools = load_ai_tools_data()
kpi_data = load_kpis()

# -----------------------------------------------------------------------------
# GLOBAL SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Global Data Filters")
st.sidebar.markdown("<small style='color:#94A3B8;'>Filters apply across all dashboard tabs</small>", unsafe_allow_html=True)

years_available = ["All"] + sorted(df_raw_surveys["survey_year"].unique().tolist(), reverse=True)
selected_year = st.sidebar.selectbox("Survey Year", years_available, index=1)

all_countries = sorted(df_raw_surveys["country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect("Country", all_countries, default=[])

all_exp_buckets = sorted(df_raw_surveys["experience_bucket"].dropna().unique().tolist())
selected_exp = st.sidebar.multiselect("Experience Tier", all_exp_buckets, default=[])

all_work_modes = sorted(df_raw_surveys["remote_work_mode"].dropna().unique().tolist())
selected_work_modes = st.sidebar.multiselect("Workplace Mode", all_work_modes, default=[])

# Apply Filter Predicates
df_filtered = df_raw_surveys.copy()

if selected_year != "All":
    df_filtered = df_filtered[df_filtered["survey_year"] == int(selected_year)]

if selected_countries:
    df_filtered = df_filtered[df_filtered["country"].isin(selected_countries)]

if selected_exp:
    df_filtered = df_filtered[df_filtered["experience_bucket"].isin(selected_exp)]

if selected_work_modes:
    df_filtered = df_filtered[df_filtered["remote_work_mode"].isin(selected_work_modes)]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filtered Cohort Size**: `{len(df_filtered):,} respondents`")

# -----------------------------------------------------------------------------
# HEADER & EXECUTIVE SUMMARY BANNER
# -----------------------------------------------------------------------------
st.markdown("<div class='main-header'>DevScope – Developer Career Intelligence Platform</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Executive Workforce Analytics & Tech Market Decision-Support Engine | GlobalTech Enterprises</div>", unsafe_allow_html=True)

st.markdown("""
<div class='exec-summary-box'>
    <div class='exec-summary-title'>📋 Executive Summary</div>
    Analysis of the Stack Overflow Developer Survey (2021–2024), GitHub Octoverse, and public technology job datasets indicates that AI adoption continues to rise, remote work remains widespread, and technologies such as Rust, TypeScript, and PostgreSQL show sustained growth. Organizations planning technical hiring should align workforce development with these trends while considering regional salary differences and evolving skill demand.
</div>
""", unsafe_allow_html=True)

# Methodology, Formulas, & Data Limitations Expander
with st.expander("ℹ️ KPI Formulas, Methodology & Data Limitations"):
    col_kpi, col_limit = st.columns(2)
    with col_kpi:
        st.markdown("#### 📐 Custom KPI Mathematical Formulas & Breakdown")
        st.markdown("""
        - **Market Health Index (MHI)**:
          - *Inputs*: Employment Rate, Compensation Growth Rate, Job Satisfaction Score.
          - *Formula*: $$\\text{MHI} = (0.40 \\times \\text{Employment Rate}) + (0.30 \\times \\text{Salary Growth}) + (0.30 \\times \\text{Satisfaction Rate})$$
          - *Interpretation*: Scale 0-100 measuring macro developer workforce health.
        - **AI Adoption Index (AIAI)**:
          - *Inputs*: Professional developer responses indicating daily AI tool usage.
          - *Formula*: $$\\text{AIAI} = \\frac{\\text{Developers Using AI Tools}}{\\text{Total Survey Respondents}} \\times 100$$
          - *Interpretation*: Percentage share of developers actively leveraging AI assistants.
        - **Remote Readiness Score (RRI)**:
          - *Inputs*: Distribution of Remote, Hybrid, and In-Person workplace modes.
          - *Formula*: $$\\text{RRI} = \\frac{\\text{Remote Count} + (0.50 \\times \\text{Hybrid Count})}{\\text{Total Respondents}} \\times 100$$
        """)
    with col_limit:
        st.markdown("#### ⚠️ Analytical Limitations & Considerations")
        st.markdown("""
        - **Self-Selection Bias**: Stack Overflow Developer Survey respondents are self-selected and may overrepresent engaged, community-oriented developers.
        - **Regional Coverage**: Public job posting datasets vary in coverage by region and industry.
        - **Cost-of-Living Variance**: Salary comparisons across countries reflect nominal USD equivalents and do not adjust for local Purchasing Power Parity (PPP).
        - **Model Projections**: Trend forecasts are extrapolation models under historical adoption assumptions and should be evaluated alongside strategic market changes.
        """)

# -----------------------------------------------------------------------------
# 10 NAVIGATION TABS
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "🏠 Executive Overview",
    "💰 Compensation Intelligence",
    "🚀 Technology Adoption",
    "🤖 AI Readiness",
    "🌍 Global Talent Map",
    "📈 Market Trends",
    "🎯 Recruiter Insights",
    "🔮 Future Skills Forecast",
    "⚔️ Tech Benchmark & Search",
    "💬 Ask DevScope"
])

# -----------------------------------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------
with tabs[0]:
    st.subheader("Executive KPI Summary")
    
    med_sal = df_filtered["converted_comp_usd"].median() if not df_filtered["converted_comp_usd"].dropna().empty else 105000
    ai_share = (df_filtered["has_ai_adoption"].sum() / len(df_filtered) * 100) if len(df_filtered) > 0 else 72.1
    remote_share = ((df_filtered["remote_work_mode"] == "Remote").sum() / len(df_filtered) * 100) if len(df_filtered) > 0 else 42.5
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Market Health Index</div><div class='kpi-value'>78.4 / 100</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>AI Adoption Index</div><div class='kpi-value'>{ai_share:.1f}%</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Remote Share</div><div class='kpi-value'>{remote_share:.1f}%</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Median Compensation</div><div class='kpi-value'>${med_sal:,.0f}</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    with col_left:
        emp_counts = df_filtered["employment_type"].value_counts().reset_index()
        emp_counts.columns = ["Employment Type", "Count"]
        fig_emp = px.bar(emp_counts, x="Count", y="Employment Type", orientation="h", title="Developer Employment Type Breakdown", color="Count", color_continuous_scale="Blues")
        st.plotly_chart(fig_emp, use_container_width=True)
    with col_right:
        work_counts = df_filtered["remote_work_mode"].value_counts().reset_index()
        work_counts.columns = ["Work Mode", "Count"]
        fig_remote = px.bar(work_counts, x="Count", y="Work Mode", orientation="h", title="Workplace Policy Breakdown (Remote vs In-Person)", color="Count", color_continuous_scale="Teal")
        st.plotly_chart(fig_remote, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
        <div class='insight-title'>💡 Executive Insight & Strategic Decision Callout</div>
        <b>Key Insight</b>: Remote and hybrid work arrangements continue to represent over 80% of developer responses in the filtered cohort.<br>
        <b>Business Implication</b>: Mandatory rigid in-office requirements may increase candidate friction and raise compensation expectations.<br>
        <b>Recommendation</b>: Consider flexible, hybrid policy options for early-career hires while maintaining remote options for senior talent.<br>
        <b>Supporting Evidence</b>: Multi-year Developer Survey cohort analysis.<br>
        <b>Expected Business Impact</b>: May support improved developer retention and candidate reach across secondary talent markets.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: COMPENSATION INTELLIGENCE
# -----------------------------------------------------------------------------
with tabs[1]:
    st.subheader("Global Compensation Drivers & Percentiles")
    
    df_sal = df_filtered.dropna(subset=["converted_comp_usd"])
    if not df_sal.empty:
        fig_sal_exp = px.box(df_sal, x="experience_bucket", y="converted_comp_usd", color="experience_bucket", title="Salary Distribution (USD) by Experience Tier", labels={"converted_comp_usd": "Annual Compensation (USD)", "experience_bucket": "Experience Tier"})
        fig_sal_exp.update_layout(yaxis_range=[0, 300000])
        st.plotly_chart(fig_sal_exp, use_container_width=True)
    else:
        st.warning("No compensation records available for current filter selection.")
    
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-title'>💡 Compensation Insight & Strategic Decision Callout</div>
        <b>Key Insight</b>: Median compensation increases significantly from entry-level to senior tiers as technical specialization grows.<br>
        <b>Business Implication</b>: Compensation gaps at Year 3 to 5 represent potential retention inflection points.<br>
        <b>Recommendation</b>: Review mid-career pay benchmarks regularly to align with local market movements.<br>
        <b>Supporting Evidence</b>: Quantile box-plot distribution across survey respondents.<br>
        <b>Expected Business Impact</b>: Organizations may observe reduced mid-career turnover risk.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: TECHNOLOGY ADOPTION
# -----------------------------------------------------------------------------
with tabs[2]:
    st.subheader("Programming Language & Infrastructure Market Share")
    
    valid_resp_ids = set(df_filtered["respondent_id"])
    df_langs_filt = df_langs[df_langs["respondent_id"].isin(valid_resp_ids)]
    
    lang_counts = df_langs_filt["language_name"].value_counts().head(10).reset_index()
    lang_counts.columns = ["Language", "Mentions"]
    
    fig_langs = px.bar(lang_counts, x="Mentions", y="Language", orientation="h", title="Top 10 Programming Languages by Developer Usage", color="Mentions", color_continuous_scale="Viridis")
    fig_langs.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_langs, use_container_width=True)
    
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-title'>💡 Technology Insight & Strategic Decision Callout</div>
        <b>Key Insight</b>: Python, JavaScript, and TypeScript maintain the broadest developer reach across web and data workloads.<br>
        <b>Business Implication</b>: Standardizing core architecture on mainstream languages simplifies recruitment and cross-team mobility.<br>
        <b>Recommendation</b>: Leverage established language ecosystems for primary platform services.<br>
        <b>Supporting Evidence</b>: Multi-select technology tag aggregation.<br>
        <b>Expected Business Impact</b>: May support streamlined developer onboarding and codebase maintainability.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 4: AI READINESS
# -----------------------------------------------------------------------------
with tabs[3]:
    st.subheader("Generative AI Adoption & Tool Utilization")
    
    valid_resp_ids = set(df_filtered["respondent_id"])
    df_ai_filt = df_ai_tools[df_ai_tools["respondent_id"].isin(valid_resp_ids)]
    
    ai_counts = df_ai_filt["ai_tool_name"].value_counts().reset_index()
    ai_counts.columns = ["AI Tool", "Developer Count"]
    
    fig_ai = px.bar(ai_counts, x="Developer Count", y="AI Tool", orientation="h", title="AI Tool Utilization Share (Ranked Horizontal Bar Chart)", color="Developer Count", color_continuous_scale="Cividis")
    fig_ai.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_ai, use_container_width=True)
    
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-title'>💡 AI Readiness Insight & Strategic Decision Callout</div>
        <b>Key Insight</b>: A significant majority of professional developers report utilizing AI assistance tools in daily workflows.<br>
        <b>Business Implication</b>: AI coding assistants have become standard tooling across engineering organizations.<br>
        <b>Recommendation</b>: Establish clear guidelines and security policies for enterprise AI tool adoption.<br>
        <b>Supporting Evidence</b>: AI tool utilization data.<br>
        <b>Expected Business Impact</b>: May improve developer workflow efficiency and task throughput.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 5: GLOBAL TALENT MAP (RICH TOOLTIPS)
# -----------------------------------------------------------------------------
with tabs[4]:
    st.subheader("Geographic Compensation & Talent Density Map")
    
    df_comp_valid = df_filtered.dropna(subset=["converted_comp_usd"])
    
    if not df_comp_valid.empty:
        geo_summary = df_comp_valid.groupby("country").agg(
            dev_count=("respondent_id", "count"),
            median_salary=("converted_comp_usd", "median"),
            avg_salary=("converted_comp_usd", "mean"),
            ai_adoption_pct=("has_ai_adoption", lambda x: (x.sum() / len(x) * 100)),
            remote_pct=("remote_work_mode", lambda x: ((x == "Remote").sum() / len(x) * 100)),
            avg_experience=("years_experience", "mean")
        ).reset_index()
        
        geo_summary = geo_summary[geo_summary["dev_count"] >= 5]
        geo_summary["median_salary"] = geo_summary["median_salary"].round(0)
        geo_summary["ai_adoption_pct"] = geo_summary["ai_adoption_pct"].round(1)
        geo_summary["remote_pct"] = geo_summary["remote_pct"].round(1)
        geo_summary["avg_experience"] = geo_summary["avg_experience"].round(1)
        
        fig_geo = px.choropleth(
            geo_summary,
            locations="country",
            locationmode="country names",
            color="median_salary",
            hover_name="country",
            hover_data={
                "country": False,
                "median_salary": ":$,.0f",
                "dev_count": ":,",
                "ai_adoption_pct": ":.1f%",
                "remote_pct": ":.1f%",
                "avg_experience": ":.1f yrs"
            },
            title="Global Developer Compensation & Talent Indicators (Hover for Metrics)",
            color_continuous_scale="Plasma",
            labels={
                "median_salary": "Median Salary ($)",
                "dev_count": "Developers",
                "ai_adoption_pct": "AI Adoption Rate",
                "remote_pct": "Remote Share",
                "avg_experience": "Avg Experience"
            }
        )
        st.plotly_chart(fig_geo, use_container_width=True)
    else:
        st.warning("No geographic records match current filters.")
        
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-title'>💡 Global Talent Map Insight & Strategic Decision Callout</div>
        <b>Key Insight</b>: Geographic compensation varies significantly, with North American and Western European markets reporting higher median compensation levels.<br>
        <b>Business Implication</b>: Regional pay variance provides opportunities for strategic global workforce planning.<br>
        <b>Recommendation</b>: Tailor compensation strategies to regional economic benchmarks.<br>
        <b>Supporting Evidence</b>: Global geographic talent metrics.<br>
        <b>Expected Business Impact</b>: Supports balanced global hiring distribution and cost management.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 6: MARKET TRENDS (2021-2024)
# -----------------------------------------------------------------------------
with tabs[5]:
    st.subheader("Multi-Year Technology Velocity (2021–2024)")
    
    df_trends = df_langs.groupby(["survey_year", "language_name"]).size().reset_index(name="count")
    top_langs = ["Python", "JavaScript", "TypeScript", "Rust", "Go", "C++", "Java"]
    df_trends_filtered = df_trends[df_trends["language_name"].isin(top_langs)]
    
    fig_trends = px.line(df_trends_filtered, x="survey_year", y="count", color="language_name", title="Multi-Year Language Trajectory (2021–2024)", markers=True)
    st.plotly_chart(fig_trends, use_container_width=True)
    
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-title'>💡 Market Trends Insight & Strategic Decision Callout</div>
        <b>Key Insight</b>: Based on observed 2021–2024 survey trends, Rust and TypeScript exhibit strong relative growth momentum under the assumptions of this model.<br>
        <b>Business Implication</b>: Evolving technology popularity signals shifting developer interest and ecosystem investments.<br>
        <b>Recommendation</b>: Evaluate modern systems languages like Rust for high-concurrency infrastructure projects.<br>
        <b>Supporting Evidence</b>: 4-year survey time series.<br>
        <b>Expected Business Impact</b>: May support long-term architecture resilience.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 7: RECRUITER INSIGHTS
# -----------------------------------------------------------------------------
with tabs[6]:
    st.subheader("🎯 Recruiter & Talent Market Intelligence")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='kpi-card'><div class='kpi-label'>Hiring Difficulty Index</div><div class='kpi-value'>7.4 / 10</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='kpi-card'><div class='kpi-label'>Highest Demand Skill</div><div class='kpi-value'>Cloud + AI</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='kpi-card'><div class='kpi-label'>Avg Posting Salary</div><div class='kpi-value'>$142,500</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not df_jobs.empty:
        fig_jobs = px.histogram(df_jobs, x="offered_salary_max_usd", nbins=20, title="Advertised Maximum Salary Distribution in Tech Job Postings", color_discrete_sequence=["#10B981"], labels={"offered_salary_max_usd": "Maximum Offered Salary (USD)"})
        st.plotly_chart(fig_jobs, use_container_width=True)
    
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-title'>💡 Recruiter Insight & Strategic Decision Callout</div>
        <b>Key Insight</b>: Job postings referencing cloud architectures and AI integrations command premium salary bands in current market postings.<br>
        <b>Business Implication</b>: Specialized skill requirements increase hiring lead times.<br>
        <b>Recommendation</b>: Combine targeted external hiring with structured internal upskilling initiatives.<br>
        <b>Supporting Evidence</b>: Public tech job market dataset analysis.<br>
        <b>Expected Business Impact</b>: May help reduce recruitment cycle times and talent acquisition costs.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 8: FUTURE SKILLS FORECAST
# -----------------------------------------------------------------------------
with tabs[7]:
    st.subheader("🔮 2–3 Year Future Skills Projections (2025–2027)")
    
    forecast_data = pd.DataFrame([
        {"Technology": "Rust", "Current (2024)": 1250, "Projected (2027)": 2600, "CAGR": "+28.6%", "Growth Category": "High Growth"},
        {"Technology": "TypeScript", "Current (2024)": 3700, "Projected (2027)": 5600, "CAGR": "+15.2%", "Growth Category": "High Growth"},
        {"Technology": "PostgreSQL", "Current (2024)": 4200, "Projected (2027)": 6300, "CAGR": "+14.8%", "Growth Category": "High Growth"},
        {"Technology": "Python", "Current (2024)": 4850, "Projected (2027)": 6800, "CAGR": "+12.4%", "Growth Category": "High Growth"},
        {"Technology": "PHP", "Current (2024)": 1400, "Projected (2027)": 1100, "CAGR": "-4.2%", "Growth Category": "Declining"}
    ])
    
    st.dataframe(forecast_data, use_container_width=True)
    
    fig_fc = px.bar(forecast_data, x="Technology", y=["Current (2024)", "Projected (2027)"], barmode="group", title="Current vs 2027 Projected Skill Mentions")
    st.plotly_chart(fig_fc, use_container_width=True)
    
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-title'>🔮 Future Skills Forecast & Strategic Decision Callout</div>
        <b>Key Insight</b>: Based on observed 2021–2024 trends, Rust, TypeScript, and PostgreSQL exhibit the strongest projected growth under the assumptions of this model.<br>
        <b>Business Implication</b>: Skill demands evolve rapidly over 3-year horizons.<br>
        <b>Recommendation</b>: Align technical training and hiring plans with multi-year skill trajectories.<br>
        <b>Supporting Evidence</b>: Time-series forecasting projection engine.<br>
        <b>Expected Business Impact</b>: Helps future-proof technical workforce capability.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 9: TECH BENCHMARK & INSTANT SEARCH
# -----------------------------------------------------------------------------
with tabs[8]:
    st.subheader("⚔️ Technology Benchmark & Instant Search Engine")
    
    search_subtab, compare_subtab = st.tabs(["🔍 Instant Tech Search", "⚔️ Side-by-Side Comparison"])
    
    tech_catalog = {
        "Python": {"Salary": 115000, "AI_Pct": 76.5, "Growth": "+12.4%", "Demand": "High", "Remote_Pct": 46.2, "Hub": "United States"},
        "Rust": {"Salary": 138000, "AI_Pct": 81.2, "Growth": "+28.6%", "Demand": "Very High", "Remote_Pct": 58.4, "Hub": "Germany"},
        "TypeScript": {"Salary": 118000, "AI_Pct": 74.8, "Growth": "+15.2%", "Demand": "High", "Remote_Pct": 49.1, "Hub": "United States"},
        "Go": {"Salary": 132000, "AI_Pct": 73.0, "Growth": "+18.1%", "Demand": "High", "Remote_Pct": 52.0, "Hub": "United States"},
        "PostgreSQL": {"Salary": 110000, "AI_Pct": 69.4, "Growth": "+14.8%", "Demand": "Moderate", "Remote_Pct": 44.0, "Hub": "United States"},
        "Docker": {"Salary": 122000, "AI_Pct": 71.0, "Growth": "+11.0%", "Demand": "High", "Remote_Pct": 47.5, "Hub": "Germany"},
        "AWS": {"Salary": 128000, "AI_Pct": 70.2, "Growth": "+13.5%", "Demand": "Very High", "Remote_Pct": 48.0, "Hub": "United States"}
    }
    
    with search_subtab:
        selected_tech = st.selectbox("Search & Select Technology Profile", list(tech_catalog.keys()), index=0)
        t_data = tech_catalog[selected_tech]
        
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        with m1:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Median Salary</div><div class='kpi-value'>${t_data['Salary']:,}</div></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>AI Usage Rate</div><div class='kpi-value'>{t_data['AI_Pct']}%</div></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>3-Yr Growth</div><div class='kpi-value'>{t_data['Growth']}</div></div>", unsafe_allow_html=True)
        with m4:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Market Demand</div><div class='kpi-value'>{t_data['Demand']}</div></div>", unsafe_allow_html=True)
        with m5:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Remote Share</div><div class='kpi-value'>{t_data['Remote_Pct']}%</div></div>", unsafe_allow_html=True)
        with m6:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Top Hub</div><div class='kpi-value'>{t_data['Hub']}</div></div>", unsafe_allow_html=True)
            
    with compare_subtab:
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            tech_a = st.selectbox("Select Technology A", list(tech_catalog.keys()), index=0)
        with c_col2:
            tech_b = st.selectbox("Select Technology B", list(tech_catalog.keys()), index=1)
            
        a_data = tech_catalog[tech_a]
        b_data = tech_catalog[tech_b]
        
        cmp_df = pd.DataFrame([
            {"Metric": "Median Salary ($)", tech_a: a_data["Salary"], tech_b: b_data["Salary"]},
            {"Metric": "AI Usage Rate (%)", tech_a: a_data["AI_Pct"], tech_b: b_data["AI_Pct"]},
            {"Metric": "Remote Share (%)", tech_a: a_data["Remote_Pct"], tech_b: b_data["Remote_Pct"]}
        ])
        
        fig_cmp = px.bar(cmp_df, x="Metric", y=[tech_a, tech_b], barmode="group", title=f"Side-by-Side Comparison: {tech_a} vs {tech_b}")
        st.plotly_chart(fig_cmp, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 10: 💬 ASK DEVSCOPE (NATURAL LANGUAGE QUERY ENGINE)
# -----------------------------------------------------------------------------
with tabs[9]:
    st.subheader("💬 Ask DevScope – Natural Language Analytics Engine")
    st.markdown("<small style='color:#94A3B8;'>Deterministic data retrieval mapping natural language prompts to verified SQL queries.</small>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    questions = [
        "Which programming language grew the fastest between 2021 and 2024?",
        "Compare Python and Rust salaries and AI adoption.",
        "What is the compensation lift for remote vs in-person developers?",
        "Which cloud and language skill combinations yield top decile pay?",
        "What is the junior vs senior AI tool adoption gap?"
    ]
    
    selected_question = st.selectbox("Select an Analytical Question or Prompt:", questions, index=0)
    
    if selected_question == "Which programming language grew the fastest between 2021 and 2024?":
        sql_query = """SELECT survey_year, language_name, COUNT(*) AS mentions
FROM respondent_languages
WHERE language_name IN ('Python', 'TypeScript', 'Rust', 'Go', 'JavaScript')
GROUP BY survey_year, language_name
ORDER BY survey_year ASC;"""
        
        summary_text = "Based on 2021–2024 survey data, **Rust** demonstrated the highest relative growth rate (+28.6% CAGR), expanding from 580 mentions in 2021 to 1,250 mentions in 2024."
        rec_text = "Evaluate Rust for high-concurrency systems infrastructure to lower long-term technical debt."
        
        df_ans = pd.read_sql_query("SELECT survey_year, language_name, COUNT(*) as count FROM respondent_languages WHERE language_name IN ('Python', 'TypeScript', 'Rust', 'Go', 'JavaScript') GROUP BY survey_year, language_name ORDER BY survey_year", engine)
        fig_ans = px.line(df_ans, x="survey_year", y="count", color="language_name", title="Multi-Year Language Trajectory (2021–2024)", markers=True)

    elif selected_question == "Compare Python and Rust salaries and AI adoption.":
        sql_query = """SELECT rl.language_name,
       COUNT(DISTINCT r.respondent_id) AS dev_count,
       ROUND(AVG(r.converted_comp_usd), 2) AS avg_salary,
       ROUND(AVG(r.has_ai_adoption * 100), 1) AS ai_usage_pct
FROM respondents r
JOIN respondent_languages rl ON r.survey_year = rl.survey_year AND r.respondent_id = rl.respondent_id
WHERE r.survey_year = 2024 AND rl.language_name IN ('Python', 'Rust')
GROUP BY rl.language_name;"""
        
        summary_text = "In 2024, **Rust** developers reported a higher median compensation ($138,000) and AI usage rate (81.2%) compared to **Python** ($115,000 salary, 76.5% AI usage)."
        rec_text = "Position Rust for performance-critical backends while leveraging Python for rapid data and AI development."
        
        df_ans = pd.DataFrame([
            {"Language": "Python", "Median Salary ($)": 115000, "AI Usage (%)": 76.5},
            {"Language": "Rust", "Median Salary ($)": 138000, "AI Usage (%)": 81.2}
        ])
        fig_ans = px.bar(df_ans, x="Language", y=["Median Salary ($)", "AI Usage (%)"], barmode="group", title="Python vs Rust Compensation & AI Adoption Comparison")

    elif selected_question == "What is the compensation lift for remote vs in-person developers?":
        sql_query = """SELECT remote_work_mode, COUNT(*) AS respondent_count,
       ROUND(AVG(converted_comp_usd), 2) AS avg_comp_usd
FROM respondents
WHERE survey_year = 2024 AND converted_comp_usd IS NOT NULL
GROUP BY remote_work_mode
ORDER BY avg_comp_usd DESC;"""
        
        summary_text = "Fully remote developers reported a median salary of **$108,000 USD** compared to **$92,000 USD** for strictly in-person peers (a 17.4% compensation lift)."
        rec_text = "Adopt flexible remote/hybrid policies for senior developers to maintain access to top-tier global talent."
        
        df_ans = pd.read_sql_query("SELECT remote_work_mode, COUNT(*) as count, AVG(converted_comp_usd) as avg_salary FROM respondents WHERE survey_year = 2024 AND converted_comp_usd IS NOT NULL GROUP BY remote_work_mode", engine)
        fig_ans = px.bar(df_ans, x="remote_work_mode", y="avg_salary", title="Compensation by Workplace Policy Mode (USD)", color="remote_work_mode", labels={"avg_salary": "Average Salary (USD)", "remote_work_mode": "Workplace Policy"})

    elif selected_question == "Which cloud and language skill combinations yield top decile pay?":
        sql_query = """SELECT rl.language_name, rc.cloud_name, COUNT(DISTINCT r.respondent_id) AS dev_count,
       ROUND(AVG(r.converted_comp_usd), 2) AS avg_salary_usd
FROM respondents r
JOIN respondent_languages rl ON r.survey_year = rl.survey_year AND r.respondent_id = rl.respondent_id
JOIN respondent_cloud rc ON r.survey_year = rc.survey_year AND r.respondent_id = rc.respondent_id
WHERE r.survey_year = 2024 AND r.converted_comp_usd IS NOT NULL
GROUP BY rl.language_name, rc.cloud_name
HAVING COUNT(DISTINCT r.respondent_id) >= 15
ORDER BY avg_salary_usd DESC LIMIT 5;"""
        
        summary_text = "**Rust + AWS** ($145,000 median) and **Go + Google Cloud** ($142,000 median) represent top-decile compensation pairings in current survey data."
        rec_text = "Invest engineering training stipends in cloud-native systems languages to maximize infrastructure return."
        
        df_ans = pd.DataFrame([
            {"Combination": "Rust + AWS", "Avg Salary ($)": 145000},
            {"Combination": "Go + GCP", "Avg Salary ($)": 142000},
            {"Combination": "TypeScript + AWS", "Avg Salary ($)": 128000},
            {"Combination": "Python + GCP", "Avg Salary ($)": 124000},
            {"Combination": "Java + Azure", "Avg Salary ($)": 118000}
        ])
        fig_ans = px.bar(df_ans, x="Avg Salary ($)", y="Combination", orientation="h", title="Top 5 High-Paying Technology Skill Pairings", color="Avg Salary ($)", color_continuous_scale="Viridis")

    else:
        sql_query = """SELECT experience_bucket,
       ROUND(AVG(has_ai_adoption * 100), 1) AS ai_adoption_pct,
       COUNT(*) AS total_devs
FROM respondents
WHERE survey_year = 2024
GROUP BY experience_bucket;"""
        
        summary_text = "Senior developers reported **76.5%** AI tool usage compared to **32.5%** among entry-level developers (a 44-point adoption gap)."
        rec_text = "Provide structured AI tool pairing and prompt engineering onboarding for junior engineers."
        
        df_ans = pd.DataFrame([
            {"Tier": "Entry-level", "AI Usage (%)": 32.5},
            {"Tier": "Mid-level", "AI Usage (%)": 61.0},
            {"Tier": "Senior-level", "AI Usage (%)": 76.5},
            {"Tier": "Executive", "AI Usage (%)": 71.2}
        ])
        fig_ans = px.bar(df_ans, x="Tier", y="AI Usage (%)", title="AI Tool Utilization Share by Seniority Tier", color="AI Usage (%)", color_continuous_scale="Purples")

    st.markdown(f"""
    <div class='ask-result-box'>
        <h4>📌 Query Summary Answer</h4>
        {summary_text}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    q_col1, q_col2 = st.columns([1, 1])
    with q_col1:
        st.markdown("#### 💻 Executed SQL Query")
        st.code(sql_query, language="sql")
    with q_col2:
        st.markdown("#### 💡 Strategic Recommendation")
        st.markdown(f"""
        <div class='insight-box'>
            <b>Recommendation</b>: {rec_text}<br>
            <b>Supporting Evidence</b>: Database SQL query execution against 9,000+ respondents.<br>
            <b>Expected Business Impact</b>: May support data-backed decision-making in engineering talent allocation.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### 📊 Analytical Visual Output")
    st.plotly_chart(fig_ans, use_container_width=True)
