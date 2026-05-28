variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "suffix" {
  type = string
}

variable "key_vault_id" {
  type = string
}

variable "key_vault_url" {
  type = string
}

variable "openai_endpoint" {
  type = string
}

variable "storage_account_name" {
  type = string
}

variable "app_password" {
  type      = string
  sensitive = true
}