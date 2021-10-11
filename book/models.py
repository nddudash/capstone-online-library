import requests
import os
from PIL import Image
from django.db import models
from django.core.files import File
from requests.sessions import default_headers

# Create your models here.
# CITATION - https://stackoverflow.com/questions/16381241/django-save-image-from-url-and-connect-with-imagefield


class Book(models.Model):

    text = models.URLField(max_length=1500)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    copies_available = models.PositiveIntegerField(default=2)
    gutenberg_id = models.IntegerField(default=0)
    is_reserved = models.BooleanField(default=False)
    image_file = models.ImageField(
        upload_to="book_covers", default='placeholder.jpg')
    image_url = models.URLField(max_length=1500, blank=True, null=True)

    def __str__(self):
        return f"{self.title}, ({self.copies_available})"

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = requests.get(self.image_url)
            self.image_file.save(
                os.path.basename(self.image_url),
                File(open(result[0]))
            )
            self.save()
