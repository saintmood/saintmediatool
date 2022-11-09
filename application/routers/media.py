import io

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends
from fastapi.responses import Response

from application.internal.handlers import (
    RetrieveSingleImageHandler,
    ImageDimensionHandler,
)
from ..settings import Settings, settings

router = APIRouter(prefix='/media')


@router.get('/pictures/{picture_id}/{dimension}/')
async def get_single_image(picture_id: str, dimension: str, settings: Settings = Depends(settings)):
    retrieve_handler = RetrieveSingleImageHandler()
    dimensions_handler = ImageDimensionHandler(dimension=dimension)
    retrieve_handler.set_next(dimensions_handler)
    try:
        picture: io.Bytes = retrieve_handler.handle(picture_id, settings.media_bucket_name)
    except ClientError:
        return {'status': 'error', 'data': {'message': 'boto3 error'}}
    return Response(picture, media_type='image/png')
