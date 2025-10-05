from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet, FoodItemViewSet, OrderViewSet, CartViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'food-items', FoodItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'carts', CartViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
