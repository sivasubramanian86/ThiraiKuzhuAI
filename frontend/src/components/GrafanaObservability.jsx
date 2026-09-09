import React, { useState } from 'react';

const PROMQL_PRESETS = [
  {
    name: 'CDN 504 OTT Error Rate',
    query: "sum(rate(cdn_requests_total{status=~'5..'}[1m])) > 0.08",
    threshold: '8% spike',
    severity: 'CRITICAL'
  },
  {
    name: '8K IMAX GPU VRAM Saturation',
    query: 'gpu_vram_usage_bytes / gpu_vram_total_bytes > 0.95',
    threshold: '95% VRAM',
    severity: 'HIGH'
  },
  {
    name: 'Dolby Atmos Spatial Clock Drift',
    query: 'dolby_atmos_clock_drift_ms > 40',
    threshold: '40ms drift',
    severity: 'MEDIUM'
  },
  {
    name: 'HFR 120fps Frame Drop Ratio',
    query: 'playback_frame_drop_ratio > 0.05',
    threshold: '5% drop',
    severity: 'HIGH'
  }
];

const MOCK_LOKI_LOGS = [
  { time: '14:32:01.102', level: 'INFO', msg: '[Grafana MCP] Streamable HTTP transport handshake established on endpoint /mcp' },
  { time: '14:32:04.450', level: 'WARN', msg: '[Transcoder Origin] Secondary stream buffer depleted to 180ms. Origin cluster B under heavy load.' },
  { time: '14:32:08.891', level: 'ERROR', msg: '[OTT Gateway] 504 Gateway Timeout burst detected on regional edge node edge-bom-04.' },
  { time: '14:32:10.012', level: 'ALERT', msg: '[Alertmanager] Alert-OTT-504-ChaosSpike triggered. Fired to Thirai Kuzhu webhook.' },
  { time: '14:32:12.340', level: 'INFO', msg: '[ADK Agent Mesh] Executive Producer (A01) and Direction (B01) dispatched for incident INC-2026-CHAOS-01.' },
  { time: '14:32:18.910', level: 'SUCCESS', msg: '[Grafana Annotation] Registered director mitigation annotation (ID: ann-774129) on cinema-stream-master.' }
];

