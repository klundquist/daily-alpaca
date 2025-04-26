#!/usr/bin/env python3
# ---------- daily_stop.py  ------------------------------------
from datetime import datetime, timedelta, timezone
from alpaca_trade_api.rest import REST, TimeFrame
import os

# -- credentials (export these in your shell or .bash_profile) --
#API_KEY    = os.environ["ALPACA_KEY"]
#API_SECRET = os.environ["ALPACA_SECRET"]
API_KEY = 'PKUFN8ISSUV0H03YZOW8'
API_SECRET = 'pWW27pR7LaXZ4L8zxOVq3DY3ngubnyDFbbCf2gov'
BASE_URL   = "https://paper-api.alpaca.markets"      # change if using live

api = REST(API_KEY, API_SECRET, BASE_URL)

SYMBOL = "SPXL"

# 1 ▸ get last 3 trading-day closes
start = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
bars  = api.get_bars(SYMBOL, TimeFrame.Day, start=start).df.tail(3)
avg_3d = bars["close"].mean()
print("3-day average close:", round(avg_3d, 4))

# 2 ▸ cancel any open stop orders we left from yesterday
open_orders = api.list_orders(status="open", symbols=[SYMBOL])
# … 3-day average logic unchanged …

# 2 ▸ hard-cancel any open SPXL orders
for o in api.list_orders(status="open"):
    if o.symbol == SYMBOL:
        api.cancel_order(o.id)

import time
while any(o.symbol == SYMBOL for o in api.list_orders(status="open")):
    time.sleep(0.5)          # wait until cancellations settle

# 3 ▸ refresh position & buying-power
try:
    qty_owned = float(api.get_position(SYMBOL).qty)
except Exception:
    qty_owned = 0.0
buy_pow = float(api.get_account().buying_power)

# 4 ▸ place the new stop
if qty_owned > 0:
    api.submit_order(
        symbol=SYMBOL,
        qty=qty_owned,
        side="sell",
        type="stop",
        stop_price=round(avg_3d, 2),
        time_in_force="day"
    )
else:
    api.submit_order(
        symbol=SYMBOL,
        notional=round(buy_pow, 2),
        side="buy",
        type="stop",
        stop_price=round(avg_3d, 2),
        time_in_force="day"
    )
