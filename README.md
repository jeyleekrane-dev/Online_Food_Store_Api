# Online Food Store API

A full-stack web application for an online food ordering system built with Django and Django REST Framework.

## Description

This project consists of a RESTful API backend powered by Django REST Framework and a frontend built using Django templates. It allows customers to browse food items, place orders, manage carts, and leave reviews, while sellers can manage their food listings.

## Features

- **User Management**: Custom user model with roles (Customer and Seller)
- **Food Items**: Sellers can add and manage food items with categories, prices, and images
- **Ordering System**: Customers can place orders, track status, and manage order history
- **Shopping Cart**: Persistent cart functionality for customers
- **Reviews and Ratings**: Customers can review and rate food items
- **Favorites**: Customers can save favorite food items
- **Authentication**: Token-based authentication for API access
- **Admin Panel**: Django admin interface for administrative tasks

## Tech Stack

- **Backend**: Django 5.2, Django REST Framework
- **Database**: SQLite (development), configurable for production
- **Frontend**: Django Templates, HTML, CSS
- **Authentication**: Token Authentication, Session Authentication
- **Media Handling**: Image uploads for food items

## Project Structure

```
online_food_store_api/
├── api/                    # REST API app
│   ├── models.py          # Database models
│   ├── views.py           # API views and viewsets
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # API URL patterns
│   └── management/commands/populate_db.py  # Database population command
├── frontend/              # Frontend app
│   ├── templates/         # HTML templates
│   ├── views.py           # Frontend views
│   └── urls.py            # Frontend URL patterns
├── food_store/            # Main Django project
│   ├── settings.py        # Project settings
│   └── urls.py            # Main URL configuration
├── vnv/                   # Virtual environment (not tracked)
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
└── README.md              # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create and activate virtual environment**:
   ```bash
   python -m venv vnv
   vnv\Scripts\activate  # On Windows
   # source vnv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install django djangorestframework
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Populate the database with sample data**:
   ```bash
   python manage.py populate_db
   ```

6. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### API Endpoints

The API is accessible at `/api/` and includes the following main endpoints:

- `/api/users/` - User management
- `/api/categories/` - Food categories
- `/api/food-items/` - Food items
- `/api/orders/` - Order management
- `/api/carts/` - Shopping cart
- `/api/reviews/` - Reviews and ratings
- `/api/favorites/` - Favorite items

### Authentication

For API access, include the Authorization header:
```
Authorization: Token <your-token>
```

### Frontend Pages

- `/` - Home page
- `/food-items/` - Browse food items
- `/login/` - User login
- `/logout/` - User logout
- `/cart/` - Shopping cart
- `/admin/` - Django admin panel


