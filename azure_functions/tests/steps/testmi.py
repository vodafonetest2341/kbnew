import os
import tempfile
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.textanalytics import TextAnalyticsClient
from openai import AzureOpenAI, OpenAI, RateLimitError
from azure.storage.blob import BlobServiceClient
import requests
from behave import given, when, then
from common.sql import __SqlConnector__
from common.search import __SearchManager__


def _get_secret(
    secret_name,
):
    _key_vault_url = os.environ["KEY_VAULT_URL"]
    _secret_name = secret_name
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


@given("the KeyVault")
def step_impl(
    context,
):
    pass


@when("we get the secret {secret_name} using managed identity")
def step_impl(
    context,
    secret_name,
):
    _secret_value = _get_secret(
        secret_name=secret_name,
    )
    context._secret_value = _secret_value


@then("the secret returned is {secret_value}")
def step_impl(
    context,
    secret_value,
):
    _expected_secret_value = secret_value
    _actual_secret_value = context._secret_value
    assert _actual_secret_value == _expected_secret_value


@given("the Document Intelligence {document_intelligence_endpoint}")
def step_impl(
    context,
    document_intelligence_endpoint,
):
    context._document_intelligence_endpoint = _get_secret(
        document_intelligence_endpoint
    )


@when(
    "we call the begin analyze document method with a document {file_path} using managed identity"
)
def step_impl(
    context,
    file_path,
):
    _model_id = "prebuilt-layout"
    _endpoint = context._document_intelligence_endpoint
    _credential = DefaultAzureCredential()
    with open(file_path, "rb") as _content:
        with DocumentAnalysisClient(
            endpoint=_endpoint,
            credential=_credential,
            headers={"x-ms-useragent": "azure-functions/1.0.0"},
        ) as form_recognizer_client:
            poller = form_recognizer_client.begin_analyze_document(
                model_id=_model_id,
                document=_content,
            )
            form_recognizer_results = poller.result()
    context._form_recognizer_results = form_recognizer_results


@then("we should get the results from the Document Intelligence service")
def step_impl(
    context,
):
    assert context._form_recognizer_results is not None


@given("the AI Language {ai_language_endpoint}")
def step_impl(
    context,
    ai_language_endpoint,
):
    context._ai_language_endpoint = _get_secret(
        secret_name=ai_language_endpoint,
    )


@when(
    "we call the recognize pii entites method with a text {sample_text} using managed identity"
)
def step_impl(
    context,
    sample_text,
):
    _sample_text = sample_text
    _credential = DefaultAzureCredential()
    _text_analytics_client = TextAnalyticsClient(
        endpoint=context._ai_language_endpoint,
        credential=_credential,
    )
    response = _text_analytics_client.recognize_pii_entities(
        [_sample_text],
        language="en",
    )
    result = [doc for doc in response if not doc.is_error]
    for doc in result:
        context._redacted_text = doc.redacted_text


@then(
    "we should get the results from the AI Language with redacted text {redacted_text}"
)
def step_impl(
    context,
    redacted_text,
):
    _expected_text = redacted_text
    _actual_text = context._redacted_text
    assert _actual_text == _expected_text


@given("the SQL Server {sql_server} and SQL Database {sql_database}")
def step_impl(
    context,
    sql_server,
    sql_database,
):
    context._sql_server = _get_secret(
        secret_name=sql_server,
    )
    context._sql_database = _get_secret(
        secret_name=sql_database,
    )


@when("we call the database with a query {sample_query} using managed identity")
def step_impl(
    context,
    sample_query,
):
    _sample_query = sample_query
    _sql_connector = __SqlConnector__(
        sql_server=context._sql_server,
        sql_database=context._sql_database,
    )
    _connection = _sql_connector.get_sql_connection()
    _cursor = _connection.cursor()
    _cursor.execute(_sample_query)
    _row = _cursor.fetchone()
    _response = _row[0]
    context._actual_response = _response


@then("we should get the results from the database with text {query_response}")
def step_impl(
    context,
    query_response,
):
    _expected_response = int(query_response)
    _actual_response = context._actual_response
    assert _actual_response == _expected_response


@given("the Azure Open AI service {open_ai_endpoint}")
def step_impl(
    context,
    open_ai_endpoint,
):
    context._open_ai_endpoint = _get_secret(
        secret_name=open_ai_endpoint,
    )


@when(
    "we call create embeddings from deployment {open_ai_deployment} for model {open_ai_model_name} with api version {open_ai_api_version} with a text {sample_text} using managed identity"
)
def step_impl(
    context,
    open_ai_deployment,
    open_ai_model_name,
    open_ai_api_version,
    sample_text,
):
    _credential = DefaultAzureCredential()
    _access_token = _credential.get_token(
        "https://cognitiveservices.azure.com/.default"
    )
    _token = _access_token.token
    _open_ai_client = AzureOpenAI(
        azure_endpoint=context._open_ai_endpoint,
        azure_deployment=open_ai_deployment,
        api_key=_token,
        api_version=open_ai_api_version,
    )
    _emb_response = _open_ai_client.embeddings.create(
        model=open_ai_model_name,
        input=sample_text,
    )
    for data in _emb_response.data:
        context._actual_result = data.embedding


