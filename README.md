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

The opened program should look similar to this. If it's your first time running the python or the program on your computer, run the first code by first clicking on the cell, then clicking the "Run" button or shift-enter as a shortcut to run the cell. The next two code-cells should be run everytime you first open the program as they import the required python modules and define the programs functions.

![Screen Shot 2022-02-11 at 4 11 19 PM](https://user-images.githubusercontent.com/43760657/153622848-014e7e59-448f-43ff-9a45-6d43fb03f39f.png)

Now the program is ready to run. The first step is to change the value

![Screen Shot 2022-02-11 at 4 48 46 PM](https://user-images.githubusercontent.com/43760657/153623162-33536670-e737-4523-8fe4-24d24b17c1a0.png)



1. First run the first two  jupyter-cells to import the necessary python modules and define the custom functions.
2. After this, the user should enter the filepath of the local directory containing the images to be analyzed in the "User Inputs" jupyter-cell. Additional parameters for fine tuning of the cytoplasm, nuclei and fluorescent dot segmentation shold be adjusted in this cell as well.
3. Run the "Run Program" jupyter-cell, which will loop through and anaylze all images in the given filepath.
4. If needed, tune segmentation parameters and re-run the "User Inputs" and "Run Program" jupyter-cells.
