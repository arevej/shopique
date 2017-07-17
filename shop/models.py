from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.CharField(max_length=10000)
    size = models.FloatField()
    weight = models.FloatField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product_name

class Basket(models.Model):
    def total(self):
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

class LineItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def total(self):
        return self.product.price * self.qty
