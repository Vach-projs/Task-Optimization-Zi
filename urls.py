from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.upload_view, name='upload'),
]