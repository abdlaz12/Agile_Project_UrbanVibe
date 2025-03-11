import json
import datetime
import uuid
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import *


def index(request):
    return render(request, 'WebPage/index.html')

def about_us(request):
    return render(request, 'WebPage/about_us.html')

def sign_up(request):
    return render(request, 'WebPage/sign_up.html')

def favorites(request):
    # Fetch 4 latest fashion products
    fashion_products = Fashion.objects.order_by('-product_id')[:8]

    # Fetch 4 latest beauty products
    beauty_products = Beauty.objects.order_by('-product_id')[:8]

    # Fetch trending products (modify logic as needed)
    trending_fashion = Fashion.objects.order_by('-product_id')[:5]
    trending_beauty = Beauty.objects.order_by('-product_id')[:3]

    # Manually combine products into a list
    trending_products = list(trending_fashion) + list(trending_beauty)

    # Make sure all products have at least one image
    # This is a safety check for demonstration purposes
    for product in fashion_products:
        if not product.images.exists():
            # Create a placeholder image if needed for testing
            ProductImage.objects.create(
                fashion=product, 
                image='product_images/placeholder.jpg'
            )
    
    for product in beauty_products:
        if not product.images.exists():
            # Create a placeholder image if needed for testing
            ProductImage.objects.create(
                beauty=product, 
                image='product_images/placeholder.jpg'
            )

    context = {
        'fashion_products': fashion_products,
        'beauty_products': beauty_products,
        'trending_products': trending_products,
    }
    return render(request, 'WebPage/favorites.html', context)

def catalogue(request):
    category = request.GET.get('category', None)  # Get category from URL query
    subcategory = request.GET.get('subcategory', None)  # Get subcategory from URL query

    # Fetch products based on filters
    if category == "fashion":
        if subcategory:
            fashion_products = Fashion.objects.filter(sub_category=subcategory)
        else:
            fashion_products = Fashion.objects.all()
        beauty_products = []
        accessories_products = []
    elif category == "beauty":
        fashion_products = []
        beauty_products = Beauty.objects.all()
        accessories_products = []
    elif category == "accessories":
        fashion_products = []
        beauty_products = []
        accessories_products = Accessories.objects.all()
    else:
        # Show all products if no category is selected
        fashion_products = Fashion.objects.all()
        beauty_products = Beauty.objects.all()
        accessories_products = Accessories.objects.all()

    return render(request, "WebPage/catalogue.html", {
        "fashion_products": fashion_products,
        "beauty_products": beauty_products,
        "accessories_products": accessories_products,
    })

def fashion_detail(request, pk):
    fashion = get_object_or_404(Fashion, pk=pk)
    return render(request, 'WebPage/fashion_detail.html', {'fashion': fashion})

def beauty_detail(request, pk):
    beauty = get_object_or_404(Beauty, pk=pk)
    return render(request, 'WebPage/beauty_detail.html', {'beauty': beauty})

def accessories_detail(request, pk):
    accessories = get_object_or_404(Accessories, pk=pk)
    return render(request, 'WebPage/accessories_detail.html', {'accessories': accessories})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Pastikan untuk menyebutkan backend yang digunakan
            login(request, user, backend='WebPage.backends.EmailBackend')

            messages.success(request, 'Registration successful!')
            return redirect('index')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'WebPage/register.html', {'form': form})

def login_customer(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user, backend='WebPage.backends.EmailBackend')
                messages.success(request, 'Login successful!')
                
                # Redirect to checkout if that's where they were heading
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Form validation failed. Please check your entries.')
    else:
        form = CustomerLoginForm()
    
    return render(request, 'WebPage/login.html', {'form': form})

