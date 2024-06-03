from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswParameters,
    HnswVectorSearchAlgorithmConfiguration,
    PrioritizedFields,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticSettings,
    SimpleField,
    VectorSearch,
    VectorSearchAlgorithmKind,
    VectorSearchProfile,
)
from helpers.configmapper import __ConfigMapper__


class __SearchInfo__:
    """
    Class representing a connection to a search service
    To learn more, please visit https://learn.microsoft.com/azure/search/search-what-is-azure-search
    """

    def __init__(
        self,
        endpoint: str,
        credential,
        index_name: str,
        verbose: bool = False,
    ):
        self.endpoint = endpoint
        self.credential = credential
        self.index_name = index_name
        self.verbose = verbose

    def create_search_client(self) -> SearchClient:
        return SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=self.credential,
        )

    def create_search_index_client(self) -> SearchIndexClient:
        return SearchIndexClient(
            endpoint=self.endpoint,
            credential=self.credential,
        )


class __SearchManager__:
    """
    Class to manage a search service. It can create indexes, and update or remove sections stored in these indexes
    To learn more, please visit https://learn.microsoft.com/azure/search/search-what-is-azure-search
    """

    def __init__(
        self, _searchservice, _index_name, _credential, config_mapper: __ConfigMapper__
    ):

        self.search_info = __SearchInfo__(
            endpoint=f"https://{_searchservice}.search.windows.net/",
            credential=_credential,
            index_name=_index_name,
            verbose=config_mapper.verbose,
        )

        self.search_analyzer_name = config_mapper.search_analyzer_name
        self.use_acls = config_mapper.use_acls
        self.search_images = config_mapper.search_images
        self.algorithm = (config_mapper.algorithm,)
        self.embedding_config = (config_mapper.embedding_config,)
        self.simple_field = (config_mapper.simple_field,)
        self.searchable_field = (config_mapper.searchable_field,)
        self.search_field = (config_mapper.search_field,)
        self.simple_field2 = (config_mapper.simple_field2,)
        self.simple_field3 = (config_mapper.simple_field3,)
        self.simple_field4 = (config_mapper.simple_field4,)
        self.simple_field5 = (config_mapper.simple_field5,)
        self.simple_field6 = (config_mapper.simple_field6,)
        self.simple_field7 = (config_mapper.simple_field7,)
        self.search_field2 = (config_mapper.search_field2,)
        self.metric = (config_mapper.metric,)
        self.field_type = (config_mapper.field_type,)
        self.vector_search_dimensions = (config_mapper.vector_search_dimensions,)
        self.vector_search_dimensions2 = config_mapper.vector_search_dimensions2

    def _create_index(self):
        with self.search_info.create_search_index_client() as search_index_client:
            fields = [
                SimpleField(name=self.simple_field, type=self.field_type, key=True),
                SearchableField(
                    name=self.searchable_field,
                    type=self.field_type,
                    analyzer_name=self.search_analyzer_name,
                ),
                SearchField(
                    name=self.search_field,
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    hidden=False,
                    searchable=True,
                    filterable=False,
                    sortable=False,
                    facetable=False,
                    vector_search_dimensions=self.vector_search_dimensions,
                    vector_search_profile=self.embedding_config,
                ),
                SimpleField(
                    name=self.simple_field2,
                    type=self.field_type,
                    filterable=True,
                    facetable=True,
                ),
                SimpleField(
                    name=self.simple_field3,
                    type=self.field_type,
                    filterable=True,
                    facetable=True,
                ),
                SimpleField(
                    name=self.simple_field4,
                    type=self.field_type,
                    filterable=True,
                    facetable=True,
                ),
                SimpleField(
                    name=self.simple_field7,
                    type=self.field_type,
                    filterable=True,
                    facetable=True,
                ),
            ]
            if self.use_acls:
                fields.append(
                    SimpleField(
                        name=self.simple_field5,
                        type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                        filterable=True,
                    )
                )
                fields.append(
                    SimpleField(
                        name=self.simple_field6,
                        type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                        filterable=True,
                    )
                )
            if self.search_images:
                fields.append(
                    SearchField(
                        name=self.search_field2,
                        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        hidden=False,
                        searchable=True,
                        filterable=False,
                        sortable=False,
                        facetable=False,
                        vector_search_dimensions=self.vector_search_dimensions2,
                        vector_search_profile=self.embedding_config,
                    ),
                )

            index = SearchIndex(
                name=self.search_info.index_name,
                fields=fields,
                semantic_settings=SemanticSettings(
                    configurations=[
                        SemanticConfiguration(
                            name="default",
                            prioritized_fields=PrioritizedFields(
                                title_field=None,
                                prioritized_content_fields=[
                                    SemanticField(field_name=self.searchable_field)
                                ],
                            ),
                        )
                    ]
                ),
                vector_search=VectorSearch(
                    algorithms=[
                        HnswVectorSearchAlgorithmConfiguration(
                            name=self.algorithm,
                            kind=VectorSearchAlgorithmKind.HNSW,
                            parameters=HnswParameters(metric=self.metric),
                        )
                    ],
                    profiles=[
                        VectorSearchProfile(
                            name=self.embedding_config,
                            algorithm=self.algorithm,
                        ),
                    ],
                ),
            )
            if self.search_info.index_name not in [
                name for name in search_index_client.list_index_names()
            ]:
                if self.search_info.verbose:
                    search_index_client.create_index(index)

    def _update_content(
        self,
        documents,
    ):
        with self.search_info.create_search_client() as search_client:
            search_client.upload_documents(documents)
            return True

    def add(
        self,
        documents,
    ):
        __response = False
        self._create_index()
        __response = self._update_content(
            documents,
        )
        return __response
    

    def _remove_content(self, sourcefile):
        with self.search_info.create_search_client() as search_client:
            _filter = None
            if sourcefile is not None:
                _filter = f"sourcefile eq '{sourcefile}'"

            _search_documents = search_client.search(search_text="", filter=_filter,include_total_count=True)

            if _search_documents.get_count() > 0:
                _documents_to_remove = []
                for document in _search_documents:
                    _documents_to_remove.append({"id":document['id']})

                _removed_docs  = search_client.delete_documents(_documents_to_remove)
                return len(_removed_docs)
            else:
                return 0
