import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard - Aluguel de Casas", layout="wide")

def remove_outliers(dados, campo):
  #Calculo dos quartis e IQR
  Q1 = dados[campo].quantile(0.25)
  Q3 = dados[campo].quantile(0.75)
  IQR = Q3 - Q1
  #Define limites para outliers em relação a área
  limite_inferior = Q1 - 4 * IQR
  limite_superior = Q3 + 4 * IQR
  #Retira outliers referente a área
  dados = dados[(dados[campo] >= limite_inferior) & (dados[campo] <= limite_superior)]
  return dados


@st.cache_data
def carregar_dados():
  dados = pd.read_csv('houses_to_rent_v2.csv')
  #Remove outliers de area
  dados_tratados = remove_outliers(dados, 'area')
  dados_final = remove_outliers(dados_tratados, 'total (R$)')
  return dados_final

#Carrega os dados para uso nos containers
dados = carregar_dados()

#Cabeçalho do dashboard
with st.container():
  st.subheader('Universidade Federal do Maranhão - UFMA')
  st.subheader('Especialização em Análise de Dados e IA')
  st.subheader('Disciplina Visualização de Dados', divider="gray")
  st.title("Dashboard de Aluguel de Casas")
  st.write('Gabriel Silva - [Github - Projeto](https://github.com/gfcarvalhos/dashboardRentHouses)')

#Primeira linha de graficos - Visao Global
with st.container(border=True):
  col1, col2, col3 = st.columns(3)
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

