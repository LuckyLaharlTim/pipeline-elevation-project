# <ins>Transportation Pipeline Elevation Predictor</ins>

This project aims to use satellite images in Google Earth Engine as input for a built neural network model identifying natural gas & CO2 pipelines as above or below ground. Given the desire to retrieve values for a large area and concern of finer resolution, satellite images are chosen over aerial photography and detail a maximum of 1 square kilometer. The workflow for retrieving images and obtaining estimates from the model will be put into a Google Cloud workflow with data appended to the initial line feature shapefiles.

---------------------------

## Methodology - Overview
1. **<ins>Create a python cloud function (image_imports) that does the following</ins>**:
   1. *Import shapefile of Texas pipline locations.*
        - preferably from Cloud Storage 
   2. *Extract aerial imagery clipped to locations for each record*
        - (~1km^2 square around each segment).
        - Use USDA aerial imagery where available, otherwise use SKYSAT ortho imagery.
    3. *Export extracted imagery to cloud storage for modeling.*
2. **<ins>View sample of images and label observed aboveground pipelines</ins>**
    - Ideally, a subset of 200/300 are labeled for use as a training set
3. **<ins>Create model architecture</ins>**
   1. *Consists of network including convolutional layers*
        - examples of architectures like U-Net [here](https://joshting.medium.com/satellite-imagery-segmentation-with-convolutional-neural-networks-f9254de3b907)
4. **<ins>Fit completed model with 500+ sample dataset</ins>**
5. **<ins>Output binary prediction & model test accuracy details as respective</ins>**...
   1. enhanced shapefile
   2. auto-formatted documentation of model evaluation

----------------------------

Input: Zip Folder of pipline shapefile
<br>Output: Zip folder of pipeline shapefile with added `Aboveground` column