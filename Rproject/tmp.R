options(scipen = 100, digits = 4, encoding = "UTF-8")


# Rutas -------------------------------------------------------------------


usuario <- "Kevin"

if (usuario == "Kevin") {
  source(paste0("D:/SimulAva/Rproject", "/01Direcciones.R"), echo = TRUE)
} else if (usuario == "Esteban"){
  source(paste0("G:/Mi unidad/Semestre actual/trading/entregable/developer/R",
                "/01Direcciones.R"),
         echo = TRUE)
} else {
  print("Usuario no identificado")
}


# Libraries ---------------------------------------------------------------


source(paste0(dir.root, "/02Librerias.R"), echo=FALSE)



# Datos -------------------------------------------------------------------

datos <- c(23.39, 6.12, 16.35, 20.41, 9.67, 22.57, 5.37, 18.58,
        18.24, 15.05, 7.62, 65.06, 33.48, 16.38, 18.23, 14.43,
        4.03, 23.61, 22.69, 5.73, 17.61, 40.39, 21.55, 26.42,
        11.7, 18.83, 13.86, 28.83, 21.8, 34.58, 20.33, 18.25,
        23.7, 45.54, 28.22, 10.71, 18.6, 19.51, 13.01, 34.86,
        18.37, 24.45, 15.67, 17.12, 65.23, 20.3, 5.64, 15.07,
        15.46, 16.05, 16.41, 6.49, 16.93, 17.88, 18.55,
        15.3, 14.73, 11.04, 10.78, 5.44)


# Histograma --------------------------------------------------------------

# opción 1
hist(datos)
# opción 2
ggplot(NULL, aes(x = datos)) +
  geom_histogram(binwidth = 7) +
  labs(title = 'Histograma', x = 'datos', y = 'Frecuencia')
# opción 3
qplot(datos, binwidth=7)


# Boxplot -----------------------------------------------------------------

boxplot(datos)

ggplot(NULL, aes(x = datos)) +
  geom_boxplot()
