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