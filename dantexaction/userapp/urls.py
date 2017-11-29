from django.conf.urls import url
from django.contrib import admin
from userapp.views import login, is_auth, logout, registration

urlpatterns = [
    url(r'login/$', login, name='login'),
    url(r'is_auth/$', is_auth, name='is_auth'),
    url(r'logout/$', logout, name='logout'),
    url(r'registration/$', registration, name='registration')
]

