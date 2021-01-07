from .base import BaseTestCase


class ImageUploadTestCase(BaseTestCase):

    endpoint_url = '/upload/images/'

    def test_upload_image_success(self):
        upload_data = {
            'image': 'image_object'
        }
        expected_url = 'http://saintmtool/media/pictures/picture_id'
        response = self.client.post(self.endpoint_url, headers={"AuthToken": "sometokenvalue"}, json=upload_data)
        self.assertEqual(response.status_code, 201)
        resp_json = response.json()
        self.assertEqual(resp_json['status'], 'success')
        self.assertEqual(resp_json['url'], expected_url)