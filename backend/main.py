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


@app.get("/")
async def root():
    """Root endpoint - Redirect to API docs"""
    from fastapi.responses import HTMLResponse
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Market Signals API</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
                color: #e2e8f0;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                padding: 3rem;
                text-align: center;
            }
            h1 {
                font-size: 3rem;
                font-weight: 800;
                background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1rem;
            }
            .status {
                display: inline-block;
                padding: 0.75rem 1.5rem;
                background: linear-gradient(135deg, #065f46 0%, #047857 100%);
                color: #d1fae5;
                border-radius: 0.75rem;
                font-weight: 700;
                margin: 1rem 0;
            }
            .endpoints {
                background: rgba(30, 41, 59, 0.7);
                border: 2px solid #3b82f6;
                border-radius: 1rem;
                padding: 2rem;
                margin: 2rem 0;
                text-align: left;
            }
            .endpoint {
                margin: 1rem 0;
                padding: 1rem;
                background: rgba(15, 23, 42, 0.8);
                border-radius: 0.5rem;
            }
            .endpoint-label {
                color: #94a3b8;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            }
            .endpoint-url {
                color: #60a5fa;
                font-family: monospace;
                font-size: 0.95rem;
                margin-top: 0.5rem;
            }
            a {
                color: #60a5fa;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .btn {
                display: inline-block;
                padding: 1rem 2rem;
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                color: white;
                border-radius: 0.75rem;
                font-weight: 700;
                margin: 1rem 0.5rem;
                text-decoration: none;
                transition: transform 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Market Signals API</h1>
            <div class="status">✅ Live & Running</div>
            <p style="font-size: 1.2rem; color: #cbd5e1; margin: 2rem 0;">
                Trading signals with live Zerodha data, Greeks calculation, and option chain analysis
            </p>
            
            <div style="margin: 2rem 0;">
                <a href="/docs" class="btn">📚 API Documentation</a>
                <a href="/api/signal?symbol=NIFTY" class="btn">📊 Get Signal</a>
            </div>

            <div class="endpoints">
                <h3 style="color: #e2e8f0; margin-top: 0;">Available Endpoints</h3>
                
                <div class="endpoint">
                    <div class="endpoint-label">📊 Get Trading Signal</div>
                    <div class="endpoint-url"><a href="/api/signal?symbol=NIFTY">/api/signal?symbol=NIFTY</a></div>
                </div>
                
                <div class="endpoint">
                    <div class="endpoint-label">🔗 Connection Status</div>
                    <div class="endpoint-url"><a href="/api/connection">/api/connection</a></div>
                </div>
                
                <div class="endpoint">
                    <div class="endpoint-label">❤️ Health Check</div>
                    <div class="endpoint-url"><a href="/health">/health</a></div>
                </div>
                
                <div class="endpoint">
                    <div class="endpoint-label">📋 Available Symbols</div>
                    <div class="endpoint-url"><a href="/api/symbols">/api/symbols</a></div>
                </div>
                
                <div class="endpoint">
                    <div class="endpoint-label">🔐 Zerodha Login</div>
                    <div class="endpoint-url"><a href="/auth/login">/auth/login</a></div>
                </div>
            </div>

            <p style="color: #64748b; font-size: 0.9rem;">
                Version 2.0.0 | FastAPI + Zerodha KiteConnect
            </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


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

