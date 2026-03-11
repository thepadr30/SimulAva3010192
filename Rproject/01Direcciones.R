cat("
/*----------------------------------------------------------------------------+
|                                                                             |
|                             copyright (c) 2026                              |
|                                                                             |
+-------------+---------------------------------------------------------------+
| producto:   | 3010192 Simulación Avanzada                                   |
| Tema:       | Simulación Monte Carlo                                        |
| programa:   | 01Direcciones.R                                               |
| soporte:    | kfhidalgoh@unal.edu.co                                        |
| version:    | 4.5.2 (2025-10-31) -- [Not] Part in a Rumble                  |
| lenguaje:   | R                                                             |
+-------------+---------------------------------------------------------------+
| proposito:  | generar rutas de trabajo                                      |
+-------------+---------------------------------------------------------------+
| parametros: | ruta archivo carpeta                                          |
+-------------+---------------------------------------------------------------+
| Salidas   : | variables con rutas                                           |
| Generadas   |                                                               |
+-------------+---------------------------------------------------------------+
| comentarios:| se debe cambiar las rutas de archivos para su adecuada        |
|             | ejecución                                                     |
+-------------+---------------------------------------------------------------+
| Autor(es):  | Kevin Hidalgo | Estadístico                                   |
+-------------+--------------+-----------+-----------------------------------*/
"
)



# rutas -------------------------------------------------------------------

if (usuario == "Kevin") {
  dir.root <- "D:/SimulAva/Rproject"
  dir.data.processed <- paste0(dir.root, '/data/processed')
  dir.data.raw <- paste0(dir.root, '/data/raw')
  dir.log <- paste0(dir.root, "/log")
} else {
  print('Usuario no identificado')
}