from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.contrib import auth
from protocolapp.models import ProtocolEncoder, StatusResponse
from protocolapp.decorators import post_required
from .forms import RegistrationForm


def is_auth(request):
    return JsonResponse({'result': request.user.is_authenticated})


@post_required
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)

    result = StatusResponse(StatusResponse.OK)
    if user:
        auth.login(request, user)
    else:
        result.errors = True
    return JsonResponse(result, encoder=ProtocolEncoder, safe=False)


@post_required
def logout(request):
    auth.logout(request)
    result = StatusResponse(StatusResponse.OK)
    return JsonResponse(result, encoder=ProtocolEncoder, safe=False)


@post_required
def registration(request):

    form = RegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        result = StatusResponse(StatusResponse.OK)
        return JsonResponse(result, encoder=ProtocolEncoder, safe=False)
    else:
        result = StatusResponse(StatusResponse.OK, errors=True, alert=form.errors)
        return JsonResponse(result, encoder=ProtocolEncoder, safe=False)
