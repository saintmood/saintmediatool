import boto3
from application.internal import utils
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends

from ..settings import Settings, settings

router = APIRouter(prefix='/retrieve')


@router.post('/images/', status_code=200)
async def retrieve_images(settings:Settings=Depends(settings)):
    s3_client = boto3.client('s3')
    bucket_name = settings.media_bucket_name
    return {'status': 'success'}