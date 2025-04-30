variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The region to deploy resources"
  type        = string
  default     = "europe-west3"
}

variable "zone" {
  description = "The zone to deploy resources"
  type        = string
  default     = "europe-west3-b"
}

variable "my_secret_api_key" {
  description = "The secret API key"
  type        = string
  sensitive   = true
}
