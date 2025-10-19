from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('food-items/', views.food_items, name='food_items'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),
]
