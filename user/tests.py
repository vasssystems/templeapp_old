# webapp/user/test.py
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient
import logging
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .models import CustomUser

logger = logging.getLogger(__name__)
base_url = "/api/v1/user"
User = get_user_model()


def log_api_response(test_function, code, res_data):
    logger.info(f" FEATURES | {test_function} API Status Code : {code}")
    if str(code) in ("400", "401", "404", "500"):
        logger.error(f" FEATURES | {test_function} API Response : {code} - {res_data}")
    else:
        logger.debug(f" FEATURES | {test_function} API Response : {code} - {res_data}")


"""
class UserRegistrationAPITest(APITestCase):

    def test_user_registration(self):
        url = reverse('user:registration')  # Replace 'register' with the actual URL name for user registration

        data = {
            "username": "testuser",
            "password": "TestPassword123",
            "password2": "TestPassword123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "mobile_number": "1234567890",
            "department_id": 1,
            "designation": "6",
            "user_scope": "6"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the user is created in the database
        self.assertTrue(User.objects.filter(username='testuser').exists())


class UserLoginAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='demo', email='demo@example.com', password='TestPassword123')
        self.login_url = reverse('user:login')  # Replace 'login' with the actual URL name for login

    def test_user_login_response(self):
        data = {
            "username": "demo",
            "password": "TestPassword123",
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'User logged Successfully')

        user_data = response.data['data']
        self.assertEqual(user_data['id'], self.user.id)
        self.assertEqual(user_data['uuid'], str(self.user.uuid))
        self.assertEqual(user_data['username'], self.user.username)
        self.assertEqual(user_data['scope'], self.user.user_scope)
        self.assertTrue(response.data['token'])


# Admin API Test cases
class ViewUsersAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test_user', password='password', email="test_user@example.com", user_scope='2'
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.user_1 = CustomUser.objects.create(
            username='demo_user_1', first_name='Demo', last_name='User 1', email='demo1@example.com',
            department_id=1, designation='Staff User', user_scope='6', mobile_number='1234567890', clubs=1
        )
        self.user_2 = CustomUser.objects.create(
            username='demo_user_2', first_name='Demo', last_name='User 2', email='demo2@example.com',
            department_id=2, designation='Portal Admin', user_scope='2', mobile_number='9876543210', clubs=2
        )

    def log_api_response(self, test_function, response_data, err=None):
        if err:
            logger.error(f"USERS | {test_function} API Response : {response_data}")
        else:
            logger.info(f"USERS | {test_function} API Response :")

    def test_retrieve_user(self):
        response = self.client.get(f'{base_url}/view-users/{self.user_1.uuid}/')
        self.assertEqual(response.status_code, 200)
        self.log_api_response('test_retrieve_user', response.data)

    def test_list_users(self):
        response = self.client.get(f'{base_url}/view-users/')
        self.assertEqual(response.status_code, 200)
        self.log_api_response('test_list_users', response.data)

    def test_create_user(self):
        data = {
            'username': 'test_user_3',
            'first_name': 'Test',
            'last_name': 'User 3',
            'email': 'test3@example.com',
            'department_id': 3,
            'designation': '5',
            'user_scope': '7',
            'mobile_number': '1112223330',
            'clubs': 3,
            'password': 'Pass@1234'
        }
        response = self.client.post(f'{base_url}/view-users/', data=data)
        self.assertEqual(response.status_code, 201)
        self.log_api_response('test_create_user', response.data)

    def test_update_user(self):
        data = {
            'first_name': 'Updated',
            'last_name': 'User 1',
            'email': 'updated@example.com',
            'department_id': 4,
            'designation': '5',
            'user_scope': '1',
            'mobile_number': '9998887770',
            'clubs': 4
        }
        response = self.client.put(f'{base_url}/view-users/{self.user_1.uuid}/', data=data)
        self.log_api_response('test_update_user', response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        response = self.client.delete(f'{base_url}/view-users/{self.user_2.uuid}/')
        self.assertEqual(response.status_code, 204)
        self.log_api_response('test_delete_user', response.data)

    def test_pagination(self):
        for i in range(10):
            CustomUser.objects.create(
                username=f'test_user_{i}',
                first_name=f'Test',
                last_name=f'User {i}',
                email=f'test{i}@example.com',
                department_id=i + 10,
                designation='Staff User',
                user_scope='6',
                mobile_number=f'12345678{i}',
                clubs=i + 10
            )

        response = self.client.get(f'{base_url}/view-users/')
        self.assertEqual(response.status_code, 200)
        self.log_api_response('test_pagination', response.data)

        res_data = response.data.get("data")
        if 'next' in res_data:
            self.assertIsNotNone(res_data['next'])
        else:
            self.assertIsNone(res_data.get('next'))
        self.assertIsNone(res_data['previous'])
        self.assertEqual(len(res_data['results']), 10)

"""

# F
# ailed Test cases - Fix and correct future

""" 
class UserAuthenticationTestCase(APITestCase):

    def setUp(self):
        self.register_url = reverse('user:registration')
        self.login_url = reverse('user:login')
        self.logout_url = reverse('user:logout')
        self.change_password_url = reverse('user:change-password')
        self.reset_password_url = reverse('user:reset-user-password')
        self.notification_url = reverse('user:notification-list-create')
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="testuser54",
        password="testpassword", email="testuser54@example.com",user_scope="3")
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "password2": "testpassword",
            "email": "testuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "mobile_number": "1234567890",
            "department_id": 1,
            "designation": "5",
            "user_scope": "6"
        }

        self.login_data = {
            "username": "testuser",
            "password": "testpassword",
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        log_api_response('test_notification_list_create', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

    def test_user_login(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_api_response('test_notification_list_create', response.status_code, response.data)
        self.assertTrue('token' in response.data)

    def test_user_logout(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        response = self.client.post(self.logout_url, format='json')
        log_api_response('test_notification_list_create', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        change_password_data = {
            "old_password": "testpassword",
            "new_password": "newtestpassword"
        }
        response = self.client.post(self.change_password_url, change_password_data, format='json')
        log_api_response('test_notification_list_create', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_user_password(self):
        user = User.objects.create_user(**self.user_data)
        reset_password_data = {
            "uuid": str(user.uuid)
        }
        response = self.client.post(self.reset_password_url, reset_password_data, format='json')
        log_api_response('test_notification_list_create', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_notification_list_create(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        notification_data = {
            "title": "Test Notification",
            "message": "This is a test notification",
        }
        response = self.client.post(self.notification_url, notification_data, format='json')
        log_api_response('test_notification_list_create', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)

    def test_notification_list(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        notification_data = {
            "title": "Test Notification",
            "message": "This is a test notification",
        }
        self.client.post(self.notification_url, notification_data, format='json')

        response = self.client.get(self.notification_url, format='json')
        log_api_response('test_notification_list', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
"""