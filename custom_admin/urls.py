from django.urls import path
from .views import AdminLoginView, AdminDashboardView, AdminAddMovieView
# from django.views.generic import RedirectView

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin_login"), 
    path("dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("dashboard/add-movie", AdminAddMovieView.as_view(), name="admin_dashboard_add_movie"),
    # path("dashboard/movies/<str:category>", DashboardMoviesView.as_view(), name="admin_dashboard_movies"),
]