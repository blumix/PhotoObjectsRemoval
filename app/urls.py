from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^send_info/$', views.send_info, name='send_info'),
]


# if settings.DEBUG:
#     urlpatterns += patterns(
#         'django.views.static',
#          (r'^media/(?P<path>.*)',
#          'serve',
#          {'document_root': settings.MEDIA_ROOT}), )