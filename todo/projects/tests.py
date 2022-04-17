from unittest import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APISimpleTestCase, APITestCase
from mixer.backend.django import mixer
from django.contrib.auth.models import User

from .views import ProjectModelViewSet, TodoModelViewSet
from .models import Project, Todo
from users.models import User


class TestProjectViewSet(TestCase):

    def setUp(self) -> None:
        self.data = {'first_name': 'Иван', 'last_name': 'Иванов', 'password': '123456', 'email': 'test2@mail.ru'}
        self.data_put = {'first_name': 'Петр', 'last_name': 'Петров', 'password': '123456', 'email': 'test3@mail.ru'}
        self.url = '/api/users/'
        self.admin = User.objects.create_superuser('admin', 'drf@django.local', 'rest')
        self.password = 'rest'

    def test_get_list_project(self):
        factory = APIRequestFactory()
        request = factory.get(self.url)
        view = ProjectModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project_guest(self):
        factory = APIRequestFactory()
        request = factory.post(self.url, {'name': 'Тест', 'repository_url': 'https://test.com/',
                                          'users': [self.admin.id]})
        view = ProjectModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_admin(self):
        factory = APIRequestFactory()
        request = factory.post(self.url, {'name': 'Тест', 'repository_url': 'https://test.com/',
                                          'users': [self.admin.id]})
        force_authenticate(request, self.admin)
        view = ProjectModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail(self):
        client = APIClient()
        project = Project.objects.create(name='Тест', repository_url='https://test.com/')
        project.users.add(self.admin.id)
        project.save()
        response = client.get(f'{self.url}{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_guest(self):
        client = APIClient()
        project = Project.objects.create(name='Тест', repository_url='https://test.com//')
        project.users.add(self.admin.id)
        project.save()
        response = client.put(f'{self.url}{project.id}/', name='Тест', repository_url='https://test.com/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_admin(self):
        client = APIClient()
        project = Project.objects.create(name='Тест', repository_url='https://test.com/')
        project.users.add(self.admin.id)
        project.save()
        client.login(username=self.admin.username, password=self.password)
        response = client.put(f'{self.url}{project.id}/',
                              {'name': 'Тест2', 'repository_url': 'https://test.com/',
                               'users': [self.admin.id]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project = Project.objects.get(id=project.id)
        self.assertEqual(project.name, 'Тест2')
        self.assertEqual(project.repository_url, 'https://test.com/')
        client.logout()

    def tearDown(self) -> None:
        pass


class TestTodoViewSet(APITestCase):

    def setUp(self) -> None:
        self.data = {'first_name': 'Иван', 'last_name': 'Иванов', 'password': '123456', 'email': 'test2@mail.ru'}
        self.data_put = {'first_name': 'Петр', 'last_name': 'Петров', 'password': '123456', 'email': 'test2@mail.ru'}
        self.url = '/api/users/'
        self.admin = User.objects.create_superuser('admin', 'drf@django.local', 'rest')
        self.password = 'rest'

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_admin(self):
        project = Project.objects.create(name='Тест', repository_url='https:/test.com/')
        todo = Todo.objects.create(title='Тестовая заметка', text='Заметка', project=project,
                                   user=self.admin)
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.put(f'{self.url}{todo.id}/',
                                   {'title': 'Тестовая заметка 2', 'text': 'Заметка 2',
                                    'project': project.id, 'user': self.admin.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo = Todo.objects.get(id=todo.id)
        self.assertEqual(todo.title, 'Тестовая заметка 2')
        self.assertEqual(todo.text, 'Заметка 2')
        self.client.logout()

    def test_edit_admin_with_mixer(self):
        project = mixer.blend(Project, name='Тест')
        todo = Todo.objects.create(title='Тестовая заметка', text='Заметка', project=project,
                                   user=self.admin)
        self.client.login(username=self.admin.username, password=self.password)  # логинимся
        response = self.client.put(f'{self.url}{todo.id}/',
                                   {'title': 'Тестовая заметка 2', 'text': 'Заметка 2',
                                    'project': project.id, 'user': self.admin.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo = Todo.objects.get(id=todo.id)
        self.assertEqual(todo.title, 'Тестовая заметка 2')
        self.assertEqual(todo.text, 'Заметка 2')
        self.assertEqual(project.name, 'Тест')
        self.client.logout()
