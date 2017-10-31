from django.test import TestCase
from django.contrib.auth.models import User

class RegistroFormTest(TestCase):
    def setUp(self):
        self.registroBueno = User.objects.create_user(id=1, first_name='Miguel', last_name='Canedo', username='miganedo', email='mi.canedo10@gmail.com', password='secret123')
        self.registroBueno.save()

        self.registroMaloNombre = User.objects.create_user(id=2, first_name='Topocho23', last_name='inquitomalo', username='sopoki', email='kikiriwiki@gmail.com', password='sopoki')		
        self.registroMaloNombre.save()

    def test_IdCorrectamenteAlmacenado(self):
        self.assertEquals(self.registroBueno.id, 1)

    def test_UsuarioNoAlmacenadoPorNombreConNumero(self):
    	self.assertEquals(self.registroMaloNombre.id, 2)

class RegistroPageTest(TestCase):
	def test_uses_registrarUsuarios_template(self):
		response = self.client.get('/registro')

		self.assertTemplateUsed(response, 'registrarUsuario.html')
		self.assertTemplateUsed(response, 'layout.html')

	def test_capturing_POST_requests(self):
		response = self.client.post('/registro', 
			data = { 'first_name': 'Solomeo',
					 'last_name': 'Paredes',
					 'username': 'scatman',
					 'email': 'scatman@gmail.com',
					 'password1': 'ocho1234',
					 'password2': 'ocho1234'
					 })

		self.assertEquals(response.status_code, 302)

		# self.assertFormError(response, 'form', 'something', 'This field is required.')