export function GrafanaObservability({ i18n = {} }) {
  const [selectedPreset, setSelectedPreset] = useState(PROMQL_PRESETS[0]);
  const [customQuery, setCustomQuery] = useState(PROMQL_PRESETS[0].query);
  const [queryResult, setQueryResult] = useState({
    status: 'success',
    value: '0.128 (12.8% Error Burst)',
    timestamp: '2026-09-07T09:12:00Z',
    active_alerts: 1
  });

  const handleApplyPreset = (p) => {
    setSelectedPreset(p);
    setCustomQuery(p.query);
    setQueryResult({
      status: 'success',
      value: p.name.includes('VRAM') ? '0.982 (98.2% VRAM saturation)' :
             p.name.includes('Clock') ? '48.2ms clock drift detected' :
             p.name.includes('Frame') ? '0.075 (7.5% frame drop)' :
             '0.128 (12.8% Error Burst)',
      timestamp: new Date().toISOString(),
      active_alerts: 1
    });
  };

  return (
    <div className="observability-container">
      {/* Header */}
      <div className="obs-header-glass">
        <div className="obs-title-group">
          <h2>📊 {i18n.grafana_telemetry_title || 'Grafana Cloud Observability & Telemetry'}</h2>
          <p>
            {i18n.grafana_telemetry_desc || 'Real-time telemetry infrastructure powered by Prometheus, Tempo distributed tracing, Loki logs, and Grafana Cloud MCP Streamable HTTP transport.'}
          </p>
        </div>
        <div className="mcp-badge-pill">
          <span className="pulse-dot" aria-hidden="true"></span>
          <span>{i18n.status_active ? `Grafana MCP: Streamable HTTP ${i18n.status_active}` : 'Grafana MCP: Streamable HTTP Active'}</span>
        </div>
      </div>

      {/* Live Metrics Cards */}
      <div className="metrics-summary-grid">
        {PROMQL_PRESETS.map((p, idx) => {
          const isSelected = selectedPreset.name === p.name;
          return (
            <div
              key={idx}
              className={`metric-stat-card-glass ${isSelected ? 'selected-card' : ''}`}
              onClick={() => handleApplyPreset(p)}
            >
              <div className="stat-card-header">
                <span className="stat-name">{p.name}</span>
                <span className={`severity-badge ${p.severity.toLowerCase()}`}>{p.severity}</span>
              </div>
              <div className="stat-value-row">
                <span className="stat-big-num">
                  {p.name.includes('VRAM') ? '98.2%' :
                   p.name.includes('Clock') ? '48ms' :
                   p.name.includes('Frame') ? '7.5%' : '12.8%'}
                </span>
                <span className="stat-unit">Alert Limit: {p.threshold}</span>
              </div>
              <p className="stat-query-code">{p.query}</p>
            </div>
          );
        })}
      </div>

      {/* PromQL Explorer & Trace Waterfall */}
      <div className="obs-workspace-layout">
        {/* Left Column: PromQL Console */}
        <div className="promql-card-glass">
          <h3>Prometheus Query Console</h3>
          <p className="hint-text">Inspect PromQL telemetry across cloud rendering, OTT streaming, and post-production nodes:</p>

          <div className="query-input-wrap">
            <span className="prom-prompt-symbol">&gt;</span>
            <input
              type="text"
              className="promql-input"
              value={customQuery}
              onChange={(e) => setCustomQuery(e.target.value)}
              placeholder="Enter PromQL query..."
            />
            <button className="btn-run-query" onClick={() => handleApplyPreset(selectedPreset)}>
              Run Query
            </button>
          </div>

          <div className="query-response-box">
            <div className="response-header">
              <span className="status-indicator-green">● Status: {queryResult.status}</span>
              <span className="ts-text">{queryResult.timestamp}</span>
            </div>
            <div className="metric-result-row">
              <span className="metric-key">Result Vector:</span>
              <span className="metric-val text-critical">{queryResult.value}</span>
            </div>
            <div className="metric-result-row">
              <span className="metric-key">Fired Alerts:</span>
              <span className="metric-val">{queryResult.active_alerts} Active</span>
            </div>
          </div>

          {/* Simulated Grafana Embed */}
          <div className="grafana-live-widget">
            <h4>Live Grafana Dashboard: cinema-stream-master</h4>
            <div className="chart-preview-box">
              <svg viewBox="0 0 500 120" className="chart-svg-live">
                <defs>
                  <linearGradient id="liveGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#EF4444" stopOpacity="0.3" />
                    <stop offset="100%" stopColor="#EF4444" stopOpacity="0" />
                  </linearGradient>
                </defs>
                <path d="M 0 100 Q 80 95, 150 90 T 260 85 T 340 30 T 420 20 L 500 25 L 500 120 L 0 120 Z" fill="url(#liveGrad)" />
                <path d="M 0 100 Q 80 95, 150 90 T 260 85 T 340 30 T 420 20 L 500 25" fill="none" stroke="#EF4444" strokeWidth="2.5" />
                <circle cx="420" cy="20" r="5" fill="#EF4444" />
                <text x="360" y="16" fill="#EF4444" fontSize="10" fontFamily="monospace">Spike: 12.8%</text>
              </svg>
            </div>
            <p className="grafana-caption">
              Auto-annotated via Thirai Kuzhu AI backend during incident triage.
            </p>
          </div>
        </div>

        {/* Right Column: Distributed Traces & Loki Logs */}
        <div className="traces-card-glass">
          <h3>Tempo Distributed Tracing & Loki Logs</h3>

          {/* Trace Waterfall */}
          <div className="trace-box">
            <div className="trace-header">
              <span>Trace ID: chaos-trace-8a9b1c</span>
              <span>Total Duration: 842ms</span>
            </div>

            <div className="waterfall-bars">
              <div className="span-row">
                <span className="span-name">Gateway Ingress</span>
                <div className="span-bar-container">
                  <div className="span-bar" style={{ left: '0%', width: '12%' }}></div>
                </div>
                <span className="span-duration">42ms</span>
              </div>
              <div className="span-row">
                <span className="span-name">Incident Triage</span>
                <div className="span-bar-container">
                  <div className="span-bar" style={{ left: '12%', width: '28%', background: '#F59E0B' }}></div>
                </div>
                <span className="span-duration">180ms</span>
              </div>
              <div className="span-row">
                <span className="span-name">ADK Agent Mesh</span>
                <div className="span-bar-container">
                  <div className="span-bar" style={{ left: '40%', width: '45%', background: '#06B6D4' }}></div>
                </div>
                <span className="span-duration">390ms</span>
              </div>
              <div className="span-row">
                <span className="span-name">Grafana Annotation</span>
                <div className="span-bar-container">
                  <div className="span-bar" style={{ left: '85%', width: '15%', background: '#10B981' }}></div>
                </div>
                <span className="span-duration">130ms</span>
              </div>
            </div>
          </div>

          {/* Loki Log Stream */}
          <div className="loki-stream-box">
            <h4>Live Loki Log Stream</h4>
            <div className="loki-scroll-window">
              {MOCK_LOKI_LOGS.map((log, idx) => (
                <div key={idx} className="loki-log-row">
                  <span className="log-time">{log.time}</span>
                  <span className={`log-level ${log.level.toLowerCase()}`}>[{log.level}]</span>
                  <span className="log-msg">{log.msg}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
