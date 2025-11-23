export default function SignalCard({ signal }) {
  const isStrongBuy = signal.side === 'BUY' && signal.confidence >= 0.7
  const bgColor = isStrongBuy ? '#065f46' : signal.side === 'BUY' ? '#1e3a8a' : '#7f1d1d'

  return (
    <div
      style={{
        border: '1px solid #334155',
        padding: '1rem',
        borderRadius: '0.5rem',
        background: bgColor,
        backdropFilter: 'blur(10px)',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
        <div>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
            {signal.symbol} • {signal.timestamp}
          </div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, marginTop: '0.25rem' }}>
            {signal.side}
          </div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#4ade80' }}>
            {(signal.confidence * 100).toFixed(0)}%
          </div>
          <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>Confidence</div>
        </div>
      </div>

      <div style={{ borderTop: '1px solid #475569', paddingTop: '0.75rem', fontSize: '0.875rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
          <div>
            <div style={{ color: '#94a3b8' }}>Greeks</div>
            <div style={{ color: '#e2e8f0' }}>
              δ: {signal.delta.toFixed(3)} • γ: {signal.gamma.toFixed(3)}
            </div>
            <div style={{ color: '#e2e8f0' }}>
              θ: {signal.theta.toFixed(3)} • ν: {signal.vega.toFixed(3)}
            </div>
          </div>
          <div>
            <div style={{ color: '#94a3b8' }}>Strikes</div>
            <div style={{ color: '#60a5fa' }}>#{signal.strike1}</div>
            <div style={{ color: '#f87171' }}>#{signal.strike2}</div>
          </div>
        </div>
      </div>

      <div style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid #475569' }}>
        <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
          Open Interest
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
          <span>Call OI: <strong>{signal.iv_call_oi.toLocaleString()}</strong></span>
          <span>Put OI: <strong>{signal.iv_put_oi.toLocaleString()}</strong></span>
        </div>
      </div>
    </div>
  )
}
