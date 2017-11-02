import csv
from django.shortcuts import render, redirect
from apps.registro.models import *
from apps.carga.models import *
from .forms import DocumentForm


# Create your views here.

#Funcion para separar el archivo csv por estudiantes
def separar_estudiantes(archivo, trimestre_limite="xxx-xxx xxxx"):
    with open(archivo) as f:
        archivo12 = csv.reader(f, delimiter=';', quotechar='|')
        listaEstudiantes = []
        expEstudiante = []
        for linea in archivo12:
            if linea[0] == 'Carnet':
                listaEstudiantes.append(expEstudiante)
                expEstudiante = []
                expEstudiante.append(linea)
            else:
                expEstudiante.append(linea)
        listaEstudiantes.append(expEstudiante)

    return read_csv(listaEstudiantes[1:len(listaEstudiantes)], trimestre_limite)


#Funcion para leer la lista de los estudiantes y va agregando los datos en las base ed datos
def read_csv(lista, trimestre_limite):
    estudianteEncontrado = None
    #Para cada estudiante
    for estudianteEval in lista:
        estudianteEncontrado = None
        inicio = True
        para = True
        cred_aprobados = 0
        for linea in estudianteEval:
            #print(linea)
            if linea[0] == 'Carnet':
                carnetEst = linea[1]
                estatusEstudiante = Estudiante.objects.filter(carnet=carnetEst)
                if estatusEstudiante.count() != 0:
                    estudianteEncontrado = estatusEstudiante.first()
                    print('ESTUDIANTE ENCONTRADO')
                print('----carnetEst: ' + carnetEst)

                cohorteEst = int(carnetEst[0:2])
                estatusCohorte = Cohorte.objects.filter(id=cohorteEst)
                if estatusCohorte.count() != 0:
                    cohorteEncontrada = estatusCohorte.first()
                else:
                    cohorteEncontrada = Cohorte(id=cohorteEst)
                    cohorteEncontrada.save()

                print('----cohorteEst: ' + str(cohorteEst))
            elif linea[0] == 'Nombre:':
                nombreEst = linea[1]
                print('----nombreEst: '+nombreEst)
                if estudianteEncontrado is None:
                    estudianteEncontrado = Estudiante(carnet= carnetEst, nombre= nombreEst, cohorte=cohorteEncontrada)
                    estudianteEncontrado.save()
            elif (len(linea[0]) > 8):
                if inicio:
                    trimestreEst = linea[1]

                    estatusTrimestre = Trimestre.objects.filter(id=trimestreEst)
                    if estatusTrimestre.count() != 0:
                        print('TRIMESTRE ENCONTRADO')
                        trimestreEncontrado = estatusTrimestre.first()
                    else:
                        trimestreEncontrado = Trimestre(id=trimestreEst)
                        trimestreEncontrado.save()
                        print('TRIMESTRE CREADO: ' + trimestreEst)
                    print('----trimestreEst: '+trimestreEst)

                    inicio = False
                else:
                    if para == False:
                        print('PARATEEEEEEEEEE')
                        break
                    elif linea[1] != trimestre_limite:

                        estatusCursa = Cursa.objects.filter(estudiante=estudianteEncontrado,trimestre=trimestreEncontrado)
                        if estatusCursa.count() != 0:
                            print('CURSA ENCONTRADO')
                        else:
                            cursaEncontrado = Cursa(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado, creditosAprobados=cred_aprobados)
                            cursaEncontrado.save()
                            #print('CURSA CREADO: ' + nombreEst + ' - ' + trimestreEst)

                        print('=========  ' + carnetEst + ' --curso-- ' + trimestreEst + ' --cred_aprobados-- ' + str(
                            cred_aprobados))

                        trimestreEst = linea[1]

                        estatusTrimestre = Trimestre.objects.filter(id=trimestreEst)
                        if estatusTrimestre.count() != 0:
                            print('TRIMESTRE ENCONTRADO')
                            trimestreEncontrado = estatusTrimestre.first()
                            print(trimestreEncontrado.id)
                        else:
                            trimestreEncontrado = Trimestre(id=trimestreEst)
                            trimestreEncontrado.save()
                            print('TRIMESTRE CREADO: ' + trimestreEst)


                        #cursaEncontrado = Cursa(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado, creditosAprobados=cred_aprobados)
                        #cursaEncontrado.save()
                        #print('=========  ' + carnetEst + ' --curso-- ' + trimestreEst + ' --cred_aprobados-- ' + str(cred_aprobados))
                        #trimestreEst = linea[1]


                        print('----trimestreEst: '+trimestreEst)
                        cred_aprobados = 0
                    elif linea[1] == trimestre_limite and para:
                        #print('=========  ' + carnetEst + ' --curso-- ' + trimestreEst + ' --cred_aprobados-- ' + str(cred_aprobados))
                        trimestreEst = linea[1]
                        print('----trimestreEst: '+trimestreEst)
                        cred_aprobados = 0
                        para = False
            else:
                if str(linea[2]) == 'R':
                    print('Retirada')
                elif int(linea[2]) >= 3:
                    cred_aprobados += int(linea[3])
                    print('Paso')
                else:
                    print('Raspo')

        estatusCursa = Cursa.objects.filter(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado)
        if estatusCursa.count() != 0:
            print('CURSA ENCONTRADO')
        else:
            cursaEncontrado = Cursa(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado,
                                    creditosAprobados=cred_aprobados)
            cursaEncontrado.save()
            print('CURSA CREADO: ' + nombreEst + ' - ' + trimestreEst)
        #cursaEncontrado = Cursa(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado, creditosAprobados=cred_aprobados)
        #cursaEncontrado.save()
        print('=========  ' + carnetEst + ' --curso-- ' + trimestreEst + ' --cred_aprobados-- ' + str(cred_aprobados))
    print('------------------------------------------')

def cargarArchivo(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('form.html')

    else:
        form = DocumentForm()

    if documento.objects.count() != 0:
        filetoload = str(documento.objects.order_by().reverse().first().documento)

        separar_estudiantes(filetoload)

    return render(request, 'cargaArchivo.html', {'form':form})