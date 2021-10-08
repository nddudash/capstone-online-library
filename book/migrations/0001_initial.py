# Generated by Django 3.2.7 on 2021-10-08 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.URLField(max_length=1500)),
                ('author', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('copies_available', models.PositiveIntegerField(default=2)),
                ('gutenberg_id', models.IntegerField(default=0)),
                ('is_reserved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, max_length=500, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_comment', to='book.book')),
            ],
        ),
    ]
