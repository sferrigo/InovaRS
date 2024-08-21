import requests
import pandas as pd
import sqlite3
import json

# URLs e cabeçalhos de autorização
urls = [
    # 'https://api.tago.io/device/637f518abe07280011be786d/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Senzemo Caxias
    # 'https://api.tago.io/device/663d0d67337e5f0009098a42/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Senzemo Mayron
    # 'https://api.tago.io/device/663d0b4e1b7f7100097d4e71/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Senzemo São Chico
    # 'https://api.tago.io/device/663d0b166669a5000916775e/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Senzemo Bento
    # 'https://api.tago.io/device/663d0af56669a50009167382/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z' #Senzemo Flores
    # 'https://api.tago.io/device/66a13be0629b410009b5e54a/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Senzemo Gramado
    # 'https://api.tago.io/device/667c8488908fae0009601a51/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Senzemo Canela
    # 'https://api.tago.io/device/660e80d1594ba7001039aec8/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Escola São Chico 21
    # 'https://api.tago.io/device/660e8190e9191e0010e6d692/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Biblioteca São Chico 20
    # 'https://api.tago.io/device/660e8151e4076300090b5881/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Seplan São Chico 16
    # 'https://api.tago.io/device/66a29cd0ac7e460009eee891/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Prefeitura Gramado 22
    # 'https://api.tago.io/device/660e7f8a044d5e0009825997/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Gramado Escola 09
    # 'https://api.tago.io/device/660e81d2de4c2a001010dab9/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Gramado Cãmara 13
    # 'https://api.tago.io/device/660e7f54e4076300090b2b1c/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Flores Vindima 19
    # 'https://api.tago.io/device/660e7fcc34e4f30010867839/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Flores UBS Centro 23
    # 'https://api.tago.io/device/660e84131d22140011ef9080/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Flores Escola 10
    # 'https://api.tago.io/device/663d145a867da80009091cd6/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Caxias UBS São José 05
    # 'https://api.tago.io/device/663d13a638ca2f0008c9e6b1/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Caxias Praça DAnte 06
    # 'https://api.tago.io/device/663d141d142d0d0009f5d365/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Caxias Mato Sartori 11
    # 'https://api.tago.io/device/661edf4f3384bc00108bbce9/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Canela Prefeitura 17
    # 'https://api.tago.io/device/661edf2b961a4c0010fc4de2/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Canela Distrito Industrial 14
    # 'https://api.tago.io/device/660e7e9c6305d2000991f87f/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Canela CIT 12
    # 'https://api.tago.io/device/660e8221de4c2a001010e25d/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Bento UPA ZS 08
    # 'https://api.tago.io/device/6627f2d430f98d0009c1a00f/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z', #Bento Igreja São Bento 18
    # 'https://api.tago.io/device/6627efb880e9c600102609fb/data?qty=100000&end_date=2024-07-29T23%3A59%3A59.999Z' #Bento Igreja Cristo Rei 15
    #Retorna devices
    'https://api.tago.io/device?amount=25&fields[0]=id&fields[1]=name'
]
headers = [
    #Senzemo
    #{'Authorization': '688c5334-306d-4b8d-8170-fd3ce1503541'},
    #Senzemo Gramado/Canela
    #{'Authorization': 'e3281fd8-4a76-4fe4-93d3-399928d33584'},
    {'Authorization': 'b3c885e3-6f7d-4168-a495-65445d921dcb'}
]

header = {'Authorization': 'e3281fd8-4a76-4fe4-93d3-399928d33584'}

# Conectando ao banco de dados SQLite (ou criando um novo banco de dados)
conn = sqlite3.connect('data.db')

# Loop através das URLs e cabeçalhos
#for url, header in zip(urls, headers):
for url in urls:
    # Fazendo a requisição
    response = requests.get(url, headers=header)
    data = response.json()

    # Verificando se a requisição foi bem-sucedida
    if data['status']:
        result = data['result']

        # Convertendo tipos complexos para JSON
        for item in result:
            for key, value in item.items():
                if isinstance(value, (dict, list)):
                    item[key] = json.dumps(value)

        # Criando o DataFrame
        df = pd.DataFrame(result)

        # Armazenando os dados no banco de dados
        df.to_sql('api_data', conn, if_exists='append', index=False)

        # Confirmando a inserção dos dados
        print(f"Dados armazenados no banco de dados SQLite 'data.db' na tabela 'api_data' para URL: {url}")

    else:
        print(f"Erro ao obter os dados da API para URL: {url}")

# Fechando a conexão
conn.close()
