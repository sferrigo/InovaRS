import pandas as pd
import matplotlib.pyplot as plt

# Leitura do arquivo CSV
df = pd.read_csv('tabela2.csv', sep=';')

# Convertendo a coluna 'data' para o tipo datetime
df['data'] = pd.to_datetime(df['data'], format='mixed')

# Substituir vírgulas por pontos e converter as colunas para float
df['temperature'] = df['temperature'].str.replace(',', '.').astype(float)
df['humidity'] = df['humidity'].str.replace(',', '.').astype(float)

# Definindo o período específico
data_inicio = '2024-03-19 00:00:00'
data_fim = '2024-03-20 08:00:00'

# Filtrando os dados pelo período específico
df_filtrado_por_periodo = df[(df['data'] >= data_inicio) & (df['data'] <= data_fim)]

# Remover linhas com valores em branco nas colunas de temperatura e umidade
df_filtrado_por_periodo = df_filtrado_por_periodo.dropna(subset=['temperature', 'humidity'])

# Dispositivos a serem desconsiderados
dispositivos_a_desconsiderar = ['senzemo', 'sirrosteste_UCS_AMV-22', 'sirrosteste_UCS_AMV-19']

# Filtrar os dados para desconsiderar os dispositivos especificados
df_filtered = df_filtrado_por_periodo[df_filtrado_por_periodo['device'].isin(dispositivos_a_desconsiderar)]



# Verificar se a coluna 'device' está presente no dataframe filtrado
if 'device' in df_filtered.columns:
    
    # Quantidade de registros retornados
    num_registros = len(df_filtered)
    
    # Quantidade de dispositivos presentes na coluna 'device'
    num_dispositivos = df_filtered['device'].nunique()

    print(f"Quantidade de registros retornados: {num_registros}")
    print(f"Quantidade de dispositivos presentes na coluna 'device': {num_dispositivos}")
    
    # Agrupamento dos dados por dispositivo
    grouped = df_filtered.groupby('device')

    # Variáveis que queremos plotar
    variables = ['temperature', 'humidity']

    # Calcular o número de linhas e colunas para os subplots
    num_plots = len(variables)
    num_cols = 2 if num_plots > 1 else 1
    num_rows = (num_plots + 1) // 2  # Adiciona 1 para garantir que haja pelo menos uma linha

    # Criação de subplots para cada variável
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

    # Loop sobre cada variável e plotagem dos dados
    for i, var in enumerate(variables):
        row = i // num_cols
        col = i % num_cols
        if num_rows == 1 or num_cols == 1:
            ax = axs[i]
        else:
            ax = axs[row, col]
        soma = 0
        for device, data in grouped:
            data.plot(x='data', y=var, title=var, ax=ax, label=device, fontsize=8)
            soma = soma+1
        ax.set_ylabel('Valor', fontsize=8)
        ax.set_xlabel('Data', fontsize=8)
        ax.legend(loc='upper left', fontsize=8)

    # Ajustes de layout
    plt.suptitle(f"Quantidade de registros retornados: {num_registros}", fontsize=12)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.6, wspace=0.11)  # Ajuste os espaçamentos entre os subplots
    plt.show()
    print(soma)
else:
    print("A coluna 'device' não foi encontrada no arquivo CSV filtrado.")
