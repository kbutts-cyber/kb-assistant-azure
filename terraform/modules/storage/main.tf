resource "azurerm_storage_account" "main" {
  name                     = "kbstorage${var.suffix}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  allow_nested_items_to_be_public = false
  min_tls_version                 = "TLS1_2"
  https_traffic_only_enabled              = true
}

resource "azurerm_storage_container" "docs" {
  name                  = "docs"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}