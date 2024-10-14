from django.urls import path
from .views import AdminLoginView, AdminDashboardView, AdminDashboardAddUserView
# from django.views.generic import RedirectView

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin_login"), 
    path("dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("dashboard/add_user/", AdminDashboardAddUserView.as_view(), name="admin_dashboard_add_user")
]