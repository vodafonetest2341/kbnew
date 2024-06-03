import time
import logging
import tiktoken
from typing import List, Optional
from azure.core.credentials import AccessToken
from openai import AzureOpenAI, OpenAI, RateLimitError
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)
from abc import ABC
from shared.shared import __EmbeddingBatch__
from helpers.configmapper import __ConfigMapper__


class __OpenAIEmbeddings__(ABC):
    """
    Contains common logic across both OpenAI and Azure OpenAI embedding services
    Can split source text into batches for more efficient embedding calls
    """

    def __init__(
        self,
        open_ai_model_name: str,
        supported_batch_aoai_model: str,
        disable_batch: bool = False,
        verbose: bool = False,
    ):
        self.open_ai_model_name = open_ai_model_name
        self.disable_batch = disable_batch
        self.verbose = verbose
        self.supported_batch_aoai_model = supported_batch_aoai_model

    def create_client(self) -> OpenAI:
        raise NotImplementedError

    def before_retry_sleep(self, retry_state):
        if self.verbose:
            logging.debug(
                "Rate limited on the OpenAI embeddings API, sleeping before retrying..."
            )

    def calculate_token_length(self, text: str):
        encoding = tiktoken.encoding_for_model(self.open_ai_model_name)
        return len(encoding.encode(text))

    def split_text_into_batches(self, texts: List[str]) -> List[__EmbeddingBatch__]:
        batch_info = self.supported_batch_aoai_model.get(self.open_ai_model_name)
        if not batch_info:
            raise NotImplementedError(
                f"Model {self.open_ai_model_name} is not supported with batch embedding operations"
            )

        batch_token_limit = batch_info["token_limit"]
        batch_max_size = batch_info["max_batch_size"]
        batches: List[__EmbeddingBatch__] = []
        batch: List[str] = []
        batch_token_length = 0
        for text in texts:
            text_token_length = self.calculate_token_length(text)
            if (
                batch_token_length + text_token_length >= batch_token_limit
                and len(batch) > 0
            ):
                batches.append(__EmbeddingBatch__(batch, batch_token_length))
                batch = []
                batch_token_length = 0

            batch.append(text)
            batch_token_length = batch_token_length + text_token_length
            if len(batch) == batch_max_size:
                batches.append(__EmbeddingBatch__(batch, batch_token_length))
                batch = []
                batch_token_length = 0

        if len(batch) > 0:
            batches.append(__EmbeddingBatch__(batch, batch_token_length))

        return batches

    # Creating Emedding batch with max limit of configurable value (1000 default one)
    def create_embedding_batch(self, texts: List[str]) -> List[List[float]]:
        batches = self.split_text_into_batches(texts)
        embeddings = []
        client = self.create_client()
        for batch in batches:
            for attempt in Retrying(
                retry=retry_if_exception_type(RateLimitError),
                wait=wait_random_exponential(min=15, max=60),
                stop=stop_after_attempt(15),
                before_sleep=self.before_retry_sleep,
            ):
                with attempt:
                    emb_response = client.embeddings.create(
                        model=self.open_ai_model_name, input=batch.texts
                    )
                    embeddings.extend([data.embedding for data in emb_response.data])
                    if self.verbose:
                        logging.debug(
                            f"Batch Completed. Batch size  {len(batch.texts)} Token count {batch.token_length}"
                        )
        # return generated emeddings with Azure Open AI list of vectors
        return embeddings
    # Create a single emeddings out of the batch

    def create_embedding_single(self, text: str) -> List[float]:
        client = self.create_client()
        for attempt in Retrying(
            retry=retry_if_exception_type(RateLimitError),
            wait=wait_random_exponential(min=15, max=60),
            stop=stop_after_attempt(15),
            before_sleep=self.before_retry_sleep,
        ):
            with attempt:
                emb_response = client.embeddings.create(
                    model=self.open_ai_model_name, input=text
                )
        # return single emedding
        return emb_response.data[0].embedding

    # create emdding method which will cal internally batch and single emedding model
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        if (
            not self.disable_batch
            and self.open_ai_model_name in self.supported_batch_aoai_model
        ):
            return self.create_embedding_batch(texts)

        return [self.create_embedding_single(text) for text in texts]


class __AzureOpenAIEmbeddingService__(__OpenAIEmbeddings__):
    """
    Class for using Azure OpenAI embeddings
    To learn more please visit https://learn.microsoft.com/azure/ai-services/openai/concepts/understand-embeddings
    """

    def __init__(self, open_ai_service: str, credential, config_mapper: __ConfigMapper__):
        super().__init__(
            config_mapper.openai_model,
            config_mapper.batch_model,
            config_mapper.disable_batch_vectors,
            config_mapper.verbose,
        )
        self.open_ai_service = open_ai_service
        self.open_ai_deployment = config_mapper.openai_deployment
        self.credential = credential
        self.cached_token: Optional[AccessToken] = None
        self.open_ai_api_version = config_mapper.open_ai_api_version

    def create_client(self) -> OpenAI:
        return AzureOpenAI(
            azure_endpoint=f"https://{self.open_ai_service}.openai.azure.com",
            azure_deployment=self.open_ai_deployment,
            api_key=self.wrap_credential(),
            api_version=self.open_ai_api_version,
        )

    def wrap_credential(self) -> str:
        if not self.cached_token or self.cached_token.expires_on <= time.time():
            self.cached_token = self.credential.get_token(
                "https://cognitiveservices.azure.com/.default"
            )

        return self.cached_token.token
