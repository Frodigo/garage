resource "google_project_service" "artifactregistry" {
  service                    = "artifactregistry.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

resource "google_project_service" "containerregistry" {
  service                    = "containerregistry.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

resource "google_project_service" "cloudbuild" {
  service                    = "cloudbuild.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

resource "google_project_service" "pubsub" {
  service                    = "pubsub.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

resource "google_project_service" "run" {
  service                    = "run.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}