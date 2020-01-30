from __future__ import absolute_import, unicode_literals
from precocerto.celery import app
import random, requests, time
from math import ceil


@app.task(name='tasks.integraVendas')
def integraVendas(request):
    url_sitevendas = "http://192.168.1.22:8000/api/orders/"
    response = requests.get(url_sitevendas)
    if response.status_code == 200:

        print(response.content)

#simula aleatóriamente a quantidade 
# de vendas entre 100 e 500 e chama a integração
@app.task(name='tasks.getQuantidadeVendas')
def getQuantidadeVendas():
    quantidadeVendas = random.randint(100,500)
    quantidadeCallApi = ceil(quantidadeVendas/100)
    print(quantidadeVendas)
    print(quantidadeCallApi)
    for i in range(quantidadeCallApi):
        integraVendas.delay(i+1)