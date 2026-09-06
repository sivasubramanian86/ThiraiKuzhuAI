import React from 'react';

/**
 * GrafanaPanelEmbed Component
 * Visualizes real-time metrics, alert thresholds, and PromQL telemetry queries.
 */
export function GrafanaPanelEmbed({ promqlQuery, alertLabel }) {
  return (
    <section className="card-glass grafana-embed-card">
      <div className="card-header">
        <div className="grafana-header">
          <span className="grafana-icon" aria-hidden="true">📊</span>
          <h3 className="panel-subheading">Grafana Live Panel</h3>
        </div>
        <span className="badge-grafana">Mimir + Loki</span>
      </div>

      <div className="grafana-chart-container" id="grafana-chart">
        {/* SVG Real-Time Telemetry Graph */}
        <svg
          className="telemetry-chart"
          viewBox="0 0 320 160"
          preserveAspectRatio="none"
          role="img"
          aria-label="Live Telemetry Graph displaying PromQL alert spike"
        >
          <title>Live Telemetry Graph displaying PromQL alert spike</title>
          <defs>
            <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#F59E0B" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#F59E0B" stopOpacity="0.0" />
            </linearGradient>
          </defs>
          <path
            className="chart-grid"
            d="M 0,40 L 320,40 M 0,80 L 320,80 M 0,120 L 320,120"
          />
          <path
            className="chart-area"
            d="M 0,140 Q 40,130 80,120 T 160,110 T 240,40 T 320,30 L 320,160 L 0,160 Z"
          />
          <path
            className="chart-line"
            d="M 0,140 Q 40,130 80,120 T 160,110 T 240,40 T 320,30"
          />
          {/* Animated Critical Marker */}
          <circle cx="240" cy="40" r="5" className="chart-marker" />
          <text x="175" y="25" className="chart-label">
            {alertLabel || '504 Spike: 8.4%'}
          </text>
        </svg>
      </div>

      <div className="grafana-footer">
        <span className="mono tel-query">
          {promqlQuery || 'sum(rate(cdn_requests_total{status=~"5.."}[2m]))'}
        </span>
      </div>
    </section>
  );
}
