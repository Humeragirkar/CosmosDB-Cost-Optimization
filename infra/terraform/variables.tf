variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "East US"
}

variable "prefix" {
  description = "Prefix for resource naming"
  type        = string
  default     = "costopt"
}
