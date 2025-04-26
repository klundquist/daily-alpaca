# SPXL Daily Stop‑Order Bot

A lightweight, server‑less workflow that refreshes a **24‑hour stop order** for SPXL once per day.  It calculates the three‑day simple moving‑average (3‑DMA) of the daily **close**, then:

* **If you hold SPXL** → submits a `STOP‑SELL` for your full position at the 3‑DMA.
* **If you hold zero shares** → submits a `STOP‑BUY` using *all* available buying power at the 3‑DMA.

The job runs in a GitHub Actions runner—no VPS, EC2, or always‑on machine required.

---

## 📂 Repository Structure

```text
.
├─ daily_stop.py            # core script
├─ requirements.txt         # Python deps (alpaca‑trade‑api)
└─ .github
   └─ workflows
      └─ daily.yml          # GitHub Actions schedule (00:00 São Paulo)
```

---

## 🛠 Prerequisites

| Item | Notes |
|------|-------|
| **Alpaca account** | Paper or live; script defaults to paper URL. |
| **API keys**       | Generate in Alpaca dashboard → *Paper keys*. |
| **GitHub repo**    | Private recommended (store secrets safely). |

---

## 🚀 Setup

1. **Fork / clone** this repo or create a new private repo and add the files.
2. **Add repo secrets** (<kbd>Settings → Secrets → Actions</kbd>):
   * `ALPACA_KEY`
   * `ALPACA_SECRET`
3. *(Optional)* Edit `daily.yml` if you prefer a different run time.
4. Commit & push.  GitHub Actions will trigger nightly and you can also run it manually from the **Actions** tab.

---

## 🗓 How It Works

1. **Pull last 3 trading‑day closes** via Alpaca `/v2/stocks/{symbol}/bars`.
2. Compute the **3‑DMA**.
3. Cancel any open orders for SPXL so shares aren’t reserved twice.
4. Query current position & buying power.
5. Submit one **stop order** (`time_in_force: day`).  It expires automatically at the next market close.

> **Fractional shares** `notional=` is used on the buy side so every cent of buying‑power is deployed—even fractions.

---

## 🔄 Local Test Run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export ALPACA_KEY="PK…"
export ALPACA_SECRET="pW…"
python daily_stop.py   # prints average and order details
```

---

## 📝 Customisation

| Want to… | Where to change |
|----------|-----------------|
| Use **live trading** | `BASE_URL` in `daily_stop.py` → `https://api.alpaca.markets` |
| Different **symbol** | `SYMBOL` constant in `daily_stop.py` |
| Different **look‑back** | Change `tail(3)` to e.g. `tail(5)` and adjust doc strings |
| Adjust **stop buffer** | e.g. `stop_price = avg_3d * 0.99` |
| Run at another **time zone** | Edit `cron:` field in `.github/workflows/daily.yml` |

---

## 📄 License

MIT License — see `LICENSE` file.

---

## 🙋 Support / Questions

Open an issue in the repo or ping me in Discussions. PRs welcome!

