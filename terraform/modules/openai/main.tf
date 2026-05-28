resource "azurerm_cognitive_account" "main" {
  name                = "oai-kb-${var.suffix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "OpenAI"
  sku_name            = "S0"

  custom_subdomain_name = "oai-kb-${var.suffix}"
}