from api.models import Product, Order
from rest_framework import serializers

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id','sku','quantity','name','price','cost_price']

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id','status','date','partial_total','discount','point_sale','shipment_value','total','modified','ProductsSold']