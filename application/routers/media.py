import base64

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends

from application.internal import utils
from application.internal.handlers import RetrieveSingleImageHandler, ImageDimensionHandler
from ..settings import Settings, settings

router = APIRouter(prefix='/media')

@router.get('/images/{image_id}/')
async def get_single_image(image_id:str, settings:Settings=Depends(settings)):
    print(image_id.split('_'))
