import os
import logging
import azure.functions as func
from datetime import datetime
from shared.shared import __FunctionResponse__
from shared.shared import __ContainerPath__
import json


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


# Heartbeat service to check Azure Function health and build number
@app.route(route="heartbeat", methods=["GET"])
def heartbeat(req: func.HttpRequest) -> func.HttpResponse:

    _build_id = os.environ["BUILD_ID"]
    if _build_id is None:
        _build_id = "Local Build"
    logging.info(
        f"Build id {_build_id}: Heartbeat request recieved @ {datetime.utcnow()}. Time is in UTC."
    )
    return func.HttpResponse(
        f"Build id {_build_id}: Function is alive @ {datetime.utcnow()}. Time is in UTC",
        status_code=200,
    )


# Extract Content from the provided document in container Path
@app.route(route="getContent", methods=["GET", "POST"])
def getContent(req: func.HttpRequest) -> func.HttpResponse:
    # Set global TracerProvider before instrumenting
    container_path = __ContainerPath__(req).get_container_path()
    if container_path:
        logging.info(f"Container Path: {container_path}")
        try:
            from helpers.orchestrator import __Orchestrator__

            _orchestrator = __Orchestrator__(
                container_path=container_path,
            )
            _response = _orchestrator.process_documents()
            if _response:
                return __FunctionResponse__._return_http_response(
                    "Document has been successfully processed", status_code=200
                )
            else:
                return __FunctionResponse__._return_http_response(
                    "Document has not been processed", status_code=404
                )
        except Exception as e:
            logging.error("Failed to get content", exc_info=e)
            return __FunctionResponse__._return_http_response("Document has not been processed", status_code=404)
    else:
        return __FunctionResponse__._return_http_response(
            "No document found for the provided input field.", status_code=404
        )


# Extract Emeddings from the provided document in container Path
@app.route(
    route="getEmbeddings", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"]
)
def getEmbeddings(req: func.HttpRequest) -> func.HttpResponse:

    container_path = __ContainerPath__(req).get_container_path()
    if container_path:
        logging.info(f"Container Path: {container_path}")
        try:
            from helpers.orchestrator import __Orchestrator__

            _orchestrator = __Orchestrator__(
                container_path=container_path,
            )
            _orchestrator._get_embeddings()
            return __FunctionResponse__._return_http_response(
                "Document has been successfully processed", status_code=200
            )
        except Exception as e:
            logging.error("Failed to get embeddings", exc_info=e)
            return __FunctionResponse__._return_http_response("Document has not been processed", status_code=404)
    else:
        return __FunctionResponse__._return_http_response(
            "No document found for the provided input field.", status_code=404
        )


# Identify and mask PII content
@app.route(route="redactPII", methods=["GET", "POST"])
def redactPII(req: func.HttpRequest) -> func.HttpResponse:
    # Set global TracerProvider before instrumenting
    container_path = __ContainerPath__(req).get_container_path()
    if container_path:
        logging.info(f"Container Path: {container_path}")
        try:
            from helpers.orchestrator import __Orchestrator__

            _orchestrator = __Orchestrator__(
                container_path=container_path,
            )
            _response = _orchestrator._pii_recognition(container_path)
            if _response:
                return __FunctionResponse__._return_http_response(
                    "Document has been successfully masked", status_code=200
                )
            else:
                return __FunctionResponse__._return_http_response(
                    "Document has not been masked", status_code=404
                )
        except Exception as e:
            logging.error("Failed to get redacted content", exc_info=e)
            return __FunctionResponse__._return_http_response("Document has not been processed", status_code=404)
    else:
        return __FunctionResponse__._return_http_response(
            "No document found for the provided input field.", status_code=404
        )


# Create indexes from the provided document in container Path
@app.route(
    route="createIndexes", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"]
)
def createIndexes(req: func.HttpRequest) -> func.HttpResponse:
    container_path = __ContainerPath__(req).get_container_path()
    if container_path:
        logging.info(f"Container Path: {container_path}")
        try:
            from helpers.orchestrator import __Orchestrator__

            _orchestrator = __Orchestrator__(
                container_path=container_path,
            )
            _orchestrator.index_documents()
            return __FunctionResponse__._return_http_response(
                "Document has been successfully processed", status_code=200
            )
        except Exception as e:
            logging.error("Failed to create indexes", exc_info=e)
            return __FunctionResponse__._return_http_response("Document has not been processed", status_code=404)
    else:
        return __FunctionResponse__._return_http_response(
            "Document has not been processed, input containerFilePath is missing", status_code=404
        )

# Remove documents from Knowledgebase indexes
@app.route(
    route="removeContent", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"]
)
def removeContent(req: func.HttpRequest) -> func.HttpResponse:
    container_path = __ContainerPath__(req).get_container_path()
    if container_path:
        logging.info(f"Container Path: {container_path}")
        try:
            from helpers.orchestrator import __Orchestrator__

            _orchestrator = __Orchestrator__(
                container_path=container_path,
            )
            _response = _orchestrator._remove_index_content()
            _response_message = json.loads(_response.get_body().decode('utf8'))
            if _response_message['Code'] == 200:
                return  __FunctionResponse__._return_http_response(
                    "Document has been successfully removed from index", status_code=200
                )
            else:
                return __FunctionResponse__._return_http_response(
                    "Document not found in Azure Search index", status_code=404
                    )
        except Exception as e:
            logging.error("Failed to remove the document", exc_info=e)
            return  __FunctionResponse__._return_http_response("Failed to remove the document", status_code=404)
    else:
        return  __FunctionResponse__._return_http_response(
            "Document has not been processed, input containerFilePath is missing", status_code=404
        )
