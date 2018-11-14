from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^inpaint/$', views.inpaint, name='inpaint'),
    url(r'^detect/$', views.detectObjects, name='detect'),
]


# if settings.DEBUG:
#     urlpatterns += patterns(
#         'django.views.static',
#          (r'^media/(?P<path>.*)',
#          'serve',
#          {'document_root': settings.MEDIA_ROOT}), )