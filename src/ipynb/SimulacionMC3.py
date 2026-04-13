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
sns.set_palette("husl")
warnings.filterwarnings('ignore')  # Ignorar warnings no críticos

"""
Bloque 1 — Construcción de la tabla de frecuencias
Descripción
Recrear la distribución empírica de demanda diaria de leche a partir de los datos históricos
resumidos en la tabla de frecuencias del PDF (364 observaciones = 52 semanas × 7 días). Se calculan
probabilidades simples, acumuladas e intervalos de números aleatorios (estos últimos serán la base
del muestreo Monte Carlo en bloques posteriores).
Justificación
Antes de simular, es indispensable formalizar la distribución de probabilidad empírica. Los
intervalos de números aleatorios permiten el método de la transformada inversa discreta, que es el
estándar en simulación de inventarios con demanda histórica discreta.
"""

#%%
#################
# Lectura Excel #
#################

logging.info('Lectura Excel')

ventas    = [0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10]  # cajas/día
num_dias  = [1,  5, 12, 19, 27, 59, 74, 59, 49, 37, 22]   # frecuencia absoluta

total_obs = sum(num_dias)   # debe ser 364
assert total_obs == 364, f"Total esperado 364, obtenido {total_obs}"

#%%
############################
# CÁLCULOS DE PROBABILIDAD #
############################

prob = [n / total_obs for n in num_dias]  # P(X = x)
prob_acum = list(np.cumsum(prob))  # F(X ≤ x) acumulada

#%%
##########################################
# INTERVALOS DE NÚMEROS ALEATORIOS (INA) #
##########################################

# Método de transformada inversa discreta:
#   INA_inferior = F(x-1)  [0 para x=0]
#   INA_superior = F(x)
# Un número aleatorio u ∈ [INA_inf, INA_sup) → demanda = x
ina_inf = [0.0] + [round(prob_acum[i], 6) for i in range(len(prob_acum)-1)]
ina_sup = [round(p, 6) for p in prob_acum]

#%%
#############################
# CONSTRUIR DATAFRAME TABLA #
#############################

df = pd.DataFrame({
    "Ventas (cajas)":       ventas,
    "Núm. de días":         num_dias,
    "P(X = x)":             [round(p, 4) for p in prob],
    "F(X ≤ x)":             [round(p, 4) for p in prob_acum],
    "INA inferior":         ina_inf,
    "INA superior":         ina_sup,
})

# Fila de totales
total_row = pd.DataFrame([{
    "Ventas (cajas)": "TOTAL",
    "Núm. de días":   total_obs,
    "P(X = x)":       round(sum(prob), 4),
    "F(X ≤ x)":       "",
    "INA inferior":   "",
    "INA superior":   "",
}])
df_display = pd.concat([df, total_row], ignore_index=True)

#%%
#############################
# IMPRIMIR TABLA EN CONSOLA #
#############################

print("=" * 72)
print("  TABLA DE FRECUENCIAS — DEMANDA DIARIA DE LECHE (364 observaciones)")
print("=" * 72)
print(df_display.to_string(index=False))
print()
print(f"  Total observaciones verificadas: {total_obs}  (52 semanas × 7 días)")
print(f"  Demanda media histórica:         {sum(v*p for v,p in zip(ventas,prob)):.4f} cajas/día")
print(f"  Demanda media semanal esperada:  {sum(v*p for v,p in zip(ventas,prob))*7:.2f} cajas/semana")
print("=" * 72)

#%%
#################
# VISUALIZACIÓN #
#################

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle(
    "Distribución Empírica de Demanda Diaria de Leche\n"
    "52 semanas × 7 días = 364 observaciones",
    fontsize=14, fontweight="bold", y=1.01
)

# — Gráfico izquierdo: Histograma de frecuencias absolutas —
color_bar = "#2E86AB"
axes[0].bar(ventas, num_dias, color=color_bar, edgecolor="white", linewidth=0.8)
axes[0].set_xlabel("Ventas diarias (cajas)", fontsize=12)
axes[0].set_ylabel("Número de días", fontsize=12)
axes[0].set_title("Frecuencia absoluta", fontsize=13)
axes[0].set_xticks(ventas)

# Etiquetas encima de cada barra
for x, n in zip(ventas, num_dias):
    axes[0].text(x, n + 0.5, str(n), ha="center", va="bottom", fontsize=9)

# — Gráfico derecho: P(X=x) y F(X≤x) superpuestas —
ax2 = axes[1]
color_prob = "#2E86AB"
color_acum = "#E84855"

bars = ax2.bar(ventas, prob, color=color_prob, alpha=0.75,
               edgecolor="white", linewidth=0.8, label="P(X = x)")
ax2.set_xlabel("Ventas diarias (cajas)", fontsize=12)
ax2.set_ylabel("Probabilidad simple  P(X = x)", fontsize=12, color=color_prob)
ax2.tick_params(axis="y", labelcolor=color_prob)
ax2.set_xticks(ventas)
ax2.set_title("Probabilidad simple y acumulada", fontsize=13)

# Eje secundario para F(X ≤ x)
ax2b = ax2.twinx()
ax2b.plot(ventas, prob_acum, color=color_acum, marker="o",
          linewidth=2, markersize=6, label="F(X ≤ x)")
ax2b.set_ylabel("Probabilidad acumulada  F(X ≤ x)", fontsize=12, color=color_acum)
ax2b.tick_params(axis="y", labelcolor=color_acum)
ax2b.set_ylim(0, 1.05)
ax2b.axhline(y=0.80, color="gray", linestyle="--", linewidth=1,
             alpha=0.7, label="Nivel servicio 80%")

# Leyenda combinada
h1 = mpatches.Patch(color=color_prob, alpha=0.75, label="P(X = x)")
h2 = plt.Line2D([0], [0], color=color_acum, marker="o", linewidth=2, label="F(X ≤ x)")
h3 = plt.Line2D([0], [0], color="gray", linestyle="--", linewidth=1, label="80% servicio")
ax2.legend(handles=[h1, h2, h3], loc="upper left", fontsize=9)

plt.tight_layout()
# plt.savefig("/mnt/user-data/outputs/bloque1_distribucion.png",
#             dpi=150, bbox_inches="tight")
plt.show()
print("Gráfico guardado: bloque1_distribucion.png")

"""
Resultados del Bloque 1 ✅
La tabla se construyó y verificó correctamente. Puntos clave:
Verificación: 364 observaciones confirmadas (52 × 7).
Demanda media: 6.29 cajas/día → 44.06 cajas/semana, lo que ya anticipa que el contrato actual de 30
    cajas/semana es insuficiente.
Intervalos de números aleatorios (INA): calculados por transformada inversa. Por ejemplo:

Demanda = 6 cajas → u ∈ [0.3379, 0.5412)
Demanda = 7 cajas → u ∈ [0.5412, 0.7033)

Línea de 80% de servicio: el acumulado F(X ≤ 8) = 0.8379, lo que indica que para cubrir el 80% de
los días con una sola entrega semanal se necesitarían al menos 8 cajas/día × 7 días = 56 cajas/semana.
"""

# %%
###############################
# SEMILLA DE REPRODUCIBILIDAD #
###############################
"""
Bloque 2 — Simulación base: contrato actual (30 cajas/lunes)
Descripción
Simular 100 semanas con la política actual: entrega de 30 cajas cada lunes, inventario inicial = 0,
faltantes no acumulan entre días. Se calculan: stockouts por semana, nivel de servicio, costo de
inventario acumulado y costo de suministro. Esto establece la línea base contra la cual comparar las
políticas alternativas.
Justificación
Antes de optimizar, es necesario cuantificar el desempeño actual. La simulación base permite validar
el motor de simulación con parámetros conocidos y demostrar formalmente por qué el contrato actual
no cumple el objetivo del 80%.
"""

np.random.seed(42)

#%%
########################################
# DISTRIBUCIÓN EMPÍRICA (del Bloque 1) #
########################################

ventas   = np.array([0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10])
num_dias = np.array([1,  5, 12, 19, 27, 59, 74, 59, 49, 37, 22])
prob     = num_dias / num_dias.sum()          # probabilidades empíricas

#%%
##################################
# PARÁMETROS DE LA POLÍTICA BASE #
##################################

N_SEMANAS      = 100      # horizonte de simulación
CAJAS_PEDIDO   = 30       # unidades entregadas cada lunes
DIA_ENTREGA    = 0        # 0 = lunes (entrega al inicio del día)
COSTO_INV      = 800      # $/caja que queda al final del día
COSTO_FIJO     = 15000   # $ fijo por despacho
COSTO_VAR      = 100      # $/caja despachada

