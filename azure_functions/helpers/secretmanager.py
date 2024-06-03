from common.handlers import __KeyVaultHandler__
from common import __Constants__


class __SecretsHandler__:

    def __init__(self):
        self._key_vault_handler = __KeyVaultHandler__()

    def get_secrets(self):
        # Get secrets from Azure Key Vault & account key
        forms_recognizer_service = self._key_vault_handler.get_secret(
            secret_name=__Constants__.__Keyvault__.document_intelligent_endPoint_secret,
        )
        storage_account_base = self._key_vault_handler.get_secret(
            secret_name=__Constants__.__Keyvault__.storage_account_basePath_secret,
        )
        sql_server_name = self._key_vault_handler.get_secret(
            secret_name=__Constants__.__Keyvault__.sql_server_name_secret,
        )
        sql_db_name = self._key_vault_handler.get_secret(
            secret_name=__Constants__.__Keyvault__.sql_db_name_secret,
        )
        open_ai_service = self._key_vault_handler.get_secret(
            secret_name=__Constants__.__Keyvault__.open_ai_service_secret_name,
        )
        app_inst_key = self._key_vault_handler.get_secret(
            secret_name=__Constants__.__Keyvault__.app_insights_instkey,
        )
        search_service = self._key_vault_handler.get_secret(
            secret_name=__Constants__.__Keyvault__.azure_ai_search_service,
        )
        index_name = self._key_vault_handler.get_secret(
            secret_name=__Constants__.__Keyvault__.azure_ai_search_index,
        )
        lang_endPoint_secret = self._key_vault_handler.get_secret(
            secret_name=__Constants__.__Keyvault__.lang_endpoint_secret,
        )

        return (
            forms_recognizer_service,
            storage_account_base,
            sql_server_name,
            sql_db_name,
            open_ai_service,
            app_inst_key,
            search_service,
            index_name,
            lang_endPoint_secret,
        )
