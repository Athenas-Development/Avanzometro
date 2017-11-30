from django.test import LiveServerTestCase
from django.test import Client
from selenium.webdriver.support.ui import Select
from selenium import webdriver

from apps.registro.models import *

import time

# Casos de pruebas unitarios

class MultigraphTest(LiveServerTestCase):

	# Configuracion de los objetos necesarios para las pruebas
	def setUp(self):
		self.client = Client()
		self.set_db()

	# Recoleccion y eliminacion de los objetos usados para las pruebas
	def tearDown(self):
		self.client = None


	# Pruebas de Interfaz y Graficas Multiples

	# Configuracion de la base de datos. Para correr esta prueba, se deberia correr esta funcion con anterioridad,
	# si se quiere dar tambien un vistazo a la funcionalidad de la base de datos y su interaccion con el controlador
	# y las vistas. SI NO SE HACE 3 DE ESTAS PRUEBAS RESULTARAN FALLIDAS! pero aun asi se podra ver en el navegador
	# Firefox que estas si cumplen con lo especificado.
	def set_db(self):
		# Carga de 5 cohortes
		ch11 = Cohorte(id='11')
		ch12 = Cohorte(id='12')
		ch13 = Cohorte(id='13')
		ch68 = Cohorte(id='68')
		ch17 = Cohorte(id='17')

		ch11.save()
		ch12.save()
		ch13.save()
		ch68.save()
		ch17.save()

		# Carga de 5 trimestres
		tr11 = Trimestre(id='Sep-Dic 2011')
		tr12 = Trimestre(id='Sep-Dic 2012')
		tr13 = Trimestre(id='Sep-Dic 2013')
		tr68 = Trimestre(id='Sep-Dic 1968')
		tr17 = Trimestre(id='Sep-Dic 2017')

		tr11.save()
		tr12.save()
		tr13.save()
		tr68.save()
		tr17.save()

		# Carga de 1 Estudiante por Cohorte
		chf11 = Cohorte.objects.filter(id='11').first()
		est11 = Estudiante(carnet='11-10000', nombre='abc11', cohorte=chf11)
		est11.save()

		chf12 = Cohorte.objects.filter(id='12').first()
		est12 = Estudiante(carnet='12-10000', nombre='abc12', cohorte=chf12)
		est12.save()

		chf13 = Cohorte.objects.filter(id='13').first()
		est13 = Estudiante(carnet='13-10000', nombre='abc13', cohorte=chf13)
		est13.save()

		chf68 = Cohorte.objects.filter(id='68').first()
		est68 = Estudiante(carnet='68-10000', nombre='abc68', cohorte=chf68)
		est68.save()

		chf17 = Cohorte.objects.filter(id='17').first()
		est17 = Estudiante(carnet='17-10000', nombre='abc17', cohorte=chf17)
		est17.save()

		# Carga 1 cursa por estudiante
		trf11 = Trimestre.objects.filter(id='Sep-Dic 2011').first()
		estf11 = Estudiante.objects.filter(carnet='11-10000').first()
		cs11 = Cursa(estudiante=estf11, trimestre=trf11, creditosAprobados=0)
		cs11.save()

		trf12 = Trimestre.objects.filter(id='Sep-Dic 2012').first()
		estf12 = Estudiante.objects.filter(carnet='12-10000').first()
		cs12 = Cursa(estudiante=estf12, trimestre=trf12, creditosAprobados=1)
		cs12.save()

		trf13 = Trimestre.objects.filter(id='Sep-Dic 2013').first()
		estf13 = Estudiante.objects.filter(carnet='13-10000').first()
		cs13 = Cursa(estudiante=estf13, trimestre=trf13, creditosAprobados=120)
		cs13.save()

		trf68 = Trimestre.objects.filter(id='Sep-Dic 1968').first()
		estf68 = Estudiante.objects.filter(carnet='68-10000').first()
		cs68 = Cursa(estudiante=estf68, trimestre=trf68, creditosAprobados=240)
		cs68.save()

		trf17 = Trimestre.objects.filter(id='Sep-Dic 2017').first()
		estf17 = Estudiante.objects.filter(carnet='17-10000').first()
		cs17 = Cursa(estudiante=estf17, trimestre=trf17, creditosAprobados=241)
		cs17.save()

	# Primera parte del formulario. Solo 1 cohorte
	def start_form(self, browser):
		browser.get('http://localhost:8000/multigrafica/')
		inputbox = browser.find_element_by_id('ncohortes')
		inputbox.clear()
		inputbox.send_keys('1')
		time.sleep(1)
		button = browser.find_element_by_id('sendcohortes')
		button.click()
		time.sleep(5)


	# Pruebas de Funcionalidad
	# Prueba: Status HTTP Ok
	def test_a_http_response_ok(self):
		response = self.client.get('/multigrafica/')
		self.assertEquals(response.status_code, 200)

	# Prueba: Carga exitosa de Templates
	def test_b_correct_templates(self):
		response = self.client.get('/multigrafica/')

		self.assertTemplateUsed(response, 'multigraph.html')
		self.assertTemplateUsed(response, 'layout.html')

	# Prueba: Captura de datos de tipo POST
	def test_c_capturing_POST_requests(self):
		response = self.client.post('/multigrafica/',
			data = { 'ncohortes': '5'})

		self.assertEquals(response.status_code, 200)


	# Se cuenta con una serie de "centinela" escondido dentro
	# del html que indica el paso del formulario uno se encuentra.
	# El formulario es el que realiza todas las validaciones y muestra los errores correspondientes.

	# Prueba: Mostrar Grafica
	def test_d_show_graph(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('16')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('2000')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('11')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		form_error =  browser.find_element_by_id('error_mostrado')
		error = form_error.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'1')
		self.assertEqual(error, '0')

	# Numero de Cohortes. Dominio [1 .. 5]
	# Prueba Borde: Numero de Cohortes igual a 5
	def test_e_ncohortes_exactly_5(self):
		browser = webdriver.Firefox()
		browser.get('http://localhost:8000/multigrafica/')
		inputbox=browser.find_element_by_id('ncohortes')
		inputbox.clear()
		inputbox.send_keys('5')
		time.sleep(1)
		button=browser.find_element_by_id('sendcohortes')
		button.click()
		time.sleep(5)
		form_step = browser.find_element_by_id('forma')
		step = form_step.get_attribute("value")
		time.sleep(5)
		browser.quit()

		self.assertEqual(step, "0") # paso al siguiente paso del formulario

	# Prueba Borde: Numero de Cohortes igual a 1
	def test_e_ncohortes_exactly_1(self):
		browser = webdriver.Firefox()
		browser.get('http://localhost:8000/multigrafica/')
		inputbox = browser.find_element_by_id('ncohortes')
		inputbox.clear()
		inputbox.send_keys('1')
		time.sleep(1)
		button = browser.find_element_by_id('sendcohortes')
		button.click()
		time.sleep(5)
		form_step = browser.find_element_by_id('forma')
		step = form_step.get_attribute("value")
		time.sleep(5)
		browser.quit()

		self.assertEqual(step, "0")  # paso al siguiente paso del formulario

	# Prueba Malicia: Numero de Cohortes mayor a 5
	def test_e_ncohortes_more_than_5(self):
		browser = webdriver.Firefox()
		browser.get('http://localhost:8000/multigrafica/')
		inputbox = browser.find_element_by_id('ncohortes')
		inputbox.clear()
		inputbox.send_keys('7')
		time.sleep(1)
		button = browser.find_element_by_id('sendcohortes')
		button.click()
		time.sleep(5)
		form_step = browser.find_element_by_id('forma')
		step = form_step.get_attribute("value")
		time.sleep(5)
		browser.quit()

		self.assertEqual(step, "1")  # No paso al siguiente paso del formulario

	# Prueba Malicia: Numero de Cohortes menor a 1
	def test_e_ncohortes_less_than_1(self):
		browser = webdriver.Firefox()
		browser.get('http://localhost:8000/multigrafica/')
		inputbox = browser.find_element_by_id('ncohortes')
		inputbox.clear()
		inputbox.send_keys('-3')
		time.sleep(1)
		button = browser.find_element_by_id('sendcohortes')
		button.click()
		time.sleep(5)
		form_step = browser.find_element_by_id('forma')
		step = form_step.get_attribute("value")
		time.sleep(5)
		browser.quit()

		self.assertEqual(step, "1")  # No paso al siguiente paso del formulario

	# Carrera
	# Prueba Malicia: Carrera no elegida
	def test_f_carrera_empty(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('16')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('2000')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('11')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		time.sleep(5)
		browser.quit()


		self.assertEqual(step, '0')


	# Granularidad: Dominio [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 21, 26, 34, 40, 48, 60, 80, 120, 240]
	# Prueba Borde: Granularidad 5
	def test_g_granularidad_exactly_5(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('5')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('2000')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('11')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		form_error =  browser.find_element_by_id('error_mostrado')
		error = form_error.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'1')
		self.assertEqual(error, '0')

	# Prueba Borde: Granularidad 240
	def test_g_granularidad_exactly_240(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('240')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('2000')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('11')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		form_error =  browser.find_element_by_id('error_mostrado')
		error = form_error.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'1')
		self.assertEqual(error, '0')

	# Prueba Malicia: Granularidad no elegida
	def test_g_granularidad_empty(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('2000')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('11')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'0')

	# Velocidad de Imagen: Dominio [500, 1000, 1500, 2000, 2500, 3000]
	# Prueba Borde: Milisegundos 500
	def test_h_mlsPorImagen_exactly_500(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('16')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('500')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('11')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		form_error =  browser.find_element_by_id('error_mostrado')
		error = form_error.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'1')
		self.assertEqual(error, '0')

	# Prueba Borde: Milisegundos 3000
	def test_h_mlsPorImagen_exactly_3000(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('16')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('3000')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('11')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		form_error =  browser.find_element_by_id('error_mostrado')
		error = form_error.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'1')
		self.assertEqual(error, '0')

	# Prueba Malicia: Milisegundos no elegida
	def test_h_mlsPorImagen_empty(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('16')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('11')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'0')


	# Cohorte: Dominio [68 .. 99] + [00 .. 17]
	# Prueba Borde: Cohorte 68
	def test_i_cohorte_68(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('16')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('2000')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('68')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		form_error =  browser.find_element_by_id('error_mostrado')
		error = form_error.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'1')
		self.assertEqual(error, '0')

	# Prueba Borde: Cohorte 17
	def test_i_cohorte_17(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('16')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('2000')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('17')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		form_error =  browser.find_element_by_id('error_mostrado')
		error = form_error.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'1')
		self.assertEqual(error, '0')

	# Prueba Malicia: Cohorte sin datos
	def test_i_cohorte_00(self):
		browser = webdriver.Firefox()
		self.start_form(browser)

		carrera_select = Select(browser.find_element_by_id('carrera'))
		carrera_select.select_by_visible_text('Urbanismo')
		time.sleep(1)

		rango_select = Select(browser.find_element_by_id('rango'))
		rango_select.select_by_visible_text('16')
		time.sleep(1)

		mls_select = Select(browser.find_element_by_id('mlsPorImagen'))
		mls_select.select_by_visible_text('2000')
		time.sleep(1)

		ch_select = Select(browser.find_element_by_id('Cohorte1'))
		ch_select.select_by_visible_text('00')
		time.sleep(1)

		button = browser.find_element_by_id('send_data')
		button.click()
		time.sleep(5)

		form_step = browser.find_element_by_id('grafica_mostrada')
		step = form_step.get_attribute("value")
		form_error =  browser.find_element_by_id('error_mostrado')
		error = form_error.get_attribute("value")
		time.sleep(5)
		browser.quit()
		self.assertEqual(step,'1')
		self.assertEqual(error, '1')










