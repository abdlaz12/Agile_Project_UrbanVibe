from django.shortcuts import render

def index(request):
    return render(request, 'WebPage/index.html')

def about_us(request):
    return render(request, 'WebPage/about_us.html')

def sign_up(request):
    return render(request, 'WebPage/sign_up.html')

def login_page(request):
    return render(request, 'WebPage/login_page.html')

def favorites(request):
    return render(request, 'WebPage/favorites.html')

def catalogue(request):
    return render(request, 'WebPage/catalogue.html')

def product_detail(request):
    return render(request, 'WebPage/product_detail.html')

def shoppingcart(request):
    return render(request, 'WebPage/shoppingcart.html')

def invoice(request):
    return render(request, 'WebPage/invoice.html')


def cart_view(request):
    return render(request, 'WebPage/shoppingcart.html')  #