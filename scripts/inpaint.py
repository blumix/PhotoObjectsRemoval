import sys

INPAINT_MODEL_PATH="/home/dimjava/generative_inpainting"
SYNC_FLODER_NAME="/home/dimjava/PROJECT/tmp/sync_inpaint/"
FILES_FLODER_NAME="/home/dimjava/PROJECT/PhotoObjectsRemoval/media/tmp/"

IMG_HEIGHT=1024
IMG_WIDTH=1024

sys.path.append(INPAINT_MODEL_PATH)  # To find local version of the library

import argparse

import cv2
import numpy as np
import tensorflow as tf
import neuralgym as ng
from os import listdir
from os.path import isfile, join
from time import sleep
import os

from inpaint_model import InpaintCAModel

parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint_dir', default='', type=str,
                    help='The directory of tensorflow checkpoint.')


def process_img_new (img_name, mask_name, result_name, sess, output, input_image_ph):
    image = cv2.imread(img_name)
    mask = cv2.imread(mask_name)

    h_init, w_init, _ = image.shape

    image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    mask = cv2.resize(mask, (IMG_WIDTH, IMG_HEIGHT))
    assert image.shape == mask.shape
    h, w, _ = image.shape
    grid = 4
    image = image[:h//grid*grid, :w//grid*grid, :]
    mask = mask[:h//grid*grid, :w//grid*grid, :]
    print('Shape of image: {}'.format(image.shape))
    image = np.expand_dims(image, 0)
    mask = np.expand_dims(mask, 0)
    input_image = np.concatenate([image, mask], axis=2)
    result = sess.run(output, feed_dict={input_image_ph: input_image})
    print('Processed: {}'.format(result_name))

    cv2.imwrite(result_name, cv2.resize (result[0][:, :, ::-1], (w_init, h_init)))



def main ():
    ng.get_gpus(1)
    args = parser.parse_args()

    sess_config = tf.ConfigProto()
    sess_config.gpu_options.allow_growth = True
    sess = tf.Session(config=sess_config)

    model = InpaintCAModel()
    input_image_ph = tf.placeholder(
        tf.float32, shape=(1, IMG_HEIGHT, IMG_WIDTH*2, 3))
    output = model.build_server_graph(input_image_ph)
    output = (output + 1.) * 127.5
    output = tf.reverse(output, [-1])
    output = tf.saturate_cast(output, tf.uint8)
    vars_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
    assign_ops = []
    for var in vars_list:
        vname = var.name
        from_name = vname
        var_value = tf.contrib.framework.load_variable(
            args.checkpoint_dir, from_name)
        assign_ops.append(tf.assign(var, var_value))
    sess.run(assign_ops)
    print('Model loaded.')
    while (True):
            try:
                new_jobs = [f for f in listdir(SYNC_FLODER_NAME) if f.startswith ("go_")]
                if len (new_jobs) == 0:
                    sleep (0.1)
                    continue

                job_id = new_jobs[0][3:]
                mask_name = open (SYNC_FLODER_NAME + new_jobs[0]).readline ().strip ()

                os.remove (SYNC_FLODER_NAME + new_jobs[0]) #delete go_ file
                print ("Processing image: ", job_id)
                pic_folder = FILES_FLODER_NAME + job_id + "/"

                process_img_new (img_name=pic_folder + "init", \
                             mask_name=mask_name, \
                             result_name=pic_folder + "out.png", \
                             sess=sess, \
                             output=output, \
                             input_image_ph=input_image_ph)

                open(SYNC_FLODER_NAME + "done_" + job_id, 'a').close() #create done_ file
                print ("Job {} done.".format (job_id))

            except KeyboardInterrupt:
                sys.exit()

if __name__ == "__main__":
    main()
