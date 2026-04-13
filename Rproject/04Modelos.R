cat("
/*----------------------------------------------------------------------------+
|                                                                             |
|                             copyright (c) 2021                              |
|                                                                             |
+-------------+---------------------------------------------------------------+
| producto:   | Trading                                                       |
| Tema:       | Indicadores técnicos.                                         |
| programa:   | 04Modelos.R                                                   |
| soporte:    | luemartinezro@unal.edu.co                                     |
| version:    | 4.0.3 (2020-10-10) -- Bunny-Wunnies Freak Out                 |
| lenguaje:   | R                                                             |
+-------------+---------------------------------------------------------------+
| proposito:  | generar Indicadores técnicos                                  |
+-------------+---------------------------------------------------------------+
| parametros: | BD con fecha, open, close, low, hight, volumen                |
+-------------+---------------------------------------------------------------+
| Salidas   : |                                                               |
| Generadas   |                                                               |
+-------------+---------------------------------------------------------------+
| comentarios:| venta = 0, compra = 1                                         |
+-------------+---------------------------------------------------------------+
| Autor(es):  | Esteban Martinez | Estadístico                                |
+-------------+--------------+-----------+-----------------------------------*/
"
)

# Holdout -----------------------------------------------------------------

train <- data[1:(nrow(data)-n),]
st.train <- xts(train[, c("open","high", "low", "close")],
                order.by = train$fecha_hora)
test <- data[(nrow(data)-n + 1):nrow(data),]

# Agregar la serie por minutes y periodos ---------------------------------

tsagg2min = aggregateTS(st, alignBy="minutes", alignPeriod=2)
tsagg2min.train = aggregateTS(st.train, alignBy="minutes", alignPeriod=2)
#head(tsagg2min)

# Model Close -------------------------------------------------------------

model.close <- HARForecast(tsagg2min$close, periods = c(1,5,22), nRoll =10,
                          nAhead = n, type = "HAR")

model.close.train <- HARForecast(tsagg2min.train$close, periods = c(1,5,22),
                                 nRoll =10, nAhead = n, type = "HAR")


data.close <- data.frame(model.close@forecast)
data.close.train <- data.frame(model.close.train@forecast)

tmp <- ncol(data.close)
tem <- sample(tmp,1)

data.close <- data.close %>%
  mutate(
    t = seq(1, nrow(data.close), 1),
    close = data.close[,tem]
  )

tmp <- ncol(data.close.train)
tem <- sample(tmp,1)

data.close.train <- data.close.train %>%
  mutate(
    t = seq(1, nrow(data.close.train), 1),
    close = data.close.train[,tem]
  )

data.close.tem <- data.close %>%
  rowwise() %>%
  mutate(
    min.close = min(roll1, roll2, roll3, roll4, roll5, roll6, roll7, roll8,
                    roll9, roll10),
    max.close = max(roll1, roll2, roll3, roll4, roll5, roll6, roll7, roll8,
                    roll9, roll10)
  )

data.close <- data.close %>% select(t, close)
data.close.train <- data.close.train %>% select(t, close)

metricas.close <- data.frame(Variable = "Close",
                             ME = ME(test$close, data.close.train$close),
                             MAE = MAE(test$close, data.close.train$close),
                             MSE = MSE(test$close, data.close.train$close),
                             MPE = MPE(test$close, data.close.train$close),
                             MAPE = MAPE(test$close, data.close.train$close))

# Model Open --------------------------------------------------------------

model.open <- HARForecast(tsagg2min$open, periods = c(1,5,22), nRoll =10,
                          nAhead = n, type = "HAR")

model.open.train <- HARForecast(tsagg2min.train$open, periods = c(1,5,22), nRoll =10,
                          nAhead = n, type = "HAR")

data.open <- data.frame(model.open@forecast)
data.open.train <- data.frame(model.open.train@forecast)

tmp <- ncol(data.open)
tem <- sample(tmp,1)

data.open <- data.open %>%
  mutate(
    t = seq(1, nrow(data.open), 1),
    open = data.open[,tem]
  )

tmp <- ncol(data.open.train)
tem <- sample(tmp,1)

data.open.train <- data.open.train %>%
  mutate(
    t = seq(1, nrow(data.open.train), 1),
    open = data.open.train[,tem]
  )

