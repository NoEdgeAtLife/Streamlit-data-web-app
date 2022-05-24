import yfinance as yf
import streamlit as st
import pandas as pd
import pandas_ta as ta
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from binance import Client
import numpy as np
import time

st.write("""
# UP or DOWN!? BTC 亞洲盤
""")

symbols = ['BTCUSDT']

ticker = st.sidebar.selectbox(
    'Choose a coin',
     symbols)  

api_key = ""
api_secret = ""

client = Client(api_key, api_secret)

low = 0
high = 0
price = 0


placeholder1 = st.empty()

while True:
    time.sleep(1)
    price = float(client.futures_symbol_ticker(symbol=ticker)['price'])
    klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    high = np.max(np.array(klines)[:,2].astype("float"))
    low = np.min(np.array(klines)[:,3].astype("float"))
    low_odd = round((1-low/price)/(high/price-1) + 1 ,2)
    high_odd = round((high/price-1)/(1-low/price) + 1,2)
    with placeholder1.container():
        price1 = st.container()
        price1.header('Current Price:')
        low1,high1 = st.columns((2,1))
        low1.subheader('Bet to 24H Low!')
        high1.subheader('Bet to 24H High!')
        with price1:
            st.write(f'<p style="color:#fff;font-size:36px;border-radius:2%;">'+str(price)+'</p>', unsafe_allow_html=True)
        with low1:
            st.write(f'<p style="color:#de0d0d;font-size:24px;border-radius:2%;">'+str(low)+'</p>', unsafe_allow_html=True)
            st.write(f'<p style="color:#de0d0d;font-size:36px;border-radius:2%;"> 1賠'+str(low_odd)+'</p>', unsafe_allow_html=True)
        with high1: 
            st.write(f'<p style="color:#1de612;font-size:24px;border-radius:2%;">'+str(high)+'</p>', unsafe_allow_html=True)
            st.write(f'<p style="color:#1de612;font-size:36px;border-radius:2%;"> 1賠'+str(high_odd)+'</p>', unsafe_allow_html=True)