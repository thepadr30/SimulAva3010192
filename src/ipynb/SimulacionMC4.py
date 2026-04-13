#%%
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simulación Monte Carlo
Este archivo será el entorno de desarrollo donde se implementará la prueba técnica de analítica
empresarial, siguiendo las instrucciones y objetivos definidos en el documento
Prueba_técnica_analítica_Analítica_Empresarial.docx.

Proyecto: 3010192 Simulación Avanzada

Tema: Simulación Monte Carlo

Programa: SimulacionMC.py

Soporte: kfhidalgoh@unal.edu.co

version: 1.0.0

lenguaje: Python 3.12
pip
CD: 20260223

LUD: 20260223

Comentarios:
    * 20260223 Kevin Hidalgo -> PEP8.
"""

__authors__ = ["Kevin Hidalgo"]
__contact__ = "kfhidalgoh@unal.edu.co"
__copyright__ = "Copyright 2026"
__credits__ = ["Kevin Hidalgo"]
__email__ = "kfhidalgoh@unal.edu.co"
__status__ = "Desarrollo"
__version__ = "1.0.0"
__date__ = "2026-02-23"

import logging
import os
import sys
import warnings
from time import localtime, strftime, time

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
import itertools
import matplotlib.gridspec as gridspec

from src.graph.fun_graph_matplotlib import FnGraphMat
from src.logs.logger import fn_limpieza_carpeta, setup_logging


__file__ = "SimulacionMCPy"
file_log = os.path.join(
    'D:\SimulAva\logs',
    strftime("%Y%m%d%H%M%S", localtime()) + "_" + __file__ + ".log"
)

# file_log = os.path.join(  # NOSONAR
#     os.path.join(os.path.abspath(os.curdir), 'logs'),
#     strftime("%Y%m%d%H%M%S", localtime()) + "_" + __file__ + ".log"
# )


logger = setup_logging(file_log)
logging.info("Python %s on %s", sys.version, sys.platform)
logging.info("Root: %s", os.getcwd())  # os.path.abspath(os.curdir)
logging.info("Log: %s", file_log)

#%%
##############
# Constantes #
##############

varData = r'D:\SimulAva\data\raw'
grmt = FnGraphMat('dark_style')  # seaborn-v0_8-darkgrid, dark_style
# sns.set_palette("husl")
warnings.filterwarnings('ignore')  # Ignorar warnings no críticos


#%%
##################################################################
# Bloque 1 — Preparación de Datos y Distribución de Probabilidad #
##################################################################

"""
Descripción
En este primer paso vamos a recrear en Python la tabla de frecuencias históricas que se encuentra en
la página 2 de tu documento. Registraremos los niveles de demanda diaria (de 0 a 10 cajas) y su
frecuencia en días (sumando un total de 364 días). A partir de estos datos, calcularemos la
probabilidad simple (frecuencia relativa) y la probabilidad acumulada para cada nivel de demanda.
Justificación
Para aplicar el método de Simulación Monte Carlo, necesitamos definir la distribución de
probabilidad empírica de la variable aleatoria (la demanda de leche). Al calcular las probabilidades
y su forma acumulada, preparamos el terreno para que herramientas de selección aleatoria en Python
(como las de la librería numpy) puedan generar escenarios futuros respetando el comportamiento
histórico del supermercado. Utilizaremos pandas, que es el equivalente natural a dplyr en el
ecosistema de Python, ideal para manipular datos tabulares.
"""

logging.info('1. Definir las listas con los datos históricos extraídos del documento PDF')
ventas_cajas = list(range(11))  # Genera una lista del 0 al 10
numero_dias = [1, 5, 12, 19, 27, 59, 74, 59, 49, 37, 22]

logging.info('2. Crear el DataFrame base con las frecuencias')
tabla_historica = pd.DataFrame({
    'Ventas': ventas_cajas,
    'Dias': numero_dias
})

logging.info('3. Calcular probabilidades usando pandas')
logging.info('Se calcula la probabilidad simple dividiendo los días entre el total de días')
tabla_historica['Probabilidad'] = tabla_historica['Dias'] / tabla_historica['Dias'].sum()

logging.info('Se calcula la probabilidad acumulada usando el método cumsum()')
tabla_historica['Prob_Acumulada'] = tabla_historica['Probabilidad'].cumsum()

logging.info('Se redondean los resultados a 4 decimales para mayor claridad al visualizar')
tabla_historica['Probabilidad'] = tabla_historica['Probabilidad'].round(4)
tabla_historica['Prob_Acumulada'] = tabla_historica['Prob_Acumulada'].round(4)

logging.info('4. Mostrar la tabla resultante en consola para verificar los cálculos')
print("Tabla de Distribución de Probabilidades:")
print(tabla_historica.to_string(index=False)) # Imprimimos sin el índice para que se vea más limpio

logging.info('Validar que la suma total de días es 364 como indica el problema')
total_dias = tabla_historica['Dias'].sum()
print(f"\nTotal de días históricos: {total_dias}")


# %%
###########################################
# Bloque 2: Función Generadora de Demanda #
###########################################
"""
Descripción
En este bloque crearemos la función generar_demanda en Python. Esta función recibirá la cantidad de
días que queremos simular y el DataFrame con las probabilidades (creado en el Bloque 1). Su objetivo
es devolver un arreglo (array) con valores aleatorios de demanda de cajas de leche, respetando
estrictamente la probabilidad de ocurrencia histórica de cada valor.
Justificación
Para la generación de variables aleatorias discretas basadas en una distribución empírica en Python,
la herramienta más eficiente y estándar en la industria es la librería numpy. Específicamente, el
método numpy.random.choice aplica el método de la transformada inversa de forma optimizada y 
vectorizada bajo el capó (el equivalente exacto al sample() de R). Además, aprovecharemos las 
anotaciones de tipo (type hints) nativas de Python 3.12 para que el código sea más robusto y legible.
"""

logging.info('1. Definir la función generadora de demanda con type hints')

def generar_demanda(n_dias: int, tabla_prob: pd.DataFrame) -> np.ndarray:
    """
    Genera una secuencia de demanda diaria simulada.

    Parámetros:
    - n_dias: Cantidad de días a simular (ej. 7 para una semana).
    - tabla_prob: DataFrame con las columnas 'Ventas' y 'Probabilidad'.

    Retorna:
    - Un array de numpy con las demandas simuladas.
    """

    # Extraer los valores posibles y sus probabilidades del DataFrame
    valores_posibles = tabla_prob['Ventas'].to_numpy()
    probabilidades = tabla_prob['Probabilidad'].to_numpy()
    probabilidades = probabilidades / probabilidades.sum()

    # Generar la demanda usando muestreo aleatorio ponderado
    demandas_simuladas = np.random.choice(
        a=valores_posibles,  # Espacio muestral (0 a 10 cajas)
        size=n_dias,  # Cantidad de números a generar
        replace=True,  # Con reemplazo (los valores pueden repetirse)
        p=probabilidades  # Vector de probabilidades simples
    )

    # Retornar el array con las demandas simuladas
    return demandas_simuladas

#%%
#############################################################
# Bloque 3: Lógica de Simulación de Inventario (Una Semana) #
#############################################################

"""
Descripción:
En este bloque construiremos la función simular_semana en Python. Esta función modelará el flujo
diario del inventario durante una semana completa (7 días). Recibirá como parámetros la demanda
simulada de la semana, las entregas programadas (ej. pedidos recibidos el lunes y/o miércoles) y el
inventario sobrante de la semana anterior. Día a día, sumará las entregas al inventario disponible,
restará la demanda y calculará tanto el inventario final como los faltantes, asegurando la regla de
negocio de que los faltantes no se acumulan para el día siguiente.

