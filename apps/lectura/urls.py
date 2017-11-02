from django.conf.urls import url, include
from django.contrib import admin
from apps.registro.views import RegistroUsuario, welcome

#Con estos urls se controlan los enlaces desde lectura
urlpatterns = [
    url(r'^$', RegistroUsuario.as_view()),
]