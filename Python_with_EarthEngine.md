
**project**: pipeline-elevation-project
- use this name in `ee.Initialize()`
- access the project in your browser [here](https://code.earthengine.google.com/?accept_repo=users/timoliver200/satellite_data)

## Python Earth Engine Resources
[Using Earth Engine in Python](https://developers.google.com/earth-engine/tutorials/community/intro-to-python-api)
- mainly for grabbing image collections or data quickly
- we might need to use Google Colab

[Exporting Data from Earth Engine](https://developers.google.com/earth-engine/guides/exporting_images#colab-python)
- gives examples of export to Cloud Storage (which is preferred)
- Remote Sensing Project might prefer to Drive
- stored images will be used as ML model inputs

[Using Earth Engine in Python Notebooks](https://github.com/giswqs/earthengine-py-notebooks/blob/master/Image/image_visualization.ipynb)

## Note on Javascript

Should the view of Images be Difficult in Python, access the [Code Editor](code.earthengine.google.com/?project=pipeline-elevation-project) and perform data exploration in Javascript.<br>
***Actual public maps will use exported data clipped to the extent of our Area(s) of Interest***

## Earth Engine Data Catalog Resources
[USGS 3DEP 10m National Map Seamless Data (can also ingest 1 m)](https://developers.google.com/earth-engine/datasets/catalog/USGS_3DEP_10m)

[Aerial Imagery Catalog](https://developers.google.com/earth-engine/datasets/tags/highres)

[LandSat Catalog (expect LandSat 9 Raw Images)](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1)