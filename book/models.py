from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import BooleanField
from custom_user.models import CustomUser
from django.utils import timezone

# Create your models here.


class Book(models.Model):
    text = models.URLField(max_length=1500)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    copies_available = models.PositiveIntegerField(default=2)
    gutenberg_id = models.IntegerField(default=0)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}, ({self.copies_available})"


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
