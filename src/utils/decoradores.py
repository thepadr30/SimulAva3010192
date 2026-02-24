#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""decoradores
Decorador para medir el tiempo de ejecución de una función.

Proyecto: Entrevista Meli

Tema: HU técnica

Programa: no_decoradores.py

Soporte: kevin.hidalgo@globalmvm.com

version: 1.0.0

lenguaje: Python 3.10

CD: 20240722

LUD: 20240722

Comentarios:
    * 20240719 Kevin Hidalgo -> PEP8.
"""

__authors__ = ["Kevin Hidalgo"]
__contact__ = "kevin.hidalgo@globalmvm.com"
__copyright__ = "Copyright 2024, MVM ingenieria de software"
__credits__ = ["Kevin Hidalgo"]
__email__ = "kevin.hidalgo@globalmvm.com"
__status__ = "Desarrollo"
__version__ = "1.0.0"
__date__ = "2024-02-12"

import csv
import datetime
import logging
import math
import os
import time
from functools import wraps
from pathlib import Path
from time import localtime, strftime

VAR_FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
VAR_PAD = "#" * 60

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def print_header(msg: str, bool_terminal: int = 1):
    """Impresión título

    Args:
        msg (str): mensaje

    Returns:
        NoneType: print
    """
    if bool_terminal == 1:
        return logging.info(f"\033[96m{msg}\033[00m\n{'-' * len(msg)}")
    else:
        return print(f"\033[96m{msg}\033[00m\n{'-' * len(msg)}")


def fn_date_start(bool_terminal: int = 1) -> datetime.datetime:
    """Captura el tiempo de inicio del proceso.

    Args:
        bool_terminal (int, optional): Indica el modo de impresión. Defaults to 3.

    Returns:
        datetime.datetime: Tiempo actual en formato datetime.
    """
    var_incp = datetime.datetime.now()
    formatted_time = strftime(VAR_FORMAT_DATE, localtime())

    if bool_terminal == 1:
        logging.info(
            "Hora inicio proceso -> %s", formatted_time
        )
    elif bool_terminal == 2:
        print(VAR_PAD)
        print(f"## Hora inicio proceso -> {formatted_time} ########")
        print(VAR_PAD)
    else:
        print(f"\033[92m{formatted_time} [INFO]:\033[00m "
              f"Hora inicio proceso ->"
              f" {formatted_time}")

    return var_incp


def fn_date_end(bool_terminal: int = 1) -> datetime.datetime:
    """Captura el tiempo de fin del proceso.

    Args:
        bool_terminal (int, optional): Indica el modo de impresión. Defaults to 3.

    Returns:
        datetime.datetime: Tiempo actual en formato datetime.
    """
    var_fnpr = datetime.datetime.now()
    formatted_time = strftime(VAR_FORMAT_DATE, localtime())

    if bool_terminal == 1:
        logging.info("Hora fin proceso -> %s", formatted_time)
    elif bool_terminal == 2:
        print(VAR_PAD)
        print(
            "## Hora fin proceso -> "
            + formatted_time
            + " ###########"
        )
        print(VAR_PAD)
    else:
        print(f"\033[92m{formatted_time} [INFO]:\033[00m "
              f"Hora fin proceso ->"
              f" {formatted_time}")

    return var_fnpr


def fn_runtime(
        tiempo_inicial: datetime.datetime, tiempo_final: datetime.datetime, bool_terminal: int = 1
):
    """Calcula y muestra el tiempo total de ejecución del proceso.

    Args:
        tiempo_inicial (datetime.datetime): Tiempo de inicio del proceso.
        tiempo_final (datetime.datetime): Tiempo final del proceso.
        bool_terminal (int, optional): Indica el modo de impresión. Defaults to 3.
    """
    tiempo_final = tiempo_final.replace(microsecond=0)
    tiempo_inicial = tiempo_inicial.replace(microsecond=0)
    total_time = tiempo_final - tiempo_inicial
    formatted_time = str(total_time)

    if bool_terminal == 1:
        logging.info("El tiempo total de ejecución fue: %s", formatted_time)
    elif bool_terminal == 2:
        print(VAR_PAD)
        print(f"## El tiempo total de ejecución fue: {formatted_time} #########")
        print(VAR_PAD)
    else:
        formatted_now = strftime(VAR_FORMAT_DATE, localtime())
        print(f"\033[92m{formatted_now} [INFO]:\033[00m "
              f"El tiempo total de ejecución fue -> {formatted_time}")


def fn_medicion_timepo(str_name: str):  # pragma no cover
    """Decorador para medir el tiempo de ejecución de una función.

    Args:
        str_name (str): Nombre de la etapa del proceso.

    Returns:
        Callable: Función decorada.

    Examples:
        @fn_medicion_timepo("lectura de archivo")
        def fn_lectura_archivo():
            ...
            Returns None
    """
    def decorator(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            print_header(str_name)
            info_incp = fn_date_start()
            result = funcion(*args, **kwargs)
            info_fnpr = fn_date_end()
            fn_runtime(info_incp, info_fnpr)
            return result
        return wrapper
    return decorator

def medir_tiempo(nombre_etapa):
    """Decorador para medir el tiempo de ejecución de una función.

    Args:
        nombre_etapa:

    Returns:
        None

    Examples:
        @medir_tiempo("Lectura PDF")
        def _load_pdf(file_path: Path) -> Any:
            ...
            Returns None
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            inicio = time.perf_counter()
            resultado = func(*args, **kwargs)
            duracion = time.perf_counter() - inicio

            # Registrar en log estructurado
            logging.info(
                'METRICA_TIEMPO - Etapa: %s - Duración: %.4f segundos',
                nombre_etapa,
                duracion
            )

            # Escribir en CSV para análisis posterior
            with open('metricas_tiempo.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.datetime.now().isoformat(),
                    nombre_etapa,
                    duracion,
                    args[0] if args else ''
                ])
            return resultado
        return wrapper
    return decorador


