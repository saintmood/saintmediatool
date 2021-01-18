
from unittest import mock

import boto3
from moto import mock_s3

from application.routers import upload
from application.tests import fixtures

from .base import BaseTestCase


class ImagesRetriveTestCase(BaseTestCase):

    endpoint_url = '/retrive/images/'

    @mock_s3
    def test_retrive_images_success(self):
        response = self.client.get(
            self.endpoint_url
        )
        self.assertEqual(response.status_code, 200)

class ImageRetriveTestCase(BaseTestCase):

    endpoint_url = '/retrive/image/{image_id}/'

    @mock_s3
    def test_retrive_single_image_success(self):
        expected_image_id = 'abc123'
        response = self.client.get(
            self.endpoint_url.format(image_id=expected_image_id)
        )
        self.assertEqual(response.status_code, 200)