data.open.tem <- data.open %>%
  rowwise() %>%
  mutate(
    min.open = min(roll1, roll2, roll3, roll4, roll5, roll6, roll7, roll8,
                   roll9, roll10),
    max.open = max(roll1, roll2, roll3, roll4, roll5, roll6, roll7, roll8,
                   roll9, roll10)
  )

data.open <- data.open %>% select(t, open)
data.open.train <- data.open.train %>% select(t, open)

metricas.open <- data.frame(Variable = "Open",
                            ME = ME(test$open, data.open.train$open),
                            MAE = MAE(test$open, data.open.train$open),
                            MSE = MSE(test$open, data.open.train$open),
                            MPE = MPE(test$open, data.open.train$open),
                            MAPE = MAPE(test$open, data.open.train$open))

# Model Hight -------------------------------------------------------------

model.hight <- HARForecast(tsagg2min$high, periods = c(1,5,22), nRoll =10,
                          nAhead = n, type = "HAR")

model.hight.train <- HARForecast(tsagg2min.train$high, periods = c(1,5,22), nRoll =10,
                          nAhead = n, type = "HAR")

data.hight <- data.frame(model.hight@forecast)
data.hight.train <- data.frame(model.hight.train@forecast)

tmp <- ncol(data.hight)
tem <- sample(tmp,1)

data.hight <- data.hight %>%
  mutate(
    t = seq(1, nrow(data.hight), 1),
    hight = data.hight[,tem]
  )

tmp <- ncol(data.hight.train)
tem <- sample(tmp,1)

data.hight.train <- data.hight.train %>%
  mutate(
    t = seq(1, nrow(data.hight.train), 1),
    hight = data.hight.train[,tem]
  )

data.hight.tem <- data.hight %>%
  rowwise() %>%
  mutate(
    min.hight = min(roll1, roll2, roll3, roll4, roll5, roll6, roll7, roll8,
                    roll9, roll10),
    max.hight = max(roll1, roll2, roll3, roll4, roll5, roll6, roll7, roll8,
                    roll9, roll10)
  )

data.hight <- data.hight %>% select(t, hight)
data.hight.train <- data.hight.train %>% select(t, hight)

metricas.hight <- data.frame(Variable = "Hight",
                            ME = ME(test$high, data.hight.train$hight),
                            MAE = MAE(test$high, data.hight.train$hight),
                            MSE = MSE(test$high, data.hight.train$hight),
                            MPE = MPE(test$high, data.hight.train$hight),
                            MAPE = MAPE(test$high, data.hight.train$hight))

# Model Low ---------------------------------------------------------------

model.low <- HARForecast(tsagg2min$low, periods = c(1,5,22), nRoll =10,
                          nAhead = n, type = "HAR")

model.low.train <- HARForecast(tsagg2min.train$low, periods = c(1,5,22), nRoll =10,
                          nAhead = n, type = "HAR")

data.low <- data.frame(model.low@forecast)
data.low.train <- data.frame(model.low.train@forecast)

tmp <- ncol(data.low)
tem <- sample(tmp,1)

data.low <- data.low %>%
  mutate(
    t = seq(1, nrow(data.low), 1),
    low = data.low[,tem]
  )

tmp <- ncol(data.low.train)
tem <- sample(tmp,1)

data.low.train <- data.low.train %>%
  mutate(
    t = seq(1, nrow(data.low.train), 1),
    low = data.low.train[,tem]
  )

data.low.tem <- data.low %>%
  rowwise() %>%
  mutate(
    min.low = min(roll1, roll2, roll3, roll4, roll5, roll6, roll7, roll8,
                  roll9, roll10),
    max.low = max(roll1, roll2, roll3, roll4, roll5, roll6, roll7, roll8,
                  roll9, roll10)
  )

data.low <- data.low %>% select(t, low)
data.low.train <- data.low.train %>% select(t, low)

metricas.low <- data.frame(Variable = "Low",
                          ME = ME(test$low, data.low.train$low),
                          MAE = MAE(test$low, data.low.train$low),
                          MSE = MSE(test$low, data.low.train$low),
                          MPE = MPE(test$low, data.low.train$low),
                          MAPE = MAPE(test$low, data.low.train$low))

# Métricas ----------------------------------------------------------------

metricas <- rbind(metricas.open, metricas.close, metricas.hight, metricas.low)
stargazer(metricas, type = "text", summary = F, title = "Métricas")

# unión -------------------------------------------------------------------

