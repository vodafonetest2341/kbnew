import os
import re
import base64
import json
import azure.functions as func
from typing import IO, Optional, List


class __File__:
    """
    Represents a file stored either locally or in a data lake storage account
    This file might contain access control information about which users or groups can access it
    """

    def __init__(
        self,
        content: IO,
        acls: Optional[dict[str, list]] = None,
    ):
        self.content = content
        self.acls = acls or {}

    def filename(self):
        return os.path.basename(self.content.name)

    def filename_to_id(self):
        filename_ascii = re.sub("[^0-9a-zA-Z_-]", "_", self.filename())
        filename_hash = base64.b16encode(self.filename().encode("utf-8")).decode(
            "ascii"
        )
        return f"file-{filename_ascii}-{filename_hash}"

    def close(self):
        if self.content:
            self.content.close()


class __SplitPage__:
    """
    A section of a page that has been split into a smaller chunk.
    """

    def __init__(
        self,
        page_num: int,
        text: str,
    ):
        self.page_num = page_num
        self.text = text


class __Section__:
    """
    A section of a page that is stored in a search service. These sections are used as context by Azure OpenAI service
    """

    def __init__(
        self,
        split_page: __SplitPage__,
        content: __File__,
        category: Optional[str] = None,
    ):
        self.split_page = split_page
        self.content = content
        self.category = category


class __Page__:
    """
    A single page from a pdf

    Attributes:
        page_num (int): Page number
        offset (int): If the text of the entire PDF was concatenated into a single string, the index of the first character on the page. For example, if page 1 had the text "hello" and page 2 had the text "world", the offset of page 2 is 5 ("hellow")
        text (str): The text of the page
    """

    def __init__(
        self,
        page_num: int,
        offset: int,
        text: str,
    ):
        self.page_num = page_num
        self.offset = offset
        self.text = text


class __EmbeddingBatch__:
    """
    Represents a batch of text that is going to be embedded
    """

    def __init__(
        self,
        texts: List[str],
        token_length: int,
    ):
        self.texts = texts
        self.token_length = token_length


class __FunctionResponse__:
    """
    Represents a function response with JSON
    """

    def _return_http_response(
        message,
        status_code,
    ):
        return func.HttpResponse(
            json.dumps(
                {
                    "Code": status_code,
                    "Message": message,
                }
            ),
            status_code=status_code,
            headers={"Content-Type": "application/json"},
        )

class __ContainerPath__:
    """
    Represents a container path
    """

    def __init__(
        self,
        req: func.HttpRequest,
    ):
        self.req = req

    def get_container_path(self):
        container_path = self.req.params.get("containerFilePath")
        if not container_path:
            try:
                req_body = self.req.get_json()
            except ValueError as e:
                return False
            else:
                container_path = req_body.get("containerFilePath")

        return container_path
