from django.urls import path
from . import views

urlpatterns = [
    path('add-products/', views.add_products, name='add-products'),
    path('add-product',views.add_product, name='add-product'),
    path('edit-product/<int:id>/',views.edit_product, name='edit-product'),
    path("view-products/", views.view_products, name="view-products"),
    path("delete-product/<int:id>/", views.delete_product, name="delete-product"),
    path("search-products/", views.search_products, name="search-products"),
    path("search-products-catalog/", views.search_products_catalog, name="search-products-catalog"),
    path("initiate-order/", views.initiate_order, name="initiate-order"),
    path("catalog/", views.product_catalog, name="catalog"),
    path("billing/",views.billing_cart, name="billing"),
    path("add-to-cart/<int:id>",views.add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<int:index>",views.remove_from_cart, name="remove-from-cart"),
    path("complete-order/",views.complete_order, name="complete-order"),
    path("bill/<int:id>",views.bill, name="bill"),
    path("order-history/",views.order_records, name="order-records"),
]