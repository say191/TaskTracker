from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(
            email='admin@gmail.com',
            fio='admin',
            position='admin',
            phone='+79111111111',
            password='111',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        self.client.force_authenticate(user=self.admin)

    def test_create_user(self):
        """Test for creating user"""
        data = {
            "email": "1@gmail.com",
            "fio": "1",
            "position": "engineer",
            "phone": "+71111111111",
            "password": "111"
        }
        response = self.client.post(
            '/users/create/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEquals(
            response.json(),
            {
                "email": "1@gmail.com",
                "password": "111",
                "fio": "1",
                "position": "engineer",
                "phone": "+71111111111",
                "task_count": 0,
                "tasks": []
            }
        )

    def test_users_list(self):
        """Test for display all users"""
        response = self.client.get(
            '/users/'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            [{
                'email': 'admin@gmail.com',
                'password': '111',
                'fio': 'admin',
                'position': 'admin',
                'phone': '+79111111111',
                'task_count': 0,
                'tasks': []
            }]
        )

    def test_user_get(self):
        """Test for display one chosen user"""
        response = self.client.get(
            '/users/17/'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {
                'email': 'admin@gmail.com',
                'password': '111',
                'fio': 'admin',
                'position': 'admin',
                'phone': '+79111111111',
                'task_count': 0,
                'tasks': []
            }
        )

    def test_update_user(self):
        """Test for updating one chosen user"""
        data = {
            "email": "2@gmail.com",
            "fio": "2",
            "position": "2",
            "phone": "+78888888888",
            "password": "111"
                }
        User.objects.create(
            email='3@gmail.com',
            fio='3',
            position='3',
            phone='+77777777777',
            password='111'
        )
        response = self.client.patch(
            '/users/update/16/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'email': '2@gmail.com',
             'password': '111',
             'fio': '2',
             'position': '2',
             'phone': '+78888888888',
             'task_count': 0,
             'tasks': []
             }
        )

    def test_delete_user(self):
        """Test for deleting one chosen user"""
        User.objects.create(
            email='test@gmail.com',
            fio='Test Testov',
            position='engineer',
            phone='+79999999999',
            password='111'
        )
        response = self.client.delete(
            '/users/delete/14/'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
