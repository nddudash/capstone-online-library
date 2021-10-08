from django.db import models
from django.db.models.fields import related
from django.utils import timezone
from custom_user.models import CustomUser
from book.models import Book
# Create your models here.

class Notifications(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_notified')
    exclamation = models.BooleanField(default=False)

    def __str__(self):
            return f"{self.user} reserved {self.book}. Exclamation = {self.exclamation}"