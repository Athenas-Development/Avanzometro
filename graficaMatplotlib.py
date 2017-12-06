# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from matplotlib.axes import Axes
import matplotlib.patches as patches 
import matplotlib.patches


class sliderModificado(Slider):

	def __init__(self, ax, label, valmin=0, valmax=10, valinit=0, valfmt='%1d', **kwargs):
		
		#Imprimir kwargs y args
		'''
		for key, value in kwargs.iteritems():
 			print "%s = %s" % (key, value)

 		for arg in args:
			print "another arg through *args :", arg

		'''
		self.facecolor= kwargs.get('facecolor','white')
		self.activecolor = kwargs.pop('activecolor','red')
		self.fontsize = kwargs.pop('fontsize', 14)

		super(sliderModificado, self).__init__(ax, label, valmin, valmax, valinit, valfmt,**kwargs)

		#if dragging:
			#self.connect_event('motion_notify_event', self._update)
		self.poly.set_visible(False)
		self.vline.set_visible(False)
		self.arreglo_de_rectangulos = []
		cadena = ["1ro", "2do", "3ro", "4to", "5to", "6to", "7to", "8vo", "9no", "10mo", "11vo", "12vo", "13vo", "14vo", "15vo"]

		for i in range(valmax):
			facecolor = self.facecolor
			r  = matplotlib.patches.Rectangle((float(i)/valmax, 0), float(1)/valmax, 1, 
							transform=ax.transAxes, facecolor=facecolor)
			ax.add_artist(r)
			self.arreglo_de_rectangulos.append(r)

			ax.text(float(i)/valmax+0.5/valmax, 0.5, str(cadena[i]),  
					ha="center", va="center", transform=self.ax.transAxes,
					fontsize=self.fontsize)
		self.valtext.set_visible(False)

	def _update(self, event):
		super(sliderModificado, self)._update(event)
		i = int(self.val)
		print("------------>" +str(i))
		if 1 < i >=self.valmax :
			return
		self._colorize(i)

	def _colorize(self, i):
		for j in range(self.valmax):
			self.arreglo_de_rectangulos[j].set_facecolor(self.facecolor)
		self.arreglo_de_rectangulos[i].set_facecolor(self.activecolor)

