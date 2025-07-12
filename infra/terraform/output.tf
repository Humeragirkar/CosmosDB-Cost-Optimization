output "storage_account_name" {
  value = azurerm_storage_account.blob.name
}

output "cosmosdb_account_endpoint" {
  value = azurerm_cosmosdb_account.cosmos.endpoint
}
