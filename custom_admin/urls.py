from django.urls import path, reverse_lazy
from .views import (
    AdminLoginView, AdminDashboardView, AdminDashboardAddUserView, 
    AdminDashboardAllUsersView, AdminLogoutView, AdminDashboardUpdateUserView, AdminDashboardTicketsView, AdminDashboardAddTicketView, AdminDashboardCinema, 
    AdminDashboardAddNowShowing, AdminDashboardAddCinema, AdminDashboardMovieListView,
    AdminDashboardAddMovieView, AdminDashboardAddScheduledMovieView)
from django.views.generic import RedirectView

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin_login"), 
    path("logout/", AdminLogoutView.as_view(), name="admin_logout"),
    # path("dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("dashboard/", RedirectView.as_view(url=reverse_lazy('admin_dashboard_add_user'), permanent=True), name="admin_dashboard"),
    path("dashboard/add_user/", AdminDashboardAddUserView.as_view(), name="admin_dashboard_add_user"),
    path("dashboard/all_users/", AdminDashboardAllUsersView.as_view(), name="admin_dashboard_all_users"),
    path("dashboard/update_user/<int:user_id>/", AdminDashboardUpdateUserView.as_view(), name="admin_dashboard_update_user"),
    path("dashboard/movie_list/", AdminDashboardMovieListView.as_view(), name="admin_dashboard_movie_list"),
    path("dashboard/add_movie/", AdminDashboardAddMovieView.as_view(), name="admin_dashboard_add_movie"),
    path("dashboard/add_scheduled_movie/", AdminDashboardAddScheduledMovieView.as_view(), name="admin_dashboard_add_scheduled_movie"),
    path("dashboard/tickets/", AdminDashboardTicketsView.as_view(), name="admin_dashboard_tickets"),
    path("dashboard/add_ticket/", AdminDashboardAddTicketView.as_view(), name="admin_dashboard_add_ticket"),
    path("dashboard/cinema/", AdminDashboardCinema.as_view(), name="admin_dashboard_cinema"),
    path("dashboard/cinema/add_now_showing", AdminDashboardAddNowShowing.as_view(), name="admin_dashboard_add_now_showing"),
    path("dashboard/cinema/add_cinema", AdminDashboardAddCinema.as_view(), name="admin_dashboard_add_cinema")
]