variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "tenant_id" {
  type = string
}

variable "object_id" {
  type = string
}

variable "suffix" {
  type = string
}

variable "openai_api_key" {
  type      = string
  sensitive = true
}

variable "pipeline_object_id" {
  type = string
}

variable "admin_object_id" {
  type = string
}