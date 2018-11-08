import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import cv2

ROOT_DIR = "/host/Mask_RCNN/"
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
sys.path.append(os.path.join(ROOT_DIR, "/host/Mask_RCNN/samples/coco/"))  # To find local version
import coco
from mrcnn import visualize

MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    
def find_masks_impl (image):
    config = InferenceConfig()
    config.display()
    
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
    model.load_weights(COCO_MODEL_PATH, by_name=True)
    results = model.detect([image], verbose=1)
    return results[0]

def find_masks (pic_folder):
    image = skimage.io.imread(pic_folder + "init")
    r = find_masks_impl (image)
    N = len (r['rois'])
    
    colors = visualize.random_colors(N)

    # save mask and masked image to display
    for i in range (N):
        mask = r['masks'][:,:,i]
        maskImage = np.zeros(image.shape)
        maskImage[mask==True] = [255, 255, 255]
        maskImage = expandMask(maskImage, 20)
        
        cv2.imwrite (pic_folder + "mask_" + str (i) + ".jpg", maskImage)
       
        masked_image = visualize.apply_mask(np.copy (image), mask, colors[i])
        skimage.io.imsave (pic_folder + "mask_pic_" + str (i) + ".png", masked_image)
    return N

def expandMask(mask, n):
    result = np.zeros(mask.shape)
    
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            result[i, j, :] = np.max(mask[max(0, i-n):min(mask.shape[0], i+n), max(0, j-n):min(mask.shape[1], j+n), :])
    
    return result
    
print ("Masks found:", find_masks (sys.argv[1]))