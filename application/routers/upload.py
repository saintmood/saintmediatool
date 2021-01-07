from fastapi import APIRouter


router = APIRouter(prefix='/upload')


@router.post('/images/')
async def upload_image():
    pass