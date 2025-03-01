from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('login/', views.login_customer, name='login'),
    path('logout/', views.logout_customer, name='logout'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('register/', views.register_customer, name='register'),
    path('favorites/', views.favorites, name='favorites'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('shoppingcart/', views.shoppingcart, name='shoppingcart'),
    path('invoice/', views.invoice, name='invoice'),
    path('fashion/<int:pk>/', views.fashion_detail, name='fashion_detail'),
    path('beauty/<int:pk>/', views.beauty_detail, name='beauty_detail'),
    path('accessories/<int:pk>/', views.accessories_detail, name='accessories_detail'),
    path('profile/', views.profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
