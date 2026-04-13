#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simulación Monte Carlo del juego de la moneda con condición de parada |C-S| == 3."""

# =============================================================================
# 1. IMPORTS Y CONFIGURACIÓN GLOBAL
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from typing import Tuple, Dict, List

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


# =============================================================================
# 2. FUNCIÓN DE SIMULACIÓN DE UN JUEGO INDIVIDUAL
# =============================================================================

def simular_juego(
        prob_cara: float,
        premio: float,
        costo_lanzamiento: float,
        **kwargs
) -> Tuple[int, float]:
    """
    Simula un juego completo de lanzamiento de moneda.

    El juego continúa hasta que la diferencia absoluta entre el número
    de caras y sellos es exactamente 3.

    Args:
        prob_cara: Probabilidad de obtener cara en cada lanzamiento (0-1)
        premio: Premio fijo recibido al finalizar el juego
        costo_lanzamiento: Costo por cada lanzamiento realizado

    Returns:
        Tuple[int, float]: (número de lanzamientos, ganancia neta)

    Example:
        >>> lanzamientos, ganancia = simular_juego(0.5, 8.0, 1.0)
        >>> print(f"Lanzamientos: {lanzamientos}, Ganancia: {ganancia:.2f}")
    """
    caras = 0
    sellos = 0
    lanzamientos = 0
    rng = kwargs.get("generador", None)

    # Continuar hasta que la diferencia absoluta sea 3
    while abs(caras - sellos) != 3:
        # Simular lanzamiento de moneda
        # if np.random.random() < prob_cara:
        if rng.random() < prob_cara:
            caras += 1
        else:
            sellos += 1
        lanzamientos += 1

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
        costo_lanzamiento: float
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Ejecuta múltiples juegos y recolecta los resultados.

    Args:
        nro_juegos: Número de juegos a simular
        prob_cara: Probabilidad de obtener cara
        premio: Premio fijo por juego
        costo_lanzamiento: Costo por lanzamiento

    Returns:
        Tuple[np.ndarray, np.ndarray]: Arrays con (lanzamientos, ganancias)

    Example:
        >>> lanz, gan = ejecutar_simulacion(1000, 0.5, 8.0, 1.0)
        >>> print(f"Media ganancias: {gan.mean():.2f}")
    """
    lanzamientos = np.zeros(nro_juegos, dtype=int)
    ganancias = np.zeros(nro_juegos, dtype=float)

    for i in range(nro_juegos):
        lanzamientos[i], ganancias[i] = simular_juego(
            prob_cara, premio, costo_lanzamiento, generador=rng
        )

    return lanzamientos, ganancias


# =============================================================================
# 4. ANÁLISIS ESTADÍSTICO
# =============================================================================

def analizar_resultados(
        lanzamientos: np.ndarray,
        ganancias: np.ndarray
) -> Dict[str, float]:
    """
    Calcula estadísticas descriptivas de los resultados.

    Args:
        lanzamientos: Array con número de lanzamientos por juego
        ganancias: Array con ganancias por juego

    Returns:
        Dict[str, float]: Diccionario con métricas estadísticas
    """
    estadisticas = {
        # Estadísticas de lanzamientos
        'lanzamientos_media': np.mean(lanzamientos),
        'lanzamientos_std': np.std(lanzamientos),
        'lanzamientos_var': np.var(lanzamientos),
        'lanzamientos_min': np.min(lanzamientos),
        'lanzamientos_max': np.max(lanzamientos),
        'lanzamientos_mediana': np.median(lanzamientos),
        'lanzamientos_perc_25': np.percentile(lanzamientos, 25),
        'lanzamientos_perc_75': np.percentile(lanzamientos, 75),

        # Estadísticas de ganancias
        'ganancia_media': np.mean(ganancias),
        'ganancia_std': np.std(ganancias),
        'ganancia_var': np.var(ganancias),
        'ganancia_min': np.min(ganancias),
        'ganancia_max': np.max(ganancias),
        'ganancia_mediana': np.median(ganancias),
        'ganancia_perc_25': np.percentile(ganancias, 25),
        'ganancia_perc_75': np.percentile(ganancias, 75),

        # Probabilidad de ganancia positiva
        'prob_ganancia_positiva': np.mean(ganancias > 0),

        # Ganancia esperada por juego
        'ganancia_esperada': np.mean(ganancias)
    }

    return estadisticas


# =============================================================================
# 5. VISUALIZACIÓN CON MATPLOTLIB (ESTÁTICA)
# =============================================================================

def visualizar_matplotlib(
        lanzamientos: np.ndarray,
        ganancias: np.ndarray
) -> None:
    """
    Crea visualizaciones estáticas con Matplotlib.

    Args:
        lanzamientos: Array con número de lanzamientos
        ganancias: Array con ganancias
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Simulación Monte Carlo - Juego de la Moneda (Matplotlib)',
                 fontsize=16, fontweight='bold')

    # PDF de lanzamientos
    axes[0, 0].hist(lanzamientos, bins=30, density=True, alpha=0.7,
                    color='skyblue', edgecolor='black')
    axes[0, 0].set_xlabel('Número de Lanzamientos')
    axes[0, 0].set_ylabel('Densidad de Probabilidad')
    axes[0, 0].set_title('PDF - Distribución de Lanzamientos')
    axes[0, 0].grid(True, alpha=0.3)

    # CDF de lanzamientos
    axes[0, 1].hist(lanzamientos, bins=30, density=True, cumulative=True,
                    alpha=0.7, color='lightcoral', edgecolor='black')
    axes[0, 1].set_xlabel('Número de Lanzamientos')
    axes[0, 1].set_ylabel('Probabilidad Acumulada')
    axes[0, 1].set_title('CDF - Distribución de Lanzamientos')
    axes[0, 1].grid(True, alpha=0.3)

    # PDF de ganancias
    axes[1, 0].hist(ganancias, bins=30, density=True, alpha=0.7,
                    color='lightgreen', edgecolor='black')
    axes[1, 0].set_xlabel('Ganancia Neta ($)')
    axes[1, 0].set_ylabel('Densidad de Probabilidad')
    axes[1, 0].set_title('PDF - Distribución de Ganancias')
    axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2,
                       label='Punto de equilibrio')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # CDF de ganancias
    axes[1, 1].hist(ganancias, bins=30, density=True, cumulative=True,
                    alpha=0.7, color='gold', edgecolor='black')
    axes[1, 1].set_xlabel('Ganancia Neta ($)')
    axes[1, 1].set_ylabel('Probabilidad Acumulada')
    axes[1, 1].set_title('CDF - Distribución de Ganancias')
    axes[1, 1].axvline(x=0, color='red', linestyle='--', linewidth=2)
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('simulacion_matplotlib.png', dpi=300, bbox_inches='tight')
    plt.show()