def logout_customer(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required
def profile_view(request):
    # Get user's orders
    orders = Order.objects.filter(user=request.user, complete=True).order_by('-date_ordered')
    
    return render(request, 'WebPage/userprofile.html', {
        'user': request.user,
        'orders': orders
    })

# Shopping Cart Views
def shoppingcart(request):
    """View for displaying the shopping cart with all items and summary."""
    if request.user.is_authenticated:
        # Get or create an incomplete order for the user
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
        
        try:
            # Try to calculate cart totals with the property
            subtotal = sum([item.get_total for item in items])
        except AttributeError:
            # If get_total is not available, calculate directly
            subtotal = 0
            for item in items:
                product = None
                try:
                    if item.product_type == 'fashion':
                        product = Fashion.objects.get(product_id=item.product_id)
                    elif item.product_type == 'beauty':
                        product = Beauty.objects.get(product_id=item.product_id)
                    elif item.product_type == 'accessories':
                        product = Accessories.objects.get(product_id=item.product_id)
                    
                    if product:
                        subtotal += product.price * item.quantity
                except (Fashion.DoesNotExist, Beauty.DoesNotExist, Accessories.DoesNotExist):
                    pass
        
        tax = int(subtotal * 0.10)  # 10% tax
        final_total = subtotal + tax - order.discount_amount
        
        context = {
            'items': items,
            'order': order,
            'subtotal': subtotal,
            'tax': tax,
            'final_total': final_total
        }
    else:
        # For anonymous users, we'll rely on the client-side cart in localStorage
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, 'discount_amount': 0}
        context = {
            'items': items,
            'order': order,
        }
    return render(request, 'WebPage/shoppingcart.html', context)
