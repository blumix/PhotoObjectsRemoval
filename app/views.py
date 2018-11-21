from base64 import b64encode, b64decode

from urllib.parse import unquote

import random

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

import re

from app.forms import PictureForm
from .models import Photo
# from photo_corrector.urls import urlpatterns

from os import listdir
from os.path import isfile, join
from time import sleep

import numpy as np
import skimage.io
import cv2
SYNC_FLODER_NAME="/home/dimjava/PROJECT/tmp/sync_mask/"

def index(request):
    print("upload def called")
    form = PictureForm()
    return render(request, 'app/index.html', {'form': form})
    # return HttpResponse("Hello!")

def upload(request):
    print("Upload called")
    path_to_folder = ""

    if request.method == 'POST':
        path_to_folder = 'tmp/' + str(random.randint(1, 10000)) + "/";
        full_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, path_to_folder)
        os.makedirs(full_path)

        #TODO: fix possible NPE
        header, data = unquote(str(request.body)).split(",", 1)
        data = b64decode(data)

        with open(os.path.join(full_path, 'init'), 'wb') as fout:
            fout.write(data)
    else:
        print(form.errors)

    return HttpResponse(path_to_folder, content_type="text/plain")

def inpaint(request):
    print("Inpaint called")

    if request.method != 'POST':
        return HttpResponse(content="Other than POST not supported", content_type="text/plain", status_code=400)

    #TODO: fix possible NPE
    header, data = unquote(str(request.body)).split(",")

    path_to_folder = re.findall("dir=([\\w|/]+)", header)[0]
    maskIdx = re.findall("idx=([-|\\d:]+)", header)
    maskIdxs = []
    if (len(maskIdx) == 0):
        maskIdx = None
    else:
        maskIdx = maskIdx[0]
        maskIdxs = maskIdx.split(":")

    print("path and mask", path_to_folder, maskIdx)

    full_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, path_to_folder)

    imagePath = os.path.join(full_path, 'init')
    outPath = os.path.join(full_path, 'out.png')
    maskPath = ""

    compositeMaskPath = prepareCompositeMask(full_path, maskIdxs)
    if (maskIdx != None and maskIdx != ""):
        maskPath = compositeMaskPath
    else:
        maskPath = os.path.join(full_path, 'mask')
        data = b64decode(data)

        with open(os.path.join(full_path, 'mask'), 'wb') as fout:
            fout.write(data)

    result = _inpaint(path_to_folder, imagePath, maskPath, outPath)

    return HttpResponse(content=result, content_type="text/plain")

def _inpaint(path_to_folder, imagePath, maskPath, outPath):
    command = "python3.5 ~/generative_inpainting/test.py " + \
        " --image " + imagePath + \
        " --mask " + maskPath + \
        " --output " + outPath + \
        " --checkpoint_dir ~/generative_inpainting/model_logs/places2_256"        
        
    print("Gonna run:", command)
    os.system(command)

    return os.path.join("/", settings.MEDIA_ROOT, path_to_folder, 'out.png')

def detectObjects(request):
    print("Detecting objects")
    if request.method != 'GET':
        return HttpResponse(content="Other than GET not supported", content_type="text/plain", status_code=400)

    path = request.GET.get('path')

    if (path == None or path == ""):
        return HttpResponse(content="Path should not be empty", content_type="text/plain", status_code=400)

    img_hash = path[4:-1]
    open(SYNC_FLODER_NAME + "go_" + img_hash, 'a').close()
    print("Created job {}.".format (SYNC_FLODER_NAME + "go_" + img_hash))
    done_name = "done_" + img_hash    
    print("Waiting for {}.".format (done_name))
    done = False
    for i in range (100):
        done_jobs = [f for f in listdir(SYNC_FLODER_NAME) if f.startswith ("done_")]
        if done_name not in done_jobs:
            sleep (0.1)
            continue
        os.remove (SYNC_FLODER_NAME + done_name)
        done = True
        break
            
    if not done:
        print ("Timeout.")
        return HttpResponse(content="Timeout in objects detection.", content_type="text/plain", status_code=400)
    
    maskPics = sorted(filter(lambda s: s.startswith("mask_pic"), listdir(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, path))))
    maskPics = list(map(lambda s: os.path.join("/", settings.MEDIA_ROOT, path ,s), maskPics))

    out = ";".join(maskPics)

    return HttpResponse(content=out, content_type="text/plain")


def prepareCompositeMask(path_to_folder, maskIdxs):
    if len(maskIdxs) == 0:
        return path_to_folder

    resultPath = os.path.join(path_to_folder, "mask_" + ''.join(maskIdxs) + ".jpg")

    print("Composite path = " + resultPath)

    if len(maskIdxs) == 1:
        return resultPath

    result = skimage.io.imread(os.path.join(path_to_folder, "mask_" + maskIdxs[0] + ".jpg"))
    for idx in maskIdxs[1:]:
        if idx == "":
            continue
        result += skimage.io.imread(os.path.join(path_to_folder, "mask_" + idx + ".jpg"))

    cv2.imwrite(resultPath, result)

    return resultPath
