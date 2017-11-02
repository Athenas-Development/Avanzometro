from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.views import logout_then_login
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.

#Controladores de las vistas de login

#envia al inicio de la pagina
def index(request):
    return render(request, "index.html")

#Deslogea el usuario de l apagina y devuelve a la pagina principal
@login_required
def logout (request):

    logout_then_login(request)