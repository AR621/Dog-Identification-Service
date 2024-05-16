from django.db import models

class DogPhoto(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.BinaryField()
    real_class_name = models.CharField(max_length=100, blank=True)
    predicted_class_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Photo {self.id}'
