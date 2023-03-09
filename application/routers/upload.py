import boto3
from fastapi import APIRouter, Depends, File, UploadFile

from application.internal import utils
from application.types import Picture, PictureUrls, Response

from ..settings import Settings, settings

router = APIRouter(prefix='/upload')


@router.post('/images/', status_code=201)
async def upload_image(
    upload: UploadFile = File(...), settings: Settings = Depends(settings)
) -> Response:
    s3_client = boto3.client('s3')
    bucket_name = settings.media_bucket_name
    metadata = {'original_file_name': upload.filename}
    image_key = utils.generate_s3_key()
    s3_client.upload_fileobj(
        upload.file, bucket_name, image_key, ExtraArgs={'Metadata': metadata}
    )
    resource_url = f'https://{settings.domain}/media/pictures/{image_key}/'
    picture_urls = PictureUrls(
        large_url=resource_url + 'large/',
        medium_url=resource_url + 'medium/',
        small_url=resource_url + 'small/',
        thumb_url=resource_url + 'thumb/'
    )
    picture = Picture(
        picture_id=image_key,
        picture_urls=picture_urls
    )
    return Response(status='success', data=picture)
