output "storage_account_name" {
  value = azurerm_storage_account.main.name
}

output "docs_container_name" {
  value = azurerm_storage_container.docs.name
}

output "storage_account_id" {
  value = azurerm_storage_account.main.id
}