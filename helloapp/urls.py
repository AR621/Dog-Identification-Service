from django.urls import path
from helloapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('about/', views.aboutpage, name='about'),
    path('', views.homepage, name='home'),
    # path('upload/', views.upload_photo, name='upload_photo'),
    path('dog/', views.upload_image, name='upload_photo'),
    path('results/', views.classify_photo, name='classifier'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)