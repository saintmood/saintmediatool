import abc
import io
from typing import Collection, Optional, Union

import boto3

from application import types
from application.internal import constants
from application.tasks.resize_image import resize_image


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

    def __init__(self, dimension: Optional[str] = None) -> None:
        self.dimension = dimension

    def process_input(self, picture_io: io.BytesIO) -> Collection[io.BytesIO]:
        picture_io.seek(0)
        resize_map = types.ResizeMap()
        resize_width = getattr(resize_map, f'{self.dimension}_width')
        resized_images: Union[Collection[io.BytesIO], io.BytesIO] = resize_image(
            picture_io, resize_map, specific_width=resize_width)
        return resized_images
