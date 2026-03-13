[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AG7uuOyW)


Información importante del código:

-No me funcionaron los comandos:
!coverage run --rcfile=.coveragerc -m unittest discover -s tests
!coverage report -m --omit="tests/*,src/models.py"

-Pero con los comandos:
!coverage report -m --omit="tests/*,src/models.py"
!coverage report -m --omit="tests/*,src/models.py"

Tengo 100% de coverage



Fuentes:
-Para llevar a cabo esta tarea, se utilizó el material de clases, y la feature "autocomplete" de copilot.


Supuestos:
Se asume que no es necesario hacer Mocks para funciones estables como strip().upper()