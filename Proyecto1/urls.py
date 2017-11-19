"""Proyecto1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from apps.carga.views import cargarArchivo
from apps.login.views import logout_then_login
from apps.instantanea.views import instantanea
from apps.animacion.views import animacion
from apps.multigraph.views import multigrafica

#Urls a los que redirecciona todas las paginass dentro de el software

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'$^', login, {'template_name':'login.html'}),
    url(r'^registro/', include('apps.registro.urls')),
    url(r'^instantanea/', instantanea),
    url(r'^cargaArchivo/', cargarArchivo),
    url(r'^logout/$', logout_then_login),
    url(r'^animacion/$', animacion),
    url(r'multigrafica/$', multigrafica)
]
