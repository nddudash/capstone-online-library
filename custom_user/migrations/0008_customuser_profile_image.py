# Generated by Django 3.2.7 on 2021-10-18 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0007_remove_customuser_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='imgs/profile.jpg', null=True, upload_to='profile_pic'),
        ),
    ]
