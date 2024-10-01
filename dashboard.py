import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard - Aluguel de Casas", layout="wide")


with st.container():
  st.subheader('Universidade Federal do Maranhão - UFMA')
  st.subheader('Especialização em Análise de Dados e IA')
  st.subheader('Disciplina Visualização de Dados', divider="gray")
  st.title("Dashboard de Aluguel de Casas")
  st.write('Gabriel Silva - [Github](https://github.com/gfcarvalhos)')

@st.cache_data
def carregar_dados():
  dados = pd.read_csv('houses_to_rent_v2.csv')
  return dados

with st.container(border=True):
  col1, col2, col3 = st.columns(3)
  dados = carregar_dados()

  total_casas = dados['city'].value_counts().sum()
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

with st.container(border=True):
  col1, col2, col3 = st.columns(3)
  dados = carregar_dados()

  dados_por_cidade = dados['city'].value_counts().reset_index()
  dados_por_cidade.columns = ['city', 'count']

  fig_dados_por_cidade = px.pie(dados_por_cidade,values='count',names='city', 
                                title='Porcentagem de Imóveis por Cidade',
                                color_discrete_sequence=px.colors.qualitative.Bold)
  fig_dados_por_cidade.update_traces(textfont=dict(size=12, color='black', family='Arial, sans-serif', weight='bold'))
  col1.plotly_chart(fig_dados_por_cidade)

  dados_media_total = dados[['total (R$)', 'city']].groupby('city').mean().reset_index()
  dados_media_total['total (R$)'] = dados_media_total['total (R$)'].round(2)

  fig_media_total = px.bar(dados_media_total, x='city', y='total (R$)',  
                     title="Média do Valor de Aluguel por Cidade",
                     labels={'total (R$)': 'Total (R$)', 'city': 'Cidade'},
                     color = 'total (R$)',
                     text='total (R$)',
                     color_continuous_scale=px.colors.sequential.Blues)
  fig_media_total.update_coloraxes(showscale=False)
  fig_media_total.update_traces(textfont=dict(size=12, color='black', family='Arial, sans-serif', weight='bold')) 
  col2.plotly_chart(fig_media_total)

  dados_media_area = dados[['area', 'city']].groupby('city').mean().reset_index()
  dados_media = pd.merge(dados_media_total, dados_media_area, on='city', suffixes=('_total', '_area'))
  dados_media['metro_quadrado'] = dados_media['total (R$)'] / dados_media['area']
  dados_media['metro_quadrado'] = dados_media['metro_quadrado'].round(2)

  fig_metro_quadrado = px.bar(dados_media, x= 'metro_quadrado', y='city', 
                              title='Valor do metro quadrado por cidade',
                              orientation='h',text='metro_quadrado',
                              labels={'metro_quadrado': 'Valor do Metro Quadrado (R$)', 'city': 'Cidade'}, 
                              color = 'metro_quadrado',
                              color_continuous_scale=px.colors.sequential.Blues)
  fig_metro_quadrado.update_coloraxes(showscale=False) 
  fig_metro_quadrado.update_traces(textfont=dict(size=12, color='black', family='Arial, sans-serif', weight='bold'))
  col3.plotly_chart(fig_metro_quadrado)


with st.container():
  st.write('---')
  dados_nao_tratados = carregar_dados()
  nome_cidade = st.selectbox('Cidade', dados_nao_tratados['city'].unique())
