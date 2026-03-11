options(scipen = 100, digits = 4, encoding = "UTF-8")
cat("
/*----------------------------------------------------------------------------+
|                                                                             |
|                             copyright (c) 2026.                             |
|                                                                             |
+-------------+---------------------------------------------------------------+
| producto:   | 3010192 Simulación avanzada                                   |
| Tema:       | ejecutor                                                      |
| programa:   | 00Run.R                                                       |
| soporte:    | kfhidalgoh@unal.edu.co                                        |
| version:    | 4.5.2 (2025-10-31) -- [Not] Part in a Rumble                  |
| lenguaje:   | R                                                             |
+-------------+---------------------------------------------------------------+
| proposito:  | Ejecución flujo de trabajo                                    |
+-------------+---------------------------------------------------------------+
| parametros: | Usuario                                                       |
+-------------+---------------------------------------------------------------+
| Salidas   : |                                                               |
| Generadas   |                                                               |
+-------------+---------------------------------------------------------------+
| comentarios:| 1. se debe cambiar las rutas de archivos para su adecuada     |
+-------------+---------------------------------------------------------------+
| Autor(es):  | Kevin Hidalgo | Estadístico                                   |
+-------------+--------------+-----------+-----------------------------------*/
"
)

# Usuario -----------------------------------------------------------------

cat('Por favor ingrese Esteban o Kevin termine con la tecla enter pulsando dos
    veces esta')
usuario <- scan(what = "")
#usuario <- "Kevin"
#usuario <- "Esteban"


if (usuario == "Kevin") {
  dir.log <- "G:/Mi unidad/Semestre actual/trading/entregable/developer/log"
  log <- file(paste0(dir.log,
                     "/00Run_",
                     format(Sys.time(), "%Y_%m_%d_%H_%M_%S"),
                     ".log"),
              open = "wt")
  sink(log, type = "output")
  sink(log, type = "message")
} else if (usuario == "Esteban") {
  dir.log <- "D://Desktop//Trade//trading//data//csv"
  log <- file(paste0(dir.log,
                     "/00Run_",
                     format(Sys.time(), "%Y_%m_%d_%H_%M_%S"),
                     ".log"),
              open = "wt")
  sink(log, type = "output")
  sink(log, type = "message")
} else {
  print("Usuario no identificado")
}


# Direcciones -------------------------------------------------------------

s1 <- Sys.time()

if (usuario == "Kevin") {
  source(paste0("G:/Mi unidad/Semestre actual/trading/entregable/developer/R",
                "/01Direcciones.R"),
         echo = TRUE)
} else if (usuario == "Esteban"){
  source(paste0("G:/Mi unidad/Semestre actual/trading/entregable/developer/R",
                "/01Direcciones.R"),
         echo = TRUE)
} else {
  print("Usuario no identificado")
}

# Librerías ---------------------------------------------------------------

source(paste0(dir.R, "/02Librerias.R"), echo=FALSE)

# Funciones auxiliares ----------------------------------------------------

source(paste0(dir.R, "/03Funciones.R"), echo=FALSE)

# Lectura -----------------------------------------------------------------

Data_ANALISIS <- read_delim(paste0(dir.Data.Input.csv,"/Data ANALISIS.csv"), ";",
                            escape_double = FALSE, trim_ws = TRUE)

data <- Data_ANALISIS[, c(1:22)]

names(data) <- organiza.nombres.columnas(data)

data <- data %>% unite("fecha_hora", fecha, hora, sep = " ", remove = FALSE)

data$fecha_hora <- strptime(data$fecha_hora, format = "%d/%m/%Y %H:%M:%S")

#Número de periodos a pronosticas
n = 15

#temp <- data$fecha_hora[nrow(data)] - 2592000 # mes
#temp <- data$fecha_hora[nrow(data)] - 1296000 # 15 días
#temp <- data$fecha_hora[nrow(data)] - 86400 # 24 horas
#temp <- data$fecha_hora[nrow(data)] - (86400) * 2 # 24 horas

#data <- data %>% filter(fecha_hora >= temp)

#data <- data %>% filter(fecha_hora <= "2020-12-04 10:00:00 -05")

#test.1 <- data %>% filter(fecha_hora >= "2020-12-15 09:30:00 -05" &
#                            fecha_hora <= "2020-12-15 11:00:00 -05")

#test.2 <- data %>% filter(fecha_hora >= "2020-08-01 09:30:00 -05" &
#                            fecha_hora <= "2020-08-07 11:00:00 -05")

# filtrado por fechas
data <- data %>% filter(fecha_hora >= "2020-12-03 09:30:00 -05" &
                          fecha_hora <= "2020-12-04 10:00:00 -05")


# serie de tiempo
#st <- xts(data$close, order.by = data$fecha_hora)
st <- xts(data[, c("open","high", "low", "close")], order.by = data$fecha_hora)
#st.test.1 <- xts(test.1[, c("open","high", "low", "close")],
#                 order.by = test.1$fecha_hora)
#st.test.2 <- xts(test.2[, c("open","high", "low", "close")],
#                 order.by = test.2$fecha_hora)

# Modelos -----------------------------------------------------------------

source(paste0(dir.R, "/04Modelos.R"), echo = FALSE)

# Control tiempo ----------------------------------------------------------

s2 <- Sys.time()
s2 - s1

sessionInfo()

sink()
sink()