from django.db import models
import csv

'''
Cohorte:
    id: Integer // Identificador de la cohorte el cual es representado por los dos ultimos numero del a;o
'''
class Cohorte(models.Model):
    id = models.IntegerField(primary_key=True)

'''
Estudiante:
    carnet: String // Llave primaria del estudiante que representa el numero de su carnet
    nombre: String // String del estudiante que representa su nombre y apellido
    cohorte: Integer // Llave foraner de Cohorte el cual identifica la cohorte del estudiante
'''
class Estudiante(models.Model):
    carnet = models.CharField(primary_key=True, max_length = 8)
    nombre = models.CharField(max_length = 50)
    cohorte = models.ForeignKey(Cohorte, on_delete=models.CASCADE)

'''
Trimestre:
    id: String // Llave primaria del trimestre que identifica el trimestre del a;o cursado (Ene-Mar, Abr-Jul, Sept-Dic)
'''
class Trimestre(models.Model):
    id = models.CharField(primary_key=True, max_length = 50)

'''
Cursa (Relacion):
    estudiante: String // Llave foranea que representa el carnet del estudiante que curso el trimestre
    trimestre: String // Llave foranea que identifica el trimestre cursado por el estudiante
    creditosAprobados: Interger // Numero que representa la cantidad de creditos aprobados por el estudiante 
'''
class Cursa(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)
    creditosAprobados = models.IntegerField()



