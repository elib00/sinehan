from django.db import models
from django.forms import ValidationError
from accounts.models import CustomUser
from movies.models import Movie
# from django.contrib.auth import get_user_model

class Cinema(models.Model):
    capacity = models.PositiveIntegerField(default=0)
    cinema_name = models.CharField(max_length=100, default="")

# class NowShowingMovie(models.Model):
#     cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_showing_movies")
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showing_movies")
#     end_date = models.DateTimeField()
#     is_active = models.BooleanField(default=True)           
    
class ScheduledMovie(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_scheduled_movies")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="scheduled_movies")
    audience_number = models.PositiveIntegerField(default=0)
    schedule = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    seats = models.JSONField(default=list)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cinema', 'movie', 'schedule'], name='unique_scheduled_movie')
        ]

    def clean(self):
        # Check if the movie is "now showing"
        if not self.movie.now_showing:
            raise ValidationError(f"The movie '{self.movie}' is not marked as now showing.")
    
    def initialize_seats(self):
        self.seats = [[False for _ in range(5)] for _ in range(12)]
        self.save()
        
class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_tickets")
    scheduled_movie = models.ForeignKey(ScheduledMovie, on_delete=models.CASCADE, related_name="movie_tickets")
    seat_identifier = models.CharField(max_length=3, default="")
    is_active = models.BooleanField(default=True)