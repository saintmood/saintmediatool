import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, File, UploadFile

from application.internal import utils

from ..settings import Settings, settings

router = APIRouter(prefix='/upload')


@router.post('/images/', status_code=201)
async def upload_image(upload:UploadFile=File(...), settings:Settings=Depends(settings)):
    s3_client = boto3.client('s3')
    bucket_name = settings.media_bucket_name
    image_filename = utils.generate_s3_key()
    metadata = {'original_file_name': upload.filename}
    s3_client.upload_fileobj(upload.file, bucket_name, image_filename, ExtraArgs={'Metadata': metadata})
    resource_url = f'https://{settings.domain}/media/pictures/{image_filename}/'
    return {'status': 'success', 'url': resource_url}
