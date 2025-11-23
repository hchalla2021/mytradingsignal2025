import os
from dotenv import load_dotenv

load_dotenv()

# Zerodha API Credentials
ZERODHA_API_KEY = os.getenv('ZERODHA_API_KEY', 'g5tyrnn1mlckrb6f')
ZERODHA_API_SECRET = os.getenv('ZERODHA_API_SECRET', '9qlzwmum5f7pami0gacyxc7uxa6w823s')
ZERODHA_USERNAME = os.getenv('ZERODHA_USERNAME', '')
ZERODHA_PASSWORD = os.getenv('ZERODHA_PASSWORD', '')
REDIRECT_URL = os.getenv('REDIRECT_URL', 'http://127.0.0.1:8000/auth/callback')

# Signal thresholds for STRONG BUY (all must match)
DEFAULT_THRESHOLDS = {
    'vega_min': 0.3,          # Minimum vega (volatility sensitivity)
    'gamma_min': 0.05,        # Minimum gamma (delta sensitivity)
    'theta_min': -0.5,        # Maximum theta (time decay, negative)
    'delta_min': 0.4,         # Minimum delta (directional movement)
    'iv_call_oi_min': 50000,  # Minimum Open Interest (high liquidity)
    'iv_min': 0.20,           # Minimum Implied Volatility (20%)
    'confidence_min': 0.80,   # Minimum confidence for STRONG BUY (80%)
}

# Symbol mappings - Zerodha instrument tokens
SYMBOL_MAPPING = {
    'NIFTY': {
        'token': '99926009',
        'strike_base': 20000,
        'expiry': 'current',
    },
    'BANKNIFTY': {
        'token': '99926037',
        'strike_base': 45000,
        'expiry': 'current',
    },
    'SENSEX': {
        'token': '99926000',
        'strike_base': 70000,
        'expiry': 'current',
    },
}

# Cache settings
CACHE_DURATION = 5  # seconds
PRICE_CACHE = {}
OPTION_CHAIN_CACHE = {}
