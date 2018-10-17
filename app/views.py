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
            print("valid", img)
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
    return render(request, 'app/upload_tmpl.html', {'form': form, 'img': img, 'range': range(5)})
    # try:
    #     form = PictureForm()
    #     person = Person.objects.get(pk=person_id)
    #     #print (person.username)
    #     #print (person.views)
    #     person.views = person.views + 1
    #     #print (person.views)
    #     person.save()
    #     #person.views = person.views + 1
    #     #person.save()
    # except Person.DoesNotExist:
    #     raise Http404("Person doesn't exist")
    # return render(request, 'friends_plans/user.html', {'form': form, 'person': person})