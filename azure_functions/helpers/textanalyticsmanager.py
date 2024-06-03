from azure.ai.textanalytics import TextAnalyticsClient
from shared.shared import __Page__
from helpers.sqlmanager import __DbOperationsManager__


class __TextAnalyticsManager__:

    # Return TextAnalyticsClient object
    def authenticate_client(self, lang_endPoint_secret, credentials):
        return TextAnalyticsClient(
            endpoint=lang_endPoint_secret, credential=credentials
        )

    # use inbuilt method to identify and mask PII content
    def pii_recognition(self, client, content, lang):
        if not content and not lang:
            raise Exception(f"Please provide valid inputs for language and content.")
        else:
            documents = [content]
            response = client.recognize_pii_entities(documents, language="en")
            result = [doc for doc in response if not doc.is_error]
            for doc in result:
                RedactedContent = doc.redacted_text
            return RedactedContent
