from .base import BaseTestCase


class ImageUploadTestCase(BaseTestCase):

    endpoint_url = '/api/v1/image/upload'

    def test_upload_image_success(self):
        response = self.client.post(self.endpoint_url)
        self.assertEqual(response.status_code, 201)