# =============================================================================
# 6. VISUALIZACIÓN CON SEABORN (ESTÉTICA SOBRE MATPLOTLIB)
# =============================================================================

def visualizar_seaborn(
        lanzamientos: np.ndarray,
        ganancias: np.ndarray
) -> None:
    """
    Crea visualizaciones mejoradas con Seaborn.

    Args:
        lanzamientos: Array con número de lanzamientos
        ganancias: Array con ganancias
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Simulación Monte Carlo - Juego de la Moneda (Seaborn)',
                 fontsize=16, fontweight='bold')

    # PDF de lanzamientos
    sns.histplot(lanzamientos, kde=True, stat='density', bins=30,
                 ax=axes[0, 0], color='#2E86AB', alpha=0.6)
    axes[0, 0].set_xlabel('Número de Lanzamientos')
    axes[0, 0].set_ylabel('Densidad de Probabilidad')
    axes[0, 0].set_title('PDF - Distribución de Lanzamientos')

    # CDF de lanzamientos
    sns.ecdfplot(lanzamientos, ax=axes[0, 1], color='#A23B72', linewidth=2)
    axes[0, 1].set_xlabel('Número de Lanzamientos')
    axes[0, 1].set_ylabel('Probabilidad Acumulada')
    axes[0, 1].set_title('CDF - Distribución de Lanzamientos')

    # PDF de ganancias
    sns.histplot(ganancias, kde=True, stat='density', bins=30,
                 ax=axes[1, 0], color='#F18F01', alpha=0.6)
    axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2,
                       label='Punto de equilibrio')
    axes[1, 0].set_xlabel('Ganancia Neta ($)')
    axes[1, 0].set_ylabel('Densidad de Probabilidad')
    axes[1, 0].set_title('PDF - Distribución de Ganancias')
    axes[1, 0].legend()

    # CDF de ganancias
    sns.ecdfplot(ganancias, ax=axes[1, 1], color='#C73E1D', linewidth=2)
    axes[1, 1].axvline(x=0, color='blue', linestyle='--', linewidth=2,
                       label='Punto de equilibrio')
    axes[1, 1].set_xlabel('Ganancia Neta ($)')
    axes[1, 1].set_ylabel('Probabilidad Acumulada')
    axes[1, 1].set_title('CDF - Distribución de Ganancias')
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig('simulacion_seaborn.png', dpi=300, bbox_inches='tight')
    plt.show()


# =============================================================================
# 7. VISUALIZACIÓN CON PLOTLY (INTERACTIVA)
# =============================================================================

def visualizar_plotly(
        lanzamientos: np.ndarray,
        ganancias: np.ndarray
) -> None:
    """
    Crea visualizaciones interactivas con Plotly.

    Args:
        lanzamientos: Array con número de lanzamientos
        ganancias: Array con ganancias
    """
    # Crear subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('PDF - Distribución de Lanzamientos',
                        'CDF - Distribución de Lanzamientos',
                        'PDF - Distribución de Ganancias',
                        'CDF - Distribución de Ganancias'),
        vertical_spacing=0.12,
        horizontal_spacing=0.15
    )

    # PDF de lanzamientos (histograma normalizado)
    hist_lanz, bins_lanz = np.histogram(lanzamientos, bins=30, density=True)
    fig.add_trace(
        go.Bar(x=bins_lanz[:-1], y=hist_lanz, width=np.diff(bins_lanz),
               name='PDF Lanzamientos', marker_color='#2E86AB',
               hovertemplate='Lanzamientos: %{x}<br>Densidad: %{y:.4f}<extra></extra>'),
        row=1, col=1
    )

    # CDF de lanzamientos
    x_lanz = np.sort(lanzamientos)
    y_lanz = np.arange(1, len(x_lanz) + 1) / len(x_lanz)
    fig.add_trace(
        go.Scatter(x=x_lanz, y=y_lanz, mode='lines',
                   name='CDF Lanzamientos', line=dict(color='#A23B72', width=3),
                   hovertemplate='Lanzamientos: %{x}<br>Probabilidad: %{y:.3f}<extra></extra>'),
        row=1, col=2
    )

    # PDF de ganancias
    hist_gan, bins_gan = np.histogram(ganancias, bins=30, density=True)
    fig.add_trace(
        go.Bar(x=bins_gan[:-1], y=hist_gan, width=np.diff(bins_gan),
               name='PDF Ganancias', marker_color='#F18F01',
               hovertemplate='Ganancia: $%{x:.2f}<br>Densidad: %{y:.4f}<extra></extra>'),
        row=2, col=1
    )

    # Línea de equilibrio en PDF de ganancias
    fig.add_vline(x=0, line_dash="dash", line_color="red",
                  annotation_text="Equilibrio", row=2, col=1)

    # CDF de ganancias
    x_gan = np.sort(ganancias)
    y_gan = np.arange(1, len(x_gan) + 1) / len(x_gan)
    fig.add_trace(
        go.Scatter(x=x_gan, y=y_gan, mode='lines',
                   name='CDF Ganancias', line=dict(color='#C73E1D', width=3),
                   hovertemplate='Ganancia: $%{x:.2f}<br>Probabilidad: %{y:.3f}<extra></extra>'),
        row=2, col=2
    )

    # Línea de equilibrio en CDF de ganancias
    fig.add_vline(x=0, line_dash="dash", line_color="blue", row=2, col=2)

    # Actualizar layout
    fig.update_layout(
        title_text='Simulación Monte Carlo - Juego de la Moneda (Plotly Interactivo)',
        title_font_size=20,
        showlegend=False,
        height=800,
        hovermode='x unified'
    )

    # Actualizar ejes
    fig.update_xaxes(title_text="Número de Lanzamientos", row=1, col=1)
    fig.update_xaxes(title_text="Número de Lanzamientos", row=1, col=2)
    fig.update_xaxes(title_text="Ganancia Neta ($)", row=2, col=1)
    fig.update_xaxes(title_text="Ganancia Neta ($)", row=2, col=2)

    fig.update_yaxes(title_text="Densidad", row=1, col=1)
    fig.update_yaxes(title_text="Probabilidad Acumulada", row=1, col=2)
    fig.update_yaxes(title_text="Densidad", row=2, col=1)
    fig.update_yaxes(title_text="Probabilidad Acumulada", row=2, col=2)

    # Guardar y mostrar
    fig.write_html("simulacion_plotly.html")
    fig.show()


# =============================================================================
# 8. FUNCIÓN PRINCIPAL Y PUNTO DE ENTRADA
# =============================================================================

def imprimir_estadisticas(estadisticas: Dict[str, float]) -> None:
    """
    Imprime las estadísticas formateadas en consola.

    Args:
        estadisticas: Diccionario con métricas estadísticas
    """
    print("=" * 60)
    print("RESULTADOS DE LA SIMULACIÓN MONTE CARLO")
    print("=" * 60)

    print("\n📊 ESTADÍSTICAS DE LANZAMIENTOS:")
    print(f"   • Media: {estadisticas['lanzamientos_media']:.2f}")
    print(f"   • Desviación estándar: {estadisticas['lanzamientos_std']:.2f}")
    print(f"   • Varianza: {estadisticas['lanzamientos_var']:.2f}")
    print(f"   • Mínimo: {estadisticas['lanzamientos_min']}")
    print(f"   • Máximo: {estadisticas['lanzamientos_max']}")
    print(f"   • Mediana: {estadisticas['lanzamientos_mediana']:.2f}")
    print(f"   • Percentil 25: {estadisticas['lanzamientos_perc_25']:.2f}")
    print(f"   • Percentil 75: {estadisticas['lanzamientos_perc_75']:.2f}")

    print("\n💰 ESTADÍSTICAS DE GANANCIAS ($):")
    print(f"   • Media: ${estadisticas['ganancia_media']:.2f}")
    print(f"   • Desviación estándar: ${estadisticas['ganancia_std']:.2f}")
    print(f"   • Varianza: ${estadisticas['ganancia_var']:.2f}")
    print(f"   • Mínimo: ${estadisticas['ganancia_min']:.2f}")
    print(f"   • Máximo: ${estadisticas['ganancia_max']:.2f}")
    print(f"   • Mediana: ${estadisticas['ganancia_mediana']:.2f}")
    print(f"   • Percentil 25: ${estadisticas['ganancia_perc_25']:.2f}")
    print(f"   • Percentil 75: ${estadisticas['ganancia_perc_75']:.2f}")

    print("\n🎲 PROBABILIDADES:")
    print(
        f"   • Probabilidad de ganancia positiva: {estadisticas['prob_ganancia_positiva'] * 100:.1f}%")
    print(f"   • Ganancia esperada por juego: ${estadisticas['ganancia_esperada']:.2f}")

    print("\n" + "=" * 60)


def main() -> None:
    """
    Función principal que coordina la simulación completa.
    """
    print("Iniciando simulación Monte Carlo...")
    print(f"Parámetros: {NRO_JUEGOS} juegos, P(cara)={PROB_CARA}, "
          f"premio=${PREMIO}, costo=${COSTO_LANZAMIENTO}/lanzamiento\n")

    # Ejecutar simulación
    lanzamientos, ganancias = ejecutar_simulacion(
        NRO_JUEGOS, PROB_CARA, PREMIO, COSTO_LANZAMIENTO
    )

    # Análisis estadístico
    estadisticas = analizar_resultados(lanzamientos, ganancias)
    imprimir_estadisticas(estadisticas)

    # Visualizaciones
    print("\nGenerando visualizaciones...")

    print("  • Matplotlib (estática)...")
    visualizar_matplotlib(lanzamientos, ganancias)

    print("  • Seaborn (estética)...")
    visualizar_seaborn(lanzamientos, ganancias)

    print("  • Plotly (interactiva)...")
    visualizar_plotly(lanzamientos, ganancias)

    print("\n✅ Simulación completada exitosamente.")
    print("   Archivos generados:")
    print("   - simulacion_matplotlib.png")
    print("   - simulacion_seaborn.png")
    print("   - simulacion_plotly.html")





if __name__ == "__main__":
    main()