Justificación:
A diferencia de la generación aleatoria de demanda que se puede vectorizar fácilmente, el cálculo de
inventario tiene una naturaleza secuencial estricta: el inventario inicial del martes depende
directamente del inventario final del lunes. Por ello, el uso de un bucle for estándar en Python
iterando sobre listas es el enfoque algorítmico más lógico y eficiente. Al finalizar la iteración
semanal, consolidamos los resultados en un pandas.DataFrame para facilitar la lectura tabular y
simplificar el cálculo de costos vectorizado que realizaremos en el siguiente bloque.
"""

logging.info('1. Definir la función de simulación semanal con type hints')

def simular_semana(demanda_semana: np.ndarray | list, entregas_semana: list,
                   inv_inicial: int = 0) -> pd.DataFrame:
    """
    Simula el comportamiento del inventario durante 7 días.

    Parámetros:
    - demanda_semana: Array o lista con la demanda de los 7 días.
    - entregas_semana: Lista con la cantidad de cajas recibidas cada día (7 elementos).
    - inv_inicial: Cajas de leche que sobraron del domingo anterior (por defecto 0).

    Retorna:
    - DataFrame de pandas con el balance diario detallado.
    """

    # Inicializar listas para guardar los resultados de cada día
    inv_final = []
    faltantes = []

    # Variable de estado para llevar el control del inventario
    inv_actual = inv_inicial

    # Bucle iterativo para recorrer los 7 días de la semana (0 al 6 en índices de Python)
    for dia in range(7):
        # El inventario disponible en la mañana incluye la entrega de ese día
        inv_disponible = inv_actual + entregas_semana[dia]

        # Demanda específica de este día
        demanda_hoy = demanda_semana[dia]

        # Evaluar si la demanda supera lo que tenemos disponible
        if demanda_hoy > inv_disponible:
            # Registramos cuántas cajas faltaron para cumplir la demanda
            faltantes.append(demanda_hoy - inv_disponible)
            # El inventario queda vacío (los faltantes no generan inventario negativo)
            inv_actual = 0
        else:
            # Se cubre toda la demanda sin problemas
            faltantes.append(0)
            # Descontamos las cajas vendidas del inventario
            inv_actual = inv_disponible - demanda_hoy

        # Guardamos el inventario con el que cierra este día
        inv_final.append(inv_actual)

    # Consolidar los resultados en un DataFrame para su análisis
    df_resultado = pd.DataFrame({
        'Dia': range(1, 8),
        'Entrega': entregas_semana,
        'Demanda': demanda_semana,
        'Inventario_Final': inv_final,
        'Faltante': faltantes
    })

    return df_resultado

#%%
##########################################
# Bloque 4: Cálculo de Costos y Métricas #
##########################################

"""
Descripción:
En este bloque vamos a crear la función evaluar_semana en Python. Esta función tomará como entrada 
el DataFrame generado por la simulación de la semana (Bloque 3) y calculará el desempeño financiero 
y de servicio. Sumará el costo de mantener inventario ($800 por cada caja que quede al final de cada
 día), calculará el costo de suministro ($15,000 fijos por cada día que haya entrega, más $100 por 
 cada caja entregada), e identificará mediante un valor booleano (True/False) si ocurrió algún 
 faltante durante esa semana. Además, extraerá el inventario final del domingo.

