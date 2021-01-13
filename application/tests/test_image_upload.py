import boto3
from moto import mock_s3

from application.tests import fixtures
from .base import BaseTestCase


class ImageUploadTestCase(BaseTestCase):

    endpoint_url = '/upload/images/'

    @mock_s3
    def test_upload_image_success(self):
        conn = boto3.resource('s3')
        conn.create_bucket(Bucket='saintmtool')
        test_image = fixtures.create_test_image()
        expected_url = 'http://saintmtool/media/pictures/picture_id'
        response = self.client.post(
            self.endpoint_url, 
            headers={'AuthToken': 'sometokenvalue'},
            files={'upload': (test_image.name, test_image, 'image/png')}
        )
        self.assertEqual(response.status_code, 201)
        resp_json = response.json()
        self.assertEqual(resp_json['status'], 'success')
        self.assertEqual(resp_json['url'], expected_url)