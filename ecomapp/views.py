from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from ecomapp.models import Category, Product, Cart, CartItem
from decimal import Decimal


def cart_creation(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except (ObjectDoesNotExist, KeyError):
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart


def base_view(request):
    cart = cart_creation(request)
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
    }

    return render(request, 'base.html', context)


def product_view(request, product_slug):
    cart = cart_creation(request)
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'product.html', context)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    products_of_category = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'categories': categories,
    }
    return render(request, 'category.html', context)


def cart_view(request):
    cart = cart_creation(request)
    context = {
                'cart': cart
              }
    return render(request, 'cart.html', context)


def add_to_cart_view(request):
    cart = cart_creation(request)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
    cart = cart_creation(request)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def change_item_qty(request):
    cart = cart_creation(request)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse({'cart_total': cart.items.count(), 'item_total': cart_item.item_total,
                        'cart_total_price': cart.cart_total})
