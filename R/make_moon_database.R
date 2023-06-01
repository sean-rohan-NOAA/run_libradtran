library(DBI)


moon_db <- DBI::dbConnect(RSQLite::SQLite(), "output", "moon_database.sqlite")


moon_files <- list.files(here::here("output", "moon"), full.names = TRUE)

out <- data.frame(wavelength = numeric(length = 0L), 
                  irradiance = numeric(length = 0L), 
                  zenith_angle = numeric(length = 0L), 
                  moon_phase = numeric(length = 0L))

for(ii in 1:length(moon_files)) {

  base_name <- basename(moon_files[ii])
  dat <- read.table(moon_files[ii])[,c(1,3)]
  names(dat) <- c("wavelength", "irradiance")
  dat$doy <- as.numeric(strsplit(base_name, "_")[[1]][2])
  dat$zenith_angle <- as.numeric(strsplit(base_name, "_")[[1]][3])
  dat$moon_phase <- as.numeric(strsplit(strsplit(base_name, "_")[[1]][4],
                                        "[.]")[[1]][1])
  
  if(ii > 1) {
    append <- TRUE
  } else {
    append <- FALSE
  }
  
  DBI::dbWriteTable(conn = moon_db, 
                    name = "moon", 
                    value = dat, 
                    append = append)
  
}

DBI::dbListTables()

test <- DBI::dbReadTable(moon_db, name = "moon") |>
  dplyr::group_by(zenith_angle, doy) |>
  dplyr::summarise(total_irradiance = sum(irradiance))



library(ggplot2)

ggplot() +
  geom_path(data = test,
            mapping = aes(x = zenith_angle,
                          y = total_irradiance, 
                          color = factor(doy))) +
  scale_y_log10()


ggplot() +
  geom_path(data = test |>
              dplyr::filter(zenith_angle > 100),
            mapping = aes(x = zenith_angle,
                          y = total_irradiance, 
                          color = factor(doy))) +
  scale_y_log10()




