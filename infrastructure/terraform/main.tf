data "google_project" "current" {
  project_id = var.project_id
}

output "gcp_project_name" {
  value = data.google_project.current.name
}

output "gcp_project_number" {
  value = data.google_project.current.number
}