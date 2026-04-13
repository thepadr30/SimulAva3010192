<hr style="border:2px solid #CC00FF"> </hr>
<a><img src="https://www.vhv.rs/dpng/d/313-3134285_logo-de-la-universidad-nacional-de-colombia-png.png" width="100" align="center"></a>
<a><img src="https://minaslap.net/pluginfile.php/1/core_admin/logo/0x200/1770226238/Logo%20MinasLAP-3%20%281%29.png" width="100" align="center"></a>
<h1><center>Simulación Avanzada</center></h1>
<h2><center>Tarea 4</center></h2>
<h3><center>Implementación de juegos de azar (parte 1 y 2)</center></h3>

<a name="conte"></a>
<hr style="border:2px solid #CC00FF"> </hr>


**Elaborado por:** _Laura Isabel Greiffenstein Moreno_ & _Kevin Ferney Hidalgo Higuita_

**Correos:** _lgreiffenstein@unal.edu.co_ & _kfhidalgoh@unal.edu.co_

**Fecha de elaboración:** _2026 Marzo 28_

**Fecha última modificación:** _2026 Marzo 28_

---

<h2><center>Tabla de contenido</center></h2>

- [Objetivo](#objetivo)
- [Parte 1](#parte-1)
- [Parte 2](#parte-2)
- [Parte 3](#parte-3)
- [Desarrollo](#desarrollo)
  - [Excavación en el Valle de los Reyes](#excavación-en-el-valle-de-los-reyes)

---

## Objetivo

En esta tarea, los estudiantes tendrán la oportunidad de integrar de manera práctica los conceptos
fundamentales de probabilidad, variables aleatorias y simulación, mediante el diseño, análisis e
implementación de un juego de azar.
La actividad está pensada como un ejercicio técnico, y como una experiencia creativa aplicada, donde
cada estudiante (o grupo máximo de dos estudiantes) construirá un sistema aleatorio desde cero,
definiendo sus reglas, su lógica de funcionamiento y las variables de interés que permitirán
analizar su comportamiento.
A lo largo del desarrollo del taller, se espera que comprendan que detrás de cualquier juego de azar
existe una estructura probabilística que puede ser modelada, simulada y estudiada rigurosamente. En
este sentido, el objetivo no es únicamente “jugar” sino, además, entender, modelar y explicar el
fenómeno aleatorio que subyace en el sistema diseñado.
Adicionalmente, el uso de herramientas computacionales permitirá observar cómo, a través de la
simulación, es posible aproximar distribuciones de probabilidad, estimar medidas estadísticas y
analizar estrategias o comportamientos del juego bajo diferentes escenarios.
Este ejercicio busca fortalecer cuatro competencias: (i) el pensamiento probabilístico, (ii) la
modelación de sistemas aleatorios, (iii) la interpretación de resultados simulados, (iv) y la
capacidad de comunicar ideas de forma clara y estructurada.
Finalmente, se invita a los estudiantes a asumir este reto con creatividad, rigor y criterio
analítico, entendiendo que la simulación no solo es una herramienta académica, sino un instrumento
poderoso para la toma de decisiones en contextos reales.

## Parte 1

Diseñar un juego de azar que permita simular sus posibles resultados. Deberá dejar en claro el juego
con sus reglas y supuestos para que sea entendible para cualquier jugador. Las reglas del juego las
deberá acompañar de un ejercicio que le permita simular los resultados en algún paquete de software.
Utilice también un diagrama de flujo y opcional un pseudo-código para que pueda elaborar su algoritmo
y apoyar la sustentación de este en clase (revise una presentación sobre notas de elaboración de un
diagrama de flujo y pseudocódigo que habíamos cargado previamente en MinasLap).

## Parte 2

Defina por lo menos una variable aleatoria de interés (pueden ser dos o más) que pueda ser estudiada
en el juego, con sus probabilidades, distribución de probabilidad, esperanza, varianza y desviación
estándar, y otras medidas de tendencia central y variabilidad que considere pertinente.

## Parte 3

Implementar el desarrollo de juego en algún paquete de software acompañado de su diagrama de flujo o
pseudocódigo y el proceso simulado en el software, que sea funcional para cuando lo esté presentando.

## Desarrollo

### Excavación en el Valle de los Reyes

**Objetivo del juego**
El jugador asume el papel de un arqueólogo financiando una expedición. El objetivo es encontrar
reliquias, pesarlas y venderlas al museo para recuperar el costo de la expedición y obtener la mayor
ganancia posible.

**Mecánica y Reglas Explícitas**
  1. Costo de Expedición: El jugador paga una tarifa fija de 35 monedas para iniciar la ronda.
  2. Fase de Búsqueda: El jugador excava y encuentra un número aleatorio de reliquias. Es posible no
     encontrar ninguna (0 reliquias).
  3. Fase de Pesaje: Cada reliquia encontrada tiene un peso aleatorio en kilogramos (kg).
  4. Fase de Tasación: El museo compra las reliquias a un precio fijo de 5 monedas por kg. El valor
     base del premio es la suma del peso de todas las reliquias multiplicado por 5.
  5. Bono del "Ídolo de Oro": Al final de la tasación, el jugador lanza un dado de 20 caras. Si saca
     un 20 exacto, descubre el Ídolo de Oro y el museo duplica el valor total de su recompensa.
     Cualquier otro resultado mantiene la recompensa base.

**Diagrama de flujo**

![DigramaFlujoExcavacionValleReyes][img1]

**Variables de interés y supuestos estadísticos**

Para modelar este sistema de forma rigurosa, definimos tres variables aleatorias principales que controlan la incertidumbre del juego.
  * Número de reliquias encontradas ($X$):
    - Tipo: Discreta.
    - Distribución: Poisson.
    - Parámetro: $\lambda = 3$ (esperanza de 3 reliquias por expedición).
    <!-- - Justificación: La distribución de Poisson es ideal para modelar el conteo de eventos independientes que ocurren en un intervalo de tiempo o espacio fijo (una expedición). -->
    Modela el número de hallazgos por expedición. Se utiliza distribución Poisson por tratarse de un
    conteo de eventos aleatorios en un intervalo fijo. El valor $\lambda = 3$ representa el promedio
    esperado de reliquias y es definido por el diseñador del juego.

  * Peso de cada reliquia ($W_i$):
    - Tipo: Continua.
    - Distribución: Exponencial.
    - Parámetro: Media $\beta = 2$ kg (tasa o rate $\lambda_w = 0.5$).
    <!-- - Justificación: La distribución exponencial modela variables estrictamente positivas donde los valores pequeños o medianos son más comunes, pero existe la posibilidad remota de encontrar una reliquia extremadamente pesada. -->
    Modela el peso de las reliquias, que siempre es positivo. La distribución exponencial permite
    representar muchos valores pequeños y algunos valores grandes poco frecuentes. La media de 2 kg
    es una decisión del diseñador para definir un escenario plausible.

  * Bono del Ídolo de Oro ($B$):
    - Tipo: Discreta (Binaria).
    - Distribución: Bernoulli.
    - Parámetro: $p = 0.05$ (1 entre 20).
    <!-- - Justificación: Modela un evento dicotómico clásico (éxito/fracaso) independiente de los hallazgos anteriores, añadiendo volatilidad y emoción al final del juego. -->
    Modela la ocurrencia del bono (1 si ocurre, 0 si no). Se usa Bernoulli por ser un evento de dos
    resultados posibles. La probabilidad del 5% refleja un evento raro, definido por el diseñador
    del juego.

En conjunto, las distribuciones y sus parámetros son elecciones del diseñador que permiten
representar la incertidumbre del sistema de forma coherente y controlada.

<!-- 1. Diagrama de flujo
A continuación, se presenta la lógica estructurada por nodos para la ejecución de una ronda: -->


<!-- ![digramaFlujoExcavacionValleReyes](digramaFlujoExcavacionValleReyes.png) -->

**Metodología y contexto**

El juego “Excavación en el Valle de los Reyes” fue modelado como un sistema probabilístico con tres fuentes de incertidumbre: el número de reliquias (X∼Poisson(3)), el peso de cada reliquia (Wi∼Exponencial(2)) y la ocurrencia del bono (B∼Bernoulli(0.05)). Estos supuestos corresponden a decisiones del diseñador del juego, quien define el comportamiento del sistema y su nivel de variabilidad.

Debido a la complejidad del modelo, se utilizó simulación Monte Carlo, ejecutando 10,000 iteraciones del juego. Esto permitió estimar empíricamente métricas como la ganancia promedio y la probabilidad de ganar, y validar los resultados teóricos.


---
[img1]: digramaFlujoExcavacionValleReyes.png "DiagramaFlujoExcavacionValleReyes"