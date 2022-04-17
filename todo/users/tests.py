from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APISimpleTestCase, APITestCase

from .views import UserModelViewSet
from .models import User


class TestUserViewSet(TestCase):

    def setUp(self) -> None:
        self.data = {'first_name': 'Иван', 'last_name': 'Иванов', 'password': '123456', 'email': 'test2@mail.ru'}
        self.data_put = {'first_name': 'Петр', 'last_name': 'Петров', 'password': '123456', 'email': 'test3@mail.ru'}
        self.url = '/api/users/'
        self.admin = User.objects.create_superuser('admin', 'drf@django.local', 'rest')

    def test_get_list(self):
        # создать объект класса APIRequestFactory
        factory = APIRequestFactory()
        # определяем адрес и метод отправки запроса
        request = factory.get(self.url)
        # указываем тип запроса будет передан UserModelViewSet
        view = UserModelViewSet.as_view({'get': 'list'})
        # передаем во view и получаем ответ
        response = view(request)
        # проверяем код ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_guest(self):
        factory = APIRequestFactory()
        request = factory.post(self.url, self.data, format='json')
        view = UserModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_admin(self):
        factory = APIRequestFactory()
        request = factory.post(self.url, self.data, format='json')
        force_authenticate(request, self.admin)
        view = UserModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail(self):
        client = APIClient()
        # Создать user через ORM для проверки детализации
        user = User.objects.create(**self.data)
        response = client.get(f'{self.url}{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_guest(self):
        client = APIClient()
        user = User.objects.create(**self.data)
        response = client.put(f'{self.url}{user.id}/', self.data_put)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_admin(self):
        client = APIClient()
        user = User.objects.create(**self.data)
        client.login(username='admin', password='rest')
        response = client.put(f'{self.url}{user.id}/', self.data_put)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=user.id)
        self.assertEqual(user.username, 'test_user2')
        self.assertEqual(user.email, 'test2@mail.ru')
        client.logout()

    def tearDown(self) -> None:
        pass


class TestMath(APISimpleTestCase):
    def test_sqrt(self):
        import math
        response = math.sqrt(4)
        self.assertEqual(response, 2)
