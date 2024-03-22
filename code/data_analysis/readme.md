fototoestel: Spiegelreflex Nikon D3300 
fotos      : 8 typen dakpannen , total ca 1000 fotos - kiem onderzoek circulare Dakpannen (Proof of concept)
type fotos : volledige dakpannen, verschillende hoeken, verschillende opstellingen, verschilldende achtergronden 

# Order of preprocessors

1. extension_converter.py: This converts all image formats to .PNG. this preserves the details better and causes the image to not lose detail whenever it's processed.
2. data_analysis_hierarchy.py: resizes all images to *0.25 with a res of 3000 or above in either width or height for a smaller dataset.
3. b_o_splitter.py: Places all topsides and bottomsides of the rooftile in folder "b" (topside) or "o" (bottomside)
4. grayscale_converter.py: Does the following:
    * Converts all images within dataset to grayscale.
    * Picks 3 random images and shows the colorchannels in histogram
5. normalization_converter.py: Does the following:
    * Normalizes all images within dataset to remove noise and glare from camera.
    * Picks 3 random images and shows the colorchannels in histogram
6. clahe_converter_small.py: **Don't use clahe_converter.py as it puts all images in 1 array which eats RAM like cake** Does the following:
    * Applies CLAHE (Contract Limited Adaptive Histogram Equalization) to all images within dataset.
    * Picks 3 random images and shows the colorchannels in histogram
7. stratified_splitter.py: Stratified dataset splitting test and train (preserve amount of images per rooftile)
8. **APPLY ONLY ON TRAIN**: Augmentation.py: Makes a copy of the inputted image, one for each augmentation effect (3 effects)
9. resize_all_keep_ratio.py: Converts images to 640 by 640 by adding a border around each image depending on the original aspect ratio