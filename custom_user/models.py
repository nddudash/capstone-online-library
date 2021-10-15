import os
import random
import tempfile

import requests
from django.contrib.auth.models import AbstractUser
from django.core.files.images import ImageFile
from django.db import models
from PIL import Image
from requests.sessions import default_headers


class CustomUser(AbstractUser):
    def random_card_number():
        return str(random.randint(100000, 999999))
    
    username = models.CharField(max_length=255, unique=True)
    checked_out_books = models.ManyToManyField(to='book.Book', blank=True, related_name='checked_out')
    reserved_books = models.ManyToManyField(to='book.Book', blank=True)
    library_card_number = models.CharField(max_length=10, default=random_card_number)
    profile_image = models.ImageField(upload_to='profile_pic', default='imgs/profile.jpg', null= True, blank= True)
    image_url = models.URLField(max_length=1500, blank=True, null=True)

    def __str__(self) -> str:
        return self.username
