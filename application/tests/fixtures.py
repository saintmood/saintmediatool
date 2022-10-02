from io import BytesIO
from typing import Any

from PIL import Image


def create_test_image() -> Any:
    file = BytesIO()
    image = Image.new('RGBA', size=(1600, 1440), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file
