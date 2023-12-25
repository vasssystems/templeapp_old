# webapp/utils/test.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.apps import apps

base_url = "/api/v1/features"

""" 
class ChangeStatusAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_change_status(self):
        # Define a list of tuples containing slug names and their corresponding model names
        model_slug_mapping = [
            ('noticeboard', 'NoticeBoard'),
            ('batch', 'Batch'),
            ('faq', 'Faq'),
            # Add more tuples for other models here as needed
        ]

        for slug, model_name in model_slug_mapping:
            # Create an object in the model for testing
            model = apps.get_model(app_label='features', model_name=model_name)
            obj = model.objects.create(title=f'Test {model_name}', id_no=1, message='Test Message')

            # Send a POST request to toggle the status of the object
            data = {
                'slug': slug,
                'obj_id': obj.id,
                'status': False  # Replace with the desired status change
            }

            url = base_url + 'utils/change-status/'
            response = self.client.post(url, data, format='json')

            # Check if the status change was successful
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            updated_obj = model.objects.get(id=obj.id)
            self.assertEqual(updated_obj.status, data['status'])

"""
