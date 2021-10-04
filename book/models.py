from django.db import models

# Create your models here.


class Book(models.Model):
    text = models.TextField(max_length=1500)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    copies_available = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.title}, ({self.copies_available})"
