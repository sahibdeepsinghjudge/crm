from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login-page'),
    path('login/', views.login_handler, name='login'),
    path('create-account/', views.register_page, name='register-page'),
    path('register/', views.register, name='register'),

]