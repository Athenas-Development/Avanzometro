from django.test import TestCase
from django.test import LiveServerTestCase
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

# Casos de pruebas unitarios

class MultigraphTest(LiveServerTestCase):

	# Configuracion de los objetos necesarios para las pruebas
	def setUp(self):
		self.client = Client()

	# Recoleccion y eliminacion de los objetos usados para las pruebas
	def tearDown(self):
		self.client = None

	# Pruebas de Interfaz y Graficas

	# Prueba: Status HTTP Ok
	def test_http_response_ok(self):
		response = self.client.get('/multigrafica/')
		self.assertEquals(response.status_code, 200)

	# Prueba: Carga exitosa de Templates
	def test_correct_templates(self):
		response = self.client.get('/multigrafica/')

		self.assertTemplateUsed(response, 'multigraph.html')
		self.assertTemplateUsed(response, 'layout.html')

	# Prueba: Captura de datos de tipo POST
	def test_capturing_POST_requests(self):
		response = self.client.post('/multigrafica/',
			data = { 'ncohortes': '5'})

		self.assertEquals(response.status_code, 200)

	# Prueba Borde: Numero de Cohortes mayor a 5
	def test_ncohortes_more_than_5(self):
		browser = webdriver.Firefox()
		browser.get('http://localhost:8000/multigrafica/')
		inputbox=browser.find_element_by_id('ncohortes')
		inputbox.clear()
		inputbox.send_keys('6')
		time.sleep(1)
		button=browser.find_element_by_id('sendcohortes')
		button.click()
		time.sleep(1)
		form_step = browser.find_element_by_id('forma')
		step = form_step.get_attribute("value")
		browser.quit()

		self.assertEqual(step, "1") # No paso al siguiente paso del formulario

	# Prueba Borde: Numero de Cohortes menor a 1
	def test_ncohortes_less_than_1(self):
		browser = webdriver.Firefox()
		browser.get('http://localhost:8000/multigrafica/')
		inputbox = browser.find_element_by_id('ncohortes')
		inputbox.clear()
		inputbox.send_keys('0')
		time.sleep(1)
		button = browser.find_element_by_id('sendcohortes')
		button.click()
		time.sleep(1)
		form_step = browser.find_element_by_id('forma')
		step = form_step.get_attribute("value")
		browser.quit()

		self.assertEqual(step, "1")  # No paso al siguiente paso del formulario

	# Prueba de Malicia: 