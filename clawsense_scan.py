import os
import time
import requests
import pandas as pd
import ta
from binance.client import Client
from datetime import datetime

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
if not api_key or not api_secret:
    raise Exception("Missing Binance API keys")

client = Client(api_key, api_secret)

# WSL time sync fix
server_time = client.get_server_time()['serverTime']
client.timestamp_offset = server_time - int(time.time() * 1000)

WEBHOOK_URL = "https://discord.com/api/webhooks/1481148679061766246/mPh-HMNiNWIwJvMyXFrRFkt7PMJS_N45-EBUBtYUlIVr5ljKD_W00QPwyLXs9YNrpqJ_"

WATCHLIST = ['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','PAXGUSDT','LINKUSDT','XRPUSDT','ZECUSDT']

def send_discord(msg):
    try:
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)
    except Exception as e:
        print(f"Discord error: {e}")

print("=== ClawSense Guard Mode ===")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M PKT')}\n")

alerts = []

for symbol in WATCHLIST:
    try:
        klines = client.get_klines(symbol=symbol, interval='15m', limit=100)

        df = pd.DataFrame(klines, columns=[
            'time','open','high','low','close','volume',
            'close_time','qav','trades','tbav','tqav','ignore'
        ])
        df['close']  = df['close'].astype(float)
        df['high']   = df['high'].astype(float)
        df['low']    = df['low'].astype(float)
        df['volume'] = df['volume'].astype(float)

        # RSI - Wilder's (matches Binance)
        rsi = ta.momentum.RSIIndicator(df['close'], window=14).rsi().iloc[-2]
        rsi = round(rsi, 2)

        # MACD
        macd_ind = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
        macd     = round(macd_ind.macd().iloc[-2], 4)
        signal   = round(macd_ind.macd_signal().iloc[-2], 4)
        hist     = round(macd_ind.macd_diff().iloc[-2], 4)

        # Price + Support
        price   = df['close'].iloc[-2]
        support = round(df['low'].iloc[-21:-1].min(), 4)

        # Volume spike - closed candles only
        vols    = df['volume'].iloc[-21:-1]
        avg_vol = vols.iloc[:-1].mean()
        cur_vol = vols.iloc[-1]
        vol_spike = round(cur_vol / avg_vol, 2) if avg_vol > 0 else 0

        # Rejection candle
        last    = df.iloc[-2]
        body    = abs(last['close'] - float(last['open']))
        wick    = last['high'] - last['low']
        rejection = wick > body * 2

        near_support = price <= support * 1.01

        # Verdict
        if rsi < 35 and near_support and vol_spike > 1.5:
            verdict = "VALID"
        elif rsi < 45 and near_support:
            verdict = "WATCH"
        elif rsi > 70:
            verdict = "DANGER"
        else:
            verdict = "NOT YET"

        print(f"{symbol}")
        print(f"  Price: {round(price,4)} | RSI: {rsi} | MACD: {macd}/{signal} | Hist: {hist}")
        print(f"  Support: {support} | Vol Spike: {vol_spike}x | Rejection: {rejection}")
        print(f"  Verdict: [{verdict}]")
        print()

        if verdict in ["VALID", "WATCH"]:
            alerts.append(f"🦞 {symbol} | Price: {round(price,4)} | RSI: {rsi} | [{verdict}]")

    except Exception as e:
        print(f"{symbol}: Error - {e}\n")

if alerts:
    msg = "**ClawSense Guard Alert**\n" + "\n".join(alerts)
    send_discord(msg)

print("=== Scan Complete ===")
