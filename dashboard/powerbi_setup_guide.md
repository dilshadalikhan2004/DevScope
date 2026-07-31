# 📊 DevScope Power BI (`DevScope.pbix`) Executive Dashboard Guide

This guide documents the architecture, data connections, visual layouts, and DAX measures for building **`DevScope.pbix`** in Power BI Desktop to match the Streamlit application's design system and executive metrics.

---

## 🎨 Color Palette & Branding Specifications

To ensure visual consistency with the Streamlit dashboard:

- **Background Color**: Dark Slate `#0F172A`
- **Container / Card Background**: Slate Gray `#1E293B`
- **Border / Grid Color**: Slate Border `#334155`
- **Primary Accent / Text Highlight**: Sky Blue `#38BDF8`
- **Secondary Accent**: Emerald Green `#10B981`
- **Text Color**: Pure White `#F8FAFC` & Muted Gray `#94A3B8`

Import the custom dark theme JSON from [`dashboard/theme.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/DevScope/dashboard/theme.json) in Power BI Desktop (*View -> Themes -> Browse for themes*).

---

## 🎛️ Global Slicers & Filters (Top Slicer Panel on Every Page)

Each of the 4 executive pages features a top horizontal filter panel containing 5 synchronized interactive slicers:

1. **Survey Year**: Dropdown (`2021`, `2022`, `2023`, `2024`, `All`)
2. **Country**: Multi-select Searchable Dropdown
3. **Experience Tier**: Multi-select (`Entry-level`, `Mid-level`, `Senior-level`, `Executive`)
4. **Workplace Mode**: Multi-select (`Remote`, `Hybrid`, `In-person`)
5. **Technology**: Searchable Multi-select from `RespondentLanguages`

---

## 🖥️ Executive Page Hierarchy (4 Executive Pages)

### 📄 Page 1: 🏠 Executive Overview & Workforce Policy
- **Executive Summary Banner**: Text box card displaying the executive summary text.
- **Top KPI Cards**:
  - `Market Health Index` (`78.4 / 100`)
  - `AI Adoption Index %` (`[AI Adoption Index %]`)
  - `Remote Share %` (`[Remote Share %]`)
  - `Median Compensation` (`[Median Compensation USD]`)
- **Visual 1**: Ranked Horizontal Bar Chart — *Developer Employment Type Distribution*.
- **Visual 2**: Ranked Horizontal Bar Chart — *Workplace Policy Distribution (Remote vs In-Person)*.
- **Executive Decision Callout**: Card summarizing policy recommendations.

---

### 📄 Page 2: 💰 Compensation & Global Talent Benchmarks
- **Top KPI Cards**:
  - `US Median Compensation` (`[US Median Compensation USD]`)
  - `Remote Pay Premium %` (`[Remote Salary Premium %]`)
- **Visual 1**: Box Plot / Clustered Bar Chart — *Salary Distribution (USD) by Experience Tier*.
- **Visual 2**: Filled Map / Choropleth Map — *Global Median Salary Heatmap (USD)* with Tooltips:
  - Country, Median Salary, Respondent Count, Remote %, AI Adoption %.
- **Executive Decision Callout**: Mid-career retention insights card.

---

### 📄 Page 3: 🚀 Technology Stack & Demand Gaps
- **Top KPI Cards**:
  - `Hiring Difficulty Index` (`7.4 / 10`)
  - `Highest Demand Skill` (`Cloud + AI`)
  - `Avg Advertised Salary` (`$142,500`)
- **Visual 1**: Ranked Horizontal Bar Chart — *Top 10 Programming Languages by Developer Usage*.
- **Visual 2**: Matrix Visual — *Top Skill Combinations & Median Compensation*.
- **Visual 3**: Histogram / Column Chart — *Advertised Maximum Salary Distribution in Tech Job Postings*.

---

### 📄 Page 4: 🔮 AI Readiness & Future Skills Forecast
- **Top KPI Cards**:
  - `Senior AI Usage %` (`[Senior AI Adoption %]`)
  - `Junior AI Usage %` (`[Junior AI Adoption %]`)
  - `Junior AI Usage Gap` (`[Junior AI Adoption Gap]`)
- **Visual 1**: Ranked Horizontal Bar Chart — *AI Tool Utilization Share*.
- **Visual 2**: Clustered Column Chart — *Current (2024) vs Projected (2027) Skill Mentions*.
- **Visual 3**: Table Visual — *Multi-Year Skill CAGR Projections & Growth Categories*.

---

## ⚡ Data Connection Setup

1. Open Power BI Desktop.
2. Click **Get Data -> PostgreSQL Database** (or SQLite ODBC).
3. Server: `localhost`, Database: `devscope`.
4. Copy M-Code queries from [`dashboard/power_query_m_code.m`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/DevScope/dashboard/power_query_m_code.m).
5. Load tables into Star Schema:
   - `Respondents` (Fact)
   - `RespondentLanguages` (Dimension, 1-to-many on `survey_year` + `respondent_id`)
   - `RespondentCloud` (Dimension)
   - `RespondentAITools` (Dimension)
   - `JobPostings` (Dimension)
6. Copy DAX measures from [`dashboard/dax_measures.dax`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/DevScope/dashboard/dax_measures.dax).
7. Save report as **`DevScope.pbix`**.
