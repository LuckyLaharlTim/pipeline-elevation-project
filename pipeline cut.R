library(sf)
library(ggplot2)
library(tidyverse)
library(mapview)
library(tigris)


# Load the data
pl <- st_read("/Users/annaduan/Downloads/TX_NGPipe/NaturalGas_Pipelines_TX.shp") %>%
  st_transform("EPSG:3081") %>%
  group_by(TYPEPIPE, Operator, Status) %>%
  summarize(length = sum(Shape_Leng, na.rm = T),
            geometry = st_union(geometry))

# tx 
texas <- states(year = 2020) %>% filter(NAME == "Texas") %>%
  st_transform("EPSG:3081")

# make grid
grid <- st_make_grid(texas, square = F, cellsize = 3280.84) %>%
  st_as_sf() %>%
  st_transform("EPSG:3081")

pl_grid <- pl %>%
  st_intersection(grid)

pl_grid <- pl_grid %>%
  mutate(unique_id = row_number())

st_write(pl_grid, "pl_segments.geojson", driver = "GeoJSON")
