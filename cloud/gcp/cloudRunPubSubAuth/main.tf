resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "docker-repo-cloud-run"
  format        = "DOCKER"
  description   = "A Docker repository for cloud run POC"
}

resource "google_pubsub_topic" "default" {
  name = "pubsub-cloudrun-poc"
}

resource "google_cloud_run_v2_service" "default" {
  name     = "pubsub-tutorial"
  location = var.region
  template {
    containers {
      image = "europe-west3-docker.pkg.dev/frodigo-tutorials-terraform/docker-repo-cloud-run/pubsub:1.5"
    }
  }
}

# Create or select a service account to represent the Pub/Sub subscription identity.
resource "google_service_account" "pubsub-sa" {
  account_id   = "cloud-run-pubsub-invoker"
  display_name = "Cloud Run Pub/Sub Invoker"
}

# Give the invoker service account permission to invoke your pubsub-tutorial service
resource "google_cloud_run_service_iam_binding" "binding" {
  location = google_cloud_run_v2_service.default.location
  service  = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  members  = ["serviceAccount:${google_service_account.pubsub-sa.email}"]
}

# Allow Pub/Sub to create authentication tokens in your project
resource "google_project_service_identity" "pubsub_agent" {
  provider = google-beta
  project  = var.project_id
  service  = "pubsub.googleapis.com"
}

resource "google_project_iam_binding" "project_token_creator" {
  project = var.project_id
  role    = "roles/iam.serviceAccountTokenCreator"
  members = ["serviceAccount:${google_project_service_identity.pubsub_agent.email}"]
}

#Create a Pub/Sub subscription with the service account
resource "google_pubsub_subscription" "subscription" {
  name  = "pubsub_subscription"
  topic = google_pubsub_topic.default.name
  push_config {
    push_endpoint = google_cloud_run_v2_service.default.uri
    oidc_token {
      service_account_email = google_service_account.pubsub-sa.email
    }
    attributes = {
      x-goog-version = "v1"
    }
  }
}