Justificación:
Separar la lógica financiera de la lógica de flujo de inventario mantiene el código modular y sigue
las mejores prácticas de ingeniería de software. Utilizaremos las operaciones vectorizadas de pandas
(como .sum() y .any()), las cuales están optimizadas en C por debajo, haciendo que estos cálculos
sean extremadamente rápidos. Esto es vital porque en el Bloque 6 llamaremos a esta función decenas
de miles de veces. Retornaremos un diccionario nativo de Python, que es una estructura ligera y
perfecta para acumular resultados en la simulación de largo plazo.
"""

logging.info('Definir la función para evaluar los costos y métricas con type hints')


def evaluar_semana(df_semana: pd.DataFrame) -> dict:
    """
    Calcula los costos totales y el nivel de servicio de una semana simulada.

    Parámetros:
    - df_semana: DataFrame con los resultados diarios de 'simular_semana'.

    Retorna:
    - Diccionario con los costos, indicador de faltantes y el inventario de traspaso.
    """

    # --- CÁLCULO DE COSTO DE INVENTARIO ---
    # Se cobra $800 por cada caja que permanezca en inventario al final del día
    total_cajas_guardadas = df_semana['Inventario_Final'].sum()
    costo_inventario = total_cajas_guardadas * 800

    # --- CÁLCULO DE COSTO DE ENTREGA ---
    # El costo fijo de $15,000 se aplica por CADA DÍA que se reciba un pedido (> 0)
    dias_con_entrega = (df_semana['Entrega'] > 0).sum()
    costo_fijo_entrega = dias_con_entrega * 15000

    # El costo variable es de $100 por cada unidad recibida en la semana
    total_cajas_entregadas = df_semana['Entrega'].sum()
    costo_variable_entrega = total_cajas_entregadas * 100

    # Costo total de entrega
    costo_entrega_total = costo_fijo_entrega + costo_variable_entrega

    # --- CÁLCULO DEL COSTO TOTAL ---
    costo_total = costo_inventario + costo_entrega_total

    # --- MÉTRICA DE NIVEL DE SERVICIO ---
    # Evaluamos si hubo al menos un día con faltantes en toda la semana
    hubo_faltante = (df_semana['Faltante'] > 0).any()

    # --- INVENTARIO PARA LA PRÓXIMA SEMANA ---
    # El inventario con el que cierra el domingo (último registro, índice -1)
    inv_final_domingo = df_semana['Inventario_Final'].iloc[-1]

    # 2. Retornar un diccionario con los resultados consolidados
    return {
        'Costo_Inventario': costo_inventario,
        'Costo_Entrega': costo_entrega_total,
        'Costo_Total': costo_total,
        'Hubo_Faltante': hubo_faltante,
        'Inv_Traspaso': inv_final_domingo
    }

#%%
#############################################
# Bloque 5: Motor Monte Carlo (100 Semanas) #
#############################################

"""
Descripción:
En este bloque construiremos la función simular_montecarlo en Python. Esta función actuará como el
orquestador principal de nuestra simulación. Ejecutará un bucle de 100 iteraciones (representando
100 semanas), y en cada una llamará secuencialmente a las funciones que ya creamos: generará la
demanda, simulará el inventario diario y evaluará los costos semanales. Es crucial que esta función
pase el inventario final del domingo como el inventario inicial del lunes de la semana siguiente. Al
terminar el ciclo, calculará el costo total acumulado y el porcentaje de semanas que lograron no
tener faltantes (nivel de servicio).

