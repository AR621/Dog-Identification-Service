from django import forms
from .models import DogPhoto

class PhotoForm(forms.ModelForm):
    class Meta:
        model = DogPhoto
        fields = []


    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['image'] = forms.ImageField()
        self.fields['save_to_db'] = forms.BooleanField(required=False, label='Save results to database')
        self.fields['image'].label = (
            "Add an image of a dog for the dog breed classifier by clicking browse "
            "or dragging the image into the field"
        )  # Modify field label
        self.fields['image'].widget.attrs.update({'id': 'id_image_input'})  # Update widget attributes


    def save(self, commit=True, predicted_class_name = None, real_class_name = None):
        instance = super(PhotoForm, self).save(commit=False)
        uploaded_file = self.cleaned_data['image']
        instance.image = uploaded_file.read()
        print(f"Image uploaded {instance.id}")
        if predicted_class_name:
            instance.predicted_class_name = predicted_class_name
        if real_class_name:
            instance.real_class_name = real_class_name
        if commit:
            instance.save()
        return instance