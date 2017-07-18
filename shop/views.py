from django.shortcuts import render
from .models import Category, Product, Basket, LineItem, Order, LineItemOrder
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    if 'query' in request.GET:
        q = request.GET['query']
        all_products = Product.objects.filter(
            Q(product_name__contains=q)
        ).distinct()
    else:
        recommended_products = Product.objects.all()[:3]
        return render (request, 'index.html', {'recommended_products': recommended_products})

def product_list(request, category_name):
    category = Category.objects.get(category_name=category_name)
    products = category.product_set.all()
    return render (request, 'category.html', {'products': products, 'category': category})

def add_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    basket = get_basket(request)
    basket.add_product(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def basket(request):
    basket = get_basket(request)
    return render(request, 'basket.html', {'basket': basket})

def get_basket(request):
    if 'basket_id' in request.session:
        basket = Basket.objects.get(pk=request.session['basket_id'])
    else:
        basket = Basket.objects.create()
        request.session['basket_id'] = basket.id
    return basket

def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    basket = get_basket(request)
    basket.delete_product(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def increment_qty(request, product_id):
    product = Product.objects.get(pk=product_id)
    basket = get_basket(request)
    basket.increment(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def decrement_qty(request, product_id):
    product = Product.objects.get(pk=product_id)
    basket = get_basket(request)
    basket.decrement(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def place_order(request):
    if request.method == "GET":
        return render(request, 'place_order.html', {})
    else:
         buyer_name = request.POST['buyer_name']
         buyer_number = request.POST['buyer_number']
         delivery_country = request.POST['delivery_country']
         delivery_city = request.POST['delivery_city']
         delivery_address = request.POST['delivery_address']
         order = Order.objects.create(buyer_name=buyer_name, buyer_number=buyer_number, delivery_country=delivery_country, delivery_city=delivery_city, delivery_address=delivery_address)
         basket = get_basket(request)
         for lineitem in basket.lineitem_set.all():
             order.lineitemorder_set.create(product=lineitem.product, product_price=lineitem.product.price, product_qty=lineitem.qty)
         return HttpResponseRedirect(reverse('order_confirmation', args=(order.id,)))

def order_confirmation(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'order_confirmation.html', {'order':order})