Justificación:
La esencia del método de Monte Carlo radica en la repetición de múltiples escenarios aleatorios para
observar el comportamiento agregado de un sistema bajo incertidumbre. Usar un bucle for a nivel
semanal nos permite capturar el efecto "bola de nieve" del inventario (si me sobra mucha leche esta
semana, la siguiente semana arranco con ventaja o con sobrecosto de almacenamiento). Además,
empaquetar todo esto en una sola función parametrizada por q_lunes y q_miercoles nos da la interfaz
perfecta para ejecutar la búsqueda exhaustiva (Grid Search) en el próximo bloque de manera limpia y
modular.
"""

logging.info('Definir el motor principal de la Simulación Monte Carlo con type hints')

def simular_montecarlo(q_lunes: int, q_miercoles: int, n_semanas: int,
                       tabla_prob: pd.DataFrame) -> dict:
    """
    Ejecuta la simulación de inventario a lo largo de múltiples semanas continuas.

    Parámetros:
    - q_lunes: Cantidad de cajas a pedir el Lunes (día 1).
    - q_miercoles: Cantidad de cajas a pedir el Miércoles (día 3).
    - n_semanas: Horizonte de simulación en semanas (por defecto 100).
    - tabla_prob: DataFrame con la distribución de probabilidad de la demanda.

    Retorna:
    - Diccionario con los resultados consolidados del horizonte de simulación.
    """

    # Estructurar la lista de entregas para los 7 días (L, M, X, J, V, S, D)
    entregas = [q_lunes, 0, q_miercoles, 0, 0, 0, 0]

    # Inicializar variables para acumular los resultados globales
    costo_total_acumulado = 0
    semanas_con_faltantes = 0

    # Según el documento, la simulación inicia un lunes en la mañana sin inventario previo
    inv_inicial_semana = 0

    # Bucle que recorre cada una de las semanas del horizonte de simulación
    for semana in range(n_semanas):

        # Paso A: Generar la demanda aleatoria para los 7 días de esta semana
        demanda_sem = generar_demanda(n_dias=7, tabla_prob=tabla_prob)

        # Paso B: Simular el flujo de inventario con el inventario inicial correspondiente
        df_semana = simular_semana(
            demanda_semana=demanda_sem,
            entregas_semana=entregas,
            inv_inicial=inv_inicial_semana
        )

        # Paso C: Evaluar los costos y verificar si hubo faltantes en esta semana
        metricas_sem = evaluar_semana(df_semana)

        # Paso D: Acumular el costo total de la semana al gran total
        costo_total_acumulado += metricas_sem['Costo_Total']

        # Si la evaluación indica que hubo faltante, sumar 1 al contador
        if metricas_sem['Hubo_Faltante']:
            semanas_con_faltantes += 1

        # Paso E: El inventario final del domingo pasa a ser el inicial del próximo lunes
        inv_inicial_semana = metricas_sem['Inv_Traspaso']

    # Calcular el porcentaje de semanas SIN faltantes (Nivel de Servicio)
    semanas_sin_faltantes = n_semanas - semanas_con_faltantes
    pct_sin_faltantes = (semanas_sin_faltantes / n_semanas) * 100

    # Retornar el resultado final empaquetado
    return {
        'Q_Lunes': q_lunes,
        'Q_Miercoles': q_miercoles,
        'Costo_Total_100_Sem': costo_total_acumulado,
        'Pct_Sin_Faltantes': pct_sin_faltantes
    }

#%%
#########################################
# Bloque 6: Optimización de Estrategias #
#########################################

"""
Descripción:
En este bloque implementaremos un proceso de búsqueda exhaustiva (Grid Search) en Python. 
Definiremos un rango de posibles cantidades de pedido para los días lunes y miércoles. Luego, 
iteraremos sobre todas las combinaciones posibles, ejecutando nuestro motor de simulación de 100 
semanas para cada par de valores. Finalmente, consolidaremos los resultados en un DataFrame de 
Pandas para filtrar las estrategias que cumplen la meta de al menos un 80% de semanas sin faltantes
y ordenar las opciones viables para encontrar la de menor costo.

