import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns


# Método para extrair várias páginas de uma só vez
def scrape_stats(base_url, year_start, year_end):
    years = range(year_start,year_end+1,1)

    final_df = pd.DataFrame()

    for year in years:
        print('Extraindo ano {}'.format(year))
        req_url = base_url.format(year)
        req = requests.get(req_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        table = soup.find('table', {'id':'totals_stats'})
        df = pd.read_html(str(table))[0]
        df['Year'] = year

        final_df = final_df.append(df)
    return final_df


# Utilizando o método
url = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'
df = scrape_stats(url, 2013,2018)

drop_indexes = df[df['Rk'] == 'Rk'].index
df.drop(drop_indexes, inplace=True)

# Convertendo tabelas para valores numéricos
numeric_cols = df.columns.drop(['Player', 'Pos', 'Tm'])
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

# Gráfico de média de bolas de 3 pontos arremessadas por ano
plt.scatter(x='Year', y='3PA')
plt.show()

sorted_df = df.sort_values(by=['3P'], axis=0, ascending=False)
sorted_df[['Player', '3P', 'Year']].head()

# Agrupando os dados por jogador e somando os valores
grouped_df = df.groupby('Player', as_index=False).sum()
# Ordena Data Frame por bolas de 3 pontos convertidas em ordem decrescente
sorted_df = df.sort_values(by=['3P'], axis=0, ascending=False)
# Mostra 5 primeiras posições da tabela
sorted_df[['Player', '3P', '3PA']].head()
print(sorted_df)
