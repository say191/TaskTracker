from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from tasks.models import Task
from django.contrib.auth.models import Group


class TaskTestCase(APITestCase):
    def setUp(self):
        self.taskgiver = User.objects.create(
            email='test@gmail.com',
            fio='test',
            position='test',
            phone='+79111111111',
            password='111',
            is_active=True
        )
        self.admin = User.objects.create(
            email='me@gmail.com',
            fio='me',
            position='me',
            phone='++70000000000',
            password='111',
            is_active=True,
            is_superuser=True,
            is_staff=True
        )
        group, created = Group.objects.get_or_create(name='Taskgiver')
        self.taskgiver.groups.add(group)

    def test_create_task(self):
        """Test for creating task"""
        self.client.force_authenticate(user=self.taskgiver)
        data = {
            "title": "haha",
            "description": "haha",
            "term": "1 day"
        }
        response = self.client.post(
            '/tasks/create/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEquals(
            response.json(),
            {'id': 1,
             'title': 'haha',
             'description': 'haha',
             'owner': 'test',
             'executor': 'not_yet_appointed',
             'term': '1 day',
             'status': 'created',
             'parent_task': None
             }
        )

    def test_tasks_list(self):
        """Test for display all tasks"""
        self.client.force_authenticate(user=self.admin)
        Task.objects.create(
            title="haha",
            description="haha",
            term="1 day"
        )
        response = self.client.get(
            '/tasks/'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            [
                {'id': 4,
                 'title': 'haha',
                 'description': 'haha',
                 'owner': None,
                 'executor': 'not_yet_appointed',
                 'term': '1 day',
                 'status': 'created',
                 'parent_task': None
                 }
            ]
        )

    def test_task_get(self):
        """Test for display one chosen task"""
        self.client.force_authenticate(user=self.admin)
        Task.objects.create(
            title="haha",
            description="haha",
            term="1 day",
            owner="admin"
        )
        response = self.client.get(
            '/tasks/3/'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'id': 3,
             'title': 'haha',
             'description': 'haha',
             'owner': 'admin',
             'executor': 'not_yet_appointed',
             'term': '1 day',
             'status': 'created',
             'parent_task': None
             }
        )

    def test_update_task(self):
        """Test for updating one chosen task"""
        self.client.force_authenticate(user=self.admin)
        data = {
            "title": "qwe",
            "description": "qwe",
            "term": "1 day",
            "owner": "admin"
        }
        Task.objects.create(
            title="haha",
            description="haha",
            term="1 day",
            owner="admin"
        )
        response = self.client.patch(
            '/tasks/update/5/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'id': 5,
             'title': 'qwe',
             'description': 'qwe',
             'owner': 'admin',
             'executor': 'not_yet_appointed',
             'term': '1 day',
             'status': 'created',
             'parent_task': None
             }
        )

    def test_delete_task(self):
        """Test for deleting one chosen task"""
        self.client.force_authenticate(user=self.admin)
        Task.objects.create(
            title="haha",
            description="haha",
            term="1 day",
            owner="admin"
        )
        response = self.client.delete(
            '/tasks/delete/2/'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
