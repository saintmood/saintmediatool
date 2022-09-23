from dataclasses import dataclass


@dataclass
class PictureUrls:
    large_url: str
    medium_url: str
    small_url: str
    thumb_url: str


@dataclass
class Picture:
    urls: PictureUrls
