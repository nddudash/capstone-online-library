from django.db import models
from book.models import Book
from custom_user.models import CustomUser

class Checkout(models.Model):
    book_to_check_out = models.ManyToManyField(Book, blank=True)
    user_checking_out_book = models.ManyToManyField(CustomUser, blank=True)


