#%%
"""
Simulación Monte Carlo: Juego de Moneda
========================================
Simula un juego donde se lanza una moneda hasta que la diferencia absoluta
entre caras y sellos alcanza 3. Genera análisis estadístico y tres tipos de
visualización: Matplotlib (estático), Seaborn (estético) y Plotly (interactivo).
"""

# =============================================================================
# 1. IMPORTS Y CONFIGURACIÓN GLOBAL
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from typing import Tuple

# Semilla aleatoria para reproducibilidad total
SEMILLA = 42
np.random.seed(SEMILLA)
rng = np.random.default_rng(seed=SEMILLA)

# Parámetros globales del juego
NRO_JUEGOS: int = 1000
PROB_CARA: float = 0.5
PREMIO: float = 8.0
COSTO_LANZAMIENTO: float = 1.0

# Condición de parada: diferencia absoluta entre caras y sellos
DIFERENCIA_LIMITE: int = 3

#%%
# =============================================================================
# 2. FUNCIÓN: SIMULAR UN ÚNICO JUEGO (versión original — sin límite)
# =============================================================================

def simular_juego(
    prob_cara: float,
    premio: float,
    costo_lanzamiento: float,
    rng: np.random.Generator
) -> Tuple[int, float]:
    """Simula una única partida del juego de moneda (condición original).

    Lanza una moneda repetidamente acumulando caras y sellos hasta que
    la diferencia absoluta entre ambos contadores alcanza exactamente 3.
    Calcula la ganancia neta como ``premio - costo_lanzamiento * n_lanzamientos``.

    Args:
        prob_cara: Probabilidad de obtener cara en cada lanzamiento [0, 1].
        premio: Monto fijo en dólares que recibe el jugador al ganar.
        costo_lanzamiento: Costo en dólares por cada lanzamiento realizado.
        rng: generadores números aleatoreos

    Returns:
        Tuple con dos elementos:
            - n_lanzamientos (int): Número total de lanzamientos en la partida.
            - ganancia_neta (float): Ganancia neta en dólares (puede ser negativa).

    Example:
        >>> n, g = simular_juego(prob_cara=0.5, premio=8.0, costo_lanzamiento=1.0)
        >>> isinstance(n, int) and n >= 3  # Mínimo 3 lanzamientos posibles
        True
    """
    total_caras: int = 0
    total_sellos: int = 0

    # Lanzar moneda hasta alcanzar la diferencia límite
    while abs(total_caras - total_sellos) < DIFERENCIA_LIMITE:
        # Resultado: True = cara, False = sello
        # es_cara: bool = np.random.random() < prob_cara
        es_cara: bool = rng.random() < prob_cara
        if es_cara:
            total_caras += 1
        else:
            total_sellos += 1

    n_lanzamientos: int = total_caras + total_sellos
    ganancia_neta: float = premio - (costo_lanzamiento * n_lanzamientos)

    return n_lanzamientos, ganancia_neta


# =============================================================================
# 2b. FUNCIÓN: SIMULAR UN ÚNICO JUEGO CON DOBLE CONDICIÓN DE PARADA
# =============================================================================

# Límite máximo de lanzamientos permitidos por partida (nueva regla)
LIMITE_LANZAMIENTOS: int = 15