# %%
################################################
# FUNCIÓN DE MUESTREO POR TRANSFORMADA INVERSA #
################################################

def simular_demanda(n):
    """Genera n valores de demanda usando la distribución empírica."""
    return np.random.choice(ventas, size=n, p=prob)

#%%
#######################
# MOTOR DE SIMULACIÓN #
#######################

def simular_politica(n_semanas, dias_entrega, cantidades):
    """
    Simula el inventario durante n_semanas semanas.

    Parámetros
    ----------
    n_semanas    : int   — número de semanas a simular
    dias_entrega : list  — días en que llega pedido (0=Lun ... 6=Dom)
    cantidades   : list  — cajas entregadas en cada día de dias_entrega

    Retorna
    -------
    df_semanas   : DataFrame con métricas agregadas por semana
    df_dias      : DataFrame con detalle diario completo
    """
    inventario   = 0          # inventario al inicio (día 0)
    registros    = []         # detalle día a día

    for semana in range(n_semanas):
        stockout_semana   = False     # ¿hubo faltante esta semana?
        inv_inicio_semana = inventario

        for dia in range(7):          # 7 días por semana
            # — Entrega al inicio del día si corresponde —
            entrega_hoy = 0
            costo_sum_hoy = 0
            if dia in dias_entrega:
                idx          = dias_entrega.index(dia)
                entrega_hoy  = cantidades[idx]
                inventario  += entrega_hoy
                costo_sum_hoy = COSTO_FIJO + COSTO_VAR * entrega_hoy

            inv_antes_venta = inventario   # inventario antes de vender

            # — Generar demanda del día —
            demanda = simular_demanda(1)[0]

            # — Satisfacer demanda o registrar faltante —
            if demanda <= inventario:
                vendido   = demanda
                faltante  = 0
            else:
                vendido   = inventario     # se vende todo lo que hay
                faltante  = demanda - inventario
                stockout_semana = True     # al menos 1 faltante esta semana

            inventario -= vendido          # actualizar inventario

            # — Costo de inventario al cierre del día —
            costo_inv_hoy = inventario * COSTO_INV

            registros.append({
                "semana":           semana + 1,
                "dia_semana":       dia,          # 0=Lun … 6=Dom
                "dia_global":       semana * 7 + dia + 1,
                "entrega":          entrega_hoy,
                "inv_inicio":       inv_antes_venta,
                "demanda":          demanda,
                "vendido":          vendido,
                "faltante":         faltante,
                "inv_fin":          inventario,
                "costo_inv":        costo_inv_hoy,
                "costo_sum":        costo_sum_hoy,
                "costo_total_dia":  costo_inv_hoy + costo_sum_hoy,
            })

        registros[-1]["stockout_semana"] = stockout_semana  # marca en último día

    df_dias = pd.DataFrame(registros)

    # — Propagar marca de stockout a todos los días de cada semana —
    stockout_map = (
        df_dias.groupby("semana")["faltante"]
        .apply(lambda x: (x > 0).any())
        .rename("stockout_semana")
    )
    df_dias = df_dias.drop(columns=["stockout_semana"], errors="ignore")
    df_dias = df_dias.merge(stockout_map, on="semana")

    # — Agregar por semana —
    df_semanas = df_dias.groupby("semana").agg(
        faltante_total  = ("faltante",         "sum"),
        stockout_semana = ("stockout_semana",   "first"),
        costo_inv       = ("costo_inv",         "sum"),
        costo_sum       = ("costo_sum",         "sum"),
        inv_fin_lunes   = ("inv_fin",           "first"),   # inventario tras lunes
    ).reset_index()
    df_semanas["costo_total"] = df_semanas["costo_inv"] + df_semanas["costo_sum"]

    return df_semanas, df_dias

#%%
############################
# EJECUTAR SIMULACIÓN BASE #
############################

df_sem, df_dia = simular_politica(
    n_semanas    = N_SEMANAS,
    dias_entrega = [DIA_ENTREGA],   # solo lunes
    cantidades   = [CAJAS_PEDIDO],  # 30 cajas
)

#%%
####################
# MÉTRICAS RESUMEN #
####################

semanas_sin_stockout = (~df_sem["stockout_semana"]).sum()
nivel_servicio       = semanas_sin_stockout / N_SEMANAS * 100
costo_inv_total      = df_sem["costo_inv"].sum()
costo_sum_total      = df_sem["costo_sum"].sum()
costo_gran_total     = df_sem["costo_total"].sum()
faltantes_totales    = df_sem["faltante_total"].sum()

print("=" * 65)
print("  SIMULACIÓN BASE — 30 cajas / lunes — 100 semanas")
print("=" * 65)
print(f"  Semanas SIN stockout:      {semanas_sin_stockout:>5} / {N_SEMANAS}")
print(f"  Nivel de servicio:         {nivel_servicio:>7.1f}%   (objetivo ≥ 80%)")
print(f"  Total faltantes (cajas):   {faltantes_totales:>7.0f}")
print(f"  Costo de inventario:    ${costo_inv_total:>12,.0f}")
print(f"  Costo de suministro:    ${costo_sum_total:>12,.0f}")
print(f"  COSTO TOTAL:            ${costo_gran_total:>12,.0f}")
print("=" * 65)
print()

#%%
#######################################
# TABLA DETALLE — PRIMERAS 10 SEMANAS #
#######################################

print("  Detalle por semana (primeras 10):")
print(
    df_sem.head(10).to_string(
        index=False,
        columns=["semana","faltante_total","stockout_semana",
                 "costo_inv","costo_sum","costo_total"],
        header=["Semana","Faltantes","¿Stockout?",
                "Costo Inv $","Costo Sum $","Costo Total $"],
    )
)
print()

#%%
#################
# VISUALIZACIÓN #
#################

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)

fig, axes = plt.subplots(2, 2, figsize=(15, 9))
fig.suptitle(
    "Simulación Base — Contrato Actual: 30 cajas / lunes — 100 semanas",
    fontsize=14, fontweight="bold"
)

DIAS = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
COLOR_OK  = "#2E86AB"
COLOR_BAD = "#E84855"
COLOR_INV = "#F4A261"

# — Panel A: Inventario diario (primeras 20 semanas = 140 días) —
ax = axes[0, 0]
dias_20 = df_dia[df_dia["semana"] <= 20].copy()
ax.fill_between(dias_20["dia_global"], dias_20["inv_fin"],
                color=COLOR_INV, alpha=0.4, label="Inventario fin día")
ax.plot(dias_20["dia_global"], dias_20["inv_fin"],
        color=COLOR_INV, linewidth=1)
# Marcar días con faltante
falt_dias = dias_20[dias_20["faltante"] > 0]
ax.scatter(falt_dias["dia_global"], [0]*len(falt_dias),
           color=COLOR_BAD, s=25, zorder=5, label="Día con faltante")
# Líneas verticales cada lunes
for s in range(1, 21):
    ax.axvline((s-1)*7 + 1, color="gray", linewidth=0.5, linestyle="--", alpha=0.5)
ax.set_title("Inventario diario (semanas 1-20)", fontsize=11)
ax.set_xlabel("Día global")
ax.set_ylabel("Cajas en inventario")
ax.legend(fontsize=8)

# — Panel B: Faltantes acumulados por semana —
ax = axes[0, 1]
colores_bar = [COLOR_BAD if s else COLOR_OK for s in df_sem["stockout_semana"]]
ax.bar(df_sem["semana"], df_sem["faltante_total"], color=colores_bar, width=0.8)
ax.set_title("Faltantes por semana", fontsize=11)
ax.set_xlabel("Semana")
ax.set_ylabel("Cajas faltantes")
# Leyenda manual
ok_p  = mpatches.Patch(color=COLOR_OK,  label="Sin stockout")
bad_p = mpatches.Patch(color=COLOR_BAD, label="Con stockout")
ax.legend(handles=[ok_p, bad_p], fontsize=8)

# — Panel C: Costo acumulado a lo largo de las semanas —
ax = axes[1, 0]
costo_acum_inv = df_sem["costo_inv"].cumsum() / 1e6
costo_acum_sum = df_sem["costo_sum"].cumsum() / 1e6
costo_acum_tot = df_sem["costo_total"].cumsum() / 1e6
ax.plot(df_sem["semana"], costo_acum_tot, color="black",   lw=2,   label="Total")
ax.plot(df_sem["semana"], costo_acum_inv, color=COLOR_INV, lw=1.5, label="Inventario")
ax.plot(df_sem["semana"], costo_acum_sum, color=COLOR_OK,  lw=1.5, label="Suministro")
ax.set_title("Costo acumulado (millones $)", fontsize=11)
ax.set_xlabel("Semana")
ax.set_ylabel("Millones de $")
ax.legend(fontsize=8)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.1fM"))

