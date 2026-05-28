# KB Assistant Azure — Infrastructure


terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "kbterraformstate123"
    container_name       = "tfstate"
    key                  = "kb-assistant-azure.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

module "storage" {
  source              = "./modules/storage"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  suffix              = random_string.suffix.result
}

module "keyvault" {
  source              = "./modules/keyvault"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  object_id           = data.azurerm_client_config.current.object_id
  suffix              = random_string.suffix.result
  openai_api_key      = var.openai_api_key
  pipeline_object_id  = "b0e8857b-6e09-4349-8fb0-a9b45fdc7ddb"
}

module "openai" {
  source              = "./modules/openai"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.openai_location
  suffix              = random_string.suffix.result
}

module "container_app" {
  source               = "./modules/container_app"
  resource_group_name  = azurerm_resource_group.main.name
  location             = azurerm_resource_group.main.location
  suffix               = random_string.suffix.result
  key_vault_id         = module.keyvault.key_vault_id
  key_vault_url        = module.keyvault.key_vault_url
  openai_endpoint      = module.openai.endpoint
  storage_account_name = module.storage.storage_account_name
  app_password         = var.app_password
}
