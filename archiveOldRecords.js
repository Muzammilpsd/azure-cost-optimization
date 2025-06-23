// Pseudocode for archiving old records
function archiveOldRecords() {
  const oldRecords = cosmos.query("SELECT * FROM c WHERE c.timestamp < DATE_SUB(NOW(), INTERVAL 3 MONTH)");
  for (let record of oldRecords) {
    const blobPath = `billing-records/${record.customerId}/${record.year}-${record.month}/${record.id}.json`;
    blobStorage.upload(blobPath, JSON.stringify(record));
    cosmos.delete(record.id);
  }
}