# — Panel D: Nivel de servicio acumulado —
ax = axes[1, 1]
ns_acum = (~df_sem["stockout_semana"]).cumsum() / \
           np.arange(1, N_SEMANAS + 1) * 100
ax.plot(df_sem["semana"], ns_acum, color=COLOR_OK, lw=2, label="Nivel servicio acum.")
ax.axhline(80, color=COLOR_BAD, linestyle="--", lw=1.5, label="Objetivo 80%")
ax.fill_between(df_sem["semana"], ns_acum, 80,
                where=(ns_acum < 80), alpha=0.2, color=COLOR_BAD,
                label="Déficit vs objetivo")
ax.set_ylim(0, 105)
ax.set_title("Nivel de servicio acumulado (%)", fontsize=11)
ax.set_xlabel("Semana")
ax.set_ylabel("% semanas sin stockout")
ax.legend(fontsize=8)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))

# Anotación del nivel final
ax.annotate(
    f"Final: {ns_acum.iloc[-1]:.1f}%",
    xy=(N_SEMANAS, ns_acum.iloc[-1]),
    xytext=(N_SEMANAS - 25, ns_acum.iloc[-1] - 10),
    arrowprops=dict(arrowstyle="->", color="black"),
    fontsize=9, color="black"
)

plt.tight_layout()
# plt.savefig("/mnt/user-data/outputs/bloque2_simulacion_base.png",
#             dpi=150, bbox_inches="tight")
plt.show()
print("Gráfico guardado: bloque2_simulacion_base.png")

"""
Resultados del Bloque 2 ✅
La simulación base confirma formalmente lo que anticipaban los datos del Bloque 1:

Métrica                Resultado        Objetivo
Semanas sin stockout   1 / 100          ≥ 80
Nivel de servicio      1.0%             ≥ 80%
Faltantes totales      1.363 cajas      0 idealmente
Costo inventario       $4.716.800       —
Costo suministro       $1.800.000       —
Costo total            $6.516.800       minimizar

Diagnóstico: el contrato actual falla estrepitosamente. Con demanda media de 44 cajas/semana y solo
30 disponibles, prácticamente cada semana termina con stockout. El inventario se agota en los
primeros días de cada semana (panel A) y el nivel de servicio nunca supera el 10% (panel D).
Esto motiva la búsqueda de una política óptima en los bloques 3, 4 y 5.
"""

#%%
##############
# CONSTANTES #
##############

"""
Bloque 3 — Generación de escenarios de política de pedidoDescripción
Definir y enumerar todas las combinaciones candidatas del espacio de búsqueda: día(s) de entrega 
(lunes, miércoles, lunes+miércoles) × cantidades de pedido por entrega. Se construye un DataFrame 
con todos los escenarios a evaluar, listos para ser alimentados al motor de simulación del 
Bloque 4.Justificación
El distribuidor solo permite entregas los lunes y/o miércoles. Las cantidades a explorar deben 
cubrir un rango razonable alrededor de la demanda media semanal (44 cajas/semana según Bloque 1). 
Enumerar explícitamente el espacio evita búsquedas ciegas y garantiza que se evalúa exhaustivamente
cada combinación viable antes de optimizar.
"""

COSTO_FIJO  = 15000   # $ fijo por despacho
COSTO_VAR   = 100      # $/caja
COSTO_INV   = 800      # $/caja-día
DEM_MEDIA_D = 6.2940   # cajas/día (Bloque 1)
DEM_MEDIA_S = DEM_MEDIA_D * 7   # ≈ 44.06 cajas/semana

#%%
#################################
# RANGOS DE CANTIDAD A EXPLORAR #
#################################

# Política 1 entrega (lunes O miércoles):
#   Rango amplio alrededor de la demanda semanal completa
RANGO_1 = list(range(30, 75, 5))      # [30, 35, 40, 45, 50, 55, 60, 65, 70]

# Política 2 entregas (lunes Y miércoles):
#   Cada pedido cubre ~3-4 días; rango ajustado
RANGO_2 = list(range(15, 50, 5))      # [15, 20, 25, 30, 35, 40, 45]

#%%
########################
# CONSTRUIR ESCENARIOS #
########################

escenarios = []

# ── 3a. Solo lunes (día 0) ─────────────────────────────────
for q in RANGO_1:
    escenarios.append({
        "id_escenario":  f"L{q}",          # etiqueta corta
        "tipo_politica": "Solo lunes",
        "dias_entrega":  [0],              # lunes
        "cantidades":    [q],
        "desc_entrega":  f"Lun: {q} cajas",
        "q_lunes":       q,
        "q_mierc":       0,
        "q_total_sem":   q,                # total cajas/semana
        "n_entregas":    1,
        "costo_sum_teo": COSTO_FIJO + COSTO_VAR * q,   # costo/semana teórico
    })

# ── 3b. Solo miércoles (día 2) ────────────────────────────
for q in RANGO_1:
    escenarios.append({
        "id_escenario":  f"M{q}",
        "tipo_politica": "Solo miércoles",
        "dias_entrega":  [2],              # miércoles
        "cantidades":    [q],
        "desc_entrega":  f"Mié: {q} cajas",
        "q_lunes":       0,
        "q_mierc":       q,
        "q_total_sem":   q,
        "n_entregas":    1,
        "costo_sum_teo": COSTO_FIJO + COSTO_VAR * q,
    })

# ── 3c. Lunes Y miércoles (días 0 y 2) ───────────────────
for ql, qm in itertools.product(RANGO_2, RANGO_2):
    escenarios.append({
        "id_escenario":  f"L{ql}M{qm}",
        "tipo_politica": "Lunes + Miércoles",
        "dias_entrega":  [0, 2],           # lunes y miércoles
        "cantidades":    [ql, qm],
        "desc_entrega":  f"Lun: {ql}, Mié: {qm}",
        "q_lunes":       ql,
        "q_mierc":       qm,
        "q_total_sem":   ql + qm,
        "n_entregas":    2,
        "costo_sum_teo": 2 * COSTO_FIJO + COSTO_VAR * (ql + qm),
    })

df_esc = pd.DataFrame(escenarios)

#%%
############################
# ESTADÍSTICAS DEL ESPACIO #
############################

n_total      = len(df_esc)
n_solo_lun   = (df_esc["tipo_politica"] == "Solo lunes").sum()
n_solo_mie   = (df_esc["tipo_politica"] == "Solo miércoles").sum()
n_lun_mie    = (df_esc["tipo_politica"] == "Lunes + Miércoles").sum()

print("=" * 65)
print("  ESPACIO DE ESCENARIOS — POLÍTICAS DE PEDIDO")
print("=" * 65)
print(f"  Total escenarios a evaluar:   {n_total}")
print(f"  └─ Solo lunes:                {n_solo_lun}")
print(f"  └─ Solo miércoles:            {n_solo_mie}")
print(f"  └─ Lunes + Miércoles:         {n_lun_mie}")
print(f"\n  Demanda media semanal:        {DEM_MEDIA_S:.2f} cajas")
print(f"  Rango 1 entrega:              {RANGO_1[0]}–{RANGO_1[-1]} cajas (step 5)")
print(f"  Rango 2 entregas c/u:         {RANGO_2[0]}–{RANGO_2[-1]} cajas (step 5)")
print("=" * 65)

#%%
########################
# MUESTRA DE CADA TIPO #
########################

print("\n  Muestra — Solo lunes (5 primeros):")
cols_show = ["id_escenario","tipo_politica","desc_entrega","q_total_sem","costo_sum_teo"]
print(df_esc[df_esc["tipo_politica"]=="Solo lunes"][cols_show].head(5).to_string(index=False))

print("\n  Muestra — Solo miércoles (5 primeros):")
print(df_esc[df_esc["tipo_politica"]=="Solo miércoles"][cols_show].head(5).to_string(index=False))

print("\n  Muestra — Lunes + Miércoles (5 primeros):")
print(df_esc[df_esc["tipo_politica"]=="Lunes + Miércoles"][cols_show].head(5).to_string(index=False))
print()

#%%
#########################################
# VISUALIZACIÓN DEL ESPACIO DE BÚSQUEDA #
#########################################

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle(
    "Espacio de Búsqueda — Escenarios de Política de Pedido",
    fontsize=14, fontweight="bold"
)

COLORES = {
    "Solo lunes":         "#2E86AB",
    "Solo miércoles":     "#F4A261",
    "Lunes + Miércoles":  "#2D6A4F",
}

