import yfinance as yf
import streamlit as st
import pandas as pd
import pandas_ta as ta
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import bs4 as bs

resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})
symbols = []
for row in table.findAll('tr')[1:]:
    symbol = row.findAll('td')[0].text
    symbols.append(symbol)

st.write("""
# Stock Price App for S&P 500
""")

symbols = [s.replace('\n', '') for s in symbols]

ticker = st.sidebar.selectbox(
    'Choose a S&P 500 Stock',
     symbols)  


#define the ticker symbol
tickerSymbol = ticker

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get the historical prices for this ticker
numYear = st.number_input('Insert period (Year): ', min_value=1, max_value=20, value=10, key=0)

tickerDf = tickerData.history(period='1d', start=dt.datetime.today()-dt.timedelta(numYear * 365), end=dt.datetime.today())
# Open	High	Low	Close	Volume	Dividends	Stock Splits

indicator = st.sidebar.radio(
        "Choose an indicator",
        ('MACD', 'RSI')
    ) 

st.write("""
## Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume
""")
st.line_chart(tickerDf.Volume)

if(indicator == 'RSI'):
    rsi_len = st.number_input('RSI Length (Day): ', min_value=5, max_value=30, value=14, key=0)  
    tickerDf.ta.rsi(length = rsi_len, append=True)
    st.write("""
    ## RSI
    """)
    st.line_chart(tickerDf['RSI_' + str(rsi_len)])
elif(indicator == 'MACD'):
    tickerDf.ta.macd(append=True)
    st.subheader('Moving Average Convergence Divergence (MACD)')
    
    figMACD = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.01)

    figMACD.add_trace(
            go.Scatter(
                    x = tickerDf.index,
                    y = tickerDf.Close,
                    name = "Price"
                ),
            row=1, col=1
        )

    figMACD.add_trace(
            go.Scatter(
                    x = tickerDf.index,
                    y = tickerDf['MACD_12_26_9'],
                ),
            row=2, col=1
        )

    figMACD.add_trace(
            go.Scatter(
                    x = tickerDf.index,
                    y = tickerDf['MACDs_12_26_9'],
                ),
            row=2, col=1
        )        
    figMACD.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=0
    ))

    figMACD.update_yaxes(tickprefix="$")
    st.plotly_chart(figMACD, use_container_width=True)
