from django.contrib import admin
from apps.registro.models import *

# Register your models here.
admin.site.register(Cohorte)
admin.site.register(Carrera)
admin.site.register(Estudiante)
admin.site.register(Trimestre)
admin.site.register(Cursa)