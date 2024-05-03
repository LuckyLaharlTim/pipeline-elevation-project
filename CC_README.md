Create a python cloud function (image_imports) that does the following:
    Import shapefile of Texas pipline locations.
    Extract aerial imagery clipped to locations (~1km square around each segment).
    Use USDA aerial imagery where available, otherwise use SKYSAT ortho imagery.
    Push extracted imagery to cloud storage for modeling.