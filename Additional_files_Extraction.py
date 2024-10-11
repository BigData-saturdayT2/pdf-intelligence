from google.cloud import storage
import os
from huggingface_hub import hf_hub_download, HfApi

# Set Hugging Face API details
HUGGINGFACE_REPO_ID = "gaia-benchmark/GAIA"  # Replace with the correct repository ID
HF_API = HfApi()

# Define GCP bucket details
GCP_BUCKET_NAME = "gaia-benchmark-project1-bucket"
GCP_BUCKET_FOLDER = "huggingface_datasets/"

# Initialize the GCP storage client
storage_client = storage.Client()

# Function to upload files to GCP bucket
def upload_file_to_gcp(bucket_name, gcp_path, local_file_path):
    """Uploads a file to a GCP bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcp_path)

    try:
        blob.upload_from_filename(local_file_path)
        print(f"Uploaded {local_file_path} to gs://{bucket_name}/{gcp_path}")
    except Exception as e:
        print(f"Failed to upload {local_file_path}: {e}")

# Function to download all files from HF and upload them to GCP
def download_and_upload_all_files(repo_id, target_directories, bucket_name, base_folder):
    """Downloads all files from Hugging Face Hub and uploads to GCP Storage."""
    # Get the list of files in the HF repository
    repo_files = HF_API.list_repo_files(repo_id, repo_type="dataset")
    print(f"Files in repository: {len(repo_files)} found")

    # Filter files based on the target directories
    all_files = [file for file in repo_files if any(dir in file for dir in target_directories)]

    print(f"Total files to process: {len(all_files)}")

    # Download and upload each file
    for file in all_files:
        print(f"Processing file: {file}")
        try:
            # Download the file from the HF repository
            local_file_path = hf_hub_download(repo_id, filename=file, repo_type="dataset")

            # Construct GCP file path
            gcp_file_path = os.path.join(base_folder, file)

            # Upload the file to GCP bucket
            upload_file_to_gcp(bucket_name, gcp_file_path, local_file_path)
        except Exception as e:
            print(f"Failed to process file {file}: {e}")

# Define target directories (folders) within the repository to process
target_directories = ["test", "validation"]

# Run the function to download and upload all files
download_and_upload_all_files(HUGGINGFACE_REPO_ID, target_directories, GCP_BUCKET_NAME, GCP_BUCKET_FOLDER)
