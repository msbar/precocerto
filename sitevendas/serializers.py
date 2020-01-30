from sitevendas.models import Product, Order
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['sku','quantity','name','price','cost_price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status','date','partial_total','discount','point_sale','shipment_value','total','modified','ProductsSold']
