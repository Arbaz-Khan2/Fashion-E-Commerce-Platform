from django.urls import path, include
from .views import register_user, login_user, manage_profile, manage_category, manage_brand, manage_product, manage_cart, checkout, get_orders, add_review, get_reviews, get_search_history, get_seggestions

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('profile/', manage_profile, name='manage_profile'),
    path('product-catalog/categories/', manage_category, name='manage_category'),
    path('product-catalog/brands/', manage_brand, name='manage_brand'),
    path('product-catalog/products/', manage_product, name='manage_product'),
    path('cart/', manage_cart, name='manage_cart'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', get_orders, name='get_orders'),
    path('add_review/', add_review, name='add_review'),
    path('reviews/', get_reviews, name='get_reviews'),
    path('search_history/', get_search_history, name='get_search_history'),
    path('suggestions/', get_seggestions, name='get_seggestions'),
]
