Feature: Test the Managed Identity

  Scenario Outline: Key Vault access using Managed Identity
    Given the KeyVault
    When we get the secret <secret_name> using managed identity
    Then the secret returned is <secret_value>

    Examples:
      | secret_name | secret_value     |
      | unit-test   | unit-test-secret |


  Scenario Outline: Document Intelligence access using Managed Identity
    Given the Document Intelligence <document_intelligence_endpoint>
    When we call the begin analyze document method with a document <file_path> using managed identity
    Then we should get the results from the Document Intelligence service

    Examples:
      | document_intelligence_endpoint | file_path                      |
      | document-intelligence-endpoint | tests/data/Benefit_Options.pdf |

  Scenario Outline: AI Language access using Managed Identity
    Given the AI Language <ai_language_endpoint>
    When we call the recognize pii entites method with a text <sample_text> using managed identity
    Then we should get the results from the AI Language with redacted text <redacted_text>

    Examples:
      | ai_language_endpoint | sample_text                                            | redacted_text                                          |
      | ai-language-endpoint | My name is John Doe and my phone number is 0123456788. | My name is ******** and my phone number is **********. |


  Scenario Outline: SQL Database access using Managed Identity
    Given the SQL Server <sql_server> and SQL Database <sql_database>
    When we call the database with a query <sample_query> using managed identity
    Then we should get the results from the database with text <query_response>

    Examples:
      | sql_server      | sql_database      | sample_query | query_response |
      | sql-server-name | sql-database-name | SELECT 1     | 1              |



  Scenario Outline: Azure Open AI access using Managed Identity
    Given the Azure Open AI service <open_ai_endpoint>
    When we call create embeddings from deployment <open_ai_deployment> for model <open_ai_model_name> with api version <open_ai_api_version> with a text <sample_text> using managed identity
    Then we should get the vectors <vectors> from the Azure Open AI service

    Examples:
      | open_ai_endpoint | open_ai_deployment                | open_ai_model_name     | open_ai_api_version | sample_text             | vectors                              |
      | open-ai-endpoint | oai-aib-we-text-embedding-ada-002 | text-embedding-ada-002 | 2023-05-15          | Give me the embeddings? | -0.0327367,-0.0148594985,0.010777514 |


  Scenario Outline: Azure AI Search access using Managed Identity
    Given the Azure AI Search service <ai_search_endpoint>
    When we call create index method to create the index <index_name> using managed identity
    Then the index should be created

    Examples:
      | ai_search_endpoint | index_name |
      | ai-search-endpoint | rag_index  |

  Scenario Outline: Azure Storage Account access using Managed Identity
    Given the Azure Storage Account <storage_account_url> with container <container_name>
    When we call download method on the blob <blob_path>
    Then the downloaded file size is <size>

    Examples:
      | storage_account_url     | container_name | blob_path           | size   |
      | landing-storage-account | test           | Benefit_Options.pdf | 544811 |

  Scenario Outline: Test redactPII API
    Given the Azure Function App URL <function_app_url> with <end_point>
    When we call the redactPII API with a valid containerFilePath <container_file_path>
    Then we should receive a successful response

    Examples:
      | end_point                         | container_file_path             | function_app_url |
      | /api/redactPII?containerFilePath= | landing/sharepoint/PIITtest.pdf | function-app-url |

  Scenario Outline: Test redactPII API
    Given the Azure Function App URL <function_app_url> with <end_point>
    When we call the redactPII API with an invalid containerFilePath <container_file_path>
    Then we should receive a failure response

    Examples:
      | end_point                         | container_file_path | function_app_url |
      | /api/redactPII?containerFilePath= | invalid/file/path   | function-app-url |

  Scenario Outline: Test getContent API
    Given the Azure Function App URL <funtion_app_url> with <end_point>
    When we call the getContent API with a valid containerFilePath <container_file_path>
    Then we should receive a successful response

    Examples:
      | end_point                          | container_file_path         | funtion_app_url  |
      | /api/getContent?containerFilePath= | landing/sharepoint/Test.png | function-app-url |

  Scenario Outline: Test getEmbeddings API
    Given the Azure Function App URL <funtion_app_url> with <end_point>
    When we call the getEmbeddings API with a valid containerFilePath <container_file_path>
    Then we should receive a successful response

    Examples:
      | end_point                             | container_file_path         | funtion_app_url  |
      | /api/getEmbeddings?containerFilePath= | landing/sharepoint/Test.png | function-app-url |

  Scenario Outline: Test createIndexes API
    Given the Azure Function App URL <funtion_app_url> with <end_point>
    When we call the getEmbeddings API with a valid containerFilePath <container_file_path>
    Then we should receive a successful response

    Examples:
      | end_point                             | container_file_path         | funtion_app_url  |
      | /api/createIndexes?containerFilePath= | landing/sharepoint/Test.png | function-app-url |

  Scenario Outline: Test getContent API
    Given the Azure Function App URL <function_app_url> with <end_point>
    When we call the getContent API with an invalid containerFilePath <container_file_path>
    Then we should receive a failure response

    Examples:
      | end_point                         | container_file_path | function_app_url |
      | /api/getContent?containerFilePath= | invalid/file/path   | function-app-url |
