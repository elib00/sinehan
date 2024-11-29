# Generated by Django 5.1.1 on 2024-11-20 05:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cinema", "0006_scheduledmovie_ticket"),
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="scheduledmovie",
            constraint=models.UniqueConstraint(
                fields=("cinema", "movie", "schedule"), name="unique_scheduled_movie"
            ),
        ),
    ]