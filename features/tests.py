# webapp/features/test.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient
from rest_framework import status
from .models import (Departments, Clubs, NoticeBoard)

import logging

base_url = "/api/v1/features"

logger = logging.getLogger(__name__)


def log_api_response(test_function, code, res_data):
    logger.info(f" FEATURES | {test_function} API Status Code : {code}")
    if str(code) in ("400", "401", "404", "500"):
        logger.error(f" FEATURES | {test_function} API Response : {code} - {res_data}")
    else:
        logger.debug(f" FEATURES | {test_function} API Response : {code} - {res_data}")

"""
class DepartmentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test_user', password='password', email="test_user@asv.con", user_scope='2'
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.department_1 = Departments.objects.create(
            name='Demo', code='T01', description='Demo department', established_at='2023-12-05'
        )
        self.department_2 = Departments.objects.create(
            name='Random ', code='T02', description='Random Dept', established_at='2023-12-06'
        )

    def test_retrieve_department(self):
        response = self.client.get(f'{base_url}/departments/{self.department_1.uuid}/')
        log_api_response('test_pagination', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_departments(self):
        response = self.client.get(f'{base_url}/departments/')
        log_api_response('test_retrieve_department', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_department(self):
        data = {
            'name': 'Test Department',
            'code': 'T03',
            'description': 'Test description',
            'established_at': '2023-12-07'
        }
        response = self.client.post(f'{base_url}/departments/', data=data)
        log_api_response('test_create_department', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_department(self):
        data = {
            'name': 'Updated Department',
            'code': 'T01A',
            'description': 'Updated description',
            'established_at': '2023-12-08'
        }
        response = self.client.put(f'{base_url}/departments/{self.department_1.uuid}/', data=data)
        log_api_response('test_update_department', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_department(self):
        response = self.client.delete(f'{base_url}/departments/{self.department_2.uuid}/')
        log_api_response('test_delete_department', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_pagination(self):
        # Create more Departments to exceed the pagination limit
        for i in range(10):
            Departments.objects.create(
                name=f'Department_{i}',
                code=f'D0{i}',
                description=f'Description_{i}',
                established_at='2023-12-05'
            )

        response = self.client.get(f'{base_url}/departments/')
        log_api_response('test_pagination', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if pagination is working by ensuring that only one page is returned
        res_data = response.data.get("data")
        if 'next' in res_data:
            self.assertIsNotNone(res_data['next'])
        else:
            self.assertIsNone(res_data.get('next'))  # To handle the KeyError gracefully
        self.assertIsNone(res_data['previous'])
        self.assertEqual(len(res_data['results']), 10)  # Assuming the default pagination limit is 10

    def test_search_and_filter(self):
        res_count = Departments.objects.filter(is_deleted=False, code='T01').count()
        response = self.client.get(f'{base_url}/departments/?search=Random')
        log_api_response('test_search_and_filter', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['results']), 1)  # Assuming 'Random' matches only one department

        # Assuming filter_fields are present in your view for code and name
        response = self.client.get(f'{base_url}/departments/?filter_field=code&filter_value=T01')
        log_api_response('test_search_and_filter', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure 'results' key exists in the response data for search/filter
        res_data = response.data.get("data")
        if 'results' in res_data:
            self.assertEqual(len(res_data['results']), res_count)
        else:
            self.fail("Results key not found in response data")  # Handle KeyError gracefully


class ClubsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test_user', password='password', email="test_user@asv.con", user_scope='2'
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.club_1 = Clubs.objects.create(
            name='Demo Club', code='C01', description='Demo Club Description'
        )
        self.club_2 = Clubs.objects.create(
            name='Random Club', code='C02', description='Random Club Description'
        )

    def test_retrieve_club(self):
        response = self.client.get(f'{base_url}/clubs/{self.club_1.uuid}/')
        log_api_response('test_retrieve_club', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_clubs(self):
        response = self.client.get(f'{base_url}/clubs/')
        log_api_response('test_list_clubs', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_club(self):
        data = {
            'name': 'Test Club',
            'code': 'C03',
            'description': 'Test Club Description'
        }
        response = self.client.post(f'{base_url}/clubs/', data=data)
        log_api_response('test_create_club', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_club(self):
        data = {
            'name': 'Updated Club',
            'code': 'C01A',
            'description': 'Updated Club Description'
        }
        response = self.client.put(f'{base_url}/clubs/{self.club_1.uuid}/', data=data)
        log_api_response('test_update_club', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_club(self):
        response = self.client.delete(f'{base_url}/clubs/{self.club_2.uuid}/')
        log_api_response('test_delete_club', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_pagination(self):
        # Create more Clubs to exceed the pagination limit
        for i in range(10):
            Clubs.objects.create(
                name=f'Club_0{i}',
                code=f'C00{i}',
                description=f'Club Description 0{i}'
            )

        response = self.client.get(f'{base_url}/clubs/')
        log_api_response('test_pagination', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = response.data.get("data")
        if 'next' in res_data:
            self.assertIsNotNone(res_data['next'])
        else:
            self.assertIsNone(res_data.get('next'))
        self.assertIsNone(res_data['previous'])
        self.assertEqual(len(res_data['results']), 10)

    def test_search_and_filter(self):
        res_count = Clubs.objects.filter(code='C01').count()
        response = self.client.get(f'{base_url}/clubs/?search=Random')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['results']), 1)

        response = self.client.get(f'{base_url}/clubs/?filter_field=code&filter_value=C01')
        log_api_response('test_search_and_filter', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = response.data.get("data")
        if 'results' in res_data:
            self.assertEqual(len(res_data['results']), res_count)
        else:
            self.fail("Results key not found in response data")

class NoticeBoardsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test_user', password='password', email="test_user@example.com", user_scope='2'
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.notice_board_1 = NoticeBoard.objects.create(
            title='Demo Notice', id_no=1, message='Demo Message'
        )
        self.notice_board_2 = NoticeBoard.objects.create(
            title='Random Notice', id_no=2, message='Random Message'
        )

    def test_retrieve_notice_board(self):
        response = self.client.get(f'{base_url}/noticeboard/{self.notice_board_1.uuid}/')
        self.assertEqual(response.status_code, 200)
        log_api_response('test_retrieve_notice_board', response.status_code, response.data)

    def test_list_notice_boards(self):
        response = self.client.get(f'{base_url}/noticeboard/')
        self.assertEqual(response.status_code, 200)
        log_api_response('test_list_notice_boards', response.status_code, response.data)

    def test_create_notice_board(self):
        data = {
            'title': 'Test Notice',
            'id_no': 3,
            'message': 'Test Message'
        }
        response = self.client.post(f'{base_url}/noticeboard/', data=data)
        self.assertEqual(response.status_code, 201)
        log_api_response('test_create_notice_board', response.status_code, response.data)

    def test_update_notice_board(self):
        data = {
            'title': 'Updated Notice',
            'id_no': 1,
            'message': 'Updated Message'
        }
        response = self.client.put(f'{base_url}/noticeboard/{self.notice_board_1.uuid}/', data=data)
        self.assertEqual(response.status_code, 200)
        log_api_response('test_update_notice_board', response.status_code, response.data)

    def test_delete_notice_board(self):
        response = self.client.delete(f'{base_url}/noticeboard/{self.notice_board_2.uuid}/')
        self.assertEqual(response.status_code, 204)
        log_api_response('test_update_notice_board', response.status_code, response.data)

    def test_pagination(self):
        for i in range(10):
            NoticeBoard.objects.create(
                title=f'Notice_0{i}',
                id_no=i + 10,
                message=f'Message_0{i}'
            )

        response = self.client.get(f'{base_url}/noticeboard/')
        self.assertEqual(response.status_code, 200)
        log_api_response('test_pagination', response.status_code, response.data)

        res_data = response.data.get("data")
        if 'next' in res_data:
            self.assertIsNotNone(res_data['next'])
        else:
            self.assertIsNone(res_data.get('next'))
        self.assertIsNone(res_data['previous'])
        self.assertEqual(len(res_data['results']), 10)
"""