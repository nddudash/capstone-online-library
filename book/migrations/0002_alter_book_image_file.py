# Generated by Django 3.2.7 on 2021-10-15 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image_file',
            field=models.ImageField(default='/imgs/placeholder.jpg', upload_to='book_covers'),
        ),
    ]
