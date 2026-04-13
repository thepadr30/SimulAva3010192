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


import pandas as pd


def estilo_dashboard_v0(df):
    return (
        df.style
        .hide(axis="index")
        .set_properties(**{ "font-size": "22px", "text-align": "center" })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#34495e"),
                    ("color", "white"), ("font-size", "24px")
                ]
            }
        ])
    )


def estilo_dashboard(df: pd.DataFrame, decimals: int = 2):
    """Aplica un estilo visual tipo dashboard a un DataFrame.

    La función oculta el índice, centra el contenido de las celdas y
    aplica estilos personalizados al encabezado de la tabla. Además,
    redondea automáticamente las columnas numéricas al número de
    decimales especificado.

    Args:
        df (pd.DataFrame):
            DataFrame al que se le aplicará el estilo visual.

        decimals (int, optional):
            Número de cifras decimales para redondear las columnas
            numéricas del DataFrame. Por defecto es 2.

    Returns:
        pd.io.formats.style.Styler:
            Objeto `Styler` de pandas con los estilos aplicados,
            listo para ser renderizado en HTML o entornos como Jupyter.

    Raises:
        TypeError:
            Si el parámetro `df` no es un `pandas.DataFrame`.

    Example:
        >>> styled_df = estilo_dashboard(df, decimals=3)
        >>> styled_df
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df debe ser un pandas.DataFrame")

    df_processed = df.copy()

    numeric_cols = df_processed.select_dtypes(include="number").columns

    styled_df = (
        df_processed.style
        #.hide(axis="index")
        .format({col: f"{{:.{decimals}f}}" for col in numeric_cols})
        .set_properties(
            **{
                "font-size": "22px",
                "text-align": "center",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#34495e"),
                        ("color", "white"),
                        ("font-size", "24px"),
                    ],
                }
            ]
        )
    )

    return styled_df


def estilo_dashboard_v2(
    df: pd.DataFrame,
    decimals: int = 2,
    thousands: bool = True,
    heatmap: bool = False,
    bars: bool = False,
):
    """Aplica un estilo visual avanzado tipo dashboard a un DataFrame.

    Esta función aplica formato visual optimizado para reportes analíticos,
    incluyendo formato numérico inteligente, separadores de miles,
    gradientes de color y barras tipo KPI dentro de celdas.

    Args:
        df (pd.DataFrame):
            DataFrame al que se aplicará el estilo.

        decimals (int, optional):
            Número de decimales para valores flotantes. Por defecto 2.

        thousands (bool, optional):
            Si es True, aplica separador de miles a números. Por defecto True.

        heatmap (bool, optional):
            Si es True, aplica un gradiente de color a columnas numéricas.
            Por defecto False.

        bars (bool, optional):
            Si es True, agrega barras horizontales tipo KPI en columnas
            numéricas. Por defecto False.

    Returns:
        pd.io.formats.style.Styler:
            Objeto Styler listo para renderizar en Jupyter o HTML.

    Raises:
        TypeError:
            Si `df` no es un pandas.DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df debe ser un pandas.DataFrame")

    df_processed = df.copy()

    numeric_cols = df_processed.select_dtypes(include="number").columns

    # -----------------------------
    # Formato numérico inteligente
    # -----------------------------
    format_dict = {}

    for col in numeric_cols:
        if pd.api.types.is_integer_dtype(df_processed[col]):
            format_dict[col] = "{:,}" if thousands else "{}"
        else:
            if thousands:
                format_dict[col] = f"{{:,.{decimals}f}}"
            else:
                format_dict[col] = f"{{:.{decimals}f}}"

    styler = (
        df_processed.style
        .hide(axis="index")
        .format(format_dict)
        .set_properties(
            **{
                "font-size": "20px",
                "text-align": "center",
                "padding": "6px",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#2c3e50"),
                        ("color", "white"),
                        ("font-size", "22px"),
                        ("text-align", "center"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("border", "1px solid #ecf0f1"),
                    ],
                },
                {
                    "selector": "table",
                    "props": [
                        ("border-collapse", "collapse"),
                        ("margin", "10px 0px"),
                    ],
                },
            ]
        )
    )

    # -----------------------------
    # Heatmap opcional
    # -----------------------------
    if heatmap and len(numeric_cols) > 0:
        styler = styler.background_gradient(
            cmap="YlGnBu",
            subset=numeric_cols,
        )

    # -----------------------------
    # Barras tipo KPI opcionales
    # -----------------------------
    if bars and len(numeric_cols) > 0:
        styler = styler.bar(
            subset=numeric_cols,
            color="#5dade2",
        )

    return styler


