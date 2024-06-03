class __ConfigMapper__:
    def __init__(self, config):
        self.config_mapping = {
            "Embeddings.max_batch_size": "max_batch_size",
            "Embeddings.has_image_embeddings": "has_image_embeddings",
            "Embeddings.verbose": "verbose",
            "Embeddings.sentence_endings": "sentence_endings",
            "Embeddings.word_breaks": "word_breaks",
            "Embeddings.max_section_length": "max_section_length",
            "Embeddings.sentence_search_limit": "sentence_search_limit",
            "Embeddings.section_overlap": "section_overlap",
            "Embeddings.openai_deployment": "openai_deployment",
            "Embeddings.openai_model": "openai_model",
            "Embeddings.batch_model": "batch_model",
            "Embeddings.open_ai_api_version": "open_ai_api_version",
            "Embeddings.disable_batch_vectors": "disable_batch_vectors",
            "Embeddings.category": "category",
            "Index.search_analyzer_name": "search_analyzer_name",
            "Index.use_acls": "use_acls",
            "Index.search_images": "search_images",
            "Index.verbose": "verbose",
            "Index.algorithm": "algorithm",
            "Index.config": "embedding_config",
            "Index.SimpleField": "simple_field",
            "Index.SearchableField": "searchable_field",
            "Index.SearchField": "search_field",
            "Index.SimpleField2": "simple_field2",
            "Index.SimpleField3": "simple_field3",
            "Index.SimpleField4": "simple_field4",
            "Index.SimpleField5": "simple_field5",
            "Index.SimpleField6": "simple_field6",
            "Index.SimpleField7": "simple_field7",
            "Index.SearchField2": "search_field2",
            "Index.metric": "metric",
            "Index.type": "field_type",
            "Index.vector_search_dimensions": "vector_search_dimensions",
            "Index.vector_search_dimensions2": "vector_search_dimensions2",
        }
        self.config = config
        self.initialize_attributes()

    def initialize_attributes(self):
        for result in self.config:
            attribute_name = self.config_mapping.get(result["Name"])
            if attribute_name:
                setattr(self, attribute_name, result["Value"])
