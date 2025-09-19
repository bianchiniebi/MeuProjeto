#install.packages("jsonlite")
#library(jsonlite) 
#rodou a primeira vez para instalar e chamar a biblioteca que iremos usar

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {stop("Uso correto: Rscript clima.R \"Nome da cidade\"")}

cidade <- args[1]

geo <- jsonlite::fromJSON(
  paste0("https://geocoding-api.open-meteo.com/v1/search?name=", 
         URLencode(cidade), "&count=1&language=pt&format=json"))

if (length(geo$results) == 0) stop("Cidade não encontrada!")

lat <- geo$results$latitude[1]
lon <- geo$results$longitude[1]
nome_cidade <- geo$results$name[1]
pais <- geo$results$country[1]

clima <- jsonlite::fromJSON(paste0("https://api.open-meteo.com/v1/forecast?latitude=", 
                            lat,"&longitude=", lon, "&current_weather=true"))$current_weather

cat("\nResultados da consulta:\n")
cat("Cidade:", nome_cidade, "-", pais, "\n")
cat("Temperatura:", clima$temperature, "°C\n")
cat("Vento:", clima$windspeed, "m/s\n")
cat("Direção do vento:", clima$winddirection, "°\n")
cat("Hora da medição:", clima$time, "\n")

