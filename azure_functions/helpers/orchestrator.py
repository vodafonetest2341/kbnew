import logging
import os
from azure.identity import DefaultAzureCredential
from applicationinsights import TelemetryClient
from helpers.sqlmanager import __DbOperationsManager__
from helpers.documentmanager import __DocumentAnalysisManager__
from helpers.blobmanager import __BlobManager__
from helpers.textanalyticsmanager import __TextAnalyticsManager__
from helpers.searchmanager import __SearchManager__
from shared.shared import __File__, __Section__, __FunctionResponse__
from helpers.configmapper import __ConfigMapper__
from helpers.secretmanager import __SecretsHandler__
from common.textsplitter import __TextSplitter__
from common.embeddings import __AzureOpenAIEmbeddingService__


# This class is the orchestrating all the operations related to knowledge-base building
# It controls all operations from get Content, Get Emeddings , Create index, PII data filteration
# This will be called directly from function API (Az-function main method)
class __Orchestrator__:
    def __init__(
        self,
        **kwargs,
    ):
        self.container_path = kwargs.get("container_path")
        container_path = self.container_path
        # spliting file path into container and blob path
        self.container_name, self.file_blob_path = container_path.split("/", 1)
        # Extract file extension from the container path
        _, self.file_extension = os.path.splitext(container_path)
        # Define a list of known file extensions
        self.known_extensions = [".txt", ".json"]  # Add more file extensions as needed

        # Get secrets from Azure Key Vault & account key
        secrets_handler = __SecretsHandler__()
        (
            self.forms_recognizer_service,
            self.storage_account_base,
            self.sql_server_name,
            self.sql_db_name,
            self.open_ai_service,
            self.app_inst_key,
            self.search_service,
            self.index_name,
            self.lang_endPoint_secret,
        ) = secrets_handler.get_secrets()
        self._credential = DefaultAzureCredential()
        self._blob_manager = __BlobManager__()
        self._documentanalysismanager = __DocumentAnalysisManager__()
        # Database manager object
        self.__sql_connector = __DbOperationsManager__(
            self.sql_server_name, self.sql_db_name
        )
        # Extract Config data from Config table for Embeddings
        self.__config = self.__sql_connector.extract_configuration()
        # Extract values from matching dictionaries
        # Initialize ConfigMapper with the __config list
        self.config_mapper = __ConfigMapper__(self.__config)

        self.embeddings = __AzureOpenAIEmbeddingService__(
            open_ai_service=self.open_ai_service,
            credential=self._credential,
            config_mapper=self.config_mapper,
        )
        self.text_splitter = __TextSplitter__(config_mapper=self.config_mapper)
        self.search_manager = __SearchManager__(
            _searchservice=self.search_service,
            _index_name=self.index_name,
            _credential=self._credential,
            config_mapper=self.config_mapper,
        )
        # Use the track_event() api to send custom event telemetry
        # Takes event name and custom dimensions
        self.telemetryclient = TelemetryClient(self.app_inst_key)

    # Mask and identify PII data using language service and update content table with redacted content
    def _pii_recognition(self, container_path):
        try:

            container_path = self.container_path
            column_list = "content.ID,content.DocumentId,content.Content"
            # Get content for the given container_path document
            self.telemetryclient.track_trace(
                f"Get the content from Content table for {container_path}",
                severity=logging.INFO,
            )
            _content = self.__sql_connector.extract_FromContent(
                container_path, column_list
            )

            # get language from config table
            self.telemetryclient.track_trace(
                f"Get the language from Configuration table",
                severity=logging.INFO,
            )
            result = self.__sql_connector.extract_configuration()
            for _result in result:
                if _result["Name"] == "RedactPII.language":
                    language = '"' + _result["Value"] + '"'
            for row in _content:
                ID = row[0]
                DocumentId = row[1]
                Content = row[2]
                if Content in ["", None]:
                    self.telemetryclient.track_trace(
                        f" Document at {container_path} is a empty/blank file.",
                        severity=logging.INFO,
                    )
                else:
                    # TextAnalytics Manager object
                    self._text_analytics_client = __TextAnalyticsManager__()

                    text_analytics_client = (
                        self._text_analytics_client.authenticate_client(
                            self.lang_endPoint_secret, self._credential
                        )
                    )
                    RedactedContent = self._text_analytics_client.pii_recognition(
                        text_analytics_client, Content, language
                    )
                    self.telemetryclient.track_trace(
                        f" Document at {container_path} is a redacted successfully. Going to update SQL table next.",
                        severity=logging.INFO,
                    )
                    _response = self.__sql_connector.update_content_db(
                        DocumentId, RedactedContent, ID
                    )
                    if _response:
                        self.telemetryclient.track_trace(
                            f"Document has been successfully redacted for {container_path} and updated in Content table.",
                            severity=logging.INFO,
                        )
                        self.telemetryclient.flush()
                    else:
                        raise Exception(
                            f" Extracted content is not redacted for {container_path} and ID {row['ID']} "
                        )
            return True

        except Exception as e:
            self.telemetryclient.track_exception(str(e))
            return False
        finally:
            self.telemetryclient.flush()

    def _get_content(
        self,
        container_path,
    ):
        try:
            container_path = self.container_path
            self.telemetryclient.track_trace(
                f"Get the blob contents using Blob manager for {container_path}",
                severity=logging.INFO,
            )

            blob_content = self._blob_manager.get_Blob_Content(
                self.file_blob_path,
                self.storage_account_base,
                self._credential,
                self.container_name,
            )

            # Track an event

            if len(blob_content) > 0:
                if self.file_extension.lower() not in self.known_extensions:

                    self.telemetryclient.track_trace(
                        f"Get the contents using Document Inteligent manager for {container_path}",
                        severity=logging.INFO,
                    )
                    __results = self._documentanalysismanager.parseDocument(
                        blob_content, self.forms_recognizer_service, self._credential
                    )

                else:
                    __results = blob_content.decode("utf-8")

            if len(__results) > 0:
                self.telemetryclient.track_trace(
                    f"Match the container path with Document folder against Destination Column {container_path}",
                    severity=logging.INFO,
                )
                __document_id = self.__sql_connector.extract_document_id(container_path)

                # Placeholder for storing URL in SQL Server
                self.telemetryclient.track_trace(
                    f"Inserting the extracted content in Content table against {container_path} and Document ID {__document_id}",
                    severity=logging.INFO,
                )
                __response = self.__sql_connector.save_content_db(
                    __document_id, __results
                )
                if __response:
                    self.telemetryclient.track_trace(
                        f"Document has been successfully processed {container_path} and Document ID {__document_id}",
                        severity=logging.INFO,
                    )
                    return True
                else:
                    raise Exception(
                        f"Extracted content is not saved for {container_path} and Document ID {__document_id}, it could be due to no content available in the file"
                    )
            else:
                raise Exception(
                    f"No content extracted from the provided document {container_path} and Document ID {__document_id}"
                )
        except Exception as e:
            self.telemetryclient.track_exception(str(e))
            return False
        finally:
            self.telemetryclient.flush()

    # Process Documents (Blob Path) by calling ADLS location, use Document Inteligence service based on file type
    # Match path with SQL Document Table & store the content in Content Table store
    def process_documents(self):
        container_path = self.container_path
        _response = self._get_content(
            container_path=container_path,
        )
        return _response

    # This method is responsible for extracting emeddings vectors from Azure Open AI based on comtent save against cotainer path
    def _get_embeddings(self):
        try:
            _file_path = self.container_path
            self.telemetryclient.track_trace(
                f"Get contents for {_file_path} from data base content table",
                severity=logging.INFO,
            )
            _content = self.__sql_connector.extract_content(
                container_path=_file_path,
            )
            sections = [
                __Section__(
                    split_page, content=_content, category=self.config_mapper.category
                )
                for split_page in self.text_splitter.split_pages(_content)
            ]
            self.telemetryclient.track_trace(
                f"Split the document {_file_path} into sections to get embeddings",
                severity=logging.INFO,
            )

            section_batches = [
                sections[i : i + int(self.config_mapper.max_batch_size)]
                for i in range(0, len(sections), int(self.config_mapper.max_batch_size))
            ]
            documents = None
            for batch_index, batch in enumerate(section_batches):
                documents = [
                    {
                        "id": f"{section.split_page.page_num}",
                        "content": section.split_page.text,
                        "category": section.category,
                        "pagesource": f"{os.path.basename(self.container_path)}-page-{section.split_page.page_num}",
                        "sourcefile": self.container_path,
                    }
                    for section_index, section in enumerate(batch)
                ]
                embeddings = self.embeddings.create_embeddings(
                    texts=[section.split_page.text for section in batch]
                )
                for i, document in enumerate(documents):
                    document["embedding"] = embeddings[i]

            __response = self.__sql_connector.save_embeddings_db(
                container_path=_file_path, content=documents
            )
            if __response:
                self.telemetryclient.track_trace(
                    f"Got embeddings for {_file_path}", severity=logging.INFO
                )
                return __FunctionResponse__._return_http_response(
                    "Embeddings generated Successfully", status_code=200
                )
            else:
                raise Exception(f"Embeddings not genereated")

        except Exception as e:
            self.telemetryclient.track_exception(str(e))
            return __FunctionResponse__._return_http_response("Embeddings not genereated", status_code=400)
        finally:
            self.telemetryclient.flush()

    # This method is used to create index in AI search. It will extract the content and Document ID based on container path
    def index_documents(
        self,
    ):
        try:
            container_path = self.container_path
            self.telemetryclient.track_trace(
                f"Get emeddings for {container_path} from data base embedding table",
                severity=logging.INFO,
            )
            _documents = self.__sql_connector.extract_emeddings(
                container_path, self.config_mapper.category
            )
            self.telemetryclient.track_trace(
                f"Start the search manager for {container_path}",
                severity=logging.INFO,
            )
            __response = False
            if (len(_documents)) > 0:
                __response = self.search_manager.add(documents=_documents)

            if __response:
                self.telemetryclient.track_trace(
                    f"Indexed the document {container_path}",
                    severity=logging.INFO,
                )
                return __FunctionResponse__._return_http_response(
                    "Indexes created Successfully", status_code=200
                )
            else:
                raise Exception(f"Indexes not created")

        except Exception as e:
            self.telemetryclient.track_exception(str(e))
            return __FunctionResponse__._return_http_response("Indexes not created", status_code=400)
        finally:
            self.telemetryclient.flush()

# This method is used to remove content from Azure AI search index based on container path
    def _remove_index_content(
        self,
    ):
        try:
            container_path = self.container_path
            self.telemetryclient.track_trace(
                f"Remove the content from Azure Search index for {container_path}",
                severity=logging.INFO,
            )
            __response = self.search_manager._remove_content(container_path)
            if __response:
                self.telemetryclient.track_trace(
                    f"Removed the content from Azure Search index for {container_path}",
                    severity=logging.INFO,
                )
                return __FunctionResponse__._return_http_response(
                    "Content removed from index Successfully", status_code=200
                )
            else:
                raise Exception(f"Content not found in Azure Search index for {container_path}")

        except Exception as e:
            self.telemetryclient.track_exception(str(e))
            return __FunctionResponse__._return_http_response("Content not found in Azure Search index", status_code=400)
        finally:
            self.telemetryclient.flush()
