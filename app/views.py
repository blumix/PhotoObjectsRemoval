from base64 import b64encode
import random

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

from app.forms import PictureForm
from .models import Photo
# from photo_corrector.urls import urlpatterns

from os import listdir
from os.path import isfile, join



def index(request):
    print("upload def called")
    form = PictureForm()
    return render(request, 'app/upload_tmpl.html', {'form': form})
    # return HttpResponse("Hello!")


def get_short_url(request):
    """
    Converts url to shortened_url if url is valid    
    """
    # if request.method == 'POST':
    #     url = request.POST['url']
    #     data = {"url": url}
    #     web_service = WebService(json.dumps(data), request)
    #     response = web_service.run()
    #     return render(request, 'url_app/url.html', {'data': json.loads(response)})
    return render(request, 'app/upload_tmpl.html')


def upload(request):
    print("upload def called")
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            if 'picture' not in request.FILES:
                return render(request, 'app/upload_tmpl.html', {'form': form})
            data = request.FILES['picture']
            path_to_folder = 'tmp/' + str(random.randint(1, 10000)) + "/";
            default_storage.save(path_to_folder + "init", ContentFile(data.read()))
            command = 'docker container run -it  -v ~/:/host a6033db4efbeb4181bd9f6a87e8bc70a1f9e03c72c03c00bbdc1a352ddd8d735 python3 /host/PhotoObjectsRemoval/scripts/find_mask.py ' + '/host/PhotoObjectsRemoval/media/' + path_to_folder
            print ("Going to execute:", command)
            os.system (command)
            
            abs_path_to_folder = '/home/mikhail.belozerov/PhotoObjectsRemoval/' + 'media/' + path_to_folder
            onlyfiles = [f for f in listdir(abs_path_to_folder) if (isfile(join(abs_path_to_folder, f)) and f.endswith ('.png'))]
            print (onlyfiles)
        else:
            print (form.errors)
    else:
        form = PictureForm()
    return render(request, 'app/upload_tmpl.html', {'form': form, 'range': range(len (onlyfiles)), 'max': len (onlyfiles), 'img_path':path_to_folder})


def send_info(request):
    f = None
    if request.method == 'POST':
        
        path_to_folder = request.POST.get('img_path', None)
        print ("Image Path:", path_to_folder)

        masks = []
        print ("Post:", request.POST)
        for i in range(len(request.POST)):
            try:
                masks.append(int(list(request.POST)[i].split('_of_')[0]))
            except ValueError:
                continue
        print("Choosen masks:", masks)
        
        abs_path_to_folder = '/home/mikhail.belozerov/PhotoObjectsRemoval/' + 'media/' + path_to_folder
        
        imagePath = abs_path_to_folder + 'init'
        maskPath = abs_path_to_folder + 'mask_' + str (masks[0]) + '.jpg'
        outPath = abs_path_to_folder + "out.png"
        print ("Paths:", imagePath, maskPath, outPath)
        
        command = "python3.5 ~/generative_inpainting/test.py " + \
        " --image " + imagePath + \
        " --mask " + maskPath + \
        " --output " + outPath + \
        " --checkpoint_dir ~/generative_inpainting/model_logs/places2_256"        
        
        print ("Gonna run:", command)
        os.system(command)
        
        return render(request, 'app/ready_img.html', {'path': path_to_folder})

    return render(request, 'app/ready_img.html', f)

