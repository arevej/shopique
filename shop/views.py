from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Category, Product, Promo, Basket, LineItem, Order, LineItemOrder
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import BuyerInfo

def index(request):
    if 'query' in request.GET:
        q = request.GET['query']
        all_products = Product.objects.filter(
            Q(product_name__contains=q)
        ).distinct()
    else:
        recommended_products = Product.objects.all()[:3]
        return render(request, 'index.html', {'recommended_products': recommended_products})

def product_list(request, category_name):
    category = Category.objects.get(category_name=category_name)
    products = category.product_set.all()
    return render(request, 'category.html', {'products': products, 'category': category})

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
    basket = get_basket(request)
    if not basket.lineitem_set.all():
        return redirect(reverse('main'))
    elif request.method == "GET":
        form = BuyerInfo()
        return render(request, 'place_order.html', {'form': form })
    else:
         form = BuyerInfo(request.POST)
         if form.is_valid():
             order = Order.objects.create(
                buyer_name=form.cleaned_data['buyer_name'],
                buyer_number=form.cleaned_data['buyer_number'],
                delivery_country=form.cleaned_data['delivery_country'],
                delivery_city=form.cleaned_data['delivery_city'],
                delivery_address=form.cleaned_data['delivery_address'],
                promo=basket.promo,
                discount_ammount=basket.discount_ammount(),
                order_date=datetime.datetime.today()
             )
             for lineitem in basket.lineitem_set.all():
                 order.lineitemorder_set.create(product=lineitem.product, product_price=lineitem.product.price, product_qty=lineitem.qty)
             del request.session['basket_id']
             return redirect(reverse('payment:process', args=(order.id,)))
         else:
             return render(request, 'place_order.html', {'form': form})


def order_confirmation(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'order_confirmation.html', {'order':order})

def add_promo(request):
    basket = get_basket(request)
    if request.POST['promo'] != '':
        try:
            promo = Promo.objects.get(promocode=request.POST['promo'])
            if promo.can_apply():
                basket.promo = promo
                basket.save()
            else:
                return render(request, 'basket.html', {'basket': basket, 'error': "can't be applied" })
        except:
            pass
    return HttpResponseRedirect(reverse('basket'))