# — Panel A: Costo teórico de suministro/semana por política —
ax = axes[0]
for tipo, color in COLORES.items():
    sub = df_esc[df_esc["tipo_politica"] == tipo].copy()
    # Para 2 entregas, graficar contra q_total_sem
    ax.scatter(sub["q_total_sem"], sub["costo_sum_teo"] / 1000,
               color=color, alpha=0.6, s=30, label=tipo)
ax.axvline(DEM_MEDIA_S, color="red", linestyle="--", lw=1.2,
           label=f"Dem. media\n({DEM_MEDIA_S:.0f} cajas)")
ax.set_xlabel("Total cajas/semana")
ax.set_ylabel("Costo suministro/semana (miles $)")
ax.set_title("Costo teórico de suministro", fontsize=11)
ax.legend(fontsize=7)

# — Panel B: Distribución de cantidades totales por tipo —
ax = axes[1]
for i, (tipo, color) in enumerate(COLORES.items()):
    sub = df_esc[df_esc["tipo_politica"] == tipo]["q_total_sem"]
    ax.hist(sub, bins=15, color=color, alpha=0.65, label=tipo, edgecolor="white")
ax.axvline(DEM_MEDIA_S, color="red", linestyle="--", lw=1.2,
           label=f"Dem. media ({DEM_MEDIA_S:.0f})")
ax.set_xlabel("Total cajas/semana")
ax.set_ylabel("Número de escenarios")
ax.set_title("Distribución de cantidades totales", fontsize=11)
ax.legend(fontsize=7)

# — Panel C: Heatmap de escenarios Lunes+Miércoles —
ax = axes[2]
pivot = df_esc[df_esc["tipo_politica"] == "Lunes + Miércoles"].pivot_table(
    index="q_mierc", columns="q_lunes", values="costo_sum_teo", aggfunc="mean"
)
sns.heatmap(
    pivot / 1000, ax=ax, cmap="YlOrBr", annot=True, fmt=".0f",
    linewidths=0.5, cbar_kws={"label": "Miles $"}
)
ax.set_title("Costo suministro teórico\nLunes + Miércoles (miles $)", fontsize=11)
ax.set_xlabel("Cajas pedidas el lunes")
ax.set_ylabel("Cajas pedidas el miércoles")

plt.tight_layout()
# plt.savefig("/mnt/user-data/outputs/bloque3_espacio_escenarios.png",
#             dpi=150, bbox_inches="tight")
plt.show()
print("Gráfico guardado: bloque3_espacio_escenarios.png")

# Conservar df_esc completo en memoria para Bloque 4
print(f"\n  df_esc listo: {len(df_esc)} escenarios × {len(df_esc.columns)} columnas")

"""
Resultados del Bloque 3 ✅
Se construyó el espacio de búsqueda completo con 67 escenarios:
Política            Escenarios  Ejemplo
Solo lunes          9           30, 35, … 70 cajas
Solo miércoles      9           30, 35, … 70 cajas 
Lunes + Miércoles   49          (15+15), (15+20), … (45+45) cajas
Observaciones clave del espacio:
Costo de suministro: la doble entrega tiene un piso más alto (2 × $15.000 fijo = $30.000/semana vs 
$15.000), pero distribuye mejor el inventario a lo largo de la semana, lo que puede reducir el costo
de almacenamiento.

Heatmap (panel C): el costo teórico de suministro para Lunes+Miércoles crece linealmente con el
total de cajas, lo que hace visible el trade-off entre servicio y costo.

Zona de interés: los escenarios con 40–55 cajas/semana totales están centrados en la demanda media
(44 cajas), y serán los candidatos naturales a cumplir el 80% de servicio con menor costo.
"""

#%%
####################################
# DISTRIBUCIÓN EMPÍRICA (Bloque 1) #
####################################
"""
Bloque 4 — Motor de simulación Monte Carlo generalizadoDescripción
Construir la función central parametrizable que, dado cualquier escenario (día(s) + cantidad(es)), 
simula 100 semanas completas y devuelve nivel de servicio, costo de inventario, costo de suministro
y costo total. Se ejecuta sobre los 67 escenarios del Bloque 3 y se guardan todos los resultados 
para la optimización del Bloque 5.Justificación
Separar el motor de la optimización permite reutilizarlo, depurarlo de forma independiente y 
ejecutarlo eficientemente sobre todo el espacio de búsqueda. Se usa múltiples réplicas (30 corridas
por escenario) para obtener estimaciones robustas y reducir la varianza Monte Carlo inherente a solo
100 semanas.
"""

ventas   = np.array([0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10])
num_dias = np.array([1,  5, 12, 19, 27, 59, 74, 59, 49, 37, 22])
prob     = num_dias / num_dias.sum()

#%%
#######################
# PARÁMETROS GLOBALES #
#######################

N_SEMANAS   = 100      # horizonte por réplica
N_REPLICAS  = 30       # réplicas por escenario
COSTO_INV   = 800      # $/caja-día
COSTO_FIJO  = 15000   # $ fijo por despacho
COSTO_VAR   = 100      # $/caja despachada
OBJETIVO_NS = 0.80     # nivel de servicio mínimo requerido

#%%
###################################
# MOTOR DE SIMULACIÓN (1 réplica) #
###################################

def simular_una_replica(dias_entrega, cantidades, n_semanas, semilla):
    """
    Simula n_semanas semanas de inventario para una política dada.

    Parámetros
    ----------
    dias_entrega : list[int]  — días de entrega (0=Lun … 6=Dom)
    cantidades   : list[int]  — cajas por entrega en cada día
    n_semanas    : int        — semanas a simular
    semilla      : int        — semilla numpy para reproducibilidad

    Retorna
    -------
    dict con métricas agregadas de las n_semanas semanas
    """
    rng        = np.random.default_rng(semilla)      # generador propio
    inventario = 0                                    # inventario inicial = 0

    acum_costo_inv  = 0.0   # acumuladores
    acum_costo_sum  = 0.0
    semanas_sin_so  = 0     # semanas sin stockout
    total_faltantes = 0

    for _ in range(n_semanas):
        stockout_semana = False

        for dia in range(7):                          # 7 días/semana
            # — Entrega al INICIO del día —
            costo_sum_dia = 0.0
            if dia in dias_entrega:
                idx           = dias_entrega.index(dia)
                q             = cantidades[idx]
                inventario   += q
                costo_sum_dia = COSTO_FIJO + COSTO_VAR * q

            # — Demanda del día (transformada inversa) —
            demanda = int(rng.choice(ventas, p=prob))

            # — Satisfacer demanda —
            if demanda <= inventario:
                inventario -= demanda
            else:
                total_faltantes += demanda - inventario
                inventario       = 0                  # se agota
                stockout_semana  = True               # faltante este día

            # — Costo de inventario al cierre del día —
            acum_costo_inv += inventario * COSTO_INV
            acum_costo_sum += costo_sum_dia

        if not stockout_semana:
            semanas_sin_so += 1

    return {
        "nivel_servicio":   semanas_sin_so / n_semanas,
        "costo_inv_sem":    acum_costo_inv / n_semanas,   # promedio/semana
        "costo_sum_sem":    acum_costo_sum / n_semanas,
        "costo_total_sem":  (acum_costo_inv + acum_costo_sum) / n_semanas,
        "faltantes_sem":    total_faltantes / n_semanas,
    }

#%%
###########################
# EVALUADOR MULTI-RÉPLICA #
###########################

def evaluar_escenario(dias_entrega, cantidades,
                      n_semanas=N_SEMANAS, n_replicas=N_REPLICAS):
    """
    Corre n_replicas réplicas independientes y devuelve
    estadísticos (media, std, percentil 10) de cada métrica.
    """
    resultados = [
        simular_una_replica(dias_entrega, cantidades, n_semanas, semilla=r*1000)
        for r in range(n_replicas)
    ]
    df_r = pd.DataFrame(resultados)

    return {
        # Nivel de servicio
        "ns_media":         df_r["nivel_servicio"].mean(),
        "ns_std":           df_r["nivel_servicio"].std(),
        "ns_p10":           df_r["nivel_servicio"].quantile(0.10),
        # Costo total / semana
        "ct_media":         df_r["costo_total_sem"].mean(),
        "ct_std":           df_r["costo_total_sem"].std(),
        # Costo inventario / semana
        "ci_media":         df_r["costo_inv_sem"].mean(),
        # Costo suministro / semana
        "cs_media":         df_r["costo_sum_sem"].mean(),
        # Faltantes / semana
        "falt_media":       df_r["faltantes_sem"].mean(),
    }

#%%
#####################################
# RECONSTRUIR ESCENARIOS (Bloque 3) #
#####################################

RANGO_1 = list(range(30, 75, 5))
RANGO_2 = list(range(15, 50, 5))

