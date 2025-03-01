
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerLoginForm


from django.shortcuts import render
from .models import *


def index(request):
    return render(request, 'WebPage/index.html')

def about_us(request):
    return render(request, 'WebPage/about_us.html')

def sign_up(request):
    return render(request, 'WebPage/sign_up.html')

def favorites(request):
    return render(request, 'WebPage/favorites.html')

def catalogue(request):
    category = request.GET.get('category', None)  # Get category from URL query
    subcategory = request.GET.get('subcategory', None)  # Get subcategory from URL query

    # Fetch products based on filters
    if category == "fashion":
        if subcategory:
            fashion_products = Fashion.objects.filter(sub_category=subcategory)
        else:
            fashion_products = Fashion.objects.all()
        beauty_products = []
        accessories_products = []
    elif category == "beauty":
        fashion_products = []
        beauty_products = Beauty.objects.all()
        accessories_products = []
    elif category == "accessories":
        fashion_products = []
        beauty_products = []
        accessories_products = Accessories.objects.all()
    else:
        # Show all products if no category is selected
        fashion_products = Fashion.objects.all()
        beauty_products = Beauty.objects.all()
        accessories_products = Accessories.objects.all()

    return render(request, "WebPage/catalogue.html", {
        "fashion_products": fashion_products,
        "beauty_products": beauty_products,
        "accessories_products": accessories_products,
    })

def shoppingcart(request):
    return render(request, 'WebPage/shoppingcart.html')

def invoice(request):
    return render(request, 'WebPage/invoice.html')

def fashion_detail(request, pk):
    fashion = Fashion.objects.get(pk=pk)
    return render(request, 'fashion_detail.html', {'fashion': fashion})

def beauty_detail(request, pk):
    beauty = Beauty.objects.get(pk=pk)
    return render(request, 'beauty_detail.html', {'beauty': beauty})

def accessories_detail(request, pk):
    accessories = Accessories.objects.get(pk=pk)
    return render(request, 'WebPage/accessories_detail.html', {'accessories': accessories})


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'WebPage/register.html', {'form': form})

def login_customer(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            print(f"Attempting login with email: {email}")  # Debugging

            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Tentukan backend yang digunakan
                login(request, user, backend='WebPage.backends.EmailBackend')
                messages.success(request, 'Login successful!')
                print(f"Login successful for user: {user.email}")  # Debugging
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password.')
                print("Login failed: Invalid email or password")  # Debugging
        else:
            print("Form validation failed")  # Debugging
    else:
        form = CustomerLoginForm()
    
    return render(request, 'WebPage/login.html', {'form': form})


def logout_customer(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'WebPage/userprofile.html', {'user': request.user})

def product_detail(request):
    product = product.objects.all()  
    return render(request, 'product_detail.html', {'product':product})

def cart(request):
    return render(request, 'WebPage/shoppingcart.html')