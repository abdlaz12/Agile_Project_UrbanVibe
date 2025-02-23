from django.shortcuts import render

def index(request):
    return render(request, 'WebPage/index.html')

def about_us(request):
    return render(request, 'WebPage/about_us.html')

def login_page(request):
    return render(request, 'WebPage/login_page.html')

def favorites(request):
    return render(request, 'WebPage/favorites.html')

