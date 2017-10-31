from django.test import TestCase
from django.contrib.auth.models import User

class RegistroFormTest(TestCase):
    def setUp(self):
        self.registroBueno = User.objects.create_user(id=1, first_name='Miguel',
                        last_name='Canedo', username='miganedo', email='mi.canedo10@gmail.com', password='secret123')
        self.registroBueno.save()

    def test_IdCorrectamenteAlmacenado(self):
        self.assertEquals(self.registroBueno.id, 1)

class RegistroPageTest(TestCase):
	def test_uses_registrarUsuarios_template(self):
		response = self.client.get('/registro')

		self.assertTemplateUsed(response, 'registrarUsuario.html')
		self.assertTemplateUsed(response, 'layout.html')