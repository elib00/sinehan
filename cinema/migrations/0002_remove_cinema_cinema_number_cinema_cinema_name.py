# Generated by Django 5.1.1 on 2024-11-02 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cinema',
            name='cinema_number',
        ),
        migrations.AddField(
            model_name='cinema',
            name='cinema_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