data.forecast.hat <- inner_join(data.close, data.open, by = "t")
data.forecast.hat <- data.forecast.hat %>% inner_join(data.hight, by = "t")
data.forecast.hat <- data.forecast.hat %>% inner_join(data.low, by = "t")

# objeto serie de tiempo --------------------------------------------------

temp <- index(st)
#temp[nrow(st)]

inicio <- as.POSIXct(temp[nrow(st)]) + 120
intervalo <- 2

dates <- seq(from = inicio, by = intervalo*60,
             length.out = nrow(data.forecast.hat))

data.forecast.hat$t <-NULL

st.hat <- xts(data.forecast.hat, order.by = dates)

st.completo <- rbind(st, st.hat)
#autoplot(st.completo)

df.st.completo <- data.frame(st.completo)

# indicadores -------------------------------------------------------------

# Tendencia

## SMA

#cat("SMA")
#close.sma.13 <- SMA(Cl(st.completo), n = 13)
#close.sma.200 <- SMA(Cl(st.completo), n = 200)
#df.st.completo$close.sma.13 <- close.sma.13
#df.st.completo$close.sma.200 <- close.sma.200
#df.st.completo <- fn.signal.SMA(df.st.completo)

## EMA

#cat("EMA")
#close.ema.13 <- EMA(Cl(st.completo), n = 13)
#close.ema.200 <- EMA(Cl(st.completo), n = 200)
#df.st.completo$close.ema.13 <- close.ema.13
#df.st.completo$close.ema.200 <- close.ema.200
#df.st.completo <- fn.signal.EMA(df.st.completo)

## Moving average convergence/divergence (MACD)

#cat("MACD")
#close.MACD.13.25.9 <- MACD(Cl(st.completo), nFast = 13, nSlow = 25,
#                           nSig = 9, percent = FALSE)
#df.st.completo$close.MACD.13.25.9.macd <- close.MACD.13.25.9[,1]
#df.st.completo$close.MACD.13.25.9.signal <- close.MACD.13.25.9[,2]
#df.st.completo <- fn.signal.MACD(df.st.completo)

## Welles Wilder’s Directional Movement Indicator

#cat("ADX")
#adx.13 <- ADX(st.completo[,c("high","low","close")], n = 13)
#df.st.completo$adx.DIp <- adx.13[,1]
#df.st.completo$adx.DIn <- adx.13[,2]
#df.st.completo$adx.DX <- adx.13[,3]
#df.st.completo$adx.ADX <- adx.13[,4]
#df.st.completo <- fn.signal.ADX(df.st.completo)

## Parabolic Stop and Reverse (SAR)

cat("SAR")
sar <- SAR(st.completo[,c("high","low")])
df.st.completo$sar <- sar
df.st.completo <- fn.signal.SAR(df.st.completo, 0.05)

## Triple Smoothed Exponential Oscillator

#cat("TRIX")
#trix  <- TRIX(st.completo[,"close"])
#df.st.completo$TRIX <- trix[,1]
#df.st.completo$TRIX.signal <- trix[,2]
#df.st.completo <- fn.signal.TRIX(df.st.completo)

# Volatividad

## Bollinger band

cat("Bollinger band")
close.bollingerband.20 <- BBands(st.completo$close, n = 20, sd = 2)
df.st.completo$close.bollingerband.dn.20 <- close.bollingerband.20[,1]
df.st.completo$close.bollingerband.mavg.20 <- close.bollingerband.20[,2]
df.st.completo$close.bollingerband.up.20 <- close.bollingerband.20[,3]
df.st.completo$close.bollingerband.pctB.20 <- close.bollingerband.20[,4]

pb <- progress_bar$new(format = "[:bar] :current/:total (:percent)",
                       total = nrow(df.st.completo))
signal.bollingerband <- c()
for (i in 1:length(st.completo$close)) {
  pb$tick(1)
  Sys.sleep(1 / 100)
  signal.bollingerband[i] <- 0
  # venta si close.bollingerband.pctB.20 > 1
  if (isTRUE(df.st.completo$close.bollingerband.pctB.20[i] > 1)) {
    signal.bollingerband[i] <- 0
  } # compra si close.bollingerband.pctB.20 < 0
  else if (isTRUE(df.st.completo$close.bollingerband.pctB.20[i] < 0)) {
    signal.bollingerband[i] <- 1
  } # no hacer nada
  else {
    signal.bollingerband[i] <- -1
  }
}

