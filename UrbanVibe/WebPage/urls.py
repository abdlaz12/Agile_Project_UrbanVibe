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
    path('product/<str:category>/<int:pk>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('apply-voucher/', views.apply_voucher, name='apply_voucher'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path("send-email/", views.send_subscription_email, name="send_email"),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
