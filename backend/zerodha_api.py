import time
import random
import logging
import math
from kiteconnect import KiteConnect
from config import ZERODHA_API_KEY, ZERODHA_API_SECRET, REDIRECT_URL, SYMBOL_MAPPING, CACHE_DURATION, PRICE_CACHE, OPTION_CHAIN_CACHE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state
kite = None
is_authenticated = False
access_token = None


def initialize_kite():
    """Initialize Kite client - does NOT require authentication"""
    global kite
    try:
        kite = KiteConnect(api_key=ZERODHA_API_KEY)
        logger.info("✓ KiteConnect client initialized successfully")
        logger.info(f"✓ Redirect URL configured: {REDIRECT_URL}")
        logger.info("✓ Ready for authentication flow")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize KiteConnect: {e}")
        kite = None
        return False


def get_auth_url():
    """Generate Zerodha login URL"""
    global kite
    try:
        if not kite:
            initialize_kite()
        if kite:
            login_url = kite.login_url()
            logger.info(f"Generated login URL: {login_url}")
            return login_url
    except Exception as e:
        logger.error(f"Error generating auth URL: {e}")
    return None


def set_access_token(request_token):
    """Exchange request token for access token"""
    global kite, is_authenticated, access_token
    try:
        if not kite:
            initialize_kite()
        
        if kite:
            logger.info(f"Exchanging request_token for access_token...")
            data = kite.generate_session(request_token, ZERODHA_API_SECRET)
            access_token = data['access_token']
            kite.set_access_token(access_token)
            is_authenticated = True
            logger.info(f"✓ Successfully authenticated! Access token: {access_token[:20]}...")
            return data
    except Exception as e:
        logger.error(f"✗ Error setting access token: {e}")
        is_authenticated = False
    return None


def check_connection():
    """Check if API is connected and authenticated"""
    return {
        'kite_initialized': kite is not None,
        'authenticated': is_authenticated,
        'access_token': access_token is not None,
        'api_key': ZERODHA_API_KEY is not None,
        'status': 'AUTHENTICATED' if is_authenticated else ('READY_FOR_AUTH' if kite else 'NOT_INITIALIZED')
    }


def get_ltp(symbol: str):
    """Get Last Traded Price - works only if authenticated"""
    try:
        cache_key = f"ltp_{symbol}"
        
        # Check cache first
        if cache_key in PRICE_CACHE:
            cached_time, price = PRICE_CACHE[cache_key]
            if time.time() - cached_time < CACHE_DURATION:
                return price
        
        # Try to fetch from Zerodha ONLY if authenticated
        if is_authenticated and kite:
            try:
                logger.info(f"Fetching live LTP for {symbol}...")
                # Try different symbol formats
                symbol_formats = [
                    f"NSE:{symbol}",
                    f"NFO:{symbol}2612550CE",  # NIFTY example
                    symbol
                ]
                
                for sym_format in symbol_formats:
                    try:
                        quote = kite.quote(sym_format)
                        if quote:
                            ltp = quote[sym_format]['last_price']
                            PRICE_CACHE[cache_key] = (time.time(), ltp)
                            logger.info(f"✓ Got live LTP for {symbol}: {ltp}")
                            return ltp
                    except:
                        continue
            except Exception as auth_error:
                logger.debug(f"Could not fetch live data for {symbol}: {auth_error}")
        else:
            logger.debug(f"Not authenticated. Using simulated LTP for {symbol}")
        
        # Fallback to simulated realistic data
        base_strike = SYMBOL_MAPPING.get(symbol, {}).get('strike_base', 20000)
        ltp = base_strike * random.uniform(0.99, 1.01)
        PRICE_CACHE[cache_key] = (time.time(), ltp)
        return ltp
        
    except Exception as e:
        logger.error(f"Error in get_ltp for {symbol}: {e}")
        base_strike = SYMBOL_MAPPING.get(symbol, {}).get('strike_base', 20000)
        return base_strike * random.uniform(0.99, 1.01)


