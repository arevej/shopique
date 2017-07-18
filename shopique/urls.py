"""shopique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from shop import views

import os

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='main'),
    url(r'^basket/$', views.basket, name='basket'),
    url(r'^category/(?P<category_name>[a-zA-Z0-9]+)/$', views.product_list, name='products'),
    url(r'^add_to_basket/(?P<product_id>[0-9]+)/$', views.add_product, name='add_to_basket'),
    url(r'^delete_product/(?P<product_id>[0-9]+)/$', views.delete_product, name='delete_product'),
    url(r'^increment_qty/(?P<product_id>[0-9]+)/$', views.increment_qty, name='increment_qty'),
    url(r'^decrement_qty/(?P<product_id>[0-9]+)/$', views.decrement_qty, name='decrement_qty'),
    url(r'^place_order/$', views.place_order, name='place_order'),
    url(r'^order_confirmation/(?P<order_id>[0-9]+)/$', views.order_confirmation, name='order_confirmation'),
]

urlpatterns += static('/images/', document_root=os.path.join(settings.BASE_DIR, 'images'))
urlpatterns += static('/files/', document_root=os.path.join(settings.BASE_DIR, 'files'))
