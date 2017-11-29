from django.shortcuts import get_object_or_404
from django.http import JsonResponse, QueryDict
from protocolapp.decorators import login_required
from protocolapp.models import StatusResponse, ProtocolEncoder
from dantejcoder.coder import DanteJcoder
from .models import Action
from .forms import ActionForm
import json


def parse_response_body(body):
    text = body.decode()
    # print(text)
    replaced_text = text.replace("'", '"').replace(' ', '')
    # print(replaced_text)
    result = json.loads(replaced_text)
    # print(result)
    return result


def save_form(form, request):
    if form.is_valid():
        newaction = form.save(commit=False)
        newaction.user = request.user
        newaction.save()
        result = StatusResponse(StatusResponse.OK)
        return JsonResponse(result, encoder=ProtocolEncoder, safe=False)
    else:
        result = StatusResponse(StatusResponse.OK, errors=True, alert=form.errors)
        return JsonResponse(result, encoder=ProtocolEncoder, safe=False)


def get_action_from_body(body):
    data = parse_response_body(body)
    ID = 'id'
    if ID in data:
        action_id = data[ID]
        action = get_object_or_404(Action, id=action_id)
    else:
        action = None
    return action, data


@login_required
def action_view(request):
    if request.method == 'GET':
        actions = Action.objects.filter(user=request.user)
        return JsonResponse(actions, encoder=DanteJcoder, safe=False)
    elif request.method == 'POST':
        # print(request.body)
        form = ActionForm(request.POST)
        return save_form(form, request)
    elif request.method == 'PUT':
        # получаем данные из put тестер скорее всего неправильно шлет данные
        action, data = get_action_from_body(request.body)
        form = ActionForm(data, instance=action)
        return save_form(form, request)
    elif request.method == 'DELETE':
        action, data = get_action_from_body(request.body)
        action.delete()
        result = StatusResponse(StatusResponse.OK)
        return JsonResponse(result, encoder=ProtocolEncoder, safe=False)
