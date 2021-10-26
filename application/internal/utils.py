import uuid


def generate_s3_key() -> str:
    return uuid.uuid4().hex
