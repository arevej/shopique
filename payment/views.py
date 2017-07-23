from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
from shop.models import Order
from django.views.decorators.csrf import csrf_exempt
import requests
from decimal import Decimal

def to_url(dct):
    if settings.PAYPAL_REAL:
        prefix = 'https://ipnpb.paypal.com/cgi-bin/webscr?cmd=_notify-validate&'
    else:
        prefix = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr?cmd=_notify-validate&'
    return prefix + '&'.join([k + '=' + str(dct[k]) for k in dct])

def make_request(url):
    return requests.get(url).content

@csrf_exempt
def payment_done(request):
    paypal_data = request.POST
    url = to_url(paypal_data)
    status = make_request(url)
    order_id = int(paypal_data['invoice'])
    order = Order.objects.get(pk=order_id)
    if status == b"VERIFIED" and order.total() == Decimal(paypal_data['mc_gross']) and paypal_data['mc_currency'] == 'USD':
        order.payment = True
        order.save()
        return redirect(reverse('order_confirmation', args=(order.id,)))
    else:
        return redirect(reverse('payment:process', args=(order.id,)))

@csrf_exempt
def payment_canceled(request):
    order = Order.objects.get(pk=order_id)
    return redirect(reverse('payment:process', args=(order.id,)))

def payment_process(request, order_id):
    order = Order.objects.get(pk=order_id)
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": order.total(),
        "item_name": "Order " + str(order.id),
        "currency_code": "USD",
        "invoice": str(order.id),
        "rm": "2",
        "notify_url": "https://" + settings.APP_DOMAIN + reverse('paypal-ipn'),
        "return_url": "https://" + settings.APP_DOMAIN + reverse('payment:done'),
        "cancel_return": "https://" + settings.APP_DOMAIN + reverse('payment:canceled'),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment/process.html", {'order': order, 'form':form})
