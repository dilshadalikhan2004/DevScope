// ============================================================================
// DevScope Power Query M-Code Scripts for Power BI Import
// Connects to PostgreSQL or SQLite relational database engine
// ============================================================================

// ----------------------------------------------------------------------------
// TABLE 1: FactRespondents
// ----------------------------------------------------------------------------
let
    Source = PostgreSQL.Database("localhost", "devscope"),
    public_respondents = Source{[Schema="public",Item="respondents"]}[Data],
    TypedTable = Table.TransformColumnTypes(public_respondents,{
        {"survey_year", Int64.Type},
        {"respondent_id", Int64.Type},
        {"country", type text},
        {"years_experience", type number},
        {"education_level", type text},
        {"employment_type", type text},
        {"remote_work_mode", type text},
        {"company_size", type text},
        {"converted_comp_usd", type number},
        {"job_satisfaction", type text},
        {"experience_bucket", type text},
        {"salary_band", type text},
        {"has_ai_adoption", type logical}
    })
in
    TypedTable

// ----------------------------------------------------------------------------
// TABLE 2: DimRespondentLanguages
// ----------------------------------------------------------------------------
let
    Source = PostgreSQL.Database("localhost", "devscope"),
    public_respondent_languages = Source{[Schema="public",Item="respondent_languages"]}[Data]
in
    public_respondent_languages

// ----------------------------------------------------------------------------
// TABLE 3: DimRespondentCloud
// ----------------------------------------------------------------------------
let
    Source = PostgreSQL.Database("localhost", "devscope"),
    public_respondent_cloud = Source{[Schema="public",Item="respondent_cloud"]}[Data]
in
    public_respondent_cloud

// ----------------------------------------------------------------------------
// TABLE 4: DimRespondentAITools
// ----------------------------------------------------------------------------
let
    Source = PostgreSQL.Database("localhost", "devscope"),
    public_respondent_ai_tools = Source{[Schema="public",Item="respondent_ai_tools"]}[Data]
in
    public_respondent_ai_tools

// ----------------------------------------------------------------------------
// TABLE 5: DimJobPostings
// ----------------------------------------------------------------------------
let
    Source = PostgreSQL.Database("localhost", "devscope"),
    public_job_postings = Source{[Schema="public",Item="job_postings"]}[Data]
in
    public_job_postings
