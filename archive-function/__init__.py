
import gzip, json
from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobClient

def main(mytimer):
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    db = client.get_database_client("billing")
    container = db.get_container_client("records")
    cutoff = datetime.utcnow() - timedelta(days=90)
    
    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff.isoformat()}'"

    for record in container.query_items(query=query, enable_cross_partition_query=True):
        blob_name = f"archive/{record['id']}.json.gz"
        blob = BlobClient.from_connection_string(BLOB_CONN, container_name="billing-archive", blob_name=blob_name)
        blob.upload_blob(gzip.compress(json.dumps(record).encode()))
        container.delete_item(record['id'], partition_key=record['partitionKey'])
