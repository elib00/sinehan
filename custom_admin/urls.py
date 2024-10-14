from django.urls import path
from .views import AdminLoginView, AdminDashboardView, AdminDashboardAddUserView, AdminDashboardAllUsersView
# from django.views.generic import RedirectView

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin_login"), 
    path("dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("dashboard/add_user/", AdminDashboardAddUserView.as_view(), name="admin_dashboard_add_user"),
    path("dashboard/all_users/", AdminDashboardAllUsersView.as_view(), name="admin_dashboard_all_users")
]