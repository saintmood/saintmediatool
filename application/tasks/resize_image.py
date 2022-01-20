from wand.image import image


def resize_image(filepath):
    with Image(filename=filepath) as img:
        img.resize(100, 100)
