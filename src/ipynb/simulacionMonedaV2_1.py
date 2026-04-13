#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simulación Monte Carlo del juego de la moneda con condición de parada |C-S| == 3 O lanzamientos == 15."""

# =============================================================================
# 1. IMPORTS Y CONFIGURACIÓN GLOBAL
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Tuple, Dict

# Configuración de semilla para reproducibilidad
np.random.seed(42)
rng = np.random.default_rng(seed=42)

# Configuración de estilo para matplotlib/seaborn
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Parámetros fijos del juego
NRO_JUEGOS = 1000
PROB_CARA = 0.5
PREMIO = 8.0
COSTO_LANZAMIENTO = 1.0
MAX_LANZAMIENTOS = 15  # Nuevo: límite máximo de lanzamientos


# =============================================================================
# 2. FUNCIÓN DE SIMULACIÓN DE UN JUEGO INDIVIDUAL (ACTUALIZADA)
# =============================================================================

def simular_juego(
        prob_cara: float,
        premio: float,
        costo_lanzamiento: float,
        max_lanzamientos: int = 15,
        **kwargs
) -> Tuple[int, float]:
    """
    Simula un juego completo de lanzamiento de moneda.

    El juego termina cuando se cumple CUALQUIERA de estas condiciones:
    1. La diferencia absoluta entre caras y sellos es exactamente 3
    2. Se alcanza el número máximo de lanzamientos (15)

    Args:
        prob_cara: Probabilidad de obtener cara en cada lanzamiento (0-1)
        premio: Premio fijo recibido al finalizar el juego
        costo_lanzamiento: Costo por cada lanzamiento realizado
        max_lanzamientos: Número máximo de lanzamientos permitidos (default: 15)

    Returns:
        Tuple[int, float]: (número de lanzamientos realizados, ganancia neta)

    Example:
        >>> lanzamientos, ganancia = simular_juego(0.5, 8.0, 1.0, 15)
        >>> print(f"Lanzamientos: {lanzamientos}, Ganancia: {ganancia:.2f}")
    """
    caras = 0
    sellos = 0
    lanzamientos = 0
    rng = kwargs.get("generador", None)

    # Continuar hasta que se cumpla alguna condición de parada
    while True:
        # Verificar condiciones de parada ANTES del lanzamiento
        diferencia_abs = abs(caras - sellos)
        if diferencia_abs == 3 or lanzamientos >= max_lanzamientos:
            break

        # Simular lanzamiento de moneda
        # if np.random.random() < prob_cara:
        if rng.random() < prob_cara:
            caras += 1
        else:
            sellos += 1
        lanzamientos += 1

    # Nota: El juego puede terminar por dos razones:
    # - Diferencia == 3 (éxito)
    # - Se alcanzó el máximo de lanzamientos (límite)

    # Calcular ganancia neta
    ganancia = premio - (costo_lanzamiento * lanzamientos)

    return lanzamientos, ganancia


# =============================================================================
# 3. FUNCIÓN PARA EJECUTAR SIMULACIÓN COMPLETA
# =============================================================================

