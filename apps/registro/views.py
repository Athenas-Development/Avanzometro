from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView
from apps.registro.forms import RegistroForm
from django.http import HttpResponse
from apps.registro.grafica import crear_grafica, getcreditsbytrandct
from django.contrib.auth.decorators import login_required
from apps.registro.models import Estudiante

# Create your views here.

#Controladores de la vista de registro

#Envia a la pagina principal despues de un registro exitoso
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
        trimestre = trimestre + " " + anio
        print(cohorte)
        print(trimestre)

        total_de_estudiantes = Estudiante.objects.filter(cohorte_id = cohorte).count()
        lista = getcreditsbytrandct(trimestre, cohorte)
        cohorte_string = "Cohorte " + cohorte
        trimestre_string = "Trimestre " + trimestre

        crear_grafica(cohorte_string, carrera, trimestre_string, total_de_estudiantes, lista)

    return render(request, "instantanea.html", {'rangeano': range(1968,2018), 'rangecohorte': list1})