@require_POST
def add_to_cart(request):
    """API endpoint to add items to cart."""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product_type = data.get('product_type')
        quantity = int(data.get('quantity', 1))
        color = data.get('color')
        size = data.get('size')
        
        # Get the appropriate product model
        product = None
        if product_type == 'fashion':
            product = get_object_or_404(Fashion, product_id=product_id)
        elif product_type == 'beauty':
            product = get_object_or_404(Beauty, product_id=product_id)
        elif product_type == 'accessories':
            product = get_object_or_404(Accessories, product_id=product_id)
        
        if not product:
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        if request.user.is_authenticated:
            # Get or create user's cart
            order, created = Order.objects.get_or_create(user=request.user, complete=False)
            
            # Check if item already exists in cart
            orderitem, created = OrderItem.objects.get_or_create(
                order=order,
                product_type=product_type,
                product_id=product_id,
                color=color,
                size=size,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # If item already exists, update quantity
                orderitem.quantity += quantity
                orderitem.save()
            
            return JsonResponse({
                'success': True,
                'cart_total': order.get_cart_items,
                'message': f'Added {product.name} to cart'
            })
        else:
            # For anonymous users, response for client-side cart handling
            return JsonResponse({
                'success': True,
                'product': {
                    'id': product.product_id,
                    'name': product.name,
                    'price': product.price,
                    'type': product_type,
                    'color': color,
                    'size': size,
                },
                'message': f'Added {product.name} to cart'
            })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def update_cart_item(request):
    """API endpoint to update cart item quantity."""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')
        
        if request.user.is_authenticated:
            orderitem = get_object_or_404(OrderItem, id=item_id)
            
            if action == 'increase':
                orderitem.quantity += 1
            elif action == 'decrease':
                if orderitem.quantity > 1:
                    orderitem.quantity -= 1
                else:
                    orderitem.delete()
                    return JsonResponse({'removed': True})
            elif action == 'remove':
                orderitem.delete()
                return JsonResponse({'removed': True})
                
            orderitem.save()
            
            order = orderitem.order
            final_total, tax = order.get_final_total
            
            return JsonResponse({
                'quantity': orderitem.quantity,
                'item_total': orderitem.get_total,
                'cart_total': order.get_cart_total,
                'cart_items': order.get_cart_items,
                'tax': tax,
                'final_total': final_total
            })
        else:
            # For client-side cart handling
            return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def apply_voucher(request):
    """API endpoint to apply a voucher code to the cart."""
    try:
        data = json.loads(request.body)
        voucher_code = data.get('voucher_code')
        
        # Simple voucher logic (can be expanded with a Voucher model)
        discount_amount = 0
        valid = False
        message = "Invalid voucher code"
        
        if voucher_code == "ibusesar":
            discount_amount = 50000
            valid = True
            message = "Voucher applied successfully! Discount: Rp. 50.000"
        elif voucher_code == "URBAN25":
            # For percentage discounts, we need the cart total
            if request.user.is_authenticated:
                order = Order.objects.get(user=request.user, complete=False)
                discount_amount = int(order.get_cart_total * 0.25)
            else:
                # For client-side cart, use the subtotal from request
                subtotal = data.get('subtotal', 0)
                discount_amount = int(subtotal * 0.25)
            
            valid = True
            message = f"Voucher applied successfully! Discount: Rp. {discount_amount:,}"
        
        if valid and request.user.is_authenticated:
            order = Order.objects.get(user=request.user, complete=False)
            order.voucher_code = voucher_code
            order.discount_amount = discount_amount
            order.save()
            
            # Return updated totals
            final_total, tax = order.get_final_total
            return JsonResponse({
                'valid': valid,
                'message': message,
                'discount_amount': discount_amount,
                'final_total': final_total,
                'tax': tax
            })
        
        return JsonResponse({
            'valid': valid,
            'message': message,
            'discount_amount': discount_amount
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def checkout(request):
    """View for the checkout process."""
    # Get the current incomplete order
    order = Order.objects.filter(user=request.user, complete=False).first()
    
    if not order or order.get_cart_items == 0:
        messages.warning(request, "Your cart is empty")
        return redirect('shoppingcart')
    
    if request.method == 'POST':
        # Process the checkout form
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        
        # Create shipping address
        shipping = ShippingAddress.objects.create(
            user=request.user,
            order=order,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode
        )
        
        # Complete the order
        order.complete = True
        order.status = 'processing'
        order.transaction_id = str(uuid.uuid4())
        order.date_ordered = datetime.datetime.now()
        order.save()
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect('invoice')
    
    context = {
        'order': order,
        'items': order.orderitem_set.all()
    }
    return render(request, 'WebPage/checkout.html', context)

def invoice(request):
    """View for displaying the invoice after checkout."""
    if request.user.is_authenticated:
        # Get the most recent completed order
        order = Order.objects.filter(
            user=request.user, 
            complete=True
        ).order_by('-date_ordered').first()
        
        if order:
            items = order.orderitem_set.all()
            final_total, tax = order.get_final_total
            
            context = {
                'order': order,
                'items': items,
                'tax': tax,
                'total': final_total
            }
            return render(request, 'WebPage/invoice.html', context)
    
    # If no order or user not authenticated, fallback to client-side cart
    return render(request, 'WebPage/invoice.html')

@login_required
@require_POST
def process_payment(request):
    """API endpoint to process payment and complete order."""
    try:
        # Here you would integrate with a payment gateway
        # For now, we'll just mark the order as complete
        
        order = Order.objects.filter(user=request.user, complete=False).first()
        
        if not order:
            return JsonResponse({'error': 'No active order found'}, status=400)
        
        # Complete the order
        order.complete = True
        order.status = 'processing'
        order.transaction_id = str(uuid.uuid4())
        order.date_ordered = datetime.datetime.now()
        order.save()
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'redirect': '/invoice/'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Add wishlists functionality (optional)
@login_required
def add_to_wishlist(request):
    """API endpoint to add an item to the user's wishlist."""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product_type = data.get('product_type')
        
        # Get or create the user's wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        # Check if the item is already in the wishlist
        existing_item = WishlistItem.objects.filter(
            wishlist=wishlist,
            product_type=product_type,
            product_id=product_id
        ).exists()
        
        if existing_item:
            return JsonResponse({
                'success': False,
                'message': 'Item already in wishlist'
            })
        
        # Add the item to the wishlist
        wishlist_item = WishlistItem.objects.create(
            wishlist=wishlist,
            product_type=product_type,
            product_id=product_id
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Item added to wishlist'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def remove_from_wishlist(request, item_id):
    """Remove an item from the user's wishlist."""
    try:
        wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
        wishlist_item.delete()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        messages.success(request, 'Item removed from wishlist')
        return redirect('wishlist')
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=400)
        
        messages.error(request, f'Error removing item: {str(e)}')
        return redirect('wishlist')

@login_required
def wishlist(request):
    """View the user's wishlist."""
    try:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = wishlist.items.all().order_by('-date_added')
        
        context = {
            'wishlist_items': wishlist_items
        }
        return render(request, 'WebPage/wishlist.html', context)
    except Exception as e:
        messages.error(request, f'Error retrieving wishlist: {str(e)}')
        return redirect('index')