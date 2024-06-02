from django.urls import re_path, path, include
from django.views.generic import RedirectView
from dogidentificationapp import views
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    # handle website resouces
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),

    # handle webpages
    path('about/', views.aboutpage, name='about'),
    path('', views.homepage, name='home'),
    path('dog/', views.classify_dogs, name='classify-dogz'),

    # requests from js
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('refuse_saving_of_data/', views.refuse_saving_of_data, name='refuse_saving_of_data'),
    path('upload_example/', views.upload_example, name='upload_example')
]

