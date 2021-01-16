import uuid


def generate_s3_key():
    return uuid.uuid4().hex
