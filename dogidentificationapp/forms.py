from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = []


    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['image'] = forms.ImageField()
        self.fields['image'].label = (
            "Add an image of a dog for the dog breed classifier by clicking browse "
            "or dragging the image into the field"
        )  # Modify field label
        self.fields['image'].widget.attrs.update({'id': 'id_image_input'})  # Update widget attributes


    def save(self, commit=True):
        instance = super(PhotoForm, self).save(commit=False)
        uploaded_file = self.cleaned_data['image']
        instance.image = uploaded_file.read()
        if commit:
            instance.save()
        return instance