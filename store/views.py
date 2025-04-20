from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Order, Category
from store.models import OrderItem
from .models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test



def is_admin(user):
    return user.is_superuser



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category_products.html', {
        'category': category,
        'products': products
    })
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'store/my_orders.html', {'orders': orders})


@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if request.method == "POST":
        if not cart:
            messages.warning(request, "Your cart is empty.")
            return redirect('cart')

        order = Order.objects.create(user=request.user)

        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = item.get('quantity', 1)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")
        return redirect('my_orders')

    # Show the checkout page if GET
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image': item['image'],
            'subtotal': subtotal
        })

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total': total})

def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else '',
        }

    request.session['cart'] = cart
    return redirect('product_list')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image': item['image'],
            'subtotal': subtotal
        })

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session['cart'] = cart
    return redirect('cart')

def update_cart(request):
    if request.method == 'POST':
        product_id = str(request.POST.get('product_id'))
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if product_id in cart:
            if action == 'increase':
                cart[product_id]['quantity'] += 1
            elif action == 'decrease':
                if cart[product_id]['quantity'] > 1:
                    cart[product_id]['quantity'] -= 1
                else:
                    del cart[product_id]  # Optionnel : supprimer si 0

        request.session['cart'] = cart
    return redirect('cart')
