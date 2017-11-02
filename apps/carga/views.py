import csv
from django.shortcuts import render, redirect
from apps.registro.models import *
from apps.carga.models import *
from .forms import DocumentForm

#Funcion de lectura de archivo para separar el archivo csv por estudiantes
def separar_estudiantes(archivo, trimestre_limite="xxx-xxx xxxx"):
    with open(archivo) as f:
        # Lectura del archivo .csv y lo separa por ; y | 
        archivo12 = csv.reader(f, delimiter=';', quotechar='|') 
        listaEstudiantes = []
        expEstudiante = []
        for linea in archivo12:
            if linea[0] == 'Carnet': # Consigue inicio de expediente de un estudiante
                # Agrega expediente a la coleccion de estudiantes
                listaEstudiantes.append(expEstudiante) 
                # Creacion de un nuevo expediente
                expEstudiante = []
                # Anexo  de datos del expediente creado
                expEstudiante.append(linea)
            else:
                expEstudiante.append(linea) 
        listaEstudiantes.append(expEstudiante) # Anexo de ultimo expediente

    # Pasa por alto el primer arreglo vacio creado y realiza lectura de lista completa
    # de los expedientes de estudiantes delimitandolos por un trimestre dado
    return read_csv(listaEstudiantes[1:len(listaEstudiantes)], trimestre_limite)


#Funcion para leer la lista de los estudiantes y va agregando los datos en las base de datos
def read_csv(lista, trimestre_limite):
    estudianteEncontrado = None
    
    #Ciclo para cada estudiante 
    for estudianteEval in lista:
        estudianteEncontrado = None
        inicio = True
        para = True
        cred_aprobados = 0
        
        #Lectura del expediente de cada estudiante
        for linea in estudianteEval:

            #Lectura del carnet de estudiante
            if linea[0] == 'Carnet':
                carnetEst = linea[1] 
                # Verificacion de datos de estudiantes
                estatusEstudiante = Estudiante.objects.filter(carnet=carnetEst)
                if estatusEstudiante.count() != 0:
                    estudianteEncontrado = estatusEstudiante.first()

                # Vericiacion de cohorte correspondiente a estudiante
                cohorteEst = int(carnetEst[0:2])
                estatusCohorte = Cohorte.objects.filter(id=cohorteEst)
                if estatusCohorte.count() != 0: # Existe cohorte en la base de datos
                    cohorteEncontrada = estatusCohorte.first()
                else:                           # No existe cohorte en base de datos. Se crea una
                    cohorteEncontrada = Cohorte(id=cohorteEst)
                    cohorteEncontrada.save()

            # Lectura del nombre del estudiante
            elif linea[0] == 'Nombre:':
                nombreEst = linea[1]
                # Como no se encontro estudiante, se crea su instancia en la base de datos
                if estudianteEncontrado is None:
                    estudianteEncontrado = Estudiante(carnet= carnetEst, nombre= nombreEst, cohorte=cohorteEncontrada)
                    estudianteEncontrado.save()
            
            # Recorrido de asignaturas cursadas por el estudiante
            elif (len(linea[0]) > 8):  # Cabecera con formato: [ Trimestre xx, xxx-xxx xxxx, Nota, Creditos] 
                if inicio:  # Lectura del primer trimestre cursado por el estudiante
                    trimestreEst = linea[1]
                    # Verificacion de datos correspondientes al trimestre
                    estatusTrimestre = Trimestre.objects.filter(id=trimestreEst)
                    if estatusTrimestre.count() != 0:  # Existe trimestre en la base de datos
                        trimestreEncontrado = estatusTrimestre.first()
                    else:                              # No existe trimestre en la base de datos. Se crea uno
                        trimestreEncontrado = Trimestre(id=trimestreEst)
                        trimestreEncontrado.save()

                    # Declaracion de la culminizacion de lectura de primer trimestre cursado por el estudiante
                    inicio = False
                
                else:   # Lectura de los siguientes trimestres en el expediente del estudiante
                    if para == False:  # Detencion de lectura opcional hasta trimestre especificado
                        break
                    
                    elif linea[1] != trimestre_limite: # Vericiacion y carga de todos los trimestres 
                        # Verificacion de datos correspondientes a cada curso presente en la base de datos
                        estatusCursa = Cursa.objects.filter(estudiante=estudianteEncontrado,trimestre=trimestreEncontrado)
                        if estatusCursa.count() != 0:  # Curso presente en la base de datos
                            pass
                        else:  # No existe curso en la base de datos. Se crea
                            cursaEncontrado = Cursa(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado, creditosAprobados=cred_aprobados)
                            cursaEncontrado.save()

                        trimestreEst = linea[1]

                        # Verificacion de datos correspondientes al trimestre
                        estatusTrimestre = Trimestre.objects.filter(id=trimestreEst)
                        if estatusTrimestre.count() != 0:  # Existe trimestre en la base de datos
                            trimestreEncontrado = estatusTrimestre.first()
                        else:                   # No existe trimestre en la base de datos. Se crea uno
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
                if str(linea[2]) == 'R':  # Asignatura fue retirada
                    pass
                elif int(linea[2]) >= 3:  # Asignatura aprobada
                    cred_aprobados += int(linea[3])  #Actualizacion de contador de creditos aprobados
                else:  # Creditos insuficientes para aprobacion de asignatura
                    pass
        # Lectura del ultimo trimestre cursado por el estudiante                        
        # Verificacion de datos correspondientes a cada curso presente en la base de datos
        estatusCursa = Cursa.objects.filter(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado)
        if estatusCursa.count() != 0: # Curso presente en la base de datos
            pass
        else:   # No existe curso en la base de datos. Se crea
            cursaEncontrado = Cursa(estudiante=estudianteEncontrado, trimestre=trimestreEncontrado,
                                    creditosAprobados=cred_aprobados)
            cursaEncontrado.save()

#Controlador que manda vista formulario de carga de archivo para cargar los estudiantes en la base de datos
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