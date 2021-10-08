import os
import tempfile
import requests
from PIL import Image
from django.db import models
from django.utils import timezone
from custom_user.models import CustomUser
from django.contrib.auth.models import User
from django.core.files.images import ImageFile

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
        # CITATION - https://stackoverflow.com/questions/16174022/download-a-remote-image-and-save-it-to-a-django-model
        # Serious big ups to rockingskier, this is clean and simple code.
        if self.image_url and self.image_file == 'placeholder.jpg':
            # Stream Image from URL
            result = requests.get(self.image_url, stream=True)

            # TODO: Add some sort of error handling here
            # if result.status_code != requests.codes.ok:
            # continue

            file_name = f"{self.title[:10]}.{self.gutenberg_id}.{self.image_url.split('/')[-1]}"

            # Create a Temporary File
            temp = tempfile.NamedTemporaryFile()

            # Read Streamed image in chunks
            for chunk in result.iter_content(1024 * 8):
                if not chunk:
                    break

                temp.write(chunk)

            self.image_file.save(
                file_name,
                temp
            )

            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.get_remote_image()


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='user', on_delete=models.CASCADE)
    post = models.ForeignKey(
        Book, related_name='comment', on_delete=models.CASCADE)
    body = models.TextField(max_length=500, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post}, ({self.user})"
