from base64 import b64encode

from django.shortcuts import render
from django.http import HttpResponse

from app.forms import PictureForm
from .models import Photo
# from photo_corrector.urls import urlpatterns


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
        print ("post")
        form = PictureForm(request.POST, request.FILES)
        # img = request.FILES['picture']
        print("files", request.FILES)

        # if form.is_valid():
        #     user = form.save()
        #     user.set_password(user.password)
        #     user.save()
        #     if 'img' in request.FILES:
        #         user.img = request.FILES['img']
        #     user.save()

        if form.is_valid():
            img = request.FILES
            print("valid", img, type(img), img['picture'], type(img['picture']))
            photo = form.save()
            if 'img' in request.FILES:
                print("img in request.FILES")
                photo.picture = request.FILES['picture']
            photo.save()
            last_photo = Photo.objects.last()
            print("last_photo", last_photo)
        else:
            print (form.errors)

        # pics = Photo.objects.all()
        # for pic in pics:
        #     print("img", pic.picture)
    else:
        form = PictureForm()
    return render(request, 'app/upload_tmpl.html', {'form': form, 'img': img, 'range': range(5), 'max': 5})


def transform_img(img):
    # TO DO
    return img


def send_info(request):
    f = None
    if request.method == 'POST':
        # print("request.POST", request.POST)
        # print("len",  len(request.POST))
        # num = 0
        buttons_ind = []
        img = request.POST.get('img', None)
        print("img", img, type(img), request.POST)
        img3 = request.FILES
        print("request.FILES", request.FILES)
        # print("img ", img, type(img))
        # data = img.read()
        # encoded = b64encode(data)
        # mime =  "image/jpeg"
        # mime = mime + ";" if mime else ";"
        # f = {"upFile": "data:%sbase64,%s" % (mime, encoded)}
        # form = request.POST.get('form', None)
        # if len(request.POST) > 1:
        #     num = int(list(request.POST)[1].split('_of_')[1])
        #     print("num", num)
        # # print(request.POST['input_3_of_5'])
        for i in range(1, len(request.POST)):
            try:
                buttons_ind.append(int(list(request.POST)[i].split('_of_')[0]))
            except ValueError:
                # picture_obj = list(request.POST)[i]
                continue
        print("buttons_ind", buttons_ind, img)


        # f = {"upFile": "data:%sbase64,%s" % (mime, encoded)}
        # tmp = Photo(picture=ready_img)
        # tmp.save()
        last_photo = Photo.objects.order_by('date').last().picture
        print("last_photo", last_photo)
        first_photo = Photo.objects.order_by('date').first().picture
        print("first_photo", first_photo)
        all_pics = Photo.objects.all()
        print("all_pics", all_pics)

        ready_img = transform_img(last_photo)
        print("ready_img", ready_img, type(ready_img))

        # tmp_obj = Photo(picture=your_pic)
        # tmp_obj.save()


        return render(request, 'app/ready_img.html', {'last_photo': last_photo})

    return render(request, 'app/ready_img.html', f)

