# Binance Futures Testnet Trading Bot

A clean, structured Python CLI application that places **MARKET**, **LIMIT**, and **STOP_LIMIT** orders on the [Binance Futures Testnet (USDT-M)](https://testnet.binancefuture.com).

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST API wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Rotating file + console logger
├── logs/
│   └── trading_bot.log    # Auto-created on first run
├── cli.py                 # CLI entry point (argparse)
├── .env.example           # Credential template
├── requirements.txt
└── README.md
```

---

## Setup Steps

### 1. Get Testnet Credentials

1. Go to <https://testnet.binancefuture.com>
2. Register / log in
3. Navigate to **API Management** and generate an API Key + Secret

### 2. Clone / Download the project

```bash
git clone <your-repo-url>
cd trading_bot
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

```bash
cp .env.example .env
# Edit .env and paste your API key and secret
```

---

## How to Run

### MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000
```

### STOP_LIMIT order (Bonus)

```bash
python cli.py --symbol ETHUSDT --side BUY --type STOP_LIMIT --quantity 0.01 --price 3100 --stop-price 3050
```

### Pass credentials directly (without .env)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 \
  --api-key YOUR_KEY --api-secret YOUR_SECRET
```

---

## CLI Arguments

| Argument | Required | Description |
|---|---|---|
| `--symbol` | ✅ | Trading pair, e.g. `BTCUSDT` |
| `--side` | ✅ | `BUY` or `SELL` |
| `--type` | ✅ | `MARKET`, `LIMIT`, or `STOP_LIMIT` |
| `--quantity` | ✅ | Order quantity, e.g. `0.001` |
| `--price` | LIMIT / STOP_LIMIT | Limit price |
| `--stop-price` | STOP_LIMIT | Stop trigger price |
| `--api-key` | Optional | Overrides env var |
| `--api-secret` | Optional | Overrides env var |

---

## Logging

All API requests, responses, and errors are written to `logs/trading_bot.log`.  
The file rotates at 5 MB and keeps 3 backups.  
Console output shows INFO and above; the file captures DEBUG level.

---

## Assumptions

- Only **USDT-M** perpetual futures on the testnet are targeted.
- Minimum quantity and price filter compliance depends on the symbol — if the testnet rejects an order, adjust the quantity/price to meet the exchange's lot size filters.
- `STOP_LIMIT` is sent as Binance order type `STOP` (stop-limit), which requires both `price` and `stopPrice`.
- Credentials are loaded from `.env` via `python-dotenv`; they can also be passed via CLI flags.

---

## Evaluation Checklist

- [x] Places MARKET and LIMIT orders on Binance Futures Testnet (USDT-M)
- [x] Supports BUY and SELL sides
- [x] CLI input with validation (argparse)
- [x] Clear output: request summary + response details
- [x] Structured code: separate client / orders / validators / CLI layers
- [x] Rotating log file for requests, responses, errors
- [x] Exception handling: validation errors, API errors, network failures
- [x] Bonus: STOP_LIMIT order type
