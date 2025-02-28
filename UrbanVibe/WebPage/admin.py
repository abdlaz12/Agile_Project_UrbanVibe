from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Fashion, Beauty, Accessories, ProductImage
from multiselectfield import MultiSelectField

# Forms for Admin Panel
class FashionAdminForm(forms.ModelForm):
    class Meta:
        model = Fashion
        fields = "__all__"

    class Media:
        js = ('admin/js/fashion_filter.js',)  # Load custom JavaScript

class BeautyAdminForm(forms.ModelForm):
    class Meta:
        model = Beauty
        fields = "__all__"

class AccessoriesAdminForm(forms.ModelForm):
    class Meta:
        model = Accessories
        fields = "__all__"

# Inline Product Image Admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  
    readonly_fields = ['thumbnail']

    def thumbnail(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        return "No Image"

    thumbnail.short_description = "Preview"

# Admin for Fashion
@admin.register(Fashion)
class FashionAdmin(admin.ModelAdmin):
    form = FashionAdminForm
    list_display = ("name", "sub_category", "price", "stock")
    list_filter = ("sub_category",)
    search_fields = ("name", "description")
    inlines = [ProductImageInline]

# Admin for Beauty
@admin.register(Beauty)
class BeautyAdmin(admin.ModelAdmin):
    form = BeautyAdminForm
    list_display = ("name", "makeup_type", "price", "stock")
    list_filter = ("makeup_type",)
    search_fields = ("name", "description")
    inlines = [ProductImageInline]

# Admin for Accessories
@admin.register(Accessories)
class AccessoriesAdmin(admin.ModelAdmin):
    form = AccessoriesAdminForm
    list_display = ("name", "price", "stock")
    search_fields = ("name", "description")
    inlines = [ProductImageInline]

# CustomUser Admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'phone_number', 'address')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'address')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'address', 'password1', 'password2')}
        ),
    )
    filter_horizontal = ()
    list_filter = ()

admin.site.register(CustomUser, CustomUserAdmin)