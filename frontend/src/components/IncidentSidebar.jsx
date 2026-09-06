import React, { useState } from 'react';

/**
 * IncidentSidebar Component
 * Renders active incident list queue and synthetic chaos trigger.
 */
export function IncidentSidebar({
  incidents,
  selectedIncidentId,
  onSelectIncident,
  onInjectChaos,
  i18n
}) {
  const [selectedScenario, setSelectedScenario] = useState('ott_premiere_spike');

  return (
    <aside className="sidebar" role="region" aria-label="Active Incidents Queue">
      <div className="sidebar-header">
        <h2 className="section-heading">{i18n.incidentHeading}</h2>
        <span className="badge-count" id="incident-count">
          {incidents.length} Active
        </span>
      </div>

      <div className="incident-list" id="incident-list" role="listbox" aria-label="Incident options">
        {incidents.map((inc) => {
          const isActive = inc.id === selectedIncidentId;
          return (
            <div
              key={inc.id}
              className={`incident-card ${isActive ? 'active' : ''}`}
              id={`inc-card-${inc.id}`}
              onClick={() => onSelectIncident(inc)}
              role="option"
              aria-selected={isActive}
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  onSelectIncident(inc);
                }
              }}
              aria-label={`Incident ${inc.id}: ${inc.sequence_affected}, severity ${inc.severity}`}
            >
              <div className="card-top">
                <span className="incident-id">{inc.id}</span>
                <span className="severity-pill critical">{inc.severity}</span>
              </div>
              <div className="card-title">{inc.sequence_affected}</div>
              <div className="card-meta">
                <span>{inc.project_title}</span>
                <span>${inc.box_office_at_risk_usd ? inc.box_office_at_risk_usd.toLocaleString() : '0'} at risk</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Synthetic Chaos Trigger */}
      <div className="chaos-launcher card-glass">
        <h3 className="panel-subheading">{i18n.chaosTitle}</h3>
        <p className="panel-caption">{i18n.chaosDesc}</p>
        <select
          id="chaos-scenario-select"
          className="select-input"
          value={selectedScenario}
          onChange={(e) => setSelectedScenario(e.target.value)}
          aria-label="Select chaos scenario"
        >
          <option value="ott_premiere_spike">Midnight OTT CDN 504 Spike</option>
          <option value="vfx_crash">8K IMAX VFX CUDA OOM</option>
          <option value="wuxia_foley_lag">Wuxia Foley Combat Desync</option>
          <option value="anime_sakuga_stall">Anime Sakuga Framerate Stall</option>
        </select>
        <button
          id="btn-inject-chaos"
          className="btn btn-secondary full-width"
          onClick={() => onInjectChaos(selectedScenario)}
          aria-label="Inject synthetic chaos"
        >
          {i18n.chaosBtn}
        </button>
      </div>
    </aside>
  );
}