Justificación:
El uso de bucles anidados en Python para generar la cuadrícula de escenarios, combinado con listas
de diccionarios, es la forma más rápida y pitónica de acumular datos antes de convertirlos a un
DataFrame. Pandas nos permite aplicar filtros y ordenamientos complejos en una sola línea de código,
haciendo que la identificación del óptimo global sea trivial y altamente legible. Fijaremos una
semilla global para garantizar que todas las estrategias se evalúen bajo las mismas condiciones de
demanda aleatoria (comparación justa).
"""

#%%
#########################################
# Bloque 7: Visualización de Resultados #
#########################################

"""
Descripción:
En este último bloque utilizaremos las bibliotecas matplotlib y seaborn de Python para construir dos
visualizaciones clave. La primera será un gráfico de dispersión (scatter plot) que mostrará la
relación entre el Nivel de Servicio (% de semanas sin faltantes) y el Costo Total para todas las 
combinaciones evaluadas, trazando una línea en el umbral crítico del 80%. La segunda gráfica
ilustrará la dinámica del inventario (barras) versus la demanda (línea) día a día durante una semana
típica, aplicando la estrategia óptima ganadora.

Justificación:
seaborn es excelente para gráficos estadísticos rápidos y estéticos, simulando gran parte de la
facilidad declarativa que ofrece ggplot2 en R. Por su parte, matplotlib nos da el control fino para
superponer elementos (como texto de anotaciones o combinar barras con líneas) en la gráfica de la
semana típica. Visualizar estos datos es fundamental para que el administrador del supermercado
entienda el "trade-off" financiero y confíe en la viabilidad operativa de la recomendación antes de
firmar un nuevo contrato.
"""

#%%
########
# main #
########

def main(**kwargs):
    tabla_historica = kwargs.get('tabla_historica', None)
    logging.info("Programa: SimulacionMCPy")
    logging.info('Fijamos una semilla para reproducibilidad en esta prueba puntual')
    np.random.seed(123)

    logging.info('Simulamos la demanda para una semana (7 días) usando la tabla del Bloque 1')
    logging.info("Nota: Asegúrate de tener el DataFrame 'tabla_historica' cargado en memoria")
    demanda_semana_prueba = generar_demanda(n_dias=7, tabla_prob=tabla_historica)

    logging.info('Mostramos el resultado de la prueba en consola')
    print(f"Prueba de demanda para 7 días: {demanda_semana_prueba}")
    logging.info('2. Prueba de la función con el contrato actual planteado en el PDF (30 cajas el '
                 'lunes)')
    logging.info('Usamos una demanda de prueba ficticia (o la del bloque anterior si está en '
                 'memoria)')
    demanda_prueba = [5, 6, 8, 4, 7, 5, 9]

    logging.info('El proveedor entrega 30 cajas el lunes (Día 1) y 0 el resto de la semana')
    entregas_actuales = [30, 0, 0, 0, 0, 0, 0]

    logging.info('Ejecutamos la simulación para esta semana de prueba')
    prueba_semana_df = simular_semana(
        demanda_semana=demanda_prueba,
        entregas_semana=entregas_actuales,
        inv_inicial=0
    )

    logging.info('Mostramos el resultado en consola')
    print("Balance de inventario para una semana de prueba:")
    print(prueba_semana_df.to_string(index=False))

    logging.info('3. Prueba rápida usando el resultado del bloque anterior')
    # NOTA: Asegúrate de tener 'prueba_semana_df' generado en el Bloque 3
    metricas_prueba = evaluar_semana(prueba_semana_df)

    # Mostramos los resultados de la prueba financiera en consola
    print("Métricas calculadas para la semana de prueba:")
    for clave, valor in metricas_prueba.items():
        print(f"{clave}: {valor}")

    logging.info('4. Prueba del motor simulando el contrato actual (30 cajas solo el lunes)')
    logging.info('Fijar semilla para que el resultado de la prueba sea reproducible')
    np.random.seed(42)
    logging.info('Ejecutamos la simulación para 100 semanas con la política actual')
    resultado_contrato_actual = simular_montecarlo(
        q_lunes=30,
        q_miercoles=0,
        n_semanas=100,
        tabla_prob=tabla_historica
    )

    logging.info('Mostrar el resultado del contrato actual en consola')
    print("Resultados de la simulación del contrato actual (30 cajas el lunes) tras 100 semanas:")
    for clave, valor in resultado_contrato_actual.items():
        print(f"{clave}: {valor}")

    logging.info('5. Optimización de estrategias')
    logging.info('Definir el espacio de búsqueda (Grid Search)')
    logging.info('Posibles pedidos en múltiplos de 5 para simplificar la logística')
    posibles_lunes = range(20, 75, 5)  # De 20 a 70 cajas
    posibles_miercoles = range(0, 55, 5)  # De 0 a 50 cajas

    logging.info('Lista para guardar los resultados de cada escenario evaluado')
    resultados_simulacion = []

    logging.info('Fijar semilla global para que las comparaciones sean exactas ante la misma demanda')
    np.random.seed(2026)

    print(f"Evaluando combinaciones de estrategias. Por favor espere...\n")

    logging.info('Bucle anidado para evaluar cada combinación de la cuadrícula')
    for q_l in posibles_lunes:
        for q_m in posibles_miercoles:
            # Ejecutar la simulación para esta combinación (100 semanas)
            # Nota: 'tabla_historica' debe estar en memoria desde el Bloque 1
            resultado_iteracion = simular_montecarlo(
                q_lunes=q_l,
                q_miercoles=q_m,
                n_semanas=100,
                tabla_prob=tabla_historica
            )

            # Agregar el diccionario resultante a nuestra lista
            resultados_simulacion.append(resultado_iteracion)

    logging.info('Consolidar todos los resultados en un único DataFrame de pandas')
    df_resultados_totales = pd.DataFrame(resultados_simulacion)

    logging.info('Filtrar y encontrar la estrategia óptima')
    logging.info('Regla de negocio: Nivel de servicio >= 80%')
    estrategias_viables = df_resultados_totales[df_resultados_totales['Pct_Sin_Faltantes'] >= 80]

    logging.info('Ordenar de menor a mayor costo total')
    analisis_optimo = estrategias_viables.sort_values(by='Costo_Total_100_Sem')

    logging.info('Mostrar las 5 mejores estrategias viables')
    print("Top 5 Mejores Estrategias que cumplen la meta (>= 80%):")
    print(analisis_optimo.head(5).to_string(index=False))

    logging.info('Aislar y mostrar la estrategia campeona (la primera fila tras ordenar)')
    estrategia_campeona = analisis_optimo.iloc[0]

    print("\n" + "=" * 45)
    print("LA ESTRATEGIA ÓPTIMA ES:")
    print(f"Pedir el Lunes: {int(estrategia_campeona['Q_Lunes'])} cajas")
    print(f"Pedir el Miércoles: {int(estrategia_campeona['Q_Miercoles'])} cajas")
    print(f"Costo Total (100 sem): ${estrategia_campeona['Costo_Total_100_Sem']:,.2f}")
    print(f"Nivel de Servicio: {estrategia_campeona['Pct_Sin_Faltantes']}%")
    print("=" * 45 + "\n")

    logging.info('6. Visualizar resultados')
    logging.info('--- GRÁFICO 1: Análisis de Estrategias (Costo vs. Nivel de Servicio) ---')

    logging.info('Preparar los datos para el gráfico')
    logging.info('Clasificar si la estrategia cumple la meta del 80%')
    df_resultados_totales['Viabilidad'] = np.where(
        df_resultados_totales['Pct_Sin_Faltantes'] >= 80,
        'Cumple (>= 80%)',
        'No Cumple (< 80%)'
    )

    logging.info('Identificar la fila exacta de la estrategia óptima para resaltarla')
    optimo_mask = (df_resultados_totales['Q_Lunes'] == estrategia_campeona['Q_Lunes']) & \
                  (df_resultados_totales['Q_Miercoles'] == estrategia_campeona['Q_Miercoles'])
    df_resultados_totales['Es_Optima'] = np.where(optimo_mask, 'Óptima', 'Otras')

    logging.info('Crear la figura del primer gráfico')
    plt.figure(figsize=(10, 6))
    grafico_dispersion = sns.scatterplot(
        data=df_resultados_totales,
        x='Pct_Sin_Faltantes',
        y='Costo_Total_100_Sem',
        hue='Viabilidad',
        palette={'Cumple (>= 80%)': 'steelblue', 'No Cumple (< 80%)': 'gray'},
        style='Es_Optima',
        markers={'Otras': 'o', 'Óptima': '*'},
        sizes={'Otras': 50, 'Óptima': 300},
        size='Es_Optima',
        alpha=0.8
    )

    logging.info('Añadir la línea de restricción del 80%')
    plt.axvline(x=80, color='darkred', linestyle='--', label='Meta 80% Nivel de Servicio')

    logging.info('Configurar textos y leyendas')
    plt.title(
        "Simulación Monte Carlo: Evaluación de Estrategias de Pedido\nCosto Total vs % Semanas sin Faltantes (100 semanas)",
        fontsize=14)
    plt.xlabel("Nivel de Servicio (% Semanas sin Faltantes)", fontsize=12)
    plt.ylabel("Costo Total ($)", fontsize=12)
    # Ajustar formato del eje Y para mostrar moneda
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Mostrar gráfico 1
    plt.show()

    logging.info('--- GRÁFICO 2: Comportamiento del Inventario (Semana Típica con Estrategia Óptima) ---')

    logging.info('Extraer las cantidades óptimas del bloque 6')
    q_lunes_opt = int(estrategia_campeona['Q_Lunes'])
    q_miercoles_opt = int(estrategia_campeona['Q_Miercoles'])
    entregas_optimas = [q_lunes_opt, 0, q_miercoles_opt, 0, 0, 0, 0]

    logging.info('Generar una demanda típica para graficar (fijamos semilla para el ejemplo)')
    np.random.seed(101)
    demanda_tipica = generar_demanda(n_dias=7, tabla_prob=tabla_historica)

    logging.info('Simular esa semana con la estrategia ganadora')
    df_semana_grafico = simular_semana(
        demanda_semana=demanda_tipica,
        entregas_semana=entregas_optimas,
        inv_inicial=0
    )

    # Nombres de los días para el eje X
    dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    # 3. Crear la figura del segundo gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Barras para el inventario final
    ax.bar(dias_nombres, df_semana_grafico['Inventario_Final'], color='dodgerblue', alpha=0.6,
           label='Inventario Final al Cierre')

    # Línea y puntos para la demanda diaria
    ax.plot(dias_nombres, df_semana_grafico['Demanda'], color='darkorange', marker='o', linewidth=2,
            markersize=8, label='Demanda Diaria')

    # Añadir anotaciones de texto en los días que hay entregas
    for i in range(len(df_semana_grafico)):
        entrega_hoy = df_semana_grafico.loc[i, 'Entrega']
        inv_final = df_semana_grafico.loc[i, 'Inventario_Final']
        if entrega_hoy > 0:
            ax.text(i, inv_final + 1.5, f"+{int(entrega_hoy)} cajas", color='darkgreen',
                    fontweight='bold', ha='center', fontsize=10)

    # Configurar textos y leyendas
    ax.set_title(
        f"Dinámica de Inventario - Estrategia Óptima (Lunes: {q_lunes_opt} | Miércoles: {q_miercoles_opt})",
        fontsize=14)
    ax.set_xlabel("Día de la Semana", fontsize=12)
    ax.set_ylabel("Cantidad (Cajas de Leche)", fontsize=12)
    # Límite Y ligeramente más alto para que quepan las anotaciones
    ax.set_ylim(0, max(df_semana_grafico['Inventario_Final'].max(),
                       df_semana_grafico['Demanda'].max()) + 5)
    ax.legend(loc='upper right')

    plt.tight_layout()

    # Mostrar gráfico 2
    plt.show()


if __name__ == "__main__":
    main(tabla_historica=tabla_historica)
    fn_limpieza_carpeta('D:\SimulAva\logs')
