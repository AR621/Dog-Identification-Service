from django.db import models

class Photo(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='images/')