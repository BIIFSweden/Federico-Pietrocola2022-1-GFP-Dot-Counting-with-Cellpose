# LC3+ GFP dot counting using cellpose

# Project Overview
This python script utilizes the cellpose segmentation algorithm [https://github.com/MouseLand/cellpose] to segment the cells contained within 2-channel .nd2 fluorescent microscopy images. For the purpose of this project, it is unimportant to segment contacting neighbouring nuclei, hence simple global intensity thresholding is used to segment the nuclei of the cells. This approach is possible due to the high SNR of the nuclei channel and reduces the total computation time (by avoiding having to use cellpose for nuclei segmentation) enabling faster high-throughput analysis. If there are nuclei segmentation issues, it is recommended to set the method = 'CELLPOSE' described in the USER INPUTS section later in this document.

The fluorescent dots within the detected cells (exluding their nuclei) are segmented using a white tophat filter, manual thresholding and minimum area criteria. The script then counts the fluorescent dots within the detected cells and will ouput a "Results" folder containing images of the segmentations and an excel file which contains the dot counts in all segmented cells within each image.

![results-0002](https://user-images.githubusercontent.com/43760657/152824338-b6514bb1-f37f-41a7-8045-54970440e927.jpeg)

# Installation

1. Download Anaconda if this is not already installed.
2. Download the Git repository for this project.
   ```bash
   git clone https://github.com/BIIFSweden/LC3-GFP-Counting
   cd LC3-GFP-Counting
   ```
4. Create and activate a conda virtual environment (in this example it is named dot_counting) to isolate the project's environment.
   ```bash
   conda create --name dot_counting python=3.9
   ```
5. Download the necessary packages the command below:
  
   ```bash
   pip install -e .
   ``` 
7. Finished

# Run Program
1. In the terminal/command prompt, activate the conda environment for this project.
   ```bash
   conda activate dot_counting
   ```
3. Run the program from the command line using:
   ```bash
   python src/run_analysis.py
   ```
3. This will open a user interface. Enter the directory containing the image(s) or folders of images to be analyzed and tune the segmentation parameters.

4. Press "Run" to start the analysis

<p align="center">
<img width="350" alt="Screenshot 2023-10-06 at 13 14 37" src="https://github.com/BIIFSweden/LC3-GFP-Counting/assets/43760657/b7dd471b-ad11-4cdf-b514-7d64ee4255e2">
</p>

# Interpreting the results

After the program is finished running, a LC3counts.xlsx file is produced which shows the number of detected dots contained within each cell (0 means there was no dots detected within a cell). Additionally, .tiff images will be saved which show the segmentation results. Finally, in the main folder selected in the GUI, a .csv file is saved which shows the parameters used for segmentation.
