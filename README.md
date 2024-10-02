# Atividade Referente à disciplina Visualização de Dados

## Especialização em Análise de Dados e Inteligência Artificial - UFMA

O objetivo dessa atividade é gerar um dashboard a partir dos dados de aluguel de casas no Brasil.

---

### 📋 Pré-requisitos

Para rodar o projeto, você precisará ter instalado:

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

### 🔧 Instalação

1. Clone o repositório em sua máquina local:
   ```bash
   git clone https://github.com/gfcarvalhos/dashboardRentHouses.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd <diretorio-do-projeto/dashboardRentHouses>
   ```
3. Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Executando o Dashboard

Para executar o dashboard, utilize o seguinte comando:

```bash
streamlit run dashboard.py
```

O dashboard será aberto no navegador, permitindo a exploração interativa dos dados de aluguel de imóveis.

---

## 📃 Estudo do caso

O conjunto de dados em analise é o Brazilian houses to Rent, publicado em https://www.kaggle.com/datasets/rubenssjr/brasilian-houses-to-rent. O dataset possuí 13 colunas, sendo:

- city: Cidade onde está localizada o imóvel
- area: Área em m² do imóvel
- rooms: Quantidade de quartos
- bathroom: Quantidade de banheiros
- parking spaces: Quantidade de garagens
- floor: Andar da casa
- animal: Se permite ou não animal doméstico
- furniture: Se o imóvel está ou não mobiliado
- hoa (R$): Valor da taxa de condomínio
- rent amount (R$): Valor do aluguel
- property tax (R$): Valor do IPTU
- fire insurance (R$): Valor do seguro de incêndio
- total (R$): Valor total de aluguel do imóvel

---

## 📊 Análise explanatória

Data Storytelling

Tema: Informativo sobre o aluguel de casas nas cidades de São Paulo, Porto Alegre, Rio de Janeiro, Campinas e Belo Horizonte.

Publico-alvo: pessoas que queiram alugar casas nessas cidades

Objetivo: Auxiliar na melhor escolha de aluguel, considerando os questionamentos:

- Qual o percentual/quantidade de casas para alugar por cidade? ✅
- Qual o valor do metro quadrado para alugar total e por cidade? ✅
- Qual a média de valor total do aluguel e por cidade? ✅
- Qual a média de area e aluguel por cidade? (Correlacionados)
- Como estão distribuidos os valores imbutidos no aluguem por cidade?
- Onde se concetram os imoveis com maior valor de aluguel? E os de menor valor?
- Como estão distribuidos os imoveis por valor de aluguel, área e que podem ou não ter animais de estimação?
- Qual a relação entre o preço e a presença ou não de mobília por cidade?
- Qual a relação entre andar e valor total do aluguel por cidade?
- Qual a relação entre quantidade de vagas de estacionamento e valor total do aluguel?
