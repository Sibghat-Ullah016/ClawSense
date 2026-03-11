# 🦞 ClawSense
**AI Crypto Intelligence System built with Binance OpenClaw**

> "It senses danger and reflects your habits"

Built for the Binance OpenClaw AI Hackathon 2026.

---

## What is ClawSense?

ClawSense is a 3-module AI trading assistant that runs 24/7, monitors the crypto market, analyzes your trading behavior, and sends real-time alerts to Discord — all powered by Binance OpenClaw.

---

## Modules

### 🛡️ Guard Mode
- Scans 8 coins every 15 minutes: BTC, ETH, BNB, SOL, PAXG, LINK, XRP, ZEC
- Checks RSI, MACD, Support/Resistance, Volume Spike, Rejection Candles
- Sends Discord alert with verdict: VALID / WATCH / DANGER / NOT YET

### 🪞 Mirror Mode
- Runs daily at 6:00 AM PKT
- Fetches last 3 days of your spot trading history
- Detects bad habits: No Stop Loss, Revenge Trading, Oversized Positions
- Sends personalized coaching to Discord

### 📡 Radar Mode
- Scans every 30 minutes
- Sources: Binance Announcements, CryptoCompare News, Fear & Greed Index
- Tracks HIGH and MEDIUM impact macro events: FOMC, CPI, NFP, GDP
- All times shown in PKT (Pakistan Standard Time)
- Sends early warnings: 24 hours before and 1 hour before each event

---

## Tech Stack

- **Platform:** Binance OpenClaw
- **Language:** Python 3
- **Libraries:** python-binance, pandas, ta, requests
- **Alerts:** Discord Webhooks
- **Scheduling:** Cron Jobs
- **OS:** Ubuntu (WSL2)

---

## Setup

### 1. Install dependencies
```bash
pip install python-binance pandas ta requests
2. Set API keys in ~/.bashrc
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"
3. Add cron jobs
crontab -e
0 6 * * * /usr/bin/python3 /home/user/clawsense_mirror.py
*/15 * * * * /usr/bin/python3 /home/user/clawsense_scan.py
*/30 * * * * /usr/bin/python3 /home/user/radar_module.py
4. Start cron service
sudo service cron start
Current Limitations
Requires PC to be on (WSL2 environment)
No 24/7 hosting yet
Future Plans
☁️ Oracle Cloud Free Tier — permanent 24/7 hosting
📱 Termux — run on Android phone
🚀 Railway.app / Render — cloud deployment
📊 Web dashboard for trade analytics
🤖 Auto trade execution (Phase 2)
Author
Sibghat Ullah (Sibnix) — Binance Spot Trader & Creator
Binance Square: @Sibnix
Built with ❤️ for Binance OpenClaw Hackathon 2026 #AIBinance
