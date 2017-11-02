from django.db import models

# Create your models here.
class documento(models.Model):
    documento = models.FileField()
    fecha = models.DateTimeField(auto_now_add=True)