#Segunda linha de gráficos - Visao Global por Cidade
with st.container(border=True):
  col1, col2, col3 = st.columns(3)

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
                     labels={'total (R$)': 'Valor médio de aluguel (R$)', 'city': 'Cidade', 'color': 'Custo'},
                     color = 'color',
                     text=dados_media_total['total (R$)'].apply(lambda x: f'R$ {x}'),
                    color_discrete_map={
                      'Abaixo da média': '#aec7e8',
                      'Acima da média': '#1f77b4'   
                    })
  #Formata fonte da letra
  fig_media_total.update_traces(textfont=dict(size=9, color='white', family='Arial, sans-serif', weight='bold'))
  #Posiciona o titulo
  fig_media_total.update_layout(
    xaxis_title=None,
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
    line=dict(color="gold", width=2, dash="dash"),
  )
  #Legenda para a linha pontilhada
  fig_media_total.add_annotation(
    x=len(dados_media_total) - 0.5,
    y=media_aluguel*1.05,
    text=f"Custo médio",
    showarrow=False,
    font=dict(size=12, color="gold"),
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
                              orientation='h',
                              text=dados_media['metro_quadrado'].apply(lambda x: f'R$ {x}'),
                              labels={'metro_quadrado': 'Valor médio do Metro Quadrado (R$)', 'city': 'Cidade'}, 
                              color = 'color',
                              color_discrete_map={
                                'Abaixo da média': '#aec7e8',
                                'Acima da média': '#1f77b4'     
                             })
  fig_metro_quadrado.update_traces(textfont=dict(size=10, color='white', family='Arial, sans-serif', weight='bold'))
  fig_metro_quadrado.update_layout(
    xaxis_title=None,
    showlegend=False,
    title={
          'text': 'Valor do Metro Quadrado por Cidade',
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
    line=dict(color="gold", width=2, dash="dash"),
  )

  #Legenda para a linha pontilhada
  fig_metro_quadrado.add_annotation(
    y=len(dados_media) - 0.5,
    x=media_metro_quadrado,
    text=f"Custo médio",
    showarrow=False,
    font=dict(size=12, color="gold"),
    yanchor="bottom"
  )
  col3.plotly_chart(fig_metro_quadrado)

#Terceira linha de gráficos - Histograma Qtd x area x custo medio do m²
with st.container(border=True):
  #Calculo do metro quadrado mais barato
  dados['preco_metro_quadrado'] = dados['total (R$)'] / dados['area']
  preco_medio = dados['preco_metro_quadrado'].mean()

  #Condicao para realce de melhor custo-benefico considerando valor médio do metro quadrado
  dados['color'] = ['m² abaixo do valor médio' if preco <= preco_medio else 'm² acima do valor médio' for preco in dados['preco_metro_quadrado']]

  fig_area_aluguel = px.histogram(dados, x='area', 
                                 color='color', 
                                 hover_name='city', 
                                 facet_col='city', 
                                 nbins=30,
                                 labels={'color': 'Legenda'},
                                 color_discrete_map={
                                    'm² abaixo do valor médio': '#aec7e8', 
                                    'm² acima do valor médio': '#1f77b4'  
                                })
  fig_area_aluguel.update_layout(
    title={
          'text': 'Distribuição de Imóveis com Destaque para Preço/m² Abaixo da Média',
            'y': 0.97,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',}, 
    yaxis_title=None,  
    yaxis=dict(title='Distribuição de Imóveis', title_font=dict(size=14))  
  )
  #Atualiza o titulo dos eixos X
  fig_area_aluguel.for_each_xaxis(lambda xaxis: xaxis.update(title='Área (m²)', title_font=dict(size=14)))
  #Acrescenta bordas por intervalo
  fig_area_aluguel.update_traces(marker_line=dict(color='black', width=1))
  #Atualiza o subtitulo dos histogramas
  fig_area_aluguel.for_each_annotation(lambda a: a.update(text=a.text.split('=')[1]))
  st.plotly_chart(fig_area_aluguel)

#Quarta linha de gráficos - Valores imbutidos no aluguel por cidade
with st.container(border=True):
  dados_medios_imbutidos = dados.groupby('city')[['rent amount (R$)', 'hoa (R$)', 'property tax (R$)', 'fire insurance (R$)']].mean().reset_index().round(2)

  fig_valores_imbutidos = px.area(dados_medios_imbutidos, 
                                    x="city", 
                                    y=['rent amount (R$)', 'hoa (R$)', 'property tax (R$)', 'fire insurance (R$)'],
                                    labels={'value': 'Média dos Valores Imbutidos (R$)', 'city': 'Cidades'},
                                    title='Distribuição da Média dos Valores Embutidos no Aluguel por Cidade',
                                    )

  labels = {
    'rent amount (R$)': 'Aluguel (R$)',
    'hoa (R$)': 'Taxa de HOA (R$)',
    'property tax (R$)': 'Valor do IPTU (R$)',
    'fire insurance (R$)': 'Seguro Contra Incêndio (R$)',
  }
  fig_valores_imbutidos.for_each_trace(lambda t: t.update(name=labels[t.name]))
  fig_valores_imbutidos.update_traces(stackgroup = None, 
                                      fill = 'tozeroy',
                                      mode="markers+lines", 
                                      hovertemplate=None)
  
  fig_valores_imbutidos.update_layout(
    title={
          'text': 'Distribuição da Média dos Valores Embutidos no Aluguel por Cidade',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',}, 
    legend_title='Legenda',
    xaxis_title=None
  )
  fig_valores_imbutidos.update_xaxes(range=[-0.2, len(dados_medios_imbutidos['city']) - 0.2])
  st.plotly_chart(fig_valores_imbutidos)

#Quinta linha de gráficos - Análise para animais de estimação
with st.container(border=True):
  col1, col2, col3 = st.columns(3)

  #Grafico de porcentagem de aceites e não aceites
  contagem_animais = dados.groupby('city')['animal'].value_counts().reset_index()

  contagem_animais['total'] = contagem_animais.groupby('city')['count'].transform('sum')
  contagem_animais['percent'] = (contagem_animais['count'] / contagem_animais['total']) * 100

  fig_porcentagem_animais_cidade = go.Figure()

  dados_aceita_animais = contagem_animais[contagem_animais['animal'] == 'acept']
  dados_nao_aceita_animais = contagem_animais[contagem_animais['animal'] == 'not acept']
  #Grafico de acept
  fig_porcentagem_animais_cidade.add_trace(go.Bar(
    y=dados_aceita_animais['city'], 
    x=dados_aceita_animais['percent'], 
    name='Aceita', 
    orientation='h', 
    marker_color='#aec7e8',
    text=dados_aceita_animais['percent'].round(2).astype(str) + '%',
    textposition='inside',
    customdata=dados_aceita_animais['percent'],
    hovertemplate='%{y}<br>Aceita: %{x:.2f}%<extra></extra>'
))
  #Grafico de not acept
  fig_porcentagem_animais_cidade.add_trace(go.Bar(
    y=dados_nao_aceita_animais['city'], 
    x=-dados_nao_aceita_animais['percent'], 
    name='Não Aceita', 
    orientation='h', 
    marker_color='#1f77b4',
    text=dados_nao_aceita_animais['percent'].round(2).astype(str) + '%',
    textposition='inside',
    hovertemplate='%{y}<br>Não Aceita: %{customdata:.2f}%<extra></extra>',
    customdata=dados_nao_aceita_animais['percent']
))
  fig_porcentagem_animais_cidade.update_layout(
    title={
          'text': 'Porcentagem de Imóveis em Aceite de Animais',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',}, 
    xaxis_title=None,
    yaxis_title= None,
    barmode='overlay',
    xaxis=dict(showgrid=True, zeroline=True, showticklabels=False),
    showlegend=True,
    )
  col1.plotly_chart(fig_porcentagem_animais_cidade)

  #Grafico 2 - Quanto a area
  dados_animais_area = dados

  fig_animais_area = px.histogram(dados_animais_area, 
                                  x='area', 
                                  color='animal',
                                  facet_col='animal', 
                                  nbins=30,
                                  labels={'area': 'Área (m²)'},
                                  title='Distribuição de Imóveis por Área',
                                  marginal='violin')

  #Coloca bordas nos intervalos
  fig_animais_area.update_traces(marker_line=dict(color='black', width=1))
  #Atualiza legenda
  fig_animais_area.for_each_trace(lambda t: t.update(name='Aceita' if t.name == 'acept' else 'Não Aceita'))

  #Atualiza layout
  fig_animais_area.update_layout(
    title={
          'text': 'Distribuição de Imóveis por Área em Aceite de Animais',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',}, 
    legend_title=None,
    yaxis_title='Distribuição de Imóveis por área',
  )
  # Remove o "= valor" da anotação do eixo
  fig_animais_area.for_each_annotation(lambda a: a.update(text=''))

  col2.plotly_chart(fig_animais_area)

  #Grafico 3 - Quanto a custo
  dados_animais_custo = dados

  fig_animais_custo = px.scatter(dados_animais_custo, 
                                 x='area', 
                                 y='total (R$)', 
                                 color='animal',
                                 labels={'area': 'Área (m²)'})
  
  # Adicionando um retângulo claro para realçar uma área específica
  fig_animais_custo.add_shape(
    type="rect",
    x0=50,  
    x1=200, 
    y0=0, 
    y1=dados_animais_custo['total (R$)'].max()*1.02, 
    fillcolor="rgba(255, 255, 0, 0.2)",  
    line=dict(color="rgba(255, 255, 0, 0)"), 
  )
  #Atualiza legenda
  fig_animais_custo.for_each_trace(lambda t: t.update(name='Aceita' if t.name == 'acept' else 'Não Aceita'))

  fig_animais_custo.update_layout(
    title={
          'text': 'Distribuição de Imóveis por Área e Custo em Aceite de Animais',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',}, 
    legend_title=None,
  )
  col3.plotly_chart(fig_animais_custo)

#Sexta linha de gráfico - Análise para mobília
with st.container(border=True):
  col1, col2 = st.columns(2)
  #dados_mobilia = dados.groupby('city')['furniture'].value_counts().reset_index()
  dados_mobilia = dados

  fig_mobilia_distribuicao = px.histogram(dados_mobilia, 
                                          x='area', 
                                          color='furniture',
                                          labels={'area': 'Área (m²)'},
                                          title='Distribuição de Imóveis Mobiliados e não Mobiliados',
                                          nbins=40,
                                          color_discrete_map={
                                            'furnished': '#aec7e8',
                                            'not furnished': '#1f77b4'
                                          }
                                          )
  fig_mobilia_distribuicao.update_layout(
    legend_title=None,
    title={
          'text': 'Distribuição de Imóveis Mobiliados e não Mobiliados',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',},
    yaxis_title='Distribuição de Imóveis por área',
  )
  #Atualiza legenda
  fig_mobilia_distribuicao.for_each_trace(lambda t: t.update(name='Mobiliado' if t.name == 'furnished' else 'Não Mobiliado'))
  #Acrescenta bordas por intervalo
  fig_mobilia_distribuicao.update_traces(marker_line=dict(color='black', width=1))

  col1.plotly_chart(fig_mobilia_distribuicao)

  #Grafico 2 - Visao por cidade
  dados_mobilia_cidades = dados.groupby('city')['furniture'].value_counts().reset_index()
  dados_mobilia_cidades['preco_medio'] = dados.groupby(['city', 'furniture'])['total (R$)'].mean().reset_index(drop=True).round(2)

  fig_mobilia_cidades = px.scatter(dados_mobilia_cidades, 
                   x='city', 
                   y='preco_medio', 
                   size ='count', 
                   color='furniture',
                   title='Distribuição de Imóveis por valor e quantidade (size) nas Cidades',
                   color_discrete_map={
                     'furnished': '#aec7e8',
                     'not furnished': '#1f77b4'
                   })
  #Atualiza legenda
  fig_mobilia_cidades.for_each_trace(lambda t: t.update(name='Mobiliado' if t.name == 'furnished' else 'Não Mobiliado'))
  #Acrescenta bordas por intervalo
  fig_mobilia_cidades.update_layout(
    title={
          'text': 'Distribuição de Imóveis por valor médio e quantidade (size) nas Cidades',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',},
    yaxis_title='Média de Custo do Alugel (R$)',
    xaxis_title='Área (m²)',
    legend_title=None
  )
  col2.plotly_chart(fig_mobilia_cidades)
#Sétima linha de gráfico - Análise por andar
#Oitava linha de gráfico - Análise por vaga de estacionamento
