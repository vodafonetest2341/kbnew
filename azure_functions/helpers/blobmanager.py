from azure.storage.blob import BlobServiceClient


class __BlobManager__:
    # class for handling all operations related to BLOB

    def get_Blob_Content(
        self, container_path, base_path, accountcredentials, container_url
    ):
        # to get the Blob content related to file path provided
        # Connect to Azure Data Lake Storage
        blob_service_client = BlobServiceClient(
            account_url=base_path, credential=accountcredentials
        )
        # Retrieve files from ADLS container
        # Read blob content
        try:
            # Get the blob client for the specified file
            blob_client = blob_service_client.get_blob_client(
                container=container_url, blob=container_path
            )
            blob_data = blob_client.download_blob()
            # Download the content of the file
            blob_content = blob_data.readall()
            return blob_content
        except Exception as e:
            self.telemetryclient.track_exception(str(e))
            return
