from .base import BaseTestCase


class ImageUploadTestCase(BaseTestCase):

    endpoint_url = '/upload/images/'

    def test_upload_image_success(self):
        response = self.client.post(self.endpoint_url, headers={"AuthToken": "sometokenvalue"})
        self.assertEqual(response.status_code, 201)
        resp_json = response.json()
        self.assertEqual(resp_json['status'], 'success')