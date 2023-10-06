from nd2reader import ND2Reader
from skimage.filters import gaussian
from skimage.morphology import disk,white_tophat,disk,remove_small_objects
import numpy as np
from skimage.exposure import rescale_intensity
from cellpose import models


#Used to find max intensity projection of ND2 stack for cytoplasm and nuclei channels
def nd2_max_projection(nd2_object):
    #Get frame dimensions
    Z_DIM = nd2_object.sizes['z']
    X_DIM = nd2_object.frame_shape[0]
    Y_DIM = nd2_object.frame_shape[1]
    stack = np.empty([Z_DIM,X_DIM,Y_DIM],dtype='float32')

    #Import all cytoplasm focal planes
    nd2_object.default_coords['c'] = 0 #Cyto Channel
    for z in range(Z_DIM):
        stack[z,:,:] = np.asarray(nd2_object[z],dtype='float32')

    #Calculate maximum intensity projects for cyto channel
    max_intensity_cyto = np.amax(stack,axis=(0))

    #Import all nuclei focal planes
    nd2_object.default_coords['c'] = 1 #Nuclei Channel
    for z in range(Z_DIM):
        stack[z,:,:] = nd2_object[z]

    #Calculate maximum intensity projects for nuclei channel
    max_intensity_nuclei = np.amax(stack,axis=(0))

    return max_intensity_cyto,max_intensity_nuclei

#Used to import ND2 image stacks and return max, intensity projection of cytoplasm and nuclei channels
def import_stack(img_path,focal_plane_cyto=0,focal_plane_nuclei=0,min_percentile_cyto = 0,
                 max_percentile_cyto = 100,min_percentile_nuclei = 0,max_percentile_nuclei = 100,
                 max_intensity_projection = None):


  #Open ND2 file as object
    with ND2Reader(img_path) as nd2_object:

  #If we want maximum projection images
        if max_intensity_projection is True:
            channel_cyto,channel_nuclei = nd2_max_projection (nd2_object)

    #If we want any focal plane
        else:
            #Import cytoplasm image at desired focal plane
            nd2_object.default_coords['c'] = 0
            channel_cyto = nd2_object[focal_plane_cyto]

            #Import nuclei image at desired focal plane
            nd2_object.default_coords['c'] = 1
            channel_nuclei = nd2_object[focal_plane_nuclei]

    channel_cyto_no_saturation =  channel_cyto

    #rescale cyto channel based on max and min cyto percentile limits
    v_min, v_max = np.percentile(channel_cyto, (min_percentile_cyto, max_percentile_cyto))
    channel_cyto = rescale_intensity(channel_cyto, in_range=(v_min, v_max))

    channel_nuclei_no_saturation = channel_nuclei

    #rescale nuclei channel based on max and min nuclei percentile limits
    v_min, v_max = np.percentile(channel_nuclei, (min_percentile_nuclei, max_percentile_nuclei))
    channel_nuclei = rescale_intensity(channel_nuclei, in_range=(v_min, v_max))

    #Create 3d array with with channel 0: cytoplasm, channel 1: nuclei
    output_stack = np.zeros([3,channel_cyto.shape[0],channel_cyto.shape[1]])
    output_stack[1,:,:] = channel_cyto
    output_stack[2,:,:] = channel_nuclei

    #Create 3d array with with channel 0: cytoplasm, channel 1: nuclei
    output_stack_no_saturation = np.zeros([3,channel_cyto.shape[0],channel_cyto.shape[1]])
    output_stack_no_saturation[1,:,:] = channel_cyto_no_saturation
    output_stack_no_saturation[2,:,:] = channel_nuclei_no_saturation

    #Convert to float32 for cellpose
    output_stack = (output_stack).astype(dtype = 'float32') 
    output_stack_no_saturation = (output_stack_no_saturation/65535.0).astype(dtype = 'float32')

    return output_stack,output_stack_no_saturation


#Segments the nucleus. Pass the 3D image stack and choose manual segmentation threshold for nuclei
def nuclei_segmentation(stack,thresh_nuclei=0.06):
    #Blur nuclei image
    nuclei_image = gaussian(stack[2,:,:],1)

    mask_nuclei = ((nuclei_image > thresh_nuclei)*1).astype('float32')
    
    return mask_nuclei

#Segments the nucleus. Pass the 3D image stack and run cellpose for nuclei
def nuclei_segmentation_cellpose(stack,diameter = 80,flow_threshold = 0,use_gpu = False):
    #Blur nuclei image
    nuclei_image = gaussian(stack[2,:,:],1)

    # Lowered Batch_size from default 8 to reduce memory requirements
    model = models.Cellpose(gpu=use_gpu, model_type='nuclei',net_avg=False)
    mask_nuclei, _, _, _ = model.eval(nuclei_image,batch_size = 4, diameter = diameter,
                                      flow_threshold=flow_threshold, channels=[0,0])

    return mask_nuclei

#Function to segment the cells using Cellpose
def cell_segmentation(stack,diameter = 200,flow_threshold = 0,use_gpu = False):

    model = models.Cellpose(gpu=use_gpu, model_type='cyto',net_avg=False)

    # Lowered Batch_size from default 8 to reduce memory requirements
    mask_cyto, _, _, _ = model.eval(stack,batch_size = 4, diameter=diameter, 
                                    flow_threshold=flow_threshold, channels=[2,3])

    return mask_cyto


#Function to segment LC3 dots using white tophot and manual thresholding
def LC3_segmentation(stack,mask,threshold,tophat_size = 5,minimum_dot_size = 0):
    #mask: cytoplasm mask (no nuclei)
    
    #Use cyto channel
    image = stack[1,:,:]

    #Smooth image
    image_guassian = gaussian(image,1)

    #Tophat morphological filter to supress large objects in image
    LC3_tophat = white_tophat(image_guassian,disk(tophat_size))

    #Manual Thresholding
    LC3_segmented = LC3_tophat > threshold   

    #Remove nuclei + out-of-cell dots
    LC3_segmented = LC3_segmented * mask

    #Removes dots below specified area if needed
    if minimum_dot_size > 0 :
        LC3_segmented = remove_small_objects(np.bool_(LC3_segmented),min_size = minimum_dot_size)
       
    return np.uint16(LC3_segmented)


def find_image_paths(folder_path):
    import os
    image_paths = []
    image_roots = []
    for root, _, files in os.walk(folder_path):
        for name in files:
            if name.endswith('.nd2'):
                image_paths.append(os.path.join(root,name))
                image_roots.append(root)
    return image_paths, image_roots