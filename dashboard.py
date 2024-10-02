import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard - Aluguel de Casas", layout="wide")

@st.cache_data
def carregar_dados():
  dados = pd.read_csv('houses_to_rent_v2.csv')
  return dados

#Cabeçalho do dashboard
with st.container():
  st.subheader('Universidade Federal do Maranhão - UFMA')
  st.subheader('Especialização em Análise de Dados e IA')
  st.subheader('Disciplina Visualização de Dados', divider="gray")
  st.title("Dashboard de Aluguel de Casas")
  st.write('Gabriel Silva - [Github - Projeto](https://github.com/gfcarvalhos/dashboardRentHouses)')

#Primeira linha de graficos
with st.container(border=True):
  col1, col2, col3 = st.columns(3)
  dados = carregar_dados()

  total_casas = dados['city'].value_counts().sum()

  #Cards referentes a analise geral dos dados
  fig_total_casas = go.Figure(go.Indicator(
    mode = "number",
    value = total_casas,
    title = {"text": "Quantidade Total de Imóveis", "font": {"size": 20}},  
    number = {'valueformat': ",.0f", 'font': {"size": 50}}
  ))
  fig_total_casas.update_layout(
    height=150,
    width=270, 
    margin=dict(l=50, r=20, t=50, b=20), 
  )
  col1.plotly_chart(fig_total_casas)

  valor_total = dados['total (R$)'].sum()
  valor_medio_geral = valor_total / total_casas

  fig = go.Figure(go.Indicator(
    mode = "number", 
    value = valor_medio_geral, 
    title = {"text": "Custo Médio do Aluguel", "font": {"size": 20}},
    number = {'prefix': "R$ ", 'valueformat': ',.2f', 'font': {"size": 45}}
  ))
  fig.update_layout(
    height=150,
    width=270, 
    margin=dict(l=20, r=20, t=50, b=20), 
  )
  col2.plotly_chart(fig)

  area_total = dados['area'].sum()
  metro_quadrado_total = valor_total/area_total

  fig_metro_quadrado_total = go.Figure(go.Indicator(
    mode = "number", 
    value = metro_quadrado_total, 
    title = {"text": "Custo do Metro Quadrado", "font": {"size": 20}},
    number = {'prefix': "R$ ", 'valueformat': ',.2f', 'font': {"size": 45}, 'suffix': '/m²'}
  ))
  fig_metro_quadrado_total.update_layout(
    height=150,
    width=270, 
    margin=dict(l=20, r=20, t=50, b=20), 
  )
  col3.plotly_chart(fig_metro_quadrado_total)

