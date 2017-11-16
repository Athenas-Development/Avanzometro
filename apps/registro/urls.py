from django.conf.urls import url
from apps.registro.views import RegistroUsuario
from apps.login.views import logout
from django.conf import settings

#Estos son los urls a los que redirecciona la pagina de registro

urlpatterns = [
    url(r'^$', RegistroUsuario.as_view()),
    url(r'^logout/$', logout, {'next_page':settings.LOGOUT_REDIRECT_URL}),
]