def simular_juego_v2(
    prob_cara: float,
    premio: float,
    costo_lanzamiento: float,
    diferencia_limite: int = DIFERENCIA_LIMITE,
    limite_lanzamientos: int = LIMITE_LANZAMIENTOS,
    **kwargs
) -> Tuple[int, float, bool]:
    """Simula una partida con doble condición de parada.

    El juego termina cuando se cumple **cualquiera** de estas dos condiciones
    (la que ocurra primero):

    * ``|total_caras - total_sellos| == diferencia_limite``  → victoria normal.
    * ``n_lanzamientos == limite_lanzamientos``              → corte por límite.

    El premio se otorga **únicamente** si el juego terminó por diferencia.
    Si se alcanzó el límite de lanzamientos sin llegar a la diferencia objetivo,
    el jugador **no recibe el premio** y solo asume el costo acumulado.

    Args:
        prob_cara: Probabilidad de obtener cara en cada lanzamiento [0, 1].
        premio: Monto fijo en dólares que recibe el jugador al ganar.
        costo_lanzamiento: Costo en dólares por cada lanzamiento realizado.
        diferencia_limite: Diferencia absoluta |caras - sellos| que termina el
            juego con victoria. Por defecto ``DIFERENCIA_LIMITE`` (3).
        limite_lanzamientos: Número máximo de lanzamientos permitidos antes de
            forzar el fin del juego. Por defecto ``LIMITE_LANZAMIENTOS`` (15).

    Returns:
        Tuple con tres elementos:
            - n_lanzamientos (int): Total de lanzamientos realizados en la partida.
            - ganancia_neta (float): Ganancia neta en dólares; negativa si el costo
              supera el premio, o si no hubo victoria (premio = $0).
            - termino_por_diferencia (bool): ``True`` si el juego terminó por
              alcanzar la diferencia límite (victoria); ``False`` si terminó por
              agotar el límite de lanzamientos (derrota por tiempo).

    Raises:
        ValueError: Si ``diferencia_limite`` o ``limite_lanzamientos`` son <= 0,
            o si ``diferencia_limite`` > ``limite_lanzamientos`` (condición de
            victoria inalcanzable matemáticamente).

    Example:
        >>> n, g, victoria = simular_juego_v2(0.5, 8.0, 1.0)
        >>> 3 <= n <= 15       # Rango válido de lanzamientos con parámetros por defecto
        True
        >>> isinstance(victoria, bool)
        True
    """
    rng = kwargs.get("generador", None)

    if diferencia_limite <= 0:
        raise ValueError(
            f"diferencia_limite debe ser > 0, se recibió: {diferencia_limite}"
        )
    if limite_lanzamientos <= 0:
        raise ValueError(
            f"limite_lanzamientos debe ser > 0, se recibió: {limite_lanzamientos}"
        )
    if diferencia_limite > limite_lanzamientos:
        raise ValueError(
            f"diferencia_limite ({diferencia_limite}) no puede superar "
            f"limite_lanzamientos ({limite_lanzamientos}): la condición de "
            "victoria sería inalcanzable matemáticamente."
        )

    total_caras: int = 0
    total_sellos: int = 0
    n_lanzamientos: int = 0

    # Bucle con doble condición de salida evaluada antes de cada lanzamiento:
    #   - Condición 1: diferencia absoluta aún no alcanza el límite de victoria.
    #   - Condición 2: no se ha agotado el cupo máximo de lanzamientos.
    # El bucle se interrumpe en cuanto CUALQUIERA de las dos condiciones falla.
    while (
        abs(total_caras - total_sellos) < diferencia_limite
        and n_lanzamientos < limite_lanzamientos
    ):
        # es_cara: bool = np.random.random() < prob_cara
        es_cara: bool = rng.random() < prob_cara
        if es_cara:
            total_caras += 1
        else:
            total_sellos += 1
        # El contador se incrementa DESPUÉS del lanzamiento para reflejar
        # exactamente cuántas tiradas se consumieron en esta iteración.
        n_lanzamientos += 1

    # Determinar cuál de las dos condiciones detuvo el juego
    termino_por_diferencia: bool = (
        abs(total_caras - total_sellos) >= diferencia_limite
    )

    # Premio condicional: solo se paga si hubo victoria real (por diferencia)
    premio_obtenido: float = premio if termino_por_diferencia else 0.0
    ganancia_neta: float = premio_obtenido - (costo_lanzamiento * n_lanzamientos)

    return n_lanzamientos, ganancia_neta, termino_por_diferencia


# =============================================================================
# 2c. FUNCIÓN: EJECUTAR SIMULACIÓN COMPLETA CON DOBLE CONDICIÓN DE PARADA
# =============================================================================