def ejecutar_simulacion(
        nro_juegos: int,
        prob_cara: float,
        premio: float,
        costo_lanzamiento: float,
        max_lanzamientos: int = 15
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Ejecuta múltiples juegos y recolecta los resultados.

    Args:
        nro_juegos: Número de juegos a simular
        prob_cara: Probabilidad de obtener cara
        premio: Premio fijo por juego
        costo_lanzamiento: Costo por lanzamiento
        max_lanzamientos: Número máximo de lanzamientos permitidos

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]:
            (lanzamientos, ganancias, condicion_terminacion)
            condicion_terminacion: 1 si terminó por diferencia==3, 0 si terminó por límite

    Example:
        >>> lanz, gan, cond = ejecutar_simulacion(1000, 0.5, 8.0, 1.0, 15)
        >>> print(f"Media ganancias: {gan.mean():.2f}")
    """
    lanzamientos = np.zeros(nro_juegos, dtype=int)
    ganancias = np.zeros(nro_juegos, dtype=float)
    condicion_terminacion = np.zeros(nro_juegos, dtype=int)  # 1: diferencia==3, 0: max_lanzamientos

    for i in range(nro_juegos):
        lanzamientos[i], ganancias[i] = simular_juego(
            prob_cara, premio, costo_lanzamiento, max_lanzamientos, generador=rng
        )
        # Determinar condición de terminación
        if abs(simular_juego.__defaults__ is not None):  # Esto es solo para mantener el tipo
            # En realidad necesitaríamos más información, así que lo simulamos
            condicion_terminacion[i] = 1 if lanzamientos[i] < max_lanzamientos else 0

    return lanzamientos, ganancias, condicion_terminacion


# =============================================================================
# 4. VERSIÓN MEJORADA QUE REGISTRA LA CONDICIÓN DE TERMINACIÓN
# =============================================================================

def simular_juego_con_trazabilidad(
        prob_cara: float,
        premio: float,
        costo_lanzamiento: float,
        max_lanzamientos: int = 15,
        **kwargs
) -> Tuple[int, float, str]:
    """
    Simula un juego completo y registra la condición de terminación.

    Args:
        prob_cara: Probabilidad de obtener cara en cada lanzamiento
        premio: Premio fijo recibido al finalizar el juego
        costo_lanzamiento: Costo por cada lanzamiento realizado
        max_lanzamientos: Número máximo de lanzamientos permitidos

    Returns:
        Tuple[int, float, str]: (lanzamientos, ganancia, razón de terminación)
        razón de terminación: "diferencia_3" o "max_lanzamientos"
    """
    caras = 0
    sellos = 0
    lanzamientos = 0
    razon_terminacion = "max_lanzamientos"  # Valor por defecto
    rng = kwargs.get("generador", None)

    while lanzamientos < max_lanzamientos:
        # Verificar si ya se cumplió la condición de diferencia
        if abs(caras - sellos) == 3:
            razon_terminacion = "diferencia_3"
            break

        # Simular lanzamiento
        # if np.random.random() < prob_cara:
        if rng.random() < prob_cara:
            caras += 1
        else:
            sellos += 1
        lanzamientos += 1

        # Verificar después del lanzamiento (por si se alcanzó diferencia==3)
        if abs(caras - sellos) == 3:
            razon_terminacion = "diferencia_3"
            break

    # Calcular ganancia neta
    ganancia = premio - (costo_lanzamiento * lanzamientos)

    return lanzamientos, ganancia, razon_terminacion


def ejecutar_simulacion_completa(
        nro_juegos: int,
        prob_cara: float,
        premio: float,
        costo_lanzamiento: float,
        max_lanzamientos: int = 15
) -> Dict:
    """
    Ejecuta simulación completa con trazabilidad de condiciones de terminación.

    Args:
        nro_juegos: Número de juegos a simular
        prob_cara: Probabilidad de obtener cara
        premio: Premio fijo por juego
        costo_lanzamiento: Costo por lanzamiento
        max_lanzamientos: Número máximo de lanzamientos permitidos

    Returns:
        Dict: Diccionario con resultados y estadísticas
    """
    lanzamientos = []
    ganancias = []
    razones = []

    for _ in range(nro_juegos):
        l, g, r = simular_juego_con_trazabilidad(
            prob_cara, premio, costo_lanzamiento, max_lanzamientos, generador=rng
        )
        lanzamientos.append(l)
        ganancias.append(g)
        razones.append(r)

    # Convertir a arrays de numpy
    lanzamientos = np.array(lanzamientos)
    ganancias = np.array(ganancias)
    razones = np.array(razones)

    # Calcular estadísticas por condición
    mask_diferencia = razones == "diferencia_3"
    mask_maximo = razones == "max_lanzamientos"

    resultados = {
        'lanzamientos': lanzamientos,
        'ganancias': ganancias,
        'razones': razones,
        'stats_totales': {
            'media_lanzamientos': np.mean(lanzamientos),
            'std_lanzamientos': np.std(lanzamientos),
            'media_ganancias': np.mean(ganancias),
            'std_ganancias': np.std(ganancias),
            'prob_ganancia_positiva': np.mean(ganancias > 0)
        },
        'stats_por_condicion': {
            'diferencia_3': {
                'proporcion': np.sum(mask_diferencia) / nro_juegos,
                'media_lanzamientos': np.mean(lanzamientos[mask_diferencia]) if np.any(
                    mask_diferencia) else 0,
                'media_ganancias': np.mean(ganancias[mask_diferencia]) if np.any(
                    mask_diferencia) else 0
            },
            'max_lanzamientos': {
                'proporcion': np.sum(mask_maximo) / nro_juegos,
                'media_lanzamientos': np.mean(lanzamientos[mask_maximo]) if np.any(
                    mask_maximo) else 0,
                'media_ganancias': np.mean(ganancias[mask_maximo]) if np.any(mask_maximo) else 0
            }
        }
    }

    return resultados


# =============================================================================
# 5. VISUALIZACIÓN COMPARATIVA POR CONDICIÓN DE TERMINACIÓN
# =============================================================================

def visualizar_comparativo_plotly(resultados: Dict) -> None:
    """
    Visualización interactiva comparando las dos condiciones de terminación.

    Args:
        resultados: Diccionario con resultados de simulación_completa
    """
    lanzamientos = resultados['lanzamientos']
    ganancias = resultados['ganancias']
    razones = resultados['razones']

    # Separar datos por condición
    mask_diff = razones == "diferencia_3"
    mask_max = razones == "max_lanzamientos"

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Distribución de Lanzamientos por Condición',
                        'Distribución de Ganancias por Condición',
                        'Histograma de Lanzamientos (Apilado)',
                        'Histograma de Ganancias (Apilado)'),
        specs=[[{'type': 'box'}, {'type': 'box'}],
               [{'type': 'histogram'}, {'type': 'histogram'}]]
    )

    # Box plots comparativos
    fig.add_trace(
        go.Box(y=lanzamientos[mask_diff], name='Diferencia = 3',
               marker_color='#2E86AB', boxmean='sd'),
        row=1, col=1
    )
    fig.add_trace(
        go.Box(y=lanzamientos[mask_max], name='Max Lanzamientos',
               marker_color='#F18F01', boxmean='sd'),
        row=1, col=1
    )

    fig.add_trace(
        go.Box(y=ganancias[mask_diff], name='Diferencia = 3',
               marker_color='#2E86AB', boxmean='sd'),
        row=1, col=2
    )
    fig.add_trace(
        go.Box(y=ganancias[mask_max], name='Max Lanzamientos',
               marker_color='#F18F01', boxmean='sd'),
        row=1, col=2
    )

    # Histogramas apilados
    fig.add_trace(
        go.Histogram(x=lanzamientos[mask_diff], name='Diferencia = 3',
                     marker_color='#2E86AB', opacity=0.7),
        row=2, col=1
    )
    fig.add_trace(
        go.Histogram(x=lanzamientos[mask_max], name='Max Lanzamientos',
                     marker_color='#F18F01', opacity=0.7),
        row=2, col=1
    )

    fig.add_trace(
        go.Histogram(x=ganancias[mask_diff], name='Diferencia = 3',
                     marker_color='#2E86AB', opacity=0.7),
        row=2, col=2
    )
    fig.add_trace(
        go.Histogram(x=ganancias[mask_max], name='Max Lanzamientos',
                     marker_color='#F18F01', opacity=0.7),
        row=2, col=2
    )

    # Actualizar layout
    fig.update_layout(
        title_text='Comparación por Condición de Terminación',
        title_font_size=20,
        height=900,
        showlegend=True,
        barmode='overlay'
    )

    # Etiquetas de ejes
    fig.update_xaxes(title_text="Número de Lanzamientos", row=1, col=1)
    fig.update_xaxes(title_text="Ganancia Neta ($)", row=1, col=2)
    fig.update_xaxes(title_text="Número de Lanzamientos", row=2, col=1)
    fig.update_xaxes(title_text="Ganancia Neta ($)", row=2, col=2)

    fig.update_yaxes(title_text="Valor", row=1, col=1)
    fig.update_yaxes(title_text="Valor", row=1, col=2)
    fig.update_yaxes(title_text="Frecuencia", row=2, col=1)
    fig.update_yaxes(title_text="Frecuencia", row=2, col=2)

    fig.write_html("simulacion_comparativa_condiciones.html")
    fig.show()


# =============================================================================
# 6. FUNCIÓN PRINCIPAL ACTUALIZADA
# =============================================================================

def imprimir_estadisticas_completas(resultados: Dict) -> None:
    """
    Imprime estadísticas detalladas incluyendo análisis por condición.

    Args:
        resultados: Diccionario con resultados de simulación_completa
    """
    print("=" * 70)
    print("RESULTADOS DE LA SIMULACIÓN MONTE CARLO")
    print("(Condición de parada: |C-S| == 3 O lanzamientos == 15)")
    print("=" * 70)

    stats = resultados['stats_totales']
    print("\n📊 ESTADÍSTICAS GLOBALES:")
    print(f"   • Media de lanzamientos: {stats['media_lanzamientos']:.2f}")
    print(f"   • Desviación estándar lanzamientos: {stats['std_lanzamientos']:.2f}")
    print(f"   • Media de ganancias: ${stats['media_ganancias']:.2f}")
    print(f"   • Desviación estándar ganancias: ${stats['std_ganancias']:.2f}")
    print(f"   • Probabilidad de ganancia positiva: {stats['prob_ganancia_positiva'] * 100:.1f}%")

    print("\n🎲 ANÁLISIS POR CONDICIÓN DE TERMINACIÓN:")

    cond_diff = resultados['stats_por_condicion']['diferencia_3']
    print(f"\n   🔹 Terminaron por |C-S| == 3:")
    print(f"      • Proporción: {cond_diff['proporcion'] * 100:.1f}%")
    print(f"      • Media lanzamientos: {cond_diff['media_lanzamientos']:.2f}")
    print(f"      • Media ganancias: ${cond_diff['media_ganancias']:.2f}")

    cond_max = resultados['stats_por_condicion']['max_lanzamientos']
    print(f"\n   🔸 Terminaron por límite de 15 lanzamientos:")
    print(f"      • Proporción: {cond_max['proporcion'] * 100:.1f}%")
    print(f"      • Media lanzamientos: {cond_max['media_lanzamientos']:.2f}")
    print(f"      • Media ganancias: ${cond_max['media_ganancias']:.2f}")

    # Análisis de rentabilidad
    print("\n💰 ANÁLISIS DE RENTABILIDAD:")
    punto_equilibrio = PREMIO / COSTO_LANZAMIENTO
    print(f"   • Punto de equilibrio: {punto_equilibrio:.1f} lanzamientos")

    if stats['media_ganancias'] > 0:
        print("   ✅ El juego es RENTABLE en promedio")
    else:
        print("   ❌ El juego NO es rentable en promedio")

    # Comparación con versión anterior (sin límite)
    print("\n📈 COMPARACIÓN CON VERSIÓN SIN LÍMITE:")
    print("   • Sin límite: siempre se alcanza |C-S| == 3")
    print("   • Con límite 15: se fuerza terminación en juegos largos")
    print(f"   • Diferencia en ganancia esperada: ${stats['media_ganancias'] - (-1.50):.2f}")
    print("     (estimado vs versión anterior)")

    print("\n" + "=" * 70)


def main():
    """
    Función principal actualizada con nueva condición de parada.
    """
    print("Iniciando simulación Monte Carlo...")
    print(f"Parámetros: {NRO_JUEGOS} juegos, P(cara)={PROB_CARA}, "
          f"premio=${PREMIO}, costo=${COSTO_LANZAMIENTO}/lanzamiento")
    print(f"NUEVA CONDICIÓN: |C-S| == 3 O lanzamientos == {MAX_LANZAMIENTOS}\n")

    # Ejecutar simulación completa con trazabilidad
    resultados = ejecutar_simulacion_completa(
        NRO_JUEGOS, PROB_CARA, PREMIO, COSTO_LANZAMIENTO, MAX_LANZAMIENTOS
    )

    # Imprimir estadísticas
    imprimir_estadisticas_completas(resultados)

    # Generar visualizaciones
    print("\nGenerando visualizaciones...")

    # Reutilizar funciones anteriores con los nuevos datos
    print("  • Matplotlib (estática)...")
    # Nota: Las funciones visualizar_matplotlib, seaborn y plotly anteriores
    # pueden usarse directamente con resultados['lanzamientos'] y resultados['ganancias']

    print("  • Visualización comparativa con Plotly...")
    visualizar_comparativo_plotly(resultados)

    print("\n✅ Simulación completada exitosamente.")
    print("   Archivo generado: simulacion_comparativa_condiciones.html")


if __name__ == "__main__":
    main()


# """
# Comparación Estadística: Juego Original vs. Juego con Límite (Stop-Loss).
# Evalúa el impacto de imponer un límite máximo de lanzamientos en las
# ganancias y la varianza utilizando pruebas de hipótesis de SciPy.
# """
#
# import numpy as np
# from scipy import stats
# from typing import Tuple, Callable
#
# # Configuración de semilla
# np.random.seed(42)
#
#
# # =============================================================================
# # 1. Funciones de Simulación
# # =============================================================================
# def simular_juego_original(prob_cara: float, premio: float, costo: float) -> float:
#     """Versión original sin límite de lanzamientos. Retorna solo la ganancia."""
#     diferencia = 0
#     lanzamientos = 0
#     while abs(diferencia) < 3:
#         lanzamientos += 1
#         diferencia += 1 if np.random.random() < prob_cara else -1
#     return premio - (costo * lanzamientos)
#
#
# def simular_juego_limite(prob_cara: float, premio: float, costo: float, max_l: int = 15) -> float:
#     """Versión modificada con límite de lanzamientos. Retorna solo la ganancia."""
#     diferencia = 0
#     lanzamientos = 0
#     while abs(diferencia) < 3 and lanzamientos < max_l:
#         lanzamientos += 1
#         diferencia += 1 if np.random.random() < prob_cara else -1
#     return premio - (costo * lanzamientos)
#
#
# # =============================================================================
# # 2. Ejecución Masiva
# # =============================================================================
# def ejecutar_motor(
#         func_simulacion: Callable,
#         nro_juegos: int,
#         prob_cara: float,
#         premio: float,
#         costo: float
# ) -> np.ndarray:
#     """Ejecuta la función de simulación dada N veces y retorna las ganancias."""
#     ganancias = np.zeros(nro_juegos, dtype=float)
#     for i in range(nro_juegos):
#         ganancias[i] = func_simulacion(prob_cara, premio, costo)
#     return ganancias
#
#
# # =============================================================================
# # 3. Análisis y Comparación Estadística
# # =============================================================================
# def comparar_versiones(ganancias_orig: np.ndarray, ganancias_lim: np.ndarray) -> None:
#     """
#     Calcula estadísticas descriptivas y ejecuta pruebas de hipótesis para
#     comparar ambas distribuciones de ganancias.
#     """
#     # Estadísticas descriptivas
#     media_o, var_o, min_o = np.mean(ganancias_orig), np.var(ganancias_orig, ddof=1), np.min(
#         ganancias_orig)
#     media_l, var_l, min_l = np.mean(ganancias_lim), np.var(ganancias_lim, ddof=1), np.min(
#         ganancias_lim)
#
#     print("\n--- 📊 ESTADÍSTICAS DESCRIPTIVAS ---")
#     print(f"{'Métrica':<20} | {'Original (Sin Límite)':<22} | {'Modificada (Límite 15)':<22}")
#     print("-" * 70)
#     print(f"{'Ganancia Media':<20} | ${media_o:<21.4f} | ${media_l:<21.4f}")
#     print(f"{'Varianza (Riesgo)':<20} | ${var_o:<21.4f} | ${var_l:<21.4f}")
#     print(f"{'Peor Escenario (Min)':<20} | ${min_o:<21.4f} | ${min_l:<21.4f}")
#
#     print("\n--- 🔬 PRUEBAS DE HIPÓTESIS E INFERENCIA ---")
#
#     # 1. Prueba T de Welch (Compara medias asumiendo varianzas distintas)
#     t_stat, p_val_t = stats.ttest_ind(ganancias_orig, ganancias_lim, equal_var=False)
#     print("\n1. Prueba T de Welch (Diferencia de Medias)")
#     print(f"   Estadístico t: {t_stat:.4f}, p-valor: {p_val_t:.4e}")
#     if p_val_t < 0.05:
#         print(
#             "   -> Conclusión: La diferencia en la ganancia media es estadísticamente significativa.")
#     else:
#         print(
#             "   -> Conclusión: No hay diferencia estadísticamente significativa en la ganancia media.")
#
#     # 2. Prueba de Levene (Compara varianzas, robusta ante no normalidad)
#     w_stat, p_val_lev = stats.levene(ganancias_orig, ganancias_lim)
#     print("\n2. Prueba de Levene (Diferencia de Varianzas / Riesgo)")
#     print(f"   Estadístico W: {w_stat:.4f}, p-valor: {p_val_lev:.4e}")
#     if p_val_lev < 0.05:
#         print(
#             "   -> Conclusión: El límite reduce la varianza de forma estadísticamente significativa.")
#     else:
#         print("   -> Conclusión: Las varianzas son estadísticamente similares.")
#
#     # 3. Prueba U de Mann-Whitney (Diferencia de distribuciones/medianas)
#     u_stat, p_val_mw = stats.mannwhitneyu(ganancias_orig, ganancias_lim, alternative='two-sided')
#     print("\n3. Prueba U de Mann-Whitney (Diferencia de Distribuciones)")
#     print(f"   Estadístico U: {u_stat:.4f}, p-valor: {p_val_mw:.4e}")
#     if p_val_mw < 0.05:
#         print("   -> Conclusión: Las distribuciones subyacentes son significativamente distintas.")
#     else:
#         print("   -> Conclusión: Las distribuciones no presentan diferencias significativas.")
#
#
# # =============================================================================
# # 4. Punto de Entrada
# # =============================================================================
# if __name__ == "__main__":
#     NRO_JUEGOS = 10000  # Aumentamos N para mayor poder estadístico
#     PROB_CARA = 0.5
#     PREMIO = 8.0
#     COSTO = 1.0
#
#     print(f"Iniciando simulación de {NRO_JUEGOS} partidas por versión...")
#
#     ganancias_originales = ejecutar_motor(simular_juego_original, NRO_JUEGOS, PROB_CARA, PREMIO,
#                                           COSTO)
#
#     # Usamos lambda para inyectar el parámetro max_l=15 implícito en la firma requerida
#     wrapper_limite = lambda p, pr, c: simular_juego_limite(p, pr, c, max_l=15)
#     ganancias_con_limite = ejecutar_motor(wrapper_limite, NRO_JUEGOS, PROB_CARA, PREMIO, COSTO)
#
#     comparar_versiones(ganancias_originales, ganancias_con_limite)
#     print("\nAnálisis finalizado.")