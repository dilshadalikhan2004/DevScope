-- DevScope Relational Schema Definition
-- Supports PostgreSQL and SQLite syntax

DROP TABLE IF EXISTS respondent_languages;
DROP TABLE IF EXISTS respondent_frameworks;
DROP TABLE IF EXISTS respondent_databases;
DROP TABLE IF EXISTS respondent_cloud;
DROP TABLE IF EXISTS respondent_ai_tools;
DROP TABLE IF EXISTS respondents;
DROP TABLE IF EXISTS job_postings;

-- Fact Table: Survey Respondents (2021-2024)
CREATE TABLE respondents (
    survey_year INTEGER NOT NULL,
    respondent_id INTEGER NOT NULL,
    country VARCHAR(100),
    age_group VARCHAR(50),
    years_experience REAL,
    education_level VARCHAR(100),
    employment_type VARCHAR(100),
    remote_work_mode VARCHAR(50),
    company_size VARCHAR(50),
    converted_comp_usd REAL,
    job_satisfaction VARCHAR(50),
    languages_raw TEXT,
    frameworks_raw TEXT,
    databases_raw TEXT,
    cloud_raw TEXT,
    ai_tools_raw TEXT,
    experience_bucket VARCHAR(50),
    salary_band VARCHAR(50),
    lang_count INTEGER,
    fw_count INTEGER,
    db_count INTEGER,
    cloud_count INTEGER,
    ai_count INTEGER,
    skill_diversity_index INTEGER,
    has_ai_adoption BOOLEAN,
    PRIMARY KEY (survey_year, respondent_id)
);

-- Exploded Multi-Select Technology Tables
CREATE TABLE respondent_languages (
    survey_year INTEGER,
    respondent_id INTEGER,
    language_name VARCHAR(100)
);

CREATE TABLE respondent_frameworks (
    survey_year INTEGER,
    respondent_id INTEGER,
    framework_name VARCHAR(100)
);

CREATE TABLE respondent_databases (
    survey_year INTEGER,
    respondent_id INTEGER,
    database_name VARCHAR(100)
);

CREATE TABLE respondent_cloud (
    survey_year INTEGER,
    respondent_id INTEGER,
    cloud_name VARCHAR(100)
);

CREATE TABLE respondent_ai_tools (
    survey_year INTEGER,
    respondent_id INTEGER,
    ai_tool_name VARCHAR(100)
);

-- Job Market Postings Table
CREATE TABLE job_postings (
    job_id VARCHAR(50) PRIMARY KEY,
    job_title VARCHAR(200),
    required_skills TEXT,
    posted_country VARCHAR(100),
    offered_salary_min_usd REAL,
    offered_salary_max_usd REAL,
    remote_allowed BOOLEAN
);
