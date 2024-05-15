from django.db import models

class Photo(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.BinaryField()

    def __str__(self):
        return f'Photo {self.id}'
