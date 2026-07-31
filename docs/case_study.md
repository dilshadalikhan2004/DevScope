# 📊 Executive Case Study – DevScope: Developer Career Intelligence Platform

**Author**: Talent & Workforce Analytics Lead  
**Target Organization**: GlobalTech Enterprises (Fictional Enterprise Stakeholder)  
**Target Program**: Google Data Analytics Apprenticeship Portfolio  

---

## 🎯 1. Business Problem & Context

Engineering leadership at multinational technology companies operates in an increasingly volatile talent market. Three major macro shifts create operational friction:
1. **Compensation Disparity & Inflation**: Remote hiring has blurred traditional geographic salary boundaries, raising developer compensation expectations worldwide.
2. **Generative AI Tool Penetration**: Generative AI tools (ChatGPT, GitHub Copilot) are rapidly reshaping engineering workflows, creating uncertainty around productivity gains and onboarding.
3. **Skill Supply vs. Demand Bottlenecks**: Enterprise demand for cloud-native systems programming languages (Rust, Go, TypeScript) outpaces available candidate pools.

**Core Objective**: Build an authentic, multi-source developer intelligence platform to enable data-backed decision-making in compensation benchmarking, tech stack selection, and talent acquisition.

---

## 🔬 2. Data Strategy & Multi-Source Methodology

To ensure 100% authenticity without synthetic data, DevScope integrates three complementary datasets:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Stack Overflow Developer Surveys (2021–2024): 9,000+ Cleaned Rows   │
│    - Global Compensation, Experience, Work Mode, Tech Usage, AI Tools  │
├────────────────────────────────────────────────────────────────────────┤
│ 2. Tech Job Market Postings Dataset: 1,500 Postings                    │
│    - Employer Skill Demands, Offered Salary Max, Remote Badges         │
├────────────────────────────────────────────────────────────────────────┤
│ 3. GitHub Octoverse Activity Benchmarks: Time-series momentum metrics   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 💡 3. Key Analytical Insights & Metric Verification

Every headline metric is 100% reproducible directly from raw datasets and relational SQL queries:

| Metric Headline | Verified Data Source & Query | Fact vs. Projection Distinction |
| :--- | :--- | :--- |
| **Remote Pay Lift (+17.4%)** | `sql/salary.sql` (Query 2) & `df_filtered.groupby('remote_work_mode')` | **Fact**: Historical 2024 survey median pay ($108k remote vs $92k in-person). |
| **AI Tool Adoption (72.1%)** | `etl/transform.py` & `respondent_ai_tools` | **Fact**: Measured proportion of professional respondents reporting daily AI tool usage. |
| **Rust 4-Year CAGR (+28.6%)** | `analysis/trend_analysis.py` & `respondent_languages` | **Fact**: Multi-year growth rate calculated from 2021 (580 mentions) to 2024 (1,250 mentions). |
| **Junior AI Usage Gap (44 pts)** | `notebooks/03_Analytics.ipynb` | **Fact**: Observed AI tool usage rate (76.5% senior vs 32.5% entry-level). |
| **2027 Skill Forecast** | `analysis/forecast_engine.py` | **Projection**: Model estimate under historical adoption assumptions. |

---

## 💬 4. "Ask DevScope" Natural-Language Analytics Interface

To allow stakeholders to query datasets without manual chart configuration, DevScope includes a deterministic natural-language query interface (**Tab 10**). 

The interface maps common executive questions to pre-compiled SQL queries and returns:
1. **Summary Answer**: Direct analytical answer.
2. **Executed SQL Query**: Full syntax-highlighted SQL for transparency.
3. **Interactive Chart**: Plotly visual breakdown.
4. **Strategic Recommendation**: Actionable business advice.

---

## 🚀 5. Strategic Recommendations & Expected Business Impact

| Strategic Area | Recommendation | Supporting Evidence | Expected Business Impact |
| :--- | :--- | :--- | :--- |
| **Workplace Policy** | Adopt a 'Remote-First for Senior Engineers, Hybrid for Entry-Level' policy framework. | 82% of survey respondents operate in Remote/Hybrid modes. | May support improved developer retention and candidate reach. |
| **AI Enablement** | Provide enterprise AI licenses and mandatory prompt engineering onboarding for junior hires. | 72.1% global AI adoption rate with 44-point junior usage lag. | May improve early-career developer onboarding velocity. |
| **Tech Stack Alignment** | Standardize core microservices architecture on Rust, Python, and TypeScript. | 4-year time series momentum (Rust +28.6% CAGR). | May support long-term codebase resilience and technical debt reduction. |
| **Talent Acquisition** | Combine targeted external recruitment for cloud-native skills with internal upskilling bootcamps. | Public job postings show high salary premiums ($165k-$220k) for Cloud+AI skills. | May help reduce hiring lead times and recruitment costs. |

---

## ⚠️ 6. Analytical Limitations & Methodological Considerations

Google values analytical rigor. DevScope explicitly documents the following data boundaries:

1. **Self-Selection Bias**: Stack Overflow survey respondents are self-selected and may overrepresent active, community-engaged engineers.
2. **Regional Coverage Constraints**: Public job posting datasets vary in geographical and industry coverage.
3. **Cost-of-Living Variance**: Salary comparisons reflect nominal converted USD values and do not adjust for local Purchasing Power Parity (PPP).
4. **Forecast Model Assumptions**: Projections are trend-based extrapolations under historical adoption rates and should be evaluated alongside broader macroeconomic shifts.

---

## 🧪 7. Rigor & Verification

- **Automated Testing**: 19 pytest integration and unit tests covering ETL cleaning, transformations, database schema integrity, SQL analytics queries, and forecasting math (`19 PASSED in 0.73s`).
- **Reproducibility**: Docker containerized (`docker-compose.yml`) with automated GitHub Actions CI/CD workflow (`.github/workflows/ci.yml`).
