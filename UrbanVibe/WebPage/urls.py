from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('login_page', views.login_page, name='login_page'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('favorites/', views.favorites, name='favorites'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('shoppingcart/', views.shoppingcart, name='shoppingcart'),
    path('invoice/', views.invoice, name='invoice'),
    path('cart/', views.cart_view, name='cart'),
    path('product/', views.product_list, name='product_list'),
    path('register/', views.register_customer, name='register'),
    path('login/', views.login_customer, name='login'),
    path('logout/', views.logout_customer, name='logout'),
    path('fashion/<int:pk>/', views.fashion_detail, name='fashion_detail'),
    path('beauty/<int:pk>/', views.beauty_detail, name='beauty_detail'),
    path('accessories/<int:pk>/', views.accessories_detail, name='accessories_detail'),
    path('profile/', views.profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
