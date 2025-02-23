resource "google_project_service" "secretmanager" {
  project = var.project_id
  service = "secretmanager.googleapis.com"
}

resource "google_secret_manager_secret" "my_secret_api_key" {
 secret_id = "my_secret_api_key"

 labels = {
   label = "foobar"
 }

 replication {
   user_managed {
     replicas {
       location = var.region
     }
   }
 }
}

resource "google_secret_manager_secret_version" "my_secret_api_key_first_version" {
  secret = google_secret_manager_secret.my_secret_api_key.id

  secret_data = var.my_secret_api_key
}