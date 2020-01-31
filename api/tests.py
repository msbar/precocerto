from django.test import  SimpleTestCase
from api.models import Order
from api.tasks import *
import requests, json, time

class TaskTestCase(SimpleTestCase):
    def setUp(self):
        getQuantidadeVendas() #chama a task de integração
        time.sleep(15)

    def test_order_integracao(self):
        #pega registro id 1 do site de vendas
        url_sitevendas = "http://192.168.1.22:8000/sitevendas/orders/1"
        r = requests.get(url_sitevendas)
        sitevendas_order_1 = r.json()

        #pega registro id 1 da api
        url_api = "http://192.168.1.22:8000/api/orders/1"
        r = requests.get(url_sitevendas)
        api_order_1 = r.json()

        # testa se registro da api e do sitevendas são iguais
        self.assertEqual(api_order_1,sitevendas_order_1)
