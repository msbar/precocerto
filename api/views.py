from django.shortcuts import render
from api.models import Product, Order
from rest_framework import viewsets
from api.serializers import ProductSerializer, OrderSerializer

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer