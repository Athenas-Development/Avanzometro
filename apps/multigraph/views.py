from django.shortcuts import render
from apps.registro.models import Estudiante, Cursa
from django.core.cache import cache
import json
from apps.multigraph.granularizador import granularizador

n = 0
def obtenerMatriz(cohortes = None, rango = 16):
	jsonDict = []
	# Creacion del arreglo de limites de Creditos.
	# categoriaCreditos =  ['0']
	# lim = 0
	# bar = 1
	# while rango*bar <= 240:
	# 	categoriaCreditos.append(str(lim + 1) + '-' + str(rango * bar))
	# 	bar += 1
	# 	lim += rango
	# categoriaCreditos.append(str(rango * (bar-1)) + '+')

	categoriaCreditos = granularizador(rango)

	if cohortes is None or cohortes == []:
		porcentaje = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		creditos = ['0', '1-16', '17-32', '33-48', '49-64', '65-80', '81-96',
					'97-112', '113-128', '129-144', '145-160', '161-176', '177-192',
					'193-208', '209-224', '225-240', '240+']
		trimestres = ['Sept-Dic Año 1', 'Ene-Mar Año 1', 'Abr-Jul Año 1', 'Sept-Dic Año 2', 'Ene-Mar Año 2',
					  'Abr-Jul Año 2', 'Sept-Dic Año 3', 'Ene-Mar Año 3', 'Abr-Jul Año 3', 'Sept-Dic Año 4',
					  'Ene-Mar Año 4', 'Abr-Jul Año 4', 'Sept-Dic Año 5', 'Ene-Mar Año 5', 'Abr-Jul Año 5']

		matriz = []
		for _ in trimestres:
			matriz.append(porcentaje)

		jsonDict = []
		for j in range(len(matriz)):
			for i in range(17):
				dictdata = {'( % ) Porcentaje': matriz[j][i],
							'Créditos': creditos[i],
							'Trimestre': trimestres[j],
							'Vacío': 100,
							'Cohorte': 'XX'}

				jsonDict.append(dictdata)
		return jsonDict, categoriaCreditos

	for cohorte in cohortes:
		temp = [0] * len(categoriaCreditos)
		matriz = []
		matriz.append(temp)

		EstudianteDeCohorte = Estudiante.objects.filter(cohorte_id = cohorte)

		cuenta = EstudianteDeCohorte.count()
		trimestresVistos = []

		if int(cohorte) >= 68:
			anio = '19'
		else:
			anio = '20'

		cohorte_dada = cohorte

		trimestre = ['Sep-Dic ' + anio + str(int(cohorte_dada)),
					   'Ene-Mar ' + anio + str(int(cohorte_dada) + 1),
					   'Abr-Jul ' + anio + str(int(cohorte_dada) + 1),
					   'Sep-Dic ' + anio + str(int(cohorte_dada) + 1),
					   'Ene-Mar ' + anio + str(int(cohorte_dada) + 2),
					   'Abr-Jul ' + anio + str(int(cohorte_dada) + 2),
					   'Sep-Dic ' + anio + str(int(cohorte_dada) + 2),
					   'Ene-Mar ' + anio + str(int(cohorte_dada) + 3),
					   'Abr-Jul ' + anio + str(int(cohorte_dada) + 3),
					   'Sep-Dic ' + anio + str(int(cohorte_dada) + 3),
					   'Ene-Mar ' + anio + str(int(cohorte_dada) + 4),
					   'Abr-Jul ' + anio + str(int(cohorte_dada) + 4),
					   'Sep-Dic ' + anio + str(int(cohorte_dada) + 4),
					   'Ene-Mar ' + anio + str(int(cohorte_dada) + 5),
					   'Abr-Jul ' + anio + str(int(cohorte_dada) + 5)]

		# categoriaCreditos = ['0', '1-16', '17-32', '33-48', '49-64', '65-80', '81-96',
		# 			'97-112', '113-128', '129-144', '145-160', '161-176', '177-192',
		# 			'193-208', '209-224', '225-240', '240+']

		for estudianteAct in EstudianteDeCohorte:
			# Filtramos los cursa de un estudiante
			cursaEstudiante = Cursa.objects.filter(estudiante = estudianteAct)
			for cursaAct in cursaEstudiante:
				# identificamos el trimestre de ese cursa
				trimestreVar = cursaAct.trimestre.id
				if trimestreVar in trimestresVistos:
					pass
				else:
					trimestresVistos.append(trimestreVar)
					temp = [0] * len(categoriaCreditos)
					matriz.append(temp)

		for estudianteAct in EstudianteDeCohorte:
			# Filtramos los cursa de un estudiante
			cursaEstudiante = Cursa.objects.filter(estudiante = estudianteAct)
			for cursaAct in cursaEstudiante:
				# identificamos el trimestre de ese cursa
				trimestreVar = cursaAct.trimestre.id
				if trimestreVar in trimestresVistos:
					posicion = trimestre.index(trimestreVar) + 1 # +1 por el trim 0
					creditos = cursaAct.creditosAprobados
					if creditos <= 240:
						if creditos != 0:
							matriz[posicion][int((creditos - 1)/ rango) + 1] += 1
						else:
							matriz[posicion][0] += 1
					else:
						matriz[posicion][-1] += 1

				else:
					trimestresVistos.append(trimestreVar)
					temp = [0] * len(categoriaCreditos)
					matriz.append(temp)

		for i in range(len(matriz)):
			for j in range(len(matriz[i])):
				matriz[i][j] = matriz[i][j] * 100 / cuenta

		matriz = matriz[1:]

		for j in range(len(matriz)):
			t = 'Año: ' + str(j//3 + 1) + ' Trimestre: ' + str(j%3 + 1)
			for i in range(len(categoriaCreditos)):
				dictdata = {'( % ) Porcentaje': matriz[j][i],
							'Créditos': categoriaCreditos[i],
							'Trimestre': t,
							'Vacío': "",
							'Cohorte': "Cohorte " + str(cohorte)}

				jsonDict.append(dictdata)

	return jsonDict, categoriaCreditos


def multigrafica(request):
	cache.clear()
	list1 = []
	for i in range(68, 118):
		a = str(i)[-2] + str(i)[-1]
		list1.append(a)

	# PARA PROBAR AQUI PONEN CUALES TRIMESTRES QUIEREN VER!!!
	ncohortes = 0
	cohortes = []
	mls = 3000
	carrera = 'XXXXXXX'
	rango = 16
	tipo = 'barra'
	msg2 = 'Ejemplo'
	msg = None
	msg3 = None

	if request.POST:
		ncohortes = request.POST.get('ncohortes')
		cohortes_elegidas = []

		for i in range(1, int(ncohortes)+1):
			cohorte1 = request.POST.get('Cohorte'+str(i))
			if cohorte1 in cohortes_elegidas and not(cohorte1 is None):
				msg3 = "Se eligio la misma cohorte varias veces, se mostrará este una única vez."
			else:
				cohortes_elegidas.append(cohorte1)
				nestudiantes = Estudiante.objects.filter(cohorte=cohorte1).count()
				if cohorte1 != None:
					if nestudiantes > 0:
						cohortes.append(cohorte1)
						msg2 = 'Resultado'
					else:
						msg = "No hay datos suficientes para la cohorte " + cohorte1 + '.'
						msg2 = 'Ejemplo'
						break
				else:
					cohortes.append(cohorte1)

		carrera = request.POST.get('carrera')
		mls = request.POST.get('mlsPorImagen')
		rango = request.POST.get('rango')
		tipo = request.POST.get('tipo')


	if None in cohortes:
		cohortes = None
		rango = 16
		carrera = 'XXXXXXX'
		mls = 3000

	tipo = tipo == 'linea'

	rango = int(rango)

	jsondata, orden = obtenerMatriz(cohortes, rango)

	jsondata = json.dumps(jsondata)

	carreras = ["Ingeniería Eléctrica", "Ingeniería Mecánica",
				"Ingeniería Química", "Ingeniería Electrónica",
				"Ingeniería de Materiales", "Ingeniería de la Computación",
				"Ingeniería Geofísica", "Ingeniería de Producción",
				"Ingeniería de Mantenimiento", "Ingeniería de Telecomunicaciones",
				"Arquitectura", "Urbanismo", "Licenciatura en Química",
				"Licenciatura en Matemáticas", "Licenciatura en Física",
				"Licenciatura en Biología", "Licenciatura en Comercio Internacional",
				"Licenciatura en Gestión de la Hospitalidad", "Tecnología Eléctrica",
				"Tecnología Electrónica", "Tecnología Mecánica",
				"Mantenimiento Aeronáutico", "Administración del Turismo",
				"Administración Hotelera", "Administración del Transporte",
				"Organización Empresarial", "Comercio Exterior", "Administración Aduanera"]

	DIVISORES = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 21, 26, 34, 40, 48, 60, 80, 120, 240]

	return render(request, "multigraph.html",{'data2': jsondata, 'mls': mls, 'rangecohorte' : list1, 'carrera' : carrera,
											  'rangemls' : range(500, 3001, 500), 'ncohortes' : range(1, int(ncohortes)+1),
											  'nc' : int(ncohortes), 'orden': orden, 'r': len(orden), 'tipo' : tipo,
											  'carreras' : carreras, 'msg' : msg, 'msg2' : msg2, 'msg3': msg3,
											  'div' : DIVISORES})