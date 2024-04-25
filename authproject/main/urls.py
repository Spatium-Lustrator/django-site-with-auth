from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.RegisterView.as_view(), name="register")
]
