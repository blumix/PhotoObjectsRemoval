import os
import sys
import random
import math
import numpy as np
import skimage.io
import cv2
from os import listdir
from os.path import isfile, join
import os
from time import sleep
import cv2
import tensorflow as tf
import keras

os.environ["CUDA_VISIBLE_DEVICES"]="0"

config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
keras.backend.set_session(sess)

def _get_available_devices():
    from tensorflow.python.client import device_lib
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos]


SYNC_FLODER_NAME="/home/dimjava/PROJECT/tmp/sync_mask/"
FILES_FLODER_NAME="/home/dimjava/PROJECT/PhotoObjectsRemoval/media/tmp/"
MASK_RCNN_PATH="/home/dimjava/PROJECT/Mask_RCNN/"

sys.path.append(MASK_RCNN_PATH)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
sys.path.append(os.path.join(MASK_RCNN_PATH, "samples/coco/"))  # To find local version
import coco
from mrcnn import visualize

MODEL_DIR = os.path.join(MASK_RCNN_PATH, "logs")
COCO_MODEL_PATH = os.path.join(MASK_RCNN_PATH, "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    
def find_masks (pic_folder, model):
    image = skimage.io.imread(pic_folder + "init")
    r = model.detect([image])[0]
    N = len (r['rois'])    
    colors = visualize.random_colors(N)
    # save mask and masked image to display
    for i in range (N):
        mask = r['masks'][:,:,i]
        maskImage = np.zeros(image.shape)
        maskImage[mask==True] = [255, 255, 255]
        kernel = np.ones((5,5), np.uint8)
        maskImage = cv2.dilate (maskImage, kernel, 1)
        
        cv2.imwrite (pic_folder + "mask_" + str (i) + ".jpg", maskImage)
       
        masked_image = visualize.apply_mask(np.copy (image), mask, colors[i])
        skimage.io.imsave (pic_folder + "mask_pic_" + str (i) + ".png", masked_image)
    return N    

    
def main ():
    while (True):
        try:
            config = InferenceConfig()
            config.display()

            model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
            model.load_weights(COCO_MODEL_PATH, by_name=True)

            while (True):
                new_jobs = [f for f in listdir(SYNC_FLODER_NAME) if f.startswith ("go_")]
                if len (new_jobs) == 0:
                    sleep (0.1)
                    continue

                job_id = new_jobs[0][3:]
                os.remove (SYNC_FLODER_NAME + new_jobs[0])
                print ("Processing image: ", job_id)
                pic_folder = FILES_FLODER_NAME + job_id + "/"
                result = find_masks (pic_folder, model)
                print ("Masks found:", result)
                open(SYNC_FLODER_NAME + "done_" + job_id, 'a').close()
                print ("Job {} done.".format (job_id))
                
        except KeyboardInterrupt:
            sys.exit()            
    
if __name__ == "__main__":
    main()