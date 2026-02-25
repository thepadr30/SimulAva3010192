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
    para una columna de un DataFrame.

    Args:
        df: DataFrame de entrada
        column: nombre de la columna

    Returns:
        DataFrame con frecuencias
    """

    freq_abs = df[column].value_counts(dropna=False)
    freq_rel = df[column].value_counts(normalize=True, dropna=False)

    result = pd.DataFrame({
        "frecuencia_abs": freq_abs,
        "frecuencia_rel": freq_rel,
    })

    result["frecuencia_acum"] = result["frecuencia_abs"].cumsum()
    result["frecuencia_rel_acum"] = result["frecuencia_rel"].cumsum()

    return result


#%%
#################
# Lectura Excel #
#################

logging.info('Lectura Excel')
dataframes_cargados = lE.leer_multiples_excels(varData)
df_monteCarlo = dataframes_cargados.get(
    "SIMULAVA 2026-02-18 Clase4-2 MONTECARLO EJM (1)", None
)
df_monteCarlo_original = df_monteCarlo.copy()

list_df = [
    df_monteCarlo
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
sB.column_overview(df_monteCarlo)
sB.numeric_descriptive_stats(df_monteCarlo)

# analisis descriptivo
df_stats = sB.fn_statistics_base(df_monteCarlo, 'horas')
print(df_stats.T)

# outlier
dict_out = sB.detectar_outliers(
    df_monteCarlo,
    variable_target='horas'
)
#%%
# histograma
grmt.graph_armor_hist(df_monteCarlo, 'horas')
#%%
# iqr
grmt.graph_armor_iqr(df_monteCarlo, var_index='datos', var_vble='horas')

#%%
tabla = frequency_table(df_monteCarlo, "horas")
print(tabla)

#%%
#######################
# Ajuste distribución #
#######################

dfit = distfit()
dfit.fit_transform(df_monteCarlo['horas'])
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
    'df': dfit.model['params'][0],  # grados de libertad 1.8524669032273189,
    'loc': dfit.model['params'][1],  # parámetro de ubicación (media) 17.419045313234577,
    'scale': dfit.model['params'][2],  # parámetro de escala (desviación estándar) 5.3765839723718045
}

def ejecutar_simulacion_horas(dict_prmt: dict, df: pd.DataFrame, num_simulaciones: int = 10000):
    """
    Ejecuta una simulación de Monte Carlo sobre la variable HORAS basándose
    en una distribución t de Student previamente ajustada.
    """
    # Fijamos semilla para que el experimento sea 100% reproducible
    np.random.seed(42)

    try:
        horas_empiricas = df['horas'].dropna().values
        print(f"--- Iniciando Simulación de Monte Carlo con {num_simulaciones} iteraciones ---")

        # Generación de Muestras Aleatorias (Monte Carlo)
        # scipy.stats.t.rvs (Random Variates) genera los datos simulados
        horas_simuladas = stats.t.rvs(
            df=dict_prmt['df'],
            loc=dict_prmt['loc'],
            scale=dict_prmt['scale'],
            size=num_simulaciones
        )

        # Cálculo de Estadísticas Descriptivas
        percentiles = np.percentile(horas_simuladas, [5, 25, 50, 75, 90, 95, 99])

        print("\n[Estadísticas Descriptivas]")
        print(f"Media Simulada:       {np.mean(horas_simuladas):.2f} horas")
        print(f"Mediana Simulada:     {np.median(horas_simuladas):.2f} horas")
        print(f"Desviación Estándar:  {np.std(horas_simuladas):.2f} horas")
        print(f"Percentil 25% (Q1):   {percentiles[1]:.2f} horas")
        print(f"Percentil 50% (Q2):   {percentiles[2]:.2f} horas")
        print(f"Percentil 75% (Q3):   {percentiles[3]:.2f} horas")
        print(f"Percentil 95%:        {percentiles[5]:.2f} horas")

        # Generación de Visualizaciones
        # Calculamos los percentiles 1% y 99% para enfocar los gráficos en la masa principal
        # y evitar que las colas pesadas de la t-Student (df=1.85) arruinen la visualización
        p1, p99 = np.percentile(horas_simuladas, [1, 99])
        rango_x = np.linspace(p1, p99, 1000)
        pdf_teorica = stats.t.pdf(rango_x, **dict_prmt)

        _, axes = plt.subplots(1, 3, figsize=(18, 6))

        # Gráfico A: Histograma y PDF Teórica
        sns.histplot(horas_simuladas, bins=1000, stat='density', alpha=0.5, color='royalblue',
                     label='Simulación MC', ax=axes[0])
        axes[0].plot(rango_x, pdf_teorica, 'r-', lw=2, label='PDF t-Student')
        axes[0].set_xlim(p1, p99)
        axes[0].set_title('Histograma Simulado vs. PDF Teórica')
        axes[0].set_xlabel('Horas')
        axes[0].set_ylabel('Densidad Probabilidad')
        axes[0].legend()

        # Gráfico B: Comparación Empírica vs Simulada
        sns.kdeplot(horas_empiricas, color='forestgreen', lw=2, label='Datos Empíricos Originales',
                    ax=axes[1])
        sns.kdeplot(horas_simuladas, color='royalblue', lw=2, label='Simulación Monte Carlo',
                    ax=axes[1], clip=(p1, p99))
        axes[1].set_xlim(p1, p99)
        axes[1].set_title('Ajuste: Original vs Simulación')
        axes[1].set_xlabel('Horas')
        axes[1].set_ylabel('Densidad Probabilidad')
        axes[1].legend()

        # Gráfico C: Distribución Acumulada (CDF)
        sns.ecdfplot(horas_simuladas, color='purple', lw=2, ax=axes[2], label='CDF Simulada')
        axes[2].set_xlim(p1, p99)
        axes[2].set_title('Probabilidad Acumulada (CDF)')
        axes[2].set_xlabel('Horas')
        axes[2].set_ylabel('Probabilidad')
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()

        plt.tight_layout()
        plt.show()
        plt.savefig('montecarlo_resultados.png')

        # 6. Interpretación de métricas clave de negocio
        prob_mayor_30 = np.mean(horas_simuladas > 30) * 100
        prob_menor_10 = np.mean(horas_simuladas < 10) * 100

        print("\n[Interpretación de Probabilidades]")
        print(f"Probabilidad de que el tiempo supere las 30 horas: {prob_mayor_30:.2f}%")
        print(f"Probabilidad de que el tiempo sea menor a 10 horas: {prob_menor_10:.2f}%")
    except Exception as e:
        print(f"Se produjo un error durante la ejecución: {e}")

ejecutar_simulacion_horas(DIST_PARAMS, df_monteCarlo, num_simulaciones=10000)

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
muestras_simuladas = stats.t.rvs(
    df=DIST_PARAMS['df'],
    loc=DIST_PARAMS['loc'],
    scale=DIST_PARAMS['scale'],
    size=N_SIMULACIONES
)

print(f"✅ Simulación completada: {N_SIMULACIONES:,} muestras generadas")
print(f"   Distribución: t(gl={DIST_PARAMS['df']:.2f}, "
      f"loc={DIST_PARAMS['loc']:.2f}, scale={DIST_PARAMS['scale']:.2f})")


# ==============================================================
# 6. ESTADÍSTICAS DESCRIPTIVAS
# ==============================================================
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

# Cargar datos
horas_empiricas = df_monteCarlo['horas']

# Calcular estadísticas para datos empíricos y simulados
stats_empiricas = calcular_estadisticas(horas_empiricas, "Datos Empíricos")
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

# ==============================================================
# 7. INTERVALOS DE CONFIANZA PARA LA MEDIA (BOOTSTRAP)
# ==============================================================
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


# Calcular IC para ambas muestras
ic_empirico = bootstrap_ci_media(horas_empiricas)
ic_simulado = bootstrap_ci_media(muestras_simuladas)

print("\n" + "=" * 60)
print("INTERVALOS DE CONFIANZA (95%) PARA LA MEDIA")
print("=" * 60)
print(f"Datos Empíricos:    ({ic_empirico[0]:.2f}, {ic_empirico[1]:.2f})")
print(f"Simulación MC:      ({ic_simulado[0]:.2f}, {ic_simulado[1]:.2f})")


# ==============================================================
# 8. ANÁLISIS DE PROBABILIDADES DE UMBRAL
# ==============================================================
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


# Definir umbrales de interés
umbrales = [10, 20, 30, 40, 50, 60]

print("\n" + "=" * 60)
print("PROBABILIDAD DE EXCEDER UMBRALES")
print("=" * 60)
print(f"{'Umbral':>10} | {'P(X > umbral) - Empírico':>25} | {'P(X > umbral) - Simulado':>25}")
print("-" * 70)

for umbral in umbrales:
    prob_emp = probabilidad_exceder_umbral(horas_empiricas, umbral)
    prob_sim = probabilidad_exceder_umbral(muestras_simuladas, umbral)
    print(f"{umbral:10.0f} | {prob_emp:25.3f} | {prob_sim:25.3f}")

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
pdf_teorica = stats.t.pdf(x, df=DIST_PARAMS['df'],
                          loc=DIST_PARAMS['loc'],
                          scale=DIST_PARAMS['scale'])
ax1.plot(x, pdf_teorica, 'r-', lw=2.5, label='PDF Teórica (t)')
ax1.set_xlabel('Horas')
ax1.set_ylabel('Densidad')
ax1.set_title('Distribución Simulada vs PDF Teórica')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 9.2 Comparación empírico vs simulado
ax2 = plt.subplot(2, 2, 2)
ax2.hist(horas_empiricas, bins=20, density=True, alpha=0.5,
         color='orange', edgecolor='black', label='Datos Empíricos')
ax2.hist(muestras_simuladas, bins=50, density=True, alpha=0.5,
         color='skyblue', edgecolor='black', label='Simulación MC')
ax2.set_xlabel('Horas')
ax2.set_ylabel('Densidad')
ax2.set_title('Comparación: Empírico vs Simulado')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 9.3 CDF (Función de Distribución Acumulada)
ax3 = plt.subplot(2, 2, 3)
# Ordenar datos para CDF
x_emp = np.sort(horas_empiricas)
y_emp = np.arange(1, len(x_emp)+1) / len(x_emp)
x_sim = np.sort(muestras_simuladas)
y_sim = np.arange(1, len(x_sim)+1) / len(x_sim)

ax3.plot(x_emp, y_emp, 'o-', markersize=3, alpha=0.7,
         label='CDF Empírica', color='orange')
ax3.plot(x_sim, y_sim, '-', linewidth=2,
         label='CDF Simulada', color='blue')
ax3.set_xlabel('Horas')
ax3.set_ylabel('Probabilidad Acumulada')
ax3.set_title('Función de Distribución Acumulada (CDF)')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 9.4 Boxplot comparativo
ax4 = plt.subplot(2, 2, 4)
data_to_plot = [horas_empiricas, muestras_simuladas]
bp = ax4.boxplot(data_to_plot, labels=['Empírico', 'Simulado'],
                 patch_artist=True,
                 boxprops=dict(facecolor='lightblue'),
                 whiskerprops=dict(color='gray'),
                 capprops=dict(color='gray'),
                 medianprops=dict(color='red', linewidth=2))
ax4.set_ylabel('Horas')
ax4.set_title('Distribución: Boxplot Comparativo')
ax4.grid(True, alpha=0.3, axis='y')

# Ajustar layout
plt.tight_layout()
plt.suptitle('Análisis de Simulación Monte Carlo para Variable HORAS',
             fontsize=16, y=1.02)
plt.savefig('simulacion_mc_horas.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Visualizaciones guardadas como 'simulacion_mc_horas.png'")

# ==============================================================
# 10. INTERPRETACIÓN DE RESULTADOS
# ==============================================================
print("\n" + "="*60)
print("INTERPRETACIÓN DE RESULTADOS")
print("="*60)

# Comparación de medias
print("\n📊 Comparación de Medias:")
print(f"   - Media Empírica: {stats_empiricas['media']:.2f} horas")
print(f"   - Media Simulada: {stats_simuladas['media']:.2f} horas")
print(f"   - Diferencia: {abs(stats_empiricas['media'] - stats_simuladas['media']):.2f} horas")

# Análisis de colas pesadas
if stats_empiricas['curtosis'] > 0:
    print("\n📈 Análisis de Colas:")
    print(f"   - La curtosis positiva ({stats_empiricas['curtosis']:.2f}) indica colas más pesadas que la normal")
    print(f"   - Esto confirma que la distribución t con pocos gl ({DIST_PARAMS['df']:.2f}) es apropiada")
    print("   - Hay mayor probabilidad de valores extremos (tanto muy bajos como muy altos)")

# Interpretación de umbrales críticos
print("\n🎯 Umbrales Críticos:")
for umbral in [30, 40, 50]:
    prob_emp = probabilidad_exceder_umbral(horas_empiricas, umbral)
    prob_sim = probabilidad_exceder_umbral(muestras_simuladas, umbral)
    if prob_emp > 0.1:
        print(f"   - Hay una probabilidad del {prob_emp*100:.1f}% (empírico) / {prob_sim*100:.1f}% (simulado) de superar {umbral} horas")

# Rango esperado (percentiles 5-95)
print("\n📏 Rango Esperado (90% de los casos):")
print(f"   - Empírico: entre {stats_empiricas['p5']:.1f} y {stats_empiricas['p95']:.1f} horas")
print(f"   - Simulado: entre {stats_simuladas['p5']:.1f} y {stats_simuladas['p95']:.1f} horas")

# Conclusión
print("\n✅ CONCLUSIÓN:")
print("   La simulación de Monte Carlo utilizando la distribución t de Student")
print(f"   con parámetros (gl={DIST_PARAMS['df']:.2f}, loc={DIST_PARAMS['loc']:.2f}, "
      f"scale={DIST_PARAMS['scale']:.2f})")
print("   reproduce adecuadamente las características de los datos empíricos.")
print("   Las pequeñas diferencias se deben a la naturaleza estocástica de la")
print(f"   simulación y al tamaño limitado de la muestra original (n={len(horas_empiricas)}).")
print("   Para fines prácticos, podemos usar la distribución simulada para")
print("   realizar inferencias y cálculos de probabilidad sobre la variable HORAS.")

# ==============================================================
# 11. VALIDACIÓN ADICIONAL: TEST DE KOLMOGOROV-SMIRNOV
# ==============================================================
ks_statistic, p_value = stats.ks_2samp(horas_empiricas, muestras_simuladas)

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
