# Generated by Django 5.1.1 on 2024-11-03 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_remove_cinema_cinema_number_cinema_cinema_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledmovie',
            name='audience_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
