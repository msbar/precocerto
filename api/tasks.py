from __future__ import absolute_import, unicode_literals
import random, requests, time, json
from math import ceil
from django.db import connection
from precocerto.celery import app

@app.task(name='tasks.integraVendas')
def integraVendas(page):
	# prepara a url para acessar o site de vendas e obtém as vendas.
	url_sitevendas = "http://192.168.1.22:8000/sitevendas/orders/?page="+str(page)
	print(url_sitevendas)
	r = requests.get(url_sitevendas)
	if r.status_code != 200:
		print('Url Não Responde')
	else:	
		orders = r.json()
	
		# percorre o resultado e seta as variáveis para atualizar bd
		for i in range(len(orders['results'])):
			order_id = orders['results'][i]['id']
			order_status = orders['results'][i]['status']
			order_date = orders['results'][i]['date']
			order_partial_total = orders['results'][i]['partial_total']
			order_discount = orders['results'][i]['discount']
			order_point_sale = orders['results'][i]['point_sale']
			order_shipment_value = orders['results'][i]['shipment_value']
			order_total = orders['results'][i]['total']
			order_modified = orders['results'][i]['modified']
			order_ProductsSold = orders['results'][i]['ProductsSold']
			
			# Faz a query para o upinsert - se não houver o id insert e se tiver faz o update
			query = ''' INSERT INTO api_order (id,status, date, partial_total, discount, point_sale, shipment_value, total, modified)
				VALUES ({id}, '{status}','{date}',{partial_total},{discount},'{point_sale}',{shipment_value},{total},'{modified}')
				ON CONFLICT (id) DO
				UPDATE SET status = '{status}', date = '{date}', partial_total = {partial_total}, discount = {discount},
				point_sale = '{point_sale}', shipment_value = {shipment_value}, total={total}, modified = '{modified}' 
				RETURNING id '''
			
			with connection.cursor() as cursor:
				cursor.execute(query.format(id=order_id, status=order_status, date=order_date, partial_total=order_partial_total, discount=order_discount, point_sale=order_point_sale, shipment_value=order_shipment_value, total=order_total, modified=order_modified))
				# se houver o last ip houve insert se não houve update
				if cursor.lastrowid:
					api_order_id = cursor.lastrowid
					print("Insert id: %s" % api_order_id)
				else:
					result = cursor.fetchone()
					api_order_id = result[0]
					print("Update id: %s" % api_order_id)

				# Deleta produtos da tabela relacionamentos do referido ID
				query = ''' DELETE FROM "api_order_ProductsSold" WHERE order_id = {order_id}'''
				cursor.execute(query.format(order_id=api_order_id))
				# Percorre produtos e inserta na tabela de relacionamentos para o referido ID
				for l in range(len(order_ProductsSold)):
					api_product_id = order_ProductsSold[l]
					query = ''' INSERT INTO "api_order_ProductsSold" (order_id, product_id) VALUES ({order_id}, {product_id}) '''
					cursor.execute(query.format(order_id=api_order_id, product_id=api_product_id))

	print("Vendas Integradas com sucesso")

# simula aleatóriamente a quantidade
# de vendas entre 100 e 500 e chama a integração
@app.task(name='tasks.getQuantidadeVendas')
def getQuantidadeVendas():
	quantidadeVendas = random.randint(100, 500)
	quantidadeCallApi = ceil(quantidadeVendas/100)
	print(quantidadeVendas)
	print(quantidadeCallApi)
	for i in range(quantidadeCallApi):
		integraVendas.delay(i+1)