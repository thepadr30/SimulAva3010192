.. Simulación Avanzada (SIMULAVA) - Código: 3010192 documentation master file, created by
   sphinx-quickstart on Tue Feb 24 07:21:49 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Simulación Avanzada (SIMULAVA) - Código: 3010192 documentation
==============================================================

Este repositorio contiene los materiales, fundamentos técnicos y metodologías del curso Simulación
Avanzada, impartido en el Departamento de Ciencias de la Computación y la Decisión de la Facultad de
Minas. El curso es dirigido por el F. Javier Díaz S. PhD., Profesor Titular de la Universidad
Nacional de Colombia, Sede Medellín.

Descripción del Curso
---------------------

El curso se centra en el estudio y aplicación de la Simulación de Eventos Discretos como herramienta
crítica para la toma de decisiones en entornos organizacionales. El contenido abarca desde los
fundamentos de probabilidad hasta el modelamiento de sistemas complejos sujetos a incertidumbre y
dinámica.

Objetivos Académicos
--------------------

El propósito principal es desarrollar habilidades para la estructuración de modelos de simulación
que sirvan de apoyo en el análisis y evaluación del comportamiento de organizaciones bajo
condiciones variables. Estas condiciones están caracterizadas por:

* **Incertidumbre.**
* **Dinámica.**
* **Complejidad.**

Programa Temático
-----------------

1. **Fundamentos**: Probabilidad, estadística, riesgo, aleatoriedad y ambigüedad.
2. **Modelamiento de Sistemas**: Traducción del lenguaje natural al lenguaje matemático.
3. **Metodologías de Simulación**:
   * Simulación de Eventos Discretos.
   * Simulación Continua (Dinámica de Sistemas - D.S.).
   * Simulación Basada en Agentes (SBA).
4. **Historia y Métodos Clásicos**: Desde los métodos de Montecarlo y el problema de la aguja de
   Buffon hasta el cálculo de $\pi$.


Metodología de Modelamiento
---------------------------

El proceso de construcción de modelos se rige por el método científico aplicado a la toma de
decisiones, siguiendo seis etapas fundamentales:

1. **Definición del problema** y recolección de información.
2. **Formulación** del modelo de simulación.
3. **Solución** del modelo.
4. **Prueba** del modelo (Validación y Verificación).
5. **Preparación** para la aplicación.
6. **Implantación**.

Estructura Técnica de un Modelo
-------------------------------

Un modelo de simulación se define como una representación idealizada expresada en símbolos
matemáticos y estadísticos. Se clasifican sus componentes en:

Clasificación de Variables
__________________________

* **Variables Exógenas**: Independientes o de entrada al modelo (ej. tiempo entre llegadas, tiempo
  de servicio).
* **Variables de Estado**: Describen la condición del sistema en un tiempo $t$ (ej. número de
  clientes en el sistema o en cola).
* **Variables Endógenas**: Dependientes, generadas por la interacción del sistema (ej. tiempo total
  en el sistema).
* **Parámetros**: Valores estimados como $\lambda$ (tiempo promedio entre llegadas) y $\mu$ (tiempo
  promedio de servicio).

Caso de Estudio: Teoría de Colas
________________________________

El repositorio incluye ejemplos de **Simulación Dinámica Estocástica** aplicados a líneas de espera
(vehículos en una estación de servicio) bajo la lógica **FIFO** (*First In, First Out*).

La relación funcional principal para evaluar el desempeño es el Tiempo Promedio de los clientes en
el Sistema ($TPS$):

$TPS = \frac{1}{n}\sum_{i=1}^{n}TSIS_{i}$

Software y Herramientas
_______________________

Para la implementación de los modelos, se consideran las siguientes herramientas tecnológicas:

* **Lenguajes y Análisis**: R, Excel.

* **Software Especializado**: Simul8, FlexSim.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   src


Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.