import azure.functions as func
import logging
import sys
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from helpers.orchestrator import Orchestrator


# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(
    logging.WARNING)


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
@app.route(route="getContent",methods=['GET'])
def getContent(req: func.HttpRequest) -> func.HttpResponse:
    # Set global TracerProvider before instrumenting      
    container_path = req.params.get('containerFilePath')   
    if not container_path:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            container_path = req_body.get('containerPath')

    if container_path:
      try:
        _orchestrator = Orchestrator(
        container_path=container_path,
        )
        _orchestrator.process_documents()
      except Exception as e:
        logging.error(str(e))
        return func.HttpResponse("Document has not been processed", status_code=404)
    else:      
        return func.HttpResponse("No document found for the provided input field.", status_code=404)
