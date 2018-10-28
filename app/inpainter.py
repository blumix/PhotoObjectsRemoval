from os import system
from random import randint
import cv2
import numpy as np

def generativeInpaint(imagePath, maskPath, outPath):
    command = "python3.5 ~/generative_inpainting/test.py " + \
        " --image " + imagePath + \
        " --mask " + maskPath + \
        " --output " + outPath + \
        " --checkpoint_dir ~/generative_inpainting/model_logs/places2_256"        

    return system(command)


def patchMatchInpaint(imagePath, outPath):
    tmpDir = "./tmp_" + str(randint(10000000, 99999999))
    system("mkdir " + tmpDir)
    system("cd " + tmpDir + " && " + \
           "~/patchMatch/build/hole_filling" + \
           " " + "../" + imagePath + " && " + \
           "cd ..")
    
    system("mv " + tmpDir + "/result.exr " + outPath)
    system("rm -rf " + tmpDir)

# mask is binary, 1 means we want to restore the pixel
def inpaint(image, mask, fast=1):
    imageId = str(randint(10000000, 99999999))
    imagePath = "./tmp/" + imageId + ".jpg"
    maskPath = "./tmp/" + imageId + "_mask.jpg"
    outPath = "./tmp/" + imageId + "_out.jpg"

    image = np.array(image)
    mask = np.array(mask)
    
    if (not fast):
        image[mask==1] = [255, 0, 255]
    else:
        maskImage = np.zeros(image.shape)
        maskImage[mask==1] = [255, 255, 255]
        cv2.imwrite(maskPath, maskImage)
    
    cv2.imwrite(imagePath, image)
    
    if (fast):
        generativeInpaint(imagePath, maskPath, outPath)
    else:
        patchMatchInpaint(imagePath, outPath)
 
    resultImage = cv2.imread(outPath)
    
#     system("rm " + imagePath)
#     system("rm " + maskPath)
#     system("rm " + outPath)
    
    return resultImage



