import json
from django.test import TestCase
from .models import StatusResponse, ProtocolEncoder


class TestStatusResponse(TestCase):

    def test_init(self):
        s = StatusResponse(StatusResponse.OK)
        self.assertEqual(s.status, 'OK')
        s = StatusResponse(StatusResponse.OK, errors=True)
        self.assertEqual(s.errors, True)
        s = StatusResponse(StatusResponse.OK, alert='test alert')
        self.assertEqual(s.alert, 'test alert')

    def test_encode(self):
        s = StatusResponse(StatusResponse.OK, errors=True, alert='test alert')
        result = json.dumps(s, cls=ProtocolEncoder)
        self.assertJSONEqual('{"status": "OK", "errors": true, "alert": "test alert"}', result)


class TestHttp401(TestCase):
    pass