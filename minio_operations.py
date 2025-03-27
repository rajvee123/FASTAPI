from minio import Minio
from minio.error import S3Error

# Initialize MinIO client
minio_client = Minio(
    "127.0.0.1:9000",  # MinIO endpoint
    access_key="minioadmin",  
    secret_key="minioadmin",
    secure=False  # Set to True if using HTTPS
)

bucket_name = "test-bucket"

# Ensure the bucket exists
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' created successfully!")
else:
    print(f"Bucket '{bucket_name}' already exists.")

# Upload a file
file_path = "testfile.txt"  # Replace with your file
object_name = "uploaded_testfile.txt"

try:
    minio_client.fput_object(bucket_name, object_name, file_path)
    print(f"File '{file_path}' uploaded as '{object_name}'")
except S3Error as e:
    print(f"Error uploading file: {e}")

# Download the file
download_path = "downloaded_testfile.txt"
try:
    minio_client.fget_object(bucket_name, object_name, download_path)
    print(f"File '{object_name}' downloaded successfully as '{download_path}'")
except S3Error as e:
    print(f"Error downloading file: {e}")
