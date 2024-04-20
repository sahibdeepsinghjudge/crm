from django.urls import path
from . import views

urlpatterns = [
    path('add-products/', views.add_products, name='add-products'),
    path('add-product',views.add_product, name='add-product'),
    path('edit-product/<int:id>/',views.edit_product, name='edit-product'),
    path("view-products/", views.view_products, name="view-products"),
    path("delete-product/<int:id>/", views.delete_product, name="delete-product"),
    path("search-products/", views.search_products, name="search-products"),
    path("initiate-order/", views.initiate_order, name="initiate-order")
]