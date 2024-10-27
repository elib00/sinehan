
from django.urls import path, include
from sinehan.views import movies_view
from .views import movie_details

urlpatterns = [
    path('', movies_view, name='movies'),
    path('<int:movie_id>/', movie_details, name='movie_details'),
]
