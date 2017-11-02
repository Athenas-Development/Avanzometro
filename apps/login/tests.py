from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

class HomePageTest(LiveServerTestCase):

	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'login.html')
		self.assertTemplateUsed(response, 'layout.html')

	def test_successful_login(self):

		browser = webdriver.Firefox()
		browser.get('http://127.0.0.1:8000/registro/')
		inputbox=browser.find_element_by_id('first_name')
		inputbox.send_keys('Erick')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('last_name')
		inputbox.send_keys('Flejan')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('username')
		inputbox.send_keys('erickflejan67@example.com')
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

		browser.get('http://127.0.0.1:8000/')
		inputbox=browser.find_element_by_id('username')
		inputbox.send_keys('erickflejan67@gmail.com')
		time.sleep(0.5)
		inputbox=browser.find_element_by_id('password')
		inputbox.send_keys('ocho1234')
		time.sleep(0.5)
		button=browser.find_element_by_id('regbutton')
		button.click()
		time.sleep(2)

		User.objects.filter(username='erickflejan67@gmail.com').delete()

		self.assertTrue(browser.current_url, 'http://127.0.0.1:8000/instantanea/')

		browser.quit()