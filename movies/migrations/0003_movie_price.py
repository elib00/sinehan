# Generated by Django 5.1.1 on 2024-11-24 04:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0002_movie_now_showing"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="price",
            field=models.FloatField(default=0),
        ),
    ]