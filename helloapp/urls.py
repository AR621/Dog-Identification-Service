from django.urls import path, include
from helloapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('about/', views.aboutpage, name='about'),
    path('', views.homepage, name='home'),
    path('dog/', views.classify_dogs, name='classify-dogz'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

