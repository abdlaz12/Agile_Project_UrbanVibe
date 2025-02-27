from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Fashion, Beauty, Accessories, ProductImage
from .models import ProductCategory, FashionSubCategory, ColorChoices, Size, BeautyType
# Form untuk Make Up
class MakeUpAdminForm(forms.ModelForm):
    class Meta:
        model = Beauty
        fields = "__all__"

# Form untuk Fashion
class FashionAdminForm(forms.ModelForm):
    class Meta:
        model = Fashion
        fields = "__all__"

# Form untuk Accessories
class AccessoriesAdminForm(forms.ModelForm):
    class Meta:
        model = Accessories
        fields = "__all__"

# Inline untuk menampilkan gambar produk
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Jumlah form kosong yang ditampilkan untuk menambahkan gambar
    readonly_fields = ['thumbnail']

    def thumbnail(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        return "No Image"

    thumbnail.short_description = "Preview"

# Admin untuk Fashion
@admin.register(Fashion)
class FashionAdmin(admin.ModelAdmin):
    form = FashionAdminForm
    list_display = ("name", "sub_category", "color", "size", "fashion_type", "price", "stock", "category")
    list_filter = ("sub_category", "category", "color", "size")
    search_fields = ("name", "description")
    inlines = [ProductImageInline]

    def save_model(self, request, obj, form, change):
        """Pastikan kategori tetap 'Fashion' saat menyimpan"""
        obj.category = ProductCategory.FASHION
        super().save_model(request, obj, form, change)

# Admin untuk Beauty
@admin.register(Beauty)
class BeautyAdmin(admin.ModelAdmin):
    form = MakeUpAdminForm
    list_display = ("name", "makeup_type", "price", "stock", "category")
    list_filter = ("makeup_type", "category")
    search_fields = ("name", "description")
    inlines = [ProductImageInline]

    def save_model(self, request, obj, form, change):
        """Pastikan kategori tetap 'Beauty' saat menyimpan"""
        obj.category = ProductCategory.BEAUTY
        super().save_model(request, obj, form, change)

# Admin untuk Accessories
@admin.register(Accessories)
class AccessoriesAdmin(admin.ModelAdmin):
    form = AccessoriesAdminForm
    list_display = ("name", "price", "stock", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")
    inlines = [ProductImageInline]

    def save_model(self, request, obj, form, change):
        """Pastikan kategori tetap 'Accessories' saat menyimpan"""
        obj.category = ProductCategory.ACCESSORIES
        super().save_model(request, obj, form, change)


from django.contrib import admin
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

