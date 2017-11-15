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
    porcentaje = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    creditos = ['0', '1-16', '17-32', '33-48', '49-64', '65-80', '81-96',
                '97-112', '113-128', '129-144', '145-160', '161-176', '177-192',
                '193-208', '209-224', '225-240', '240+']
    trimestres = ['sept-dic 1', 'ene-mar 1', 'abr-jul 1', 'sept-dic 2', 'ene-mar 2', 'abr-jul 2', 'sept-dic 3', 'ene-mar 3', 'abr-jul 3', 'sept-dic 4',
                 'ene-mar 4', 'abr-jul 4', 'sept-dic 5', 'ene-mar 5', 'abr-jul 5']
    matriz = []
    for _ in trimestres:
        matriz.append(porcentaje)
    data2 = []
    print('Aqui')
    if request.POST:
        print('ENTRO')
        trimestre = request.POST.get('Trimestre')
        anio = request.POST.get('anio')
        cohorte = request.POST.get('Cohorte')
        carrera = request.POST.get('carrera')
        trimestre = trimestre + " " + anio
        print(cohorte)
        print(trimestre)

        total_de_estudiantes = Estudiante.objects.filter(cohorte_id=cohorte).count()
        print(str(total_de_estudiantes) + '-----estudiantes de la cohorte-----' + str(cohorte))
        matriz, trimestres = obtenerMatriz(cohorte)
        matriz = matriz[1:-1]
        cohorte_string = "Cohorte: " + cohorte
        trimestre_string = "Trimestre: " + trimestre
    print('Alla')
    for j in range(len(trimestres)):
        for i in range(17):
            dictdata = {'Porcentaje': matriz[j][i],
                        'Creditos': creditos[i],
                        'Trimestre': trimestres[j],
                        'Vacio': 100}

            data2.append(dictdata)

    data2 = json.dumps(data2)

    trimestresReversed = reversed(trimestres)

    return render(request, "advanced_matrix.html", {'rangeano': range(1968,2018), 'rangecohorte': list1, 'data2': data2,
                                                'trimestres': trimestres, "trimestresReversed": trimestresReversed})