from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView
from apps.registro.forms import RegistroForm
from django.http import HttpResponse
from apps.registro.grafica import crear_grafica
from django.contrib.auth.decorators import login_required
 
# Create your views here.

class RegistroUsuario(CreateView):
    model = User
    template_name = 'registrarUsuario.html'
    form_class = RegistroForm
    success_url = '/'

@login_required
def instantanea(request):
    list1 = []
    for i in range(68,118):
        a = str(i)[-2] + str(i)[-1]
        list1.append(a)

    if request.POST:
        trimestre = request.POST.get('Trimestre')
        anio = request.POST.get('anio')
        cohorte = request.POST.get('Cohorte')
        carrera = request.POST.get('carrera')
        cohorte = cohorte + " " + anio

        total_de_estudiantes = 20
        lista = [1, 0, 3, 4, 1, 1, 2, 3, 1, 4, 0, 0, 0, 0, 0, 0]

        crear_grafica(cohorte, carrera, trimestre, total_de_estudiantes, lista)

    return render(request, "instantanea.html", {'rangeano': range(1968,2018), 'rangecohorte': list1})