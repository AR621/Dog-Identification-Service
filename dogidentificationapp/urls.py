from django.urls import re_path, path, include
from dogidentificationapp import views
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('about/', views.aboutpage, name='about'),
    path('', views.homepage, name='home'),
    path('dog/', views.classify_dogs, name='classify-dogz'),
]

