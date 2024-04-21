from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("charts-data/", views.charts_data, name="charts-data")
]