#Segunda linha de gráficos
with st.container(border=True):
  col1, col2, col3 = st.columns(3)
  dados = carregar_dados()
  
  #Grafico de arvore representando a distribuição de imoveis por cidade
  dados_por_cidade = dados['city'].value_counts().reset_index()
  dados_por_cidade.columns = ['city', 'count']
  dados_por_cidade['percent'] = (dados_por_cidade['count'] / dados_por_cidade['count'].sum()) * 100
  
  fig_dados_por_cidade = px.treemap(dados_por_cidade,values='count',path=['city'], 
                                title='Distribuição de Imóveis por Cidade',
                                color_discrete_sequence=px.colors.sequential.Blues_r,
                                custom_data=['percent']
                                )
  #Adiciona quantidade de imoveis e porcentagem por cidade e fonte da letra
  fig_dados_por_cidade.update_traces(
    texttemplate='%{label}<br>%{value} imóveis<br>%{customdata:.2f}%',
    textfont=dict(size=12, color='white', family='Arial, sans-serif', weight='bold'),
    hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<br>Porcentagem: %{customdata:.2f}%'
  )
  #Reposiciona o titulo
  fig_dados_por_cidade.update_layout(
    title={
          'text': 'Distribuição de Imóveis por Cidade',
            'y': 0.90,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',}
)
  col1.plotly_chart(fig_dados_por_cidade)

  #Grafico do valor médio do aluguel por cidade comparando ao valor medio geral
  dados_media_total = dados[['total (R$)', 'city']].groupby('city').mean().reset_index()
  dados_media_total['total (R$)'] = dados_media_total['total (R$)'].round(2)
  media_aluguel = dados_media_total['total (R$)'].mean()
  dados_media_total['color'] = dados_media_total['total (R$)'].apply(lambda x: 'Abaixo da média' if x < media_aluguel else 'Acima da média')

  fig_media_total = px.bar(dados_media_total, x='city', y='total (R$)',  
                     title="Média do Valor de Aluguel por Cidade",
                     labels={'total (R$)': 'Total (R$)', 'city': ''},
                     color = 'color',
                     text='total (R$)',
                    color_discrete_map={
                      'Abaixo da média': '#1f77b4',
                      'Acima da média': '#aec7e8'     
                    })
  #Retira legenda de cores
  fig_media_total.update_coloraxes(showscale=False)
  #Formata fonte da letra
  fig_media_total.update_traces(textfont=dict(size=12, color='white', family='Arial, sans-serif', weight='bold'))
  #Posiciona o titulo
  fig_media_total.update_layout(
    showlegend=False,
    title={
          'text': 'Média do Valor de Aluguel por Cidade',
            'y': 0.90,
            'x': 0.55,
            'xanchor': 'center',
            'yanchor': 'top',}
) 

  #Adiciona uma linha pontilhada horizontal para a média
  fig_media_total.add_shape(
    type="line",
    x0=-0.5, #inicio do eixo
    x1=len(dados_media_total)-0.5, #fim do eixo
    y0=media_aluguel,
    y1=media_aluguel,
    line=dict(color="lightcoral", width=2, dash="dash"),
  )

  #Legenda para a linha pontilhada
  fig_media_total.add_annotation(
    x=len(dados_media_total)/2,
    y=media_aluguel*1.05,
    text=f"Custo médio",
    showarrow=False,
    font=dict(size=12, color="lightcoral"),
    xanchor="right"
  )
  col2.plotly_chart(fig_media_total)

  dados_media_area = dados[['area', 'city']].groupby('city').mean().reset_index()
  dados_media = pd.merge(dados_media_total, dados_media_area, on='city', suffixes=('_total', '_area'))
  dados_media['metro_quadrado'] = dados_media['total (R$)'] / dados_media['area']
  dados_media['metro_quadrado'] = dados_media['metro_quadrado'].round(2)
  media_metro_quadrado = dados_media['metro_quadrado'].mean()
  dados_media['color'] = dados_media['metro_quadrado'].apply(lambda x: 'Abaixo da média' if x < media_metro_quadrado else 'Acima da média')

  fig_metro_quadrado = px.bar(dados_media, x= 'metro_quadrado', y='city', 
                              title='Valor do metro quadrado por cidade',
                              orientation='h',text='metro_quadrado',
                              labels={'metro_quadrado': 'Valor do Metro Quadrado (R$)', 'city': ''}, 
                              color = 'color',
                              color_discrete_map={
                                 'Abaixo da média': '#1f77b4',  
                                 'Acima da média': '#aec7e8'    
                             })
  fig_metro_quadrado.update_coloraxes(showscale=False) 
  fig_metro_quadrado.update_traces(textfont=dict(size=12, color='white', family='Arial, sans-serif', weight='bold'))
  fig_metro_quadrado.update_layout(
    showlegend=False,
    title={
          'text': 'Valor do metro quadrado por cidade',
            'y': 0.90,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',}
) 

  #Adiciona uma linha pontilhada horizontal para a média
  fig_metro_quadrado.add_shape(
    type="line",
    x0=media_metro_quadrado,
    x1=media_metro_quadrado,
    y0=-0.5, #inicio do eixo
    y1=len(dados_media)-0.5, #fim do eixo
    line=dict(color="lightcoral", width=2, dash="dash"),
  )

  #Legenda para a linha pontilhada
  fig_metro_quadrado.add_annotation(
    y=len(dados_media) - 0.5,
    x=media_metro_quadrado,
    text=f"Custo médio",
    showarrow=False,
    font=dict(size=12, color="lightcoral"),
    yanchor="bottom"
  )
  col3.plotly_chart(fig_metro_quadrado)


with st.container():
  st.write('---')
  dados_nao_tratados = carregar_dados()
  nome_cidade = st.selectbox('Cidade', dados_nao_tratados['city'].unique())
