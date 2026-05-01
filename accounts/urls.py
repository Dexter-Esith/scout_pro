from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        http_method_names=['get', 'post'],
        next_page='/accounts/login/'
    ), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('scouts/', views.scout_list, name='scout_list'),
    path('scouts/<int:pk>/', views.scout_profile, name='scout_profile'),
]