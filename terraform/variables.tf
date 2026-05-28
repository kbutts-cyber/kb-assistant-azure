variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "eastus"
}

variable "openai_location" {
  description = "Region for Azure OpenAI"
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Name of the main resource group"
  type        = string
  default     = "rg-kb-assistant-azure"
}

variable "openai_api_key" {
  description = "Azure OpenAI API key - stored in Key Vault, never in state"
  type        = string
  sensitive   = true
}

variable "app_password" {
  description = "Password to access the KB Assistant UI"
  type        = string
  sensitive   = true
}