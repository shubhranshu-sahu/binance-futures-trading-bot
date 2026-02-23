# Binance Futures Trading Bot (CLI)

A Python CLI trading bot for Binance Futures Testnet (USDT-M) built using direct REST API integration with HMAC-SHA256 request signing.
This project demonstrates structured architecture, secure API communication, validation, logging discipline, retry logic, and enhanced CLI UX.

---

# 🚀 Features Implemented

## ✅ Core Requirements (Must-Have)

* Python 3.x
* Place **MARKET** and **LIMIT** orders
* Support both **BUY** and **SELL** sides
* CLI-based user input (Typer)
* Input validation (symbol, side, type, quantity, price)
* Clean order request summary output
* Clean order response output (orderId, status, executedQty, avgPrice)
* Success / failure messaging
* Structured code separation:

  * Client/API layer
  * Order service layer
  * Validation layer
  * CLI layer
* Logging of API requests, responses, and errors
* Exception handling:

  * Invalid input
  * API errors (4xx)
  * Network failures

---

# 🏗 Project Architecture

```
binance-futures-trading-bot/
│
├── bot/
│   ├── client.py            # REST API client (signing, retry, timeout)
│   ├── orders.py            # Order logic layer
│   ├── validators.py        # Input validation logic
│   └── logging_config.py    # Logging configuration (rotating logs)
│    
│
├── logs/
│   └── trading.log          # Generated log file (rotating)
│
├── cli.py                   # CLI entry point (Typer-based)
├── requirements.txt
├── .env
├── .env.example
└── README.md
```

The system follows clean separation of concerns:

* CLI Layer → User interaction
* Order Layer → Business logic
* Client Layer → Infrastructure (HTTP + Signing)
* Logging Layer → Observability

---

# 🔐 API Integration Details

* Base URL: `https://demo-fapi.binance.com`
* REST-based integration (no SDK used)
* HMAC-SHA256 request signing
* Timestamp-based authentication
* API key passed via `X-MBX-APIKEY` header

Private endpoints are securely signed before transmission.

---

# 🔁 Retry & Timeout Strategy

The client layer includes:

* Timeout protection (`timeout=10` seconds)
* Retry mechanism (max 3 attempts)
* Exponential backoff strategy
* Retries only for:

  * Network failures
  * 5xx server errors
* No retry for 4xx client errors (invalid symbol, precision errors, etc.)

This ensures reliability without masking client-side mistakes.

---

# 📜 Logging Strategy (Useful, Not Noisy)

Logging is designed to be production-friendly.

## Features:

* Rotating log files (5MB max, 3 backups)
* UTF-8 encoding
* Structured format including:

  * Timestamp
  * Log level
  * Module
  * Line number
* INFO level → High-level request flow
* DEBUG level → Detailed payloads (response bodies)
* Sensitive fields (signature) masked in logs

### Log Level Control

Set via environment variable:

```
LOG_LEVEL=INFO
```

or

```
LOG_LEVEL=DEBUG
```

No code change required to switch verbosity.

---

# 🖥 CLI Commands

## 1️⃣ Place Order (Command Mode)

### MARKET Order

```
python cli.py place --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

### LIMIT Order

```
python cli.py place --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 45000
```

---

## 2️⃣ Account Summary

```
python cli.py account
```

Displays:

* Total Wallet Balance
* Unrealized PnL

---

## 3️⃣ Interactive Mode (Enhanced UX)

```
python cli.py interactive
```

Features:

* Structured menu system
* Guided prompts
* Validation feedback
* Order confirmation before execution
* Clean formatted output

---

# 🛠 Setup Instructions

## 1️⃣ Clone Repository

```
git clone <your-repo-url>
cd binance-futures-trading-bot
```

## 2️⃣ Create Virtual Environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```
python -m venv venv
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

## 4️⃣ Configure Environment Variables

Rename `.env.example` to `.env` and fill in:

```
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
BASE_URL=https://demo-fapi.binance.com
LOG_LEVEL=INFO
```

---

# 🧪 Example Workflow

### Place Market Order

```
python cli.py place --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

Output:

* Order Request Summary
* Order Response Details
* Success Message

---

# ⚠ Assumptions

* Binance Futures Demo environment is active
* API key is generated from demo environment
* User has demo USDT balance
* Quantity respects symbol precision rules
* Internet connectivity available

---

# 🎯 Design Decisions

* Direct REST instead of SDK to demonstrate understanding of:

  * HMAC signing
  * Secure API authentication
  * Full request lifecycle control
* Clean separation of layers
* Production-style logging
* Controlled retry strategy
* CLI UX enhancements for usability

---

# 📌 Conclusion

This project fulfills all core requirements and includes professional enhancements such as structured logging, retry logic, timeout handling, environment-driven configuration, and interactive CLI support.

It is designed to reflect backend engineering best practices rather than a minimal script-based submission.

---
