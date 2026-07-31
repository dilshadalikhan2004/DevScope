# DevScope Data Dictionary

This document serves as the authoritative Data Dictionary for the **DevScope – Developer Career Intelligence Platform**. It outlines the attributes, data types, business definitions, missingness protocols, and cleaning rules for the core normalized datasets ingested from the official **Stack Overflow Developer Surveys (2021–2024)** and **Tech Job Market Postings**.

---

## 1. Respondent Master Table (`Respondents`)

| Column Name | Raw Field (SO Survey) | Target Data Type | Business Definition | Missingness Protocol | Cleaning & Transformation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `respondent_id` | `ResponseId` | `INTEGER` (PK) | Unique survey respondent identifier. | Critical field; drop row if missing. | Cast to integer; retain unique IDs per survey year. |
| `survey_year` | Derived | `INTEGER` | Year of survey collection (2021–2024). | Mandatory field. | Added during ingestion based on raw file source. |
| `country` | `Country` | `VARCHAR(100)` | Primary country of residence. | Impute as `'Unknown'`. | Normalized using standardized ISO country lookup table. |
| `age_group` | `Age` | `VARCHAR(50)` | Categorical age bracket. | Impute as `'Unspecified'`. | Mapped to standard brackets (`18-24`, `25-34`, `35-44`, `45-54`, `55+`). |
| `years_experience` | `YearsCodePro` | `FLOAT` | Total years of professional coding experience. | Impute median by role/age. | Stripped text (`Less than 1 year` ➔ `0.5`, `More than 50 years` ➔ `50`). Outliers > 60 filtered. |
| `education_level` | `EdLevel` | `VARCHAR(100)` | Highest formal educational attainment. | Impute as `'No Formal Degree'`. | Standardized into 5 tiers (`Doctorate`, `Master's`, `Bachelor's`, `Some College`, `Self-Taught`). |
| `employment_type` | `Employment` | `VARCHAR(100)` | Current employment status. | Impute as `'Other'`. | Mapped to `Full-time`, `Part-time`, `Contractor`, `Unemployed`, `Student`. |
| `remote_work_mode` | `RemoteWork` | `VARCHAR(50)` | Remote work policy environment. | Impute based on company size. | Standardized to `In-person`, `Hybrid`, or `Remote`. |
| `company_size` | `OrgSize` | `VARCHAR(50)` | Size of employer organization. | Impute as `'Unknown'`. | Normalized into enterprise tiers (`Startup <20`, `Mid-market 20-499`, `Enterprise 500+`). |
| `converted_comp_usd` | `ConvertedCompYearly` | `FLOAT` | Total annual compensation in USD. | Retain as `NULL` for unpaid/students; filter out for salary benchmarks. | Converted via historical exchange rates. Outliers `< $1,000` or `> $2.5M` removed. |
| `salary_band` | Derived | `VARCHAR(50)` | Quantile compensation bucket. | Computed only if compensation present. | Categorized into `Entry (<$50k)`, `Mid ($50k-$100k)`, `High ($100k-$180k)`, `Top 10% (>$180k)`. |
| `job_satisfaction` | `JobSat` | `VARCHAR(50)` | Self-reported career & job satisfaction. | Impute as `'Neutral'`. | Mapped to a 5-point scale (`Very Satisfied`, `Slightly Satisfied`, `Neutral`, `Dissatisfied`, `Very Dissatisfied`). |

---

## 2. Multi-Select Technology Dimensions

Exploded junction tables handle multi-select technology fields (`Languages`, `Frameworks`, `Databases`, `CloudPlatforms`, `AITools`).

