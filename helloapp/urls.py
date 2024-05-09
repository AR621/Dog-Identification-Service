from django.urls import path
from helloapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('about/', views.aboutpage, name='about'),
    path('', views.homepage, name='home'),
    # path('upload/', views.upload_photo, name='upload_photo'),
    path('dog/', views.classify_dogs, name='upload_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)