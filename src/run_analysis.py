from itertools import count
import gc
import os
import psutil

from csv import writer
from time import time, localtime, strftime
import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries
from skimage.measure import label,regionprops_table
import pandas as pd

from get_user_inputs import UserInputGUI
from functions import LC3_segmentation,find_image_paths,import_stack
from functions import nuclei_segmentation_cellpose, cell_segmentation

#Prompt User for inputs
print('Enter GUI parameters')
gui = UserInputGUI()
folder_directory,cell_diameter,nuclei_diameter,tophat_size,threshold_LC3,minimum_dot_size = gui.get_user_inputs()

image_paths,image_roots = find_image_paths(folder_directory)

#Get local time for unique results names
program_start_time = strftime("%Y-%m-%d %H-%M-%S", localtime())

# Save User parameters:
user_variables = [
                    ['Directory Analyzed',folder_directory],
                    ['TopHat Size',tophat_size],
                    ['LC3 Intensity Threshold',threshold_LC3],
                    ['LC3 Minimum Area',minimum_dot_size],
                    ['Cellpose Cytoplasm Diameter Estimate',cell_diameter],
                    ['Cellpose Nuclei Diameter Estimate',nuclei_diameter]
    ]

with open(os.path.join(folder_directory,'Translocation_parameters_{0}.csv').format(program_start_time),
                        'w',newline='') as csvfile:
    my_writer = writer(csvfile)
    my_writer.writerows(user_variables)

print('Beginning Analysis')

#Loop to anaylyze all images
for counter in range(len(image_paths)):
    start = time()
    print('\n     CPU Usage:', psutil.cpu_percent(interval=None),'%')

    image_path = image_paths[counter]
    image_root = image_roots[counter]

    print('     Analyzing:',image_path)
    #stack_with_sat has cytoplasm channel saturated to 95% max intensity, stack_without_sat does not
    stack_with_sat,stack_without_sat = import_stack(image_path,min_percentile_cyto=0,max_percentile_cyto=95,
                                                min_percentile_nuclei=0,max_percentile_nuclei=100,max_intensity_projection=True)

    #Create Nuclei Mask
    mask_nuclei = nuclei_segmentation_cellpose(stack_with_sat,diameter = nuclei_diameter,flow_threshold=0,use_gpu = True)

    #Create Cell Mask
    mask_cyto = cell_segmentation(stack_with_sat,diameter = cell_diameter,flow_threshold=0,use_gpu = True)

    #Create cell mask with no nuclei
    net_mask = ((mask_cyto>0) - mask_nuclei)>0   

    #Segment the LC3+ dots
    LC3_segmented = LC3_segmentation(stack_with_sat,net_mask,threshold = threshold_LC3,
                                    minimum_dot_size=minimum_dot_size,tophat_size=tophat_size)
    labeled_LC3 = label(LC3_segmented)

    #Identify with cell LC3+ proteins appear in
    props = regionprops_table(labeled_LC3,mask_cyto,properties=('label','intensity_min'))

    #Convert regionprops results to pandas data frame and count number of LC3+ per cell
    data_holder = pd.DataFrame(props)
    data_holder = data_holder['intensity_min'].value_counts().reset_index()

    num_cells = np.amax(mask_cyto)
    num_cells_with_proteins = len(data_holder)
    cells_without_proteins = num_cells-num_cells_with_proteins
    
    # #Add zeros for segmented cells with no detectable LC3 dots
    zero_pad = pd.DataFrame(np.zeros([cells_without_proteins,2]),columns=data_holder.columns)
    proteins_in_each_cell = pd.concat([data_holder,zero_pad],ignore_index = True)
    proteins_in_each_cell = proteins_in_each_cell['intensity_min'] # Only output number of proteins, discard cell ID label
    proteins_in_each_cell = pd.DataFrame(proteins_in_each_cell) #Re-format to Dataframe object
    
    #Results header string - uses number tag before .nd2 at end of file name
    # if running on mac
    if os.name == 'posix':
        split_image_path = image_path.split('/')
    # If running on windows
    elif os.name == 'nt':
        split_image_path = image_path.split('\\')

    file_number = split_image_path[-1][:-4]
    header = ['LC3+ Count: Image {0}'.format(file_number)]

    #If First file, write an excel file to store excel results
    new_storage_directory = os.path.join(image_root,'Results_{0}'.format(program_start_time))
    results_path = os.path.join(new_storage_directory,'LC3 Counts.xlsx')

    #Check if storage directory exits, if not make one
    if os.path.exists(new_storage_directory):
        pass  
    else:
        os.mkdir(new_storage_directory) 

    #create excel results file if it does not exist, otherwise write to existing
    if os.path.exists(results_path) is False:
        proteins_in_each_cell = proteins_in_each_cell.rename(columns={'intensity_min':header[0]})
        proteins_in_each_cell.to_excel(results_path,index = False,header = header[0])

    else:
        #Open Exisisting excel data and new write data to it
        existing_excel = pd.read_excel(results_path)

        #If it's the first image in the folder, clear any pre-existing results
        new_excel = pd.concat([existing_excel,proteins_in_each_cell],axis = 1,ignore_index=False)
        new_excel = new_excel.rename(columns={'intensity_min':header[0]})
        new_excel.to_excel(results_path,index = False)

    #Save Tiff. Image of results
    
    fig,ax = plt.subplots(1,3)
    fig.set_size_inches(20,20)
    
    image_name_tiff = split_image_path[-1].replace('.nd2','.tiff')

    ax[0].imshow(mark_boundaries(stack_with_sat[1,:,:],mask_cyto))
    ax[0].set_title('Cell Segmentation')

    ax[1].imshow(mark_boundaries(stack_with_sat[2,:,:],label(mask_nuclei)))
    ax[1].set_title('Nuclei Segmentation')

    ax[2].imshow(mark_boundaries(stack_with_sat[1,:,:],labeled_LC3))
    ax[2].set_title('LC3 Detected')

    plt.tight_layout()
    plt.savefig(os.path.join(new_storage_directory,'results-{0}.tiff'.format(file_number)),dpi = 200)

    #Clear figure memory
    fig.clf()
    plt.close() 
    gc.collect()    

    end = time()
    print('     Processing time:',round(end - start,1),'seconds')
    print('     Images Analyzed:',counter+1,'out of',len(image_paths))
        
print('Finished, all images analyzed.')