# LC3+ GFP dot counting using cellpose

# Project Overview
The image analysis pipeline written in this jupyter notebook utilizes the cellpose segmentation algorithm [https://github.com/MouseLand/cellpose] to segment the cells contained within 2-channel .nd2 fluorescent microscopy images. For the purpose of this project, it is unimportant to segment contacting neighbouring nuclei, hence simple global intensity thresholding is used to segment the nuclei of the cells. This approach is possible due to the high SNR of the nuclei channel and reduces the total computation time (by avoiding having to use cellpose for nuclei segmentation) enabling faster high-throughput analysis. If there are nuclei segmentation issues, it is recommended to set the method = 'CELLPOSE' described in the USER INPUTS section later in this document.

The fluorescent dots within the detected cells (exluding their nuclei) are segmented using a white tophat filter, manual thresholding and minimum area criteria. The script then counts the fluorescent dots within the detected cells and will ouput a "Results" folder containing images of the segmentations and an excel file which contains the dot counts in all segmented cells within each image.

![results-0002](https://user-images.githubusercontent.com/43760657/152824338-b6514bb1-f37f-41a7-8045-54970440e927.jpeg)

# Installation

1. Download Anaconda if this is not already installed.
2. Download the Git repository for this project.
3. Create and activate a conda virtual environment named translocation (python=3.9 or python=3.10 both should work) to isolate the project's packages.
   ```bash
   conda create --name environmentname python=3.9
   ```
4. Navigate to the downloaded git repository directory.
   ```bash
   cd directoy_of_downloaded_git_repository/code
   ```
5. Download the necessary packages the command below:
  
   ```bash
   pip install -r requirements.txt
   ``` 
6. Finished

# Run Program
1. In the terminal/command prompt, activate the conda environment for this project.
   ```bash
   conda activate environmentname
   ```
2. Change to the "Code" directory contained in this downloaded git repository
   ```bash
   cd directoy_of_downloaded_git_repository/code
   ```
3. Run the program from the command line using:
   ```bash
   python run_analysis.py
   ```
4. This will open a user interface. Enter the directory containing the image(s) or folders of images to be analyzed and tune the segmentation parameters.
6. Press "Run" to start the analysis

<p align="center">
<img width="450" alt="Screen Shot 2022-04-08 at 2 15 17 PM" src="https://user-images.githubusercontent.com/43760657/162433614-18773490-da77-48c4-b09c-43b60e8ba60c.png"> <img width="360" alt="Screen Shot 2022-04-08 at 2 15 29 PM" src="https://user-images.githubusercontent.com/43760657/162433646-51465914-4fe8-4a86-8643-1ab37a70cbe9.png">
</p>


### Running the program

#### Starting the program
The opened program should look similar to this. If it's your first time running the python or the program on your computer, run the first code by first clicking on the cell, then clicking the "Run" button or shift-enter as a shortcut to run the cell. The next two code-cells should be run everytime you first open the program as they import the required python modules and define the programs functions.

![Screen Shot 2022-02-11 at 4 11 19 PM](https://user-images.githubusercontent.com/43760657/153622848-014e7e59-448f-43ff-9a45-6d43fb03f39f.png)

#### User Inputs
Now the program's is ready to run. The first step is to define the variables defined in the "User Inputs" code-cell. Here is a detailed list:
1. filepath: This is the filepath to the folder containing the images to analyze. The directory should be entered as a string (with quotation marks around it). If running on a Windows computer, the string should be raw (add an r before it): r'filepath' not 'filepath'.

2. use_gpu: This should be set to True or False. If true, the cellpose neural network will use the computer's GPU to perform the calculations, which will significantly speed up the program. If there is no GPU available, set to False.

3.1 threshold_LC3: is a float value used to segment the LC3 dots based on their intensity value. A higher value will result in less dots segmented.

3.2 minimum_dot_size: integer value defining the minimum area (pixels) of retained LC3 dots. ie. = 10 -> any dots under 10 pixels will be discarded.

3.3 top_hat_size: interger value describing the size of the disk structuring element of the white_tophat filter used to segment the small bright LC3 dots. A larger element will allow larger dots to remain after LC3 segmentation.

4.1 cell_diameter : estimate of the diameter (in pixels) of the cell. This will affect the cytoplasm segmentation results significantly. More can be read on https://cellpose.readthedocs.io/en/latest/settings.html#diameter

4.2 flow_treshold_cyto: allowable error for cellpose flows for each mask (more information: https://cellpose.readthedocs.io/en/latest/settings.html). Typical range is -6 to 6. Default is set to 0.

Nuclei Segmentation: set to either 'CELLPOSE' or 'GLOBAL'. If 'CELLPOSE' is chosen, this will use the cellpose deep learning model to determine the nuclei mask, which will be slower than using the 'GLOBAL' approach which relies on a simple global threshold.

5. GLOBAL nuclei_threshold: Only need to modify if Nuclei Segmentation method is 'GLOBAL'. The global intensity threshold for segmentation of nuclei. Increase if the number or size of the nuclei are underestimated.

6. CELLPOSE Nuclei Segmentation.

  6.1 nuclei_diamter: estimate in pixel diameter of cell nuclei.
  
  6.2 nuclei_flow: allowable error for cellpose flows for each mask (more information: https://cellpose.readthedocs.io/en/latest/settings.html). Typical range is -6 to 6. Default is set to 0.

7. Output image saving options.

  7.1 output_images: Set to True or False, depending on if you want to save images of the segmentation results.

  7.2 resolution: sets the resolution (pixels per inch) of the output images. Greater resolution results in improved image quality but significantly increased storage demands and processing times.

![Screen Shot 2022-03-08 at 1 31 29 PM](https://user-images.githubusercontent.com/43760657/157238794-f46a4d87-97c1-458a-b48a-992676909334.png)

#### Running the program
After the user inputs are set, the final step is to run the "Run Program" code-cell. The program will print 'Finished, all images analyzed.' once finished running.

![Screen Shot 2022-02-16 at 9 31 37 AM](https://user-images.githubusercontent.com/43760657/154225725-1c188099-0387-420b-9282-9f5800bedb36.png)

#### Output Files

The output files include images for all segmentation and a single excel file containing a seperate column for each microscopy file. The rows indicate the number of counted dots per each detected cell within the frame. 

Note, if you choose to re-run the output file, change the name or delete the existing "Results" folder, otherwise the program will append new data to the exisitng results folder.
