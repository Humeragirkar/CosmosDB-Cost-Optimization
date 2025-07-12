import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    Azure HTTP Trigger Function to read a billing record from Cosmos DB.
    If the record is not found (cold data), it falls back to Azure Blob Storage.

    logging.info("Read Proxy Function triggered")

    # Parse query parameters
    record_id = req.params.get('id')
    if not record_id:
        return func.HttpResponse("Missing 'id' query parameter", status_code=400)

    # Configuration (Use env vars or Key Vault in production)
    COSMOS_ENDPOINT = "<your-cosmos-endpoint>"
    COSMOS_KEY = "<your-cosmos-key>"
    DATABASE_NAME = "billing-db"
    CONTAINER_NAME = "records"

    BLOB_CONNECTION_STRING = "<your-blob-connection-string>"
    BLOB_CONTAINER_NAME = "archived-records"

    try:
        # Initialize Cosmos DB Client
        cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
        container = cosmos_client.get_database_client(DATABASE_NAME).get_container_client(CONTAINER_NAME)

        # Try to read from Cosmos DB
        item = container.read_item(item=record_id, partition_key=record_id)
        logging.info(f"✅ Found record in Cosmos DB: {record_id}")
        return func.HttpResponse(json.dumps(item), status_code=200, mimetype="application/json")

    except exceptions.CosmosResourceNotFoundError:
        logging.warning(f"📦 Record not found in Cosmos DB. Falling back to Blob: {record_id}")

        try:
            # Initialize Blob Client
            blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
            blob_container = blob_service.get_container_client(BLOB_CONTAINER_NAME)
            blob_client = blob_container.get_blob_client(f"{record_id}.json")

            blob_data = blob_client.download_blob().readall()
            return func.HttpResponse(blob_data, status_code=200, mimetype="application/json")

        except Exception as blob_err:
            logging.error(f"❌ Record not found in Blob or error reading blob: {blob_err}")
            return func.HttpResponse("Record not found in Cosmos DB or Blob Storage", status_code=404)

    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
