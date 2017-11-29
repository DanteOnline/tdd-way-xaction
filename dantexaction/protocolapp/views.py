from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import StatusResponse, ProtocolEncoder


class JsonStatusResponse(JsonResponse):
    pass


class Http401(HttpResponse):
    def __init__(self):
        super().__init__('401 Unauthorized', status=401)