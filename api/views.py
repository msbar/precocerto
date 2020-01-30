from django.http import HttpResponse, JsonResponse
import random, requests, time, json
from math import ceil
from django.shortcuts import render
from api.models import Product, Order
from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers import ProductSerializer, OrderSerializer

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

def index(request, format=None):
    url_sitevendas = "http://localhost:8000/sitevendas/orders/?page=2"
    r = requests.get(url_sitevendas)
    vendas = r.json()
    vendas_list = []
    for i in range(len(vendas['results'])):
        vendas_list.append(vendas['results'][i]['ProductsSold'])
    return HttpResponse(vendas_list)