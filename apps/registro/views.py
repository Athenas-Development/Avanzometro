from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView
from apps.registro.forms import RegistroForm
from django.http import HttpResponse
 
# Create your views here.

class RegistroUsuario(CreateView):
    model = User
    template_name = 'registrarUsuario.html'
    form_class = RegistroForm
    success_url = '/index'

def welcome():
	return HttpResponse("Welcome!")