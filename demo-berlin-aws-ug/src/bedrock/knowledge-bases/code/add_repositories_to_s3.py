import os
import subprocess
import boto3
from botocore.exceptions import ClientError

# List of repositories to clone
repo_urls = [
    "https://github.com/trekhleb/javascript-algorithms.git",
    "https://github.com/ripienaar/free-for-dev.git",
    # "https://github.com/kamranahmedse/developer-roadmap.git"
]

# S3 bucket name
bucket_name = "swb-artifactcs"

# Create an S3 client
s3 = boto3.client("s3", region_name="us-east-1")

for repo_url in repo_urls:
    # Get the repository name from the URL
    repo_name = repo_url.split("/")[-1].replace(".git", "")

    # Clone the repository
    subprocess.run(["git", "clone", repo_url], check=True)

    # Upload the repository contents to S3
    for root, dirs, files in os.walk(repo_name):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.join('github-repositories', repo_name, os.path.relpath(file_path, repo_name))
            try:
                s3.upload_file(file_path, bucket_name, s3_key)
                print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
            except ClientError as e:
                print(f"Error uploading {file_path}: {e}")

    # Remove the cloned repository
    subprocess.run(["rm", "-rf", repo_name], check=True)
