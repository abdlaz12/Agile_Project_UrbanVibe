from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django import forms
from multiselectfield import MultiSelectField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

# Fashion Choices
class FashionSubCategory(models.TextChoices):
    DRESS = "Dress", "Dress"
    SHIRT = "Shirt", "Shirt"
    OUTERWEAR = "Outerwear", "Outerwear"
    BOTTOM = "Bottom", "Bottom"

class FashionType(models.TextChoices):
    PANTS = "Pants", "Pants"
    SKIRT = "Skirt", "Skirt"
    SHORTS = "Shorts", "Shorts"
    CARDIGAN = "Cardigan", "Cardigan"
    JACKET = "Jacket", "Jacket"
    SWEATERS = "Sweaters", "Sweaters"
    HOODIE = "Hoodie", "Hoodie"
    SHORT_SLEEVE = "Short Sleeve", "Short Sleeve"
    SHORT_CROP = "Short Crop", "Short Crop"
    LONG_SLEEVE = "Long Sleeve", "Long Sleeve"

SIZE_CHOICES = [
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
]

COLOR_CHOICES = [
    ("White", "White"),
    ("Grey", "Grey"),
    ("Black", "Black"),
    ("Red", "Red"),
    ("Orange", "Orange"),
    ("Yellow", "Yellow"),
    ("Green", "Green"),
    ("Blue", "Blue"),
    ("Purple", "Purple"),
    ("Pink", "Pink"),
    ("Beige", "Beige"),
    ("Brown", "Brown"),
]

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    class Meta:
        abstract = True

# Fashion Model
class Fashion(Product):
    sub_category = models.CharField(max_length=20, choices=FashionSubCategory.choices)
    color = MultiSelectField(choices=COLOR_CHOICES, max_length=100)  # Allows multiple colors
    size = MultiSelectField(choices=SIZE_CHOICES, max_length=50)  # Allows multiple sizes
    fashion_type = models.CharField(max_length=15, null=True, blank=True, choices=FashionType.choices)
    
    def __str__(self):
        return f"{self.name} ({self.sub_category})"

# Beauty Model
class Beauty(Product):
    class BeautyType(models.TextChoices):
        FACE = "Face", "Face"
        EYE = "Eye", "Eye"
        LIPS = "Lips", "Lips"

    makeup_type = models.CharField(max_length=20, choices=BeautyType.choices)

    def __str__(self):
        return f"{self.name} ({self.makeup_type})"

# Accessories Model
class Accessories(Product):
    def __str__(self):
        return self.name

# Product Images
class ProductImage(models.Model):
    fashion = models.ForeignKey(Fashion, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    beauty = models.ForeignKey(Beauty, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    accessories = models.ForeignKey(Accessories, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.fashion or self.beauty or self.accessories}"
    
# Order Model for Shopping Cart
class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    voucher_code = models.CharField(max_length=20, null=True, blank=True)
    discount_amount = models.IntegerField(default=0)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_final_total(self):
        total = self.get_cart_total
        tax = int(total * 0.10)  # 10% tax
        final_total = total + tax - self.discount_amount
        return final_total, tax
    
    def __str__(self):
        return f"Order {self.id} - {self.user.email if self.user else 'Guest'}"

# OrderItem Model
class OrderItem(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ('fashion', 'Fashion'),
        ('beauty', 'Beauty'),
        ('accessories', 'Accessories'),
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)
    product_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    
    @property
    def get_product(self):
        try:
            if self.product_type == 'fashion':
                return Fashion.objects.get(product_id=self.product_id)
            elif self.product_type == 'beauty':
                return Beauty.objects.get(product_id=self.product_id)
            elif self.product_type == 'accessories':
                return Accessories.objects.get(product_id=self.product_id)
        except (Fashion.DoesNotExist, Beauty.DoesNotExist, Accessories.DoesNotExist):
            return None
        return None
    
    @property
    def get_total(self):
        product = self.get_product
        return product.price * self.quantity if product else 0
    
    def __str__(self):
        product = self.get_product
        return f"{self.quantity} x {product.name if product else 'Unknown Product'}"

# Shipping Address Model
class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address

    @property
    def get_product(self):
        try:
            if self.product_type == 'fashion':
                return Fashion.objects.get(product_id=self.product_id)
            elif self.product_type == 'beauty':
                return Beauty.objects.get(product_id=self.product_id)
            elif self.product_type == 'accessories':
                return Accessories.objects.get(product_id=self.product_id)
        except (Fashion.DoesNotExist, Beauty.DoesNotExist, Accessories.DoesNotExist):
            return None
        return None
    
    def __str__(self):
        product = self.get_product
        return f"{product.name if product else 'Unknown Product'}"