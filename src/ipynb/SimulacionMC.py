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

import os
import logging
import sys
from time import localtime, strftime, time

import numpy as np
import pandas as pd

from src.logs.logger import setup_logging, fn_limpieza_carpeta
from src.utils import lecturaExcel as lE
from src.utils import statisticsBase as sB
from src.graph.fun_graph_matplotlib import FnGraphMat

__file__ = "SimulacionMCPy"
file_log = os.path.join(
    'D:\SimulAva\logs',
    strftime("%Y%m%d%H%M%S", localtime()) + "_" + __file__ + ".log"
)

logger = setup_logging(file_log)
logging.info("Python %s on %s", sys.version, sys.platform)
logging.info("Root: %s", os.getcwd())  # os.path.abspath(os.curdir)
logging.info("Log: %s", file_log)

#%%
##############
# Constantes #
##############

varData = r'D:\SimulAva\data'
grmt = FnGraphMat('dark_style')

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

dataframes_cargados = lE.leer_multiples_excels(varData)
df_monteCarlo = dataframes_cargados.get(
    "SIMULAVA 2026-02-18 Clase4-2 MONTECARLO EJM (1)", None
)
df_monteCarlo_original = df_monteCarlo.copy()

list_df = [
    df_monteCarlo
]

for i in list_df:
    lE.normalizar_columnas_snake_case(i, inplace=True)

#%%
##################
# Data wrangling #
##################

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

# histograma
grmt.graph_armor_hist(df_monteCarlo, 'horas')

# iqr
grmt.graph_armor_iqr(df_monteCarlo, var_index='datos', var_vble='horas')

#%%
tabla = frequency_table(df_monteCarlo, "horas")
print(tabla)

#%%
from distfit import distfit

dfit = distfit()
dfit.fit_transform(df_monteCarlo['horas'])
dfit.plot()
fig, ax = dfit.plot(chart='pdf')
#fig, ax = d.plot(chart='cdf')
fig.show()

print("La mejor distribución encontrada es:", dfit.model['name'])
print("Parámetros óptimos:", dfit.model['params'])

# 4. Obtener los resultados de la detección
results = dfit.predict(np.array(df_monteCarlo['horas']))

# Mostramos los índices de los valores detectados como outliers
# indices_outliers = np.where(results['outliers'] == 'y')[0]
# print(f"Valores detectados como outliers: {data_with_outliers[indices_outliers]}")

# %%
########
# main #
########

def main(**kwargs):
    logging.info("Programa: SimulacionMCPy")

if __name__ == "__main__":
    fn_limpieza_carpeta('D:\SimulAva\logs')
