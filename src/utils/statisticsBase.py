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
from typing import Dict, Tuple, Optional

import numpy as np
import pandas as pd
from scipy import stats


def fn_statistics_base(
        data_frame: pd.DataFrame,
        var_vble: str,
        dropna: bool = True,
        ddof: int = 1,
        conf_level: float = 0.95,
        decimals: Optional[int] = 4,
) -> pd.DataFrame:
    """Calcula estadísticas descriptivas básicas para una variable numérica.

    Args:
        data_frame: DataFrame que contiene la variable.
        var_vble: Nombre de la columna numérica a resumir.
        dropna: Si True elimina NaN antes de calcular estadísticas.
        ddof: Delta degrees of freedom para var/std.
        conf_level: Nivel de confianza para el intervalo de la media.
        decimals: Número de decimales para redondear resultados.

    Returns:
        pd.DataFrame: DataFrame de una fila con las estadísticas calculadas.

    Raises:
        ValueError: si `var_vble` no está en `data_frame` o no hay observaciones válidas.

    Examples::

        np.random.seed(0)
        df = pd.DataFrame({
            "A": np.concatenate([np.random.normal(50, 5, size=30), [np.nan, np.nan]]),
            "B": ["x"] * 32
        }, index=pd.date_range("2020-01-01", periods=32, freq="ME"))

        df_stats = tsmu.fn_statistics_base(df, "A")
        print(df_stats.T)
    """
    # Validación inicial
    _validate_input(data_frame, var_vble)

    # Preparar datos
    sr_clean, n_total, n_obs, missing_count = _prepare_data(data_frame, var_vble, dropna)

    if n_obs == 0:
        raise ValueError(
            f"La serie '{var_vble}' no tiene observaciones válidas tras aplicar dropna={dropna}."
        )

    # Calcular estadísticas
    basic_stats = _calculate_basic_stats(sr_clean, ddof)
    quantile_stats = _calculate_quantile_stats(sr_clean)
    shape_stats = _calculate_shape_stats(sr_clean)
    ci_stats = _calculate_confidence_interval(basic_stats, n_obs, conf_level)

    # Combinar resultados
    results = {
        "n_total": int(n_total),
        "n_obs": n_obs,
        "missing_count": missing_count,
        **basic_stats,
        **quantile_stats,
        **shape_stats,
        **ci_stats
    }

    # Aplicar redondeo si es necesario
    if decimals is not None:
        results = _round_results(results, decimals)

    return pd.DataFrame(results, index=[0])


def _validate_input(data_frame: pd.DataFrame, var_vble: str) -> None:
    """Valida los parámetros de entrada."""
    if var_vble not in data_frame.columns:
        raise ValueError(f"Columna '{var_vble}' no encontrada en el DataFrame.")


def _prepare_data(data_frame: pd.DataFrame, var_vble: str, dropna: bool) -> Tuple[
    pd.Series, int, int, int]:
    """Prepara y limpia los datos para análisis."""
    sr = data_frame[var_vble].copy()

    # Convertir a numérico
    sr = pd.to_numeric(sr, errors='coerce')

    n_total = len(sr)

    if dropna:
        sr_clean = sr.dropna()
    else:
        sr_clean = sr

    n_obs = int(sr_clean.count())
    missing_count = int(n_total - n_obs)

    return sr_clean, n_total, n_obs, missing_count

def _calculate_basic_stats(series: pd.Series, ddof: int) -> Dict[str, float]:
    """Calcula estadísticas básicas de tendencia central y dispersión."""
    mean = series.mean()
    std = series.std(ddof=ddof)

    return {
        "mean": mean,
        "median": series.median(),
        "var": series.var(ddof=ddof),
        "std": std,
        "sem": series.sem(ddof=ddof),
        "min": series.min(),
        "max": series.max(),
        "range": series.max() - series.min(),
        "CV_pct": _calculate_cv(mean, std)
    }


def _calculate_cv(mean: float, std: float) -> float:
    """Calcula el coeficiente de variación."""
    if np.isclose(mean, 0.0):
        return np.nan
    return (std / mean) * 100.0


