from django.conf.urls import url
from apps.login.views import index

#Aqui se especifican todos los urls a los que redirecciona la pagina
urlpatterns = [
    url(r'^$', index),
]
