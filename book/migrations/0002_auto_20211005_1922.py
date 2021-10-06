# Generated by Django 3.2.7 on 2021-10-05 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='gutenberg_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='copies_available',
            field=models.PositiveIntegerField(default=2),
        ),
    ]
