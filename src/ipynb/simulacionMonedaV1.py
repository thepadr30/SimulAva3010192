#%%
import random

# 1. Definición de parámetros básicos [2]
nro_juegos = 1000
prob_cara = 0.5
premio = 8.0
costo_lanzamiento = 1.0

# Inicialización de contadores para estadísticas [1, 2, 7]
utilidades = []
total_lanzamientos = []

#%%
# 2. Algoritmo de simulación (Ciclo para cada juego) [2, 8, 9]
for juego in range(nro_juegos):
    nro_caras = 0
    nro_sellos = 0
    lanzamientos_del_juego = 0

    # Ciclo del juego: continúa mientras la diferencia no sea 3 [2, 10, 11]
    while abs(nro_caras - nro_sellos) < 3:
        lanzamientos_del_juego += 1

        # Simulación del lanzamiento mediante número aleatorio R [4, 12]
        r = random.random()

        if r < prob_cara:
            nro_caras += 1
        else:
            nro_sellos += 1

    # 3. Cálculo de resultados al terminar el juego [11, 13, 14]
    utilidad = premio - (lanzamientos_del_juego * costo_lanzamiento)

    # Recolección de datos para estadísticas finales [14-16]
    utilidades.append(utilidad)
    total_lanzamientos.append(lanzamientos_del_juego)

#%%
# 4. Cálculo de estadísticas globales para la toma de decisiones [2, 16, 17]
utilidad_media = sum(utilidades) / nro_juegos
utilidad_minima = min(utilidades)
utilidad_maxima = max(utilidades)
promedio_lanzamientos = sum(total_lanzamientos) / nro_juegos
prob_terminar_3 = (total_lanzamientos.count(3) / nro_juegos) * 100

# 5. Impresión de resultados [6, 15, 17]
print(f"--- Informe final de la simulación ({nro_juegos} juegos) ---")
print(f"Utilidad media: ${utilidad_media:.2f}")
print(f"Utilidad mínima: ${utilidad_minima}")
print(f"Utilidad máxima: ${utilidad_maxima}")
print(f"Número medio de lanzamientos: {promedio_lanzamientos:.2f}")
print(f"Probabilidad de terminar en 3 lanzamientos: {prob_terminar_3:.1f}%")

# Veredicto final según el autor [6, 18]
if utilidad_media >= 0:
    print("El juego es favorable.")
else:
    print("El juego es desfavorable.")

#%%


def simular_un_juego(prob_cara=0.5, premio=8.0, costo_lanzamiento=1.0, max_lanzamientos=15):
    """
    Simula un solo juego de la moneda con un límite de lanzamientos.
    """
    nro_caras = 0
    nro_sellos = 0
    lanzamientos_realizados = 0

    # El bucle continúa MIENTRAS la diferencia sea menor a 3
    # Y el número de lanzamientos sea menor al límite (15)
    while abs(nro_caras - nro_sellos) < 3 and lanzamientos_realizados < max_lanzamientos:
        lanzamientos_realizados += 1

        # Generamos el número aleatorio R para el lanzamiento
        if random.random() < prob_cara:
            nro_caras += 1
        else:
            nro_sellos += 1

    # Calculamos la utilidad final del juego
    utilidad = premio - (lanzamientos_realizados * costo_lanzamiento)

    return utilidad, lanzamientos_realizados

#%%
utilidad_1, lanzamientos_1 = simular_un_juego()
