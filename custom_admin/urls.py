from django.urls import path, reverse_lazy
from .views import (
    AdminLoginView, AdminDashboardView, AdminDashboardAddUserView, 
    AdminDashboardAllUsersView, AdminLogoutView, AdminDashboardUpdateUserView, 
    AdminDashboardMovieList, AdminDashboardTickets, AdminDashboardCinema)
from django.views.generic import RedirectView

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin_login"), 
    path("logout/", AdminLogoutView.as_view(), name="admin_logout"),
    # path("dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("dashboard/", RedirectView.as_view(url=reverse_lazy('admin_dashboard_add_user'), permanent=True), name="admin_dashboard"),
    path("dashboard/add_user/", AdminDashboardAddUserView.as_view(), name="admin_dashboard_add_user"),
    path("dashboard/all_users/", AdminDashboardAllUsersView.as_view(), name="admin_dashboard_all_users"),
    path("dashboard/update_user/<int:user_id>/", AdminDashboardUpdateUserView.as_view(), name="admin_dashboard_update_user"),
    path("dashboard/movie_list/", AdminDashboardMovieList.as_view(), name="admin_dashboard_movie_list"),
    path("dashboard/tickets/", AdminDashboardTickets.as_view(), name="admin_dashboard_tickets"),
    path("dashboard/cinema/", AdminDashboardCinema.as_view(), name="admin_dashboard_cinema")
]