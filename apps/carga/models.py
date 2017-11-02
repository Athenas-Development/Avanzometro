from django.db import models

# Create your models here.

'''
Documento:
	documento: File // Contiene el documento csv de la carga de los estudiantes
	fecha: DateTime // Contiene la fecha en que fue a;adido el documento
'''
class documento(models.Model):
    documento = models.FileField()
    fecha = models.DateTimeField(auto_now_add=True)