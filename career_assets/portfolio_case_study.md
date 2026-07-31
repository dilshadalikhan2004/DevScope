# 💼 Portfolio Case Study – DevScope: Developer Career Intelligence Platform

**Project Title**: DevScope – Developer Career Intelligence Platform  
**Target Role**: Google Data Analytics Apprenticeship  
**Tech Stack**: Python 3.12, Pandas, NumPy, Plotly, Streamlit, PostgreSQL / SQLite, SQLAlchemy, Docker, pytest  

---

## 📌 Executive Summary

DevScope is a production-grade analytics platform that ingests, cleans, analyzes, and projects workforce dynamics across **9,000 Stack Overflow Developer Survey responses (2021–2024)** and **1,500 Tech Job Market Postings**. 

Built to solve talent planning challenges for enterprise technology leadership, DevScope translates complex multi-year survey rows into actionable decision support covering salary benchmarking, AI adoption, technology trends, and recruiter supply/demand gaps.

---

## 🎯 Business Problem

Global technology organizations face three major talent headwinds:
1. High compensation variance across remote vs in-person roles.
2. Rapid adoption of Generative AI tools with uneven penetration across seniority tiers.
3. Severe employer supply deficits for specialized cloud-native systems skills (Rust, Go, TypeScript).

---

## 🔬 Multi-Source Analytics Methodology

- **Authentic Data Pipeline**: Ingests official Stack Overflow Developer Survey CSVs (2021, 2022, 2023, 2024) and Tech Job Postings datasets with zero synthetic data.
- **Data Quality Protocols**: Missing values handled via strict, documented business logic protocols (`docs/data_dictionary.md`).
- **Feature Engineering**: Derivation of experience cohorts, exploded technology junction tables, and executive indexes (Market Health Index, AI Adoption Index, Remote Readiness Score).
- **Consolidated SQL Engine**: 50+ business SQL queries executed against SQLite / PostgreSQL relational schemas.

---

## 📊 Key Findings & Recommendations

1. **Remote Work Dynamics**: Fully remote developers earn a median salary of $108,000 USD compared to $92,000 for in-person peers.
   - *Recommendation*: Adopt a 'Remote-First for Senior Engineers, Hybrid for Entry-Level' policy to optimize talent reach.
2. **Generative AI Penetration**: AI adoption reached 72.1% among developers in 2024.
   - *Recommendation*: Provide enterprise AI tool licenses and structured prompt engineering training.
3. **Multi-Year Technology Velocity**: Rust (+28.6% CAGR) and TypeScript (+15.2% CAGR) exhibit the highest relative growth momentum.
   - *Recommendation*: Align long-term platform architecture with modern systems programming languages.

---

## 🧪 Rigor & Reproducibility

- **Automated Test Suite**: 19/19 pytest tests passing (`0.73s`).
- **Dockerization**: Single-command build via `docker-compose up --build`.
- **CI/CD**: GitHub Actions pipeline enforcing linting, data validation, and unit tests on push.
