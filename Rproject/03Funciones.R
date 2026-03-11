cat("
/*----------------------------------------------------------------------------+
|                                                                             |
|                   copyright (c) 2021 by Kevin Hidalgo.                      |
|                                                                             |
+-------------+---------------------------------------------------------------+
| producto:   | Proyecto trading                                              |
| Tema:       | funciones auxiliares                                          |
| programa:   | 03Funciones.R                                                 |
| soporte:    | kfhidalgoh@unal.edu.co                                        |
| version:    | 4.0.3 (2020-10-10) -- Bunny-Wunnies Freak Out                 |
| lenguaje:   | R                                                             |
+-------------+---------------------------------------------------------------+
| proposito:  | funciones auxiliares para la adecuada ejecución del proyecto  |
+-------------+---------------------------------------------------------------+
| parametros: |                                                               |
+-------------+---------------------------------------------------------------+
| Salidas   : | funciones en memoria                                          |
| Generadas   |                                                               |
+-------------+---------------------------------------------------------------+
| comentarios:|                                                               |
+-------------+---------------------------------------------------------------+
| Autor(es):  | Kevin Hidalgo | Estadístico                                   |
+-------------+--------------+-----------+-----------------------------------*/
"
)

# limpieza de datos -------------------------------------------------------

organiza.nombres.columnas <- function(dataframe) {
  # retorna los nombres de las columnas del dataframe
  # corregidos con buenas prácticas de sintaxis.
  #
  # Args:
  #   dataframe: dataframe.
  #
  # Returns:
  #   retorna un vector con los nombre de sus columnas sin los siguientes
  #   caracteres especiales:
  #   ., _, á, é, í, ó, ú, ü
  # Usage:
  #   names(dataframe) <- organizanombrescolumnas(dataframe)
  # author:
  #   Kevin Hidalgo
  #
  nombres <- names(dataframe)
  nombres <- tolower(nombres)
  nombres <- gsub("\\.", "", nombres)
  nombres <- gsub(" ", "_", nombres)
  nombres <- gsub("á", "a", nombres)
  nombres <- gsub("é", "e", nombres)
  nombres <- gsub("í", "i", nombres)
  nombres <- gsub("ó", "o", nombres)
  nombres <- gsub("ú", "u", nombres)
  nombres <- gsub("ü", "u", nombres)
  #nombres <- gsub("\\$", "cop", nombres)
  #nombres <- gsub("\\#", "num", nombres)
  nombres
}

organiza.elementos.variable.string <- function(dataframe) {
  # A cada observación del dataframe le aplicará buenas prácticas y limpieza de
  # texto.
  #
  # Args:
  #   dataframe: dataframe de R
  #
  # Returns:
  #   Un Dataframe con sus observaciones corregidas con buenas prácticas y con
  #   limpieza de algunos caracteres especiales.
  # Usage:
  #   dataframe <- organiza.elementos.variable.string(daataframe)
  # author:
  #   Kevin Hidalgo
  #
  df_tem <- sapply(as.data.frame(dataframe), function(x) {
    tolower(x) %>%
      str_replace_all("á", "a") %>%
      str_replace_all("é", "e") %>%
      str_replace_all("í", "i") %>%
      str_replace_all("ó", "o") %>%
      str_replace_all("ú", "u") %>%
      str_replace_all("ü", "u") 
  })
  
  df_tem <- as.data.frame(df_tem)
  return(df_tem)
}

fn.signal.SMA <- function(data) {
  # Crear la señal de la variable SMA.13 y SMA.200
  #
  # Args:
  #   dataframe: dataframe de R
  #
  # Returns:
  #   Un Dataframe con la variable adicional signal.momentum.5
  # Usage:
  #   dataframe <- fn.signal.SMA(daataframe)
  # author:
  #   Kevin Hidalgo
  #
  pb <- progress_bar$new(format = "[:bar] :current/:total (:percent)",
                         total = nrow(data))
  data$signal.SMA <- NA
  for (i in seq_len(nrow(data))) {
    pb$tick(1)
    Sys.sleep(1 / 100)
    if (isTRUE(data$close.sma.13[i] > data$close.sma.200[i])) {
      # compra
      data$signal.SMA[i] <- 1
    } else if (isTRUE(data$close.sma.13[i] < data$close.sma.200[i])) {
      # venta
      data$signal.SMA[i] <- 0
    } else data$signal.SMA[i] <- -1
  }
  return(data)
}

