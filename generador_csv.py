import random
import datetime

class EstudianteG():
	def __init__(self, cohorte, super=False, carnets_no_validos=[]):
		self.arreglo_acumulado = []
		self.largo = 0
		self.acumulado = 0
		self.nombre = ""
		self.cohorte = str(cohorte)
		if cohorte < 10:
			self.cohorte = "0" + str(cohorte)
		self.carnet = ""
		self.carnets_no_validos = carnets_no_validos
		self.anio = str(2000 + cohorte)
		self.string = ""
		self.super = super

		if cohorte >= 68:
			self.anio = str(1900 + cohorte)

		self.generar_todo()


	def __str__(self):
		return self.string

	def generar_todo(self):
		self.generar_nombre()
		self.generar_carnet()
		self.generar_notas()
		self.generar_string()

	def generar_nombre(self):
		last_names = ["Jacquemin", "Ellery", "Eck", "Abadie", "Asper", "Danielson", "Goebel",
		 "Estevez", "Lamy", "Okelley", "Grumbles", "Rau", "Noah", "Wisdom", "Sokoloski",
		 "Pedigo", "Ramsier", "Sechrest", "Northington", "Rinaldo"]

		first_names = ["Jim", "Emile", "Ernest", "Alejandro", "Abdul", "Darrel", "Granville",
		 "Ethan", "Lou", "Osvaldo", "Gordon", "Ronny", "Ned", "Willie", "Silas",
		 "Patricia", "Rodrick", "Sonny", "Nestor", "Robert"]

		self.nombre = "%s %s" % (random.choice(first_names), random.choice(last_names))

	def generar_carnet(self):
		body = random.randint(10000, 11999)
		self.carnet =  "%s-%d" % (self.cohorte, body)
		if self.carnet in self.carnets_no_validos:
			self.generar_carnet()

	def generar_notas(self):
		for i in range(0,15):
			eleccion = random.randint(1, 200)
			if self.super:
				eleccion = random.randint(150, 200)
			verano = 0

			if (i + 1)%3 == 0 and eleccion >= 120:
				verano = random.randint(2,8)

			if eleccion <= 2:
				if self.largo == 0:
					self.generar_notas()
				else:
					break

			elif eleccion <= 12:
				if self.largo == 0:
					self.generar_notas()
					break
				else:
					self.arreglo_acumulado.append(self.acumulado)
					self.largo += 1

			elif eleccion <= 20:
				self.acumulado += (random.randint(2,7) + verano)
				self.arreglo_acumulado.append(self.acumulado)
				self.largo += 1

			elif eleccion <= 190:
				self.acumulado += (random.randint(8,16) + verano)
				self.arreglo_acumulado.append(self.acumulado)
				self.largo += 1

			else:
				self.acumulado += (random.randint(16, 20) + verano)
				self.arreglo_acumulado.append(self.acumulado)
				self.largo += 1

	def generar_string(self):
		self.string = "%s;%s;%s" % (self.carnet, self.anio, self.nombre)

		for i in range(0,15):
			if self.largo > i:
				self.string += ";" + str(self.arreglo_acumulado[i])
			else:
				self.string += ";"


def generar_cohorte_05_09(n):

	string = "Carnet;Cohorte;Nombre;1ro_1;1ro_2;1ro_3;2do_1;2do_2;2do_3;3ro_1;3ro_2;3ro_3;4to_1;4to_2;4to_3;5to_1;5to_2;5to_3"

	for i in range(105, 110):
		ch = i
		if ch >= 100:
			ch = ch - 100

		cnv = []
		super = False
		for i in range(0,n):
			string += "\n"

			if i > 7*n/8:
				super = True

			x = EstudianteG(ch, super, cnv)
			cnv.append(x.carnet)
			string += x.string

	f = open("test.csv", 'w')
	f.write(string)
	f.close()

generar_cohorte_05_09(10)