def get_option_chain(symbol: str):
    """Get option chain with ATM and ITM strikes for both CE and PE with real data"""
    try:
        cache_key = f"option_chain_{symbol}"
        
        # Check cache
        if cache_key in OPTION_CHAIN_CACHE:
            cached_time, chain = OPTION_CHAIN_CACHE[cache_key]
            if time.time() - cached_time < CACHE_DURATION:
                return chain
        
        # Get current LTP to determine ATM
        ltp = get_ltp(symbol)
        if not ltp or ltp <= 0:
            base_strike = SYMBOL_MAPPING.get(symbol, {}).get('strike_base', 20000)
            ltp = base_strike
        
        # Determine strike interval
        strike_interval = 50 if symbol == "NIFTY" else (100 if symbol == "BANKNIFTY" else 100)
        atm_strike = round(ltp / strike_interval) * strike_interval
        
        # Get ATM and ITM strikes for both CE and PE
        strikes_to_fetch = [
            atm_strike,                     # ATM
            atm_strike - strike_interval,   # ITM for CE, OTM for PE
        ]
        
        # Try live data if authenticated
        if is_authenticated and kite:
            try:
                logger.info(f"Fetching LIVE option chain for {symbol} | LTP: {ltp:.2f} | ATM: {atm_strike}...")
                
                # Get instruments for option chain
                # Format: NFO:NIFTY26DEC24C20000
                from datetime import datetime, timedelta
                
                # Get nearest expiry (next Thursday for NIFTY/BANKNIFTY)
                today = datetime.now()
                days_ahead = (3 - today.weekday()) % 7  # Thursday = 3
                if days_ahead == 0:
                    days_ahead = 7
                expiry_date = today + timedelta(days=days_ahead)
                expiry_str = expiry_date.strftime('%y%b%d').upper()
                
                chain_data = {'strikes': []}
                
                for strike in strikes_to_fetch:
                    # Build instrument names for CE and PE
                    ce_instrument = f"NFO:{symbol}{expiry_str}{int(strike)}CE"
                    pe_instrument = f"NFO:{symbol}{expiry_str}{int(strike)}PE"
                    
                    try:
                        # Fetch quotes for both CE and PE
                        quotes = kite.quote([ce_instrument, pe_instrument])
                        
                        ce_data = quotes.get(ce_instrument, {})
                        pe_data = quotes.get(pe_instrument, {})
                        
                        strike_info = {
                            'strike': strike,
                            'ce': {
                                'ltp': ce_data.get('last_price', 0),
                                'oi': ce_data.get('oi', 0),
                                'iv': ce_data.get('ohlc', {}).get('close', 0) / strike * 100 * 0.01,  # Approximation
                                'volume': ce_data.get('volume', 0),
                                'bid': ce_data.get('depth', {}).get('buy', [{}])[0].get('price', 0),
                                'ask': ce_data.get('depth', {}).get('sell', [{}])[0].get('price', 0),
                            },
                            'pe': {
                                'ltp': pe_data.get('last_price', 0),
                                'oi': pe_data.get('oi', 0),
                                'iv': pe_data.get('ohlc', {}).get('close', 0) / strike * 100 * 0.01,  # Approximation
                                'volume': pe_data.get('volume', 0),
                                'bid': pe_data.get('depth', {}).get('buy', [{}])[0].get('price', 0),
                                'ask': pe_data.get('depth', {}).get('sell', [{}])[0].get('price', 0),
                            }
                        }
                        
                        chain_data['strikes'].append(strike_info)
                        logger.info(f"✓ Got LIVE data for strike {strike}: CE OI={strike_info['ce']['oi']}, PE OI={strike_info['pe']['oi']}")
                        
                    except Exception as strike_error:
                        logger.warning(f"Could not fetch strike {strike}: {strike_error}")
                        continue
                
                if chain_data['strikes']:
                    OPTION_CHAIN_CACHE[cache_key] = (time.time(), chain_data)
                    logger.info(f"✓ LIVE option chain cached for {symbol} with {len(chain_data['strikes'])} strikes")
                    return chain_data
                    
            except Exception as e:
                logger.error(f"Failed to fetch live option chain: {e}")
                logger.info(f"Falling back to simulated data...")
        
        # Fallback: Generate simulated data
        logger.info(f"Using simulated option chain for {symbol} (not authenticated)")
        chain_data = {
            'strikes': [
                {
                    'strike': strike,
                    'ce': {
                        'ltp': random.uniform(50, 500),
                        'oi': random.randint(10000, 200000),
                        'iv': random.uniform(0.15, 0.40),
                        'volume': random.randint(1000, 50000),
                        'bid': 0,
                        'ask': 0,
                    },
                    'pe': {
                        'ltp': random.uniform(50, 500),
                        'oi': random.randint(10000, 200000),
                        'iv': random.uniform(0.15, 0.40),
                        'volume': random.randint(1000, 50000),
                        'bid': 0,
                        'ask': 0,
                    }
                }
                for strike in strikes_to_fetch
            ]
        }
        
        OPTION_CHAIN_CACHE[cache_key] = (time.time(), chain_data)
        return chain_data
        
    except Exception as e:
        logger.error(f"Error in get_option_chain for {symbol}: {e}")
        return None


