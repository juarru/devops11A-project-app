// variables.tf

variable "project_id" {
  description = "despliegue-458304"
  type        = string
}

variable "region" {
  description = "Región de Google Cloud"
  type        = string
  default     = "europe-west4"
}

variable "zones" {
  description = "Zonas para desplegar los nodos del cluster"
  type        = list(string)
  default     = ["europe-west4-a"]
}

variable "cluster_name" {
  description = "Nombre del cluster GKE"
  type        = string
  default     = "despliegue-final-cluster"
}

variable "network" {
  description = "Red VPC para el cluster"
  type        = string
  default     = "default"
}

variable "subnetwork" {
  description = "Subred para el cluster"
  type        = string
  default     = "default"
}

variable "ip_range_pods" {
  description = "Rango de IP secundario para pods"
  type        = string
  default     = ""
}

variable "ip_range_services" {
  description = "Rango de IP secundario para servicios"
  type        = string
  default     = ""
}

variable "machine_type" {
  description = "Tipo de máquina para los nodos"
  type        = string
  default     = "e2-standard-8"
}

variable "min_node_count" {
  description = "Número mínimo de nodos por zona"
  type        = number
  default     = 1
}

variable "max_node_count" {
  description = "Número máximo de nodos por zona"
  type        = number
  default     = 3
}

variable "disk_size_gb" {
  description = "Tamaño del disco para los nodos en GB"
  type        = number
  default     = 100
}

variable "initial_node_count" {
  description = "Número inicial de nodos por zona"
  type        = number
  default     = 1
}

variable "service_account" {
  description = "Cuenta de servicio para los nodos"
  type        = string
  default     = ""
}

variable "argocd_chart_version" {
  description = "Versión del chart de Helm para Argo CD"
  type        = string
  default     = "5.51.4" 
}
variable "app_namespace" {
  description = "Namespace para la aplicación gestionada por ArgoCD"
  type        = string
  default     = "despliegue-final-ns"
}

