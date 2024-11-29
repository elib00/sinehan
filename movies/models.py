from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

def media_path(instance, filename): 
    return f'{filename}' 

class Movie(models.Model):
    movie_name = models.CharField(max_length=50)
    director = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    synopsis = models.TextField()
    cast = models.TextField()
    duration = models.DurationField()
    movie_format = models.CharField(
        max_length=2, 
        choices=[("2D", "2D"), ("3D", "3D")], 
        default="2D"
    )
    movie_rating = models.CharField(
        max_length=10,
        choices=[("G", "General Audience"), ("PG", "Parental Guidance"),
                 ("R-13", "Restricted-13"), ("R-16", "Restricted-16"),
                 ("R-18", "Restricted-18")],
        default="G"
    )
    genre = models.CharField(max_length=100)
    now_showing = models.BooleanField(default=True)
    price = models.FloatField(default=0)
    
    poster_portrait = models.ImageField(upload_to=media_path, default="")
    poster_landscape = models.ImageField(upload_to=media_path, default="")
    poster_trailer = models.FileField(upload_to=media_path, default="")

