# Avanzometro
Proyecto de Ingenieria de Software. Trimestre Septiembre - Diciembre 2017.

## Integrantes de Athenas Development
 - Miguel Canedo 13-10214
 - Carlos Perez 13-11089
 - Erick Flejan 12-11555
 - Andres Buelvas 13-10184
 - Yezabel Rincon 10-11005
 - Jose Bracuto 13-10173
 - Ritces Parra 12-11088
 - Rafael Cisneros 13-11156
 
## Softwares necesarios:
  - Python 3
  - Django
  - Psycopg2
  - MatPlotLib
  - Selenium
  - Firefox
  - Postgresql
  - NumPy
  
## Pasos para la instalación de la DB:
- Descargar e Instalar PostgreSQL 9.X
- Iniciar sesión como usuario postgres y crear la BD Avanzometro:
```
sudo -su postgres
CREATE DATABASE "Avanzometro";
```
- Crear usuario Avanzometro y garantarizar el acceso a la BD:
```
CREATE USER "Avanzometro" WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE "Avanzometro" to "Avanzometro";
```
- Y a trabajar :D

## Pasos para instalar librerias de Python:
 ```
 python -m pip install django --upgrade
 
 python -m pip install psycopg2 --upgrade
 
 python -m pip install matplotlib --upgrade
 
 python -m pip install selenium --upgrade
 
 python -m pip install numpy --upgrade
 ```
