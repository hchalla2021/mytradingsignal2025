# Market Signals - Zerodha Integration

Trading signals application with FastAPI backend and Next.js frontend for options Greeks calculation and signal generation.

## Architecture

**Backend (FastAPI)**: REST API serving real-time signals with Greeks calculation, option chain analysis, and Zerodha API integration
**Frontend (Next.js)**: Single-page dashboard with 10-second polling for live signal updates

### Critical Data Flow (STRONG BUY Only)

1. Frontend polls `/api/signal?symbol=X` every 10 seconds (see `frontend/pages/index.js` useEffect)
2. Backend generates signal via `zerodha_api.generate_signal_from_market_data()` which:
   - Fetches real-time option chain with ATM + ITM strikes for BOTH CE and PE
   - For each strike, calculates Greeks using Black-Scholes (delta, gamma, theta, vega)
   - **Checks ALL criteria for STRONG BUY**: vega ≥ 0.3, gamma ≥ 0.05, theta ≤ -0.5, delta ≥ 0.4, OI ≥ 50K, IV ≥ 20%
   - Only returns signal if **ALL Greeks + OI + IV match** for either CE or PE
   - Returns **single best signal** (highest confidence) or `None` if no match
3. Frontend displays STRONG BUY signal or "No Signal" waiting state

### State Management

- **Backend**: Dual-mode operation controlled by `is_authenticated` flag in `zerodha_api.py`
  - **Authenticated**: Uses live Zerodha API via `kite` instance
  - **Unauthenticated**: Falls back to realistic simulated data (ATM strikes calculated from base prices)
- **Frontend**: No global state - single signal stored in component state, updates every 10 seconds
- **Cache**: 5-second TTL for LTP and option chain in `PRICE_CACHE`/`OPTION_CHAIN_CACHE` dictionaries

## Development Workflows

### Running Locally (Windows)

```powershell
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend  
cd frontend
npm install  # first time only
npm run dev
```

Backend serves on `http://localhost:8000`, frontend on `http://localhost:3000`. API docs at `/docs`.

### Zerodha Authentication Flow

1. Start backend (initializes `kite` client in `zerodha_api.py`)
2. Call `GET /auth/login` to get login URL
3. User authenticates in browser, receives `request_token`
4. Call `POST /auth/callback?request_token=X` to exchange for `access_token`
5. Backend switches from simulated to live data (`is_authenticated = True`)

No manual token refresh - session persists until restart.

### Testing Without Zerodha

Backend runs in **demo mode** by default. `generate_signal_from_market_data()` detects `is_authenticated=False` and uses simulated Greeks with realistic ATM strikes. Frontend displays identical UI.

## Code Conventions

### Signal Structure (API Contract - STRONG BUY Only)

```python
{
    'symbol': str,           # NIFTY | BANKNIFTY | SENSEX
    'timestamp': str,        # HH:MM:SS UTC
    'option_type': str,      # CE | PE (Call or Put)
    'strike': int,           # The single strike price that matched
    'vega': float,           # Greek values for this strike
    'gamma': float,
    'theta': float,
    'delta': float,
    'oi': int,               # Open Interest for this option
    'iv': float,             # Implied Volatility (0-1)
    'ltp_option': float,     # Option LTP
    'ltp': float,            # Index LTP
    'side': str,             # STRONG BUY CE | STRONG BUY PE
    'confidence': float,     # 0.80-1.0 (only high confidence signals)
    'data_source': str,      # ZERODHA_LIVE | SIMULATED
}
# Returns None if no signal meets ALL criteria
```

### STRONG BUY Signal Logic

**All criteria must match for signal generation:**

1. **Strike Selection**: ATM and ITM strikes for both CE and PE
   - `atm_strike = round(ltp / strike_interval) * strike_interval`
   - Fetches: `[ATM, ATM - interval]` with full CE and PE data

