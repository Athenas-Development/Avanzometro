from django.conf.urls import url, include
from django.contrib import admin
from apps.registro.views import RegistroUsuario, welcome, instantanea


urlpatterns = [
    url(r'^$', RegistroUsuario.as_view()),
    url(r'^welcome', welcome),
]