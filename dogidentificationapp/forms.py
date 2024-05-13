from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = "Add an image of a dog for the dog breed classifier by clicking browse or dragging the image into the field"  # Modify field label
        self.fields['image'].widget.attrs.update({'id': 'id_image_input'})