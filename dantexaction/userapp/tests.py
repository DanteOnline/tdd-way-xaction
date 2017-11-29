from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client


class TestUserManagement(TestCase):
    def setUp(self):
        self.crawler = Client()
        self.user = User.objects.create_user('dante', 'test@test.com', 'dante123456')

    def test_is_authenticate(self):
        # специальная страница сервиса
        response = self.crawler.get('/users/is_auth/')
        self.assertJSONEqual('{"result": false}', response.content.decode())
        self.crawler.login(username='dante', password='dante123456')
        # специальная страница сервиса
        response = self.crawler.get('/users/is_auth/')
        self.assertJSONEqual('{"result": true}', response.content.decode())

    def test_login(self):
        # пользователь есть в базе
        response = self.crawler.post('/users/login/', {'username': 'dante', 'password': 'dante123456'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual('{ "status": "OK"}', response.content.decode())
        # надо проверить что пользователь вошел
        # специальная страница сервиса
        response = self.crawler.get('/users/is_auth/')
        self.assertJSONEqual('{"result": true}', response.content.decode())
        # запрос методом get
        response = self.crawler.get('/users/login/', {'username': 'dante', 'password': 'dante123456'})
        self.assertEqual(response.status_code, 404)
        # пользователя нет в базе или неверный логин или пароль
        response = self.crawler.post('/users/login/', {'username': 'dante', 'password': 'dante1'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual('{ "status": "OK", "errors": true }', response.content.decode())
        # что если он уже вошел и хочет зайти снова
        # всё ок) ничего не надо изменять походу
        response = self.crawler.post('/users/login/', {'username': 'dante', 'password': 'dante123456'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual('{ "status": "OK"}', response.content.decode())

    def test_logout(self):
        # стадартное применене
        # логиним пользователя
        self.crawler.login(username='dante', password='dante123456')
        # разлогиниваем
        response = self.crawler.post('/users/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual('{ "status": "OK"}', response.content.decode())
        # гет запрос
        response = self.crawler.get('/users/logout/')
        self.assertEqual(response.status_code, 404)

    def test_registration(self):
        # гет запрос
        response = self.crawler.get('/users/registration/')
        self.assertEqual(response.status_code, 404)
        # пост запрос
        response = self.crawler.post('/users/registration/', data={'username': 'Newuser', 'password1': 'dante123456',
                                                                   'password2': 'dante123456',
                                                                   'email': 'test@test.com'})
        self.assertEqual(response.status_code, 200)
        # кривые параметры
        response = self.crawler.post('/users/registration/', data={'opa': 'na'})
        self.assertEqual(response.status_code, 200)
        # там есть описание ошибок
        self.assertTrue(b'alert' in response.content)
