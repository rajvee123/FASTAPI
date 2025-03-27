#1
from fastapi import FastAPI, UploadFile, File
from minio import Minio
import io

app = FastAPI()

# MinIO Configuration
MINIO_ENDPOINT = "http://localhost:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"

# Initialize MinIO client
minio_client = Minio(
    endpoint=MINIO_ENDPOINT.replace("http://", "").replace("https://", ""),
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False  # Set to True if using HTTPS
)

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "FastAPI with MinIO is working!"}

# List All Buckets
@app.get("/list_buckets")
def list_buckets():
    buckets = minio_client.list_buckets()
    return {"buckets": [bucket.name for bucket in buckets]}

# Upload File to MinIO
@app.post("/upload/")
async def upload_file(bucket_name: str, file: UploadFile = File(...)):
    try:
        # Ensure bucket exists
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        # Read file content
        file_content = await file.read()
        file_stream = io.BytesIO(file_content)

        # Upload to MinIO
        minio_client.put_object(
            bucket_name, file.filename, file_stream, len(file_content)
        )

        return {"message": f"File '{file.filename}' uploaded to bucket '{bucket_name}'"}
    
    except Exception as e:
        return {"error": str(e)}

# List Files in a Bucket
@app.get("/list_files/{bucket_name}")
def list_files(bucket_name: str):
    try:
        objects = minio_client.list_objects(bucket_name)
        return {"files": [obj.object_name for obj in objects]}
    
    except Exception as e:
        return {"error": str(e)}

# Download a File
@app.get("/download/")
def download_file(bucket_name: str, file_name: str):
    try:
        response = minio_client.get_object(bucket_name, file_name)
        return {"file_content": response.read().decode()}
    
    except Exception as e:
        return {"error": str(e)}



#2
from fastapi import FastAPI
from app.routers import s3

app = FastAPI()

app.include_router(s3.router, prefix="/minio", tags=["MinIO"])

@app.get("/")
def home():
    return {"message": "Welcome to S3cretTables"}

#3
app.include_router(s3.router, prefix="/s3", tags=["MinIO Operations"])