def bomper(*args, flag: bool = 1):  # pragma no cover
    """bomper

    Args:
        args[0] (str): __file__, nombre NB.

    Returns:
        pyspark.sql.dataframe.DataFrame: DataFrame final.
    """
    try:
        var_bomper = f"""{
        '=' * (math.floor((80 - len(os.path.basename(Path(args[0])).split('/')[-1]) - 2) / 2))
        + ' ' + str(os.path.basename(Path(args[0])).split('/')[-1]) + ' '
        + '=' * (math.floor((80 - len(os.path.basename(Path(args[0])).split('/')[-1]) - 2) / 2))
        }"""
        if flag == 0:
            print("="*80)
            print(var_bomper)
            print("=" * 80)
        if flag == 1:
            logging.info("=" * 80)
            logging.info(var_bomper)
            logging.info("=" * 80)
    except ValueError:
        var_bomper = f"""{
        '=' * (math.floor((80 - len(args[0]) - 2) / 2))
        + ' ' + str(args[0]) + ' '
        + '=' * (math.floor((80 - len(args[0]) - 2) / 2))
        }"""
        if flag == 0:
            print("="*80)
            print(var_bomper)
            print("=" * 80)
        if flag == 1:
            logging.info("=" * 80)
            logging.info(var_bomper)
            logging.info("=" * 80)

dict_cnst = {
    1: "Error de tipo: %s. Verifica los tipos de datos del DataFrame y el diccionario.",
    2: "Error de clave: '%s' no está presente en el diccionario.",
    3: "Serie creada a partir del diccionario: %s",
    4: "Ha ocurrido un error inesperado: %s",
    5: "El argumento 'df' debe ser un DataFrame de pandas.",
}


def uerrors(var_caso: int) -> str:
    """Reduce los return de tipo str dentro de las funciones.

    Args:
        var_caso (int): opción cadena caracteres para retornar.

    Returns:
        str: cadena de caracteres.

    Examples:
        logging.error(uerrors(4), e)
    """
    return f"{dict_cnst.get(var_caso)}"
