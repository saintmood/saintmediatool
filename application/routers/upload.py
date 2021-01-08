from fastapi import APIRouter, File, UploadFile


router = APIRouter(prefix='/upload')


@router.post('/images/', status_code=201)
async def upload_image(
    upload:UploadFile=File(...)
):
    return {'status': 'success', 'url': 'http://saintmtool/media/pictures/picture_id'}