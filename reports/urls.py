from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('add/<int:player_id>/', views.add_report, name='add_report'),
    path('<int:pk>/edit/', views.report_edit, name='report_edit'),
    path('<int:pk>/delete/', views.report_delete, name='report_delete'),
]