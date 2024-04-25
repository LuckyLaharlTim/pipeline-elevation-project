# upload texas images to gcloud

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import geopandas as gpd
import matplotlib.pyplot as plt
import ee
import folium
import geemap.core as geemap
import geehydro
import math
import requests
import os
import skimage
import functions_framework as ff


@ff.http
def main(request):
    try:
    ## should be a one-time run
        ee.Authenticate()
        ee.Initialize(project="pipeline-elevation-project")
    except:
        ee.Initialize(project="pipeline-elevation-project")

    lstColl = ee.ImageCollection("LANDSAT/LC09/C02/T1")
    i_date = '2022-05-01'
    f_date = '2022-06-30'
    lst = lstColl.select('B1','B2','B3','B4').filterDate(i_date,f_date)

    img = lst.toList(10).get(1)

    zipPath = "~/Downloads/"
    ngPipePath = zipPath+"TX_NGPipe/NaturalGas_Pipelines_TX.shp"
    ngPipes = gpd.read_file(ngPipePath)
    MercNGPipes = ngPipes.to_crs(epsg=4326)
    MercNGPipes["centroids"] = MercNGPipes.geometry.centroid
    MercNGPipes["beg"] = MercNGPipes.geometry.boundary.centroid

    i = 2500
    lat1 = MercNGPipes.centroids[i:i+1].squeeze().y
    lon1 = MercNGPipes.centroids[i:i+1].squeeze().x
    bbox = MercNGPipes.geometry[i:i+1].squeeze().boundary # attempt

    task = ee.batch.Export.image.toCloudStorage(ee.Image(img),
                                description="testLandSatExport",  
                                bucket = "test_export_bucket0"  
                                )
    task.start()

    if __name__=="__main__":
        main("sample")