def _calculate_quantile_stats(series: pd.Series) -> Dict[str, float]:
    """Calcula estadísticas basadas en cuantiles."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    return {
        "q1": q1,
        "q3": q3,
        "iqr": q3 - q1
    }


def _calculate_shape_stats(series: pd.Series) -> Dict[str, float]:
    """Calcula estadísticas de forma de la distribución."""
    return {
        "skewness": float(stats.skew(series, nan_policy="omit")),
        "kurtosis": float(stats.kurtosis(series, nan_policy="omit"))
    }


def _calculate_confidence_interval(basic_stats: Dict, n_obs: int, conf_level: float) -> \
Dict[str, float]:
    """Calcula el intervalo de confianza para la media."""
    mean = basic_stats["mean"]
    sem = basic_stats["sem"]

    dof = n_obs - 1
    if dof <= 0:
        return {"ci_mean_lower": np.nan, "ci_mean_upper": np.nan}

    alpha = 1.0 - conf_level
    t_crit = stats.t.ppf(1.0 - alpha / 2.0, dof)
    margin = t_crit * sem

    return {
        "ci_mean_lower": mean - margin,
        "ci_mean_upper": mean + margin
    }


def _round_results(results: Dict, decimals: int) -> Dict:
    """Aplica redondeo a los resultados numéricos."""
    rounded = {}

    for key, value in results.items():
        if isinstance(value, (int, np.integer)):
            rounded[key] = int(value)
        elif isinstance(value, (float, np.floating)) and not np.isnan(value):
            rounded[key] = round(float(value), decimals)
        else:
            rounded[key] = value

    return rounded


def column_overview(data_frame: pd.DataFrame) -> pd.DataFrame:
    dtypes = data_frame.dtypes.astype(str).to_frame('dtype')
    missing_count = data_frame.isna().sum().to_frame('missing_count')
    unique_count = data_frame.nunique(dropna=False).to_frame('unique_count')
    col_overview = pd.concat([dtypes, missing_count, unique_count], axis=1)
    return col_overview


def numeric_descriptive_stats(data_frame: pd.DataFrame) -> pd.DataFrame:
    num_cols = data_frame.select_dtypes(include=[np.number]).columns.tolist()
    desc = data_frame[num_cols].describe(percentiles=[0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99]).T
    desc['median'] = data_frame[num_cols].median()
    desc['missing'] = data_frame[num_cols].isna().sum()
    return desc


def analisis_descriptivo(data_frame: pd.DataFrame, **kwargs) -> dict:
    """
    Realiza análisis descriptivo completo por tipo
    """
    print("\n=== ANÁLISIS DESCRIPTIVO ===")

    var = kwargs.get("variable_cat", None)
    target = kwargs.get("variable_target", None)
    estadisticas_completas = {}
    tipos = data_frame[var].unique()

    for tipo in tipos:
        datos_tipo = data_frame[data_frame[var] == tipo][target]  # 'Generacion_MWh'

        stats = {
            'count': datos_tipo.count(),
            'mean': datos_tipo.mean(),
            'median': datos_tipo.median(),
            'std': datos_tipo.std(),
            'min': datos_tipo.min(),
            'max': datos_tipo.max(),
            'q25': datos_tipo.quantile(0.25),
            'q75': datos_tipo.quantile(0.75),
            'missing': datos_tipo.isnull().sum(),
            'missing_pct': (datos_tipo.isnull().sum() / len(datos_tipo)) * 100
        }

        estadisticas_completas[tipo] = stats

        print(f"\n--- {tipo} ---")
        print(f"Registros: {stats['count']}")
        print(f"Valores faltantes: {stats['missing']} ({stats['missing_pct']:.2f}%)")
        print(f"Media: {stats['mean']:,.2f} kWh")
        print(f"Mediana: {stats['median']:,.2f} kWh")
        print(f"Desv. Estándar: {stats['std']:,.2f} kWh")
        print(f"Rango: {stats['min']:,.2f} - {stats['max']:,.2f} kWh")

    return estadisticas_completas


def detectar_outliers(data_frame: pd.DataFrame, **kwargs) -> dict:
    """
    Detecta valores atípicos usando método IQR
    """
    print("\n=== DETECCIÓN DE OUTLIERS (MÉTODO IQR) ===")

    var = kwargs.get("variable_cat", None)
    target = kwargs.get("variable_target", None)
    outliers_por_tipo = {}

    if var is not None:
        tipos = data_frame[var].unique()

        for tipo in tipos:
            datos = data_frame[data_frame[var] == tipo][target].dropna()

            Q1 = datos.quantile(0.25)
            Q3 = datos.quantile(0.75)
            IQR = Q3 - Q1

            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR

            # Ajustar límite inferior para evitar valores negativos en generación
            limite_inferior = max(limite_inferior, 0)

            outliers = datos[(datos < limite_inferior) | (datos > limite_superior)]

            outliers_por_tipo[tipo] = {
                'outliers': outliers,
                'limite_inferior': limite_inferior,
                'limite_superior': limite_superior,
                'count': len(outliers),
                'porcentaje': (len(outliers) / len(datos)) * 100
            }

            print(f"\n--- {tipo} ---")
            print(f"Límites IQR: [{limite_inferior:.2f}, {limite_superior:.2f}]")
            print(
                f"Outliers detectados: {len(outliers)} ({outliers_por_tipo[tipo]['porcentaje']:.2f}%)")
            if len(outliers) > 0:
                print(f"Valores outliers: {outliers.values}")

    if var is None:
        datos = data_frame[target].dropna()

        Q1 = datos.quantile(0.25)
        Q3 = datos.quantile(0.75)
        IQR = Q3 - Q1

        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        # Ajustar límite inferior para evitar valores negativos en generación
        limite_inferior = max(limite_inferior, 0)

        outliers = datos[(datos < limite_inferior) | (datos > limite_superior)]

        outliers_por_tipo = {
            'outliers': outliers,
            'limite_inferior': limite_inferior,
            'limite_superior': limite_superior,
            'count': len(outliers),
            'porcentaje': (len(outliers) / len(datos)) * 100
        }

        print(f"\n--- {target} ---")
        print(f"Límites IQR: [{limite_inferior:.2f}, {limite_superior:.2f}]")
        print(
            f"Outliers detectados: {len(outliers)} ({outliers_por_tipo['porcentaje']:.2f}%)")
        if len(outliers) > 0:
            print(f"Valores outliers: {outliers.values}")

    return outliers_por_tipo
