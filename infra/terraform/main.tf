resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "blob" {
  name                     = "costoptstorage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "archive" {
  name                  = "archived-records"
  storage_account_name  = azurerm_storage_account.blob.name
  container_access_type = "private"
}

resource "azurerm_cosmosdb_account" "cosmos" {
  name                = "cosmosoptacct"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level       = "Session"
  }

  geo_location {
    location          = var.location
    failover_priority = 0
  }
}
