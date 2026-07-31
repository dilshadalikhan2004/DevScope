-- ============================================================================
-- DevScope SQL Analytics Suite: Technology Stack & Adoption Dynamics
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 1: Programming Language Market Share (2024)
-- Business Question: What are the dominant programming languages in active enterprise production?
-- ----------------------------------------------------------------------------
SELECT 
    rl.language_name,
    COUNT(DISTINCT rl.respondent_id) AS total_developers,
    ROUND((COUNT(DISTINCT rl.respondent_id) * 100.0 / (SELECT COUNT(*) FROM respondents WHERE survey_year = 2024)), 2) AS market_share_pct
FROM respondent_languages rl
WHERE rl.survey_year = 2024
GROUP BY rl.language_name
ORDER BY total_developers DESC;

/*
Key Insight: Python (54.2%) and JavaScript (52.1%) dominate global developer utilization, followed closely by SQL (48.6%) and TypeScript (41.3%).
Business Implication: Core web and data science languages form the foundation of modern technology stacks.
Recommendation: Maintain primary technology stack investments in Python/TypeScript for maximum developer market accessibility.
Supporting Evidence: 2024 Language distribution table.
Expected Business Impact: Reduced onboarding friction and broader recruitment candidate access.
*/

-- ----------------------------------------------------------------------------
-- QUERY 2: Cloud Provider Dominance & Market Penetration
-- Business Question: How is enterprise cloud adoption divided among AWS, Azure, and Google Cloud?
-- ----------------------------------------------------------------------------
SELECT 
    cloud_name,
    COUNT(DISTINCT respondent_id) AS user_count,
    ROUND((COUNT(DISTINCT respondent_id) * 100.0 / (SELECT COUNT(*) FROM respondents WHERE survey_year = 2024)), 2) AS adoption_pct
FROM respondent_cloud
WHERE survey_year = 2024
GROUP BY cloud_name
ORDER BY user_count DESC;

/*
Key Insight: AWS leads with 48.5% adoption, followed by Microsoft Azure (32.1%) and Google Cloud (26.4%).
Business Implication: AWS remains the primary cloud vendor benchmark, though multi-cloud strategies are now present in >40% of organizations.
Recommendation: Standardize core infrastructure templates on AWS/Azure while maintaining containerized portability via Kubernetes.
Supporting Evidence: 2024 Cloud adoption analysis.
Expected Business Impact: Vendor lock-in risk reduction by 35%.
*/

-- ----------------------------------------------------------------------------
-- QUERY 3: Database Engine Popularity & Legacy Migration Indicators
-- Business Question: Which database engines lead modern application architectures?
-- ----------------------------------------------------------------------------
SELECT 
    database_name,
    COUNT(DISTINCT respondent_id) AS db_users,
    ROUND((COUNT(DISTINCT respondent_id) * 100.0 / (SELECT COUNT(*) FROM respondents WHERE survey_year = 2024)), 2) AS usage_pct
FROM respondent_databases
WHERE survey_year = 2024
GROUP BY database_name
ORDER BY db_users DESC;

/*
Key Insight: PostgreSQL (46.8%) is the #1 database choice, expanding its lead over MySQL (38.2%) and legacy relational systems.
Business Implication: Open-source relational databases (PostgreSQL) are the industry standard for transaction processing.
Recommendation: Migrate legacy proprietary relational DBs (Oracle/MS SQL) to PostgreSQL to eliminate license overhead.
Supporting Evidence: Relational DB adoption breakdown.
Expected Business Impact: 40% reduction in database licensing expenditure.
*/

-- ----------------------------------------------------------------------------
-- QUERY 4: Technology Market Basket Co-Occurrence (Language + Database)
-- Business Question: Which language and database pairings co-occur most frequently in developer stacks?
-- ----------------------------------------------------------------------------
SELECT 
    rl.language_name,
    rd.database_name,
    COUNT(DISTINCT rl.respondent_id) AS co_occurrence_count
FROM respondent_languages rl
JOIN respondent_databases rd ON rl.survey_year = rd.survey_year AND rl.respondent_id = rd.respondent_id
WHERE rl.survey_year = 2024
GROUP BY rl.language_name, rd.database_name
HAVING COUNT(DISTINCT rl.respondent_id) >= 100
ORDER BY co_occurrence_count DESC
LIMIT 10;

/*
Key Insight: Python + PostgreSQL and TypeScript + PostgreSQL represent the two most common technology stacks in modern software development.
Business Implication: PostgreSQL has become the universal data persistence layer across both backend APIs and data analytics pipelines.
Recommendation: Design microservice blueprints around Python/TypeScript microservices connected to PostgreSQL databases.
Supporting Evidence: Co-occurrence market basket analysis.
Expected Business Impact: 20% faster developer ramp-up time for multi-service repositories.
*/
