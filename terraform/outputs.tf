output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "container_app_url" {
  value = module.container_app.app_url
}

output "openai_endpoint" {
  value = module.openai.endpoint
}

output "key_vault_url" {
  value = module.keyvault.key_vault_url
}

output "acr_login_server" {
  value = module.container_app.acr_login_server
}