escenarios = []
for q in RANGO_1:
    escenarios.append({"id": f"L{q}",    "tipo": "Solo lunes",
                       "dias": [0],     "cant": [q]})
for q in RANGO_1:
    escenarios.append({"id": f"M{q}",    "tipo": "Solo miércoles",
                       "dias": [2],     "cant": [q]})
for ql, qm in itertools.product(RANGO_2, RANGO_2):
    escenarios.append({"id": f"L{ql}M{qm}", "tipo": "Lunes + Miércoles",
                       "dias": [0, 2],  "cant": [ql, qm]})

print(f"Total escenarios: {len(escenarios)}")
print(f"Réplicas por escenario: {N_REPLICAS}")
print(f"Semanas por réplica: {N_SEMANAS}")
print(f"Total semanas simuladas: {len(escenarios)*N_REPLICAS*N_SEMANAS:,}")
print("\nEjecutando simulaciones...\n")

#%%
#################################
# BUCLE PRINCIPAL DE EVALUACIÓN #
#################################

t0       = time()
filas    = []

for i, esc in enumerate(escenarios):
    metricas = evaluar_escenario(esc["dias"], esc["cant"])

    # Calcular cajas totales semanales y descripción
    q_total = sum(esc["cant"])
    q_lun   = esc["cant"][0] if 0 in esc["dias"] else 0
    q_mie   = esc["cant"][esc["dias"].index(2)] if 2 in esc["dias"] else 0

    filas.append({
        "id_escenario":  esc["id"],
        "tipo_politica": esc["tipo"],
        "q_lunes":       q_lun,
        "q_mierc":       q_mie,
        "q_total_sem":   q_total,
        "n_entregas":    len(esc["dias"]),
        **metricas,
        # columnas auxiliares para filtrado
        "cumple_ns":     metricas["ns_media"] >= OBJETIVO_NS,
        "ns_robusto":    metricas["ns_p10"]   >= OBJETIVO_NS,  # p10 ≥ 80%
    })

    # Progreso cada 10 escenarios
    if (i + 1) % 10 == 0:
        print(f"  [{i+1:>3}/{len(escenarios)}] último: {esc['id']:12s} "
              f"NS={metricas['ns_media']:.1%}  CT=${metricas['ct_media']:,.0f}/sem")

elapsed = time() - t0
df_res = pd.DataFrame(filas)
print(f"\nSimulación completada en {elapsed:.1f}s")

#%%
################################
# RESUMEN POR TIPO DE POLÍTICA #
################################

print("\n" + "=" * 70)
print("  RESUMEN POR TIPO DE POLÍTICA")
print("=" * 70)
resumen = df_res.groupby("tipo_politica").agg(
    escenarios      = ("id_escenario",  "count"),
    ns_media_max    = ("ns_media",      "max"),
    ns_media_min    = ("ns_media",      "min"),
    ct_media_min    = ("ct_media",      "min"),
    ct_media_max    = ("ct_media",      "max"),
    cumplen_ns      = ("cumple_ns",     "sum"),
).reset_index()
print(resumen.to_string(index=False))

print("\n  Escenarios que cumplen NS ≥ 80% (media):",
      df_res["cumple_ns"].sum())
print("  Escenarios que cumplen NS p10 ≥ 80% (robusto):",
      df_res["ns_robusto"].sum())

#%%
############################################
# TOP 5 MEJORES POR COSTO (que cumplen NS) #
############################################

print("\n" + "=" * 70)
print("  TOP 5 — Menor costo total promedio con NS ≥ 80%")
print("=" * 70)
top5 = (df_res[df_res["cumple_ns"]]
        .sort_values("ct_media")
        .head(5)[["id_escenario","tipo_politica","q_total_sem",
                  "ns_media","ct_media","ci_media","cs_media"]])
top5_fmt = top5.copy()
top5_fmt["ns_media"]  = top5_fmt["ns_media"].map("{:.1%}".format)
top5_fmt["ct_media"]  = top5_fmt["ct_media"].map("${:,.0f}".format)
top5_fmt["ci_media"]  = top5_fmt["ci_media"].map("${:,.0f}".format)
top5_fmt["cs_media"]  = top5_fmt["cs_media"].map("${:,.0f}".format)
print(top5_fmt.to_string(index=False))

#%%
#################
# VISUALIZACIÓN #
#################

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)

COLORES = {
    "Solo lunes":         "#2E86AB",
    "Solo miércoles":     "#F4A261",
    "Lunes + Miércoles":  "#2D6A4F",
}

fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle(
    "Motor Monte Carlo — Evaluación de 67 Escenarios\n"
    "(30 réplicas × 100 semanas por escenario)",
    fontsize=14, fontweight="bold"
)

# — Panel A: NS vs Costo total (scatter principal) —
ax = axes[0, 0]
for tipo, color in COLORES.items():
    sub = df_res[df_res["tipo_politica"] == tipo]
    ax.scatter(sub["ns_media"] * 100, sub["ct_media"] / 1000,
               color=color, alpha=0.7, s=50, label=tipo, zorder=3)

ax.axvline(80, color="red", linestyle="--", lw=1.5, label="Objetivo 80%")
ax.set_xlabel("Nivel de servicio promedio (%)")
ax.set_ylabel("Costo total promedio / semana (miles $)")
ax.set_title("NS vs Costo total por semana", fontsize=11)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fK"))
ax.legend(fontsize=8)

# Anotar el mejor escenario
mejor = df_res[df_res["cumple_ns"]].nsmallest(1, "ct_media").iloc[0]
ax.annotate(
    f"  ★ {mejor['id_escenario']}\n  NS={mejor['ns_media']:.0%}\n"
    f"  CT=${mejor['ct_media']/1000:.1f}K",
    xy=(mejor["ns_media"]*100, mejor["ct_media"]/1000),
    xytext=(mejor["ns_media"]*100 - 12, mejor["ct_media"]/1000 + 5),
    arrowprops=dict(arrowstyle="->", color="black", lw=1),
    fontsize=8, color="black",
    bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="gray", lw=0.8)
)

# — Panel B: Costo inventario vs Costo suministro —
ax = axes[0, 1]
for tipo, color in COLORES.items():
    sub = df_res[df_res["tipo_politica"] == tipo]
    ax.scatter(sub["ci_media"] / 1000, sub["cs_media"] / 1000,
               color=color, alpha=0.7, s=50, label=tipo, zorder=3)
ax.set_xlabel("Costo inventario / semana (miles $)")
ax.set_ylabel("Costo suministro / semana (miles $)")
ax.set_title("Trade-off: inventario vs suministro", fontsize=11)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fK"))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fK"))
ax.legend(fontsize=8)

# — Panel C: Distribución NS por tipo de política —
ax = axes[1, 0]
for tipo, color in COLORES.items():
    sub = df_res[df_res["tipo_politica"] == tipo]["ns_media"] * 100
    sns.kdeplot(sub, ax=ax, color=color, fill=True, alpha=0.35, label=tipo)
ax.axvline(80, color="red", linestyle="--", lw=1.5, label="Objetivo 80%")
ax.set_xlabel("Nivel de servicio promedio (%)")
ax.set_ylabel("Densidad")
ax.set_title("Distribución del nivel de servicio\npor tipo de política", fontsize=11)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.legend(fontsize=8)

# — Panel D: Heatmap NS para Lunes+Miércoles —
ax = axes[1, 1]
pivot_ns = df_res[df_res["tipo_politica"] == "Lunes + Miércoles"].pivot_table(
    index="q_mierc", columns="q_lunes", values="ns_media", aggfunc="mean"
)
sns.heatmap(
    pivot_ns * 100, ax=ax, cmap="RdYlGn", annot=True, fmt=".0f",
    linewidths=0.5, vmin=0, vmax=100,
    cbar_kws={"label": "NS promedio (%)"}
)
ax.set_title("Nivel de servicio (%)\nLunes + Miércoles", fontsize=11)
ax.set_xlabel("Cajas pedidas el lunes")
ax.set_ylabel("Cajas pedidas el miércoles")

plt.tight_layout()
# plt.savefig("/mnt/user-data/outputs/bloque4_motor_montecarlo.png",
#             dpi=150, bbox_inches="tight")
plt.show()
print("Gráfico guardado: bloque4_motor_montecarlo.png")

