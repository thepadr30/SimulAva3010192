"""
Simulación Monte Carlo: Juego de la Moneda.
Este módulo simula un juego de apuestas basado en lanzamientos de una moneda,
calcula estadísticas descriptivas sobre los resultados y genera visualizaciones
en Matplotlib, Seaborn y Plotly.
"""

# =============================================================================
# 1. Imports y configuración global
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


# =============================================================================
# 2. Lógica de Simulación Individual
# =============================================================================
def simular_juego(
        prob_cara: float,
        premio: float,
        costo_lanzamiento: float,
        **kwargs
) -> Tuple[int, float]:
    """
    Simula una única partida del juego de la moneda.

    El juego termina cuando el valor absoluto de la diferencia entre caras
    y sellos es exactamente 3.

    Args:
        prob_cara (float): Probabilidad de obtener cara (0.0 a 1.0).
        premio (float): Valor fijo recibido al finalizar la partida.
        costo_lanzamiento (float): Costo a descontar por cada lanzamiento.

    Returns:
        Tuple[int, float]: Una tupla que contiene:
            - Cantidad de lanzamientos realizados (int).
            - Ganancia neta obtenida en la partida (float).
    """
    diferencia = 0
    lanzamientos = 0
    rng = kwargs.get("generador", None)

    # Condición de fin: la diferencia absoluta entre caras y sellos llega a 3
    while abs(diferencia) < 3:
        lanzamientos += 1
        # np.random.random() genera un float en [0.0, 1.0)
        # if np.random.random() < prob_cara:
        if rng.random() < prob_cara:
            diferencia += 1  # Cara
        else:
            diferencia -= 1  # Sello

    ganancia_neta = premio - (costo_lanzamiento * lanzamientos)

    return lanzamientos, ganancia_neta


def simular_juego_con_limite(
        prob_cara: float,
        premio: float,
        costo_lanzamiento: float,
        max_lanzamientos: int = 15,
        **kwargs
) -> Tuple[int, float]:
    """
    Simula una partida del juego de la moneda con un límite máximo de tiros.

    El juego termina bajo una de dos condiciones (lo que ocurra primero):
    1. El valor absoluto de la diferencia entre caras y sellos es exactamente 3.
    2. El número total de lanzamientos alcanza `max_lanzamientos`.

    Args:
        prob_cara (float): Probabilidad de obtener cara (0.0 a 1.0).
        premio (float): Valor fijo recibido al finalizar la partida.
        costo_lanzamiento (float): Costo a descontar por cada lanzamiento.
        max_lanzamientos (int, opcional): Límite de tiros permitidos. Por defecto 15.

    Returns:
        Tuple[int, float]: Una tupla que contiene:
            - Cantidad de lanzamientos realizados (int).
            - Ganancia neta obtenida en la partida (float).
    """
    diferencia = 0
    lanzamientos = 0
    rng = kwargs.get("generador", None)

    # Condición de fin combinada: diferencia menor a 3 Y no haber llegado al límite
    while abs(diferencia) < 3 and lanzamientos < max_lanzamientos:
        lanzamientos += 1

        # np.random.random() genera un float en [0.0, 1.0)
        # if np.random.random() < prob_cara:
        if rng.random() < prob_cara:
            diferencia += 1  # Cara
        else:
            diferencia -= 1  # Sello

    # El cálculo de la ganancia se mantiene igual sin importar por qué terminó el bucle
    ganancia_neta = premio - (costo_lanzamiento * lanzamientos)

    return lanzamientos, ganancia_neta

