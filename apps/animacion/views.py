from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.registro.models import Estudiante, Cursa
from django.core.cache import cache
import json

# Create your views here.
def obtenerMatriz(cohorte):
    matriz = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    EstudianteDeCohorte = Estudiante.objects.filter(cohorte_id = cohorte)

    cuenta = EstudianteDeCohorte.count()
    trimestresVistos = []

    if int(cohorte) >= 68:
        apendboy = '19'
    else:
        apendboy = '20'
    cohorte_dada = cohorte

    trimestress = ['Sep-Dic ' + apendboy + str(int(cohorte_dada)), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+1), 'Abr-Jul '+ apendboy + str(int(cohorte_dada)+1), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+1), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+2),
        'Abr-Jul '+ apendboy +str(int(cohorte_dada)+2), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+2), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+3), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+3), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+3),
        'Ene-Mar '+ apendboy + str(int(cohorte_dada)+4), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+4),'Sep-Dic ' + apendboy + str(int(cohorte_dada)+4), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+5), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+5)]

    for estudianteAct in EstudianteDeCohorte:
        # Filtramos los cursa de un estudiante
        CursasEsatudiante = Cursa.objects.filter(estudiante = estudianteAct)
        for cursaAct in CursasEsatudiante:
            # identificamos el trimestre de ese cursa
            trimestreVar = cursaAct.trimestre.id
            if trimestreVar in trimestresVistos:
                pass
            else:
                trimestresVistos.append(trimestreVar)
                temp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                matriz.append(temp)

    for estudianteAct in EstudianteDeCohorte:
        # Filtramos los cursa de un estudiante
        CursasEsatudiante = Cursa.objects.filter(estudiante = estudianteAct)
        for cursaAct in CursasEsatudiante:
            # identificamos el trimestre de ese cursa
            trimestreVar = cursaAct.trimestre.id
            if trimestreVar in trimestresVistos:
                posicion = trimestress.index(trimestreVar) + 1 # +1 por el trim 0
                creditos = cursaAct.creditosAprobados
                if creditos <= 240:
                    if creditos != 0:
                        matriz[posicion][int((creditos - 1)/ 16) + 1] += 1
                    else:
                        matriz[posicion][0] += 1
                else:
                    matriz[posicion][16] += 1

            else:
                trimestresVistos.append(trimestreVar)
                temp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                matriz.append(temp)

    for i in matriz:
        print(i)

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = matriz[i][j] * 100 / cuenta


    return [matriz, trimestresVistos]

@login_required
def animacion(request):
    cache.clear()
    list1 = []
    for i in range(68,118):
        a = str(i)[-2] + str(i)[-1]
        list1.append(a)

    # Crear grafica vacia
    porcentaje = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    creditos = ['0', '1-16', '17-32', '33-48', '49-64', '65-80', '81-96',
                '97-112', '113-128', '129-144', '145-160', '161-176', '177-192',
                '193-208', '209-224', '225-240', '240+']
    trimestres = ['Sept-Dic Año 1', 'Ene-Mar Año 1', 'Abr-Jul Año 1', 'Sept-Dic Año 2', 'Ene-Mar Año 2', 'Abr-Jul Año 2', 'Sept-Dic Año 3', 'Ene-Mar Año 3', 'Abr-Jul Año 3', 'Sept-Dic Año 4',
                 'Ene-Mar Año 4', 'Abr-Jul Año 4', 'Sept-Dic Año 5', 'Ene-Mar Año 5', 'Abr-Jul Año 5']

    matriz = []
    for _ in trimestres:
        matriz.append(porcentaje)


    data2 = []
    carrera = "Leyenda"
    cohorte = "XX"
    mls = 3000
    msg = None
    msg2 = "Ejemplo"
    if request.POST:
        cohorte = request.POST.get('Cohorte')
        carrera = request.POST.get('carrera')
        mls = request.POST.get('mlsPorImagen')

        nestudiantes = Estudiante.objects.filter(cohorte = cohorte).count()
        if nestudiantes > 0:
            matriz, trimestres = obtenerMatriz(cohorte)
            matriz = matriz[1:]
            msg2 = "Resultado"
        else:
            msg = "No hay datos suficientes para esa cohorte."

    for j in range(len(matriz)):
        for i in range(17):

            dictdata = {'( % ) Porcentaje': matriz[j][i],
                        'Créditos': creditos[i],
                        'Trimestre': trimestres[j],
                        'Vacío': 100,
                        'Leyenda': carrera}

            data2.append(dictdata)

    data2 = json.dumps(data2)

    trimestresReversed = reversed(trimestres)

    return render(request, "animacion.html", {'rangecohorte': list1, 'data2': data2, 'trimestres': trimestres, "trimestresReversed": trimestresReversed,
                                              "carrera": carrera, 'cohorte' : cohorte, 'mls' : mls, 'msg' : msg, 'msg2' : msg2, 'rangemls' : range(500, 3001, 500)})