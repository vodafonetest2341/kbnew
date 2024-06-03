import logging
from azure.identity import DefaultAzureCredential
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


class __SearchManager__:
    def __init__(
        self,
        endpoint: str,
        index_name: str,
    ):
        self.endpoint = endpoint
        self.index_name = index_name
        self.search_analyzer_name = None
        self.use_acls = False
        self.search_images = False

    def create_search_index_client(self) -> SearchIndexClient:
        _credential = DefaultAzureCredential()
        return SearchIndexClient(
            endpoint=self.endpoint,
            credential=_credential,
        )

    def create_index(self):
        with self.create_search_index_client() as search_index_client:
            fields = [
                SimpleField(name="id", type="Edm.String", key=True),
                SearchableField(
                    name="content",
                    type="Edm.String",
                    analyzer_name=self.search_analyzer_name,
                ),
                SearchField(
                    name="embedding",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    hidden=False,
                    searchable=True,
                    filterable=False,
                    sortable=False,
                    facetable=False,
                    vector_search_dimensions=1536,
                    vector_search_profile="embedding_config",
                ),
                SimpleField(
                    name="category", type="Edm.String", filterable=True, facetable=True
                ),
                SimpleField(
                    name="sourcepage",
                    type="Edm.String",
                    filterable=True,
                    facetable=True,
                ),
                SimpleField(
                    name="sourcefile",
                    type="Edm.String",
                    filterable=True,
                    facetable=True,
                ),
            ]
            if self.use_acls:
                fields.append(
                    SimpleField(
                        name="oids",
                        type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                        filterable=True,
                    )
                )
                fields.append(
                    SimpleField(
                        name="groups",
                        type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                        filterable=True,
                    )
                )
            if self.search_images:
                fields.append(
                    SearchField(
                        name="imageEmbedding",
                        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        hidden=False,
                        searchable=True,
                        filterable=False,
                        sortable=False,
                        facetable=False,
                        vector_search_dimensions=1024,
                        vector_search_profile="embedding_config",
                    ),
                )

            index = SearchIndex(
                name=self.index_name,
                fields=fields,
                semantic_settings=SemanticSettings(
                    configurations=[
                        SemanticConfiguration(
                            name="default",
                            prioritized_fields=PrioritizedFields(
                                title_field=None,
                                prioritized_content_fields=[
                                    SemanticField(field_name="content")
                                ],
                            ),
                        )
                    ]
                ),
                vector_search=VectorSearch(
                    algorithms=[
                        HnswVectorSearchAlgorithmConfiguration(
                            name="hnsw_config",
                            kind=VectorSearchAlgorithmKind.HNSW,
                            parameters=HnswParameters(metric="cosine"),
                        )
                    ],
                    profiles=[
                        VectorSearchProfile(
                            name="embedding_config",
                            algorithm="hnsw_config",
                        ),
                    ],
                ),
            )
            _index = None
            if self.index_name not in [
                name for name in search_index_client.list_index_names()
            ]:
                logging.debug(f"Creating {self.index_name} search index")
                _index = search_index_client.create_index(index)
            else:
                logging.debug(f"Search index {self.index_name} already exists")
                _index = search_index_client.get_index(self.index_name)
        return _index
