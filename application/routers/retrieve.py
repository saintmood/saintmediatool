import boto3
from application.internal import utils
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends

from application.internal.handlers import RetrieveSingleImageHandler
from ..settings import Settings, settings

router = APIRouter(prefix='/retrieve')


@router.get('/images/', status_code=200)
async def retrieve_images(settings:Settings=Depends(settings)):
    s3_client = boto3.client('s3')
    bucket_name = settings.media_bucket_name
    return {'status': 'success'}


@router.get('/images/{image_id}/')
async def retrieve_single_image(image_id:str, settings:Settings=Depends(settings)):
    retrieve_handler = RetrieveSingleImageHandler()
    response = retrieve_handler.handle(image_id)
    return {'status': 'success', 'data': {'small': response['small']}}