"""
Resultados del Bloque 4 ✅
El motor evaluó 201.000 semanas simuladas (67 escenarios × 30 réplicas × 100 semanas) en 18
segundos. Los hallazgos más importantes:
Escenarios que cumplen NS ≥ 80%: 55 de 67, todos con estimación robusta (percentil 10 también ≥ 80%).
Top 5 candidatos por menor costo total:

Escenario   Política    Cajas/sem   NS      Costo/sem
L15M30      Lun+Mié     45          96.2%   $397.990
L20M25      Lun+Mié     45          96.3%   $404.581
L25M20      Lun+Mié     45          96.3%   $412.581
L30M15      Lun+Mié     45          96.3%   $420.581
L45         Solo lunes  45          96.3%   $429.581

Patrón claro: la política Lunes + Miércoles con 45 cajas totales domina en costo gracias a que
distribuir el inventario en dos entregas reduce los días que las cajas permanecen almacenadas (menor
costo de holding). El escenario L15M30 lidera porque concentrar más cajas el miércoles cubre los
días de mayor permanencia (jue–dom) con menos días de acumulación previa.
El Bloque 5 confirmará y presentará la solución óptima final con análisis completo.
"""

#%%
##########################################################
# RECONSTRUIR DISTRIBUCIÓN Y PARÁMETROS (auto-contenido) #
##########################################################

"""
Bloque 5 — Optimización y análisis de resultados finales
Descripción
Consumir los resultados del Bloque 4, identificar la política óptima, comparar todas las 
alternativas viables y producir el informe visual y tabular completo con la recomendación final 
para el administrador del supermercado.

Justificación
Con los 67 escenarios ya evaluados, este bloque aplica el criterio de decisión del problema: 
minimizar costo total sujeto a NS ≥ 80%. Se produce un dashboard ejecutivo completo que incluye 
comparación contra la línea base, análisis de sensibilidad y simulación detallada de la política
ganadora.
"""

ventas   = np.array([0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10])
num_dias = np.array([1,  5, 12, 19, 27, 59, 74, 59, 49, 37, 22])
prob     = num_dias / num_dias.sum()

N_SEMANAS   = 100
N_REPLICAS  = 30
COSTO_INV   = 800
COSTO_FIJO  = 15000
COSTO_VAR   = 100
OBJETIVO_NS = 0.80

#%%
####################################################
# MOTORES DE SIMULACIÓN (reutilizados de Bloque 4) #
####################################################

def simular_una_replica(dias_entrega, cantidades, n_semanas, semilla):
    rng        = np.random.default_rng(semilla)
    inventario = 0
    acum_ci = acum_cs = sem_sin_so = total_falt = 0

    for _ in range(n_semanas):
        stockout = False
        for dia in range(7):
            cs_dia = 0
            if dia in dias_entrega:
                idx         = dias_entrega.index(dia)
                q           = cantidades[idx]
                inventario += q
                cs_dia      = COSTO_FIJO + COSTO_VAR * q
            demanda = int(rng.choice(ventas, p=prob))
            if demanda <= inventario:
                inventario -= demanda
            else:
                total_falt += demanda - inventario
                inventario  = 0
                stockout    = True
            acum_ci += inventario * COSTO_INV
            acum_cs += cs_dia
        if not stockout:
            sem_sin_so += 1

    return {
        "nivel_servicio":  sem_sin_so / n_semanas,
        "costo_inv_sem":   acum_ci / n_semanas,
        "costo_sum_sem":   acum_cs / n_semanas,
        "costo_total_sem": (acum_ci + acum_cs) / n_semanas,
        "faltantes_sem":   total_falt / n_semanas,
    }


def evaluar_escenario(dias_entrega, cantidades,
                      n_semanas=N_SEMANAS, n_replicas=N_REPLICAS):
    res = [simular_una_replica(dias_entrega, cantidades, n_semanas, r*1000)
           for r in range(n_replicas)]
    df  = pd.DataFrame(res)
    return {k: df[k].mean() for k in df.columns} | {
        "ns_std":  df["nivel_servicio"].std(),
        "ns_p10":  df["nivel_servicio"].quantile(0.10),
        "ct_std":  df["costo_total_sem"].std(),
    }


def simular_detalle_diario(dias_entrega, cantidades, n_semanas, semilla=42):
    """Devuelve DataFrame con detalle día a día para graficar inventario."""
    rng        = np.random.default_rng(semilla)
    inventario = 0
    filas      = []

    for sem in range(n_semanas):
        for dia in range(7):
            entrega = cs_dia = 0
            if dia in dias_entrega:
                idx         = dias_entrega.index(dia)
                entrega     = cantidades[idx]
                inventario += entrega
                cs_dia      = COSTO_FIJO + COSTO_VAR * entrega
            demanda = int(rng.choice(ventas, p=prob))
            faltante = max(0, demanda - inventario)
            inventario = max(0, inventario - demanda)
            filas.append({
                "semana": sem + 1,
                "dia":    dia,
                "dia_g":  sem * 7 + dia + 1,
                "entrega": entrega,
                "demanda": demanda,
                "faltante": faltante,
                "inv_fin":  inventario,
                "ci_dia":   inventario * COSTO_INV,
                "cs_dia":   cs_dia,
            })
    return pd.DataFrame(filas)

#%%
###################################
# RE-EVALUAR TODOS LOS ESCENARIOS #
###################################

RANGO_1 = list(range(30, 75, 5))
RANGO_2 = list(range(15, 50, 5))

escenarios_raw = []
for q in RANGO_1:
    escenarios_raw.append({"id": f"L{q}",       "tipo": "Solo lunes",
                            "dias": [0],         "cant": [q],
                            "q_lun": q, "q_mie": 0})
for q in RANGO_1:
    escenarios_raw.append({"id": f"M{q}",       "tipo": "Solo miércoles",
                            "dias": [2],         "cant": [q],
                            "q_lun": 0, "q_mie": q})
for ql, qm in itertools.product(RANGO_2, RANGO_2):
    escenarios_raw.append({"id": f"L{ql}M{qm}", "tipo": "Lunes + Miércoles",
                            "dias": [0, 2],      "cant": [ql, qm],
                            "q_lun": ql, "q_mie": qm})

print(f"Re-evaluando {len(escenarios_raw)} escenarios × {N_REPLICAS} réplicas…")
filas = []
for esc in escenarios_raw:
    m = evaluar_escenario(esc["dias"], esc["cant"])
    filas.append({
        "id_escenario":  esc["id"],
        "tipo_politica": esc["tipo"],
        "q_lunes":       esc["q_lun"],
        "q_mierc":       esc["q_mie"],
        "q_total_sem":   sum(esc["cant"]),
        "n_entregas":    len(esc["dias"]),
        **m,
        "cumple_ns":     m["nivel_servicio"] >= OBJETIVO_NS,
    })
df_res = pd.DataFrame(filas)
print("Listo.\n")

#%%
###############################
# IDENTIFICAR POLÍTICA ÓPTIMA #
###############################

df_ok   = df_res[df_res["cumple_ns"]].copy()
optimo  = df_ok.nsmallest(1, "costo_total_sem").iloc[0]
top10   = df_ok.nsmallest(10, "costo_total_sem").reset_index(drop=True)

# Línea base (30 cajas / lunes)
base    = df_res[df_res["id_escenario"] == "L30"].iloc[0]

print("=" * 68)
print("  POLÍTICA ÓPTIMA")
print("=" * 68)
print(f"  Escenario:          {optimo['id_escenario']}")
print(f"  Tipo:               {optimo['tipo_politica']}")
print(f"  Cajas lunes:        {int(optimo['q_lunes'])}")
print(f"  Cajas miércoles:    {int(optimo['q_mierc'])}")
print(f"  Total cajas/semana: {int(optimo['q_total_sem'])}")
print(f"  Nivel de servicio:  {optimo['nivel_servicio']:.1%}  (±{optimo['ns_std']:.1%})")
print(f"  Costo inv/semana:   ${optimo['costo_inv_sem']:>12,.0f}")
print(f"  Costo sum/semana:   ${optimo['costo_sum_sem']:>12,.0f}")
print(f"  COSTO TOTAL/semana: ${optimo['costo_total_sem']:>12,.0f}")
print(f"  COSTO TOTAL/100sem: ${optimo['costo_total_sem']*100:>12,.0f}")
print("=" * 68)

print("\n  Comparación con línea base (L30 — contrato actual):")
print(f"  Línea base NS:      {base['nivel_servicio']:.1%}")
print(f"  Línea base costo:   ${base['costo_total_sem']*100:>12,.0f}")
ahorro = (base["costo_total_sem"] - optimo["costo_total_sem"]) * 100
print(f"  Ahorro 100 semanas: ${ahorro:>12,.0f}  "
      f"({ahorro/(base['costo_total_sem']*100):.1%} menos)")

print("\n  Top 10 escenarios viables (NS ≥ 80%, menor costo):")
cols_show = ["id_escenario","tipo_politica","q_total_sem",
             "nivel_servicio","costo_total_sem","costo_inv_sem","costo_sum_sem"]