# =============================================================================
# 3. Lógica de Ejecución Masiva
# =============================================================================
def ejecutar_simulacion(
        nro_juegos: int,
        prob_cara: float,
        premio: float,
        costo_lanzamiento: float
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Ejecuta múltiples partidas de la simulación mediante Monte Carlo.

    Args:
        nro_juegos (int): Número de partidas a simular.
        prob_cara (float): Probabilidad de obtener cara.
        premio (float): Premio fijo por finalizar el juego.
        costo_lanzamiento (float): Costo por cada lanzamiento.

    Returns:
        Tuple[np.ndarray, np.ndarray]:
            - Array con el número de lanzamientos por juego.
            - Array con la ganancia neta por juego.
    """
    lanzamientos_arr = np.zeros(nro_juegos, dtype=int)
    ganancias_arr = np.zeros(nro_juegos, dtype=float)

    for i in range(nro_juegos):
        lanzamientos, ganancia = simular_juego(prob_cara, premio, costo_lanzamiento, generador=rng)
        lanzamientos_arr[i] = lanzamientos
        ganancias_arr[i] = ganancia

    return lanzamientos_arr, ganancias_arr


# =============================================================================
# 4. Bloque de Análisis Estadístico
# =============================================================================
def calcular_estadisticas(ganancias: np.ndarray) -> Dict[str, float]:
    """
    Calcula las estadísticas descriptivas de las ganancias obtenidas.

    Args:
        ganancias (np.ndarray): Arreglo numérico con las ganancias netas.

    Returns:
        Dict[str, float]: Diccionario con media, varianza, desviación estándar,
        ganancia esperada y percentiles (25, 50, 75).
    """
    stats = {
        "media": np.mean(ganancias),
        "varianza": np.var(ganancias, ddof=1),
        "std_dev": np.std(ganancias, ddof=1),
        "percentil_25": np.percentile(ganancias, 25),
        "mediana_50": np.median(ganancias),
        "percentil_75": np.percentile(ganancias, 75),
        "ganancia_esperada": np.mean(ganancias)  # Numéricamente igual a la media empírica
    }
    return stats


# =============================================================================
# 5. Bloque de Visualización: Matplotlib (Estático)
# =============================================================================
def graficar_matplotlib(ganancias: np.ndarray) -> None:
    """
    Genera gráficos estáticos (PDF y CDF) de las ganancias usando Matplotlib.

    Args:
        ganancias (np.ndarray): Datos de ganancias netas.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Distribución de Ganancias Netas - Matplotlib', fontsize=14)

    # PDF: Histograma normalizado
    axes[0].hist(ganancias, bins=20, density=True, color='skyblue', edgecolor='black')
    axes[0].set_title('PDF (Función de Densidad de Probabilidad)')
    axes[0].set_xlabel('Ganancia Neta ($)')
    axes[0].set_ylabel('Densidad')

    # CDF: Función de Distribución Acumulada Empírica
    x_sort = np.sort(ganancias)
    y_cdf = np.arange(1, len(x_sort) + 1) / len(x_sort)
    axes[1].plot(x_sort, y_cdf, marker='.', linestyle='none', color='navy')
    axes[1].set_title('CDF Empírica')
    axes[1].set_xlabel('Ganancia Neta ($)')
    axes[1].set_ylabel('Probabilidad Acumulada')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# =============================================================================
# 6. Bloque de Visualización: Seaborn (Estético)
# =============================================================================
def graficar_seaborn(ganancias: np.ndarray) -> None:
    """
    Genera gráficos estéticos (PDF y CDF) de las ganancias usando Seaborn.

    Args:
        ganancias (np.ndarray): Datos de ganancias netas.
    """
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Distribución de Ganancias Netas - Seaborn', fontsize=14)

    # PDF
    sns.histplot(ganancias, bins=20, stat="density", kde=True, ax=axes[0], color="teal")
    axes[0].set_title('PDF con Estimación de Densidad Kernel')
    axes[0].set_xlabel('Ganancia Neta ($)')
    axes[0].set_ylabel('Densidad')

    # CDF
    sns.ecdfplot(data=ganancias, ax=axes[1], color="darkred")
    axes[1].set_title('CDF Empírica')
    axes[1].set_xlabel('Ganancia Neta ($)')
    axes[1].set_ylabel('Probabilidad Acumulada')

    plt.tight_layout()
    plt.show()


# =============================================================================
# 7. Bloque de Visualización: Plotly (Interactivo)
# =============================================================================
def graficar_plotly(ganancias: np.ndarray) -> None:
    """
    Genera un panel interactivo (PDF y CDF) de las ganancias usando Plotly.

    Args:
        ganancias (np.ndarray): Datos de ganancias netas.
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("PDF (Histograma)", "CDF Empírica")
    )

    # PDF
    fig.add_trace(
        go.Histogram(
            x=ganancias,
            histnorm='probability density',
            name='Densidad',
            marker_color='mediumpurple',
            opacity=0.75
        ),
        row=1, col=1
    )

    # CDF
    x_sort = np.sort(ganancias)
    y_cdf = np.arange(1, len(x_sort) + 1) / len(x_sort)
    fig.add_trace(
        go.Scatter(
            x=x_sort,
            y=y_cdf,
            mode='lines',
            name='CDF',
            line=dict(color='firebrick', width=2)
        ),
        row=1, col=2
    )

    fig.update_layout(
        title_text="Distribución de Ganancias Netas - Plotly (Interactivo)",
        xaxis_title="Ganancia Neta ($)",
        yaxis_title="Densidad",
        xaxis2_title="Ganancia Neta ($)",
        yaxis2_title="Probabilidad Acumulada",
        showlegend=False,
        template='plotly_white'
    )

    fig.show()


# =============================================================================
# 8. Punto de Entrada (Main)
# =============================================================================
if __name__ == "__main__":
    # Parámetros fijos
    NRO_JUEGOS = 1000
    PROB_CARA = 0.5
    PREMIO = 8.0
    COSTO_LANZAMIENTO = 1.0

    print("--- Iniciando Simulación Monte Carlo ---")

    # 1. Ejecutar simulación
    arr_lanzamientos, arr_ganancias = ejecutar_simulacion(
        NRO_JUEGOS, PROB_CARA, PREMIO, COSTO_LANZAMIENTO
    )

    # 2. Calcular y mostrar resultados estadísticos
    estadisticas = calcular_estadisticas(arr_ganancias)

    print(f"\nResultados tras {NRO_JUEGOS} juegos simulados:")
    print("-" * 45)
    print(f"Ganancia Esperada (Media) : ${estadisticas['ganancia_esperada']:.4f}")
    print(f"Desviación Estándar       : ${estadisticas['std_dev']:.4f}")
    print(f"Varianza                  : ${estadisticas['varianza']:.4f}")
    print(f"Percentil 25 (Q1)         : ${estadisticas['percentil_25']:.4f}")
    print(f"Mediana (Q2)              : ${estadisticas['mediana_50']:.4f}")
    print(f"Percentil 75 (Q3)         : ${estadisticas['percentil_75']:.4f}")
    print("-" * 45)

    # 3. Generar visualizaciones (las ventanas de Matplotlib/Seaborn bloquearán
    #    la ejecución hasta ser cerradas; Plotly se abrirá en el navegador).
    print("\nGenerando gráficos con Matplotlib...")
    graficar_matplotlib(arr_ganancias)

    print("Generando gráficos con Seaborn...")
    graficar_seaborn(arr_ganancias)

    print("Generando gráficos interactivos con Plotly...")
    graficar_plotly(arr_ganancias)

    print("\n--- Simulación Finalizada ---")