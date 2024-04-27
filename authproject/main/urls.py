from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('profile/', views.profile_view, name='profile'),
    path('history/', views.history_view, name='history'),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.logout_view, name='logout'),

    path('routes/', views.validate_trops_view, name='routes'),
    path('routes/<str:route_id>/', views.some_trop_view, name='some_route'),
    path('routes/<str:route_id>/select', views.select_some_trop_view, name='go_some_route'),

    path('routes/<str:route_id>/vote', views.vote_some_trop_view, name='vote_some_route'),
    path('routes/<str:route_id>/donate', views.donate_some_trop_view, name='donate_some_route'),

    path('routes/<str:route_id>/go', views.go_some_trop_view, name='go_some_route'),
    path('routes/<str:route_id>/end', views.end_some_trop_view, name='end_some_route'),

    path('profile/add_money/<int:sum>/', views.add_money_view, name='add_money'),

    path('profile/admin/change_state/', views.change_state, name='admin_golos'),
]