@then("we should get the vectors {vectors} from the Azure Open AI service")
def step_impl(
    context,
    vectors,
):
    _expected_result = list(map(float, vectors.split(",")))
    _actual_result = context._actual_result[:3]
    assert len(_actual_result) == len(_expected_result)


@given("the Azure AI Search service {ai_search_endpoint}")
def step_impl(
    context,
    ai_search_endpoint,
):
    context._ai_search_endpoint = _get_secret(
        secret_name=ai_search_endpoint,
    )


@when(
    "we call create index method to create the index {index_name} using managed identity"
)
def step_impl(
    context,
    index_name,
):
    _search_manager = __SearchManager__(
        endpoint=context._ai_search_endpoint,
        index_name=index_name,
    )
    _result = _search_manager.create_index()
    context._result = _result


@then("the index should be created")
def step_impl(
    context,
):
    assert context._result is not None


@given(
    "the Azure Storage Account {storage_account_url} with container {container_name}"
)
def step_impl(
    context,
    storage_account_url,
    container_name,
):
    context._storage_account_url = _get_secret(
        secret_name=storage_account_url,
    )
    context._container_name = container_name


@when("we call download method on the blob {blob_path}")
def step_impl(
    context,
    blob_path,
):
    _blob_path = blob_path
    _credential = DefaultAzureCredential()
    with BlobServiceClient(
        account_url=context._storage_account_url,
        credential=_credential,
    ) as _service_client:
        with _service_client.get_blob_client(
            container=context._container_name,
            blob=_blob_path,
        ) as _blob_client:
            _temp_file_path = os.path.join(
                tempfile.gettempdir(), os.path.basename(_blob_path)
            )
            with open(_temp_file_path, "wb") as _temp_file:
                _download_stream = _blob_client.download_blob()
                _temp_file.write(_download_stream.readall())
                context._downloaded_file_size = os.path.getsize(_temp_file_path)


@then("the downloaded file size is {size}")
def step_impl(
    context,
    size,
):
    _expected_file_size = int(size)
    _actual_file_size = context._downloaded_file_size
    assert _actual_file_size == _expected_file_size


# Step definitions for testing Azure Function App for PII redaction
@given("the Azure Function App URL {function_app_url} with {end_point}")
def step_impl(
    context,
    function_app_url,
    end_point,
):
    _end_point = end_point
    _function_app_url = _get_secret(
        secret_name=function_app_url,
    )
    context._function_key = _get_secret(
        secret_name=os.environ["FUNCTION_APP_KEY_NAME"],
    )
    context._function_app_url = f"{_function_app_url}{_end_point}"


@when("we call the redactPII API with a valid containerFilePath {container_file_path}")
def step_impl(context, container_file_path):
    _function_app_url = context._function_app_url
    url = f"{_function_app_url}{container_file_path}"
    headers = {
        "x-functions-key": context._function_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)  # nosec
    context._content_api_response = response.status_code == 200  # nosec
    # Make the HTTP request to the getContent API with the provided containerFilePath
    # Check if the response is successful


@then("we should receive a successful response")
def step_impl(context):
    assert context._content_api_response


@when(
    "we call the redactPII API with an invalid containerFilePath {container_file_path}"
)
def step_impl(context, container_file_path):
    _function_app_url = context._function_app_url
    url = f"{_function_app_url}{container_file_path}"
    headers = {
        "x-functions-key": context._function_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)  # nosec
    context._content_api_response = response.status_code == 404  # nosec


@then("we should receive a failure response")
def step_impl(context):
    assert context._content_api_response


@when("we call the getContent API with a valid containerFilePath {container_file_path}")
def step_impl(context, container_file_path):
    _function_app_url = context._function_app_url
    url = f"{_function_app_url}{container_file_path}"
    headers = {
        "x-functions-key": context._function_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)  # nosec
    context._content_api_response = response.status_code == 200  # nosec
    # Make the HTTP request to the getContent API with the provided containerFilePath
    # Check if the response is successful


def step_impl(context):
    assert context._content_api_response


@when(
    "we call the getEmbeddings API with a valid containerFilePath {container_file_path}"
)
def step_impl(context, container_file_path):
    _function_app_url = context._function_app_url
    url = f"{_function_app_url}{container_file_path}"
    headers = {
        "x-functions-key": context._function_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)  # nosec
    context._content_api_response = response.status_code == 200  # nosec


@when(
    "we call the createIndexes API with a valid containerFilePath {container_file_path}"
)
def step_impl(context, container_file_path):
    _function_app_url = context._function_app_url
    url = f"{_function_app_url}{container_file_path}"
    headers = {
        "x-functions-key": context._function_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)  # nosec
    context._content_api_response = response.status_code == 200  # nosec


@when(
    "we call the getContent API with an invalid containerFilePath {container_file_path}"
)
def step_impl(context, container_file_path):
    _function_app_url = context._function_app_url
    url = f"{_function_app_url}{container_file_path}"
    headers = {
        "x-functions-key": context._function_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)  # nosec
    context._content_api_response = response.status_code == 404  # nosec
