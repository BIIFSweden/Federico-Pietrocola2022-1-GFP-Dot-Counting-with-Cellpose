# Federico-Pietrocola2022-1-GFP-Dot-Counting-with-Cellpose

#### This jupyter notebook utilizes the cellpose segmentation algorithm to segment both the cytoplasm and nuclei of the microscopy images. The fluorescent dots within the detected cells (exluding their nuclei) are segmented using a white tophat filter and manual thresholding. The script then counts the fluorescent dots within the detected cells and will ouput a "Results" folder containing images of the segmentations and an excel file which contains the dot counts in all segmented cells within each image.

#### The user should run as following:


1. First run the first two  jupyter-cells to import the necessary python modules and define the custom functions.
2. After this, the user should enter the filepath of the local directory containing the images to be analyzed in the "User Inputs" jupyter-cell. Additional parameters for fine tuning of the cytoplasm, nuclei and fluorescent dot segmentation shold be adjusted in this cell as well.
3. Run the "Run Program" jupyter-cell, which will loop through and anaylze all images in the given filepath.
4. If needed, tune segmentation parameters and re-run the "User Inputs" and "Run Program" jupyter-cells.
