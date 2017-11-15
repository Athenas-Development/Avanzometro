import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from apps.registro.models import *
import mpld3
#import matplotlib as matplt

def crear_grafica(cohorte, carrera, trimestre, total_estudiantes, lista):

    carrera = carrera
    total_de_estudiantes = total_estudiantes
    total_de_creditos_carrera = 240
    cohorte = cohorte
    trimestre = trimestre
    titulo = cohorte + '\n' + trimestre
    lista = lista

    # Statico
    datos = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%', '']
    creditos = []

    # arreglo que contendra un % con respecto al 100 % de la cohorte
    y = []

    for i in lista:
        y.append(((float(i * 100)) / total_de_estudiantes) / 10)

    # creditos que estaran en el eje x (varia con respecto al total de creditos de la carrera)
    contador = 0
    string = ""
    creditos.append(str(contador))
    seguir = False
    while not (seguir):
        if total_de_creditos_carrera == contador:
            seguir = True

        else:
            contador += 1

            if contador == total_de_creditos_carrera:
                creditos.append(str(contador))
                seguir = True

            else:
                string += str(contador)
                valor_a_sumar = total_de_creditos_carrera - contador
                if valor_a_sumar >= 15:
                    string += "-"
                    contador += 15
                    string += str(contador)

                else:
                    string += "-"
                    contador += valor_a_sumar
                    string += str(contador)

        if len(string) != 0:
            creditos.append(string)
        else:
            pass
        string = ""

    creditos.append("240+")
    # OJO: La longitud de creditos debe ser igual a la longitud de la lista que contiene el numero de estudiantes por trimestre


    idsx = np.arange(len(creditos))
    idsy = np.arange(len(datos))

    # Formato de la figura
    fig = plt.figure(figsize=(22, 12), dpi=60, frameon=True)

    # 1 cuadro por imagen
    ax = fig.add_subplot(1, 1, 1)

    # Grafia barra
    plt.bar(idsx, y, width=0.5, color='c', align="center", label=carrera)

    # labels
    plt.yticks(idsy, datos, fontsize=14)
    plt.xticks(idsx, creditos, fontsize=14)  # labels del eje horizontal

    # nombres, titulos y leyenda y frontera del eje y
    plt.xlabel("Créditos", fontsize=18)
    plt.ylabel("% de Estudiantes", fontsize=18)
    plt.ylim(0, 11)

    plt.title(titulo, fontsize=20)
    plt.legend(bbox_to_anchor=(0, 0, 1, 1), fontsize=15, loc=2, shadow=True)  # loc= "lower left"
    #plt.savefig(fname="static/grafica.png", dpi=100)
    return mpld3.fig_to_html(fig)
