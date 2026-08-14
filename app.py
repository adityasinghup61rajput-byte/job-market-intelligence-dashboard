import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

from src.config import DB_PATH
from src.genai import generate_insight


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Cloud Job Market Intelligence",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
}

.hero h1 {
    margin: 0;
    font-size: 38px;
    font-weight: 800;
}

.hero p {
    margin-top: 8px;
    color: #dbeafe;
    font-size: 16px;
}

.kpi {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    min-height: 120px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
}

.kpi-label {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
}

.kpi-value {
    color: #0f172a;
    font-size: 28px;
    font-weight: 800;
    margin-top: 8px;
}

.section-title {
    font-size: 23px;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 12px;
    color: #0f172a;
}

.insight {
    background: white;
    border-left: 5px solid #2563eb;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE CHECK
# =========================================================

if not DB_PATH.exists():

    st.error("❌ Warehouse database not found.")

    st.info(
        "Run this command first:\n\n"
        "`python -m orchestration.pipeline`"
    )

    st.stop()


# =========================================================
# DATABASE QUERY FUNCTION
# =========================================================

def query(sql):

    with sqlite3.connect(DB_PATH) as con:

        return pd.read_sql_query(sql, con)


# =========================================================
# LOAD JOB DATA
# =========================================================

jobs = query("""
SELECT
    f.job_id,
    t.job_title,
    c.company,
    l.location,
    f.experience,
    f.salary_min,
    f.salary_max,
    f.salary_avg,
    f.employment_type,
    d.full_date AS posted_date

FROM fact_job_posting f

LEFT JOIN dim_company c
    ON f.company_key = c.company_key

LEFT JOIN dim_location l
    ON f.location_key = l.location_key

LEFT JOIN dim_title t
    ON f.title_key = t.title_key

LEFT JOIN dim_date d
    ON f.date_key = d.date_key
""")


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("☁️ Job Market")

st.sidebar.caption(
    "Interactive dashboard filters"
)


locations = sorted(
    jobs["location"].dropna().unique()
)

titles = sorted(
    jobs["job_title"].dropna().unique()
)

employment_types = sorted(
    jobs["employment_type"].dropna().unique()
)


selected_locations = st.sidebar.multiselect(
    "📍 Location",
    locations,
    default=locations
)


selected_titles = st.sidebar.multiselect(
    "💼 Job Title",
    titles,
    default=titles
)


selected_employment = st.sidebar.multiselect(
    "🧑‍💻 Employment Type",
    employment_types,
    default=employment_types
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered = jobs[
    jobs["location"].isin(selected_locations)
    &
    jobs["job_title"].isin(selected_titles)
    &
    jobs["employment_type"].isin(selected_employment)
].copy()


if filtered.empty:

    st.warning(
        "⚠️ No jobs match the selected filters."
    )

    st.stop()


# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">

<h1>☁️ Cloud Job Market Intelligence</h1>

<p>
Bronze → Silver → Gold → Star Schema → SQL → GenAI
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_jobs = len(filtered)

average_salary = filtered["salary_avg"].mean()

highest_salary = filtered["salary_avg"].max()

top_city = (
    filtered["location"]
    .value_counts()
    .idxmax()
)


# =========================================================
# KPI CARDS
# =========================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        f"""
        <div class="kpi">

        <div class="kpi-label">
        TOTAL JOBS
        </div>

        <div class="kpi-value">
        {total_jobs:,}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="kpi">

        <div class="kpi-label">
        AVERAGE SALARY
        </div>

        <div class="kpi-value">
        ₹{average_salary:,.0f}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="kpi">

        <div class="kpi-label">
        HIGHEST AVG SALARY
        </div>

        <div class="kpi-value">
        ₹{highest_salary:,.0f}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        f"""
        <div class="kpi">

        <div class="kpi-label">
        TOP HIRING CITY
        </div>

        <div class="kpi-value">
        {top_city}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HIRING DEMAND
# =========================================================

st.markdown(
    '<div class="section-title">📊 Hiring Demand</div>',
    unsafe_allow_html=True
)


left, right = st.columns(2)


# ---------------------------------------------------------
# LOCATION CHART
# ---------------------------------------------------------

location_df = (
    filtered
    .groupby("location")
    .size()
    .reset_index(name="jobs")
    .sort_values("jobs")
)


with left:

    fig = px.bar(
        location_df,
        x="jobs",
        y="location",
        orientation="h",
        text="jobs",
        title="Jobs by Location"
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        xaxis_title="Number of Jobs",
        yaxis_title=""
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# JOB TITLE CHART
# ---------------------------------------------------------

title_df = (
    filtered
    .groupby("job_title")
    .size()
    .reset_index(name="jobs")
    .sort_values("jobs")
)


with right:

    fig = px.bar(
        title_df,
        x="jobs",
        y="job_title",
        orientation="h",
        text="jobs",
        title="Jobs by Job Title"
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        xaxis_title="Number of Jobs",
        yaxis_title=""
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SALARY ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">💰 Salary & Hiring Analysis</div>',
    unsafe_allow_html=True
)


left, right = st.columns(2)


# ---------------------------------------------------------
# SALARY BY LOCATION
# ---------------------------------------------------------

salary_df = (
    filtered
    .groupby("location", as_index=False)["salary_avg"]
    .mean()
    .sort_values(
        "salary_avg",
        ascending=False
    )
)


with left:

    fig = px.bar(
        salary_df,
        x="location",
        y="salary_avg",
        text_auto=".2s",
        title="Average Salary by Location"
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        xaxis_title="Location",
        yaxis_title="Average Salary (₹)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# COMPANY ANALYSIS
# ---------------------------------------------------------

company_df = (
    filtered
    .groupby("company")
    .size()
    .reset_index(name="jobs")
    .sort_values(
        "jobs",
        ascending=False
    )
)


with right:

    fig = px.pie(
        company_df,
        names="company",
        values="jobs",
        hole=0.45,
        title="Hiring Share by Company"
    )

    fig.update_layout(
        template="plotly_white",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SKILL ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">🛠️ Most In-Demand Skills</div>',
    unsafe_allow_html=True
)


raw = pd.read_csv(
    "data/raw/jobs.csv"
)


filtered_ids = set(
    filtered["job_id"]
)


skills = []


for _, row in raw.iterrows():

    if row["job_id"] in filtered_ids:

        for skill in str(
            row["skills"]
        ).split("|"):

            skill = skill.strip()

            if skill:

                skills.append(skill)


if skills:

    skill_df = (
        pd.Series(skills)
        .value_counts()
        .head(10)
        .rename_axis("skill")
        .reset_index(name="jobs")
        .sort_values("jobs")
    )


    fig = px.bar(
        skill_df,
        x="jobs",
        y="skill",
        orientation="h",
        text="jobs",
        title="Top 10 In-Demand Skills"
    )


    fig.update_layout(
        template="plotly_white",
        height=430,
        xaxis_title="Job Postings",
        yaxis_title="Skill"
    )


    fig.update_traces(
        textposition="outside"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# JOB DATA TABLE
# =========================================================

st.markdown(
    '<div class="section-title">🔎 Job Data</div>',
    unsafe_allow_html=True
)


st.dataframe(
    filtered.sort_values(
        "posted_date",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# GENAI
# =========================================================

st.markdown(
    '<div class="section-title">🤖 GenAI Career Insight</div>',
    unsafe_allow_html=True
)


insight = generate_insight(
    {
        "total_jobs": total_jobs,
        "avg_salary": average_salary
    }
)


st.markdown(
    f"""
    <div class="insight">

    {insight}

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ARCHITECTURE
# =========================================================

with st.expander(
    "🏗️ View Data Engineering Architecture"
):

    st.code(
"""
SOURCE
   ↓
BRONZE — Raw CSV / API
   ↓
SILVER — Cleaning + Validation
   ↓
GOLD — Curated Parquet
   ↓
STAR SCHEMA — Fact + Dimensions
   ↓
SQL ANALYTICS
   ↓
STREAMLIT DASHBOARD
   ↓
GENAI INSIGHTS
""",
        language="text"
    )


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "☁️ Cloud Job Market Intelligence • "
    "Cloud Data Engineering Capstone"
)