from flask import Flask, render_template_string, Response
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def index():
    # Conectando ao banco de dados SQLite
    conn = sqlite3.connect('data.db')
    
    # Lendo os dados da tabela 'api_data' para um DataFrame
    df = pd.read_sql_query("SELECT api_data.*, api_devices.name as nome_device FROM api_data INNER JOIN api_devices ON api_data.device = api_devices.id ORDER BY api_data.id DESC LIMIT 10000", conn)
    
    # Fechando a conexão
    conn.close()

    # Criando uma lista para armazenar os dados processados
    processed_data = []

    # Agrupando os dados pelo campo 'group'
    grouped = df.groupby('group')

    for group_name, group_data in grouped:
        row = {}
        
        row['Dispositivo'] = group_data['nome_device'].values[0] if not group_data['nome_device'].empty else None
        # Pegando o primeiro horário do grupo e convertendo para GMT-3
        first_time = group_data['time'].min().replace('Z', '')
        gmt_time = datetime.fromisoformat(first_time)
        local_time = gmt_time - timedelta(hours=3)  # Ajuste manual para GMT-3
        row['Horário'] = local_time.strftime('%Y-%m-%d %H:%M:%S')
        # if 'timestamp' in group_data['variable'].values:
        #     timestamp_value = int(group_data[group_data['variable'] == 'timestamp']['value'].values[0])
        #     row['Timestamp GMT-3'] = datetime.fromtimestamp(timestamp_value, tz=pytz.UTC).astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
        # else:
        #     row['Timestamp GMT-3'] = None
            
        # Extraindo as variáveis específicas
        row['Contador'] = group_data[group_data['variable'] == 'fcnt']['value'].values[0] if not group_data[group_data['variable'] == 'fcnt'].empty else None
        row['Temperatura'] = group_data[group_data['variable'] == 'temperature']['value'].values[0] if not group_data[group_data['variable'] == 'temperature'].empty else None
        row['Umidade'] = group_data[group_data['variable'] == 'humidity']['value'].values[0] if not group_data[group_data['variable'] == 'humidity'].empty else None
        row['Pressão Atmosférica'] = group_data[group_data['variable'] == 'airpressure']['value'].values[0] if not group_data[group_data['variable'] == 'airpressure'].empty else None
        row['Ruído'] = group_data[group_data['variable'] == 'noise']['value'].values[0] if not group_data[group_data['variable'] == 'noise'].empty else None
        row['Luminosidade'] = group_data[group_data['variable'] == 'luminosity']['value'].values[0] if not group_data[group_data['variable'] == 'luminosity'].empty else None
        row['etvoc'] = group_data[group_data['variable'] == 'etvoc']['value'].values[0] if not group_data[group_data['variable'] == 'etvoc'].empty else None
        row['eco2'] = group_data[group_data['variable'] == 'eco2']['value'].values[0] if not group_data[group_data['variable'] == 'eco2'].empty else None
        row['Latitude'] = group_data[group_data['variable'] == 'latitude']['value'].values[0] if not group_data[group_data['variable'] == 'latitude'].empty else None
        row['Longitude'] = group_data[group_data['variable'] == 'longitude']['value'].values[0] if not group_data[group_data['variable'] == 'longitude'].empty else None
        row['Bateria'] = group_data[group_data['variable'] == 'batterylevel']['value'].values[0] if not group_data[group_data['variable'] == 'batterylevel'].empty else None
        row['RSSI'] = group_data[group_data['variable'] == 'rssi']['value'].values[0] if not group_data[group_data['variable'] == 'rssi'].empty else None
        row['SNR'] = group_data[group_data['variable'] == 'snr']['value'].values[0] if not group_data[group_data['variable'] == 'snr'].empty else None
        row['SF'] = group_data[group_data['variable'] == 'lora_spreading_factor']['value'].values[0] if not group_data[group_data['variable'] == 'lora_spreading_factor'].empty else None
        row['Frequencia'] = group_data[group_data['variable'] == 'frequency']['value'].values[0] if not group_data[group_data['variable'] == 'frequency'].empty else None
        row['GW'] = group_data[group_data['variable'] == 'gateway_eui']['value'].values[0] if not group_data[group_data['variable'] == 'gateway_eui'].empty else None

        # Adicionando a linha à lista
        processed_data.append(row)

    # Convertendo a lista de dicionários para um DataFrame
    processed_data_df = pd.DataFrame(processed_data)

    # Gerando a tabela HTML
    html_table = processed_data_df.to_html(classes='data', header="true", index=False)

    # Gerando os gráficos
    #img_files = generate_plots()

    # HTML básico com placeholders para a tabela e os gráficos
    html_template = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Dados Lora</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <style>
              body {
                font-size: 0.75rem; /* Tamanho de fonte menor */
                 margin: 0; /* Remove a margem padrão */
                padding: 0; /* Remove o padding padrão */
              }
              table.data {
                width: 100%;
                margin: 2px 0;
                border-collapse: collapse;
                font-size: 0.75rem; /* Tamanho de fonte menor */
              }
              table.data th, table.data td {
                border: 1px solid #ddd;
                padding: 4px; /* Espaçamento menor */
              }
              table.data th {
                padding-top: 8px; /* Espaçamento menor */
                padding-bottom: 8px; /* Espaçamento menor */
                text-align: left;
                background-color: #f2f2f2;
              }
              .chart-container {
                text-align: center;
                margin: 20px 0;
              }
              .container {
                padding-left: 0 !important; /* Remove padding à esquerda da tabela */
                padding-right: 0 !important; /* Remove padding à direita da tabela */
              }
              h1, h2 {
                font-size: 1.5rem; /* Tamanho de fonte menor para os títulos */
              }
      </style>  
      </head>
      <body>
        
          <h1>Dados Lora</h1>
          {{ table|safe }}
                  
      </body>
    </html>
    '''

    # Renderizando a página HTML com a tabela e os gráficos
    #return render_template_string(html_template, table=html_table, imgs=range(1, len(img_files)+1))
    return render_template_string(html_template, table=html_table)

if __name__ == '__main__':
    app.run(debug=True)