fn.signal.EMA <- function(data) {
  # Crear la señal de la variable SMA.13 y SMA.200
  #
  # Args:
  #   dataframe: dataframe de R
  #
  # Returns:
  #   Un Dataframe con la variable adicional signal.momentum.5
  # Usage:
  #   dataframe <- fn.signal.EMA(dataframe)
  # author:
  #   Kevin Hidalgo
  #
  pb <- progress_bar$new(format = "[:bar] :current/:total (:percent)",
                         total = nrow(data))
  data$signal.EMA <- NA
  for (i in seq_len(nrow(data))) {
    pb$tick(1)
    Sys.sleep(1 / 100)
    if (isTRUE(data$close.ema.13[i] > data$close.ema.200[i])) {
      # compra
      data$signal.EMA[i] <- 1
    } else if (isTRUE(data$close.ema.13[i] < data$close.ema.200[i])) {
      # venta
      data$signal.EMA[i] <- 0
    } else data$signal.EMA[i] <- -1
  }
  return(data)
}

fn.signal.MACD <- function(data){
  # Crear la señal de la variable momentum.5
  #
  # Args:
  #   dataframe: dataframe de R
  #
  # Returns:
  #   Un Dataframe con la variable adicional signal.momentum.5
  # Usage:
  #   dataframe <- fn.signal.Momentum(daataframe)
  # author:
  #   Kevin Hidalgo
  #
  pb <- progress_bar$new(format = "[:bar] :current/:total (:percent)",
                         total = nrow(data))
  data$signal.MACD.signal <- NA
  for (i in seq_len(nrow(data))){
    pb$tick(1)
    Sys.sleep(1 / 100)
    #print(i)
    if (!is.na(data$close.MACD.13.25.9.signal[i])){
      if (!is.na(data$close.MACD.13.25.9.signal[i-1])){
        if (data$close.MACD.13.25.9.signal[i-1] < 0 &&
            data$close.MACD.13.25.9.signal[i] > 0){
          data$signal.MACD.signal[i] = 1
        } else if (data$close.MACD.13.25.9.signal[i-1] > 0 &&
                   data$close.MACD.13.25.9.signal[i] < 0){
          data$signal.MACD.signal[i] = 0
        } else {
          data$signal.MACD.signal[i] = -1
        }
      } else {
        next
      }
    } else {
      next
    }
  }
  return(data)
}

fn.signal.ADX <- function(data) {
  # Crear la señal de la variable SMA.13 y SMA.200
  #
  # Args:
  #   dataframe: dataframe de R
  #
  # Returns:
  #   Un Dataframe con la variable adicional signal.momentum.5
  # Usage:
  #   dataframe <- fn.signal.EMA(dataframe)
  # author:
  #   Kevin Hidalgo
  #
  pb <- progress_bar$new(format = "[:bar] :current/:total (:percent)",
                         total = nrow(data))
  data$signal.ADX <- NA
  for (i in seq_len(nrow(data))) {
    pb$tick(1)
    Sys.sleep(1 / 100)
    if (isTRUE(data$adx.DIp[i] > data$adx.DIn[i])) {
      # compra
      data$signal.ADX[i] <- 1
    } else if (isTRUE(data$adx.DIp[i] < data$adx.DIn[i])) {
      # venta
      data$signal.ADX[i] <- 0
    } else data$signal.ADX[i] <- -1
  }
  return(data)
}

