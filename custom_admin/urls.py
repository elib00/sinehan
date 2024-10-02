from django.urls import path
from .views import AdminLoginView
# from django.views.generic import RedirectView

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin_login")
]