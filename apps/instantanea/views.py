from django.shortcuts import render
from apps.registro.models import Estudiante, Cursa
from django.contrib.auth.decorators import login_required
import json
# Create your views here.

def getcreditsbytrandct(trimestre_dado, cohorte_dada):
	EstudiantesDeCohorteCT = Estudiante.objects.filter(cohorte_id=cohorte_dada)
	print(Estudiante.objects.first().cohorte_id)

	listadeCursaporEstdecohortect = []
	for estudianteCT in EstudiantesDeCohorteCT:
		listadeCursaporEstdecohortect.append(Cursa.objects.filter(estudiante=estudianteCT))

	if int(cohorte_dada) >= 68:
		apendboy = '19'
	else:
		apendboy = '20'

	trimestres = ['Sep-Dic ' + apendboy + str(int(cohorte_dada)),
				  'Ene-Mar ' + apendboy + str(int(cohorte_dada) + 1),
				  'Abr-Jul ' + apendboy + str(int(cohorte_dada) + 1),
				  'Sep-Dic ' + apendboy + str(int(cohorte_dada) + 1),
				  'Ene-Mar ' + apendboy + str(int(cohorte_dada) + 2),
				  'Abr-Jul ' + apendboy + str(int(cohorte_dada) + 2),
				  'Sep-Dic ' + apendboy + str(int(cohorte_dada) + 2),
				  'Ene-Mar ' + apendboy + str(int(cohorte_dada) + 3),
				  'Abr-Jul ' + apendboy + str(int(cohorte_dada) + 3),
				  'Sep-Dic ' + apendboy + str(int(cohorte_dada) + 3),
				  'Ene-Mar ' + apendboy + str(int(cohorte_dada) + 4),
				  'Abr-Jul ' + apendboy + str(int(cohorte_dada) + 4),
				  'Sep-Dic ' + apendboy + str(int(cohorte_dada) + 4),
				  'Ene-Mar ' + apendboy + str(int(cohorte_dada) + 5),
				  'Abr-Jul ' + apendboy + str(int(cohorte_dada) + 5)]

	lista = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for cursa_est in listadeCursaporEstdecohortect:
		creditos = 0
		for i in trimestres:
			if cursa_est.filter(trimestre_id=i).count() > 0:
				creditos += cursa_est.filter(trimestre_id=i).first().creditosAprobados

			if i == trimestre_dado:
				break
		if creditos == 0:
			lista[0] += 1
		else:
			if creditos <= 240:
				lista[int((creditos - 1) / 16) + 1] += 1
			else:
				lista[-1] += 1
	print(lista)

	return lista

@login_required
def instantanea(request):
	porcentaje = [5, 15, 20, 15, 30, 14, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	creditos = ['0', '1-16', '17-32', '33-48', '49-64', '65-80', '81-96',
				'97-112', '113-128', '129-144', '145-160', '161-176', '177-192',
				'193-208', '209-224', '225-240', '240+']
	data2 = []
	for i in range(17):
		dictdata = {'porcentaje': porcentaje[i],
					'creditos': creditos[i]}

		data2.append(dictdata)

	print(data2)
	data2 = json.dumps(data2)

	return render(request, "instantanea.html", {'data2':data2})

