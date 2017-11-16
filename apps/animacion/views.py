from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.registro.models import Estudiante, Cursa
from django.core.cache import cache
import json

# Create your views here.
def obtenerMatriz(cohorte):
    matriz = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    EstudianteDeCohorte = Estudiante.objects.filter(cohorte_id = cohorte)
    print('id cohorte: ' + str(Estudiante.objects.first().cohorte_id))
    #for x in EstudianteDeCohorte:
     #   print(x.cohorte_id)
      #  print(x.carnet)
    cuenta = EstudianteDeCohorte.count()
    numeroTrimestres = 0
    trimestresVistos = []
    listaEstudiantes = []

    if int(cohorte) >= 68:
        apendboy = '19'
    else:
        apendboy = '20'
    cohorte_dada = cohorte

    trimestress = ['Sep-Dic ' + apendboy + str(int(cohorte_dada)), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+1), 'Abr-Jul '+ apendboy + str(int(cohorte_dada)+1), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+1), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+2),
        'Abr-Jul '+ apendboy +str(int(cohorte_dada)+2), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+2), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+3), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+3), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+3),
        'Ene-Mar '+ apendboy + str(int(cohorte_dada)+4), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+4),'Sep-Dic ' + apendboy + str(int(cohorte_dada)+4), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+5), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+5)]


    for estudianteAct in EstudianteDeCohorte:
        print(estudianteAct.nombre)
        CursasEsatudiante = Cursa.objects.filter(estudiante = estudianteAct)
        for cursaAct in CursasEsatudiante:
            trimestreVar = cursaAct.trimestre.id
            print(trimestreVar)
            if trimestreVar in trimestresVistos:
                posicion = trimestress.index(trimestreVar) + 1
                creditos = cursaAct.creditosAprobados
                print(creditos)
                if creditos <= 240:
                    matriz[posicion][int((creditos - 1)/ 16) + 1] += 1
                else:
                    matriz[posicion][16] += 1
            else:
                trimestresVistos.append(trimestreVar)
                temp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                matriz.append(temp)
    print(trimestresVistos)
    print(matriz)

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = matriz[i][j] * 100 / cuenta
    print(matriz)
    return [matriz, trimestresVistos]

@login_required
def animacion(request):
    cache.clear()
    list1 = []
    for i in range(68,118):
        a = str(i)[-2] + str(i)[-1]
        list1.append(a)

    # Crear grafica vacia
    #porcentaje = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    creditos = ['0', '1-16', '17-32', '33-48', '49-64', '65-80', '81-96',
                '97-112', '113-128', '129-144', '145-160', '161-176', '177-192',
                '193-208', '209-224', '225-240', '240+']
    trimestres = ['sept-dic 1', 'ene-mar 1', 'abr-jul 1', 'sept-dic 2', 'ene-mar 2', 'abr-jul 2', 'sept-dic 3', 'ene-mar 3', 'abr-jul 3', 'sept-dic 4',
                 'ene-mar 4', 'abr-jul 4', 'sept-dic 5', 'ene-mar 5', 'abr-jul 5']
    matriz = [[4, 96, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [3, 82, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 60, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 45, 25, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 25, 35, 10, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 15, 25, 25, 10, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 10, 15, 30, 10, 33, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 10, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 10, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 10, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 10, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 10, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 10, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 10, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 10, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
    #for _ in trimestres:
    #    matriz.append(porcentaje)


    data2 = []
    carrera = "Leyenda"
    if request.POST:
        cohorte = request.POST.get('Cohorte')
        carrera = request.POST.get('carrera')
        mls = request.POST.get('mlsPorImagen')

        matriz, trimestres = obtenerMatriz(cohorte)
        matriz = matriz[1:-1]
        cohorte_string = "Cohorte: " + cohorte

    tr = 1
    for j in range(len(matriz)):
        for i in range(17):
            dictdata = {'Porcentaje': matriz[j][i],
                        'Creditos': creditos[i],
                        'Trimestre': trimestres[j],
                        'Vacio': 100,
                        'Leyenda': carrera}

            data2.append(dictdata)

    data2 = json.dumps(data2)

    trimestresReversed = reversed(trimestres)

    return render(request, "animacion.html", {'rangecohorte': list1, 'data2': data2,
                                                'trimestres': trimestres, "trimestresReversed": trimestresReversed, "carrera": carrera})