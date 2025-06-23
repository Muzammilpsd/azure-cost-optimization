import gzip, json
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobClient
from fastapi import HTTPException

def get_record(record_id):
    try:
        item = cosmos_container.read_item(item=record_id, partition_key=record_id)
        return item
    except Exception:
        blob_name = f"archive/{record_id}.json.gz"
        blob = BlobClient.from_connection_string(BLOB_CONN, container_name="billing-archive", blob_name=blob_name)
        if not blob.exists():
            raise HTTPException(status_code=404, detail="Record not found")
        blob_data = blob.download_blob().readall()
        return json.loads(gzip.decompress(blob_data))
