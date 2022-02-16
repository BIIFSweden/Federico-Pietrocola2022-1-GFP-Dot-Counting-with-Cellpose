# LC3+ GFP dot counting using cellpose

## Project Overview
The image analysis pipeline written in this jupyter notebook utilizes the cellpose segmentation algorithm [https://github.com/MouseLand/cellpose] to segment the cells contained within 2-channel .nd2 fluorescent microscopy images. For the purpose of this project, it is unimportant to segment contacting neighbouring nuclei, hence simple global intensity thresholding is used to segment the nuclei of the cells. This approach is possible due to the high SNR of the nuclei channel and reduces the total computation time (by avoiding having to use cellpose for nuclei segmentation) enabling faster high-throughput analysis.

The fluorescent dots within the detected cells (exluding their nuclei) are segmented using a white tophat filter, manual thresholding and minimum area criteria. The script then counts the fluorescent dots within the detected cells and will ouput a "Results" folder containing images of the segmentations and an excel file which contains the dot counts in all segmented cells within each image.

![results-0002](https://user-images.githubusercontent.com/43760657/152824338-b6514bb1-f37f-41a7-8045-54970440e927.jpeg)


## Script Guide

### Installation

#### 1. Python Installation
If you do not already have Python3 installed, Anaconda should first be installed using the following guide:

https://docs.anaconda.com/anaconda/install/index.html

This will install the latest version of Python, Jupyter notebook to run the code and many commonly used Python modules.

#### 2. Segmentation Algorithm Installation

Download the code as a zip file and extract the files to a directory where you wish to save the program (eg. desktop, documents etc.).

![Screen Shot 2022-02-11 at 3 42 16 PM](https://user-images.githubusercontent.com/43760657/153612004-74be87e9-c553-4529-89a3-e2a14ec60170.png)

### 3. Opening the dot counting program in Jupyter Notebook

To open the program, first open jupyter notebook using your terminal (mac) or command prompt (windows). Then type in "jupyter notebook" and press the return key, which will then open jupyter in your default web browser. 
<img width="561" alt="Screen Shot 2022-02-11 at 3 52 37 PM" src="https://user-images.githubusercontent.com/43760657/153613873-93f14e1b-00c2-4c29-bca9-42207b1bb898.png">

Once open, navigate to the directory containing the extracted ZIP folder. This is where you'll run the code. The example image shows it stored on my desktop.

![Screen Shot 2022-02-11 at 4 04 01 PM](https://user-images.githubusercontent.com/43760657/153615657-81643ef4-cf36-41a4-81bc-5848ce6d4f5b.png)

![Screen Shot 2022-02-11 at 4 07 52 PM](https://user-images.githubusercontent.com/43760657/153616281-1335d30c-ba9c-4b1a-907c-f304f921feb0.png)

![Screen Shot 2022-02-11 at 4 08 46 PM](https://user-images.githubusercontent.com/43760657/153616407-84e0d5e9-45ec-4fbc-a517-fa4bc173a6ba.png)


Once you find the "Cellpose-Segmentation.ipynb" file, open it by clicking on the filename.


### Running the program

#### Starting the program
The opened program should look similar to this. If it's your first time running the python or the program on your computer, run the first code by first clicking on the cell, then clicking the "Run" button or shift-enter as a shortcut to run the cell. The next two code-cells should be run everytime you first open the program as they import the required python modules and define the programs functions.

![Screen Shot 2022-02-11 at 4 11 19 PM](https://user-images.githubusercontent.com/43760657/153622848-014e7e59-448f-43ff-9a45-6d43fb03f39f.png)

#### User Inputs
Now the program's is ready to run. The first step is to define the variables defined in the "User Inputs" code-cell. Here is a detailed list:
1. filepath: This is the filepath to the folder containing the images to analyze. The directory should be entered as a string (with quotation marks around it).

2. use_gpu: This should be set to True or False. If true, the cellpose neural network will use the computer's GPU to perform the calculations, which will significantly speed up the program. If there is no GPU available, set to False.

3.1 threshold_LC3: is a float value used to segment the LC3 dots based on their intensity value. A higher value will result in less dots segmented.

3.2 minimum_dot_size: integer value defining the minimum area (pixels) of retained LC3 dots. ie. = 10 -> any dots under 10 pixels will be discarded.

3.3 top_hat_size: interger value describing the size of the disk structuring element of the white_tophat filter used to segment the small bright LC3 dots. A larger element will allow larger dots to remain after LC3 segmentation.

4.1 cell_diameter : estimate of the diameter (in pixels) of the cell. This will affect the cytoplasm segmentation results significantly. More can be read on https://cellpose.readthedocs.io/en/latest/settings.html#diameter

4.2 flow_treshold_cyto: allowable error for cellpose flows for each mask (more information: https://cellpose.readthedocs.io/en/latest/settings.html). Typical range is -6 to 6. Default is set to 0.

5. nuclei_threshold: the global intensity threshold for segmentation of nuclei. Increase if the number or size of the nuclei are underestimated.

6.1 output_images: Set to True or False, depending on if you want to save images of the segmentation results.

6.2 resolution: sets the resolution (pixels per inch) of the output images. Greater resolution results in improved image quality but significantly increased storage demands and processing times.

![Screen Shot 2022-02-11 at 4 48 46 PM](https://user-images.githubusercontent.com/43760657/153623162-33536670-e737-4523-8fe4-24d24b17c1a0.png)

#### Running the program
After the user inputs are set, the final step is to run the "Run Program" code-cell. The program will print 'Finished, all images analyzed.' once finished running.

![Screen Shot 2022-02-16 at 9 31 37 AM](https://user-images.githubusercontent.com/43760657/154225725-1c188099-0387-420b-9282-9f5800bedb36.png)

#### Output Files

The output files include images for all segmentation and a single excel file containing a seperate column for each microscopy file. The rows indicate the number of counted dots per each detected cell within the frame.
