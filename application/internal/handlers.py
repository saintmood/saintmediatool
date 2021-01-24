import abc
import io

import boto3
from PIL import Image


class BaseHandler(abc.ABC):
    """
        Define parent for all handlers.
        This is another implementation of "Chain Of Command" patter.
    """

    def __init__(self):
        self.next_to = None

    def set_next(self, handler) -> None:
        self.next_to = handler

    @abc.abstractmethod
    def process_input(self, *args, **kwargs):
        """Implement the actions."""

    def handle(self, *args, **kwargs):
        result = self.process_input(*args, **kwargs)
        if self.next_to is not None:
            return self.next_to.process_input(result)
        return result


class RetrieveSingleImageHandler(BaseHandler):

    def process_input(self, image_uuid: str, butcket_name: str):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(butcket_name)
        image_io = io.BytesIO()
        bucket.download_fileobj(image_uuid, image_io)
        return image_io


class ImageDimensionHandler(BaseHandler):

    def process_input(self, image_io: io.BytesIO):
        image_io.seek(0)
        image = Image.open(image_io)
        small_image = image.resize((128, 128))
        medium_image = image.resize((450, 450))
        large_image = image.resize((960, 960))
        small_image_io = io.BytesIO()
        small_image.save(small_image_io, 'png')
        medium_image_io = io.BytesIO()
        medium_image.save(medium_image_io, 'png')
        large_image_io = io.BytesIO()
        large_image.save(large_image_io, 'png')
        small_image_io.seek(0)
        medium_image_io.seek(0)
        large_image_io.seek(0)
        return small_image_io, medium_image_io, large_image_io