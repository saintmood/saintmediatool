import boto3
from moto import mock_s3

from application.tests import fixtures

from .base import BaseTestCase


class ImageGetTestCase(BaseTestCase):

    endpoint_url = '/media/pictures/{picture_id}/{dimension}/'

    @mock_s3
    def test_get_image_small_dimension_success(self):
        expected_image_id = 'abc123'
        expected_image_dimension = 'small'
        conn = boto3.resource('s3')
        conn.create_bucket(Bucket=self.settings.media_bucket_name)
        test_image = fixtures.create_test_image()
        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(
            test_image, self.settings.media_bucket_name, expected_image_id
        )

        response = self.client.get(
            self.endpoint_url.format(
                picture_id=expected_image_id, dimension=expected_image_dimension
            ),
            headers={'AuthToken': 'sometokenvalue'},
        )
        self.assertEqual(response.status_code, 200)

    @mock_s3
    def test_get_image_small_dimension_wrong_filename(self):
        expected_image_id = 'abc123'
        expected_image_dimension = 'small'
        conn = boto3.resource('s3')
        conn.create_bucket(Bucket=self.settings.media_bucket_name)
        test_image = fixtures.create_test_image()
        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(
            test_image, self.settings.media_bucket_name, expected_image_id
        )

        response = self.client.get(
            self.endpoint_url.format(
                picture_id=expected_image_id + '!' + expected_image_dimension,
                dimension='small'
            ),
            headers={'AuthToken': 'sometokenvalue'},
        )
        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertEqual(resp_json['status'], 'error')
