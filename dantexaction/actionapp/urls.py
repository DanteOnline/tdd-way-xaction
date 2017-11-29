from django.conf.urls import url
from .views import action_view

urlpatterns = [
    url(r'^$', action_view, name='actions'),
]