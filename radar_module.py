import requests
import json
import os
from datetime import datetime, timezone, timedelta

WEBHOOK_URL = "https://discord.com/api/webhooks/1481148679061766246/mPh-HMNiNWIwJvMyXFrRFkt7PMJS_N45-EBUBtYUlIVr5ljKD_W00QPwyLXs9YNrpqJ_"
CACHE_FILE = os.path.expanduser("~/radar_cache.json")
PKT = timezone(timedelta(hours=5))

# Fixed UTC times for DST (8:30 AM ET = 12:30 UTC | 2:00 PM ET = 18:00 UTC)
MACRO_EVENTS = [
    {
        "title": "CPI Data Release",
        "desc": "US inflation report. High inflation = Fed may raise rates = crypto can drop. Low inflation = good for crypto.",
        "datetime_utc": "2026-03-11 12:30",
        "impact": "HIGH"
    },
    {
        "title": "FOMC Interest Rate Decision",
        "desc": "US Federal Reserve announces interest rate. Rate cut = good for crypto. Rate hike = bad for crypto.",
        "datetime_utc": "2026-03-18 18:00",
        "impact": "HIGH"
    },
    {
        "title": "CPI Data Release",
        "desc": "US inflation report. High inflation = Fed may raise rates = crypto can drop. Low inflation = good for crypto.",
        "datetime_utc": "2026-04-10 12:30",
        "impact": "HIGH"
    },
    {
        "title": "FOMC Interest Rate Decision",
        "desc": "US Federal Reserve announces interest rate. Rate cut = good for crypto. Rate hike = bad for crypto.",
        "datetime_utc": "2026-05-07 18:00",
        "impact": "HIGH"
    },
]

MEDIUM_EVENTS = [
    {
        "title": "US Jobs Report (NFP)",
        "desc": "US employment data. Strong jobs = Fed keeps rates high = pressure on crypto.",
        "datetime_utc": "2026-04-03 12:30",
        "impact": "MEDIUM"
    },
    {
        "title": "US GDP Data",
        "desc": "US economic growth report. Weak GDP = possible rate cuts = good for crypto.",
        "datetime_utc": "2026-03-26 12:30",
        "impact": "MEDIUM"
    },
]

ALL_MACRO = MACRO_EVENTS + MEDIUM_EVENTS

def send_discord(msg):
    try:
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)
    except Exception as e:
        print(f"Discord error: {e}")

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=1", timeout=10)
        data = r.json()['data'][0]
        return data['value'], data['value_classification']
    except:
        return None, None

def get_binance_announcements():
    try:
        url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageNo=1&pageSize=5"
        r = requests.get(url, timeout=10)
        articles = r.json()['data']['articles']
        events = []
        for a in articles:
            title = a['title'].upper()
            if any(k in title for k in ['LISTING', 'DELIST', 'AIRDROP', 'LAUNCHPOOL', 'FUTURES']):
                events.append({
                    "title": a['title'],
                    "impact": "HIGH",
                    "source": "Binance"
                })
        return events
    except:
        return []

def get_crypto_news():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN&sortOrder=latest"
        r = requests.get(url, timeout=10)
        articles = r.json()['Data'][:10]
        events = []
        for a in articles:
            title = a['title'].upper()
            if any(k in title for k in ['FED', 'FOMC', 'REGULATION', 'SEC', 'ETF', 'HACK', 'CRASH', 'RALLY']):
                events.append({
                    "title": a['title'],
                    "impact": "HIGH",
                    "source": "CryptoCompare"
                })
        return events
    except:
        return []

def check_macro_events():
    now_utc = datetime.now(timezone.utc)
    alerts = []
    for e in ALL_MACRO:
        event_utc = datetime.strptime(e['datetime_utc'], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        event_pkt = event_utc.astimezone(PKT)
        diff_hours = (event_utc - now_utc).total_seconds() / 3600

        if diff_hours < 0:
            continue

        pkt_str = event_pkt.strftime('%d %b %Y, %I:%M %p PKT')
        impact_emoji = "🔴" if e['impact'] == "HIGH" else "🟡"

        if diff_hours <= 1:
            alerts.append(
                f"{impact_emoji} **{e['impact']} IMPACT — STARTING IN {round(diff_hours * 60)} MINUTES**\n"
                f"📌 Event: {e['title']}\n"
                f"🕐 Time: {pkt_str}\n"
                f"ℹ️ What it means: {e['desc']}\n"
                f"⚠️ Market can move sharply — avoid new entries now."
            )
        elif diff_hours <= 24:
            alerts.append(
                f"{impact_emoji} **{e['impact']} IMPACT — {round(diff_hours, 1)} HOURS LEFT**\n"
                f"📌 Event: {e['title']}\n"
                f"🕐 Time: {pkt_str}\n"
                f"ℹ️ What it means: {e['desc']}\n"
                f"📋 Plan your trades before this event."
            )
    return alerts

# === MAIN ===
print("=== ClawSense Radar Mode ===")
print(f"Time: {datetime.now(PKT).strftime('%Y-%m-%d %H:%M PKT')}\n")

cache = load_cache()
alerts = []

# Fear & Greed
fg_value, fg_label = get_fear_greed()
if fg_value:
    fg_int = int(fg_value)
    print(f"Fear & Greed Index: {fg_value} — {fg_label}")
    if fg_int <= 25:
        alerts.append(
            f"😱 **MARKET SENTIMENT: EXTREME FEAR**\n"
            f"Fear & Greed Index is at {fg_value} out of 100.\n"
            f"ℹ️ This means most traders are scared and selling. Historically this can be a good time to look for buy setups — but always wait for confirmation."
        )
    elif fg_int >= 75:
        alerts.append(
            f"🤑 **MARKET SENTIMENT: EXTREME GREED**\n"
            f"Fear & Greed Index is at {fg_value} out of 100.\n"
            f"ℹ️ Most traders are buying aggressively. Market may be overheated — be careful with new entries, a correction can happen soon."
        )

# Binance Announcements
binance_events = get_binance_announcements()
for e in binance_events:
    key = "binance_" + e['title'][:40]
    if key not in cache:
        cache[key] = True
        alerts.append(
            f"📢 **BINANCE ANNOUNCEMENT**\n"
            f"📌 {e['title']}\n"
            f"ℹ️ New listings or launchpools can cause price pumps. Check if any coin in your watchlist is affected."
        )
        print(f"Binance: {e['title']}")

# Crypto News
news_events = get_crypto_news()
for e in news_events:
    key = "news_" + e['title'][:40]
    if key not in cache:
        cache[key] = True
        alerts.append(
            f"📰 **MARKET NEWS**\n"
            f"📌 {e['title']}\n"
            f"ℹ️ This news can affect crypto prices. Stay alert and do not make impulsive trades."
        )
        print(f"News: {e['title']}")

# Macro Events
macro_alerts = check_macro_events()
for a in macro_alerts:
    alerts.append(a)

save_cache(cache)

if alerts:
    for alert in alerts:
        msg = f"**🦞 ClawSense Radar**\n{alert}"
        send_discord(msg)
        print(f"Sent: {alert[:60]}...")
    print(f"\nTotal alerts sent: {len(alerts)}")
else:
    print("No new events found.")

print("\n=== Radar Scan Complete ===")
