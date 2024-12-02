from django.db import models
from django.forms import ValidationError
from accounts.models import CustomUser
from movies.models import Movie
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Cinema(models.Model):
    capacity = models.PositiveIntegerField(default=0)
    cinema_name = models.CharField(max_length=100, default="")

def default_seat_matrix():
    return [[False for _ in range(12)] for _ in range(5)]


class ScheduledMovie(models.Model):
    cinema = models.ForeignKey(
        Cinema, 
        on_delete=models.CASCADE, 
        related_name="cinema_scheduled_movies"
    )
    
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE, 
        related_name="scheduled_movies"
    )
    
    audience_number = models.PositiveIntegerField(default=0)
    schedule = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    seats = models.JSONField(default=default_seat_matrix)  

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cinema', 'movie', 'schedule'], name='unique_scheduled_movie')
        ]

    def clean(self):
        if not self.movie.now_showing:
            raise ValidationError(f"The movie '{self.movie}' is not marked as now showing.")

    def update_seat_matrix(self):
        tickets = Ticket.objects.filter(scheduled_movie=self, is_active=True)
        seat_matrix = default_seat_matrix()
        seat_map = {
            f"{chr(row + 65)}{col + 1}": (row, col)
            for row in range(5)
            for col in range(12)
        }   

        for ticket in tickets:
            seat_id = ticket.seat_identifier
            if seat_id in seat_map:
                row, col = seat_map[seat_id]
                seat_matrix[row][col] = True
                
        self.audience_number = tickets.count()
        self.seats = seat_matrix
        self.save()
    
class Ticket(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name="user_tickets"
    )
    
    scheduled_movie = models.ForeignKey(
        ScheduledMovie, 
        on_delete=models.CASCADE, 
        related_name="movie_tickets"
    )
    
    seat_identifier = models.CharField(
        max_length=3, 
        default="Z1" 
    )
    is_active = models.BooleanField(default=True)
    
@receiver(post_save, sender=Ticket)
def update_seat_matrix_on_ticket_creation(sender, instance, created, **kwargs):
    if created:
        instance.scheduled_movie.update_seat_matrix()

@receiver(post_delete, sender=Ticket)
def update_seat_matrix_on_ticket_deletion(sender, instance, **kwargs):
    instance.scheduled_movie.update_seat_matrix()