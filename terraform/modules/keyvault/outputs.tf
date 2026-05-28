output "key_vault_id" {
  value = azurerm_key_vault.main.id
}

output "key_vault_url" {
  value = azurerm_key_vault.main.vault_uri
}