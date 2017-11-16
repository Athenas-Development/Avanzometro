from django.contrib.auth.models import User
from django.views.generic import CreateView
from apps.registro.forms import RegistroForm


# Create your views here.

#Controladores de la vista de registro

#Envia a la pagina principal despues de un registro exitoso
class RegistroUsuario(CreateView):
    model = User
    template_name = 'registrarUsuario.html'
    form_class = RegistroForm
    success_url = '/'

