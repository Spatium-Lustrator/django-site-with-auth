from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('profile/', views.profile_view, name='profile'),
    path('vote/', views.vote_view, name='vote'),
    path('basic_vote/', views.basic_vote_view, name='basic_vote'),
    path('federal_vote/', views.basic_vote_view, name='federal_vote'),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('email-confirmed/', views.EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email-confirmation-sent/', views.EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email-failed/', views.EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('confirm-email/<str:uidb64>/<str:token>/', views.UserConfirmEmailView.as_view(), name='confirm_email')
]