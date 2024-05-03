# upload texas images to gcloud
import geopandas as gpd
import ee
import folium
import geemap.core as geemap
import geehydro
from google.cloud import storage
import os
from zipfile import ZipFile
import functions_framework as ff

DEBUG = True


def mapImg(img, lon, lat):
    Map = folium.Map()
    Map.setOptions()

    Map.setCenter(lon, lat)  # coordinates of poi
    # Map.addLayer(tx, {'color': '#FECA1E', 'fillColor': '#4c4cff'})
    Map.addLayer(img, {}, 'default color composite')

    Map.setControlVisibility()
    return Map

def getSHP():
    
    destFile = "./data/TX_NGPipe.zip"
    if not(os.path.exists(destFile)):
        os.makedirs("./data/",exist_ok=True)

    blob = storage.Client(
        project="pipeline-elevation-project").bucket(
        "pipeline_data_bucket").blob("raw/TX_NGPipe.zip")
    blob.download_to_filename(destFile)

    with ZipFile(destFile, 'r') as zipped:
        zipped.extractall("./data")
    

@ff.http
def main(request):
    try:
        # should be a one-time run
        ee.Authenticate()
        ee.Initialize(project="pipeline-elevation-project")
    except:
        ee.Initialize(project="pipeline-elevation-project")

    getSHP()

    zipPath = "./data/"
    ngPipePath = zipPath+"TX_NGPipe/NaturalGas_Pipelines_TX.shp"
    ngPipes = gpd.read_file(ngPipePath)
    MercNGPipes = ngPipes.to_crs(epsg=4326)
    MercNGPipes["centroids"] = MercNGPipes.geometry.centroid.to_crs(epsg=4326)
    MercNGPipes["beg"] = MercNGPipes.geometry.boundary.centroid.to_crs(epsg=4326)

    metersPerUnit = (1.11/0.00001)
    FHmeters = 500/metersPerUnit
    aerColl = ee.ImageCollection("USDA/NAIP/DOQQ")
    orthColl = ee.ImageCollection("SKYSAT/GEN-A/PUBLIC/ORTHO/RGB")
    i_date = '2022-05-01'
    f_date = '2022-06-30'
    retrievedPics = 0
    # TX rectangle bounds
    # tx = ee.Geometry.Rectangle(-106.64719063660635,25.840437651866516,-93.5175532104321,36.50050935248352)


    for i in range(len(MercNGPipes)):
            
        # using new shapefile, so more 
        lat = MercNGPipes.centroids[i:i+1].squeeze().y
        lon = MercNGPipes.centroids[i:i+1].squeeze().x
        # bbox args: west, south, east, north
        bbox = ee.Geometry.BBox(lon-FHmeters, lat-FHmeters, lon+FHmeters, 
                                lat+FHmeters)

        # get image(s) within box
        aList = aerColl.select('R', 'G', 'B', 'N').filterDate(i_date, f_date).filterBounds(bbox)
        oList = orthColl.select('R', 'G', 'B').filterDate(i_date, f_date).filterBounds(bbox)
        # need to check if list is empty
        # use .filterBounds(tx) if later issues

        aImg = ee.Image(aList.toList(100).get(1))
        try:
            mapImg(aImg, lon, lat)
            ## Export section
            task = ee.batch.Export.image.toCloudStorage(aImg,
                                    description=f"USDA_aerials/pipeline{i}",  # put part of pipeline here too
                                    # ^ put desired name for the task & file in cloud storage
                                    bucket = "gee_image_exports",  # should be gee_image_exports
                                    region=bbox,  # I wonder if filtering by box first works too
                                    #maxPixels=1500000000  
                                    )
            task.start()
            ##### to view proper map
            print(f"Aerial Ag {i}")
            retrievedPics += 1
        except:
            if DEBUG:
                print(f"skipped agriculture pipe {i}")
            pass

        oImg = ee.Image(oList.toList(100).get(1))
        try:
            mapImg(oImg, lon, lat)
            ## Export section
            task = ee.batch.Export.image.toCloudStorage(oImg,
                                    description=f"SKYSAT_ortho/pipeline{i}",  # put part of pipeline here too
                                    # ^ put desired name for the task & file in cloud storage
                                    bucket = "gee_image_exports",  # should be gee_image_exports
                                    region=bbox,  # I wonder if filtering by box first works too
                                    #maxPixels=1500000000  
                                    )
            task.start()
            ##### to view proper map
            print(f"Aerial Orthro {i}")
            retrievedPics += 1
            continue
        except:
            if DEBUG:
                print(f"skipped ortho pipe {i}")
            pass

    return f"Successfully retrieved {retrievedPics} images out of {len(MercNGPipes)} total records."

    if __name__ == "__main__":
        main("sample")