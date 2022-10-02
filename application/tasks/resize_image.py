from wand import image

from application.internal import utils
from application.types import ResizeMap


async def resize_image(picture_io, resize_map: ResizeMap):
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
