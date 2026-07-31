-- DevScope Database Performance Tuning Indexes

CREATE INDEX IF NOT EXISTS idx_resp_year_country ON respondents(survey_year, country);
CREATE INDEX IF NOT EXISTS idx_resp_comp ON respondents(converted_comp_usd);
CREATE INDEX IF NOT EXISTS idx_resp_exp ON respondents(years_experience);
CREATE INDEX IF NOT EXISTS idx_resp_remote ON respondents(remote_work_mode);

CREATE INDEX IF NOT EXISTS idx_lang_name ON respondent_languages(language_name);
CREATE INDEX IF NOT EXISTS idx_fw_name ON respondent_frameworks(framework_name);
CREATE INDEX IF NOT EXISTS idx_db_name ON respondent_databases(database_name);
CREATE INDEX IF NOT EXISTS idx_cloud_name ON respondent_cloud(cloud_name);
CREATE INDEX IF NOT EXISTS idx_ai_name ON respondent_ai_tools(ai_tool_name);

CREATE INDEX IF NOT EXISTS idx_job_title ON job_postings(job_title);
CREATE INDEX IF NOT EXISTS idx_job_country ON job_postings(posted_country);
