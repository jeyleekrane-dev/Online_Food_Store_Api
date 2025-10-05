from rest_framework import serializers
from .models import User, Category, FoodItem, Order, OrderItem, Cart, CartItem, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'first_name', 'last_name', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FoodItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name', read_only=True)
    seller_name = serializers.CharField(
        source='seller.username', read_only=True)

    class Meta:
        model = FoodItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.CharField(
        source='food_item.name', read_only=True)
    food_item_price = serializers.DecimalField(
        source='food_item.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(
        source='customer.username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.CharField(
        source='food_item.name', read_only=True)
    food_item_price = serializers.DecimalField(
        source='food_item.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = '__all__'

    def get_total_price(self, obj):
        return obj.quantity * obj.food_item.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        return sum(item.quantity * item.food_item.price for item in obj.items.all())


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='customer.username', read_only=True)
    food_item_name = serializers.CharField(
        source='food_item.name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