fn.signal.SAR <- function(data, delta) {
  # Crear la señal de la variable SAR
  #
  # Args:
  #   dataframe: dataframe de R
  #
  # Returns:
  #   Un Dataframe con la variable adicional signal.momentum.5
  # Usage:
  #   dataframe <- fn.signal.SAR(dataframe)
  # author:
  #   Kevin Hidalgo
  #
  pb <- progress_bar$new(format = "[:bar] :current/:total (:percent)",
                         total = nrow(data))
  data$signal.SAR <- NA
  for (i in seq_len(nrow(data))) {
    pb$tick(1)
    Sys.sleep(1 / 100)
    if (isTRUE(data$sar[i] > data$close[i])) {
      if (isTRUE(abs(data$sar[i] - data$close[i]) < delta)) {
        data$signal.SAR[i] <- 1
      } else data$signal.SAR[i] <- -1
    } else if (isTRUE(data$sar[i] < data$close[i])) {
      if (isTRUE(abs(data$sar[i] - data$close[i]) < delta)) {
        data$signal.SAR[i] <- 0
      } else data$signal.SAR[i] <- -1
    } else data$signal.SAR[i] <- -1
  }
  return(data)
}

fn.signal.TRIX <- function(data){
  # Crear la señal de la variable momentum.5
  #
  # Args:
  #   dataframe: dataframe de R
  #
  # Returns:
  #   Un Dataframe con la variable adicional signal.momentum.5
  # Usage:
  #   dataframe <- fn.signal.Momentum(daataframe)
  # author:
  #   Kevin Hidalgo
  #
  pb <- progress_bar$new(format = "[:bar] :current/:total (:percent)",
                         total = nrow(data))
  data$signal.TRIX.signal <- NA
  for (i in seq_len(nrow(data))){
    pb$tick(1)
    Sys.sleep(1 / 100)
    #print(i)
    if (!is.na(data$TRIX.signal[i])){
      if (!is.na(data$TRIX.signal[i-1])){
        if (data$TRIX.signal[i-1] < 0 &&
            data$TRIX.signal[i] > 0){
          data$signal.TRIX.signal[i] = 1
        } else if (data$TRIX.signal[i-1] > 0 &&
                   data$TRIX.signal[i] < 0){
          data$signal.TRIX.signal[i] = 0
        } else {
          data$signal.TRIX.signal[i] = -1
        }
      } else {
        next
      }
    } else {
      next
    }
  }
  return(data)
}

fn.signal.Momentum <- function(data){
  # Crear la señal de la variable momentum.5
  #
  # Args:
  #   dataframe: dataframe de R
  #
  # Returns:
  #   Un Dataframe con la variable adicional signal.momentum.5
  # Usage:
  #   dataframe <- fn.signal.Momentum(daataframe)
  # author:
  #   Kevin Hidalgo
  #
  pb <- progress_bar$new(format = "[:bar] :current/:total (:percent)",
                         total = nrow(data))
  data$signal.momentum.5 <- NA
  for (i in seq_len(nrow(data))){
    pb$tick(1)
    Sys.sleep(1 / 100)
    #print(i)
    if (!is.na(data$close.momentum.5[i])){
      if (!is.na(data$close.momentum.5[i-1])){
        if (data$close.momentum.5[i-1] < 0 &&
            data$close.momentum.5[i] > 0){
          data$signal.momentum.5[i] = 1
        } else if (data$close.momentum.5[i-1] > 0 &&
                   data$close.momentum.5[i] < 0){
          data$signal.momentum.5[i] = 0
        } else {
          data$signal.momentum.5[i] = -1
        }
      } else {
        next
      }
    } else {
      next
    }
  }
  return(data)
}

head.cast_df <- function (x, n = 6L, ...)  {
  stopifnot(length(n) == 1L)
  n <- if (n < 0L) {
    max(nrow(x) + n, 0L)
  } else min(n, nrow(x))
  h <- x[seq_len(n), , drop = FALSE]
  ## fix cast_df-specific row names element
  attr(h,"rdimnames")[[1]] <- rdimnames(h)[[1]][seq_len(n),,drop=FALSE]
  h
}