signal.bollingerband <- reclass(signal.bollingerband, st.completo)
df.st.completo$signal.bollingerband <- signal.bollingerband

## Average True Range

#cat("ATR")
#atr <- ATR(st.completo[,c("high","low","close")], n=13)
#df.st.completo$tr <- atr[,1]
#df.st.completo$atr <- atr[,2]
#df.st.completo$atr.trueHigh <- atr[,3]
#df.st.completo$atr.trueLow <- atr[,4]

# Momentum

## Momentum

#cat("Momentum")
#close.momentum.5 <- momentum(st.completo$close, n = 5)
#df.st.completo$close.momentum.5 <- close.momentum.5
#df.st.completo <- fn.signal.Momentum(df.st.completo)

## Relative Strength index (RSI)

#cat("RSI")
#close.RSI.25 <- RSI(st.completo$close, SMA, n = 25)
#df.st.completo$close.RSI.25 <- close.RSI.25
#
#df.st.completo <- df.st.completo %>%
#  mutate(
#    zona.RSI = case_when(
#      close.RSI.25 < 30 ~ "sobreventa",
#      close.RSI.25 > 70 ~ "sobrecompra",
#      TRUE ~ "sin_tendencia"
#    ),
#    tipo.RSI = case_when(
#      close.RSI.25 < 10 ~ "lenta",
#      (close.RSI.25 >= 10 & close.RSI.25 < 20) ~ "normal",
#      (close.RSI.25 >= 20 & close.RSI.25 < 30) ~ "rapida",
#      (close.RSI.25 >= 70 & close.RSI.25 < 80) ~ "rapida",
#      (close.RSI.25 >= 80 & close.RSI.25 < 90) ~ "normal",
#      close.RSI.25 >= 90 ~ "lenta"
#    )
#  )

#signal.RSI <- c()
#for (i in 1:length(st.completo$close)) {
#  signal.RSI[i] <- -1
#  if (isTRUE(df.st.completo$close.RSI.25[i] < 30)) {
#    # compra si signal.RSI.25 < 30
#    signal.RSI[i] <- 1
#  }
#  else if (isTRUE(df.st.completo$close.RSI.25[i] < 70)) {
#    # no hacer nada
#    signal.RSI[i] <- -1
#  }
#  else {
#    # venta si signal.RSI.25 > 70
#    signal.RSI[i] <- 0
#  }
#}

#signal.RSI <- reclass(signal.RSI, st.completo)
#df.st.completo$signal.RSI <- signal.RSI

## William’s %R

#cat("W")
#w <- WPR(st.completo[,c("high","low","close")], n = 13)
#df.st.completo$w <- w
#
#df.st.completo <- df.st.completo %>%
#  mutate(
#    signal.w = case_when(
#      w >= 0 & w < 0.2 ~ "sobrecompra",
#      w >= 0.8 & w < 1 ~ "sobreventa"
#    )
#  )

## Commodity Channel Index (CCI)

#cat("CCI")
#cci <- CCI(st.completo[,c("high","low","close")])
#df.st.completo$cci <- cci

## Rate of Change (ROC)

#cat("ROC")
#close.ROC.13 <- ROC(st.completo$close, type = "discrete", n = 13)
#close.ROC.25 <- ROC(st.completo$close, type = "discrete", n = 25)
#df.st.completo$close.ROC.13 <- close.ROC.13
#df.st.completo$close.ROC.25 <- close.ROC.25


# extracción de pronóstico con indicadores --------------------------------

df.tem <- df.st.completo %>% filter(index(st.completo) >= inicio)
df.tem$min.close <- data.close.tem$min.close
df.tem$max.close <- data.close.tem$max.close
df.tem$min.open <- data.open.tem$min.open
df.tem$max.open <- data.open.tem$max.open
df.tem$min.hight <- data.hight.tem$min.hight
df.tem$max.hight <- data.hight.tem$max.hight
df.tem$min.low <- data.low.tem$min.low
df.tem$max.low <- data.low.tem$max.low

xtem <- head.cast_df(df.tem, n = nrow(df.tem))

write.csv2(xtem, file = paste0(dir.csv, "/pronostico_",
                                 format(Sys.time(), "%Y_%m_%d_%H_%M_%S"),
                                 ".csv"),
           fileEncoding = "UTF-8")

st.tem <- reclass(df.st.completo, st.completo)

## gráficas

