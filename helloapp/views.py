from django.shortcuts import render
import os
import requests
from django.shortcuts import render, redirect
from .forms import PhotoForm
import base64
from PIL import Image
from helloapp.model import Model

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
        print('fiut')
        if form.is_valid():
            # Save the uploaded image
            photo_instance = form.save()
            # results = [
            #     ('borzoi', 0.8861562013626099), ('Scottish_deerhound', 0.03872758522629738), 
            #     ('Irish_wolfhound', 0.0251463670283556), ('Saluki', 0.014366214163601398), ('collie', 0.0056389993987977505)
            #     ]

            import os

            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, 'model', 'model.pth')
            class_names_path = os.path.join(current_dir, 'model', 'class_names.txt')

            model = Model(model_path, class_names_path)

            # input_image = Image.open('/home/killshot/Pictures/ziumba/download20240102175124.png')
            image = Image.open(os.path.join(current_dir, photo_instance.image.path))

            # Convert the image to JPG format
            if image.format != 'JPEG':
                # If the image is not already in JPEG format, convert it
                image = image.convert('RGB')

            results = model.classify_dog(image)

            # Pass the saved photo instance and results to the template context to be rendered
            return render(request, 'classifier.html', {'form': form, 'img_obj': photo_instance, 'results': results})
    else:
        form = PhotoForm()  # Your form class for uploading image
    return render(request, 'classifier.html', {'form': form})
