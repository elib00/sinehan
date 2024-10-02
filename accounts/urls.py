from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    # path('<int:id>/profile', views.profile_view, name='profile'),
    # path('<int:id>/update_profile', views.update_profile, name='update_profile'),
    # path('<int:id>/tickets', views.tickets_view, name='tickets'), 
    # path('<int:id>/history', views.history_view, name='history')
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('tickets/', views.tickets_view, name='tickets'), 
    path('history/', views.history_view, name='history')
]