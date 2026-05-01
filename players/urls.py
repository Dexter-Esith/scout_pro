from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('players/', views.player_list, name='player_list'),
    path('players/add/', views.player_add, name='player_add'),
    path('players/<int:pk>/', views.player_detail, name='player_detail'),
    path('players/<int:pk>/edit/', views.player_edit, name='player_edit'),
    path('players/<int:pk>/delete/', views.player_delete, name='player_delete'),
    path('players/<int:pk>/photo/', views.player_photo_upload, name='player_photo_upload'),
    path('players/<int:pk>/shortlist/', views.shortlist_toggle, name='shortlist_toggle'),
    path('shortlist/', views.shortlist, name='shortlist'),
    path('compare/', views.player_compare, name='player_compare'),
]