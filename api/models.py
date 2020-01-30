from django.db import models

# Create your models here.

class Product(models.Model):
    sku = models.CharField(max_length=50)
    quantity = models.IntegerField()
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    cost_price = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    status = models.CharField(max_length=30)
    date = models.DateField()
    partial_total = models.DecimalField(max_digits=19, decimal_places=2)
    discount = models.DecimalField(max_digits=19, decimal_places=2)
    point_sale = models.CharField(max_length=30)
    shipment_value =models.DecimalField(max_digits=19, decimal_places=2)
    total = models.DecimalField(max_digits=19, decimal_places=2)
    modified = models.DateTimeField(auto_now=True)
    ProductsSold = models.ManyToManyField(Product)

    def __str__(self):
        return self.id


