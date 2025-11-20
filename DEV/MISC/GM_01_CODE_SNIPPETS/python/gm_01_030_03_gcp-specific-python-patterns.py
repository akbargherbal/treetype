# PATTERN: GCP-Specific Python Patterns

from google.cloud import storage

def create_storage_client():
    """Creates a Google Cloud Storage client."""
    client = storage.Client()
    print("Storage client created successfully.")
    return client

if __name__ == "__main__":
    storage_client = create_storage_client()

# PATTERN: GCP-Specific Python Patterns

from google.cloud import storage

def upload_blob_from_string(bucket_name, blob_name, contents):
    """Uploads a string to a blob in the bucket."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(contents)
    print(f"String uploaded to {blob_name} in bucket {bucket_name}.")

if __name__ == "__main__":
    upload_blob_from_string("my-unique-gcs-bucket", "my-test-file.txt", "Hello, Cloud Storage!")

# PATTERN: GCP-Specific Python Patterns

from google.cloud import storage

def download_blob_as_string(bucket_name, blob_name):
    """Downloads a blob as a string."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    contents = blob.download_as_bytes().decode("utf-8")
    print(f"Downloaded contents from {blob_name}: {contents}")
    return contents

if __name__ == "__main__":
    download_blob_as_string("my-unique-gcs-bucket", "my-test-file.txt")

# PATTERN: GCP-Specific Python Patterns

from google.cloud import storage

def list_blobs_in_bucket(bucket_name):
    """Lists all the blobs in the given bucket."""
    client = storage.Client()
    blobs = client.list_blobs(bucket_name)
    print(f"Blobs in bucket {bucket_name}:")
    for blob in blobs:
        print(f"- {blob.name}")

if __name__ == "__main__":
    list_blobs_in_bucket("my-unique-gcs-bucket")

# PATTERN: GCP-Specific Python Patterns

import functions_framework

@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    if request_json and 'name' in request_json:
        name = request_json['name']
    else:
        name = 'World'
    return f'Hello, {name}!'

# PATTERN: GCP-Specific Python Patterns

import os

def get_gcp_project_id():
    """Retrieves the GCP project ID from environment variables."""
    project_id = os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project_id:
        return f"GCP Project ID: {project_id}"
    else:
        return "GCP Project ID environment variable not found."

if __name__ == "__main__":
    print(get_gcp_project_id())
    # Example for a custom variable:
    # os.environ["MY_CUSTOM_VAR"] = "my_value"
    # print(f"MY_CUSTOM_VAR: {os.environ.get('MY_CUSTOM_VAR', 'Not set')}")