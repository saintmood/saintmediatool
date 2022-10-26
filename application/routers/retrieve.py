import io
from typing import Collection

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends

from application.internal.handlers import (
    RetrieveSingleImageHandler,
    ImageDimensionHandler,
)

from application.types import Image, Picture, PictureUrls, Response

from ..settings import Settings, settings

router = APIRouter(prefix='/retrieve')


@router.get('/images/', status_code=200)
async def retrieve_images(settings: Settings = Depends(settings)):
    s3_client = boto3.client('s3')
    bucket_name = settings.media_bucket_name
    return {'status': 'success'}


@router.get('/images/{image_id}/')
async def retrieve_single_picture(image_id: str, settings: Settings = Depends(settings)):
    retrieve_handler = RetrieveSingleImageHandler()
    try:
        retrieve_handler.handle(image_id, settings.media_bucket_name)
    except ClientError:
        return {'status': 'error', 'data': {'message': 'boto3 error'}}
    resource_url = f'https://{settings.domain}/media/pictures/{image_id}/'
    picture = Picture(
        picture_id=image_id,
        picture_urls=PictureUrls(
            large_url=resource_url + 'large/',
            medium_url=resource_url + 'medium/',
            small_url=resource_url + 'small/',
            thumb_url=resource_url + 'thumb/'
        )
    )
    return Response(status="success", data=picture)
