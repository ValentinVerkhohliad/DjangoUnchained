from django.urls import path
from ecomapp.views import base_view, category_view, product_view, cart_view, add_to_cart_view, remove_from_cart_view,\
    change_item_qty

urlpatterns = [
    path('category/<category_slug>/', category_view, name='category_detail'),
    path('product/<product_slug>/', product_view, name='product_detail'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('change_item_qty/', change_item_qty, name='change_item_qty'),
    path('cart/', cart_view, name='cart'),
    path('', base_view, name='base'),
]
