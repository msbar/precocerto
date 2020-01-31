# Desafio Preço Certo

Este código resolve o desafio do link abaixo:
https://bitbucket.org/precocertoco/precocerto_challenges/src/master/3/

## Requisitos para a instalação:
- Toda a aplicação está dockerizada, sendo necessário possuir o Docker.

## Principais Tecnologias Utilizadas:
- Docker - Software Contêiner.
- Python 3 - Linguagem de Programação
- Django 3.0.2 - Framework python para web
- Django rest_Framework 3.11.0 - Framework para construção de API rest.
- Postgres - Banco de Dados
- Celery - Task Queue
- Celery Beat - Agendamento de Tarefas Periódicas
- Redis - Worker

## Resumo do Sistema:
- A partir de um projeto Django foi criado 2 Apps: sitevendas e api

- O App sitevendas contém uma base de dados com 5 produtos e cerca de 1280 ordens de vendas disponibilizada por api rest_Framework nas urls: local: localhost: http://localhost:8000/sitevendas/ e no Docker http://192.168.1.22:8000/sitevendas/ para requisições internas entre o celery e o web server.

- O App api é aplicação que vai consumir os dados do App sitevendas e registrar no Banco de Dados. Suas urls são: localhost: http://localhost:8000/api/ e no Docker http://192.168.1.22:8000/api/ para requisições internas entre o celery e o web server.

-  Arquivo /precocerto/api/tasks.py é onde está as funções que são chamadas de forma automática e realizam a integração de forma assíncrona e com querys otimizadas.

- No arquivo /precocerto/precocerto/setting.py está a Chamamada para o Tasks.py e o disparo para executar a função tasks.getQuantidadeVendas a cada minuto 
- Para Chamar a cada 30 minutos alterar crontab(minute='*/30')

                CELERY_BEAT_SCHEDULE = {
                    'getQuantidadeVendas': {
                    'task': 'tasks.getQuantidadeVendas',
                        'schedule': crontab()  # executa a cada minuto
                    }
                }
## Explicando a Task /precocerto/api/tasks.py:
### getQuantidadeVendas():
- a função getQuantidadeVendas(): busca no sitevendas a quantidade de vendas através da url: http://192.168.1.22:8000/sitevendas/orders/.

- Calcula quantas páginas serão necessárias para se obter todas as vendas. Cada página contém 100 registros.

- Dispara a task integraVendas.delay(i+1) de forma assíncrona na quantidade de páginas necessárias passando o número da page a ser acessada na url, ou seja, se houver 500 registro serão disparados 5 tasks assíncroa uma para acessar cada página.

### integraVendas(page):

- A funcão recebe o número da página e faz o acesso a url http://192.168.1.22:8000/sitevendas/orders/?page=page e captura as vendas da contindas na página.

- Ao percorrer cada venda faz o up insert otimizado com SQL RAW no BD, ou seja em uma query faz o insert do registro quando não o tem e quando já tem o id faz o update sempre retornando o id.

- Com o id do último upinsert são deletados os registros anteriores da tabela de relacionamento order_ProductSold da referida venda e insertados produtos baseado no objeto atualizado.

## Instalação:
- Faça o clone do projeto no endereço: https://github.com/msbar/precocerto.git na pasta local que escolher.

- Com o Docker instalado realizar o seguinte comando no terminal na pasta do projeto:
                
        $ docker-compose up --build

- Se Prefirir pode fazer o buil diretamente do guithub:
                
        $ docker build https://github.com/msbar/precocerto
        $ docker compose up

## Tests
- Você pode acompanhar as tasks pelo terminal.

- Você pode fazer alterações nos registros através do browser nos endereços de url http://localhost:8000/sitevendas/order e acompanar integração no endereço http://localhost:8000/api/order

## O aquivo /precocerto/api/tests.py:
- O test consiste em rodar a integração e comparar o registro de id 1 no bd local com o site vendas. 
- O teste passa se os registro forem iguais.
- Para rodar os testes execute os comandos no terminal:

        $ docker exec -it web bash
        $ python manage.py test 

## Contato e Dúvidas:
- Marciel da Silva Barcellos
- Tel e WhatsApp = +55 33 988313983
- Email: msbar2@gmail.com


