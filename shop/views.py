from django.shortcuts import render
from .models import Category, Product, Basket, LineItem
from django.db.models import Q
from django.http import HttpResponseRedirect

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
