import base64

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends

from application.internal import utils
from application.internal.handlers import (
    RetrieveSingleImageHandler,
    ImageDimensionHandler,
)

from application.types import Picture, PictureUrls
from ..settings import Settings, settings

router = APIRouter(prefix='/retrieve')


@router.get('/images/', status_code=200)
async def retrieve_images(settings: Settings = Depends(settings)):
    s3_client = boto3.client('s3')
    bucket_name = settings.media_bucket_name
    return {'status': 'success'}


@router.get('/images/{image_id}/')
async def retrieve_single_image(image_id: str, settings: Settings = Depends(settings)):
    retrieve_handler = RetrieveSingleImageHandler()
    dimensions_handler = ImageDimensionHandler()
    retrieve_handler.set_next(dimensions_handler)
    try:
        thumbnail, small, medium, large = retrieve_handler.handle(
            image_id, settings.media_bucket_name
        )
    except ClientError:
        return {'status': 'error', 'data': {'message': 'boto3 error'}}
    picture_urls = PictureUrls(large_url=large, medium_url=medium, small_url=small, thumb_url=thumbnail)
    picture = Picture(urls=picture_urls)
    return {
        'status': 'success',
        'data': picture
    }