2. **Greeks Thresholds** (ALL must pass):
   - Vega ≥ 0.3 (volatility sensitivity)
   - Gamma ≥ 0.05 (delta rate of change)
   - Theta ≤ -0.5 (time decay acceptable)
   - Delta ≥ 0.4 (directional exposure)

3. **Liquidity Thresholds** (ALL must pass):
   - Open Interest ≥ 50,000 (high liquidity)
   - Implied Volatility ≥ 20% (sufficient premium)

4. **Confidence Score** (weighted):
   - `(vega_score × 0.20) + (gamma_score × 0.20) + (delta_score × 0.20) + (oi_score × 0.25) + (iv_score × 0.15)`
   - Must be ≥ 0.80 (80%) to generate signal

5. **Best Signal Selection**: Returns highest confidence signal across all strikes/types, or `None`

### Backend Module Responsibilities

- `main.py`: FastAPI routes only, no business logic
- `zerodha_api.py`: All Zerodha integration + Greeks calculation + signal generation
- `signal_engine.py`: Legacy demo signal generator (not used in production flow)
- `config.py`: Credentials and thresholds (loads from `.env`)

### Frontend Patterns

- All styling is inline CSS-in-JS (no external CSS files for components)
- Animations defined in `<style jsx>` blocks within components
- Single API endpoint call: `axios.get('http://localhost:8000/api/signal', {params: {symbol}})`
- No parameter adjustment UI implemented (parameters hardcoded in backend)

## Integration Points

### Zerodha Kite API

**Authentication**: 3-legged OAuth flow (see "Zerodha Authentication Flow" above)

**Key Methods**:
- `kite.quote([instruments])` → Real-time LTP, OI, depth data
  - Format: `"NFO:NIFTY26DEC24C20000"` (segment:symbol+expiry+strike+type)
  - Returns: `last_price`, `oi`, `volume`, `depth` (bid/ask), `ohlc`
- `kite.generate_session(request_token, secret)` → access token exchange

**Option Chain Fetching**:
- Expiry calculation: Next Thursday for NIFTY/BANKNIFTY (weekly)
- Instrument format: `NFO:{SYMBOL}{YYMONDD}{STRIKE}{CE|PE}`
- Example: `NFO:NIFTY26DEC19850CE` for NIFTY 19850 Call expiring Dec 26

**Credential Sources**:
1. Environment variables (`.env` file)
2. Fallback to hardcoded values in `config.py`

### CORS Configuration

Backend allows all origins (`allow_origins=["*"]`) for local development. Production should restrict to deployed frontend domain.

## Key Files

- `backend/zerodha_api.py` - Core signal generation logic, Greeks calculation, API integration
- `backend/main.py` - FastAPI routes and endpoint definitions
- `frontend/pages/index.js` - Main dashboard with polling logic and animations
- `backend/config.py` - Credentials, symbol mappings, thresholds
- `build.bat` / `build.sh` - Dependency installation scripts (does NOT start servers)

## Common Tasks

**Add new symbol**: Update `SYMBOL_MAPPING` in `config.py` with token and strike_base, add to dropdown in `index.js`

**Adjust STRONG BUY thresholds**: Modify `DEFAULT_THRESHOLDS` in `config.py`:
- Increase `vega_min`/`gamma_min` for stricter Greeks
- Raise `iv_call_oi_min` for higher liquidity requirement
- Increase `confidence_min` (currently 0.80) for fewer but stronger signals

**Change polling interval**: Update `setInterval(fetchSignal, 10000)` in `index.js` useEffect

**Modify confidence formula**: Edit weights in `zerodha_api.generate_signal_from_market_data()` confidence calculation (~line 250)

**Debug live data**: 
- Check `/api/connection` for authentication status
- Verify `data_source` field in signal response (ZERODHA_LIVE vs SIMULATED)
- Backend logs show `✓ STRONG CE/PE MATCH` when criteria pass

**Test signal logic without Zerodha**: Backend automatically falls back to simulated data with realistic Greeks when not authenticated
