from unittest import mock

import boto3
from moto import mock_s3

from application.tests import fixtures

from .base import BaseTestCase


class ImageUploadTestCase(BaseTestCase):

    endpoint_url = '/upload/images/'

    @mock_s3
    @mock.patch('application.internal.utils.generate_s3_key')
    def test_upload_image_success(self, generate_s3_key_mock):
        picture_aws_key = 'aws_s3_bucket_key'
        generate_s3_key_mock.return_value = picture_aws_key
        conn = boto3.resource('s3')
        conn.create_bucket(Bucket=self.settings.media_bucket_name)
        test_image = fixtures.create_test_image()
        # expected_url = (
        #     f'https://{self.settings.domain}/media/pictures/{picture_aws_key}/'
        # )
        response = self.client.post(
            self.endpoint_url,
            headers={'AuthToken': 'sometokenvalue'},
            files={'upload': (test_image.name, test_image, 'image/png')},
        )
        self.assertEqual(response.status_code, 201)
        resp_json = response.json()
        self.assertEqual(resp_json['status'], 'success')
        self.assertEqual(resp_json['data']['picture_id'], picture_aws_key)
