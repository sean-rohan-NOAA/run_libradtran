# Convert lunar irradiance to separate files


lunar_irrad <- read.csv(file = here::here("data", "lunar_irrad_1AU_MeanME_300_750.csv"))
lunar_irrad$wavelength <- lunar_irrad$wavelength * 1000
lunar_irrad$phase <- sort(rep(0:180, 451), decreasing = TRUE)

for(ii in 0:(nrow(lunar_irrad)/451-1)) {

  file1 <- file(here::here("data", paste0("lunar_irrad", ii)), "w")
  
  cat("# Top-of-atmosphere (TOA) lunar irradiance from Miller and Turner (2009)\n", file = file1)
  cat("# First column wavelength (nm), second column TOA irradiance", file = file1)
  cat(paste0("# Lunar phase angle: ", ii, "\n"), file = file1)
  cat("# Irradiance units: mW/m^2-micrometer\n\n", file = file1)
  write.table(x = lunar_irrad[lunar_irrad$phase == ii, 1:2],
              file = file1,
              col.names = FALSE, 
              row.names = FALSE)
  
  close(file1)
  
  
  file2 <- file(here::here("data", paste0("lunar_irrad", ii, "_10nm")), "w")
  
  cat("# Top-of-atmosphere (TOA) lunar irradiance from Miller and Turner (2009) by 10 nm increments\n", file = file2)
  cat("# First column wavelength (nm), second column TOA irradiance", file = file2)
  cat(paste0("# Phase angle = ", ii, "\n"), file = file2)
  cat("# Units = mW/m^2-micrometer\n\n", file = file2)
  write.table(x = lunar_irrad[lunar_irrad$phase == ii & lunar_irrad$wavelength %% 10 == 0, 1:2],
              file = file2,
              col.names = FALSE, 
              row.names = FALSE)
  
  close(file2)
  
}


# Verify that phases are partitioned correctly
lunar_irrad |>
  dplyr::group_by(phase) |>
  dplyr::summarise(total_E = sum(E)) |>
ggplot() +
  geom_path(mapping = aes(x = phase, y = total_E))
