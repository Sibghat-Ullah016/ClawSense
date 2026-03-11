import os
import time
import requests
from binance.client import Client
from datetime import datetime, timedelta

# Configuration
WEBHOOK_URL = "https://discord.com/api/webhooks/1481148679061766246/mPh-HMNiNWIwJvMyXFrRFkt7PMJS_N45-EBUBtYUlIVr5ljKD_W00QPwyLXs9YNrpqJ_"
client = Client(os.environ['BINANCE_API_KEY'], os.environ['BINANCE_API_SECRET'])

# Auto-Detect Range: Monday = 7 Days, Others = 3 Days
today_name = datetime.now().strftime('%A')
REPORT_DAYS = 7 if today_name == "Monday" else 3
start_ts = int((datetime.now() - timedelta(days=REPORT_DAYS)).timestamp() * 1000)

def send_discord(msg):
    try:
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)
    except Exception as e:
        print(f"Discord error: {e}")

print(f'=== ClawSense Mirror: {today_name} Mode ({REPORT_DAYS} Days) ===\n')

symbols = ['PAXGUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'BTCUSDT',
           'ZECUSDT', 'TRXUSDT', 'RENDERUSDT', 'XPLUSDT', 'DUSKUSDT', 'HOMEUSDT']

all_trades = []

# 1. Spot Trades
for symbol in symbols:
    try:
        trades = client.get_my_trades(symbol=symbol, startTime=start_ts)
        for t in trades:
            all_trades.append({
                'symbol': symbol, 'time': t['time'],
                'side': 'BUY' if t['isBuyer'] else 'SELL',
                'price': float(t['price']), 'qty': float(t['qty']),
                'total': float(t['quoteQty']), 'type': 'SPOT'
            })
    except: pass

# 2. Spot Converts
try:
    result = client._request_margin_api(
        'get', 'convert/tradeFlow', True,
        data={'startTime': start_ts, 'endTime': int(time.time() * 1000), 'limit': 100}
    )
    if result and 'list' in result:
        for t in result['list']:
            if (t['orderStatus'] == 'SUCCESS' and t['toAsset'] == 'USDT'):
                all_trades.append({
                    'symbol': t['fromAsset'] + 'USDT', 'time': t['createTime'],
                    'side': 'SELL', 'price': float(t['toAmount']) / float(t['fromAmount']),
                    'qty': float(t['fromAmount']), 'total': float(t['toAmount']), 'type': 'CONVERT'
                })
except Exception as e: print(f'Convert error: {e}')

seen = set()
unique = [t for t in all_trades if not (key := (t['symbol'], t['time'], t['side'])) in seen and not seen.add(key)]
all_trades = sorted(unique, key=lambda x: x['time'])

completed = []
for symbol in set(t['symbol'] for t in all_trades):
    sym_trades = sorted([t for t in all_trades if t['symbol'] == symbol], key=lambda x: x['time'])
    buys = []
    for t in sym_trades:
        if t['side'] == 'BUY': buys.append(t)
        elif t['side'] == 'SELL' and buys:
            buy = buys.pop(0)
            pnl_usdt = (t['price'] - buy['price']) * min(buy['qty'], t['qty'])
            completed.append({
                'symbol': symbol, 'pnl_pct': round(((t['price'] - buy['price']) / buy['price']) * 100, 2),
                'pnl_usdt': round(pnl_usdt, 2), 'hold_min': (t['time'] - buy['time']) / 60000,
                'type': t['type'], 'sell_time': t['time']
            })

completed.sort(key=lambda x: x['sell_time'])
total_pnl = sum(t['pnl_usdt'] for t in completed)
wins = len([t for t in completed if t['pnl_usdt'] > 0])
winrate = round(wins/len(completed)*100, 1) if completed else 0

# Report Formatting
report_type = "WEEKLY" if REPORT_DAYS == 7 else "ROUTINE"
report = f"🪞 **ClawSense Mirror: {report_type} REPORT**\n"
report += f"📅 Range: {REPORT_DAYS} Days ({today_name})\n\n"

if completed:
    for t in completed:
        emoji = "✅" if t['pnl_usdt'] > 0 else "❌"
        report += f"{emoji} **{t['symbol']}**: {t['pnl_pct']}% (${t['pnl_usdt']})\n"
    
    report += f"\n📊 **Stats**\nTrades: {len(completed)} | WinRate: {winrate}%\n💰 **Net PnL: ${total_pnl:.2f}**"
else:
    report += "No closed trades detected in this window."

print(report)
send_discord(report)
