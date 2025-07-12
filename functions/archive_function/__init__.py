import datetime
import json
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

def main(mytimer: func.TimerRequest) -> None:

    # Configuration (Ideally use environment variables or Azure Key Vault)
    COSMOS_ENDPOINT = "<your-cosmos-endpoint>"
    COSMOS_KEY = "<your-cosmos-key>"
    DATABASE_NAME = "billing-db"
    CONTAINER_NAME = "records"

    BLOB_CONNECTION_STRING = "<your-blob-connection-string>"
    BLOB_CONTAINER_NAME = "archived-records"

    # Initialize Cosmos DB Client
    cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    container = cosmos_client.get_database_client(DATABASE_NAME).get_container_client(CONTAINER_NAME)

    # Initialize Blob Storage Client
    blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    blob_container = blob_service.get_container_client(BLOB_CONTAINER_NAME)

    # Calculate cutoff date (90 days ago)
    cutoff_date = (datetime.datetime.utcnow() - datetime.timedelta(days=90)).isoformat()

    # Query records older than cutoff
    query = "SELECT * FROM c WHERE c.timestamp < @cutoff"
    parameters = [{"name": "@cutoff", "value": cutoff_date}]
    archived_records = container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True)

    # Archive records to Blob Storage
    for record in archived_records:
        record_id = record.get("id")
        partition_key = record.get("partitionKey")
        blob_name = f"{record_id}.json"

        try:
            # Upload to blob
            blob_container.upload_blob(name=blob_name, data=json.dumps(record), overwrite=True)

            # Delete from Cosmos DB
            container.delete_item(item=record_id, partition_key=partition_key)

        except Exception as e:
            print(f"Error archiving record {record_id}: {str(e)}")
