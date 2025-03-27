from minio import Minio
from minio.error import S3Error
from app.core.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME

# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Change to True if using HTTPS
)

def list_objects():
    """ List all objects in the MinIO bucket """
    try:
        objects = minio_client.list_objects(MINIO_BUCKET_NAME)
        return [obj.object_name for obj in objects]
    except S3Error as e:
        return {"error": str(e)}

def get_object_metadata(object_name):
    """ Fetch metadata of a specific object """
    try:
        obj_stat = minio_client.stat_object(MINIO_BUCKET_NAME, object_name)
        return {
            "filename": obj_stat.object_name,
            "size": obj_stat.size,
            "last_modified": obj_stat.last_modified.isoformat(),
            "content_type": obj_stat.content_type,
        }
    except S3Error as e:
        return {"error": str(e)}
