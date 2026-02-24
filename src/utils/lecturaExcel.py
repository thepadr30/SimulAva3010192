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
import re
import sys
from time import localtime, strftime

import pandas as pd
import unicodedata


def leer_multiples_excels(ruta_directorio: str) -> dict:
    """
    Lee todos los archivos de Excel en una ruta de directorio y los carga en DataFrames.

    Args:
        ruta_directorio: La ruta del directorio donde se encuentran los archivos Excel.

    Returns:
        Un diccionario donde las claves son los nombres de los archivos (sin extensión)
        y los valores son los DataFrames de pandas.
    """
    dataframes_por_nombre = {}

    # 1. Verificar si la ruta existe y es un directorio
    if not os.path.isdir(ruta_directorio):
        print(f"Error: La ruta '{ruta_directorio}' no es un directorio válido o no existe.")
        return dataframes_por_nombre  # Devuelve un diccionario vacío

    # 2. Iterar sobre los archivos en el directorio
    for nombre_archivo in os.listdir(ruta_directorio):
        # 3. Comprobar si es un archivo de Excel
        if nombre_archivo.endswith(('.xlsx', '.xls')):
            # Construir la ruta completa del archivo
            ruta_completa_archivo = os.path.join(ruta_directorio, nombre_archivo)

            try:
                # 4. Leer el archivo Excel en un DataFrame
                df = pd.read_excel(ruta_completa_archivo)

                # 5. Generar el nombre del DataFrame (nombre del archivo sin extensión)
                #   os.path.splitext separa la base y la extensión
                nombre_base, _ = os.path.splitext(nombre_archivo)

                # 6. Almacenar en el diccionario
                dataframes_por_nombre[nombre_base] = df
                print(
                    f"✅ Archivo '{nombre_archivo}' leído. "
                    f"DataFrame guardado como '{nombre_base}'."
                )

            except Exception as e:
                # Manejar posibles errores de lectura de Excel (corrupción, formato incorrecto)
                print(f"❌ Error al leer el archivo '{nombre_archivo}': {e}")

    return dataframes_por_nombre


def normalizar_columnas_snake_case(df, inplace=False):
    """
    Normaliza los nombres de las columnas de un DataFrame a snake_case sin caracteres especiales.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame cuyas columnas se van a normalizar
    inplace : bool, optional
        Si es True, modifica el DataFrame original. Si es False, retorna una copia.
        Por defecto False.

    Retorna:
    --------
    pandas.DataFrame or None
        Si inplace=False, retorna el DataFrame con columnas normalizadas.
        Si inplace=True, retorna None y modifica el DataFrame original.
    """

    def a_snake_case(texto):
        """
        Convierte un texto a snake_case sin caracteres especiales.
        """
        if not isinstance(texto, str):
            texto = str(texto)

        # Normalizar caracteres unicode (remover acentos)
        texto = unicodedata.normalize('NFKD', texto)
        texto = ''.join([c for c in texto if not unicodedata.combining(c)])

        # Reemplazar caracteres especiales y espacios por underscore
        texto = re.sub(r'[^\w\s]', '_', texto)
        texto = re.sub(r'[\s]+', '_', texto)

        # Convertir a minúsculas y eliminar underscores múltiples
        texto = texto.lower()
        texto = re.sub(r'_+', '_', texto)

        # Eliminar underscores al inicio y final
        texto = texto.strip('_')

        return texto

    # Crear mapeo de nombres antiguos a nuevos
    mapeo_columnas = {col: a_snake_case(col) for col in df.columns}

    if inplace:
        # Modificar el DataFrame original
        df.rename(columns=mapeo_columnas, inplace=True)
        return None
    else:
        # Retornar una copia con las columnas renombradas
        return df.rename(columns=mapeo_columnas)
