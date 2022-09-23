from unittest import mock

import boto3
from moto import mock_s3

from application.routers import upload
from application.tests import fixtures

from .base import BaseTestCase


class ImagesRetriveTestCase(BaseTestCase):

    endpoint_url = '/retrieve/images/'

    @mock_s3
    def test_retrive_images_success(self):
        response = self.client.get(
            self.endpoint_url, headers={'AuthToken': 'sometokenvalue'}
        )
        self.assertEqual(response.status_code, 200)


class ImageRetriveTestCase(BaseTestCase):

    endpoint_url = '/retrieve/images/{image_id}/'

    @mock_s3
    def test_retrive_single_image_success(self):
        expected_image_id = 'abc123'
        conn = boto3.resource('s3')
        conn.create_bucket(Bucket=self.settings.media_bucket_name)
        test_image = fixtures.create_test_image()
        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(
            test_image, self.settings.media_bucket_name, expected_image_id
        )

        response = self.client.get(
            self.endpoint_url.format(image_id=expected_image_id),
            headers={'AuthToken': 'sometokenvalue'},
        )
        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertEqual(resp_json['status'], 'success')
        self.assertIsNotNone(resp_json['data']['urls']['small_url'])
        self.assertIsNotNone(resp_json['data']['urls']['medium_url'])
        self.assertIsNotNone(resp_json['data']['urls']['large_url'])

    @mock_s3
    def test_retrive_single_image_not_found_error(self):
        expected_image_id = 'abc123'
        conn = boto3.resource('s3')
        conn.create_bucket(Bucket=self.settings.media_bucket_name)

        response = self.client.get(
            self.endpoint_url.format(image_id=expected_image_id),
            headers={'AuthToken': 'sometokenvalue'},
        )
        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertEqual(resp_json['status'], 'error')
        self.assertIsNotNone(resp_json['data']['message'])
