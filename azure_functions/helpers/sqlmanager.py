import json
from datetime import datetime
from common.sql import __SqlConnector__
from shared.shared import __FunctionResponse__


class __DbOperationsManager__:

    def __init__(self, _sql_server_name, _sql_db_name):
        _sql_connector = __SqlConnector__(
            sql_server=_sql_server_name,
            sql_database=_sql_db_name,
        )
        self.__sql_connector = _sql_connector

    # extract Document ID by comparing container path to destination folder in Document table
    def extract_document_id(self, container_path):
        # Placeholder for extracting document ID from container_path

        if not (container_path):
            return __FunctionResponse__._return_http_response("Please provide valid inputs", status_code=400)

        # Connect to Azure SQL Database using Managed Identity

        _connection = self.__sql_connector.get_sql_connection()
        _cursor = _connection.cursor()
        _cursor.execute(
            "SELECT Id FROM [knowledgebase].[Document] WHERE Destination = ?",
            container_path,
        )
        _row = _cursor.fetchone()
        if _row:
            document_id = _row[0]
            return document_id
        else:
            raise Exception(f"No document found for the provided input field")

    # Update RedactedContent from Content table for given ID and document_id
    def update_content_db(self, document_id, content, ID):
        # Placeholder for extracting document ID from container_path
        if not (document_id and content and ID):
            raise Exception(
                f" Kindly provide valid ID, Document ID: {document_id} and content"
            )
        else:

            # Connect to Azure SQL Database using Managed Identity
            _connection = self.__sql_connector.get_sql_connection()
            _cursor = _connection.cursor()
            _content = content.replace("'", "''")
            # Concatenate text from each page in _results
            _cursor.execute(
                f"""UPDATE [knowledgebase].[Content] SET RedactedContent = '{_content}' WHERE\
                DocumentId= {document_id} and  ID={ID}"""
            )
            _connection.commit()
            return True

    # store Content page wise by comparing container path to destination folder in Document table
    def save_content_db(self, document_id, content):
        # Placeholder for extracting document ID from container_path

        if not (document_id and content):
            raise Exception(f"Please provide valid inputs")
        # Get the current date and time
        _current_datetime = datetime.now()
        # Connect to Azure SQL Database using Managed Identity
        _connection = self.__sql_connector.get_sql_connection()
        _cursor = _connection.cursor()
        page_number = 1
        # Concatenate text from each page in _results
        if isinstance(content, str):
            _cursor.execute(
                "INSERT INTO [knowledgebase].[Content] (DocumentId,Content,RedactedContent,PageNO,CreatedAt) VALUES (?,?,?,?,?)",
                int(document_id),
                content,
                content,
                page_number,
                _current_datetime,
            )
        elif isinstance(content, list):
            if all(page.text == "" for page in content):
                return False
            for page in content:
                if page.text:
                    _cursor.execute(
                        "INSERT INTO [knowledgebase].[Content] (DocumentId,Content,RedactedContent,PageNO,CreatedAt) VALUES (?,?,?,?,?)",
                        int(document_id),
                        page.text,
                        page.text,
                        page_number,
                        _current_datetime,
                    )
                    page_number += 1
        _connection.commit()
        return True

    def extract_FromContent(self, container_path, column_list):
        # Placeholder for extracting document ID from container_path

        if not container_path or not column_list:
            return __FunctionResponse__._return_http_response("Please provide valid inputs", status_code=400)

        # Connect to Azure SQL Database using Managed Identity
        _connection = self.__sql_connector.get_sql_connection()
        _cursor = _connection.cursor()
        _cursor.execute(
            f"""SELECT {column_list} FROM [knowledgebase].[Document] document join [knowledgebase].[Content] as \
                content on content.DocumentId=document.ID \
                WHERE document.Destination = '{container_path}'"""
        )
        _rows = _cursor.fetchall()
        if _rows:
            return _rows
        else:
            return __FunctionResponse__._return_http_response(
                "No document found for the provided input field.", status_code=404
            )

    # extract Content by comparing container path to destination folder in Document table and then based on document ID, extract content
    def extract_content(self, container_path):
        # Placeholder for extracting document ID from container_path

        if not (container_path):
            return __FunctionResponse__._return_http_response("Please provide valid inputs", status_code=400)

        # Connect to Azure SQL Database using Managed Identity

        _connection = self.__sql_connector.get_sql_connection()
        _cursor = _connection.cursor()
        _cursor.execute(
            f"SELECT content.PageNo,content.RedactedContent FROM [knowledgebase].[Document] document join [knowledgebase].[Content] as content on content.DocumentId=document.ID  WHERE document.Destination = ?",
            container_path,
        )
        _rows = _cursor.fetchall()
        if _rows:
            return _rows
        else:
            return __FunctionResponse__._return_http_response(
                "No document found for the provided input field.", status_code=404
            )

    # extract Embeddings Configuration from [knowledgebase].[Config] table
    def extract_configuration(self):
        # Placeholder for extracting document ID from container_path
        # Connect to Azure SQL Database using Managed Identity
        # Initialize a flag to track whether a connection has been established
        connection_established = False

        # Check if a SQL connection exists
        if not connection_established:
            # If connection doesn't exist, create a new connection
            _connection = self.__sql_connector.get_sql_connection()
            _cursor = _connection.cursor()
            # Update the flag to indicate that a connection has been established
            connection_established = True
        else:
            # If connection already exists, reuse the existing connection
            _cursor = _connection.cursor()

        _cursor.execute(
            f"select * from knowledgebase.Config",
        )
        _rows = _cursor.fetchall()
        # Initialize a list to store the results
        _results_list = []
        if _rows:
            # Store rows in a list of dictionaries
            _results_list = [
                {"ID": row[0], "Name": row[1], "Value": row[2]} for row in _rows
            ]
            return _results_list
        else:
            return __FunctionResponse__._return_http_response(
                "No document found for the provided input field.", status_code=404
            )

    # Save Embeddings data by getting Content ID from Content table and getting Document ID from Document table
    def save_embeddings_db(self, container_path, content: list):
        # Placeholder for extracting document ID from container_path

        if not (container_path and content):
            return __FunctionResponse__._return_http_response("Please provide valid inputs", status_code=400)
        # Get the current date and time
        _current_datetime = datetime.now()
        # Connect to Azure SQL Database using Managed Identity
        _connection = self.__sql_connector.get_sql_connection()
        _cursor = _connection.cursor()

        # Concatenate text from each page in _results
        _cursor.execute(
            "SELECT content.ID, content.PageNo FROM [knowledgebase].[Document] document join [knowledgebase].[Content] as content on content.DocumentId=document.ID WHERE document.Destination = ?",
            container_path,
        )
        # Fetch all rows returned by the query
        _rows = _cursor.fetchall()
        for ID, PageNo in _rows:
            for document in content:
                if int(document["id"]) == PageNo:
                    _cursor.execute(
                        "INSERT INTO [knowledgebase].[Embeddings] (ContentId,ChunkedContent,PageSource,Vectors,CreatedAt) VALUES (?,?,?,?,?)",
                        int(ID),
                        document["content"],
                        document["pagesource"],
                        json.dumps(document["embedding"]).encode("utf-8"),
                        _current_datetime,
                    )
        _connection.commit()
        return True

    # extract Emeddings by comparing container path to destination folder in Document table and then based on document ID, extract content
    def extract_emeddings(self, container_path, category):
        # Placeholder for extracting document ID from container_path

        if not (container_path and category):
            return __FunctionResponse__._return_http_response("Please provide valid inputs", status_code=400)

        # Connect to Azure SQL Database using Managed Identity

        _connection = self.__sql_connector.get_sql_connection()
        _cursor = _connection.cursor()
        _cursor.execute(
            f"SELECT embeddings.ID, embeddings.ChunkedContent, embeddings.vectors, embeddings.PageSource, content.DocumentId FROM [knowledgebase].[Document] document join [knowledgebase].[Content] as content on content.DocumentId=document.ID join [knowledgebase].[Embeddings] as embeddings on embeddings.ContentId= content.ID WHERE document.Destination = ?",
            container_path,
        )
        _rows = _cursor.fetchall()
        documents = []
        if _rows:
            for row in _rows:
                document = {
                    "id": str(row[0]),
                    "content": row[1],
                    "embedding": json.loads(row[2].decode("utf-8")),
                    "category": category,
                    "sourcepage": row[3],
                    "sourcefile": container_path,
                    "documentId": str(row[4]),
                }
                documents.append(document)

        return documents
