import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, File, UploadFile

from ..settings import settings

router = APIRouter(prefix='/upload', dependencies=[Depends(settings)])


@router.post('/images/', status_code=201)
async def upload_image(
    upload:UploadFile=File(...)
):
    s3_client = boto3.client('s3')
    bucket_name = 'saintmtool'
    s3_client.upload_fileobj(upload.file, bucket_name, upload.filename)
    return {'status': 'success', 'url': 'http://saintmtool/media/pictures/picture_id'}