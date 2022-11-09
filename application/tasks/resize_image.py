import io
from typing import Collection, Optional

from wand import image

from application.types import ResizeMap


def resize_image(picture_io, resize_map: ResizeMap, specific_width: Optional[int] = None) -> Collection[io.BytesIO]:
    if specific_width is not None:
        with (image.Image(file=picture_io) as picture,
              picture.clone() as resized_picture
              ):
            resized_picture.transform(resize=f'{specific_width}x')
            return resized_picture.make_blob(format='png')
    with (
        image.Image(file=picture_io) as picture,
        picture.clone() as large_picture,
        picture.clone() as medium_picture,
        picture.clone() as small_picture,
        picture.clone() as thumb_picture
    ):
        large_picture.transform(resize=f'{resize_map.large_width}x')
        medium_picture.transform(resize=f'{resize_map.medium_width}x')
        small_picture.transform(resize=f'{resize_map.small_width}x')
        thumb_picture.transform(resize=f'{resize_map.thumb_width}x')
        return (large_picture.make_blob(format='png'),
                medium_picture.make_blob(format='png'),
                small_picture.make_blob(format='png'),
                thumb_picture.make_blob(format='png'),)
