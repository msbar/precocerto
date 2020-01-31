from sitevendas.models import Product, Order
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','sku','quantity','name','price','cost_price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','status','date','partial_total','discount','point_sale','shipment_value','total','modified','ProductsSold']
    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)
        representation['modified'] = instance.modified.strftime("%Y-%m-%d %H:%M:%S")
        return representation