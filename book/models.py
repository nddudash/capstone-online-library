import os
import tempfile
import requests
from PIL import Image
from django.db import models
import cloudinary.uploader
from django.conf import settings


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
        upload_to="book_covers", default='static/images/placeholder.jpg')
    image_url = models.URLField(max_length=1500, blank=True, null=True)

    def __str__(self):
        return f"{self.title}, ({self.copies_available})"

    def get_remote_image(self):
        if settings.DEBUG:
            # CITATION - https://stackoverflow.com/questions/16174022/download-a-remote-image-and-save-it-to-a-django-model
            # Serious big ups to rockingskier, this is clean and simple code.
            if self.image_url and self.image_file == 'static/images/placeholder.jpg':
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
                    print("Chunky")
                    if not chunk:
                        break

                    temp.write(chunk)

                self.image_file.save(
                    file_name,
                    temp
                )
                self.save()

        elif not settings.DEBUG:
            # CITATION - https://github.com/cloudinary/pycloudinary/blob/master/samples/basic/basic.py
            if "cloudinary" not in self.image_url:

                if os.path.exists("config/settings.py"):
                    exec(open("config/settings.py").read())

                response = cloudinary.uploader.upload(
                    self.image_url,
                )

                print("UPLOAD: ")
                for key in sorted(response.keys()):
                    print("  %s: %s" % (key, response[key]))

                self.image_url = (response["secure_url"])
                self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.get_remote_image()
