import csv
from django.shortcuts import render, redirect
from apps.registro.models import *
from apps.carga.models import *
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def comprobar_entero(dato):
    print(dato)
    try:
        if int(dato) >= 0:
            return True
        else:
            print('notas negativas encontradas')
            return False
    except ValueError:
        print('strings desconocidos encontrados')
        return False


# Funcion de lectura de archivo para separar el archivo csv por estudiantes
def separar_estudiantes(archivo, request, trimestre_limite="xxx-xxx xxxx"):
    with open(archivo) as f:
        # Lectura del archivo .csv y lo separa por ; y |
        archivo12 = csv.reader(f, delimiter=';', quotechar='|')
        listaEstudiantes = []
        expEstudiante = []
        for linea in archivo12:
            if linea[0] == 'Carnet':  # Consigue inicio de expediente de un estudiante
                # Agrega expediente a la coleccion de estudiantes
                listaEstudiantes.append(expEstudiante)
                # Creacion de un nuevo expediente
                expEstudiante = []
                # Anexo  de datos del expediente creado
                expEstudiante.append(linea)
            else:
                expEstudiante.append(linea)
        listaEstudiantes.append(expEstudiante)  # Anexo de ultimo expediente

    # Pasa por alto el primer arreglo vacio creado y realiza lectura de lista completa
    # de los expedientes de estudiantes delimitandolos por un trimestre dado
    return read_csv(listaEstudiantes[1:len(listaEstudiantes)], trimestre_limite, request)


def separar_estudiantes_V2(archivo, request, trimestre_limite="xxx-xxx xxxx"):
    with open(archivo) as f:
        # Lectura del archivo .csv y lo separa por ; y |
        archivo1 = csv.reader(f, delimiter=',', quotechar='|')
        listaEstudiantes = []
        expEstudiantes = []
        for linea in archivo1:
            if linea[0] == 'Carnet':
                cohorte = 0
                carnet = 0
                nombre = ''
            else:
                expEstudiantes = []
                lineaEst = []
                cohorte = linea[1]
                carnet = linea[0]
                nombre = linea[2]

                trimestres = ['Sep-Dic ' + str(int(cohorte)), 'Ene-Mar ' + str(int(cohorte) + 1),
                              'Abr-Jul ' + str(int(cohorte) + 1), 'Sep-Dic ' + str(int(cohorte) + 1),
                              'Ene-Mar ' + str(int(cohorte) + 2),
                              'Abr-Jul ' + str(int(cohorte) + 2), 'Sep-Dic ' + str(int(cohorte) + 2),
                              'Ene-Mar ' + str(int(cohorte) + 3), 'Abr-Jul ' + str(int(cohorte) + 3),
                              'Sep-Dic ' + str(int(cohorte) + 3),
                              'Ene-Mar ' + str(int(cohorte) + 4), 'Abr-Jul ' + str(int(cohorte) + 4),
                              'Sep-Dic ' + str(int(cohorte) + 4), 'Ene-Mar ' + str(int(cohorte) + 5),
                              'Abr-Jul ' + str(int(cohorte) + 5)]

                lineaEst.append('Carnet')
                lineaEst.append(carnet)
                lineaEst.append(cohorte)
                lineaEst.append('')
                expEstudiantes.append(lineaEst)

                lineaEst = []
                lineaEst.append('Nombre:')
                lineaEst.append(nombre)
                lineaEst.append('')
                lineaEst.append('')
                expEstudiantes.append(lineaEst)

                trim = 0
                for x in (linea[3:len(linea)]):
                    lineaEst = []
                    if comprobar_entero(x):
                        nota = x
                        lineaEst.append('Trimestre ' + str(trim + 1))
                        lineaEst.append(trimestres[trim])
                        lineaEst.append('Nota')
                        lineaEst.append('Creditos')
                        expEstudiantes.append(lineaEst)

                        lineaEst = []
                        lineaEst.append('codAsig')
                        lineaEst.append('nombAsig')
                        lineaEst.append('5')
                        lineaEst.append(nota)
                        expEstudiantes.append(lineaEst)

                        trim += 1
                    elif x == '':
                        break
                    else:
                        messages.error(request, 'Datos del documentos invalidos.')
                        return
                print(trim)
                listaEstudiantes.append(expEstudiantes)
                print(listaEstudiantes)

    return read_csv(listaEstudiantes, trimestre_limite, request)


