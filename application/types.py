from dataclasses import dataclass


@dataclass
class PictureUrls:
    large_url: str
    medium_url: str
    small_url: str
    thumb_url: str


@dataclass
class Picture:
    image_id: str
    urls: PictureUrls


@dataclass
class ResizeMap:
    large_width: int = 1400
    medium_width: int = 700
    small_width: int = 300
    thumb_width: int = 100


@dataclass
class Response:
    data: None
    status: str
