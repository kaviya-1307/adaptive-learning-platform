import React, { useState, useEffect } from 'react';
import { RefreshCw, CheckCircle2, AlertCircle, Server, Database, Activity } from 'lucide-react';
import { fetchHealthStatus } from '../services/api';

export default function HealthIndicator() {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastChecked, setLastChecked] = useState(null);

  const checkHealth = async () => {
    setLoading(true);
    try {
      const result = await fetchHealthStatus();
      setHealthData(result || null);
    } catch (err) {
      setHealthData({
        success: false,
        data: null,
        latency: null,
        error: err?.message || 'Failed to check backend health',
      });
    } finally {
      setLastChecked(new Date().toLocaleTimeString());
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
    // Auto check every 15 seconds
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const isConnected = Boolean(healthData?.success);
  const latency = healthData?.latency;
  const hasLatency = latency !== null && latency !== undefined;

  return (
    <div className="card" style={{ borderLeft: isConnected ? '4px solid var(--accent-success)' : '4px solid var(--accent-danger)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <Server size={22} color="var(--accent-primary)" />
          <div>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 600 }}>Backend Connection Status</h3>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
              Checking endpoint: <code style={{ color: '#38bdf8' }}>GET http://localhost:8000/api/health</code>
            </p>
          </div>
        </div>

        <button 
          className="btn btn-secondary" 
          onClick={checkHealth} 
          disabled={loading}
          style={{ padding: '0.4rem 0.8rem', fontSize: '0.8125rem' }}
        >
          <RefreshCw size={14} className={loading ? 'spin' : ''} style={{ animation: loading ? 'spin 1s linear infinite' : 'none' }} />
          <span>Refresh</span>
        </button>
      </div>

      <div className="grid-3" style={{ marginTop: 0, marginBottom: '1rem' }}>
        {/* Status */}
        <div style={{ padding: '0.75rem 1rem', background: 'rgba(0,0,0,0.2)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <Activity size={16} color="var(--text-secondary)" />
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>Status</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span className={`status-indicator ${loading ? 'loading' : isConnected ? 'online' : 'offline'}`}></span>
            <span style={{ fontWeight: 600, fontSize: '0.9375rem' }}>
              {loading ? 'Checking...' : isConnected ? 'CONNECTED' : 'DISCONNECTED'}
            </span>
          </div>
        </div>

        {/* Latency */}
        <div style={{ padding: '0.75rem 1rem', background: 'rgba(0,0,0,0.2)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <Activity size={16} color="var(--text-secondary)" />
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>Latency</span>
          </div>
          <div style={{ fontWeight: 600, fontSize: '0.9375rem', color: hasLatency ? '#34d399' : 'var(--text-muted)' }}>
            {hasLatency ? `${latency} ms` : '—'}
          </div>
        </div>

        {/* Database */}
        <div style={{ padding: '0.75rem 1rem', background: 'rgba(0,0,0,0.2)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <Database size={16} color="var(--text-secondary)" />
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>Database</span>
          </div>
          <div style={{ fontWeight: 500, fontSize: '0.8125rem', color: healthData?.data?.database?.includes('healthy') ? '#34d399' : '#fbbf24', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={healthData?.data?.database || 'Pending'}>
            {healthData?.data?.database || (isConnected ? 'MySQL Configured' : 'Offline')}
          </div>
        </div>
      </div>

      {/* Raw Response Details */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
            Raw API Response {lastChecked && `(Last checked: ${lastChecked})`}
          </span>
        </div>
        <pre className="code-block">
          {healthData 
            ? JSON.stringify(isConnected ? (healthData?.data || {}) : { error: healthData?.error || 'Unavailable' }, null, 2)
            : '// Awaiting backend response...'}
        </pre>
      </div>
    </div>
  );
}