#signal.SMA <- df.st.completo$signal.SMA
#signal.SMA <- reclass(signal.SMA, st.completo)

#signal.EMA <- df.st.completo$signal.EMA
#signal.EMA <- reclass(signal.EMA, st.completo)

#signal.MACD <- df.st.completo$signal.MACD.signal
#signal.MACD <- reclass(signal.MACD, st.completo)

#signal.ADX <- df.st.completo$signal.ADX
#signal.ADX <- reclass(signal.ADX, st.completo)

signal.SAR <- df.st.completo$signal.SAR
signal.SAR <- reclass(signal.SAR, st.completo)

#signal.trix <- df.st.completo$signal.TRIX.signal
#signal.trix <- reclass(signal.trix, st.completo)

signal.bollingerband <- df.st.completo$signal.bollingerband
signal.bollingerband <- reclass(signal.bollingerband, st.completo)

#signal.momentum.5 <- df.st.completo$signal.momentum.5
#signal.momentum.5 <- reclass(signal.momentum.5, st.completo)

#signal.RSI <- df.st.completo$signal.RSI
#signal.RSI <- reclass(signal.RSI, st.completo)

pdf(file = paste0(dir.img, "/pronostico_",
                  format(Sys.time(), "%Y_%m_%d_%H_%M_%S"),
                  ".pdf"),
    width = 16, height = 9)

#autoplot(st.hat$close) + ggtitle("Close")
#autoplot(st.hat$close) + ggtitle("Open")
#autoplot(st.hat$close) + ggtitle("Hight")
#autoplot(st.hat$close) + ggtitle("Low")

#chartSeries(Cl(st.completo),
#            type = "line",
#            theme="white",
#            subset = "last 30",
#            TA = "addSMA(n = 13, on = 1, col = 'coral');
#            addSMA(n = 200, on = 1, col = 'blue');
#            addTA(signal.SMA, type = 'S', col = 'red')"
#)

#chartSeries(Cl(st.completo),
#            type = "line",
#            theme="white",
#            subset = "last 30",
#            TA = "addEMA(n = 13, on = 1, col = 'coral');
#            addEMA(n = 200, on = 1, col = 'blue');
#            addTA(signal.EMA, type = 'S', col = 'red')"
#)

#chartSeries(Cl(st.completo),
#            type = "line",
#            theme="white",
#            subset = "last 30",
#            TA = "addMACD(fast = 13, slow = 25, signal = 9, type = 'EMA');
#            addTA(signal.MACD, type = 'S', col = 'red')"
#)

#chartSeries(st.completo,
#            type = "line",
#            #theme="white",
#            subset = "last 30",
#            TA = "addSAR(col = 'blue');
#            addTA(signal.SAR, type = 'S', col = 'red')"
#)

#chartSeries(Cl(st.completo),
#            type = "line",
#            theme="white",
#            subset = "last 30",
#            TA = "addTRIX();
#            addTA(signal.trix, type = 'S', col = 'red')"
#)

#chartSeries(Cl(st.completo),
#            type = "line",
#            #theme="white",
#            subset = "last 30",
#            TA = "addBBands(n = 20, sd = 2);
#            addTA(signal.bollingerband, type = 'S', col = 'red')"
#)

#chartSeries(st.completo,
#            type = "line",
#            theme="white",
#            subset = "last 30",
#            TA = "addATR(n = 13);"
#)
#title("ATR")

#chartSeries(Cl(st.completo),
#            type = "line",
#            theme="white",
#            subset = "last 30",
#            TA = "addMomentum(n = 5);
#            addTA(signal.momentum.5, type = 'S', col = 'red');
#            addRSI(n = 25);
#            addTA(signal.RSI, type = 'S', col = 'red')"
#)

#chartSeries(st.completo,
#            type = "line",
#            theme="white",
#            subset = "last 30",
#            TA = "addCCI()"
#)

#chartSeries(Cl(st.completo),
#            type = "line",
#            theme="white",
#            subset = "last 30",
#            TA = "addROC(n = 13);addROC(n = 25)"
#)
#title("ROC n = 13 y ROC = 25")

chartSeries(st.completo,
            type = "line",
            #theme="white",
            subset = "last 30",
            TA = "addBBands(n = 20, sd = 2);
            addTA(signal.bollingerband, type = 'S', col = 'red');
            addSAR(col = 'magenta');
            addTA(signal.SAR, type = 'S', col = 'orange')"
)

dev.off()
