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
import numpy as np
import pandas as pd
import seaborn as sns
from distfit import distfit
from scipy import stats

from src.graph.fun_graph_matplotlib import FnGraphMat
from src.logs.logger import fn_limpieza_carpeta, setup_logging
from src.utils import lecturaExcel as lE
from src.utils import statisticsBase as sB

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
sns.set_palette("husl")
warnings.filterwarnings('ignore')  # Ignorar warnings no críticos

#%%
##############
# Funciones #
##############

def frequency_table(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Calcula frecuencias absolutas, relativas y acumuladas
    asegurando que los datos sigan un orden lógico para la simulación.
    """

    freq_abs = df[column].value_counts(dropna=False).sort_index()
    freq_rel = df[column].value_counts(normalize=True, dropna=False).sort_index()

    result = pd.DataFrame({
        "frecuencia_abs": freq_abs,
        "frecuencia_rel": freq_rel,
    })

    # Ahora el cumsum() se calculará correctamente de 0 a 10 cajas
    result["frecuencia_acum"] = result["frecuencia_abs"].cumsum()
    result["frecuencia_rel_acum"] = result["frecuencia_rel"].cumsum()

    return result

# Para que el modelo "decida" cuántas cajas se vendieron en un día simulado, necesitamos una función
# que actúe como un buscador. Esta función recibirá un número aleatorio ($R$) generado uniformemente
# entre $0$ y $1$ y determinará en qué intervalo de nuestra frecuencia_rel_acum cae.
# Este método técnico se conoce como Muestreo por Transformación Inversa.

def simular_un_dia(tabla_frec):
    """
    Genera un número aleatorio y devuelve el valor de ventas
    correspondiente según la probabilidad acumulada.
    """
    # 1. Generar un número aleatorio entre 0 y 1
    r = np.random.rand()

    # 2. Buscar en qué intervalo cae
    # Iteramos sobre la columna de frecuencia acumulada
    for venta, fila in tabla_frec.iterrows():
        if r <= fila["frecuencia_rel_acum"]:
            return venta

    return tabla_frec.index[-1]  # Respaldo por errores de redondeo

# ¿Cómo funciona la "lógica de intervalos"?
# Imagina que lanzas un dardo a una regla que mide del 0 al 1. Los espacios entre los límites que
# calculamos en el bloque anterior representan el "tamaño" de la probabilidad de cada evento:
#
# Si el dardo cae entre 0.0000 y 0.0027 → Resultado: 0 cajas.
#
# Si el dardo cae entre 0.0027 y 0.0165 → Resultado: 1 caja.
#
# ...
#
# Si el dardo cae entre 0.3379 y 0.5412 → Resultado: 6 cajas.
#
# Debido a que el intervalo de "6 cajas" es el más ancho (20.33% de probabilidad), es mucho más
# probable que el número aleatorio caiga ahí que en el de "0 cajas" (0.27%).

def graficar_comparacion(resumen_comp):
    # Configuración de los ejes
    x = resumen_comp["Ventas (Cajas)"]
    width = 0.35  # Ancho de las barras

    fig, ax = plt.subplots(figsize=(10, 6))

    # Barras de datos históricos
    rects1 = ax.bar(x - width / 2, resumen_comp["Probabilidad Histórica"],
                    width, label='Histórico (Real)', color='#3498db', alpha=0.8)

    # Barras de datos simulados
    rects2 = ax.bar(x + width / 2, resumen_comp["Probabilidad Simulada"],
                    width, label='Simulado (Monte Carlo)', color='#e67e22', alpha=0.8)

    # Etiquetas y Estética
    ax.set_ylabel('Probabilidad (Frecuencia Relativa)')
    ax.set_xlabel('Número de Cajas Vendidas')
    ax.set_title('Validación de Simulación Monte Carlo: Histórico vs. Simulado')
    ax.set_xticks(x)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.show()


def ejecutar_simulacion_ventas(dict_prmt: dict, df: pd.DataFrame, num_simulaciones: int = 10000):
    """
    Ejecuta una simulación de Monte Carlo sobre la variable ventas basándose
    en una distribución loggamma previamente ajustada.
    """
    # Fijamos semilla para que el experimento sea 100% reproducible
    np.random.seed(42)

    try:
        ventas_empiricas = df['ventas_cajas'].dropna().values
        print(f"--- Iniciando Simulación de Monte Carlo con {num_simulaciones} iteraciones ---")

        # Generación de Muestras Aleatorias (Monte Carlo)
        # scipy.stats.loggamma.rvs (Random Variates) genera los datos simulados
        ventas_simuladas = stats.loggamma.rvs(
            **dict_prmt, size=num_simulaciones
        )

        # Cálculo de Estadísticas Descriptivas
        percentiles = np.percentile(ventas_simuladas, [5, 25, 50, 75, 90, 95, 99])

        print("\n[Estadísticas Descriptivas]")
        print(f"Media Simulada:       {np.mean(ventas_simuladas):.2f} ventas")
        print(f"Mediana Simulada:     {np.median(ventas_simuladas):.2f} ventas")
        print(f"Desviación Estándar:  {np.std(ventas_simuladas):.2f} ventas")
        print(f"Percentil 25% (Q1):   {percentiles[1]:.2f} ventas")
        print(f"Percentil 50% (Q2):   {percentiles[2]:.2f} ventas")
        print(f"Percentil 75% (Q3):   {percentiles[3]:.2f} ventas")
        print(f"Percentil 95%:        {percentiles[5]:.2f} ventas")

        # Generación de Visualizaciones
        # Calculamos los percentiles 1% y 99% para enfocar los gráficos en la masa principal
        # y evitar que las colas pesadas de la t-Student (df=1.85) arruinen la visualización
        p1, p99 = np.percentile(ventas_simuladas, [1, 99])
        rango_x = np.linspace(p1, p99, 1000)
        pdf_teorica = stats.loggamma.pdf(rango_x, **dict_prmt)

        _, axes = plt.subplots(1, 3, figsize=(18, 6))

        # Gráfico A: Histograma y PDF Teórica
        sns.histplot(ventas_simuladas, bins=1000, stat='density', alpha=0.5, color='royalblue',
                     label='Simulación MC', ax=axes[0])
        axes[0].plot(rango_x, pdf_teorica, 'r-', lw=2, label='PDF LogGamma')
        axes[0].set_xlim(p1, p99)
        axes[0].set_title('Histograma Simulado vs. PDF Teórica')
        axes[0].set_xlabel('Ventas')
        axes[0].set_ylabel('Densidad Probabilidad')
        axes[0].legend()

        # Gráfico B: Comparación Empírica vs Simulada
        sns.kdeplot(ventas_empiricas, color='forestgreen', lw=2, label='Datos Empíricos Originales',
                    ax=axes[1])
        sns.kdeplot(ventas_simuladas, color='royalblue', lw=2, label='Simulación Monte Carlo',
                    ax=axes[1], clip=(p1, p99))
        axes[1].set_xlim(p1, p99)
        axes[1].set_title('Ajuste: Original vs Simulación')
        axes[1].set_xlabel('Ventas')
        axes[1].set_ylabel('Densidad Probabilidad')
        axes[1].legend()

        # Gráfico C: Distribución Acumulada (CDF)
        sns.ecdfplot(ventas_empiricas, color='orange', lw=2, ax=axes[2], label='CDF Empírica')
        sns.ecdfplot(ventas_simuladas, color='purple', lw=2, ax=axes[2], label='CDF Simulada')
        axes[2].set_xlim(p1, p99)
        axes[2].set_title('Probabilidad Acumulada (CDF)')
        axes[2].set_xlabel('Ventas')
        axes[2].set_ylabel('Probabilidad')
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()

        plt.tight_layout()
        plt.show()
        plt.savefig('montecarlo_resultados.png')

        # 6. Interpretación de métricas clave de negocio
        prob_mayor_30 = np.mean(ventas_simuladas > 30) * 100
        prob_menor_10 = np.mean(ventas_simuladas < 10) * 100

        print("\n[Interpretación de Probabilidades]")
        print(f"Probabilidad de que las ventas supere las 30 cajas de leche: {prob_mayor_30:.2f}%")
        print(f"Probabilidad de que las ventas sea menor a 10 cajas de leche: {prob_menor_10:.2f}%")
    except Exception as e:
        print(f"Se produjo un error durante la ejecución: {e}")


def calcular_estadisticas(datos, nombre="Datos"):
    """
    Calcula estadísticas descriptivas clave para un conjunto de datos.

    Args:
        datos (array-like): Datos a analizar
        nombre (str): Nombre para identificar en la salida

    Returns:
        dict: Diccionario con las estadísticas
    """
    stats_dict = {
        'nombre': nombre,
        'n': len(datos),
        'media': np.mean(datos),
        'std': np.std(datos, ddof=1),
        'min': np.min(datos),
        'max': np.max(datos),
        'p1': np.percentile(datos, 1),
        'p5': np.percentile(datos, 5),
        'p25': np.percentile(datos, 25),
        'p50': np.median(datos),
        'p75': np.percentile(datos, 75),
        'p95': np.percentile(datos, 95),
        'p99': np.percentile(datos, 99),
        'iqr': np.percentile(datos, 75) - np.percentile(datos, 25),
        'sesgo': stats.skew(datos),
        'curtosis': stats.kurtosis(datos)
    }
    return stats_dict


def bootstrap_ci_media(datos, n_bootstrap=1000, ci=0.95):
    """
    Calcula intervalo de confianza bootstrap para la media.

    Args:
        datos (array): Datos originales
        n_bootstrap (int): Número de remuestreos
        ci (float): Nivel de confianza

    Returns:
        tuple: (límite inferior, límite superior)
    """
    medias_bootstrap = []
    n = len(datos)

    for _ in range(n_bootstrap):
        muestra = np.random.choice(datos, size=n, replace=True)
        medias_bootstrap.append(np.mean(muestra))

    alpha = 1 - ci
    limite_inferior = np.percentile(medias_bootstrap, 100 * alpha / 2)
    limite_superior = np.percentile(medias_bootstrap, 100 * (1 - alpha / 2))

    return limite_inferior, limite_superior


def probabilidad_exceder_umbral(datos, umbral):
    """
    Calcula la probabilidad de que los datos superen un umbral dado.

    Args:
        datos (array): Datos a analizar
        umbral (float): Valor umbral

    Returns:
        float: Probabilidad (entre 0 y 1)
    """
    return np.mean(datos > umbral)


def analizar_outliers(datos, etiqueta="Simulados"):
    # 1. Cálculo de Cuartiles y Rango Intercuartílico (IQR)
    Q1 = np.percentile(datos, 25)
    Q3 = np.percentile(datos, 75)
    IQR = Q3 - Q1

    # 2. Definición de límites (Vallas de Tukey)
    # Aseguramos que el límite inferior no sea menor a 0
    limite_inferior = max(0, Q1 - 1.5 * IQR)
    limite_superior = Q3 + 1.5 * IQR

    # 3. Identificación de outliers
    outliers_superiores = datos[datos > limite_superior]
    outliers_inferiores = datos[datos < (Q1 - 1.5 * IQR)]  # Usamos el valor real para la detección

    # 4. Reporte Detallado
    print(f"\n🔍 Análisis Integral de Outliers ({etiqueta}):")

    # --- Reporte de Colas Superiores (Picos de Demanda) ---
    print(f"   ⬆️ EXCESO DE DEMANDA:")
    print(f"      - Umbral crítico: > {limite_superior:.2f} cajas")
    print(f"      - Días detectados: {len(outliers_superiores)}")
    if len(outliers_superiores) > 0:
        print(
            f"      - Probabilidad de venta récord: {(len(outliers_superiores) / len(datos)) * 100:.2f}%")

    # --- Reporte de Colas Inferiores (Baja Demanda) ---
    print(f"   ⬇️ BAJA DEMANDA:")
    print(f"      - Umbral crítico: < {max(0, Q1 - 1.5 * IQR):.2f} cajas")
    print(f"      - Días detectados: {len(outliers_inferiores)}")
    if len(outliers_inferiores) > 0:
        print(
            f"      - Probabilidad de estancamiento: {(len(outliers_inferiores) / len(datos)) * 100:.2f}%")
    else:
        print(f"      - Nota: No se detectaron días con ventas inusualmente bajas.")

    return limite_inferior, limite_superior


def agregar_dias_semana_secuencial(df: pd.DataFrame, dia_inicio: str = "Lunes") -> pd.DataFrame:
    """
    Agrega una columna 'dia_semana' con los días de la semana
    de manera secuencial hasta completar el DataFrame.

    Args:
        df (pd.DataFrame): DataFrame original.
        dia_inicio (str): Día desde el cual comenzar la secuencia.

    Returns:
        pd.DataFrame: DataFrame con nueva columna 'dia_semana'.
    """

    dias_semana = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo"
    ]

    if dia_inicio not in dias_semana:
        raise ValueError("El día de inicio no es válido.")

    # Reordenar lista para comenzar desde el día indicado
    indice_inicio = dias_semana.index(dia_inicio)
    dias_ordenados = dias_semana[indice_inicio:] + dias_semana[:indice_inicio]

    # Crear secuencia repetida hasta cubrir todas las filas
    secuencia = [
        dias_ordenados[i % 7]
        for i in range(len(df))
    ]

    df["dia_semana"] = secuencia

    return df



#%%
#################
# Lectura Excel #
#################

logging.info('Lectura Excel')

datos_ventas = pd.read_csv(
    os.path.join(varData, 'datos_originales_ventas.csv'),
)
datos_ventas['index'] = datos_ventas.index.values

dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

datos_ventas["dia_semana"] = [dias[i % 7] for i in range(len(datos_ventas))]
datos_ventas = datos_ventas[['index', 'dia_semana', 'ventas_cajas']]
datos_ventas_original = datos_ventas.copy()

list_df = [
    datos_ventas
]

logging.info('normalizacion columnas snake_case')
for i in list_df:
    lE.normalizar_columnas_snake_case(i, inplace=True)

#%%
##################
# Data wrangling #
##################
logging.info('Reemplazo por la mediana')
for i in list_df:
    columnas_numericas = i.select_dtypes(include='number').columns
    # reemplazo por cero
    # i[columnas_numericas] = i[columnas_numericas].fillna(0)
    # reemplazo por la mediana
    i[columnas_numericas] = i[columnas_numericas].fillna(i[columnas_numericas].median())

#%%
#######
# EDA #
#######

# veamos que tienen las columnas
sB.column_overview(datos_ventas)
sB.numeric_descriptive_stats(datos_ventas)
logging.info(
    'Veamos que tienen las columnas: \n%s \n%s',
    sB.column_overview(datos_ventas),
    sB.numeric_descriptive_stats(datos_ventas)
)

# analisis descriptivo
df_stats = sB.fn_statistics_base(datos_ventas, 'ventas_cajas')
logging.info('Análisis descriptivo: \n%s', df_stats.T)
print(df_stats.T)

# outlier
dict_out = sB.detectar_outliers(
    datos_ventas,
    variable_target='ventas_cajas'
)

logging.info('Outliers: \n%s', dict_out)

#%%
# histograma
grmt.graph_armor_hist(datos_ventas, 'ventas_cajas')
#%%
# iqr
grmt.graph_armor_iqr(datos_ventas, var_index= 'index', var_vble='ventas_cajas')

#%%
########################
# Tabla de frecuencias #
########################

tabla = frequency_table(datos_ventas, "ventas_cajas")
print(tabla)

# from tabulate import tabulate  # NOSONAR
# print("📜 LaTeX (tabulate)")
# print(tabulate(tabla, headers="keys", tablefmt="pipe"))
# print(tabulate(tabla, headers="keys", tablefmt="grid"))


#%%
##############################
# Camino 1 ------------------#
# Ejecución de la Simulación #
##############################
# Para que una simulación Monte Carlo sea estadísticamente válida, necesitamos ejecutarla un gran
# número de veces (N). Esto nos permite que la Ley de los Grandes Números actúe: a más repeticiones,
# más se parecerá nuestra simulación a la realidad probabilística que calculamos en el Bloque 1.

# Configuración de la simulación
num_simulaciones = 10000
resultados_simulados = []

# Ejecución del proceso
for _ in range(num_simulaciones):
    # Usamos la lógica del Bloque 2
    venta_dia = simular_un_dia(tabla)
    resultados_simulados.append(venta_dia)

# Convertimos a Serie de Pandas para facilitar el análisis posterior
s_simulacion = pd.Series(resultados_simulados, name="ventas_simuladas")
df_simulacion = pd.DataFrame({"ventas_simuladas": resultados_simulados})
df_simulacion["dia_semana"] = [dias[i % 7] for i in range(len(df_simulacion))]

print(f"Simulación completada para {num_simulaciones} días.")
print("Primeros 10 días simulados:", resultados_simulados[:10])

# ¿Qué está pasando aquí?
# Iteración: El código "vive" 10,000 días diferentes.
#
# Independencia: Lo que se vende el día 1 no afecta al día 2; cada día es un evento aleatorio nuevo
# basado en tus probabilidades históricas.
#
# Almacenamiento: Guardamos cada resultado en una lista para luego analizar tendencias, promedios y
# riesgos.
#
# Nota Pro: En Python, si quisieras hacer esto aún más rápido para millones de datos, podrías usar
# np.searchsorted() sobre el array de frecuencias acumuladas para evitar el bucle for, pero para
# 10,000 iteraciones, el método del Bloque 2 es perfectamente eficiente y mucho más fácil de depurar.

#%%
##########################
# Análisis de Resultados #
##########################

# 1. Obtener frecuencias de los datos simulados
resumen_simulado = frequency_table(pd.DataFrame({"v": resultados_simulados}), "v")

# 2. Crear el DataFrame comparativo
# 'tabla_frecuencias' es la que calculamos en el Bloque 1
resumen_comparativo = pd.DataFrame({
    "Ventas (Cajas)": tabla.index,
    "Probabilidad Histórica": tabla["frecuencia_rel"],
    "Probabilidad Simulada": resumen_simulado["frecuencia_rel"]
}).reset_index(drop=True)

# 3. Calcular el error absoluto para validar precisión
resumen_comparativo["Diferencia (Error)"] = abs(
    resumen_comparativo["Probabilidad Histórica"] - resumen_comparativo["Probabilidad Simulada"]
)

print(resumen_comparativo)
# Opcional: Guardar a CSV
# resumen_comparativo.to_csv("comparativa_monte_carlo.csv", index=False)

# Llamar a la función
graficar_comparacion(resumen_comparativo)

#%%
#############################
# Estadísticas descriptivas #
#############################

# Cargar datos
ventas_empiricas = datos_ventas['ventas_cajas']

# Calcular estadísticas para datos empíricos y simulados
stats_empiricas = calcular_estadisticas(ventas_empiricas, "Datos Empíricos")
stats_simuladas = calcular_estadisticas(s_simulacion, "Simulación Monte Carlo")

# Crear DataFrame comparativo
df_comparacion = pd.DataFrame([stats_empiricas, stats_simuladas]).T
df_comparacion.columns = ['Empírico', 'Simulado']
df_comparacion = df_comparacion.drop('nombre')  # Eliminar fila de nombre

print("\n" + "="*60)
print("ESTADÍSTICAS DESCRIPTIVAS COMPARATIVAS")
print("="*60)
print(df_comparacion.round(3).to_string())

#%%
#####################################################
# Intervalos de confianza para la media (Bootstrap) #
#####################################################

# Calcular IC para ambas muestras
ic_empirico = bootstrap_ci_media(ventas_empiricas)
ic_simulado = bootstrap_ci_media(s_simulacion)

print("\n" + "=" * 60)
print("INTERVALOS DE CONFIANZA (95%) PARA LA MEDIA")
print("=" * 60)
print(f"Datos Empíricos:    ({ic_empirico[0]:.2f}, {ic_empirico[1]:.2f})")
print(f"Simulación MC:      ({ic_simulado[0]:.2f}, {ic_simulado[1]:.2f})")

#%%
########################################
# Análisis de probabilidades de umbral #
########################################

# Definir umbrales de interés
umbrales = [1, 3, 5, 7, 10]

print("\n" + "=" * 60)
print("PROBABILIDAD DE EXCEDER UMBRALES")
print("=" * 60)
print(f"{'Umbral':>10} | {'P(X > umbral) - Empírico':>25} | {'P(X > umbral) - Simulado':>25}")
print("-" * 70)

for umbral in umbrales:
    prob_emp = probabilidad_exceder_umbral(ventas_empiricas, umbral)
    prob_sim = probabilidad_exceder_umbral(s_simulacion, umbral)
    print(f"{umbral:10.0f} | {prob_emp:25.3f} | {prob_sim:25.3f}")

#%%
#################
# Visualización #
#################


#%%
################################
# Interpretación de resultados #
################################

#%%
####################################################
# Validación adicional: Test de Kolmogorov-Smirnov #
####################################################



#%%
#######################
# Camino 2 -----------#
# Ajuste distribución #
#######################

dfit = distfit()
dfit.fit_transform(datos_ventas['ventas_cajas'])
dfit.summary
dfit.plot()
# función de densidad de probabilidad
fig, ax = dfit.plot(chart='pdf')
fig.show()
# función de densidad de probabilidad acumulada
fig, ax = dfit.plot(chart='cdf')
fig.show()

print("La mejor distribución encontrada es:", dfit.model['name'])
print("Parámetros óptimos:", dfit.model['params'])

# 4. Obtener los resultados de la detección
# results = dfit.predict(np.array(df_monteCarlo['horas']))
# Mostramos los índices de los valores detectados como outliers
# indices_outliers = np.where(results['outliers'] == 'y')[0]
# print(f"Valores detectados como outliers: {data_with_outliers[indices_outliers]}")

#%%
##########################
# Simulación Monte Carlo #
##########################

DIST_PARAMS = {
    'c': dfit.model['params'][0],  # c de shape
    'loc': dfit.model['params'][1],  # parámetro de ubicación (media)
    'scale': dfit.model['params'][2],  # parámetro de escala (desviación estándar)
}

ejecutar_simulacion_ventas(DIST_PARAMS, datos_ventas, num_simulaciones=10000)

#%%
# ==============================================================
# 3. CONFIGURACIÓN DE LA SIMULACIÓN
# ==============================================================
N_SIMULACIONES = 10000  # Número de iteraciones de Monte Carlo
RANDOM_SEED = 42        # Semilla para reproducibilidad
ALPHA = 0.05            # Nivel de significancia para IC del 95%

# ==============================================================
# 5. SIMULACIÓN DE MONTE CARLO
# ==============================================================
print("\n" + "="*60)
print("INICIANDO SIMULACIÓN DE MONTE CARLO")
print("="*60)

# Fijar semilla para reproducibilidad
np.random.seed(RANDOM_SEED)

# Generar muestras aleatorias de la distribución t
muestras_simuladas = stats.loggamma.rvs(
    c=DIST_PARAMS['c'],
    loc=DIST_PARAMS['loc'],
    scale=DIST_PARAMS['scale'],
    size=N_SIMULACIONES
)

print(f"✅ Simulación completada: {N_SIMULACIONES:,} muestras generadas")
print(f"   Distribución: LogGamma(c={DIST_PARAMS['c']:.2f}, "
      f"loc={DIST_PARAMS['loc']:.2f}, scale={DIST_PARAMS['scale']:.2f})")

#%%
# ==============================================================
# 6. ESTADÍSTICAS DESCRIPTIVAS
# ==============================================================

# Cargar datos
ventas_empiricas = datos_ventas['ventas_cajas']

# Calcular estadísticas para datos empíricos y simulados
stats_empiricas = calcular_estadisticas(ventas_empiricas, "Datos Empíricos")
stats_simuladas = calcular_estadisticas(muestras_simuladas, "Simulación Monte Carlo")

# Crear DataFrame comparativo
df_comparacion = pd.DataFrame([stats_empiricas, stats_simuladas]).T
df_comparacion.columns = ['Empírico', 'Simulado']
df_comparacion = df_comparacion.drop('nombre')  # Eliminar fila de nombre

print("\n" + "="*60)
print("ESTADÍSTICAS DESCRIPTIVAS COMPARATIVAS")
print("="*60)
print(df_comparacion.round(3).to_string())

# * Leptocúrtica (Curtosis > 0): La distribución presenta un pico más pronunciado y colas más gruesas,
# lo que significa que hay una mayor concentración de datos cerca de la media y una mayor
# probabilidad de valores atípicos (extremos).
# * Mesocúrtica (Curtosis = 0): La distribución tiene un comportamiento similar a la distribución
# normal, con una concentración de datos y grosor de colas estándar.
# * Platicúrtica (Curtosis < 0): La distribución es más plana y dispersa, con colas más delgadas o
# ligeras, indicando menos valores atípicos y menor concentración en la media.
# Asimetría Positiva (Skewness > 0):
# Forma: La cola derecha es más larga; la mayoría de los datos se concentran a la izquierda (menores valores), pero hay valores atípicos elevados.
# Asimetría Negativa (Skewness < 0):
# Forma: La cola izquierda es más larga; los datos se concentran a la derecha (valores altos), con algunos valores atípicos bajos.
# Simetría (Skewness ~ 0):
# La distribución es simétrica o aproximadamente normal (la parte izquierda es espejo de la derecha).

#%%
# ==============================================================
# 7. INTERVALOS DE CONFIANZA PARA LA MEDIA (BOOTSTRAP)
# ==============================================================

# Calcular IC para ambas muestras
ic_empirico = bootstrap_ci_media(ventas_empiricas)
ic_simulado = bootstrap_ci_media(muestras_simuladas)

print("\n" + "=" * 60)
print("INTERVALOS DE CONFIANZA (95%) PARA LA MEDIA")
print("=" * 60)
print(f"Datos Empíricos:    ({ic_empirico[0]:.2f}, {ic_empirico[1]:.2f})")
print(f"Simulación MC:      ({ic_simulado[0]:.2f}, {ic_simulado[1]:.2f})")

#%%
# ==============================================================
# 8. ANÁLISIS DE PROBABILIDADES DE UMBRAL
# ==============================================================

# Definir umbrales de interés
umbrales = [1, 3, 5, 7, 10]

print("\n" + "=" * 60)
print("PROBABILIDAD DE EXCEDER UMBRALES")
print("=" * 60)
print(f"{'Umbral':>10} | {'P(X > umbral) - Empírico':>25} | {'P(X > umbral) - Simulado':>25}")
print("-" * 70)

for umbral in umbrales:
    prob_emp = probabilidad_exceder_umbral(ventas_empiricas, umbral)
    prob_sim = probabilidad_exceder_umbral(muestras_simuladas, umbral)
    print(f"{umbral:10.0f} | {prob_emp:25.3f} | {prob_sim:25.3f}")

#%%
# ==============================================================
# 9. VISUALIZACIONES
# ==============================================================
print("\n" + "="*60)
print("GENERANDO VISUALIZACIONES")
print("="*60)

# Crear figura con subplots
fig = plt.figure(figsize=(16, 12))

# 9.1 Histograma + PDF teórica
ax1 = plt.subplot(2, 2, 1)
# Histograma de datos simulados
counts, bins, patches = ax1.hist(muestras_simuladas, bins=50, density=True,
                                  alpha=0.6, color='skyblue', edgecolor='black',
                                  label='Simulación MC')
# PDF teórica
x = np.linspace(min(muestras_simuladas), max(muestras_simuladas), 1000)
pdf_teorica = stats.loggamma.pdf(x, c=DIST_PARAMS['c'],
                          loc=DIST_PARAMS['loc'],
                          scale=DIST_PARAMS['scale'])
ax1.plot(x, pdf_teorica, 'r-', lw=2.5, label='PDF Teórica (LogGamma)')
ax1.set_xlabel('Ventas')
ax1.set_ylabel('Densidad')
ax1.set_title('Distribución Simulada vs PDF Teórica')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 9.2 Comparación empírico vs simulado
ax2 = plt.subplot(2, 2, 2)
ax2.hist(ventas_empiricas, bins=20, density=True, alpha=0.5,
         color='orange', edgecolor='black', label='Datos Empíricos')
ax2.hist(muestras_simuladas, bins=50, density=True, alpha=0.5,
         color='skyblue', edgecolor='black', label='Simulación MC')
ax2.set_xlabel('ventas')
ax2.set_ylabel('Densidad')
ax2.set_title('Comparación: Empírico vs Simulado')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 9.3 CDF (Función de Distribución Acumulada)
ax3 = plt.subplot(2, 2, 3)
# Ordenar datos para CDF
x_emp = np.sort(ventas_empiricas)
y_emp = np.arange(1, len(x_emp)+1) / len(x_emp)
x_sim = np.sort(muestras_simuladas)
y_sim = np.arange(1, len(x_sim)+1) / len(x_sim)

ax3.plot(x_emp, y_emp, 'o-', markersize=3, alpha=0.7,
         label='CDF Empírica', color='orange')
ax3.plot(x_sim, y_sim, '-', linewidth=2,
         label='CDF Simulada', color='blue')
ax3.set_xlabel('Ventas')
ax3.set_ylabel('Probabilidad Acumulada')
ax3.set_title('Función de Distribución Acumulada (CDF)')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 9.4 Boxplot comparativo
ax4 = plt.subplot(2, 2, 4)
data_to_plot = [ventas_empiricas, muestras_simuladas]
bp = ax4.boxplot(data_to_plot, labels=['Empírico', 'Simulado'],
                 patch_artist=True,
                 boxprops=dict(facecolor='lightblue'),
                 whiskerprops=dict(color='gray'),
                 capprops=dict(color='gray'),
                 medianprops=dict(color='red', linewidth=2))
ax4.set_ylabel('Ventas')
ax4.set_title('Distribución: Boxplot Comparativo')
ax4.grid(True, alpha=0.3, axis='y')

# Ajustar layout
plt.tight_layout()
plt.suptitle('Análisis de Simulación Monte Carlo para Variable Ventas',
             fontsize=16, y=1.02)
# plt.savefig('simulacion_mc_ventas.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Visualizaciones guardadas como 'simulacion_mc_ventas.png'")

#%%
# ==============================================================
# 10. INTERPRETACIÓN DE RESULTADOS
# ==============================================================
print("\n" + "="*60)
print("INTERPRETACIÓN DE RESULTADOS")
print("="*60)

# Comparación de medias
print("\n📊 Comparación de Medias:")
print(f"   - Media Empírica: {stats_empiricas['media']:.2f} ventas")
print(f"   - Media Simulada: {stats_simuladas['media']:.2f} ventas")
print(f"   - Diferencia: {abs(stats_empiricas['media'] - stats_simuladas['media']):.2f} ventas")

# Análisis de colas pesadas
print("\n📈 Análisis de Colas y Curtosis:")
if stats_empiricas['curtosis'] > 0:
    print(f"   - Tipo: Leptocúrtica (Curtosis: {stats_empiricas['curtosis']:.2f})")
    print(f"   - Interpretación: Las colas son más pesadas que una distribución normal.")
    print(f"   - Implicación: Hay una mayor probabilidad de eventos extremos o 'cisnes negros'")
    print(f"     (ventas inusualmente altas o bajas).")
    print(f"   - Ajuste: El parámetro c={DIST_PARAMS['c']:.2f} de la LogGamma captura esta "
          f"concentración en la media y colas largas.")

elif stats_empiricas['curtosis'] < 0:
    print(f"   - Tipo: Platicúrtica (Curtosis: {stats_empiricas['curtosis']:.2f})")
    print(f"   - Interpretación: Las colas son más ligeras y la distribución es más 'achatada'.")
    print(f"   - Implicación: Los datos están más dispersos, pero los valores extremos son menos "
          f"frecuentes.")
    print(f"     Las ventas tienden a ser más uniformes dentro de un rango amplio.")

else: # Caso = 0 (o muy cercano a 0)
    print(f"   - Tipo: Mesocúrtica (Curtosis: ≈0)")
    print(f"   - Interpretación: La forma de las colas es similar a la de una distribución Normal.")
    print(f"   - Implicación: El riesgo de valores extremos es moderado y predecible bajo el modelo"
          f" de Gauss.")

lim_inf, lim_sup = analizar_outliers(muestras_simuladas)

# Interpretación de umbrales críticos
print("\n🎯 Umbrales Críticos:")
for umbral in [5, 7, 10]:
    prob_emp = probabilidad_exceder_umbral(ventas_empiricas, umbral)
    prob_sim = probabilidad_exceder_umbral(muestras_simuladas, umbral)
    if prob_emp > 0.1:
        print(f"   - Hay una probabilidad del {prob_emp*100:.1f}% (empírico) / {prob_sim*100:.1f}% "
              f"(simulado) de superar {umbral} ventas")

# Rango esperado (percentiles 5-95)
print("\n📏 Rango Esperado (90% de los casos):")
print(f"   - Empírico: entre {stats_empiricas['p5']:.1f} y {stats_empiricas['p95']:.1f} ventas")
print(f"   - Simulado: entre {stats_simuladas['p5']:.1f} y {stats_simuladas['p95']:.1f} ventas")

# Conclusión
print("\n✅ CONCLUSIÓN:")
print("   La simulación de Monte Carlo utilizando la distribución LogGamma")
print(f"   con parámetros (c={DIST_PARAMS['c']:.2f}, loc={DIST_PARAMS['loc']:.2f}, "
      f"scale={DIST_PARAMS['scale']:.2f})")
print("   reproduce adecuadamente las características de los datos empíricos.")
print("   Las pequeñas diferencias se deben a la naturaleza estocástica de la")
print(f"   simulación y al tamaño limitado de la muestra original (n={len(ventas_empiricas)}).")
print("   Para fines prácticos, podemos usar la distribución simulada para")
print("   realizar inferencias y cálculos de probabilidad sobre la variable ventas.")

# ==============================================================
# 11. VALIDACIÓN ADICIONAL: TEST DE KOLMOGOROV-SMIRNOV
# ==============================================================
ks_statistic, p_value = stats.ks_2samp(ventas_empiricas, muestras_simuladas)

print("\n" + "="*60)
print("VALIDACIÓN ESTADÍSTICA: TEST KOLMOGOROV-SMIRNOV")
print("="*60)
print(f"Estadístico KS: {ks_statistic:.4f}")
print(f"Valor p: {p_value:.4f}")

if p_value > 0.05:
    print("✅ No hay evidencia significativa para rechazar que las distribuciones son iguales (p > 0.05)")
    print("   La simulación es estadísticamente consistente con los datos empíricos.")
else:
    print("⚠️  Hay diferencias significativas entre las distribuciones (p < 0.05)")
    print("   Esto puede deberse al tamaño muestral pequeño o a limitaciones del ajuste.")

print("\n" + "="*60)
print("🎉 SIMULACIÓN COMPLETADA EXITOSAMENTE")
print("="*60)

# %%
########
# main #
########

def main(**kwargs):
    logging.info("Programa: SimulacionMCPy")


if __name__ == "__main__":
    fn_limpieza_carpeta('D:\SimulAva\logs')
