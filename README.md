# LC3+ GFP dot counting using cellpose

The image analysis pipeline written in this jupyter notebook utilizes the cellpose segmentation algorithm [https://github.com/MouseLand/cellpose] to segment the cells contained within 2-channel .nd2 microscopy images. For the purpose of this project, it is unimportant to segment contacting neighbouring nuclei, hence simple global intensity thresholding is used to segment the nuclei of the cells. This approach is possible due to the high SNR of the nuclei channel and reduces the total computation time (by avoiding having to use cellpose for nuclei segmentation) enabling faster high-throughput analysis.

The fluorescent dots within the detected cells (exluding their nuclei) are segmented using a white tophat filter, manual thresholding and minimum area criteria. The script then counts the fluorescent dots within the detected cells and will ouput a "Results" folder containing images of the segmentations and an excel file which contains the dot counts in all segmented cells within each image.

#### The user should run as following:



1. First run the first two  jupyter-cells to import the necessary python modules and define the custom functions.
2. After this, the user should enter the filepath of the local directory containing the images to be analyzed in the "User Inputs" jupyter-cell. Additional parameters for fine tuning of the cytoplasm, nuclei and fluorescent dot segmentation shold be adjusted in this cell as well.
3. Run the "Run Program" jupyter-cell, which will loop through and anaylze all images in the given filepath.
4. If needed, tune segmentation parameters and re-run the "User Inputs" and "Run Program" jupyter-cells.
