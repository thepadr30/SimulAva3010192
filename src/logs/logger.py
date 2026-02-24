# %%
# -*- coding: utf-8 -*-
""" logging

setup logging

Proyecto: personal

Tema: logging

Programa: logger.py

Soporte: kfhidalgoh@unal.edu.co

version: 1.0.0

lenguaje: Python 3.11.9

CD: 20230131

LUD: 20230131
"""

import logging
import os
import time

from pathlib import Path

def setup_logging(file_logs: str = "mi_log.log", level: int = logging.INFO) -> logging.Logger:
    """
    Configura logging para que los mensajes se muestren
    tanto en consola como en archivo.

    Args:
        file_logs (str): Ruta del archivo de log.
        level (int): Nivel mínimo de logging (por defecto INFO).

    Returns:
        logging.Logger: Logger configurado.
    """
    # Asegurar carpeta
    Path(file_logs).parent.mkdir(parents=True, exist_ok=True)

    # Formato común
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(file_logs, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Logger root
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers = []  # limpia duplicados
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def fn_limpieza_carpeta(path):
    logging.info("Eliminando archivos con más de 15 dias en %s", path)
    var_now = time.time()
    for f in os.listdir(path):
        if os.stat(os.path.join(path, f)).st_mtime < var_now - 15 * 86400:
            if os.path.isfile(os.path.join(path, f)):
                os.remove(os.path.join(path, f))
    return None

