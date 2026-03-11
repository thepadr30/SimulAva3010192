cat("
/*----------------------------------------------------------------------------+
|                                                                             |
|                              copyright (c) 2026.                            |
|                                                                             |
+-------------+---------------------------------------------------------------+
| producto:   | 3010192 Simulación Avanzada                                   |
| Tema:       | librerías                                                     |
| programa:   | 02Librerias.R                                                 |
| soporte:    | kfhidalgoh@unal.edu.co                                        |
| version:    | 4.5.2 (2025-10-31) -- [Not] Part in a Rumble                  |
| lenguaje:   | R                                                             |
+-------------+---------------------------------------------------------------+
| proposito:  | librerias de trabajo                                          |
+-------------+---------------------------------------------------------------+
| parametros: | vector de strings con el nombre de las librerias requeridas   |
+-------------+---------------------------------------------------------------+
| Salidas   : | librerías cargadas en memoria                                 |
| Generadas   |                                                               |
+-------------+---------------------------------------------------------------+
| comentarios:|                                                               |
+-------------+---------------------------------------------------------------+
| Autor(es):  | Kevin Hidalgo | Estadístico                                   |
+-------------+--------------+-----------+-----------------------------------*/
"
)

# función auxiliar --------------------------------------------------------

ipak <- function(pkg){
  # Valida, instala y carga de librerías desde el CRAN.
  #
  # Args:
  #   pkg: Vector compuesto de los nombres de las librerías como string.
  #
  # Return:
  #   Carga de librerías en el entorno.
  #
  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg))
    install.packages(new.pkg, dependencies = TRUE)
  sapply(pkg, require, character.only = TRUE)
  cita <- sapply(names(sessionInfo()$otherPkgs),
                 function(x) print(citation(x), style = "Bibtex"))
}


# Carga -------------------------------------------------------------------

# vector.librerias <- c( "ggplot2", "quantmod", "beepr", "stringr",
#                        "stargazer", "readr", "tidyr", "dplyr",
#                        "TTR", "TSstudio", "forecast", "progress", "HARModel",
#                        "highfrequency", "reshape", "lubridate", "greybox")

vector.librerias <- c('ggplot2', 'dplyr', 'e1071', 'moments',
                      'stargazer',
                      # 'kableExtra',
                      'gt')


ipak(vector.librerias)

rm(vector.librerias)