t10 = top10[cols_show].copy()
t10["nivel_servicio"]   = t10["nivel_servicio"].map("{:.1%}".format)
t10["costo_total_sem"]  = t10["costo_total_sem"].map("${:,.0f}".format)
t10["costo_inv_sem"]    = t10["costo_inv_sem"].map("${:,.0f}".format)
t10["costo_sum_sem"]    = t10["costo_sum_sem"].map("${:,.0f}".format)
print(t10.to_string(index=False))

#%%
##############################################
# SIMULACIÓN DETALLADA DE LA POLÍTICA ÓPTIMA #
##############################################

dias_opt = [0, 2]
cant_opt = [int(optimo["q_lunes"]), int(optimo["q_mierc"])]
df_det   = simular_detalle_diario(dias_opt, cant_opt, N_SEMANAS)

df_sem_opt = df_det.groupby("semana").agg(
    faltante_total  = ("faltante",  "sum"),
    stockout        = ("faltante",  lambda x: (x > 0).any()),
    costo_inv       = ("ci_dia",    "sum"),
    costo_sum       = ("cs_dia",    "sum"),
).reset_index()
df_sem_opt["costo_total"] = df_sem_opt["costo_inv"] + df_sem_opt["costo_sum"]
ns_opt_det = (~df_sem_opt["stockout"]).mean()

#%%
#######################
# DASHBOARD EJECUTIVO #
#######################

sns.set_theme(style="whitegrid", font_scale=1.05)

COLORES = {
    "Solo lunes":         "#2E86AB",
    "Solo miércoles":     "#F4A261",
    "Lunes + Miércoles":  "#2D6A4F",
}
C_OPT  = "#E84855"   # rojo para resaltar óptimo
C_BASE = "#999999"   # gris para línea base
C_INV  = "#F4A261"
C_SUM  = "#2E86AB"

fig = plt.figure(figsize=(18, 14))
gs  = gridspec.GridSpec(3, 3, figure=fig,
                         hspace=0.42, wspace=0.35)

fig.suptitle(
    "SIMULACIÓN MONTE CARLO — Inventario de Leche\n"
    "Análisis de Política Óptima de Pedido (100 semanas)",
    fontsize=15, fontweight="bold", y=0.98
)

# ── A: Frontera eficiente NS vs Costo ─────────────────────
ax_a = fig.add_subplot(gs[0, :2])
for tipo, color in COLORES.items():
    sub = df_res[df_res["tipo_politica"] == tipo]
    sub_ok  = sub[sub["cumple_ns"]]
    sub_nok = sub[~sub["cumple_ns"]]
    ax_a.scatter(sub_nok["nivel_servicio"]*100, sub_nok["costo_total_sem"]/1000,
                 color=color, alpha=0.25, s=35, marker="x")
    ax_a.scatter(sub_ok["nivel_servicio"]*100,  sub_ok["costo_total_sem"]/1000,
                 color=color, alpha=0.75, s=50,  label=tipo)

# Marcar óptimo
ax_a.scatter(optimo["nivel_servicio"]*100, optimo["costo_total_sem"]/1000,
             color=C_OPT, s=180, zorder=6, marker="*", label=f"Óptimo: {optimo['id_escenario']}")
ax_a.scatter(base["nivel_servicio"]*100,   base["costo_total_sem"]/1000,
             color=C_BASE, s=120, zorder=6, marker="D", label=f"Base: L30")

ax_a.axvline(80, color="red", linestyle="--", lw=1.3, alpha=0.7)
ax_a.text(80.5, ax_a.get_ylim()[1]*0.95 if ax_a.get_ylim()[1] > 0 else 1200,
          "NS = 80%", color="red", fontsize=8)
ax_a.set_xlabel("Nivel de servicio promedio (%)")
ax_a.set_ylabel("Costo total / semana (miles $)")
ax_a.set_title("Frontera eficiente: NS vs Costo total/semana\n"
               "(× = no cumple NS, • = cumple NS)", fontsize=11)
ax_a.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax_a.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fK"))
ax_a.legend(fontsize=8, loc="upper left")
ax_a.annotate(
    f"  ★ {optimo['id_escenario']}\n  NS={optimo['nivel_servicio']:.0%}"
    f"\n  ${optimo['costo_total_sem']/1000:.0f}K/sem",
    xy=(optimo["nivel_servicio"]*100, optimo["costo_total_sem"]/1000),
    xytext=(optimo["nivel_servicio"]*100 - 18,
            optimo["costo_total_sem"]/1000 + 150),
    arrowprops=dict(arrowstyle="->", color="black", lw=1),
    fontsize=8, bbox=dict(boxstyle="round,pad=0.3",
                          fc="lightyellow", ec="gray", lw=0.8)
)

# ── B: Heatmap costo total Lunes+Miércoles ───────────────
ax_b = fig.add_subplot(gs[0, 2])
pivot_ct = df_res[df_res["tipo_politica"] == "Lunes + Miércoles"].pivot_table(
    index="q_mierc", columns="q_lunes", values="costo_total_sem", aggfunc="mean"
)
mask_nok = df_res[df_res["tipo_politica"] == "Lunes + Miércoles"].pivot_table(
    index="q_mierc", columns="q_lunes", values="cumple_ns", aggfunc="mean"
) < OBJETIVO_NS

sns.heatmap(pivot_ct/1000, ax=ax_b, cmap="YlOrRd_r",
            annot=True, fmt=".0f", linewidths=0.4,
            cbar_kws={"label": "Miles $/sem"},
            mask=mask_nok)
# Marcar celda óptima
q_l_idx = sorted(df_res[df_res["tipo_politica"]=="Lunes + Miércoles"]["q_lunes"].unique()).index(int(optimo["q_lunes"]))
q_m_idx = sorted(df_res[df_res["tipo_politica"]=="Lunes + Miércoles"]["q_mierc"].unique(), reverse=True).index(int(optimo["q_mierc"]))
ax_b.add_patch(plt.Rectangle((q_l_idx, q_m_idx), 1, 1,
               fill=False, edgecolor=C_OPT, lw=2.5, zorder=5))
ax_b.set_title("Costo total/sem (miles $)\nLunes+Miércoles (NS≥80% visible)", fontsize=10)
ax_b.set_xlabel("Cajas lunes")
ax_b.set_ylabel("Cajas miércoles")

# ── C: Inventario diario óptimo (semanas 1-15) ────────────
ax_c = fig.add_subplot(gs[1, :2])
dias_15 = df_det[df_det["semana"] <= 15].copy()

ax_c.fill_between(dias_15["dia_g"], dias_15["inv_fin"],
                  color=C_INV, alpha=0.35)
ax_c.plot(dias_15["dia_g"], dias_15["inv_fin"],
          color=C_INV, lw=1.2, label="Inventario fin día")

# Marcar entregas
ent_lun = dias_15[(dias_15["dia"] == 0) & (dias_15["entrega"] > 0)]
ent_mie = dias_15[(dias_15["dia"] == 2) & (dias_15["entrega"] > 0)]
ax_c.vlines(ent_lun["dia_g"], 0, dias_15["inv_fin"].max()*1.05,
            colors="#2E86AB", lw=0.7, alpha=0.5, linestyle="--", label="Entrega lunes")
ax_c.vlines(ent_mie["dia_g"], 0, dias_15["inv_fin"].max()*1.05,
            colors="#2D6A4F", lw=0.7, alpha=0.5, linestyle=":", label="Entrega miércoles")

# Marcar faltantes
falt = dias_15[dias_15["faltante"] > 0]
ax_c.scatter(falt["dia_g"], [0]*len(falt),
             color=C_OPT, s=30, zorder=5, label="Faltante")

ax_c.set_title(f"Inventario diario — Política óptima: {optimo['id_escenario']} "
               f"(semanas 1–15)", fontsize=11)
ax_c.set_xlabel("Día global")
ax_c.set_ylabel("Cajas en inventario")
ax_c.legend(fontsize=8, ncol=4)

# ── D: Desglose costo top-5 políticas ─────────────────────
ax_d = fig.add_subplot(gs[1, 2])
top5  = df_ok.nsmallest(5, "costo_total_sem")
etiq  = top5["id_escenario"].tolist() + ["L30\n(base)"]
c_inv = top5["costo_inv_sem"].tolist() + [base["costo_inv_sem"]]
c_sum = top5["costo_sum_sem"].tolist() + [base["costo_sum_sem"]]
x_pos = range(len(etiq))

bars1 = ax_d.bar(x_pos, [v/1000 for v in c_inv],
                 color=C_INV, label="Inventario")
