from django.db import models
from dantejcoder.coder import DanteJcoder


class ProtocolEncoder(DanteJcoder):
    def default(self, obj):
        if isinstance(obj, StatusResponse):
            result = {}
            result['status'] = obj.status
            if obj.errors:
                result['errors'] = obj.errors
            if obj.alert:
                result['alert'] = obj.alert
            return result
        else:
            return super().default(obj)


class StatusResponse:
    OK = 'OK'

    def __init__(self, status, errors=False, alert=None):
        self.status = status
        self.errors = errors
        self.alert = alert
