from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

class RegistroPageTest(LiveServerTestCase):
	def setUp(self):
		self.cliente = Client()
		

	def tearDown(self):
		self.cliente = None

	# Prueba: Status HTTP OK
	def test_http_response_ok(self):
		response = self.cliente.get('/registro/')

		self.assertEquals(response.status_code, 200)

	# Prueba: Carga exitosa de Templates
	
	def test_correct_templates(self):
		response = self.cliente.get('/registro/')

		self.assertTemplateUsed(response, 'registrarUsuario.html')
		self.assertTemplateUsed(response, 'layout.html')

	# Prueba: Captura de datos de tipo POST

	def test_capturing_POST_requests(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'Erick',
					 'last_name': 'Flejan',
					 'username': 'scatman@hotmail.com',
					 'password1': 'ocho1234',
					 'password2': 'ocho1234'
					 })

		self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertEquals(last_user.username, 'scatman@hotmail.com')
		self.assertEquals(response.status_code, 302)

	# Prueba frontera: frontera nombre tamano minimo 1

	def test_length_first_name_1(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'E',
					 'last_name': 'Flejan',
					 'username': 'scatman@hotmail.com',
					 'password1': 'ocho1234',
					 'password2': 'ocho1234'
					 })

		self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertEquals(len(last_user.first_name), 1)

	# Prueba frontera: frontera nombre tamano maximo 30

	def test_length_first_name_30(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'Ericknator el mejor robot dela',
					 'last_name': 'Flejan',
					 'username': 'scatman@hotmail.com',
					 'password1': 'ocho1234',
					 'password2': 'ocho1234'
					 })

		self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertEquals(len(last_user.first_name), 30)

	# Prueba frontera: frontera apellido tamano minimo 1

	def test_length_last_name_1(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'Erick',
					 'last_name': 'F',
					 'username': 'scatman@hotmail.com',
					 'password1': 'ocho1234',
					 'password2': 'ocho1234'
					 })

		self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertEquals(len(last_user.last_name), 1)

	# Prueba frontera: frontera apellido tamano minimo 30

	def test_length_last_name_30(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'Erick',
					 'last_name': 'Flejanneitor de la rosa quinti',
					 'username': 'scatman@hotmail.com',
					 'password1': 'ocho1234',
					 'password2': 'ocho1234'
					 })

		self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertEquals(len(last_user.last_name), 30)

	# Pruebas esquina: 

	# Prueba esquina: nombre con tama;o minimo 1 y apellido maximo 30

	def test_length_first_name_last_name(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'E',
					 'last_name': 'Flejaneitor hotmailgmailoutloo',
					 'username': 'scatman@hotmail.com',
					 'password1': 'ocho1234',
					 'password2': 'ocho1234'
					 })

		self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertEquals(len(last_user.first_name), 1)
		self.assertEquals(len(last_user.last_name), 30)
		
	# Prueba esquina: apellido con tama;o minimo 1 y nombre maximo 30
	
	def test_length_last_name_first_name(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'Flejaneitor hotmailgmailoutloo',
					 'last_name': 'E',
					 'username': 'scatman@hotmail.com',
					 'password1': 'ocho1234',
					 'password2': 'ocho1234'
					 })

		self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertEquals(len(last_user.first_name), 30)
		self.assertEquals(len(last_user.last_name), 1)

	# Prueba esquina: clave tama;o minimo 8 maximo 16
	def test_length_password1(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'Flejaneitor hotmailgmailoutloo',
					 'last_name': 'E',
					 'username': 'scatman@hotmail.com',
					 'password1': 'holacomoestas1111111',
					 'password2': 'holacomoestas1111111'
					 })
	
		self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertFalse(last_user.password == "holacomoestas1111111")

	#Prueba Malicia.

	# Prueba malicia: clave menor a tama;o minimo	
	def test_length_password2(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'Flejaneitor hotmailgmailoutloo',
					 'last_name': 'E',
					 'username': 'scatman@hotmail.com',
					 'password1': '',
					 'password2': ''
					 })

		self.assertEquals(User.objects.count(), 0)

	# Prueba malicia: clave mayor a tama;o maximo
	def test_length_password3(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'Flejaneitor hotmailgmailoutloo',
					 'last_name': 'E',
					 'username': 'scatman@hotmail.com',
					 'password1': '123456789101112131415',
					 'password2': '123456789101112131415'
					 })

		self.assertEquals(User.objects.count(), 0)

	# Prueba malicia: correo sin arroba
	def test_format_username1(self):
		browser = webdriver.Firefox()
		browser.get('http://127.0.0.1:8000/registro/')
		inputbox=browser.find_element_by_id('first_name')
		inputbox.send_keys('Erick')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('last_name')
		inputbox.send_keys('Flejan')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('username')
		inputbox.send_keys('hola')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('password1')
		inputbox.send_keys('ocho1234')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('password2')
		inputbox.send_keys('ocho1234')
		time.sleep(0.5)
		button=browser.find_element_by_id('regbutton')
		button.click()
		time.sleep(2)
		self.assertEquals(browser.current_url, 'http://127.0.0.1:8000/registro/')
		browser.quit()
		

	# Prueba malicia: correo como solo un punto
	def test_format_username2(self):
		browser = webdriver.Firefox()
		browser.get('http://127.0.0.1:8000/registro/')
		inputbox=browser.find_element_by_id('first_name')
		inputbox.send_keys('Erick')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('last_name')
		inputbox.send_keys('Flejan')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('username')
		inputbox.send_keys('hola.')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('password1')
		inputbox.send_keys('ocho1234')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('password2')
		inputbox.send_keys('ocho1234')
		time.sleep(0.5)
		button=browser.find_element_by_id('regbutton')
		button.click()
		time.sleep(2)
		self.assertEquals(browser.current_url, 'http://127.0.0.1:8000/registro/')
		browser.quit()

	# Prueba malicia: nombre acepte caracteres especiales
	def test_characters_first_name(self):
		response = self.cliente.post('/registro/', 
			data = { 'first_name': 'Flejan',
					 'last_name': 'E',
					 'username': 'scatmanhotmail.com',
					 'password1': 'ocho1234',
					 'password2': 'ocho1234'
					 })

		self.assertEquals(User.objects.count(), 1)