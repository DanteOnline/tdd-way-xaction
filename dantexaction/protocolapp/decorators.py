from django.http import Http404
from protocolapp.views import Http401


def login_required(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return Http401()

    return inner


def post_required(func):
    def inner(request, *args, **kwargs):
        if request.method == 'POST':
            return func(request, *args, **kwargs)
        else:
            raise Http404

    return inner
