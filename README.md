# 🦞 ClawSense
**AI Crypto Intelligence System built with Binance OpenClaw**

> "It senses danger and reflects your habits"

Built for the Binance OpenClaw AI Hackathon 2026.

---

## What is ClawSense?

ClawSense is a 3-module AI trading assistant that monitors the crypto market, analyzes your trading behavior, and sends real-time alerts to Discord — powered by Binance OpenClaw and Google Gemini.

---

## Modules

### 🛡️ Guard Mode — runs every 15 minutes
- Scans 8 coins: BTC, ETH, BNB, SOL, PAXG, LINK, XRP, ZEC
- Checks RSI (Wilder's), MACD, Support/Resistance, Volume Spike, Rejection Candles
- Verdict: VALID / WATCH / DANGER / NOT YET
- Sends instant Discord alert

### 🪞 Mirror Mode — runs daily at 6:00 AM PKT
- Fetches last 3 days of spot and convert trade history
- FIFO matching for accurate PnL calculation
- Detects bad habits: No Stop Loss, Revenge Trading, Oversized Positions
- Sends personalized coaching report to Discord

### 📡 Radar Mode — runs every 30 minutes
- Tracks HIGH and MEDIUM impact macro events: FOMC, CPI, NFP, GDP
- Monitors Binance announcements: listings, delistings, launchpools
- Scans crypto news: ETF, regulation, SEC, market crashes
- Fear and Greed Index alerts
- All times shown in PKT (Pakistan Standard Time)
- 24-hour warning and 1-hour reminder for each event

---

## Tech Stack

- **Platform:** Binance OpenClaw
- **AI Model:** Google Gemini 3 Flash Preview
- **Language:** Python 3
- **Libraries:** python-binance, pandas, ta, requests
- **Alerts:** Discord Webhooks
- **Scheduling:** Cron Jobs on WSL2 Ubuntu

---

## Setup

### 1. Install dependencies
```bash
pip install python-binance pandas ta requests
2. Set API keys in ~/.bashrc
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"
3. Add your Discord webhook URL
Open each script and replace WEBHOOK_URL with your own Discord webhook.
4. Add cron jobs
crontab -e
0 6 * * * /usr/bin/python3 /home/user/clawsense_mirror.py
*/15 * * * * /usr/bin/python3 /home/user/clawsense_scan.py
*/30 * * * * /usr/bin/python3 /home/user/radar_module.py
5. Start cron service
sudo service cron start
Customization
ClawSense is built so any trader can adapt it to their own strategy.
Change your watchlist
Open clawsense_scan.py and edit this line:
WATCHLIST = ['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','PAXGUSDT','LINKUSDT','XRPUSDT','ZECUSDT']
Add or remove any Binance spot trading pair you want.
Change RSI thresholds
Find the verdict logic in clawsense_scan.py:
if rsi < 35 and near_support and vol_spike > 1.5:
    verdict = "VALID"
elif rsi < 45 and near_support:
    verdict = "WATCH"
elif rsi > 70:
    verdict = "DANGER"
Lower the RSI values if you want more conservative entries
Raise them if you want more aggressive signals
Change timeframe
Find this line in clawsense_scan.py:
klines = client.get_klines(symbol=symbol, interval='15m', limit=100)
Change 15m to 1h or 4h depending on your trading style.
Add macro events
Open radar_module.py and add your own dates to MACRO_EVENTS or MEDIUM_EVENTS:
{
    "title": "Your Event Name",
    "desc": "What this means for crypto.",
    "datetime_utc": "2026-06-01 13:30",
    "impact": "HIGH"
}
Current Limitations
Requires PC to be on (WSL2 environment)
No 24/7 hosting yet
Single user only
Future Plans
Version 2 — Smarter Analysis
Multiple timeframe confirmation — 15m and 1h must agree before VALID signal
EMA 25/99 added to Guard Mode to match Binance chart indicators
Per-coin verdict logic — each coin has different character and behavior
Mirror Mode extended to 7 days for better pattern detection
Backtesting module — test strategy on historical data
Version 3 — More Reach
Telegram alerts alongside Discord
Web dashboard — view all signals and trade history in browser
More news sources — Binance RSS and crypto sentiment analysis
Multi-user support
Version 4 — Full Automation
Oracle Cloud free tier deployment — 24/7 without PC
Auto trade execution — place orders when VALID signal fires
Portfolio tracker — total PnL, win rate, drawdown dashboard
Mobile app integration
Author
Sibghat Ullah (Sibnix) — Binance Spot Trader and Creator
Binance Square: @Sibnix
GitHub: Sibghat-Ullah016
Built with love for Binance OpenClaw Hackathon 2026
#AIBinance #OpenClaw #BinanceSquare
