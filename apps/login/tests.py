from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from apps.login.views import index

class HomePageTest(TestCase):
	def test_uses_home_template(self):
		response = self.client.get('/')

		self.assertTemplateUsed(response, 'login.html')
		self.assertTemplateUsed(response, 'layout.html')