"""photo_corrector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# from django.contrib import admin
#
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]

# from django.conf.urls import include, url
# from django.contrib import admin
#
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# from django.conf.urls.defaults import *

# This two if you want to enable the Django Admin: (recommended)
# from django.contrib import admin
# admin.autodiscover()

# urlpatterns = [
#     url(r'^photo_corrector/', include('app.urls')),
#     url(r'^admin/', admin.site.urls),
# ]

# urlpatterns = [
#     url(r'^photo_corrector/', include('app.urls')),
#     url(r'^admin/', admin.site.urls),
#     url('django.views.static',
#         (r'^media/(?P<path>.*)',
#         'serve',
#         {'document_root': settings.MEDIA_ROOT}), )
#     # url(r'^static/(?P<path>.*)$', 'django.views.static', (r'^media/(?P<path>.*)', 'serve',{'document_root': settings.MEDIA_ROOT}),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    url(r'^photo_corrector/', include('app.urls')),
    url(r'^admin/', admin.site.urls),
    # url(r'^static/(?P<path>.*)$', 'django.views.static', (r'^media/(?P<path>.*)', 'serve',{'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# if settings.DEBUG:
#     urlpatterns += patterns(
#         'django.views.static',
#         (r'^media/(?P<path>.*)',
#          'serve',
#          {'document_root': settings.MEDIA_ROOT}), )


#
# if settings.DEBUG:
#   urlpatterns.append(url(
#       'django.views.static',
#       (r'^media/(?P<path>.*)',
#        'serve',
#        {'document_root': settings.MEDIA_ROOT}), ))