# Funcion para leer la lista de los estudiantes y va agregando los datos en las base de datos
def read_csv(lista, trimestre_limite, request):
    estudianteEncontrado = None

    # Ciclo para cada estudiante
    for estudianteEval in lista:
        estudianteEncontrado = None
        inicio = True
        para = True
        cred_aprobados = 0

        # Lectura del expediente de cada estudiante
        for linea in estudianteEval:

            # Lectura del carnet de estudiante
            if linea[0] == 'Carnet':
                carnetEst = linea[1]
                # Verificacion de datos de estudiantes
                estatusEstudiante = Estudiante.objects.filter(carnet=carnetEst)
                if estatusEstudiante.count() != 0:
                    estudianteEncontrado = estatusEstudiante.first()

                # Vericiacion de cohorte correspondiente a estudiante
                cohorteEst = int(carnetEst[0:2])
                estatusCohorte = Cohorte.objects.filter(id=cohorteEst)
                if estatusCohorte.count() != 0:  # Existe cohorte en la base de datos
                    cohorteEncontrada = estatusCohorte.first()
                else:  # No existe cohorte en base de datos. Se crea una
                    cohorteEncontrada = Cohorte(id=cohorteEst)
                    cohorteEncontrada.save()

            # Lectura del nombre del estudiante
            elif linea[0] == 'Nombre:':
                nombreEst = linea[1]
                # Como no se encontro estudiante, se crea su instancia en la base de datos
                if estudianteEncontrado is None:
                    estudianteEncontrado = Estudiante(carnet=carnetEst, nombre=nombreEst, cohorte=cohorteEncontrada)
                    estudianteEncontrado.save()

            # Recorrido de asignaturas cursadas por el estudiante
            elif (len(linea[0]) > 8):  # Cabecera con formato: [ Trimestre xx, xxx-xxx xxxx, Nota, Creditos]
                if inicio:  # Lectura del primer trimestre cursado por el estudiante
                    trimestreEst = linea[1]
                    # Verificacion de datos correspondientes al trimestre
                    estatusTrimestre = Trimestre.objects.filter(id=trimestreEst)
                    if estatusTrimestre.count() != 0:  # Existe trimestre en la base de datos
                        trimestreEncontrado = estatusTrimestre.first()
                    else:  # No existe trimestre en la base de datos. Se crea uno
                        trimestreEncontrado = Trimestre(id=trimestreEst)
                        trimestreEncontrado.save()

                    # Declaracion de la culminizacion de lectura de primer trimestre cursado por el estudiante
                    inicio = False

                else:  # Lectura de los siguientes trimestres en el expediente del estudiante
                    if para == False:  # Detencion de lectura opcional hasta trimestre especificado
                        break

                    elif linea[1] != trimestre_limite:  # Vericiacion y carga de todos los trimestres
                        # Verificacion de datos correspondientes a cada curso presente en la base de datos
                        estatusCursa = Cursa.objects.filter(estudiante=estudianteEncontrado,
                                                            trimestre=trimestreEncontrado)
                        if estatusCursa.count() != 0:  # Curso presente en la base de datos
                            pass
                        else:  # No existe curso en la base de datos. Se crea
                            cursaEncontrado = Cursa(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado,
                                                    creditosAprobados=cred_aprobados)
                            cursaEncontrado.save()

                        trimestreEst = linea[1]

                        # Verificacion de datos correspondientes al trimestre
                        estatusTrimestre = Trimestre.objects.filter(id=trimestreEst)
                        if estatusTrimestre.count() != 0:  # Existe trimestre en la base de datos
                            trimestreEncontrado = estatusTrimestre.first()
                        else:  # No existe trimestre en la base de datos. Se crea uno
                            trimestreEncontrado = Trimestre(id=trimestreEst)
                            trimestreEncontrado.save()

                        # Reinicio de creditos aprobados por estudiante
                        cred_aprobados = 0
                    elif linea[1] == trimestre_limite and para:
                        trimestreEst = linea[1]
                        cred_aprobados = 0
                        para = False
            # Lectura de todas las asignaturas cursadas en ese trimestre por el estudiante
            else:
                if int(linea[3]) >= 0:
                    if str(linea[2]) == 'R' or int(linea[2]) == 2 or int(
                            linea[2]) == 1:  # Asignatura fue retirada o no aprobada
                        pass
                    elif int(linea[2]) >= 3:  # Asignatura aprobada
                        cred_aprobados += int(linea[3])  # Actualizacion de contador de creditos aprobados
                    else:  # Nota Invalida.
                        messages.error(request, 'Datos del documentos invalidos.')
                        return
                else:  # Cantidad de Creditos Invalida.
                    messages.error(request, 'Datos del documentos invalidos.')
                    return

        # Lectura del ultimo trimestre cursado por el estudiante
        # Verificacion de datos correspondientes a cada curso presente en la base de datos
        estatusCursa = Cursa.objects.filter(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado)
        if estatusCursa.count() != 0:  # Curso presente en la base de datos
            pass
        else:  # No existe curso en la base de datos. Se crea
            cursaEncontrado = Cursa(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado,
                                    creditosAprobados=cred_aprobados)
            cursaEncontrado.save()

        messages.success(request, 'Archivo cargado exitosamente.')


# Controlador que manda vista formulario de carga de archivo para cargar los estudiantes en la base de datos
@login_required
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

        separar_estudiantes_V2(filetoload, request)

    msg = None
    if list(messages.get_messages(request)) != 0:
        msg = list(messages.get_messages(request))[-1]

    return render(request, 'cargaArchivo.html', {'form': form, 'msg': msg})




