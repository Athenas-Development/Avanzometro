from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView
from apps.registro.forms import RegistroForm
from django.http import HttpResponse
 
# Create your views here.

class RegistroUsuario(CreateView):
    model = User
    template_name = 'registrarUsuario.html'
    form_class = RegistroForm
    success_url = '/'

def welcome(request):
    return redirect('registro')


def instantanea(request):
    list1=[]
    for i in range(68,118):
        a= str(i)[-2] + str(i)[-1]
        list1.append(a)

    return render(request, "instantanea.html", {'rangeano': range(1968,2018), 'rangecohorte': list1})