def estilo_dashboard_v3(
    df: pd.DataFrame,
    decimals: int = 2,
    thousands: bool = True,
    currency: str | None = None,
    heatmap: bool = False,
    bars: bool = False,
    highlight_extremes: bool = False,
    highlight_outliers: bool = False,
):
    """Aplica un estilo avanzado tipo dashboard a un DataFrame.

    Esta función está diseñada para visualización analítica en notebooks,
    dashboards o reportes HTML. Incluye formateo numérico inteligente,
    detección automática de porcentajes, separadores de miles, formato
    monetario opcional, heatmaps, barras KPI y resaltado de valores
    extremos u outliers.

    Args:
        df (pd.DataFrame):
            DataFrame al que se aplicará el estilo.

        decimals (int, optional):
            Número de decimales para valores flotantes. Default = 2.

        thousands (bool, optional):
            Si es True, aplica separador de miles. Default = True.

        currency (str | None, optional):
            Símbolo monetario a aplicar (ej: "$", "€"). Default = None.

        heatmap (bool, optional):
            Aplica gradiente de color a columnas numéricas. Default = False.

        bars (bool, optional):
            Agrega barras horizontales tipo KPI. Default = False.

        highlight_extremes (bool, optional):
            Resalta valores máximos y mínimos. Default = False.

        highlight_outliers (bool, optional):
            Resalta outliers usando método IQR. Default = False.

    Returns:
        pd.io.formats.style.Styler:
            Objeto Styler con formato visual aplicado.

    Raises:
        TypeError:
            Si `df` no es un pandas.DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df debe ser un pandas.DataFrame")

    df_processed = df.copy()
    numeric_cols = df_processed.select_dtypes(include="number").columns

    # -----------------------------
    # Detección automática de porcentajes
    # -----------------------------
    percentage_cols = []

    for col in numeric_cols:
        col_data = df_processed[col].dropna()
        if len(col_data) > 0 and col_data.between(0, 1).all():
            percentage_cols.append(col)

    # -----------------------------
    # Construcción de formatos
    # -----------------------------
    format_dict = {}

    for col in numeric_cols:

        if col in percentage_cols:
            format_dict[col] = f"{{:.{decimals}%}}"
            continue

        if pd.api.types.is_integer_dtype(df_processed[col]):
            if thousands:
                format_dict[col] = "{:,}"
            else:
                format_dict[col] = "{}"
            continue

        if currency:
            if thousands:
                format_dict[col] = f"{currency}{{:,.{decimals}f}}"
            else:
                format_dict[col] = f"{currency}{{:.{decimals}f}}"
        else:
            if thousands:
                format_dict[col] = f"{{:,.{decimals}f}}"
            else:
                format_dict[col] = f"{{:.{decimals}f}}"

    styler = (
        df_processed.style
        .hide(axis="index")
        .format(format_dict)
        .set_properties(
            **{
                "font-size": "18px",
                "text-align": "center",
                "padding": "6px",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#2c3e50"),
                        ("color", "white"),
                        ("font-size", "20px"),
                        ("text-align", "center"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("border", "1px solid #ecf0f1"),
                    ],
                },
                {
                    "selector": "table",
                    "props": [
                        ("border-collapse", "collapse"),
                        ("margin", "10px 0px"),
                    ],
                },
            ]
        )
    )

    # -----------------------------
    # Heatmap
    # -----------------------------
    if heatmap and len(numeric_cols) > 0:
        styler = styler.background_gradient(
            cmap="YlGnBu",
            subset=numeric_cols,
        )

    # -----------------------------
    # Barras KPI
    # -----------------------------
    if bars and len(numeric_cols) > 0:
        styler = styler.bar(
            subset=numeric_cols,
            color="#5dade2",
        )

    # -----------------------------
    # Resaltado de extremos
    # -----------------------------
    if highlight_extremes and len(numeric_cols) > 0:

        styler = styler.highlight_max(
            subset=numeric_cols,
            color="#d4efdf",
        ).highlight_min(
            subset=numeric_cols,
            color="#f9e79f",
        )

    # -----------------------------
    # Outliers usando IQR
    # -----------------------------
    if highlight_outliers and len(numeric_cols) > 0:

        def highlight_outlier(series):
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            return [
                "background-color:#f5b7b1"
                if (v < lower or v > upper)
                else ""
                for v in series
            ]

        styler = styler.apply(highlight_outlier, subset=numeric_cols)

    return styler