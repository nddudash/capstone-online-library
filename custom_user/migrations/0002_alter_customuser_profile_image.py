# Generated by Django 3.2.7 on 2021-10-15 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='imgs/profile.jpg', null=True, upload_to='profile_pic'),
        ),
    ]
