
from django.urls import path, include
from sinehan.views import movies_view
from .views import movie_details
from .views import movie_book, movie_book_purchase

urlpatterns = [
    path('', movies_view, name='movies'),
    path('<int:movie_id>/', movie_details, name='movie_details'),
    path('<int:movie_id>/book/', movie_book, name='movie_book'),
    path('<int:movie_id>/book/purchase/', movie_book_purchase, name='purchase')
]