| Table Name | Entity Column | Attribute Column | Cleaning & Standardization Rule |
| :--- | :--- | :--- | :--- |
| `RespondentLanguages` | `respondent_id` | `language_name` | Semicolon-delimited string exploded; trimmed; case-normalized (e.g., `JavaScript`, `Python`, `Rust`). |
| `RespondentFrameworks` | `respondent_id` | `framework_name` | Exploded multi-select; normalized framework names (e.g., `React.js`, `Django`, `Next.js`, `Spring Boot`). |
| `RespondentDatabases` | `respondent_id` | `database_name` | Exploded multi-select; standardized DB names (e.g., `PostgreSQL`, `MongoDB`, `Redis`, `Snowflake`). |
| `RespondentCloud` | `respondent_id` | `cloud_name` | Exploded multi-select; normalized cloud providers (`AWS`, `Google Cloud`, `Microsoft Azure`, `Cloudflare`). |
| `RespondentAITools` | `respondent_id` | `ai_tool_name` | Exploded multi-select (2023–2024); standardized AI tools (`ChatGPT`, `GitHub Copilot`, `Claude`, `Gemini`). |

---

## 3. Executive Composite KPI Metrics (`ExecutiveKPIs`)

| Metric Name | Calculation Formula | Range | Business Significance |
| :--- | :--- | :--- | :--- |
| `Developer Market Health Index` | `(0.4 * EmploymentRate) + (0.3 * SatisfactionRate) + (0.3 * CompParityScore)` | `0.0 - 100.0` | Macro-level stability metric evaluating regional tech market viability. |
| `AI Adoption Index` | `(0.5 * ActiveAIUsers) + (0.3 * PositiveSentiment) + (0.2 * DailyWorkflowIntegration)` | `0.0 - 100.0` | Measures workforce AI penetration and operational maturity. |
| `Technology Growth Index (CAGR)` | `((Mentions_2024 / Mentions_2021) ^ (1/3) - 1) * 100` | `% Change` | Identifies accelerating technologies vs. declining legacy tools over a 4-year horizon. |
| `Salary Competitiveness Score` | `(Local_Median_Comp / Global_Role_Median_Comp) * 100` | Ratio | Evaluates regional compensation attractiveness for global remote hiring strategy. |
| `Skill Diversity Index` | `Count(Languages) + Count(Frameworks) + Count(Databases) + Count(Cloud)` | `1 - 30+` | Quantifies developer versatility and full-stack capabilities. |

---

## 4. Public Tech Job Postings Table (`JobPostings`)

| Column Name | Target Data Type | Business Definition | Cleaning Rule |
| :--- | :--- | :--- | :--- |
| `job_id` | `VARCHAR(50)` (PK) | Unique job posting identifier. | Unique string key. |
| `job_title` | `VARCHAR(200)` | Advertised role title. | Standardized into core roles (`Backend`, `Frontend`, `Full-Stack`, `Data/AI`, `DevOps/Cloud`). |
| `required_skills` | `TEXT` | Semicolon-delimited required skills & technologies. | Normalized and exploded to match technology tags. |
| `posted_country` | `VARCHAR(100)` | Hiring location country. | ISO country code mapped. |
| `offered_salary_min_usd` | `FLOAT` | Minimum advertised annual compensation USD. | Outliers cleaned. |
| `offered_salary_max_usd` | `FLOAT` | Maximum advertised annual compensation USD. | Outliers cleaned. |
| `remote_allowed` | `BOOLEAN` | Whether remote work is permitted. | Binary flag (`TRUE`/`FALSE`). |

---

## 5. Analytical Limitations & Methodological Considerations

1. **Self-Selection Bias**: Stack Overflow survey respondents are self-selected and may overrepresent engaged, active developers.
2. **Geographic Distribution Constraints**: Sample sizes vary across smaller developer markets; thresholds (`N >= 15`) are applied to filter noise.
3. **Purchasing Power Parity (PPP)**: Salaries are converted into nominal USD using annual average exchange rates and do not adjust for local living costs.
4. **Model Projections vs Predictions**: Growth forecasts represent mathematical trend extrapolations under historical adoption assumptions and should be evaluated alongside strategic market developments.
