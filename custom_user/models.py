from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class CustomUser(AbstractUser):
    def random_card_number():
        return str(random.randint(100000, 999999))
    
    username = models.CharField(max_length=255, unique=True)
    checked_out_books = models.ManyToManyField(to='book.Book', blank=True, related_name='checked_out')
    reserved_books = models.ManyToManyField(to='book.Book', blank=True)
    library_card_number = models.CharField(max_length=10, default=random_card_number)

    def __str__(self) -> str:
        return self.username