def ejecutar_simulacion_v2(
    nro_juegos: int,
    prob_cara: float,
    premio: float,
    costo_lanzamiento: float,
    diferencia_limite: int = DIFERENCIA_LIMITE,
    limite_lanzamientos: int = LIMITE_LANZAMIENTOS,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Ejecuta múltiples partidas con doble condición de parada.

    Llama iterativamente a ``simular_juego_v2`` y almacena los resultados en
    arrays de NumPy. Adicionalmente registra si cada partida terminó por
    diferencia o por límite de lanzamientos, habilitando análisis comparativo
    entre ambas modalidades de fin de juego.

    Args:
        nro_juegos: Número total de partidas a simular.
        prob_cara: Probabilidad de obtener cara en cada lanzamiento [0, 1].
        premio: Monto fijo en dólares que recibe el jugador al ganar.
        costo_lanzamiento: Costo en dólares por cada lanzamiento realizado.
        diferencia_limite: Diferencia absoluta que activa la condición de
            victoria. Por defecto 3.
        limite_lanzamientos: Tope máximo de lanzamientos por partida.
            Por defecto 15.

    Returns:
        Tuple con tres arrays de NumPy de longitud ``nro_juegos``:
            - lanzamientos (np.ndarray[int]): Lanzamientos realizados por partida.
            - ganancias (np.ndarray[float]): Ganancia neta por partida (USD).
            - victorias (np.ndarray[bool]): ``True`` si la partida terminó por
              diferencia (victoria); ``False`` si terminó por límite (derrota).

    Raises:
        ValueError: Si ``nro_juegos`` es menor o igual a cero.

    Example:
        >>> lanz, gan, vic = ejecutar_simulacion_v2(500, 0.5, 8.0, 1.0)
        >>> len(lanz) == len(gan) == len(vic) == 500
        True
        >>> vic.dtype == bool
        True
    """
    if nro_juegos <= 0:
        raise ValueError(f"nro_juegos debe ser positivo, se recibió: {nro_juegos}")

    # Pre-alocar arrays para máxima eficiencia (evita re-asignación dinámica)
    lanzamientos = np.empty(nro_juegos, dtype=int)
    ganancias = np.empty(nro_juegos, dtype=float)
    victorias = np.empty(nro_juegos, dtype=bool)

    for i in range(nro_juegos):
        n, g, v = simular_juego_v2(
            prob_cara, premio, costo_lanzamiento,
            diferencia_limite, limite_lanzamientos,
            generador=rng
        )
        lanzamientos[i] = n
        ganancias[i] = g
        victorias[i] = v

    return lanzamientos, ganancias, victorias


# =============================================================================
# 3. FUNCIÓN: EJECUTAR LA SIMULACIÓN COMPLETA
# =============================================================================

def ejecutar_simulacion(
    nro_juegos: int,
    prob_cara: float,
    premio: float,
    costo_lanzamiento: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """Ejecuta múltiples partidas del juego de moneda y recopila resultados.

    Llama iterativamente a ``simular_juego`` para cada partida y almacena
    los resultados en arrays de NumPy para análisis estadístico eficiente.

    Args:
        nro_juegos: Número total de partidas a simular.
        prob_cara: Probabilidad de obtener cara en cada lanzamiento [0, 1].
        premio: Monto fijo en dólares que recibe el jugador al ganar.
        costo_lanzamiento: Costo en dólares por cada lanzamiento realizado.

    Returns:
        Tuple con dos arrays de NumPy de longitud ``nro_juegos``:
            - lanzamientos (np.ndarray[int]): Nro. de lanzamientos por partida.
            - ganancias (np.ndarray[float]): Ganancia neta por partida en dólares.

    Raises:
        ValueError: Si ``nro_juegos`` es menor o igual a cero.

    Example:
        >>> lanz, gan = ejecutar_simulacion(100, 0.5, 8.0, 1.0)
        >>> len(lanz) == len(gan) == 100
        True
    """
    if nro_juegos <= 0:
        raise ValueError(f"nro_juegos debe ser positivo, se recibió: {nro_juegos}")

    lanzamientos = np.empty(nro_juegos, dtype=int)
    ganancias = np.empty(nro_juegos, dtype=float)

    for i in range(nro_juegos):
        n, g = simular_juego(prob_cara, premio, costo_lanzamiento, rng=rng)
        lanzamientos[i] = n
        ganancias[i] = g

    return lanzamientos, ganancias


# =============================================================================
# 4. BLOQUE DE ANÁLISIS ESTADÍSTICO
# =============================================================================

def calcular_estadisticas(
    lanzamientos: np.ndarray,
    ganancias: np.ndarray,
) -> dict:
    """Calcula estadísticas descriptivas completas sobre los resultados.

    Args:
        lanzamientos: Array con el número de lanzamientos por partida.
        ganancias: Array con las ganancias netas por partida.

    Returns:
        Diccionario con métricas estadísticas clave para ambos arrays.
    """
    estadisticas = {
        # --- Estadísticas de lanzamientos ---
        "lanz_media": np.mean(lanzamientos),
        "lanz_mediana": np.median(lanzamientos),
        "lanz_varianza": np.var(lanzamientos, ddof=1),
        "lanz_desv_std": np.std(lanzamientos, ddof=1),
        "lanz_min": np.min(lanzamientos),
        "lanz_max": np.max(lanzamientos),
        "lanz_p25": np.percentile(lanzamientos, 25),
        "lanz_p75": np.percentile(lanzamientos, 75),
        "lanz_p95": np.percentile(lanzamientos, 95),

        # --- Estadísticas de ganancias ---
        "gan_media": np.mean(ganancias),
        "gan_mediana": np.median(ganancias),
        "gan_varianza": np.var(ganancias, ddof=1),
        "gan_desv_std": np.std(ganancias, ddof=1),
        "gan_min": np.min(ganancias),
        "gan_max": np.max(ganancias),
        "gan_p25": np.percentile(ganancias, 25),
        "gan_p75": np.percentile(ganancias, 75),
        "gan_p5": np.percentile(ganancias, 5),

        # Probabilidad empírica de ganancia positiva
        "prob_ganancia_positiva": np.mean(ganancias > 0),

        # Ganancia esperada teórica (E[G] = premio - costo * E[N])
        "ganancia_esperada_empirica": np.mean(ganancias),
    }
    return estadisticas


def imprimir_estadisticas(estadisticas: dict, nro_juegos: int) -> None:
    """Imprime el resumen estadístico formateado en consola.

    Args:
        estadisticas: Diccionario generado por ``calcular_estadisticas``.
        nro_juegos: Número total de juegos simulados (para contexto).
    """
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  RESULTADOS DE SIMULACIÓN MONTE CARLO ({nro_juegos:,} juegos)")
    print(sep)

    print("\n📊 LANZAMIENTOS POR PARTIDA:")
    print(f"   Media          : {estadisticas['lanz_media']:.4f}")
    print(f"   Mediana        : {estadisticas['lanz_mediana']:.1f}")
    print(f"   Desv. Estándar : {estadisticas['lanz_desv_std']:.4f}")
    print(f"   Varianza       : {estadisticas['lanz_varianza']:.4f}")
    print(f"   Mínimo         : {estadisticas['lanz_min']}")
    print(f"   Máximo         : {estadisticas['lanz_max']}")
    print(f"   Percentil 25   : {estadisticas['lanz_p25']:.1f}")
    print(f"   Percentil 75   : {estadisticas['lanz_p75']:.1f}")
    print(f"   Percentil 95   : {estadisticas['lanz_p95']:.1f}")

    print("\n💰 GANANCIAS NETAS (USD):")
    print(f"   Media (E[G])   : ${estadisticas['gan_media']:.4f}")
    print(f"   Mediana        : ${estadisticas['gan_mediana']:.2f}")
    print(f"   Desv. Estándar : ${estadisticas['gan_desv_std']:.4f}")
    print(f"   Varianza       : ${estadisticas['gan_varianza']:.4f}")
    print(f"   Mínimo         : ${estadisticas['gan_min']:.2f}")
    print(f"   Máximo         : ${estadisticas['gan_max']:.2f}")
    print(f"   Percentil 5    : ${estadisticas['gan_p5']:.2f}")
    print(f"   Percentil 25   : ${estadisticas['gan_p25']:.2f}")
    print(f"   Percentil 75   : ${estadisticas['gan_p75']:.2f}")
    print(f"   P(ganancia > 0): {estadisticas['prob_ganancia_positiva']:.2%}")

    print(f"\n{sep}\n")


# =============================================================================
# 5. VISUALIZACIÓN CON MATPLOTLIB (ESTÁTICO)
# =============================================================================

def graficar_matplotlib(
    lanzamientos: np.ndarray,
    ganancias: np.ndarray,
    nro_juegos: int,
) -> None:
    """Genera gráficos PDF y CDF con Matplotlib puro.

    Produce una figura de 2×2 con histogramas normalizados (PDF empírica)
    y funciones de distribución acumulada (CDF empírica) para lanzamientos
    y ganancias netas.

    Args:
        lanzamientos: Array con el número de lanzamientos por partida.
        ganancias: Array con las ganancias netas por partida.
        nro_juegos: Número total de juegos (para título).
    """
    # Paleta de colores consistente
    color_lanz = "#2196F3"      # Azul para lanzamientos
    color_gan_pos = "#4CAF50"   # Verde para ganancias positivas
    color_gan_neg = "#F44336"   # Rojo para ganancias negativas
    color_cdf = "#FF9800"       # Naranja para CDF

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f"Simulación Monte Carlo — Juego de Moneda ({nro_juegos:,} partidas)",
        fontsize=15, fontweight="bold", y=1.01,
    )

    # -----------------------------------------------------------------
    # [0,0] PDF de Lanzamientos
    # -----------------------------------------------------------------
    ax = axes[0, 0]
    valores_unicos, conteos = np.unique(lanzamientos, return_counts=True)
    frecuencias = conteos / nro_juegos  # Normalizar a probabilidad

    ax.bar(
        valores_unicos, frecuencias,
        color=color_lanz, alpha=0.75, edgecolor="white", linewidth=0.6,
        label="Frecuencia relativa",
    )
    ax.axvline(
        np.mean(lanzamientos), color="#0D47A1", linestyle="--",
        linewidth=1.8, label=f"Media = {np.mean(lanzamientos):.2f}",
    )
    ax.set_title("PDF Empírica — Lanzamientos por Partida", fontsize=12)
    ax.set_xlabel("Número de Lanzamientos", fontsize=10)
    ax.set_ylabel("Probabilidad", fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.35, linestyle=":")

    # -----------------------------------------------------------------
    # [0,1] CDF de Lanzamientos
    # -----------------------------------------------------------------
    ax = axes[0, 1]
    lanz_sorted = np.sort(lanzamientos)
    cdf_vals = np.arange(1, nro_juegos + 1) / nro_juegos

    ax.step(lanz_sorted, cdf_vals, color=color_cdf, linewidth=2, label="CDF empírica")
    ax.axhline(0.5, color="gray", linestyle=":", alpha=0.7, label="P = 0.50")
    ax.axvline(
        np.median(lanzamientos), color="#E65100", linestyle="--",
        linewidth=1.5, label=f"Mediana = {np.median(lanzamientos):.0f}",
    )
    ax.set_title("CDF Empírica — Lanzamientos por Partida", fontsize=12)
    ax.set_xlabel("Número de Lanzamientos", fontsize=10)
    ax.set_ylabel("Probabilidad Acumulada", fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.35, linestyle=":")
    ax.set_ylim(0, 1.05)

    # -----------------------------------------------------------------
    # [1,0] PDF de Ganancias (bicolor: positivo/negativo)
    # -----------------------------------------------------------------
    ax = axes[1, 0]
    valores_gan, conteos_gan = np.unique(ganancias, return_counts=True)
    frecuencias_gan = conteos_gan / nro_juegos

    # Colorear barras según signo de la ganancia
    colores_barras = [
        color_gan_pos if v > 0 else color_gan_neg for v in valores_gan
    ]
    ax.bar(
        valores_gan, frecuencias_gan,
        color=colores_barras, alpha=0.80, edgecolor="white", linewidth=0.6,
    )
    ax.axvline(
        np.mean(ganancias), color="#1B5E20", linestyle="--",
        linewidth=1.8, label=f"Media = ${np.mean(ganancias):.2f}",
    )
    ax.axvline(0, color="black", linestyle="-", linewidth=1.0, alpha=0.5)

    # Leyenda manual para bicolor
    parche_pos = mpatches.Patch(color=color_gan_pos, alpha=0.8, label="Ganancia > $0")
    parche_neg = mpatches.Patch(color=color_gan_neg, alpha=0.8, label="Ganancia ≤ $0")
    ax.legend(handles=[parche_pos, parche_neg], fontsize=9)

    ax.set_title("PDF Empírica — Ganancia Neta por Partida", fontsize=12)
    ax.set_xlabel("Ganancia Neta (USD)", fontsize=10)
    ax.set_ylabel("Probabilidad", fontsize=10)
    ax.grid(axis="y", alpha=0.35, linestyle=":")

    # -----------------------------------------------------------------
    # [1,1] CDF de Ganancias
    # -----------------------------------------------------------------
    ax = axes[1, 1]
    gan_sorted = np.sort(ganancias)
    cdf_gan = np.arange(1, nro_juegos + 1) / nro_juegos

    ax.step(gan_sorted, cdf_gan, color=color_cdf, linewidth=2, label="CDF empírica")
    ax.axvline(0, color="black", linestyle="-", alpha=0.4, linewidth=1.0)
    ax.axhline(0.5, color="gray", linestyle=":", alpha=0.7, label="P = 0.50")

    # Marcar probabilidad de pérdida (ganancia ≤ 0)
    prob_perdida = np.mean(ganancias <= 0)
    ax.axhline(
        prob_perdida, color=color_gan_neg, linestyle="--",
        linewidth=1.5, label=f"P(G ≤ 0) = {prob_perdida:.2%}",
    )
    ax.set_title("CDF Empírica — Ganancia Neta por Partida", fontsize=12)
    ax.set_xlabel("Ganancia Neta (USD)", fontsize=10)
    ax.set_ylabel("Probabilidad Acumulada", fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.35, linestyle=":")
    ax.set_ylim(0, 1.05)

    plt.tight_layout()
    ruta_guardado = "grafico_matplotlib.png"
    plt.savefig(ruta_guardado, dpi=150, bbox_inches="tight")
    print(f"✅ Matplotlib → guardado en '{ruta_guardado}'")
    plt.show()


# =============================================================================
# 6. VISUALIZACIÓN CON SEABORN (ESTÉTICO)
# =============================================================================

def graficar_seaborn(
    lanzamientos: np.ndarray,
    ganancias: np.ndarray,
    nro_juegos: int,
) -> None:
    """Genera gráficos PDF y CDF con Seaborn sobre Matplotlib.

    Utiliza la estética de Seaborn con KDE suavizada para la PDF y
    ECDF nativa de Seaborn para la CDF, en una disposición de 2×2.

    Args:
        lanzamientos: Array con el número de lanzamientos por partida.
        ganancias: Array con las ganancias netas por partida.
        nro_juegos: Número total de juegos (para título).
    """
    # Aplicar tema Seaborn con paleta personalizada
    sns.set_theme(style="whitegrid", palette="deep", font_scale=1.05)
    paleta = sns.color_palette("deep")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f"Simulación Monte Carlo — Juego de Moneda [{nro_juegos:,} partidas]",
        fontsize=14, fontweight="bold", y=1.01,
    )

    # -----------------------------------------------------------------
    # [0,0] PDF de Lanzamientos con histograma + KDE
    # -----------------------------------------------------------------
    ax = axes[0, 0]
    sns.histplot(
        lanzamientos, stat="probability", discrete=True,
        color=paleta[0], alpha=0.65, ax=ax, label="Histograma (prob.)",
    )
    # KDE suavizada sobre eje secundario para referencia visual
    ax2 = ax.twinx()
    sns.kdeplot(
        lanzamientos.astype(float), color=paleta[3],
        linewidth=2.2, ax=ax2, label="KDE suavizada",
    )
    ax2.set_ylabel("Densidad KDE", fontsize=9, color=paleta[3])
    ax2.tick_params(axis="y", labelcolor=paleta[3])

    ax.axvline(
        np.mean(lanzamientos), color=paleta[1], linestyle="--",
        linewidth=2, label=f"Media = {np.mean(lanzamientos):.2f}",
    )
    ax.set_title("PDF — Lanzamientos por Partida", fontsize=12)
    ax.set_xlabel("Número de Lanzamientos")
    ax.set_ylabel("Probabilidad")
    ax.legend(loc="upper right", fontsize=8)

    # -----------------------------------------------------------------
    # [0,1] CDF de Lanzamientos con ECDF de Seaborn
    # -----------------------------------------------------------------
    ax = axes[0, 1]
    sns.ecdfplot(
        lanzamientos, ax=ax, color=paleta[2],
        linewidth=2.2, label="ECDF lanzamientos",
    )
    ax.axhline(0.5, color="gray", linestyle=":", alpha=0.8, label="P = 0.50")
    ax.axvline(
        np.median(lanzamientos), color=paleta[4], linestyle="--",
        linewidth=1.8, label=f"Mediana = {np.median(lanzamientos):.0f}",
    )
    ax.set_title("CDF — Lanzamientos por Partida", fontsize=12)
    ax.set_xlabel("Número de Lanzamientos")
    ax.set_ylabel("Probabilidad Acumulada")
    ax.legend(fontsize=8)
    ax.set_ylim(0, 1.05)

    # -----------------------------------------------------------------
    # [1,0] PDF de Ganancias con histograma + KDE
    # -----------------------------------------------------------------
    ax = axes[1, 0]
    # Separar ganancias positivas y negativas para colorear
    gan_pos = ganancias[ganancias > 0]
    gan_neg = ganancias[ganancias <= 0]

    sns.histplot(
        gan_pos, stat="probability", discrete=True,
        color=paleta[2], alpha=0.7, ax=ax, label="Ganancia > $0",
    )
    sns.histplot(
        gan_neg, stat="probability", discrete=True,
        color=paleta[3], alpha=0.7, ax=ax, label="Ganancia ≤ $0",
    )
    sns.kdeplot(
        ganancias.astype(float), color=paleta[0],
        linewidth=2.0, ax=ax, label="KDE total",
    )
    ax.axvline(
        np.mean(ganancias), color="black", linestyle="--",
        linewidth=1.8, label=f"Media = ${np.mean(ganancias):.2f}",
    )
    ax.axvline(0, color="red", linestyle="-", linewidth=1.0, alpha=0.5)
    ax.set_title("PDF — Ganancia Neta por Partida", fontsize=12)
    ax.set_xlabel("Ganancia Neta (USD)")
    ax.set_ylabel("Probabilidad")
    ax.legend(fontsize=8)

    # -----------------------------------------------------------------
    # [1,1] CDF de Ganancias con ECDF + anotación de riesgo
    # -----------------------------------------------------------------
    ax = axes[1, 1]
    sns.ecdfplot(
        ganancias, ax=ax, color=paleta[5],
        linewidth=2.2, label="ECDF ganancias",
    )
    prob_perdida = np.mean(ganancias <= 0)
    ax.axvline(0, color="red", linestyle="-", alpha=0.4, linewidth=1.2)
    ax.axhline(0.5, color="gray", linestyle=":", alpha=0.8, label="P = 0.50")
    ax.axhline(
        prob_perdida, color=paleta[3], linestyle="--",
        linewidth=1.8, label=f"P(G ≤ 0) = {prob_perdida:.2%}",
    )
    # Anotación con flecha señalando punto de ruptura P=0
    ax.annotate(
        f"P(pérdida) = {prob_perdida:.2%}",
        xy=(0, prob_perdida), xytext=(2, prob_perdida + 0.12),
        fontsize=8, color=paleta[3],
        arrowprops=dict(arrowstyle="->", color=paleta[3], lw=1.2),
    )
    ax.set_title("CDF — Ganancia Neta por Partida", fontsize=12)
    ax.set_xlabel("Ganancia Neta (USD)")
    ax.set_ylabel("Probabilidad Acumulada")
    ax.legend(fontsize=8)
    ax.set_ylim(0, 1.05)

    plt.tight_layout()
    ruta_guardado = "grafico_seaborn.png"
    plt.savefig(ruta_guardado, dpi=150, bbox_inches="tight")
    print(f"✅ Seaborn   → guardado en '{ruta_guardado}'")
    plt.show()

    # Restaurar estilo por defecto para no afectar otras figuras
    sns.reset_defaults()


# =============================================================================
# 7. VISUALIZACIÓN CON PLOTLY (INTERACTIVO)
# =============================================================================

def graficar_plotly(
    lanzamientos: np.ndarray,
    ganancias: np.ndarray,
    nro_juegos: int,
) -> None:
    """Genera gráficos interactivos PDF y CDF con Plotly.

    Crea una figura de 2×2 con subplots interactivos: histogramas normalizados
    (PDF) y curvas ECDF para lanzamientos y ganancias. Permite zoom, hover
    y exportación desde la interfaz del navegador.

    Args:
        lanzamientos: Array con el número de lanzamientos por partida.
        ganancias: Array con las ganancias netas por partida.
        nro_juegos: Número total de juegos (para título).
    """
    # Calcular CDF manualmente para ambas variables
    lanz_sorted = np.sort(lanzamientos)
    cdf_lanz = np.arange(1, nro_juegos + 1) / nro_juegos

    gan_sorted = np.sort(ganancias)
    cdf_gan = np.arange(1, nro_juegos + 1) / nro_juegos

    # Frecuencias discretas para histogramas de barras exactas
    vals_lanz, cnts_lanz = np.unique(lanzamientos, return_counts=True)
    prob_lanz = cnts_lanz / nro_juegos

    vals_gan, cnts_gan = np.unique(ganancias, return_counts=True)
    prob_gan = cnts_gan / nro_juegos

    # Crear figura con 4 subplots (2 filas × 2 columnas)
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "PDF — Lanzamientos por Partida",
            "CDF — Lanzamientos por Partida",
            "PDF — Ganancia Neta por Partida",
            "CDF — Ganancia Neta por Partida",
        ),
        horizontal_spacing=0.10,
        vertical_spacing=0.15,
    )

    media_lanz = float(np.mean(lanzamientos))
    media_gan = float(np.mean(ganancias))
    mediana_lanz = float(np.median(lanzamientos))
    prob_perdida = float(np.mean(ganancias <= 0))

    # -----------------------------------------------------------------
    # [1,1] PDF Lanzamientos — barras de frecuencia relativa
    # -----------------------------------------------------------------
    fig.add_trace(
        go.Bar(
            x=vals_lanz, y=prob_lanz,
            name="PDF Lanzamientos",
            marker_color="#42A5F5", marker_opacity=0.78,
            hovertemplate="Lanzamientos: %{x}<br>P = %{y:.4f}<extra></extra>",
        ),
        row=1, col=1,
    )
    # Línea vertical de la media (truco con scatter + shape)
    fig.add_vline(
        x=media_lanz, line_dash="dash", line_color="#0D47A1", line_width=2,
        annotation_text=f"Media={media_lanz:.2f}",
        annotation_position="top right",
        row=1, col=1,
    )

    # -----------------------------------------------------------------
    # [1,2] CDF Lanzamientos — curva escalonada
    # -----------------------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=lanz_sorted, y=cdf_lanz,
            name="CDF Lanzamientos",
            mode="lines", line=dict(color="#FF7043", width=2.5, shape="hv"),
            hovertemplate="Lanzamientos ≤ %{x}: P = %{y:.4f}<extra></extra>",
        ),
        row=1, col=2,
    )
    fig.add_hline(
        y=0.5, line_dash="dot", line_color="gray", line_width=1.5,
        annotation_text="P=0.50", row=1, col=2,
    )
    fig.add_vline(
        x=mediana_lanz, line_dash="dash", line_color="#BF360C", line_width=1.8,
        annotation_text=f"Mediana={mediana_lanz:.0f}",
        annotation_position="bottom right",
        row=1, col=2,
    )

    # -----------------------------------------------------------------
    # [2,1] PDF Ganancias — barras bicolor (positivo/negativo)
    # -----------------------------------------------------------------
    colores_gan = [
        "#66BB6A" if v > 0 else "#EF5350" for v in vals_gan
    ]
    fig.add_trace(
        go.Bar(
            x=vals_gan, y=prob_gan,
            name="PDF Ganancias",
            marker_color=colores_gan, marker_opacity=0.82,
            hovertemplate="Ganancia: $%{x}<br>P = %{y:.4f}<extra></extra>",
        ),
        row=2, col=1,
    )
    fig.add_vline(
        x=media_gan, line_dash="dash", line_color="#1B5E20", line_width=2,
        annotation_text=f"Media=${media_gan:.2f}",
        annotation_position="top right",
        row=2, col=1,
    )
    fig.add_vline(
        x=0, line_dash="solid", line_color="black", line_width=1.0,
        row=2, col=1,
    )

    # -----------------------------------------------------------------
    # [2,2] CDF Ganancias — curva escalonada con marca de riesgo
    # -----------------------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=gan_sorted, y=cdf_gan,
            name="CDF Ganancias",
            mode="lines", line=dict(color="#AB47BC", width=2.5, shape="hv"),
            hovertemplate="Ganancia ≤ $%{x}: P = %{y:.4f}<extra></extra>",
        ),
        row=2, col=2,
    )
    fig.add_hline(
        y=0.5, line_dash="dot", line_color="gray", line_width=1.5,
        annotation_text="P=0.50", row=2, col=2,
    )
    fig.add_hline(
        y=prob_perdida, line_dash="dash", line_color="#EF5350", line_width=1.8,
        annotation_text=f"P(G≤0)={prob_perdida:.2%}",
        annotation_position="bottom right",
        row=2, col=2,
    )
    fig.add_vline(
        x=0, line_dash="solid", line_color="red", line_width=1.0,
        opacity=0.4, row=2, col=2,
    )

    # -----------------------------------------------------------------
    # Layout global de la figura
    # -----------------------------------------------------------------
    fig.update_layout(
        title=dict(
            text=(
                f"<b>Simulación Monte Carlo — Juego de Moneda</b>"
                f"<br><sup>{nro_juegos:,} partidas | Semilla={SEMILLA} | "
                f"Premio=$8 | Costo=$1/lanzamiento</sup>"
            ),
            x=0.5, font=dict(size=16),
        ),
        showlegend=False,
        height=750,
        template="plotly_white",
        paper_bgcolor="#FAFAFA",
        margin=dict(t=100, b=60, l=60, r=40),
    )

    # Etiquetas de ejes por subplot
    fig.update_xaxes(title_text="Número de Lanzamientos", row=1, col=1, gridcolor="#E0E0E0")
    fig.update_yaxes(title_text="Probabilidad", row=1, col=1, gridcolor="#E0E0E0")
    fig.update_xaxes(title_text="Número de Lanzamientos", row=1, col=2, gridcolor="#E0E0E0")
    fig.update_yaxes(title_text="Probabilidad Acumulada", row=1, col=2, range=[0, 1.05])
    fig.update_xaxes(title_text="Ganancia Neta (USD)", row=2, col=1, gridcolor="#E0E0E0")
    fig.update_yaxes(title_text="Probabilidad", row=2, col=1, gridcolor="#E0E0E0")
    fig.update_xaxes(title_text="Ganancia Neta (USD)", row=2, col=2, gridcolor="#E0E0E0")
    fig.update_yaxes(title_text="Probabilidad Acumulada", row=2, col=2, range=[0, 1.05])

    ruta_guardado = "grafico_plotly.html"
    fig.write_html(ruta_guardado)
    print(f"✅ Plotly     → guardado en '{ruta_guardado}' (abrir en navegador)")
    fig.show()


# =============================================================================
# 8. PUNTO DE ENTRADA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("\n🎲 Iniciando Simulación Monte Carlo — Juego de Moneda...")
    print(f"   Parámetros: {NRO_JUEGOS:,} juegos | p(cara)={PROB_CARA} | "
          f"premio=${PREMIO:.2f} | costo=${COSTO_LANZAMIENTO:.2f}/lanzamiento")

    # -------------------------------------------------------------------------
    # VERSIÓN ORIGINAL: parada solo por diferencia
    # -------------------------------------------------------------------------
    lanzamientos, ganancias = ejecutar_simulacion(
        nro_juegos=NRO_JUEGOS,
        prob_cara=PROB_CARA,
        premio=PREMIO,
        costo_lanzamiento=COSTO_LANZAMIENTO,
    )

    estadisticas = calcular_estadisticas(lanzamientos, ganancias)
    imprimir_estadisticas(estadisticas, NRO_JUEGOS)

    print("📈 Generando visualización con Matplotlib...")
    graficar_matplotlib(lanzamientos, ganancias, NRO_JUEGOS)

    print("🎨 Generando visualización con Seaborn...")
    graficar_seaborn(lanzamientos, ganancias, NRO_JUEGOS)

    print("🌐 Generando visualización interactiva con Plotly...")
    graficar_plotly(lanzamientos, ganancias, NRO_JUEGOS)

    # -------------------------------------------------------------------------
    # VERSIÓN 2: doble condición de parada (diferencia=3 ó lanzamientos=15)
    # -------------------------------------------------------------------------
    sep = "=" * 60
    print(f"\n{sep}")
    print("  SIMULACIÓN V2 — DOBLE CONDICIÓN DE PARADA")
    print(f"  Parada si |caras-sellos|={DIFERENCIA_LIMITE} "
          f"ó n_lanzamientos={LIMITE_LANZAMIENTOS}")
    print(sep)

    lanz_v2, gan_v2, victorias_v2 = ejecutar_simulacion_v2(
        nro_juegos=NRO_JUEGOS,
        prob_cara=PROB_CARA,
        premio=PREMIO,
        costo_lanzamiento=COSTO_LANZAMIENTO,
    )

    # Estadísticas globales de la v2
    n_victorias = int(np.sum(victorias_v2))
    n_derrotas = NRO_JUEGOS - n_victorias
    tasa_victoria = n_victorias / NRO_JUEGOS

    print(f"\n🏆 RESULTADOS POR TIPO DE FIN:")
    print(f"   Victorias (por diferencia) : {n_victorias:>5}  ({tasa_victoria:.2%})")
    print(f"   Derrotas  (por límite)     : {n_derrotas:>5}  ({1 - tasa_victoria:.2%})")

    print(f"\n📊 LANZAMIENTOS — V2 (todos los juegos):")
    print(f"   Media          : {np.mean(lanz_v2):.4f}")
    print(f"   Desv. Estándar : {np.std(lanz_v2, ddof=1):.4f}")
    print(f"   Mínimo / Máximo: {np.min(lanz_v2)} / {np.max(lanz_v2)}")

    # Desglose por tipo de fin
    lanz_victoria = lanz_v2[victorias_v2]
    lanz_derrota = lanz_v2[~victorias_v2]
    if len(lanz_victoria) > 0:
        print(f"   Media victorias: {np.mean(lanz_victoria):.4f}")
    if len(lanz_derrota) > 0:
        print(f"   Media derrotas : {np.mean(lanz_derrota):.4f}  "
              f"(siempre = {LIMITE_LANZAMIENTOS})")

    print(f"\n💰 GANANCIAS NETAS — V2 (todos los juegos):")
    print(f"   Media (E[G])   : ${np.mean(gan_v2):.4f}")
    print(f"   Desv. Estándar : ${np.std(gan_v2, ddof=1):.4f}")
    print(f"   Mínimo / Máximo: ${np.min(gan_v2):.2f} / ${np.max(gan_v2):.2f}")
    print(f"   P(ganancia > 0): {np.mean(gan_v2 > 0):.2%}")

    # Comparativa entre ambas versiones
    print(f"\n🔍 COMPARATIVA v1 vs v2:")
    print(f"   {'Métrica':<28} {'v1 (sin límite)':>16} {'v2 (límite=15)':>16}")
    print(f"   {'-'*60}")
    print(f"   {'E[lanzamientos]':<28} {np.mean(lanzamientos):>16.4f} "
          f"{np.mean(lanz_v2):>16.4f}")
    print(f"   {'E[ganancia] (USD)':<28} {np.mean(ganancias):>16.4f} "
          f"{np.mean(gan_v2):>16.4f}")
    print(f"   {'P(ganancia > 0)':<28} {np.mean(ganancias > 0):>16.2%} "
          f"{np.mean(gan_v2 > 0):>16.2%}")
    print(f"   {'Máx. lanzamientos':<28} {np.max(lanzamientos):>16} "
          f"{np.max(lanz_v2):>16}")
    print(f"\n{sep}\n")

    print("\n✅ Simulación completa. Revisa los archivos generados:")
    print("   • grafico_matplotlib.png")
    print("   • grafico_seaborn.png")
    print("   • grafico_plotly.html  ← abrir en navegador para interactividad\n")