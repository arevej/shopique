from django.db import models
import datetime
from django.utils import timezone

class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=10000)
    size = models.FloatField()
    weight = models.FloatField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product_name

class Promo(models.Model):
    promocode = models.CharField(max_length=30)
    discount_percent = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.promocode

    def can_apply(self):
        now = timezone.now()
        if self.start_date == None and self.end_date == None:
            return True
        elif self.start_date == None:
            return now <= self.end_date
        elif self.end_date == None:
            return self.start_date <= now
        else:
            return self.start_date <= now <= self.end_date


class Basket(models.Model):
    promo = models.ForeignKey(Promo, null=True, on_delete=models.PROTECT)
    def subtotal(self):
        total = 0
        for lineitem in self.lineitem_set.all():
            total += lineitem.total()
        return total

    def get_lineitem(self, product):
        for lineitem in self.lineitem_set.all():
            if lineitem.product == product:
                return lineitem

    def add_product(self, product):
        lineitem = self.get_lineitem(product)
        if lineitem:
            is_in_basket = True
            lineitem.qty += 1
            lineitem.save()
        else:
            self.lineitem_set.create(product=product)

    def delete_product(self, product):
        lineitem = self.get_lineitem(product)
        if lineitem:
            lineitem.delete()

    def increment(self, product):
        lineitem = self.get_lineitem(product)
        if lineitem:
            lineitem.qty += 1
            lineitem.save()

    def decrement(self, product):
        lineitem = self.get_lineitem(product)
        if lineitem:
            if lineitem.qty == 1:
                lineitem.delete()
            else:
                lineitem.qty -= 1
                lineitem.save()

    def discount_ammount(self):
        if self.promo:
            return self.subtotal() * self.promo.discount_percent
        else:
            return 0

    def total(self):
        return self.subtotal()-self.discount_ammount()

class LineItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def total(self):
        return self.product.price * self.qty


class Order(models.Model):
    buyer_name = models.CharField(max_length=30)
    buyer_number = models.CharField(max_length=15)
    buyer_email = models.EmailField(max_length=30)
    delivery_country = models.CharField(max_length=100)
    delivery_city = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    promo = models.ForeignKey(Promo, null=True, on_delete=models.PROTECT)
    discount_ammount = models.DecimalField(max_digits=6, decimal_places=2)
    payment = models.BooleanField(default=False)

    def subtotal(self):
        total = 0
        for lineitem in self.lineitemorder_set.all():
            total += lineitem.total()
        return total

    def total(self):
        if self.promo:
            return self.subtotal() - self.discount_ammount
        else:
            return self.subtotal()


class LineItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    product_qty = models.IntegerField(default=1)

    def total (self):
        return self.product_price * self.product_qty
