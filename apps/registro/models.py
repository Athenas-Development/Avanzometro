from django.db import models

# Create your models here.

class Cohorte(models.Model):
    id = models.IntegerField(primary_key=True)

class Estudiante(models.Model):
    carnet = models.CharField(primary_key=True, max_length = 8)
    nombre = models.CharField(max_length = 50)
    cohorte = models.ForeignKey(Cohorte, on_delete=models.CASCADE)

class Trimestre(models.Model):
    id = models.CharField(primary_key=True, max_length = 50)

class Cursa(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)
    creditosAprobados = models.IntegerField()