import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from django.urls import reverse


def home(request):
    # Fetch categories and food items from API
    api_base = request.build_absolute_uri('/api/')
    try:
        categories_response = requests.get(f'{api_base}categories/')
        categories = categories_response.json(
        ) if categories_response.status_code == 200 else []
    except:
        categories = []

    try:
        food_items_response = requests.get(f'{api_base}food-items/')
        food_items = food_items_response.json(
        ) if food_items_response.status_code == 200 else []
    except:
        food_items = []

    context = {
        'categories': categories,
        'food_items': food_items,
    }
    return render(request, 'frontend/home.html', context)


def food_items(request):
    category = request.GET.get('category')
    search = request.GET.get('search')
    api_base = request.build_absolute_uri('/api/')
    url = f'{api_base}food-items/'
    params = {}
    if category:
        params['category'] = category
    if search:
        params['search'] = search

    try:
        response = requests.get(url, params=params)
        food_items = response.json() if response.status_code == 200 else []
    except:
        food_items = []

    context = {
        'food_items': food_items,
        'category': category,
        'search': search,
    }
    return render(request, 'frontend/food_items.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to view your cart.')
        return redirect('login')
    api_base = request.build_absolute_uri('/api/')
    try:
        response = requests.get(f'{api_base}carts/my_cart/', headers={
            'Authorization': f'Token {request.user.auth_token.key}'
        })
        cart_data = response.json() if response.status_code == 200 else {}
    except:
        cart_data = {}
    context = {
        'cart': cart_data,
    }
    return render(request, 'frontend/cart.html', context)
