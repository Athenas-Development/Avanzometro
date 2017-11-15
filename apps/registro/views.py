from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView
from apps.registro.forms import RegistroForm
from django.http import HttpResponse
from apps.registro.grafica import crear_grafica, getcreditsbytrandct
from django.contrib.auth.decorators import login_required
from apps.registro.models import Estudiante
from django.core.cache import cache
import json

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
    cache.clear()
    list1 = []
    for i in range(68,118):
        a = str(i)[-2] + str(i)[-1]
        list1.append(a)

    # Crear grafica vacia
    porcentaje = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    creditos = ['0', '1-16', '17-32', '33-48', '49-64', '65-80', '81-96',
                '97-112', '113-128', '129-144', '145-160', '161-176', '177-192',
                '193-208', '209-224', '225-240', '240+']
    data2 = []

    if request.POST:
        trimestre = request.POST.get('Trimestre')
        anio = request.POST.get('anio')
        cohorte = request.POST.get('Cohorte')
        carrera = request.POST.get('carrera')
        trimestre = trimestre + " " + anio
        print(cohorte)
        print(trimestre)

        total_de_estudiantes = Estudiante.objects.filter(cohorte_id = cohorte).count()
        porcentaje = getcreditsbytrandct(trimestre, cohorte)
        cohorte_string = "Cohorte: " + cohorte
        trimestre_string = "Trimestre: " + trimestre

        grafica = crear_grafica(cohorte_string, carrera, trimestre_string, total_de_estudiantes, lista)

    for i in range(17):
        dictdata = {'porcentaje': porcentaje[i],
                    'creditos': creditos[i]}

        data2.append(dictdata)
    data2 = json.dumps(data2)

    return render(request, "instantanea.html", {'rangeano': range(1968,2018), 'rangecohorte': list1, 'data2': data2})