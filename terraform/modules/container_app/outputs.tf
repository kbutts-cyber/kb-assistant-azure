output "app_url" {
  value = azurerm_container_app.main.latest_revision_fqdn
}

output "principal_id" {
  value = azurerm_container_app.main.identity[0].principal_id
}

output "acr_login_server" {
  value = azurerm_container_registry.main.login_server
}