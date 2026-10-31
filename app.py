import streamlit as st
import pandas as pd
import time
from binance.client import Client

st.set_page_config(page_title="Binance Bot", page_icon="💰")
st.title("💰 Binance Auto Trading Bot")
st.write("Yasir ka Bot - Live Running")

# Sidebar - API Keys
st.sidebar.header("API Settings")
api_key = st.sidebar.text_input("Binance API Key", type="password")
api_secret = st.sidebar.text_input("Binance API Secret", type="password")
symbol = st.sidebar.selectbox("Coin", ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"])

if api_key and api_secret:
    try:
        client = Client(api_key, api_secret)
        balance = client.get_asset_balance(asset='USDT')
        st.success(f"Connected! USDT Balance: {balance['free']}")
        
        # Live Price
        ticker = client.get_symbol_ticker(symbol=symbol)
        st.metric(label=f"{symbol} Price", value=ticker['price'])
        
        # Simple Strategy
        st.subheader("Trading Status")
        if st.button("Check Signal"):
            klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=20)
            df = pd.DataFrame(klines, columns=['time','o','h','l','c','v','ct','qav','not','tbav','tqav','i'])
            df['c'] = pd.to_numeric(df['c'])
            sma = df['c'].mean()
            last_price = float(ticker['price'])
            if last_price > sma:
                st.info(f"Signal: SELL - Price {last_price} > SMA {sma:.2f}")
            else:
                st.info(f"Signal: BUY - Price {last_price} < SMA {sma:.2f}")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Pehle Sidebar me Binance API Key aur Secret dalo")
    st.info("Bot abhi Test Mode me hai. API lagate hi Live ho jayega.")
