#!/usr/bin/env python
# coding: utf-8

# # Getting Data from Google Earth Engine

# In[5]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import geopandas as gpd
import matplotlib.pyplot as plt
import ee
import folium
import geemap.core as geemap
import geehydro
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.svm import LinearSVC
# from sklearn import svm, metrics, ensemble
# from keras.models import Sequential, Model
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Activation, Dropout, Flatten, MaxPool2D
# from tensorflow.keras.layers import BatchNormalization
# from tensorflow.keras.utils import plot_model

# from tensorflow.keras.optimizers import Adam
# from keras.callbacks import LearningRateScheduler
# from keras.regularizers import l2, l1
import math
import requests
import os
import skimage



# ### Authenticate and Initialize Project

# In[6]:


try:
## should be a one-time run
    ee.Authenticate()
    ee.Initialize(project="pipeline-elevation-project")
except:
    ee.Initialize(project="pipeline-elevation-project")


# ### Call Landsat Data

# In[3]:


lstColl = ee.ImageCollection("LANDSAT/LC09/C02/T1")
i_date = '2022-05-01'
f_date = '2022-06-30'
lst = lstColl.select('B1','B2','B3','B4').filterDate(i_date,f_date)


# In[4]:


img = lst.toList(10).get(1)
#display(img)


# ##### get known pipeline locations for coordinates

# * [tx_ngpipeline data](https://drive.google.com/drive/u/0/folders/1kSXfSin5b7wr6S_LMrRoc4sobY-UC-Qq)

# In[9]:


zipPath = "C:/Users/mclif/Downloads/"
ngPipePath = zipPath+"TX_NGpipe/NaturalGas_Pipelines_TX.shp"
ngPipes = gpd.read_file(ngPipePath)
MercNGPipes = ngPipes.to_crs(epsg=4326)
MercNGPipes["centroids"] = MercNGPipes.geometry.centroid
MercNGPipes["beg"] = MercNGPipes.geometry.boundary.centroid
# MercNGPipes["end"] = MercNGPipes.geometry.boundary
# type(ngPipes.geometry)


# In[10]:


print(len(MercNGPipes))
MercNGPipes.centroids


# In[11]:


# ngPipes.centroids
i = 2500
lat1 = MercNGPipes.centroids[i:i+1].squeeze().y
lon1 = MercNGPipes.centroids[i:i+1].squeeze().x
bbox = MercNGPipes.geometry[i:i+1].squeeze().boundary # attempt



print(lat1,lon1)
print(type(bbox))

# print(ngPipes.beg[:1].squeeze())


# ##### view satellite image

# In[12]:


Map = folium.Map()
Map.setOptions()

Map.setCenter(lon1,lat1) # coordinates of poi
Map.addLayer(ee.Image(img), {}, 'default color composite')

Map.setControlVisibility()
Map


#  ## Try [aerial photography](https://developers.google.com/earth-engine/datasets/tags/highres)

# In[13]:


aerColl = ee.ImageCollection("USDA/NAIP/DOQQ")
i_date = '2022-05-01'
f_date = '2022-06-30'
alst = aerColl.select('R','G','B','N').filterDate(i_date,f_date)

aimg = alst.toList(10).get(1)
#display(aimg)


# In[14]:


# Map = folium.Map()
# Map.setOptions()

# Map.setCenter(lon1,lat1) # coordinates of poi
Map.addLayer(ee.Image(aimg), {}, 'default color composite')

Map.setControlVisibility()
Map


# ## Export an image

# [documentation on exporting image function](https://developers.google.com/earth-engine/apidocs/export-image-tocloudstorage) (with links to drive, etc.)

# In[ ]:


task = ee.batch.Export.image.toCloudStorage(ee.Image(img),
                            description="testLandSatExport",  # optional
                            # ^ put desired name for the task & file in cloud storage
                            bucket = "test_export_bucket0"  # optional
                            # ^ for actual storages, use 'gee_image_exports'

                            )

task.start()


# This runs quickly, but the actual task takes a long time to finish.<br><br>Clipping the export with `region` would be helpful. *--beginnings to this idea can be found with bbox above & [this link](https://gis.stackexchange.com/questions/439924/convert-local-file-shp-csv-into-earth-engine-ee-object)--*
