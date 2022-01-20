import abc
import io

import boto3
from PIL import Image

from application.internal import constants


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
    def __init__(self):
        super().__init__()
        self.dimensions = constants.DEFAULT_DIMENSIONS

    def set_dimension(self, dimension_key: str):
        self.dimensions = {dimension_key: constants.DEFAULT_DIMENSIONS[dimension_key]}

    def process_input(self, image_io: io.BytesIO):
        resized_images = []
        image_io.seek(0)
        image = Image.open(image_io)
        for _, size in self.dimensions.items():
            resized_image = image.resize(size)
            resized_image_io = io.BytesIO()
            resized_image.save(resized_image_io, constants.DEFAULT_IMAGE_FORMAT)
            resized_image_io.seek(0)
            resized_images.append(resized_image_io)
            del resized_image
        if len(resized_images) == 1:
            return resized_images[0]
        return resized_images
