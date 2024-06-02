from django.test import TestCase, Client
from django.urls import reverse
from .models import DogPhoto
from django.core.files.uploadedfile import SimpleUploadedFile


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()


    def test_homepage_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')


    def test_aboutpage_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aboutpage.html')


    def test_classify_dogs_get(self):
        response = self.client.get(reverse('classify-dogz'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dog_classifier.html')


    def test_classify_dogs_post(self):
        # Read the image file as binary data
        with open('dogidentificationapp/static/dummy_images/dummy_dog1.jpg', 'rb') as f:
            image_data = f.read()

        # Create a SimpleUploadedFile object to represent the image file as the user upload it
        uploaded_file = SimpleUploadedFile('dummy_dog1.jpg', image_data, content_type='image/jpeg')
        form_data = {'image': uploaded_file}

        # Send the POST request with the form data
        response = self.client.post(reverse('classify-dogz'), form_data)

        # Check if the response is a redirect (status code 302) as we are expecting redirect after successful form submission
        self.assertEqual(response.status_code, 302)


    def test_submit_feedback_view(self):
        # Create a DogPhoto instance for testing
        dog_photo = DogPhoto.objects.create(image=b'dummy_image_data')

        response = self.client.post(reverse('submit_feedback'), {'is_correct': True})
        self.assertEqual(response.status_code, 200)
        # Check if real_class_name updated correctly
        self.assertEqual(dog_photo.real_class_name, dog_photo.predicted_class_name)


    def test_refuse_saving_of_data_view(self):
        response = self.client.get(reverse('refuse_saving_of_data'))
          # Expecting redirect after refusing saving data
        self.assertEqual(response.status_code, 302)
