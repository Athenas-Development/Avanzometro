import random
def generador():
	nombres = ['Rafael', 'Andres', 'Carlos', 'Adolfo', 'Salvador', 'Erick','Jose','Donato', 'Miguel', 'Clemente']
	apellidos = ['Cisneros', 'Corro', 'Perez', 'Feo', 'Canedo', 'Flejan', 'Bracuto', 'Buelvas', 'Parra', 'Rincon']
	carrera = 'Ingenieria de Computacion'
	notas = [1,2,3,4,5,'R']
	cohorte = str(random.randint(1968,2017))
	cohorteCarnet = str(cohorte[2])+str(cohorte[3])
	cantidadTrimestres = random.randint(0,15)
	trimestres = ['Sep-Dic ' + str(int(cohorte)), 'Ene-Mar '+ str(int(cohorte)+1), 'Abr-Jul '+ str(int(cohorte)+1), 'Sep-Dic ' + str(int(cohorte)+1), 'Ene-Mar '+ str(int(cohorte)+2), 
	'Abr-Jul '+str(int(cohorte)+2), 'Sep-Dic ' + str(int(cohorte)+2), 'Ene-Mar '+ str(int(cohorte)+3), 'Abr-Jul '+str(int(cohorte)+3), 'Sep-Dic ' + str(int(cohorte)+3), 
	'Ene-Mar '+ str(int(cohorte)+4), 'Abr-Jul '+str(int(cohorte)+4),'Sep-Dic ' + str(int(cohorte)+4), 'Ene-Mar '+ str(int(cohorte)+5), 'Abr-Jul '+str(int(cohorte)+5)]

	carnetsAsignados = []
	with open('prueba.csv','w') as f:
		for i in range(0,10):
			carnetinvalido = True
			while carnetinvalido:
				carnet = 'Carnet;' + cohorteCarnet + '-1' + str(random.randint(0,1)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))+';;'
				if not(carnet in carnetsAsignados):
					carnetinvalido = False
					carnetsAsignados.append(carnet)

			f.write(carnet + '\n')
			nombre = 'Nombre:;'+nombres[random.randint(0,9)]+' '+nombres[random.randint(0,9)]+' '+apellidos[random.randint(0,9)]+' '+apellidos[random.randint(0,9)]+';;'
			f.write(nombre + '\n')
			
			for j in range (1,cantidadTrimestres+1):
				trimestre = 'Trimestre 0' + str(j) + ';' + trimestres[j-1]+';Nota;Creditos'
				f.write(trimestre + '\n')
				for k in range(0,4):
					materia = 'cibla;nombre;' + str(notas[random.randint(0,5)]) + ';' + '4'
					f.write(materia + '\n')

generador()