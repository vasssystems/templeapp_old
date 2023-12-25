# webapp/adminapp/test.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import UserAgreements, AdminConfig, Logos, GeneralSettings, Payments

import logging

base_url = "/api/v1/adminapp"

logger = logging.getLogger(__name__)

""" 
def log_api_response(test_function, code, res_data):
    logger.info(f" FEATURES | {test_function} API Status Code : {code}")
    if str(code) in ("400", "401", "404", "500"):
        logger.error(f" FEATURES | {test_function} API Response : {code} - {res_data}")
    else:
        logger.debug(f" FEATURES | {test_function} API Response : {code} - {res_data}")


class usersagreementsAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test_user', password='password', email="test_user@asv.con", user_scope='2'
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create a test agreement object
        self.agreement_1 = UserAgreements.objects.create(
            title='Test Agreement',
            type='TOS',
            description='Test Description',
            # Include other fields according to the usersagreements model
        )

    def test_retrieve_agreement(self):
        # Test retrieve agreement
        response = self.client.get(f'{base_url}/usersagreements/{self.agreement_1.uuid}/')
        log_api_response('test_retrieve_agreement', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the agreement data in the response
        self.assertEqual(response.data['title'], 'Test Agreement')
        self.assertEqual(response.data['type'], 'TOS')
        # Add assertions for other fields as needed

    def test_list_usersagreements(self):
        # Test list usersagreements
        response = self.client.get(f'{base_url}/usersagreements/')
        log_api_response('test_list_usersagreements', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the structure of the response
        self.assertIn('results', response.data)
        # Add assertions for pagination if needed

    def test_create_agreement(self):
        # Test create agreement
        data = {
            'title': 'New Test Agreement',
            'type': 'TOS',
            'description': 'New Test Description',
            # Include other fields required for creating an agreement
        }
        response = self.client.post(f'{base_url}/usersagreements/', data=data)
        log_api_response('test_create_agreement', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Validate the newly created agreement's data in the response
        self.assertEqual(response.data['title'], 'New Test Agreement')
        self.assertEqual(response.data['type'], 'Privacy Policy')
        # Add assertions for other fields as needed

    def test_update_agreement(self):
        # Test update agreement
        data = {
            'title': 'Updated Agreement',
            # Include fields to update agreement
        }
        response = self.client.put(f'{base_url}/usersagreements/{self.agreement_1.uuid}/', data=data)
        log_api_response('test_update_agreement', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the updated agreement's data in the response
        self.assertEqual(response.data['title'], 'Updated Agreement')
        # Add assertions for other fields as needed

    def test_delete_agreement(self):
        # Test delete agreement
        response = self.client.delete(f'{base_url}/usersagreements/{self.agreement_1.uuid}/')
        log_api_response('test_delete_agreement', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

"""