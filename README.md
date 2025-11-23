# Market Signals — Zerodha Integration 📈

Real-time **STRONG BUY signals** for NIFTY, BANKNIFTY, and SENSEX options using live Zerodha data. Built with **FastAPI backend** and **Next.js frontend**.

## 🎯 Features

- ✅ **Real-time Zerodha API Integration** - Live option chain data
- ✅ **STRONG BUY Signals Only** - Shows signals when ALL criteria match
- ✅ **Greeks Analysis** - Delta, Gamma, Theta, Vega calculations
- ✅ **High Liquidity Focus** - OI ≥ 50K requirement
- ✅ **Both CE & PE Analysis** - Analyzes Call and Put options
- ✅ **10-Second Updates** - Continuous market scanning
- ✅ **ATM + ITM Strikes** - Optimal strike selection

## 🚀 Project Structure

```
market-signals-zerodha/
├── frontend/                 # Next.js app (port 3000)
│   ├── pages/
│   │   ├── _app.js          # App wrapper
│   │   └── index.js         # Main dashboard
│   ├── components/
│   │   └── SignalCard.js    # Signal display
│   ├── styles/
│   │   └── globals.css      # Global styles
│   └── package.json
│
├── backend/                  # FastAPI server (port 8000)
│   ├── main.py              # REST API endpoints
│   ├── zerodha_api.py       # Signal generation & Greeks
│   ├── config.py            # Configuration & thresholds
│   └── requirements.txt     # Python dependencies
│
├── docs/                     # Documentation
│   ├── DEPLOYMENT.md        # Full deployment guide
│   ├── QUICK_DEPLOY.md      # Quick start guide
│   └── INDIA_HOSTING.md     # India hosting options
│
├── docker/                   # Docker configuration
│   ├── docker-compose.yml   # Multi-container setup
│   └── Dockerfile.*         # Container definitions
│
├── scripts/                  # Deployment scripts
│   ├── deploy.bat           # Windows deployment
│   └── deploy.sh            # Linux/Mac deployment
│
└── .github/
    └── copilot-instructions.md  # AI agent guidelines
```

## ⚡ Quick Start

### 1️⃣ Backend Setup

```powershell
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

**Backend:** `http://localhost:8000`  
**API Docs:** `http://localhost:8000/docs`

### 2️⃣ Frontend Setup (new terminal)

```powershell
cd frontend
npm install
npm run dev
```

**Frontend:** `http://localhost:3000`

---

## 🎯 How It Works

### STRONG BUY Signal Logic

Signal is generated **only when ALL criteria match**:

**Greeks Thresholds:**
- ✅ Vega ≥ 0.3 (volatility sensitivity)
- ✅ Gamma ≥ 0.05 (delta sensitivity)
- ✅ Theta ≤ -0.5 (time decay)
- ✅ Delta ≥ 0.4 (directional movement)

**Liquidity Thresholds:**
- ✅ Open Interest ≥ 50,000
- ✅ Implied Volatility ≥ 20%
- ✅ Confidence Score ≥ 80%

**Result:** Only high-probability opportunities are shown!

### Strike Selection

- ATM (At The Money) strike
- ITM (In The Money) strike
- Analyzes both CE (Call) and PE (Put) options
- Returns single best signal or "No Signal"

---

## 🔌 API Endpoints

### Get Signal (STRONG BUY only)
```bash
GET http://localhost:8000/api/signal?symbol=NIFTY
```

**Response (when criteria match):**
```json
{
  "symbol": "NIFTY",
  "timestamp": "14:30:45",
  "option_type": "CE",
  "strike": 19850,
  "vega": 0.52,
  "gamma": 0.15,
  "theta": -0.42,
  "delta": 0.58,
  "oi": 125000,
  "iv": 0.28,
  "ltp_option": 245.50,
  "ltp": 19832.40,
  "side": "STRONG BUY CE",
  "confidence": 0.85,
  "data_source": "ZERODHA_LIVE"
}
```

**Response (when no signal):** `null`

### Other Endpoints
- `GET /health` - Health check
- `GET /api/symbols` - Available symbols
- `GET /api/connection` - Zerodha connection status
- `GET /auth/login` - Get Zerodha login URL

---

## 🔐 Zerodha Authentication

### Start in Demo Mode (Testing)
The app runs with simulated data by default - no authentication needed.

### Enable Live Data (Production)

1. **Get Login URL:**
   ```bash
   # Visit in browser
   http://localhost:8000/auth/login
   ```

2. **Authenticate with Zerodha**
   - Complete login flow
   - Copy `request_token` from callback URL

3. **Set Access Token:**
   ```bash
   POST http://localhost:8000/auth/callback?request_token=YOUR_TOKEN
   ```

4. **Backend switches to live data automatically** ✅

---

## 🚀 Deployment

### Quick Deploy to Render.com (Recommended)

See **[RENDER_DEPLOY.md](docs/RENDER_DEPLOY.md)** for step-by-step guide.

**Quick Start:**
1. Push code to GitHub
2. Connect to Render.com
3. Deploy backend + frontend
4. Live in 10 minutes!

### Other Options

- **[RENDER_CHECKLIST.md](docs/RENDER_CHECKLIST.md)** - Deployment checklist
- **[QUICK_DEPLOY.md](docs/QUICK_DEPLOY.md)** - Other platforms
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - All platform options
- **[INDIA_HOSTING.md](docs/INDIA_HOSTING.md)** - India-specific hosting

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | Next.js 14 + React 18 | Dashboard UI |
| Backend | FastAPI + Uvicorn | REST API |
| Data Source | Zerodha Kite API | Live market data |
| Greeks | Black-Scholes Model | Options Greeks |
| Styling | CSS-in-JS | Component styles |

---

## ⚠️ Disclaimer

This is an **analytical tool** for educational purposes. Not financial advice.

- Always verify signals independently
- Start with paper trading
- Never risk more than you can afford to lose
- Options trading involves substantial risk

---

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs) - Interactive Swagger UI
- [Copilot Instructions](.github/copilot-instructions.md) - AI agent guide
- [Deployment Guides](docs/) - Production deployment

---

## 🤝 Support

For issues or questions:
1. Check [API docs](http://localhost:8000/docs)
2. Review [deployment guides](docs/)
3. Check backend logs for errors

**Happy Trading!** 📈
