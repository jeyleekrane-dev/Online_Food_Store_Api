from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User, Category, FoodItem, Order, OrderItem, Cart, CartItem, Review
from .serializers import (
    UserSerializer, UserRegistrationSerializer, CategorySerializer,
    FoodItemSerializer, OrderSerializer, OrderItemSerializer,
    CartSerializer, CartItemSerializer, ReviewSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FoodItem.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.role != 'seller':
            raise PermissionError("Only sellers can create food items")
        serializer.save(seller=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'customer':
            return Order.objects.filter(customer=self.request.user)
        elif self.request.user.role == 'seller':
            return Order.objects.filter(items__food_item__seller=self.request.user).distinct()
        return Order.objects.none()

    @action(detail=True, methods=['post'])
    def place_order(self, request, pk=None):
        cart = Cart.objects.get(customer=request.user)
        cart_items = cart.items.all()
        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(customer=request.user)
        total = 0
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.food_item.price
            )
            total += item.quantity * item.food_item.price
        order.total_amount = total
        order.save()
        cart_items.delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return Response(OrderSerializer(order).data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user)
        food_item_id = request.data.get('food_item_id')
        quantity = request.data.get('quantity', 1)
        food_item = FoodItem.objects.get(id=food_item_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, food_item=food_item,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart = Cart.objects.get(customer=request.user)
        food_item_id = request.data.get('food_item_id')
        CartItem.objects.filter(cart=cart, food_item_id=food_item_id).delete()
        return Response(CartSerializer(cart).data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
