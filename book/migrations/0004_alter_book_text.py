# Generated by Django 3.2.7 on 2021-10-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_book_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='text',
            field=models.URLField(max_length=1500),
        ),
    ]