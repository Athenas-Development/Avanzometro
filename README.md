# Avanzometro
Proyecto de Ingenieria de Software. Trimestre Septiembre - Diciembre 2017.
## Pasos para la instalación de la DB:
- Descargar e Instalar PostgreSQL 9.X
- Iniciar sesión como usuario postgres y crear la BD SisPIO:
```
sudo -su postgres
CREATE DATABASE "Avanzometro";
```
- Crear usuario Avanzometro y garantarizar el acceso a la BD:
```
CREATE USER "Avanzometro" WITH PASSWORD 'Avanzometro';
GRANT ALL PRIVILEGES ON DATABASE "Avanzometro" to "Avanzometro";
```
- Y a trabajar :D
