output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "storage_account_name" {
  description = "Storage account name"
  value       = azurerm_storage_account.blob.name
}

output "blob_container_name" {
  description = "Blob container name"
  value       = azurerm_storage_container.archive.name
}

output "cosmosdb_account_name" {
  description = "Cosmos DB account name"
  value       = azurerm_cosmosdb_account.cosmos.name
}

output "cosmosdb_account_endpoint" {
  description = "Cosmos DB endpoint URL"
  value       = azurerm_cosmosdb_account.cosmos.endpoint
}

output "cosmosdb_database_name" {
  description = "Cosmos DB SQL database name"
  value       = azurerm_cosmosdb_sql_database.billing_db.name
}

output "cosmosdb_container_name" {
  description = "Cosmos DB container name"
  value       = azurerm_cosmosdb_sql_container.billing_records_container.name
}
