from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.hr_dashboard, name='dashboard'),
]