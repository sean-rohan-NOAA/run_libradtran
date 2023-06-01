library(DBI)

sun_db <- DBI::dbConnect(RSQLite::SQLite(), here::here("output", "sun_database.sqlite"))

sun_files <- list.files(here::here("output", "sun"), full.names = TRUE)

out <- data.frame(wavelength = numeric(length = 0L), 
                  irradiance = numeric(length = 0L), 
                  zenith_angle = numeric(length = 0L), 
                  sun_phase = numeric(length = 0L))

bad_files <- c()

for(ii in 1:length(sun_files)) {
  
  base_name <- basename(sun_files[ii])
  dat <- try(read.table(sun_files[ii])[,c(1,3)], silent = TRUE)
  
  if(class(dat) == "try-error") {
    bad_files <- c(bad_files, sun_files[ii])
    next
  }
  
  names(dat) <- c("wavelength", "irradiance")
  dat$doy <- as.numeric(strsplit(base_name, "_")[[1]][2])
  dat$zenith_angle <- 
    as.numeric(
      strsplit(
        strsplit(base_name, "_")[[1]][3],
        "[.]")[[1]][1]
    )
  
  if(ii > 1) {
    append <- TRUE
  } else {
    append <- FALSE
  }
  
  DBI::dbWriteTable(conn = sun_db, 
                    name = "sun", 
                    value = dat, 
                    append = append)
  
}

sink(file = here::here("output", "bad_files.txt"))
cat(paste(bad_files, collapse = "\n"))
