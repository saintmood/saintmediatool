import base64

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends
from fastapi.responses import Response

from application.internal import utils
from application.internal.handlers import (
    RetrieveSingleImageHandler,
    ImageDimensionHandler,
)
from ..settings import Settings, settings

router = APIRouter(prefix='/media')


@router.get('/images/{image_id}/')
async def get_single_image(image_id: str, settings: Settings = Depends(settings)):
    # @TODO splitting symbol should be a constant
    try:
        image_id, dimension = image_id.split('_')
    except ValueError:
        return {'status': 'error', 'data': {'message': 'wrong file name'}}
    retrieve_handler = RetrieveSingleImageHandler()
    dimensions_handler = ImageDimensionHandler()
    dimensions_handler.set_dimension(dimension)
    retrieve_handler.set_next(dimensions_handler)
    try:
        image = retrieve_handler.handle(image_id, settings.media_bucket_name)
    except ClientError:
        return {'status': 'error', 'data': {'message': 'boto3 error'}}
    return Response(image.read(), media_type='image/png')
