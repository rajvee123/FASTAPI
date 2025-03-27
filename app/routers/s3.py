#1
from fastapi import APIRouter
from app.services.s3_utils import list_objects, get_object_metadata

router = APIRouter()

@router.get("/list")
def list_minio_objects():
    """ API to list all objects in the MinIO bucket """
    return list_objects()

@router.get("/metadata/{object_name}")
def object_metadata(object_name: str):
    """ API to fetch metadata of an object """
    return get_object_metadata(object_name)

#2
from fastapi import APIRouter, UploadFile, File, HTTPException
from minio import Minio
from minio.error import S3Error
from app.core.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME

router = APIRouter()

# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Set to True if using HTTPS
)

# Ensure bucket exists
if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
    minio_client.make_bucket(MINIO_BUCKET_NAME)


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        minio_client.put_object(
            MINIO_BUCKET_NAME, file.filename, file.file, length=-1, part_size=10 * 1024 * 1024
        )
        return {"message": f"File '{file.filename}' uploaded successfully"}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list/")
def list_files():
    try:
        objects = minio_client.list_objects(MINIO_BUCKET_NAME)
        return {"files": [obj.object_name for obj in objects]}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
def download_file(filename: str):
    try:
        url = minio_client.presigned_get_object(MINIO_BUCKET_NAME, filename)
        return {"download_url": url}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{filename}")
def delete_file(filename: str):
    try:
        minio_client.remove_object(MINIO_BUCKET_NAME, filename)
        return {"message": f"File '{filename}' deleted successfully"}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
