import React from 'react';

/**
 * IncidentHero Component
 * Displays the active incident narrative, technical telemetry metrics,
 * and the primary dispatch button.
 */
export function IncidentHero({
  incident,
  isInvestigating,
  onDispatch,
  i18n
}) {
  if (!incident) return null;

  return (
    <section className="incident-hero card-glass" id="incident-hero" aria-labelledby="hero-title">
      <div className="hero-meta">
        <span className="severity-pill critical" id="hero-severity">
          {incident.severity}
        </span>
        <span className="genre-pill" id="hero-genre">
          {incident.genre_track ? incident.genre_track.replace(/_/g, ' ') : 'EPIC HISTORICAL'}
        </span>
        <span className="time-pill" id="hero-time">
          T-Minus 4h to Release
        </span>
      </div>

      <h2 className="hero-title" id="hero-title">
        {incident.sequence_affected} — {incident.telemetry ? incident.telemetry.grafana_alert_uid : 'Incident'}
      </h2>

      <p className="hero-narrative" id="hero-narrative">
        {incident.cinematic_narrative}
      </p>

      {/* Technical Telemetry Details Bar */}
      <div className="telemetry-bar" id="telemetry-bar">
        <div className="telemetry-item">
          <span className="tel-label">Grafana Alert</span>
          <span className="tel-value mono" id="tel-alert">
            {incident.telemetry ? incident.telemetry.grafana_alert_uid : 'N/A'}
          </span>
        </div>
        <div className="telemetry-item">
          <span className="tel-label">PromQL Condition</span>
          <span className="tel-value mono" id="tel-metric" title={incident.telemetry ? incident.telemetry.promql_metric : ''}>
            {incident.telemetry ? incident.telemetry.promql_metric : 'N/A'}
          </span>
        </div>
        <div className="telemetry-item">
          <span className="tel-label">Tempo Trace ID</span>
          <span className="tel-value mono" id="tel-trace">
            {incident.telemetry ? incident.telemetry.tempo_trace_id : '7b8f9e1204cba31d'}
          </span>
        </div>
      </div>

      <div className="hero-actions">
        <button
          id="btn-run-investigation"
          className="btn btn-primary"
          onClick={onDispatch}
          disabled={isInvestigating}
          aria-busy={isInvestigating}
          aria-label="Dispatch Screen Crew"
        >
          {isInvestigating ? i18n.dispatching : i18n.dispatchBtn}
        </button>
      </div>
    </section>
  );
}
