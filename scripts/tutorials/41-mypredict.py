# project imports
from SynthSeg.predict import predict
import numpy as np




### ! Not working ! 


# paths to input/output files
# dhcp_reg_datadir = '/home/arnaud/projects/RESEARCH-MRI-analysis/code/volumes/mri_register/dhcp'
path_images = '/home/arnaud/projects/RESEARCH-MRI-analysis/code/volumes/IXI002-Guys-0828-T1.nii.gz'
# path to the output segmentation
path_segm = './outputs_predict_modif/predicted_segmentations/'
# we can also provide paths for optional files containing the probability map for all predicted labels
# and for a csv file that will contain the volumes of each segmented structure
path_posteriors = './outputs_predict_modif/predicted_information/'
path_vol = './outputs_predict_modif/predicted_information/'

# path to the trained model
# also need to provide the path to the segmentation labels used during training
# with optional names
path_model = '../../models/synthseg_1.0.h5'

path_segmentation_labels = '../../data/labels_classes_priors/synthseg_segmentation_labels.npy'
topology_classes = '../../data/labels_classes_priors/synthseg_topological_classes.npy'
path_segmentation_names = '../../data/labels_classes_priors/synthseg_segmentation_names.npy'
# my replacement
label_removed = 12
np_segmentation_labels = np.load(path_segmentation_labels)
index_removed = np.where(np_segmentation_labels == label_removed)
# np_segmentation_labels[np_segmentation_labels == label_removed] = 0   # replace the label to be removed, by background
# # np_segmentation_labels[np_segmentation_labels > label_removed ] -= 1  
my_segmentation_labels = np_segmentation_labels

np_topology_classes = np.load(topology_classes)
val_at_index_removed = np_topology_classes[index_removed]
np_topology_classes[index_removed] = 0
np_topology_classes[np_topology_classes > val_at_index_removed] -= 1 # needs to be ordered
my_topology_classes = np_topology_classes

# doesn't seem necessary
np_segmentation_names = np.load(path_segmentation_names)
np_segmentation_names[index_removed] = 'background'
my_segmentation_names = np_segmentation_names


# We can now provide various parameters to control the preprocessing of the input.
# the size of input must be divisible by 2**n_levels, the input image will be automatically padded to the nearest shape divisible by 2**n_levels 
# (this is just for processing, the output will then be cropped to the original image size).
# Alternatively, you can crop the input to a smaller shape for faster processing, or to make it fit on your GPU.
cropping = 192
target_res = 1.
# Note that if the image is indeed resampled, you have the option to save the resampled image.
path_resampled = './outputs_predict_modif/predicted_information/'

# After the image has been processed by the network, there are again various options to postprocess it.
# First, we can apply some test-time augmentation by flipping the input along the right-left axis and segmenting
# the resulting image. In this case, and if the network has right/left specific labels, it is also very important to
# provide the number of neutral labels. This must be the exact same as the one used during training.
flip = True
n_neutral_labels = 18
# Second, we can smooth the probability maps produced by the network. This doesn't change much the results, but helps to
# reduce high frequency noise in the obtained segmentations.
sigma_smoothing = 0.5

# Finally, we can also operate a strict version of biggest connected component, to get rid of unwanted noisy label
# patch that can sometimes occur in the background. If so, we do recommend to use the smoothing option described above.
keep_biggest_component = True

# Regarding the architecture of the network, we must provide the predict function with the same parameters as during
# training.
n_levels = 5
nb_conv_per_level = 2
conv_size = 3
unet_feat_count = 24
activation = 'elu'
feat_multiplier = 2

# Just set this to None if you do not want to run evaluation. REQUIRES GT SEGMENTATION
gt_folder = None

#
# Also we can compute different surface distances (Hausdorff, Hausdorff99, Hausdorff95 and mean surface distance). The
# results will be saved in arrays similar to the Dice scores.
compute_distances = True

# All right, we're ready to make predictions !!
predict(path_images,
        path_segm,
        path_model,
        # path_segmentation_labels,
        my_segmentation_labels,
        n_neutral_labels=n_neutral_labels,
        path_posteriors=path_posteriors,
        path_resampled=path_resampled,
        path_volumes=path_vol,
        # names_segmentation=path_segmentation_names,
        names_segmentation=my_segmentation_names,
        cropping=cropping,
        target_res=target_res,
        flip=flip,
        # topology_classes=topology_classes,
        topology_classes=my_topology_classes,
        sigma_smoothing=sigma_smoothing,
        keep_biggest_component=keep_biggest_component,
        n_levels=n_levels,
        nb_conv_per_level=nb_conv_per_level,
        conv_size=conv_size,
        unet_feat_count=unet_feat_count,
        feat_multiplier=feat_multiplier,
        activation=activation,
        gt_folder=gt_folder,
        compute_distances=compute_distances)
