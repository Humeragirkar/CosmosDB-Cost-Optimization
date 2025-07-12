locals {
  resource_group_name     = "${var.prefix}-rg"
  storage_account_name    = substr("${var.prefix}storage", 0, 24)  # Storage account name max length 24
  cosmos_account_name     = substr("${var.prefix}acct", 0, 44)     # Cosmos account name max length 44
  cosmos_db_name          = "billing-db"
  cosmos_container_name   = "records"
  blob_container_name     = "archived-records"
} 
