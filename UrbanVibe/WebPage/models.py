from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django import forms
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    class Meta:
        abstract = True

# Fashion Model
class Fashion(Product):
    sub_category = models.CharField(max_length=20, choices=FashionSubCategory.choices)
    color = MultiSelectField(choices=COLOR_CHOICES, max_length=100)
    size = MultiSelectField(choices=SIZE_CHOICES, max_length=50)
    fashion_type = models.CharField(max_length=15, choices=FashionType.choices, null=True, blank=True)  # Allow null and blank

    def clean(self):
        """ Ensure fashion_type is only required if sub_category is not 'Dress' """
        if self.sub_category != FashionSubCategory.DRESS and not self.fashion_type:
            raise ValidationError({'fashion_type': 'This field is required.'})

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
    
class product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField
    image = models.ImageField

    def _str_(self):
        return f"{self.name} at {self.price}"
