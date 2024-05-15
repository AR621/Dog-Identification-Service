from django.shortcuts import render
import io
import requests
from django.shortcuts import render, redirect, HttpResponse
from django.apps import apps
from .forms import PhotoForm
import base64
from PIL import Image
from dogidentificationapp.models import Photo

def homepage(request):
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')
    
    return render(request, 'homepage.html', context={
        "message": "It's running!",
        "Service": service,
        "Revision": revision,
    })

def aboutpage(request):
    return render(request, 'aboutpage.html', context={})

def classify_dogs(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            photo_instance = form.save()
            # Open the uploaded image and convert it to a PIL Image fro classification
            image = Image.open(io.BytesIO(photo_instance.image))
            
            # Convert the image to JPG format if it's not already
            if image.format != 'JPEG':
                # If the image is not already in JPEG format, convert it
                image = image.convert('RGB')

            # Access the loaded model from the app config
            model = apps.get_app_config('dogidentificationapp').model
            results = model.classify_dog(image)
            # change results into percentage and round 2 2 decimal places and change format of title to not include _
            results = [(label.replace('_', ' ').title(), round(confidence * 100, 2)) for label, confidence in results]

            # Pass the saved photo instance and results to the template context to be rendered
            return render(request, 'dog_classifier.html', {'form': form, 'img_obj': photo_instance, 'results': results})
    else:
        form = PhotoForm()
    return render(request, 'dog_classifier.html', {'form': form})


def serve_image(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    return HttpResponse(photo.image, content_type="image/jpeg")