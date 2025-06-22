import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

import requests

app = dash.Dash(__name__)

api_key = '##'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    raise RuntimeError('Request failed')

data = response.json().get('data')[:10]
names = [o.get('name') for o in data]
symbols = [o.get('symbol') for o in data]
market_caps = [o.get('quote', {}).get('USD', {}).get('market_cap', 0) for o in data]
circulating_supplies = [o.get('circulating_supply') for o in data]
market_cap_dominance = [o.get('quote', {}).get('USD', {}).get('market_cap_dominance', 0) for o in data]
volumes = [o.get('quote', {}).get('USD', {}).get('volume_24h', 0) for o in data]
platforms = [o['platform']['name'] if o['platform'] is not None else o['name'] for o in data]

# 1
data_fig_mc = {
    'Cryptocurrency': names,
    'MarketCap': market_caps,
    'Platform': platforms,
    'circulating_supply': circulating_supplies
}

df = pd.DataFrame(data_fig_mc)
fig_mc = px.scatter(df,
                 x='Cryptocurrency',
                 y='MarketCap',
                 size='circulating_supply',
                 color='Platform',
                 hover_name='Cryptocurrency',
                 size_max=100)


# 2
data_market_dominance = {
    'Name': names,
    'Symbol': symbols,
    'Category': platforms,
    'market_cap_dominance': market_cap_dominance
}

df = pd.DataFrame(data_market_dominance)
fig_market_dominance = px.bar(
    df,
    x="market_cap_dominance",
    y="Name",
    orientation='h',
    color="Category",
    hover_name="Name",
    labels={"market_cap_dominance": "Market Dominance (% relative to USD)", "Name": "Cryptocurrency"},
    title="Market Dominance by Cryptocurrency"
)

fig_market_dominance.update_layout(yaxis={'categoryorder': 'total ascending'})


# 3
data_supply_vs_cap = [
    {
        "name": o['name'],
        "symbol": o['symbol'],
        "category": o.get('platform').get('name') if o.get('platform') is not None else o['name'],
        "circulating_supply": o['circulating_supply'],
        "market_cap": o['quote'].get('USD', {}).get('market_cap', 0),
        "num_market_pairs": o['num_market_pairs'],
    } for o in data
]

df = pd.DataFrame(data_supply_vs_cap)

fig_supply_vs_cap = px.scatter(
    df,
    x="circulating_supply",
    y="market_cap",
    size="num_market_pairs",
    color="category",
    hover_name="name",
    text="symbol",
    # color_discrete_map=color_map,
    size_max=60,
    labels={
        "circulating_supply": "Circulating Supply",
        "market_cap": "Market Capitalization"
    },
    title="Circulating Supply vs. Market Cap"
)

fig_supply_vs_cap.update_traces(textposition='top center')


# 4
data_fig_bar = {
    'Name': names,
    'Volume (24h)': volumes,
    'Category': platforms
}

df = pd.DataFrame(data_fig_bar)

fig_bar = px.bar(df, x='Name', y='Volume (24h)', color='Category', hover_name='Name')


# 5
categories_mcs = {}
for d in data:
    plat = d['platform']['name'] if d['platform'] is not None else d['name']
    mc = d.get('quote', {}).get('USD', {}).get('market_cap', 0)
    if plat in categories_mcs:
        categories_mcs[plat] += mc
    else:
        categories_mcs[plat] = mc

data_fig_pie = {
    'Category': categories_mcs.keys(),
    'MarketCap': categories_mcs.values(),
}

df = pd.DataFrame(data_fig_pie)

fig_pie = px.pie(df, names='Category', values='MarketCap', color='Category')


