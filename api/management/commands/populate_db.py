from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Category, FoodItem, Cart
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database...')

        # Create categories
        categories_data = [
            {'name': 'Pizza', 'description': 'Delicious pizzas'},
            {'name': 'Burgers', 'description': 'Juicy burgers'},
            {'name': 'Desserts', 'description': 'Sweet treats'},
        ]
        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(cat)
            if created:
                self.stdout.write(f'Created category: {cat.name}')

        # Create sellers
        sellers_data = [
            {'username': 'seller1', 'email': 'seller1@example.com',
                'password': 'pass123', 'role': 'seller'},
            {'username': 'seller2', 'email': 'seller2@example.com',
                'password': 'pass123', 'role': 'seller'},
        ]
        sellers = []
        for seller_data in sellers_data:
            seller, created = User.objects.get_or_create(
                username=seller_data['username'],
                defaults={
                    'email': seller_data['email'],
                    'role': seller_data['role']
                }
            )
            if created:
                seller.set_password(seller_data['password'])
                seller.save()
                self.stdout.write(f'Created seller: {seller.username}')
            sellers.append(seller)

        # Create customers
        customers_data = [
            {'username': 'customer1', 'email': 'customer1@example.com',
                'password': 'pass123', 'role': 'customer'},
            {'username': 'customer2', 'email': 'customer2@example.com',
                'password': 'pass123', 'role': 'customer'},
            {'username': 'customer3', 'email': 'customer3@example.com',
                'password': 'pass123', 'role': 'customer'},
        ]
        customers = []
        for cust_data in customers_data:
            customer, created = User.objects.get_or_create(
                username=cust_data['username'],
                defaults={
                    'email': cust_data['email'],
                    'role': cust_data['role']
                }
            )
            if created:
                customer.set_password(cust_data['password'])
                customer.save()
                self.stdout.write(f'Created customer: {customer.username}')
            customers.append(customer)

        # Create food items
        food_items_data = [
            # Pizza
            {'name': 'Margherita Pizza', 'description': 'Classic cheese pizza',
                'price': 12.99, 'category': categories[0]},
            {'name': 'Pepperoni Pizza', 'description': 'Spicy pepperoni pizza',
                'price': 14.99, 'category': categories[0]},
            {'name': 'Veggie Pizza', 'description': 'Loaded with vegetables',
                'price': 13.99, 'category': categories[0]},
            {'name': 'BBQ Chicken Pizza', 'description': 'Tangy BBQ chicken',
                'price': 15.99, 'category': categories[0]},
            {'name': 'Hawaiian Pizza', 'description': 'Ham and pineapple',
                'price': 14.49, 'category': categories[0]},
            # Burgers
            {'name': 'Classic Burger', 'description': 'Beef patty with lettuce and tomato',
                'price': 9.99, 'category': categories[1]},
            {'name': 'Cheese Burger', 'description': 'With melted cheese',
                'price': 10.99, 'category': categories[1]},
            {'name': 'Bacon Burger', 'description': 'Crispy bacon added',
                'price': 11.99, 'category': categories[1]},
            {'name': 'Veggie Burger', 'description': 'Plant-based patty',
                'price': 8.99, 'category': categories[1]},
            {'name': 'Double Burger', 'description': 'Two beef patties',
                'price': 13.99, 'category': categories[1]},
            # Desserts
            {'name': 'Chocolate Cake', 'description': 'Rich chocolate cake',
                'price': 6.99, 'category': categories[2]},
            {'name': 'Ice Cream Sundae', 'description': 'Vanilla ice cream with toppings',
                'price': 5.99, 'category': categories[2]},
            {'name': 'Cheesecake', 'description': 'Creamy cheesecake',
                'price': 7.49, 'category': categories[2]},
            {'name': 'Brownies', 'description': 'Fudgy chocolate brownies',
                'price': 4.99, 'category': categories[2]},
            {'name': 'Fruit Salad', 'description': 'Fresh seasonal fruits',
                'price': 5.49, 'category': categories[2]},
        ]
        for item_data in food_items_data:
            seller = random.choice(sellers)
            item, created = FoodItem.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'description': item_data['description'],
                    'price': item_data['price'],
                    'category': item_data['category'],
                    'seller': seller,
                }
            )
            if created:
                self.stdout.write(
                    f'Created food item: {item.name} by {seller.username}')

        # Create carts for customers
        for customer in customers:
            cart, created = Cart.objects.get_or_create(customer=customer)
            if created:
                self.stdout.write(f'Created cart for: {customer.username}')

        self.stdout.write('Database populated successfully!')
