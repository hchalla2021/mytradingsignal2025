from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from config import DEFAULT_THRESHOLDS
from zerodha_api import generate_signal_from_market_data, get_auth_url, set_access_token, check_connection

app = FastAPI(title="Market Signals API - Live Zerodha", version="2.0.0")

# Enable CORS
import os
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    os.getenv("FRONTEND_URL", ""),
    "https://*.onrender.com",
]
# Remove empty strings
allowed_origins = [origin for origin in allowed_origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["*"] for development, specify domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "market-signals-api-zerodha-live"}


@app.get("/api/connection")
async def get_connection_status():
    """Check Zerodha API connection status"""
    return check_connection()


@app.get("/auth/login")
async def get_login_url():
    """Get Zerodha login URL"""
    auth_url = get_auth_url()
    if auth_url:
        return {
            "login_url": auth_url,
            "instruction": "Open this URL in a browser to authenticate with Zerodha"
        }
    return {"error": "Failed to generate login URL"}


@app.post("/auth/callback")
async def auth_callback(request_token: str):
    """Handle Zerodha callback with request token"""
    result = set_access_token(request_token)
    if result:
        return {"status": "authenticated", "access_token": result.get('access_token')}
    return {"error": "Failed to authenticate"}


@app.get("/api/signal")
async def get_signal(
    symbol: str = Query("NIFTY", description="Stock symbol (NIFTY, BANKNIFTY, SENSEX)"),
    vega_min: float = Query(0.3),
    gamma_min: float = Query(0.05),
    theta_min: float = Query(-0.5),
    iv_call_oi_min: int = Query(5000),
    confidence_min: float = Query(0.6),
):
    """
    Get a single market signal with LIVE data from Zerodha.
    
    Parameters:
    - symbol: NIFTY, BANKNIFTY, or SENSEX
    - vega_min: Minimum vega threshold
    - gamma_min: Minimum gamma threshold
    - theta_min: Minimum theta threshold
    - iv_call_oi_min: Minimum IV Call OI
    - confidence_min: Minimum confidence score (0-1)
    
    Returns signal with Greeks, OI, strike prices, and buy/sell recommendation.
    """
    if symbol not in ["NIFTY", "BANKNIFTY", "SENSEX"]:
        raise HTTPException(status_code=400, detail="Invalid symbol")
    
    params = {
        'vega_min': vega_min,
        'gamma_min': gamma_min,
        'theta_min': theta_min,
        'iv_call_oi_min': iv_call_oi_min,
        'confidence_min': confidence_min,
    }
    
    signal = generate_signal_from_market_data(symbol, params)
    
    if not signal:
        # No STRONG BUY signal found - return null/empty response
        logger.info(f"No STRONG BUY signal for {symbol} - criteria not met")
        return None
    
    logger.info(f"Generated signal for {symbol}: {signal['side']} (confidence: {signal['confidence']}, source: {signal['data_source']})")
    
    return signal


@app.get("/api/signals")
async def get_signals_batch(
    symbols: str = Query("NIFTY,BANKNIFTY,SENSEX"),
    count: int = Query(1, ge=1, le=10),
):
    """Get multiple signals for multiple symbols using live data."""
    symbol_list = symbols.split(",")
    signals = []
    
    for symbol in symbol_list:
        symbol = symbol.strip().upper()
        if symbol in ["NIFTY", "BANKNIFTY", "SENSEX"]:
            for _ in range(count):
                signal = generate_signal_from_market_data(symbol, DEFAULT_THRESHOLDS)
                if signal:
                    signals.append(signal)
    
    return {"signals": signals, "count": len(signals)}


@app.get("/api/symbols")
async def get_available_symbols():
    """Get list of available symbols."""
    return {
        "symbols": ["NIFTY", "BANKNIFTY", "SENSEX"],
        "description": "Available stock index options with live Zerodha data"
    }


@app.get("/api/status")
async def get_api_status():
    """Get API and data source status"""
    return {
        "service": "market-signals-api",
        "version": "2.0.0",
        "data_source": "ZERODHA_LIVE",
        "api_key_configured": True,
        "symbols": ["NIFTY", "BANKNIFTY", "SENSEX"],
        "refresh_interval": "10 seconds"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

