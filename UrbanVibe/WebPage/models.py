from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import login
from django.contrib import messages
from django import forms

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

class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'address', 'password']


from django.db import models

# Kategori utama produk
class ProductCategory(models.TextChoices):
    FASHION = "Fashion", "Fashion"
    BEAUTY = "Beauty", "Beauty"
    ACCESSORIES = "Accessories", "Accessories"

# Subkategori Fashion
class FashionSubCategory(models.TextChoices):
    DRESS = "Dress", "Dress"
    SHIRT = "Shirt", "Shirt"
    OUTERWEAR = "Outerwear", "Outerwear"
    BOTTOM = "Bottom", "Bottom"

# Jenis fashion berdasarkan tipe
class BottomType(models.TextChoices):
    PANTS = "Pants", "Pants"
    SKIRT = "Skirt", "Skirt"
    SHORTS = "Shorts", "Shorts"

# Jenis fashion berdasarkan tipe
class Outerwear(models.TextChoices):
    CARDIGAN = "Cardigan", "Cardigan"
    JACKET = "Jacket", "Jacket"
    SWEATERS = "Sweaters", "Sweaters"
    HOODIE = "Hoodie", "Hoodie"

# Jenis fashion berdasarkan tipe
class ShirtType(models.TextChoices):
    SHORT_SLEEVE = "Short Sleeve", "Short Sleeve"
    SHORT_CROP = "Short Crop", "Short Crop"
    LONG_SLEEVE = "Long Sleeve", "Long Sleeve"

# Gabungkan semua choices untuk fashion_type
FASHION_TYPE_CHOICES = [
    *ShirtType.choices,
    *BottomType.choices,
    *Outerwear.choices,
]

# Pilihan ukuran fashion
class Size(models.TextChoices):
    XS = "XS", "XS"
    S = "S", "S"
    M = "M", "M"
    L = "L", "L"
    XL = "XL", "XL"
    XXL = "XXL", "XXL"

class ColorChoices(models.TextChoices):
    RED = "Red", "Red"
    BLUE = "Blue", "Blue"
    GREEN = "Green", "Green"
    BLACK = "Black", "Black"
    WHITE = "White", "White"
    YELLOW = "Yellow", "Yellow"

# Jenis Beauty
class BeautyType(models.TextChoices):
    AIR_CUSHION = "Air Cushion", "Air Cushion"
    WATER_CUSHION = "Water Cushion", "Water Cushion"
    CREAM_CUSHION = "Cream Cushion", "Cream Cushion"

# Model abstrak untuk produk
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=ProductCategory.choices)

    class Meta:
        abstract = True  # Tidak akan dibuat sebagai tabel

# Model Fashion
class Fashion(Product):
    sub_category = models.CharField(max_length=20, choices=FashionSubCategory.choices)
    color = models.CharField(max_length=20, choices=ColorChoices.choices)
    size = models.CharField(max_length=5, choices=Size.choices)
    fashion_type = models.CharField(max_length=15, choices=FASHION_TYPE_CHOICES)  # Perbaikan di sini

    def __str__(self):
        return f"{self.name} ({self.sub_category})"

# Model Beauty
class Beauty(Product):
    makeup_type = models.CharField(max_length=20, choices=BeautyType.choices)

    def __str__(self):
        return f"{self.name} ({self.makeup_type})"

# Model Accessories
class Accessories(Product):
    def __str__(self):
        return f"{self.name}"

# Model untuk menyimpan gambar produk
class ProductImage(models.Model):
    fashion = models.ForeignKey(Fashion, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    beauty = models.ForeignKey(Beauty, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    accessories = models.ForeignKey(Accessories, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.fashion or self.beauty or self.accessories}"