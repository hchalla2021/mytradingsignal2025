import { useEffect, useState } from 'react'
import axios from 'axios'

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

export default function Home() {
  const [symbol, setSymbol] = useState('NIFTY')
  const [signal, setSignal] = useState(null)
  const [prevSignal, setPrevSignal] = useState(null)
  const [connected, setConnected] = useState(false)
  const [loading, setLoading] = useState(false)
  const [lastUpdate, setLastUpdate] = useState(null)
  const [strikeAnimation, setStrikeAnimation] = useState(false)

  // Fetch signals every 10 seconds
  useEffect(() => {
    const fetchSignal = async () => {
      setLoading(true)
      try {
        const response = await axios.get(`${BACKEND_URL}/api/signal`, {
          params: { symbol },
        })
        setPrevSignal(signal)
        // Backend returns null if no STRONG BUY signal
        setSignal(response.data)
        setLastUpdate(new Date())
        setConnected(true)
        if (response.data) {
          setStrikeAnimation(true)
          setTimeout(() => setStrikeAnimation(false), 600)
        }
      } catch (error) {
        console.error('Error fetching signal:', error)
        setSignal(null)
        setConnected(false)
      } finally {
        setLoading(false)
      }
    }

    fetchSignal()
    const interval = setInterval(fetchSignal, 10000)

    return () => clearInterval(interval)
  }, [symbol])

  const handleSymbolChange = (newSymbol) => {
    setSymbol(newSymbol)
  }

  const getStrikeDifference = () => {
    if (!signal || !prevSignal) return null
    const diff = signal.strike1 - prevSignal.strike1
    return diff !== 0 ? diff : null
  }

  return (
    <div className="container">
      <style jsx>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
        @keyframes slideIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes glow {
          0%, 100% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
          50% { box-shadow: 0 0 40px rgba(59, 130, 246, 0.6); }
        }
        @keyframes buyGlow {
          0%, 100% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.3); }
          50% { box-shadow: 0 0 40px rgba(16, 185, 129, 0.6); }
        }
        @keyframes sellGlow {
          0%, 100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }
          50% { box-shadow: 0 0 40px rgba(239, 68, 68, 0.6); }
        }
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-2px); }
          75% { transform: translateX(2px); }
        }
        @keyframes pulse-card {
          0% { transform: scale(1); }
          50% { transform: scale(1.05); }
          100% { transform: scale(1); }
        }
        .container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        }
        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 2rem;
          background: linear-gradient(90deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
          border-bottom: 2px solid rgba(59, 130, 246, 0.2);
          backdrop-filter: blur(10px);
        }
        .header-content {
          flex: 1;
        }
        .header-left {
          display: flex;
          align-items: center;
          gap: 1.5rem;
          margin-bottom: 0.5rem;
        }
        .header-left h1 {
          font-size: 2.5rem;
          font-weight: 800;
          margin: 0;
          background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        .status {
          padding: 0.5rem 1.2rem;
          border-radius: 0.75rem;
          font-size: 0.95rem;
          font-weight: 700;
          letter-spacing: 0.05em;
        }
        .status.connected {
          background: linear-gradient(135deg, #065f46 0%, #047857 100%);
          color: #d1fae5;
          box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
        }
        .status.disconnected {
          background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
          color: #fee2e2;
          box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
        }
        .last-update {
          font-size: 0.85rem;
          color: #94a3b8;
        }
        .symbol-select {
          padding: 0.9rem 1.8rem;
          font-size: 1.1rem;
          background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
          color: #e2e8f0;
          border: 2px solid #3b82f6;
          border-radius: 0.75rem;
          cursor: pointer;
          font-weight: 700;
          transition: all 0.3s ease;
        }
        .symbol-select:hover {
          border-color: #60a5fa;
          box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        }
        .symbol-select:focus {
          outline: none;
          border-color: #93c5fd;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        .main {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
          overflow-y: auto;
        }
        .loading-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 1.5rem;
          color: #94a3b8;
        }
        .loading-spinner {
          width: 50px;
          height: 50px;
          border: 4px solid rgba(59, 130, 246, 0.2);
          border-top: 4px solid #3b82f6;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        .no-signal-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 1rem;
          padding: 3rem;
          background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.5) 100%);
          border: 2px dashed #475569;
          border-radius: 1.5rem;
          text-align: center;
          max-width: 500px;
        }
        .no-signal-icon {
          font-size: 4rem;
          opacity: 0.5;
        }
        .no-signal-title {
          font-size: 2rem;
          font-weight: 700;
          color: #94a3b8;
          margin: 0;
        }
        .no-signal-text {
          font-size: 1.1rem;
          color: #cbd5e1;
          margin: 0;
        }
        .no-signal-detail {
          font-size: 0.9rem;
          color: #64748b;
          margin: 0;
        }
        .no-signal-time {
          font-size: 0.85rem;
          color: #475569;
          margin-top: 1rem;
        }
        .data-source-badge {
          display: inline-block;
          padding: 0.5rem 1rem;
          background: rgba(59, 130, 246, 0.2);
          border: 1px solid #3b82f6;
          border-radius: 0.5rem;
          font-size: 0.85rem;
          font-weight: 700;
          color: #60a5fa;
          margin-top: 0.5rem;
        }
        .option-type-badge {
          display: inline-block;
          padding: 0.75rem 1.5rem;
          background: rgba(251, 191, 36, 0.2);
          border: 2px solid #fbbf24;
          border-radius: 0.75rem;
          font-size: 1.5rem;
          font-weight: 900;
          color: #fbbf24;
          margin: 0.5rem 0;
          letter-spacing: 0.1em;
        }
        .action-box.strong-buy {
          background: linear-gradient(135deg, #065f46 0%, #047857 100%);
          border-color: #10b981;
          animation: buyGlow 2s ease-in-out infinite;
        }
        .strike-highlight {
          display: flex;
          justify-content: center;
          margin: 2rem 0;
        }
        .strike-main-card {
          padding: 3rem 4rem;
          background: linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
          border: 3px solid #3b82f6;
          border-radius: 1.5rem;
          text-align: center;
          box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3);
        }
        .strike-price-large {
          font-size: 4rem;
          font-weight: 900;
          color: #60a5fa;
          margin: 1rem 0;
          text-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
        }
        .strike-ltp {
          font-size: 1rem;
          color: #cbd5e1;
          margin: 0.5rem 0;
        }
        .metrics-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1.5rem;
          margin: 2rem 0;
        }
        .metric-card {
          padding: 2rem;
          background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
          border: 2px solid #8b5cf6;
          border-radius: 1rem;
          text-align: center;
          backdrop-filter: blur(10px);
        }
        .metric-icon {
          font-size: 2rem;
          margin-bottom: 0.5rem;
        }
        .metric-label {
          font-size: 0.9rem;
          color: #94a3b8;
          margin-bottom: 0.75rem;
          text-transform: uppercase;
          letter-spacing: 0.1em;
        }
        .metric-value {
          font-size: 2rem;
          font-weight: 900;
          color: #a78bfa;
        }
        .signal-container {
          width: 100%;
          max-width: 700px;
          display: flex;
          flex-direction: column;
          gap: 2.5rem;
          animation: slideIn 0.5s ease-out;
        }
        .signal-header {
          text-align: center;
          margin-bottom: 1rem;
        }
        .symbol-name {
          font-size: 4rem;
          font-weight: 900;
          margin: 0;
          color: #e2e8f0;
          letter-spacing: -0.02em;
        }
        .signal-time {
          font-size: 1rem;
          color: #94a3b8;
          margin: 0.5rem 0 0 0;
        }
        .signal-action {
          display: flex;
          justify-content: center;
        }
        .action-box {
          padding: 3rem 4rem;
          border-radius: 1.5rem;
          text-align: center;
          border: 3px solid;
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
        }
        .action-box::before {
          content: '';
          position: absolute;
          top: 0;
          left: -100%;
          width: 100%;
          height: 100%;
          background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
          transition: left 0.5s ease;
        }
        .action-box.animate::before {
          left: 100%;
        }
        .action-box.buy {
          background: linear-gradient(135deg, #065f46 0%, #047857 100%);
          border-color: #10b981;
          animation: buyGlow 2s ease-in-out infinite;
        }
        .action-box.sell {
          background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
          border-color: #ef4444;
          animation: sellGlow 2s ease-in-out infinite;
        }
        .action-label {
          font-size: 3rem;
          font-weight: 900;
          margin-bottom: 1rem;
          letter-spacing: 0.05em;
        }
        .confidence-badge {
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        .confidence-value {
          font-size: 2.5rem;
          font-weight: 900;
          color: #fbbf24;
        }
        .confidence-label {
          font-size: 0.9rem;
          color: rgba(255, 255, 255, 0.8);
          margin-top: 0.25rem;
        }
        .strikes-section {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2rem;
        }
        .strike-card {
          padding: 2.5rem 2rem;
          background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
          border: 2px solid #3b82f6;
          border-radius: 1.2rem;
          text-align: center;
          transition: all 0.3s ease;
          backdrop-filter: blur(10px);
        }
        .strike-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
          border-color: #60a5fa;
        }
        .strike-card.pulse-card {
          animation: pulse-card 0.6s ease-out;
        }
        .strike-label {
          font-size: 0.85rem;
          color: #94a3b8;
          margin-bottom: 0.75rem;
          text-transform: uppercase;
          letter-spacing: 0.15em;
          font-weight: 700;
        }
        .strike-price {
          font-size: 3rem;
          font-weight: 900;
          color: #60a5fa;
          margin: 0.5rem 0;
        }
        .strike-diff {
          font-size: 0.9rem;
          font-weight: 700;
          margin-top: 0.75rem;
        }
        .strike-diff.up {
          color: #10b981;
        }
        .strike-diff.down {
          color: #ef4444;
        }
        .oi-section {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1.5rem;
        }
        .oi-card {
          padding: 1.5rem;
          background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
          border: 2px solid #8b5cf6;
          border-radius: 1rem;
          text-align: center;
          backdrop-filter: blur(10px);
          transition: all 0.3s ease;
        }
        .oi-card:hover {
          transform: translateY(-3px);
          box-shadow: 0 8px 20px rgba(139, 92, 246, 0.2);
        }
        .oi-icon {
          font-size: 1.5rem;
          margin-bottom: 0.5rem;
        }
        .oi-label {
          font-size: 0.85rem;
          color: #94a3b8;
          margin-bottom: 0.5rem;
          text-transform: uppercase;
          letter-spacing: 0.1em;
        }
        .oi-value {
          font-size: 1.8rem;
          font-weight: 900;
          color: #a78bfa;
        }
        .greeks-section {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 1.2rem;
        }
        .greek-card {
          padding: 1.5rem 1.2rem;
          background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
          border-left: 4px solid #06b6d4;
          border-radius: 0.75rem;
          text-align: center;
          backdrop-filter: blur(10px);
          transition: all 0.3s ease;
        }
        .greek-card:hover {
          transform: translateX(5px);
          box-shadow: 0 5px 15px rgba(6, 182, 212, 0.2);
        }
        .greek-symbol {
          font-size: 1.5rem;
          font-weight: 900;
          color: #06b6d4;
        }
        .greek-name {
          font-size: 0.8rem;
          color: #94a3b8;
          margin: 0.3rem 0;
          text-transform: uppercase;
          letter-spacing: 0.1em;
        }
        .greek-value {
          font-size: 1.2rem;
          font-weight: 800;
          color: #06b6d4;
        }
        .footer-info {
          text-align: center;
          color: #64748b;
          font-size: 0.9rem;
          margin-top: 1rem;
        }
      `}</style>

      <header className="header">
        <div className="header-content">
          <div className="header-left">
            <h1>Trading Signals</h1>
            <div className={`status ${connected ? 'connected' : 'disconnected'}`}>
              {connected ? '🟢 Live' : '🔴 Offline'}
            </div>
          </div>
          {lastUpdate && (
            <div className="last-update">
              Updated: {lastUpdate.toLocaleTimeString()}
            </div>
          )}
        </div>
        <select value={symbol} onChange={(e) => handleSymbolChange(e.target.value)} className="symbol-select">
          <option>NIFTY</option>
          <option>BANKNIFTY</option>
          <option>SENSEX</option>
        </select>
      </header>

      <main className="main">
        {loading && !signal ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Scanning for STRONG BUY signals...</p>
          </div>
        ) : !signal ? (
          <div className="no-signal-container">
            <div className="no-signal-icon">🔍</div>
            <h2 className="no-signal-title">No Signal</h2>
            <p className="no-signal-text">
              Waiting for STRONG BUY opportunity on {symbol}
            </p>
            <p className="no-signal-detail">
              All Greeks, OI, and IV criteria must match for signal
            </p>
            {lastUpdate && (
              <p className="no-signal-time">
                Last checked: {lastUpdate.toLocaleTimeString()}
              </p>
            )}
          </div>
        ) : (
          <div className="signal-container">
            <div className="signal-header">
              <h2 className="symbol-name">{signal.symbol}</h2>
              <p className="signal-time">{signal.timestamp}</p>
              <div className="data-source-badge">
                {signal.data_source === 'ZERODHA_LIVE' ? '📡 LIVE DATA' : '🔄 SIMULATED'}
              </div>
            </div>

            <div className="signal-action">
              <div className={`action-box strong-buy ${strikeAnimation ? 'animate' : ''}`}>
                <div className="action-label">{signal.side}</div>
                <div className="option-type-badge">{signal.option_type}</div>
                <div className="confidence-badge">
                  <div className="confidence-value">{(signal.confidence * 100).toFixed(0)}%</div>
                  <div className="confidence-label">Confidence</div>
                </div>
              </div>
            </div>

            <div className="strike-highlight">
              <div className="strike-main-card">
                <div className="strike-label">STRIKE PRICE</div>
                <div className="strike-price-large">{signal.strike}</div>
                <div className="strike-ltp">Option LTP: ₹{signal.ltp_option.toFixed(2)}</div>
                <div className="strike-ltp">Index LTP: ₹{signal.ltp.toFixed(2)}</div>
              </div>
            </div>

            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-icon">📊</div>
                <div className="metric-label">Open Interest</div>
                <div className="metric-value">{(signal.oi / 1000).toFixed(0)}K</div>
              </div>
              <div className="metric-card">
                <div className="metric-icon">📈</div>
                <div className="metric-label">Implied Volatility</div>
                <div className="metric-value">{(signal.iv * 100).toFixed(1)}%</div>
              </div>
            </div>

            <div className="greeks-section">
              <div className="greek-card">
                <div className="greek-symbol">Δ</div>
                <div className="greek-name">Delta</div>
                <div className="greek-value">{signal.delta.toFixed(3)}</div>
              </div>
              <div className="greek-card">
                <div className="greek-symbol">Γ</div>
                <div className="greek-name">Gamma</div>
                <div className="greek-value">{signal.gamma.toFixed(3)}</div>
              </div>
              <div className="greek-card">
                <div className="greek-symbol">Θ</div>
                <div className="greek-name">Theta</div>
                <div className="greek-value">{signal.theta.toFixed(3)}</div>
              </div>
              <div className="greek-card">
                <div className="greek-symbol">Ν</div>
                <div className="greek-name">Vega</div>
                <div className="greek-value">{signal.vega.toFixed(3)}</div>
              </div>
            </div>

            <div className="footer-info">
              <p>✅ All criteria matched • Updates every 10 seconds</p>
            </div>
          </div>
        )}
      </main>

      <style jsx>{`
        .container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background: #0f172a;
          color: #e2e8f0;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1.5rem;
          border-bottom: 1px solid #1e293b;
          background: #020617;
        }

        .header h1 {
          margin: 0;
          font-size: 1.5rem;
          font-weight: 700;
        }

        .status {
          padding: 0.5rem 1rem;
          border-radius: 0.375rem;
          font-size: 0.875rem;
          font-weight: 600;
        }

        .status.connected {
          background: #065f46;
          color: #d1fae5;
        }

        .status.disconnected {
          background: #7f1d1d;
          color: #fee2e2;
        }

        .main {
          display: flex;
          flex: 1;
          gap: 1.5rem;
          padding: 1.5rem;
          overflow: hidden;
        }

        .sidebar {
          width: 280px;
          background: #1e293b;
          border-radius: 0.5rem;
          padding: 1.5rem;
          border: 1px solid #334155;
          overflow-y: auto;
        }

        .symbol-selector {
          margin-bottom: 1.5rem;
        }

        .symbol-selector label {
          display: block;
          font-size: 0.875rem;
          font-weight: 600;
          margin-bottom: 0.5rem;
          color: #cbd5e1;
        }

        .symbol-selector select {
          width: 100%;
          padding: 0.5rem;
          background: #0f172a;
          color: #e2e8f0;
          border: 1px solid #334155;
          border-radius: 0.375rem;
          font-size: 0.875rem;
        }

        .symbol-selector select:focus {
          outline: none;
          border-color: #3b82f6;
        }

        .signals-grid {
          flex: 1;
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 1rem;
          overflow-y: auto;
        }

        .no-signals {
          grid-column: 1 / -1;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #64748b;
        }

        @media (max-width: 768px) {
          .main {
            flex-direction: column;
          }

          .sidebar {
            width: 100%;
          }

          .signals-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  )
}
