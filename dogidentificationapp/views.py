from django.shortcuts import render
import io
import requests
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from .forms import PhotoForm
import json
import base64
from PIL import Image
from dogidentificationapp.models import DogPhoto
from django.core.files.uploadedfile import SimpleUploadedFile



def homepage(request):
    page_title = "Dog Identification Service"
    try:
        dog_breeds = apps.get_app_config('dogidentificationapp').dog_classes
    except:
        dog_breeds = None
    return render(request, 'homepage.html', {"page_title": page_title, "dog_breeds": dog_breeds})


def aboutpage(request):
    page_title = "How to use the website?"
    return render(request, 'aboutpage.html', context={"page_title": page_title})


def classify_dogs(request):
    page_title = "Dog Classifier"
    feedback_submitted = False
    results = None
    image_b64 = None
    

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uplaoded photo
            photo_instance = form.save(commit=False)

           
            # reset feedback submitted since new photos is being uplaoded unless its example photo
            if 'example_upload' in request.FILES:
                request.session['feedback_submitted'] = True
            else:    
                request.session['feedback_submitted'] = False

            # Open the uploaded image and convert it to a PIL Image fro classification
            try:
                image = Image.open(io.BytesIO(photo_instance.image))
            except IOError:
                return JsonResponse({'status': 'error', 'message': 'Invalid image format.'})
            
            # Convert the image to JPG format if it's not already
            if image.format != 'JPEG':
                # If the image is not already in JPEG format, convert it
                image = image.convert('RGB')

            # Access the loaded model from the app config
            model = apps.get_app_config('dogidentificationapp').dog_classifier
            results = model.classify_dog(image)
            # change results into percentage and round 2 2 decimal places and change format of title to not include _
            results = [(label.replace('_', ' ').title(), round(confidence * 100, 2)) for label, confidence in results]

            if form.cleaned_data.get('save_to_db'):
                photo_instance.predicted_class_name = results[0][0]
                photo_instance.save() # real_class_name=form.cleaned_data.get('real_class_name'))
                request.session['photo_id'] = photo_instance.id  # Store the photo_id in session for updating from feedback form
                print(f"New photo saved to database: {request.session['photo_id']}")

            # lines = photo_instance.image.split('\n')
            image_b64 = base64.b64encode(photo_instance.image).decode('utf-8')

            # Store results in session to use after redirect
            request.session['results'] = results
            request.session['image_b64'] = image_b64

            # Pass the saved photo instance and results to the template context to be rendered
            return redirect('classify-dogz')
    else:
        form = PhotoForm()
        results = request.session.get('results', None)
        image_b64 = request.session.get('image_b64', None)
        photo_id = request.session.get('photo_id', None)
        feedback_submitted = request.session.get('feedback_submitted', False)


    return render(request, 'dog_classifier.html', {
        'page_title': page_title,
        'form': form,
        'results': results,
        'feedback_submitted': feedback_submitted,
        'img_obj': image_b64
    })

@csrf_exempt
def submit_feedback(request):
    """
    Handles feedback submission from the feedback form.
    If correct feedback is received, the real class name is updated in the database as predicted class.
    If incorrect feedback is received, the real class name is updated in the database as the correct breed submitted int form
    """
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            data = json.loads(body)

            is_correct = data.get('is_correct')
            correct_breed = data.get('correct_breed')
            
            # Retrieve the photo_id from the session
            photo_id = request.session.get('photo_id')

            # If photo_id is None, save the photo to the database (since being in this part of code means that user agreed to save the data)
            if photo_id is None:
                photo_instance = PhotoForm().save(commit=False, rawform=True)
                photo_instance.image = base64.b64decode(request.session.get('image_b64').encode('utf-8'))
                photo_instance.predicted_class_name = request.session.get('results')[0][0]
                photo_instance.save()
                photo_id = photo_instance.id
                print(f"New photo saved to database: photo_id {photo_id}")


            # Fetch the DogPhoto instance
            try:
                photo_instance = DogPhoto.objects.get(id=photo_id)
            except DogPhoto.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Photo not found.'})

            # Handle the feedback
            if is_correct:
                print('Feedback received: Correct, predicted saved as real')
                photo_instance.real_class_name = photo_instance.predicted_class_name
                photo_instance.save()
            else:
                print(f'Feedback received: Incorrect prediction. Correct breed saved: {correct_breed}')
                photo_instance.real_class_name = correct_breed
                photo_instance.save()

            # Remove the photo_id from the session after updating
            request.session['photo_id'] = None
            request.session['feedback_submitted'] = True

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def refuse_saving_of_data(request):
    request.session['feedback_submitted'] = True
    return redirect('classify-dogz')


@csrf_exempt
def upload_example(request):
    if request.method == 'POST':
        # Get the example image URL from the POST data
        example_image_url = request.POST.get('example_image_url')
        # get the image
        response = requests.get(example_image_url)
        # Create a PhotoForm instance and populate it with the example image URL
        if response.status_code == 200:
            image_data = response.content
            uploaded_file = SimpleUploadedFile('example.jpg', image_data)

            # Create a new POST request with the image data to mimic user input
            new_request = HttpRequest()
            new_request.method = 'POST'
            new_request.FILES['image'] = uploaded_file
            new_request.POST = request.POST
            new_request.session = request.session
            new_request.FILES['example_upload'] = 'true'

            # Call the classify_dogs function with the new request
            response = classify_dogs(new_request)

            # Handle the response if needed
            if response.status_code == 302:  # Redirect response
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Classification failed'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to fetch image data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unsupported method'})