from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store-home'),
    path("shop/<int:id>", views.shop, name="shop"),
]