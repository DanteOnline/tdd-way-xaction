import json
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from .models import Action
from dantejcoder.coder import DanteJcoder


class TestAction(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('dante', 'test@test.com', 'dante123456')
        self.user.save()
        self.a1 = Action.objects.create(name='А', user=self.user)
        self.a1_json = '{"id": 1, "name": "А", "is_done": false}'
        self.b1_json = '{"id": 2, "name": "Б", "is_done": false}'
        self.a2 = Action.objects.create(name='Б', user=self.user)
        self.crawler = Client()

    def tearDown(self):
        self.a1.delete()
        self.a2.delete()

    def test_init(self):
        # действия
        self.assertEqual(self.a1.name, 'А')
        self.assertEqual(self.a2.name, 'Б')

    def test_str(self):
        # действия
        self.assertEqual(str(self.a1), 'А')

    def test_queryset_eq(self):
        m1 = Action.objects.all()
        m2 = Action.objects.all()
        # квэрисеты сравнить между собой нельзя
        self.assertFalse(m1 == m2)

    def test_list_eq(self):
        l1 = [self.a1, self.a2]
        l2 = [self.a1, self.a2]
        self.assertTrue(l1 == l2)
        l1 = [self.a2, self.a1]
        l2 = [self.a1, self.a2]
        self.assertFalse(l1 == l2)

    def test_ord(self):
        a3 = Action.objects.create(name='С', is_done=True, user=self.user)
        a4 = Action.objects.create(name='Д', is_done=True, user=self.user)

        # сортировка действий
        actions = Action.objects.all()
        self.assertEqual(actions[0].name, 'С')
        self.assertEqual(actions[1].name, 'Д')
        self.assertEqual(actions[2].name, 'А')

    def test_to_json(self):
        ajson = json.dumps(self.a1, cls=DanteJcoder)
        self.assertJSONEqual(ajson, self.a1_json)

    def test_crud(self):
        # пользователь не зашел
        response = self.crawler.get('/actions/')
        self.assertEqual(response.status_code, 401)
        # пользователь зашел
        self.crawler.login(username='dante', password='dante123456')
        response = self.crawler.get('/actions/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual('[{}, {}]'.format(self.a1_json, self.b1_json),
                             response.content.decode())
        # добавляем пользователя
        response = self.crawler.post('/actions/', {'name': 'new'})
        self.assertEqual(response.status_code, 200)
        # результат должен быть без ошибок
        self.assertJSONEqual(response.content.decode(), '{"status": "OK"}')
        # в базе должен появиться новый объект
        response = self.crawler.get('/actions/')
        user3_json = '{"id": 3, "name": "new", "is_done": false}'
        self.assertJSONEqual(
            '[{}, {}, {}]'.format(self.a1_json, self.b1_json, user3_json),
            response.content.decode())
        # изменение пользователя
        # не тот объект
        response = self.crawler.put('/actions/', {'id': 1000})
        self.assertEqual(response.status_code, 404)
        response = self.crawler.put('/actions/', {'id': 1, 'name': 'АА'})
        self.assertEqual(response.status_code, 200)
        response = self.crawler.get('/actions/')
        self.assertJSONEqual(
            '[{}, {}, {}]'.format('{"id": 1, "name": "АА", "is_done": false}', self.b1_json, user3_json),
            response.content.decode())
        # удаление пользователя
        response = self.crawler.delete('/actions/', {'id': 1})
        self.assertEqual(response.status_code, 200)
        response = self.crawler.get('/actions/')
        self.assertJSONEqual(
            '[{}, {}]'.format(self.b1_json, user3_json), response.content.decode())
