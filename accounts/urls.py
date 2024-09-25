from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('<str:username>/profile', views.profile_view, name='profile'),
    path('<str:username>/tickets', views.tickets_view, name='tickets'), 
    path('<str:username>/history', views.history_view, name='history'), 
]