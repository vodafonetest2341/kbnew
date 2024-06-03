import os
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class __KeyVaultHandler__:

    def __init__(
        self,
        **kwargs,
    ) -> None:
        logging.info(f"Getting KEY_VAULT_URL from environment variables")
        self.key_vault_url = os.environ["KEY_VAULT_URL"]
        logging.info(f"Got KEY_VAULT_URL as {self.key_vault_url}")

    def _get_secret(
        self,
        **kwargs,
    ):
        _key_vault_url = self.key_vault_url
        _secret_name = kwargs.get("secret_name")
        _credential = DefaultAzureCredential()
        _secret_client = SecretClient(
            _key_vault_url,
            _credential,
        )
        _retrieved_secret = _secret_client.get_secret(
            _secret_name,
        )
        _secret_value = _retrieved_secret.value

        return _secret_value

    def get_secret(
        self,
        **kwargs,
    ):
        _secret_value = self._get_secret(**kwargs)
        return _secret_value