class graficaDeBarras:
	def __init__(self, carrera, cohorte, matriz, total_de_estudiantes, total_de_creditos_carrera, velocidad, cantidad_de_trimestres):

		self.carrera = carrera
		self.cohorte = cohorte
		self.matriz = matriz
		self.total_de_estudiantes = total_de_estudiantes
		self.total_de_creditos_carrera = total_de_creditos_carrera
		self.titulo = self.cohorte +'\n'
		self.datos, self.creditos = self.establecerEjes()
		self.y = self.establecerPorcentaje(matriz[0])
		self.cantidad_de_trimestres = cantidad_de_trimestres
		self.velocidad = velocidad

		#Establecer la figura
		self.fig = plt.figure(figsize = (22,12), dpi= 60, frameon=True)
		self.ax = self.fig.add_subplot(111)
		plt.subplots_adjust(left=0.10, bottom=0.25)

		#Establecer la barra
		idsx = np.arange(len(self.creditos))
		idsy = np.arange(len(self.datos))
		self.barra = plt.bar(idsx, self.y, width=0.5, color='c', align="center", label=carrera)
		plt.axis([0, 0, -10, 10])

		#Establecer etiquetas, labels

		plt.yticks(idsy, self.datos, fontsize=14)
		plt.xticks(idsx, self.creditos, fontsize=14) #labels del eje horizontal
		plt.xlabel(u"Créditos", fontsize=18, labelpad=15)
		plt.ylabel("% de Estudiantes", fontsize=18)
		plt.title(self.titulo, fontsize=20)
		plt.legend(bbox_to_anchor =(0,0,1,1), fontsize=15, loc=2, shadow=True) #loc= "lower left"
		self.titulo_medio = plt.text(4, 8, "Desarrollado por Athenas Development", fontsize=30)

		#Establecer limites de la barra
		plt.ylim(0, 11)
		plt.xlim(-1, 16)

		#Establecer animacion
		self.contador_frames = 0
		self.animacion = animation.FuncAnimation(self.fig, self.actualizar, repeat=False, blit=False, interval=self.ajustarVelocidad(),
													init_func=self.inicio)

        #Varible que controlara la animacion
		self.animacionCorriendo = True
		
        #plt.savefig("grafica.png", dpi=100)

	def inicio(self):

		altura_y = self.establecerPorcentaje(self.matriz[0])
		for rect, z in zip(self.barra, altura_y):
			rect.set_height(z)

		self.titulo_medio.set_text(self.cohorte)

		return self.barra

	def establecerPorcentaje(self, lista):
		y = []

		for i in lista:
			y.append(((float(i*100))/self.total_de_estudiantes)/10)

		return y	

	def establecerEjes(self):

		datos =['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
		creditos = []

		contador = 0
		string = ""
		creditos.append(str(contador))
		seguir = False
		while not(seguir):
			if self.total_de_creditos_carrera == contador:
				seguir = True

			else:
				contador += 1

				if contador == self.total_de_creditos_carrera:
					creditos.append(str(contador))	
					seguir = True

				else:
					string += str(contador)
					valor_a_sumar = self.total_de_creditos_carrera - contador
					if valor_a_sumar >= 15:
						string += "-"
						contador +=15
						string += str(contador)

					else:
						string += "-"
						contador += valor_a_sumar
						string += str(contador)

			if len(string) != 0:
				creditos.append(string)
			else:
				pass		
			string= ""

		return datos, creditos

	def ajustarVelocidad(self):

		self.velocidad = self.velocidad * 1000
		return self.velocidad

	#def dibujarCuadradoRojo(ax, pos_x):
	#	rect = patches.Rectangle((pos_x,0),1,2,linewidth=1,edgecolor='r',facecolor='red')
	#	ax.add_patch(rect)

	'''
	def dibujarCuadradoRojo(self, event):
		event.inaxes.patch.set_facecolor('red')
		event.canvas.draw()

	def desdibujarCuadradoRojo(self, event):
		event.inaxes.patch.set_facecolor('lightgoldenrodyellow')
		event.canvas.draw()

	'''
	def resetear(self, event):

		if self.animacionCorriendo:
			self.animacion.event_source.stop()
			self.contador_frames = 0
			self.actualizar(self.contador_frames)
			
			self.animacion.event_source.start()
			self.animacionCorriendo = True
		else:
			self.contador_frames = 0
			self.actualizar(self.contador_frames)
			self.animacion.event_source.start()
			self.animacionCorriendo = True
		print("Aqui va la instruccion del boton resetear")

	def avanzar(self, event):

		if not(self.animacionCorriendo):
			self.actualizar(self.contador_frames)
			self.animacionCorriendo = False

		print("Aqui va la instruccion del boton avanzar")

	def retroceder(self, event):

		if not(self.animacionCorriendo) and self.contador_frames > 1:
			self.contador_frames -= 2
			self.actualizar(self.contador_frames)
			self.animacionCorriendo = False
		print("Aqui va la instruccion del boton retroceder")

	def pausar(self, event):
		print("Aqui va la instruccion del boton pausar")
		if self.animacionCorriendo:
			self.animacion.event_source.stop()
			self.animacionCorriendo = False
		else:
			pass

	def iniciar(self, event):
		print("Aqui va la instruccion del boton iniciar")
		if not(self.animacionCorriendo):
			if self.contador_frames < 0:
				self.contador_frames = 1

			self.animacion.event_source.start()
			self.animacionCorriendo = True
		else:
			pass

	def velocidad(self, event):
		print("Aqui va la instruccion de la velocidad de la grafica")

	def actualizarGraficaDial(self, frame=0):

		self.animacion.event_source.stop()

		if self.slider.val > self.cantidad_de_trimestres:
			self.slider.val = self.cantidad_de_trimestres

		self.contador_frames = int(self.slider.val)+1
		#self.slider._update(self.contador_frames)
		self.animacion.event_source.start()
		self.animacionCorriendo = True
		print("Aqui va la instruccion de la actualizacion del dial")

	def solicitarAnyo(self):

		if self.contador_frames == 0:
			return self.cohorte
		if  1 <= self.contador_frames <= 3:
			return u"1er año"
		if  4 <= self.contador_frames <= 6:
			return u"2do año"
		if  7 <= self.contador_frames <= 9:
			return u"3er año"
		if  10 <= self.contador_frames <= 12:
			return u"4to año"
		if  12 <= self.contador_frames <= 15:
			return u"5to año"

	def actualizarTexto(self):

		trimestres = ["Sep-Dic", "Ene-Mar", "Abr-Jul"]

		if self.contador_frames == 0:
			self.titulo = self.solicitarAnyo()
			self.titulo_medio.set_text(self.titulo)
		if self.contador_frames == 1 or self.contador_frames == 4 or self.contador_frames == 7 or self.contador_frames == 10 or self.contador_frames == 13:
			self.titulo = trimestres[0] +" "+self.solicitarAnyo()
			self.titulo_medio.set_text(self.titulo)
		elif self.contador_frames == 2 or self.contador_frames == 5 or self.contador_frames == 8 or self.contador_frames == 11 or self.contador_frames == 14:
			self.titulo = trimestres[1] +" "+self.solicitarAnyo()
			self.titulo_medio.set_text(self.titulo)
		elif self.contador_frames == 3 or self.contador_frames == 6 or self.contador_frames == 9 or self.contador_frames == 12 or self.contador_frames == 15:
			self.titulo = trimestres[2] +" "+self.solicitarAnyo()
			self.titulo_medio.set_text(self.titulo)

	def actualizar(self, frame):

		#Actualizacion de la barra
		frame = self.contador_frames
		print(frame)
		altura_y = self.establecerPorcentaje(self.matriz[frame])
		for rect, z in zip(self.barra, altura_y):
			rect.set_height(z)

		#Actualizacion del texto
		self.actualizarTexto()

		#Actualizacion de la barra desplazadora
		self.slider.eventson = False
		self.slider.set_val(frame)
		self.slider.eventson = True

		self.contador_frames += 1

		#Detiente la grafica 
		if (self.contador_frames >=self.cantidad_de_trimestres) or (self.contador_frames < 0):
			print("Verificando" +str(self.contador_frames))
			self.animacion.event_source.stop()
			self.animacionCorriendo = False

		return self.barra

	def aumentarVelocidad(self, event):
		print("aqui va la instruccion de aumentar velocidad")

	def disminuirVelocidad(self, event):
		print("aqui va la instruccion de disminuir velocidad")	

	def animar(self):

		### Botones ###
		#Resetear
		resetearBarra = self.fig.add_axes((0.8, 0.025, 0.1, 0.05))
		boton_resetear = Button(resetearBarra, "Resetear", hovercolor='0.975')
		boton_resetear.label.set_fontsize(14)
		boton_resetear.on_clicked(self.resetear)

		#Iniciar
		iniciarBarra = self.fig.add_axes((0.69, 0.025, 0.1, 0.05))
		boton_iniciar = Button(iniciarBarra, 'Iniciar', hovercolor='0.975')
		boton_iniciar.label.set_fontsize(14)
		boton_iniciar.on_clicked(self.iniciar)
		
		#Parar
		pararBarra = self.fig.add_axes((0.58, 0.025, 0.1, 0.05))
		boton_parar = Button(pararBarra, 'Detener', hovercolor='0.975')
		boton_parar.label.set_fontsize(14)
		boton_parar.on_clicked(self.pausar)

		#Retroceder
		retrocederBarra = self.fig.add_axes((0.47, 0.025, 0.1, 0.05))
		boton_retroceder = Button(retrocederBarra, 'Retroceder', hovercolor='0.975')
		boton_retroceder.label.set_fontsize(14)
		boton_retroceder.on_clicked(self.retroceder)

		#Avanzar
		avanzarBarra = self.fig.add_axes((0.36, 0.025, 0.1, 0.05))
		boton_avanzar = Button(avanzarBarra, 'Avanzar', hovercolor='0.975')
		boton_avanzar.label.set_fontsize(14)
		boton_avanzar.on_clicked(self.avanzar)

		#Velocidad de animacion (aumentar)
		aumentarAnimacion = self.fig.add_axes((0.08, 0.025, 0.03, 0.03))
		boton_aumentar_velocidad = Button(aumentarAnimacion, label=ur'$\u25B6$', hovercolor='0.975')
		boton_aumentar_velocidad.label.set_fontsize(14)
		boton_aumentar_velocidad.on_clicked(self.aumentarVelocidad)

		#Velocidad de animacion (disminuir)
		disminuirAnimacion = self.fig.add_axes((0.03, 0.025, 0.03, 0.03))
		boton_disminuir_velocidad = Button(disminuirAnimacion, label=ur'$\u25C0$' , hovercolor='0.975')
		boton_disminuir_velocidad.label.set_fontsize(14)
		boton_disminuir_velocidad.on_clicked(self.disminuirVelocidad)

		#Slider
		barraSlider = self.fig.add_axes((0.25, 0.1, 0.65, 0.07), facecolor='lightgoldenrodyellow', label="Trimestres")
		self.slider = sliderModificado(barraSlider, label="Trimestres", valmin=0, valmax=self.cantidad_de_trimestres, valinit=0.0,
										valfmt='%1d', color="red")
		self.slider.label.set_fontsize(18)
		self.slider.on_changed(self.actualizarGraficaDial)

		plt.text(1, 13, "self.titulo", fontsize=20)

		#Lineas
		if self.cantidad_de_trimestres > 1:
			l11 = Line2D([1,1],[0,1], linewidth=1, color='black')
			barraSlider.add_line(l11)

		if self.cantidad_de_trimestres > 2:
			l12 = Line2D([2,2],[0,1], linewidth=1, color='black')
			barraSlider.add_line(l12)

		if self.cantidad_de_trimestres > 3:
			l1 = Line2D([3,3],[0,1], linewidth=4, color='black')
			barraSlider.add_line(l1)

		if self.cantidad_de_trimestres > 4:
			l21 = Line2D([4,4],[0,1], linewidth=1, color='black')
			barraSlider.add_line(l21)

		if self.cantidad_de_trimestres > 5:
			l22 = Line2D([5,5],[0,1], linewidth=1, color='black')
			barraSlider.add_line(l22)

		if self.cantidad_de_trimestres > 6:
			l2 = Line2D([6,6],[0,1], linewidth=4, color='black')
			barraSlider.add_line(l2)

		if self.cantidad_de_trimestres > 7:
			l31 = Line2D([7,7],[0,1], linewidth=1, color='black')
			barraSlider.add_line(l31)

		if self.cantidad_de_trimestres > 8:
			l32 = Line2D([8,8],[0,1], linewidth=1, color='black') 
			barraSlider.add_line(l32)

		if self.cantidad_de_trimestres > 9:
			l3 = Line2D([9,9],[0,1], linewidth=4, color='black')
			barraSlider.add_line(l3)

		if self.cantidad_de_trimestres > 10:
			l41 = Line2D([10,10],[0,1], linewidth=1, color='black')
			barraSlider.add_line(l41)

		if self.cantidad_de_trimestres > 11:
			l42 = Line2D([11,11],[0,1], linewidth=1, color='black') 
			barraSlider.add_line(l42)

 		if self.cantidad_de_trimestres > 12:
 			l4 = Line2D([12,12],[0,1], linewidth=4, color='black')
 			barraSlider.add_line(l4)

 		if self.cantidad_de_trimestres > 13:
			l51 = Line2D([13,13],[0,1], linewidth=1, color='black')
			barraSlider.add_line(l51)

		if self.cantidad_de_trimestres > 14:
			l52 = Line2D([14,14],[0,1], linewidth=1, color='black')
			barraSlider.add_line(l52)

		plt.show()

##################
#### Programa ####
##################

#Constantes y variables 
#15 trimestres
'''
lista0 = [80,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista1 = [40,60,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista2 = [23,27,50,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista3 = [17,25,30,28,0,0,0,0,0,0,0,0,0,0,0,0]
lista4 = [10,20,20,15,35,0,0,0,0,0,0,0,0,0,0,0]
lista5 = [7,13,25,25,20,10,0,0,0,0,0,0,0,0,0,0]
lista6 = [5,10,30,15,15,15,10,0,0,0,0,0,0,0,0,0]
lista7 = [2,13,15,30,18,12,5,5,0,0,0,0,0,0,0,0]
lista8 = [1,10,14,10,20,15,39,8,3,0,0,0,0,0,0,0]
lista9 = [1,7,20,16,12,25,19,15,30,10,0,0,0,0,0,0]
lista10 = [1,5,12,45,25,14,27,12,8,16,11,0,0,0,0,0]
lista11 = [0,15,24,16,8,15,21,12,25,34,7,8,0,0,0,0]
lista12 = [0,4,16,12,14,34,23,21,17,11,7,9,2,0,0,0]
lista13 = [0,0,14,22,16,12,8,25,24,13,18,19,12,7,0,0]
lista14 = [0,0,8,12,24,13,8,17,16,12,23,12,19,11,5,0]
lista15 = [0,0,0,12,23,12,7,30,12,45,21,14,17,9,15,8]

matriz = []
matriz.append(lista0)
matriz.append(lista1)
matriz.append(lista2)
matriz.append(lista3)
matriz.append(lista4)
matriz.append(lista5)
matriz.append(lista6)
matriz.append(lista7)
matriz.append(lista8)
matriz.append(lista9)
matriz.append(lista10)
matriz.append(lista11)
matriz.append(lista12)
matriz.append(lista13)
matriz.append(lista14)
matriz.append(lista15)
'''
#4 trimestres

'''
matriz = []
lista0 = [80,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista1 = [40,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista2 = [20,30,30,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista3 = [10,20,18,32,0,0,0,0,0,0,0,0,0,0,0,0]
lista4 = [5,15,10,20,30,0,0,0,0,0,0,0,0,0,0,0]

matriz.append(lista0)
matriz.append(lista1)
matriz.append(lista2)
matriz.append(lista3)
matriz.append(lista4)
'''

#8 trimestres

matriz = []
lista0 = [80,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista1 = [40,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista2 = [20,30,30,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista3 = [10,20,18,32,0,0,0,0,0,0,0,0,0,0,0,0]
lista4 = [5,15,10,20,30,0,0,0,0,0,0,0,0,0,0,0]
lista5 = [3,12,24,12,8,4,0,0,0,0,0,0,0,0,0,0]
lista6 = [1,7,17,21,30,15,8,0,0,0,0,0,0,0,0]
lista7 = [1,4,21,15,7,21,11,8,0,0,0,0,0,0,0]
lista8 = [0,1,15,20,10,12,18,20,10,0,0,0,0,0,0]
lista9 = [0,0,7,15,13,8,18,12,16,9,0,0,0,0,0]

matriz.append(lista0)
matriz.append(lista1)
matriz.append(lista2)
matriz.append(lista3)
matriz.append(lista4)
matriz.append(lista5)
matriz.append(lista6)
matriz.append(lista7)
matriz.append(lista8)
matriz.append(lista9)


#fig.canvas.mpl_connect('button_press_event', clickBarraDesplazadora)
#fig.canvas.mpl_connect('button_press_event', pausar)
grafica = graficaDeBarras(u"Ingeniería de la Computación", "Cohorte 13", matriz, 80, 240, 1, 10)
grafica.animar()