app.layout = html.Div([
    html.H1("Cryptocurrency Dashboard"),
    dcc.Tabs([
        dcc.Tab(label='Market Cap', children=[
            dcc.Graph(figure=fig_mc)
        ]),
        dcc.Tab(label='Market Dominance', children=[
            dcc.Graph(figure=fig_market_dominance)
        ]),
        dcc.Tab(label='Circulating Supply vs. Market Cap', children=[
            dcc.Graph(figure=fig_supply_vs_cap)
        ]),
        dcc.Tab(label='Trading Volume', children=[
            dcc.Graph(figure=fig_bar)
        ]),
        dcc.Tab(label='Market Dominance Per Platform (category)', children=[
            dcc.Graph(figure=fig_pie)
        ])
    ]),
    html.Div('''
    Az alábbiakban egy átfogó, interaktív kriptovaluta dashboard kerül bemutatásra, amely öt különböző diagram 
    segítségével szemlélteti a legfontosabb piaci mutatókat. Ezek a diagramok a CoinMarketCap adatai alapján készültek, 
    és céljuk, hogy a felhasználók könnyen áttekintsék a kriptovaluták piaci teljesítményét, kategóriák szerinti 
    megoszlását és dominanciáját. A diagramok színkódolással is segítik a különböző kategóriák közötti 
    megkülönböztetést, például a memecoinok, NFT-projektek vagy az Ethereum-alapú tokenek esetében.
    '''),
    html.Ol([
        html.Li(
            [html.B('Piaci Kapitalizáció Buborékdiagram (Scatter Plot)'), html.Br(),
            '''Az első diagram egy buborékdiagram, amely a legnagyobb piaci kapitalizációval rendelkező 
            kriptovalutákat ábrázolja. Az X tengely és a Y tengely a kriptovaluták elhelyezkedését mutatja, míg a 
            buborékok mérete az adott érme piaci kapitalizációját jelzi. A színek a kategóriák szerint vannak kódolva.
            Interaktív funkció: Buborékokra történő rámutatáskor egy címke megjelenik, kiemelve az adott érme részletes 
            adatait, például a piaci kapitalizációt.''']),
        html.Li(
            [html.B('Kereskedési Volumen Oszlopdiagram (Trading Volume Bar Chart)'), html.Br(), '''
            Ez az oszlopdiagram a kriptovaluták napi kereskedési volumenét mutatja be. Az X tengely a kriptovaluták 
            neveit, a Y tengely pedig a 24 órás kereskedési volument jeleníti meg. A színek ismételten a kategóriák 
            szerinti megkülönböztetést segítik. Interaktív funkció: Az oszlopokra történő rámutatás részletes adatokat 
            jelenít meg a kereskedési volumenről és az adott érme piaci aktivitásáról.''']),
        html.Li(
            [html.B('Piaci Dominancia Kördiagram (Market Dominance Pie Chart)'), html.Br(), '''
            Ez a kördiagram a különböző kriptovaluta kategóriák piaci dominanciáját szemlélteti. Az egyes szeletek 
            nagysága az adott kategória összesített piaci kapitalizációját jelzi, megmutatva, hogy például a memecoinok 
            vagy a platform tokenek mekkora részesedéssel bírnak. Interaktív funkció: A szeletekre kattintva további 
            részletek jelennek meg, segítve a piaci részesedés pontosabb megértését.''']),
        html.Li(
            [html.B('Forgalomban Lévő Kínálat és Piaci Kapitalizáció Szórásdiagram (Circulating Supply vs. Market Cap Scatter Plot)'), html.Br(), '''
            Ez a szórásdiagram a forgalomban lévő kínálatot és a piaci kapitalizációt hasonlítja össze. Az X tengely a 
            forgalomban lévő kínálatot, a Y tengely pedig a piaci kapitalizációt ábrázolja. A buborékok mérete az adott 
            érme piaci aktivitását, színe pedig kategóriáját jelzi. Interaktív funkció: Az egyes buborékokra való 
            rámutatás kiemeli az adott érme adatait, lehetővé téve a gyors összehasonlítást.''']),
        html.Li(
            [html.B('Piaci Dominancia Vízszintes Oszlopdiagram (Market Dominance Horizontal Bar Chart)'), html.Br(), '''
            Ez a diagram a vezető kriptovaluták piaci dominanciáját mutatja be százalékos formában. Az X tengely a 
            piaci dominanciát (%) ábrázolja, míg az Y tengelyen a kriptovaluták nevei szerepelnek. Interaktív funkció: 
            A sávokra történő rámutatás részletesen bemutatja az adott érme piaci részesedését és kategóriáját.'''])
    ]),
    html.Div([
        html.B('Interaktív Funkciók'),
        html.Ul([
            html.Li('''Rámutatás (hover): Részletes adatok jelennek meg a diagramokon az adott érme piaci 
                teljesítményéről. Nagyítás és pásztázás: A diagramok lehetőséget adnak a részletek kiemelésére és 
                elemzésére.'''),
            html.Li('''
            Az öt különböző interaktív diagram együttesen részletes és átfogó képet nyújt a kriptovaluták piacáról. 
            Ezek a vizualizációk nemcsak a kezdő, hanem a tapasztalt befektetők számára is hasznosak, hiszen könnyen 
            értelmezhető módon mutatják be a piaci tendenciákat, a kategóriák közötti különbségeket és a legfontosabb 
            pénzügyi mutatókat. A színkódolás és az interaktív funkciók tovább növelik a diagramok felhasználói élményét és 
            elemzési lehetőségeit.''')
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