bars2 = ax_d.bar(x_pos, [v/1000 for v in c_sum],
                 bottom=[v/1000 for v in c_inv],
                 color=C_SUM, label="Suministro")
ax_d.set_xticks(list(x_pos))
ax_d.set_xticklabels(etiq, fontsize=8)
ax_d.set_ylabel("Miles $/semana")
ax_d.set_title("Desglose de costos\nTop-5 + línea base", fontsize=10)
ax_d.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fK"))
ax_d.legend(fontsize=8)
# Resaltar barra óptima
bars1[0].set_edgecolor(C_OPT)
bars1[0].set_linewidth(2.5)
bars2[0].set_edgecolor(C_OPT)
bars2[0].set_linewidth(2.5)

# ── E: Nivel de servicio acumulado — óptimo vs base ───────
ax_e = fig.add_subplot(gs[2, :2])
ns_base_acum = []
inv_b, so_b  = 0, 0
rng_b = np.random.default_rng(42)
for sem in range(N_SEMANAS):
    so = False
    for d in range(7):
        if d == 0:
            inv_b += 30
        dm = int(rng_b.choice(ventas, p=prob))
        if dm > inv_b:
            inv_b = 0; so = True
        else:
            inv_b -= dm
    if not so: so_b += 1
    ns_base_acum.append(so_b / (sem + 1) * 100)

ns_opt_acum = []
so_o = 0
for _, grp in df_sem_opt.iterrows():
    if not grp["stockout"]: so_o += 1
    ns_opt_acum.append(so_o / grp["semana"] * 100)

semanas = list(range(1, N_SEMANAS + 1))
ax_e.plot(semanas, ns_opt_acum,  color=C_OPT,  lw=2,
          label=f"Óptimo {optimo['id_escenario']} — NS final: {ns_opt_det:.0%}")
ax_e.plot(semanas, ns_base_acum, color=C_BASE, lw=1.5,
          linestyle="--", label=f"Base L30 — NS final: {ns_base_acum[-1]/100:.0%}")
ax_e.axhline(80, color="red", linestyle=":", lw=1.3, label="Objetivo 80%")
ax_e.fill_between(semanas, ns_opt_acum, 80,
                  where=[v < 80 for v in ns_opt_acum],
                  alpha=0.15, color=C_OPT)
ax_e.set_ylim(0, 105)
ax_e.set_xlabel("Semana")
ax_e.set_ylabel("% semanas sin stockout")
ax_e.set_title("Nivel de servicio acumulado: política óptima vs línea base", fontsize=11)
ax_e.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax_e.legend(fontsize=9)

# ── F: Tabla resumen ejecutiva ─────────────────────────────
ax_f = fig.add_subplot(gs[2, 2])
ax_f.axis("off")

def fmt_k(v):    return f"${v/1000:,.0f}K"
def fmt_pct(v):  return f"{v:.0%}"

tabla_data = [
    ["",                    "Base (L30)",          f"Óptimo ({optimo['id_escenario']})"],
    ["Días entrega",        "Lunes",               "Lunes + Miércoles"],
    ["Cajas lunes",         "30",                  str(int(optimo["q_lunes"]))],
    ["Cajas miércoles",     "0",                   str(int(optimo["q_mierc"]))],
    ["Total cajas/sem",     "30",                  str(int(optimo["q_total_sem"]))],
    ["Nivel servicio",      fmt_pct(base["nivel_servicio"]),
                                                   fmt_pct(optimo["nivel_servicio"])],
    ["Cumple obj. 80%",     "✗",                   "✓"],
    ["C. inventario/sem",   fmt_k(base["costo_inv_sem"]),
                                                   fmt_k(optimo["costo_inv_sem"])],
    ["C. suministro/sem",   fmt_k(base["costo_sum_sem"]),
                                                   fmt_k(optimo["costo_sum_sem"])],
    ["C. total/sem",        fmt_k(base["costo_total_sem"]),
                                                   fmt_k(optimo["costo_total_sem"])],
    ["C. total/100 sem",    fmt_k(base["costo_total_sem"]*100),
                                                   fmt_k(optimo["costo_total_sem"]*100)],
]

tbl = ax_f.table(
    cellText   = tabla_data,
    cellLoc    = "center",
    loc        = "center",
    bbox       = [0, 0, 1, 1],
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)

# Estilo de celdas
for (r, c), cell in tbl.get_celld().items():
    cell.set_edgecolor("#cccccc")
    if r == 0:                                        # encabezado
        cell.set_facecolor("#2D3E50")
        cell.set_text_props(color="white", fontweight="bold")
    elif r % 2 == 0:
        cell.set_facecolor("#f5f5f5")
    else:
        cell.set_facecolor("white")
    if c == 2 and r > 0:                              # columna óptimo
        cell.set_facecolor("#fff3cd")
    if r == 6 and c == 2:                             # fila "Cumple"
        cell.set_facecolor("#d4edda")
        cell.set_text_props(color="#155724", fontweight="bold")
    if r == 6 and c == 1:
        cell.set_facecolor("#f8d7da")
        cell.set_text_props(color="#721c24", fontweight="bold")

ax_f.set_title("Tabla Resumen Ejecutiva", fontsize=10,
               fontweight="bold", pad=8)

# plt.savefig("/mnt/user-data/outputs/bloque5_dashboard_optimo.png",
#             dpi=150, bbox_inches="tight")
plt.show()
print("Dashboard guardado: bloque5_dashboard_optimo.png")

#%%
###############################
# CONCLUSIÓN FINAL EN CONSOLA #
###############################

ahorro_sem = base["costo_total_sem"] - optimo["costo_total_sem"]
print()
print("╔══════════════════════════════════════════════════════════════╗")
print("║              CONCLUSIÓN — POLÍTICA ÓPTIMA                    ║")
print("╠══════════════════════════════════════════════════════════════╣")
print(f"║  Política:       {optimo['id_escenario']:<44}║")
print(f"║  Descripción:    {int(optimo['q_lunes'])} cajas el lunes + "
      f"{int(optimo['q_mierc'])} cajas el miércoles{' '*(12-len(str(int(optimo['q_mierc']))))}║")
print(f"║  Total semanal:   {int(optimo['q_total_sem'])} cajas/semana"
      f"{'':>36}║")
print(f"║  Nivel servicio:  {optimo['nivel_servicio']:.1%}"
      f"  (objetivo ≥ 80%  ✓){'':>27}║")
print(f"║  Costo total/sem: ${optimo['costo_total_sem']:>10,.0f}{'':>37}║")
print(f"║  Ahorro vs base:  ${ahorro_sem:>10,.0f} / semana"
      f"{'':>30}║")
print(f"║                   ${ahorro_sem*100:>10,.0f} en 100 semanas"
      f"{'':>26}║")
print("╚══════════════════════════════════════════════════════════════╝")

# Exportar tabla final
top10_exp = df_ok.nsmallest(10, "costo_total_sem")[
    ["id_escenario","tipo_politica","q_lunes","q_mierc",
     "q_total_sem","nivel_servicio","costo_total_sem",
     "costo_inv_sem","costo_sum_sem","faltantes_sem"]
].reset_index(drop=True)

"""
Resultados del Bloque 5 ✅ — Solución Final
🏆 Política Óptima: L15M30
Atributo                Valor
Días de entrega         Lunes + Miércoles
Cajas el lunes          15
Cajas el miércoles      30
Total semanal           45 cajas
Nivel de servicio       96.2% ✓ (objetivo ≥ 80%)
Costo inventario/sem    $363.490
Costo suministro/sem    $34.500
Costo total/semana      $397.990

📊 Interpretación ejecutiva
¿Por qué L15M30 gana frente a L45 (solo lunes, mismas cajas)? Recibir 30 cajas el miércoles en lugar
del lunes reduce los días que ese stock permanece en bodega: las 30 cajas llegan a mitad de semana y
cubren jue–dom, acumulando solo 4 días de holding en lugar de 7. Eso explica la diferencia de 
~$32.000/semana en costo de inventario.

¿Por qué 45 cajas y no 50? Con 50 cajas el NS sube a ~99.9% (sobrestock innecesario) y el costo de
inventario se dispara a ~$1.7M/semana —más de 4 veces mayor—, porque las cajas sobrantes se acumulan
día tras día. Las 45 cajas cubren con holgura la demanda media (44 cajas) sin generar inventario
residual excesivo.

Ahorro vs contrato actual: $333.117/semana → $33.3 millones en 100 semanas, pasando de un nivel de
servicio del 1% a 96.2%.
"""

#%%
########
# main #
########

def main(**kwargs):
    logging.info("Programa: SimulacionMCPy")


if __name__ == "__main__":
    fn_limpieza_carpeta('D:\SimulAva\logs')
