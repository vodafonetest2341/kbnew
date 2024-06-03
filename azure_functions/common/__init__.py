# Common classes to be reused
class __ValidationException__(Exception):
    def __init__(
        self,
        *args,
    ):
        super().__init__(
            *args,
        )


# constants class for keeping all constants variable (fixed ones)
class __Constants__:
    # common date format
    DATE_FORMAT = "yyyy-MM-dd"

    # key vault constants
    class __Keyvault__:
        # Document Intelligence Service constants
        document_intelligent_endPoint_secret = (
            "aidi-vf-grp-oai-aib-de-docint-01-endpoint"  # nosec #ignore on bandit scan
        )
        # Storage Blob constants
        storage_account_basePath_secret = (
            "oai-vf-grp-oai-aib-we-oai-base"  # nosec #ignore on bandit scan
        )
        # SQL Server constants
        sql_server_name_secret = (
            "srv-vf-grp-sql-aib-de-srv-sqlserver"  # nosec #ignore on bandit scan
        )
        sql_db_name_secret = (
            "srv-vf-grp-sql-aib-de-srv-sqldb"  # nosec #ignore on bandit scan
        )
        open_ai_service_secret_name = (
            "srv-vf-grp-sql-aib-de-srv-openai-endpoint"  # nosec #ignore on bandit scan
        )
        app_insights_instkey = (
            "srv-vf-grp-sql-aib-de-srv-ai-instkey"  # nosec #ignore on bandit scan
        )
        lang_endpoint_secret = (
            "srv-vf-grp-sql-aib-de-srv-lang-endpoint"  # nosec #ignore on bandit scan
        )
        azure_ai_search_service = "srv-vf-grp-sql-aib-de-srv-ai-search-endpoint"  # nosec #ignore on bandit scan
        azure_ai_search_index = (
            "srv-vf-grp-sql-aib-de-srv-ai-search-index"  # nosec #ignore on bandit scan
        )
