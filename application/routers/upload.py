import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, File, UploadFile

from ..settings import settings, Settings

router = APIRouter(prefix='/upload')


@router.post('/images/', status_code=201)
async def upload_image(upload:UploadFile=File(...), settings:Settings=Depends(settings)):
    s3_client = boto3.client('s3')
    bucket_name = settings.media_bucket_name
    s3_client.upload_fileobj(upload.file, bucket_name, upload.filename)
    return {'status': 'success', 'url': 'http://saintmtool/media/pictures/picture_id'}