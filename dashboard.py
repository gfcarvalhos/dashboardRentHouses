import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard - Aluguel de Casas")


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

with st.container():
  col1, col2 = st.columns(2)
  dados = carregar_dados()

  dados_por_cidade = dados['city'].value_counts().reset_index()
  dados_por_cidade.columns = ['city', 'count']
  fig_dados_por_cidade = px.pie(dados_por_cidade,values='count',names='city', title='Quantidade de Imóveis por Cidade')
  col1.plotly_chart(fig_dados_por_cidade)

  dados_media_total = dados[['total (R$)', 'city']].groupby('city').mean().reset_index()
  fig_teste_2 = px.bar(dados_media_total, x='city', y='total (R$)',  
                     title="Média do Aluguel Total por Cidade",
                     labels={'total (R$)': 'Total (R$)', 'city': 'Cidade'})
  col2.plotly_chart(fig_teste_2)


with st.container():
  st.write('---')
  dados_nao_tratados = carregar_dados()
  nome_cidade = st.selectbox('Cidade', dados_nao_tratados['city'].unique())