def calculate_greeks(ltp: float, strike: float, iv: float, time_to_expiry: float = 0.038) -> dict:
    """
    Calculate Greeks using Black-Scholes approximation
    time_to_expiry: 0.038 years ≈ 10 trading days (standard for weekly options)
    """
    try:
        r = 0.05  # Risk-free rate (5%)
        s = float(ltp)
        k = float(strike)
        sigma = float(iv)
        t = float(time_to_expiry)
        
        if t <= 0 or sigma <= 0 or s <= 0 or k <= 0:
            return {'delta': 0.0, 'gamma': 0.0, 'theta': 0.0, 'vega': 0.0}
        
        # d1 and d2 for Black-Scholes
        d1 = (math.log(s / k) + (r + 0.5 * sigma ** 2) * t) / (sigma * math.sqrt(t))
        d2 = d1 - sigma * math.sqrt(t)
        
        # Standard normal CDF approximation
        from math import pi, exp
        def norm_cdf(x):
            return 0.5 * (1 + math.erf(x / math.sqrt(2)))
        
        # Delta: N(d1)
        delta = norm_cdf(d1)
        
        # Gamma: n(d1) / (S * sigma * sqrt(T))
        norm_pdf_d1 = (1 / math.sqrt(2 * pi)) * exp(-0.5 * d1 ** 2)
        gamma = norm_pdf_d1 / (s * sigma * math.sqrt(t))
        
        # Vega: S * n(d1) * sqrt(T) / 100 (per 1% change in IV)
        vega = s * norm_pdf_d1 * math.sqrt(t) / 100
        
        # Theta: daily decay
        theta = (-s * norm_pdf_d1 * sigma / (2 * math.sqrt(t)) - r * k * exp(-r * t) * norm_cdf(d2)) / 252
        
        return {
            'delta': round(delta, 4),
            'gamma': round(gamma, 6),
            'theta': round(theta, 4),
            'vega': round(vega, 4),
        }
    except Exception as e:
        logger.error(f"Error calculating Greeks: {e}")
        return {'delta': 0.0, 'gamma': 0.0, 'theta': 0.0, 'vega': 0.0}


