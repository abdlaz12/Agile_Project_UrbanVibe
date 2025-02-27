from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('login_page', views.login_page, name='login_page'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('favorites/', views.favorites, name='favorites'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('product/', views.product_detail, name='product_detail'),
    path('shoppingcart/', views.shoppingcart, name='shoppingcart'),
    path('invoice/', views.invoice, name='invoice'),
    path('cart/', views.cart_view, name='cart'),

]
