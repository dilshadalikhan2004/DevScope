# DevScope Power BI (`DevScope.pbix`) Data Model & Layout Specification

This specification documents the relational data model, DAX measures, visual hierarchy, and color palettes for building `DevScope.pbix` in Power BI Desktop.

---

## 1. Data Model Relationships (Star Schema)

- **Fact Table**: `Respondents` (Fact table holding survey responses)
- **Dimension Tables**:
  - `RespondentLanguages` (1-to-many relationship with `Respondents` on `survey_year` + `respondent_id`)
  - `RespondentCloud` (1-to-many relationship)
  - `RespondentDatabases` (1-to-many relationship)
  - `RespondentAITools` (1-to-many relationship)
  - `JobPostings` (Independent dimension table linked via skill criteria)

---

## 2. Power BI Page Hierarchy & Layout

1. **Page 1: 🏠 Executive Overview**
   - KPI Cards: Market Health Index, AI Adoption %, Remote %, Median Salary.
   - Donut Chart: Employment Type Distribution.
   - Bar Chart: Remote vs Hybrid vs In-Person.
   - Executive Callout: Key Insight & Recommendation Card.

2. **Page 2: 💰 Compensation Intelligence**
   - Box Plot: Salary Distribution by Experience Bucket.
   - Map Visual: Median Salary by Country.
   - Bar Chart: Salary Lift by Remote Status.

3. **Page 3: 🚀 Technology Stack & Growth**
   - Horizontal Bar Chart: Top 15 Languages.
   - Tree Map: Cloud Provider Market Share.
   - Matrix Visual: Language + Database Co-Occurrence.

4. **Page 4: 🤖 AI Readiness Dashboard**
   - Donut Chart: AI Tool Usage Share.
   - Bar Chart: AI Adoption by Career Level.

5. **Page 5: 🔮 Future Skills Forecast**
   - Line Chart: Multi-Year CAGR Trajectories (2021-2024).
   - Clustered Column Chart: Current vs 2027 Projected Skill Mentions.