def generate_signal_from_market_data(symbol: str, params: dict) -> dict:
    """Generate STRONG BUY signal only when ALL Greeks, OI, and IV match for CE or PE"""
    try:
        from datetime import datetime
        
        # Get current LTP
        ltp = get_ltp(symbol)
        if not ltp or ltp <= 0:
            base_strike = SYMBOL_MAPPING.get(symbol, {}).get('strike_base', 20000)
            ltp = base_strike
        
        logger.info(f"Analyzing {symbol} | LTP: {ltp:.2f}")
        
        # Get option chain with live data
        option_chain = get_option_chain(symbol)
        if not option_chain or not option_chain.get('strikes'):
            logger.error(f"Failed to get option chain for {symbol}")
            return None
        
        strikes_data = option_chain['strikes']
        if not strikes_data:
            return None
        
        # Get thresholds
        vega_min = params.get('vega_min', 0.3)
        gamma_min = params.get('gamma_min', 0.05)
        theta_max = params.get('theta_min', -0.5)  # theta is negative
        delta_min = params.get('delta_min', 0.4)
        oi_min = params.get('iv_call_oi_min', 50000)
        iv_min = params.get('iv_min', 0.20)
        confidence_min = params.get('confidence_min', 0.80)  # High threshold for STRONG BUY
        
        best_signal = None
        max_confidence = 0.0
        
        # Analyze each strike for both CE and PE
        for strike_data in strikes_data:
            strike = strike_data['strike']
            
            # Analyze CE (Call Option)
            ce_data = strike_data.get('ce', {})
            if ce_data.get('oi', 0) > 0:
                ce_greeks = calculate_greeks(ltp, strike, ce_data.get('iv', 0.25))
                
                # Check if ALL CE Greeks match criteria
                ce_vega_match = abs(ce_greeks['vega']) >= vega_min
                ce_gamma_match = ce_greeks['gamma'] >= gamma_min
                ce_theta_match = ce_greeks['theta'] <= theta_max
                ce_delta_match = abs(ce_greeks['delta']) >= delta_min
                ce_oi_match = ce_data['oi'] >= oi_min
                ce_iv_match = ce_data['iv'] >= iv_min
                
                if ce_vega_match and ce_gamma_match and ce_theta_match and ce_delta_match and ce_oi_match and ce_iv_match:
                    # Calculate confidence score
                    vega_score = min(abs(ce_greeks['vega']) / vega_min, 1.0)
                    gamma_score = min(ce_greeks['gamma'] / gamma_min, 1.0)
                    delta_score = min(abs(ce_greeks['delta']) / delta_min, 1.0)
                    oi_score = min(ce_data['oi'] / oi_min, 1.0)
                    iv_score = min(ce_data['iv'] / iv_min, 1.0)
                    
                    confidence = (vega_score * 0.20 + gamma_score * 0.20 + delta_score * 0.20 + oi_score * 0.25 + iv_score * 0.15)
                    confidence = round(min(confidence, 1.0), 2)
                    
                    if confidence >= confidence_min and confidence > max_confidence:
                        max_confidence = confidence
                        best_signal = {
                            'symbol': symbol,
                            'timestamp': datetime.utcnow().strftime('%H:%M:%S'),
                            'option_type': 'CE',
                            'strike': strike,
                            'vega': ce_greeks['vega'],
                            'gamma': ce_greeks['gamma'],
                            'theta': ce_greeks['theta'],
                            'delta': ce_greeks['delta'],
                            'oi': ce_data['oi'],
                            'iv': ce_data['iv'],
                            'ltp_option': ce_data.get('ltp', 0),
                            'side': 'STRONG BUY CE',
                            'confidence': confidence,
                            'ltp': round(ltp, 2),
                            'data_source': 'ZERODHA_LIVE' if is_authenticated else 'SIMULATED',
                        }
                        logger.info(f"✓ STRONG CE MATCH: {symbol} Strike {strike} | Confidence: {confidence*100:.0f}% | OI: {ce_data['oi']}")
            
            # Analyze PE (Put Option)
            pe_data = strike_data.get('pe', {})
            if pe_data.get('oi', 0) > 0:
                pe_greeks = calculate_greeks(ltp, strike, pe_data.get('iv', 0.25))
                
                # Check if ALL PE Greeks match criteria
                pe_vega_match = abs(pe_greeks['vega']) >= vega_min
                pe_gamma_match = pe_greeks['gamma'] >= gamma_min
                pe_theta_match = pe_greeks['theta'] <= theta_max
                pe_delta_match = abs(pe_greeks['delta']) >= delta_min
                pe_oi_match = pe_data['oi'] >= oi_min
                pe_iv_match = pe_data['iv'] >= iv_min
                
                if pe_vega_match and pe_gamma_match and pe_theta_match and pe_delta_match and pe_oi_match and pe_iv_match:
                    # Calculate confidence score
                    vega_score = min(abs(pe_greeks['vega']) / vega_min, 1.0)
                    gamma_score = min(pe_greeks['gamma'] / gamma_min, 1.0)
                    delta_score = min(abs(pe_greeks['delta']) / delta_min, 1.0)
                    oi_score = min(pe_data['oi'] / oi_min, 1.0)
                    iv_score = min(pe_data['iv'] / iv_min, 1.0)
                    
                    confidence = (vega_score * 0.20 + gamma_score * 0.20 + delta_score * 0.20 + oi_score * 0.25 + iv_score * 0.15)
                    confidence = round(min(confidence, 1.0), 2)
                    
                    if confidence >= confidence_min and confidence > max_confidence:
                        max_confidence = confidence
                        best_signal = {
                            'symbol': symbol,
                            'timestamp': datetime.utcnow().strftime('%H:%M:%S'),
                            'option_type': 'PE',
                            'strike': strike,
                            'vega': pe_greeks['vega'],
                            'gamma': pe_greeks['gamma'],
                            'theta': pe_greeks['theta'],
                            'delta': pe_greeks['delta'],
                            'oi': pe_data['oi'],
                            'iv': pe_data['iv'],
                            'ltp_option': pe_data.get('ltp', 0),
                            'side': 'STRONG BUY PE',
                            'confidence': confidence,
                            'ltp': round(ltp, 2),
                            'data_source': 'ZERODHA_LIVE' if is_authenticated else 'SIMULATED',
                        }
                        logger.info(f"✓ STRONG PE MATCH: {symbol} Strike {strike} | Confidence: {confidence*100:.0f}% | OI: {pe_data['oi']}")
        
        if best_signal:
            logger.info(f"🎯 STRONG BUY SIGNAL: {symbol} {best_signal['option_type']} @ {best_signal['strike']} | Confidence: {best_signal['confidence']*100:.0f}%")
            return best_signal
        else:
            logger.info(f"ℹ️ No STRONG BUY signal for {symbol} - criteria not met")
            return None
        
    except Exception as e:
        logger.error(f"Error generating signal for {symbol}: {e}", exc_info=True)
        return None


# Initialize on module load
initialize_kite()

