resource "azurerm_log_analytics_workspace" "main" {
  name                = "log-kb-${var.suffix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "main" {
  name                       = "cae-kb-${var.suffix}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
}

resource "azurerm_container_app" "main" {
  name                         = "ca-kb-${var.suffix}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name           = var.resource_group_name
  revision_mode                = "Single"

  identity {
    type = "SystemAssigned"
  }

  template {
    container {
      name   = "kb-assistant"
      image  = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "KEY_VAULT_URL"
        value = var.key_vault_url
      }

      env {
        name  = "AZURE_OPENAI_ENDPOINT"
        value = var.openai_endpoint
      }
      
      env {
        name  = "STORAGE_ACCOUNT_NAME"
        value = var.storage_account_name
      }

      env {
        name  = "APP_PASSWORD"
        value = var.app_password
      }
    }
  }
  
  ingress {
    external_enabled = true
    target_port      = 8000

    traffic_weight {
      percentage = 100
      latest_revision = true
    }
  }
}

resource "azurerm_key_vault_access_policy" "container_app" {
  key_vault_id = var.key_vault_id
  tenant_id    = azurerm_container_app.main.identity[0].tenant_id
  object_id    = azurerm_container_app.main.identity[0].principal_id

  secret_permissions = [
   "Get",
   "List"
  ]
}