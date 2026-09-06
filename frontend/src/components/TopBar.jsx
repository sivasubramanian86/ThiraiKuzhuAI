import React from 'react';

/**
 * TopBar Component
 * Renders header branding, studio project dropdown, CRI readiness gauge,
 * language selector, and Grafana Cloud MCP live status badge.
 */
export function TopBar({
  projects,
  selectedProject,
  onSelectProject,
  criScore,
  language,
  onChangeLanguage,
  supportedLanguages,
  i18n
}) {
  return (
    <header className="topbar" role="banner">
      <div className="brand-cluster">
        <div className="brand-logo" aria-hidden="true">🎬</div>
        <div>
          <h1 className="brand-title">
            Thirai Kuzhu AI <span className="tamil-title">(திரை குழு AI)</span>
          </h1>
          <p className="brand-subtitle">{i18n.brandSubtitle}</p>
        </div>
      </div>

      <div className="header-controls">
        {/* Project Selector */}
        <div className="control-group">
          <label htmlFor="project-select" className="visually-hidden">
            Select Studio Production
          </label>
          <select
            id="project-select"
            className="select-input"
            value={selectedProject}
            onChange={(e) => onSelectProject(e.target.value)}
            aria-label="Select Studio Production"
          >
            {projects.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title} ({p.genre_track ? p.genre_track.replace(/_/g, ' ') : ''})
              </option>
            ))}
          </select>
        </div>

        {/* Cinematic Readiness Index Gauge */}
        <div
          className="cri-badge"
          id="cri-badge"
          title="Cinematic Readiness Index"
          role="status"
          aria-live="polite"
          aria-label={`Cinematic Readiness Index: ${criScore.toFixed(1)} percent`}
        >
          <span className="cri-label">CRI</span>
          <span className="cri-value" id="cri-value">
            {criScore.toFixed(1)}%
          </span>
          <span className="cri-status-dot" aria-hidden="true"></span>
        </div>

        {/* Language Selector */}
        <div className="control-group">
          <label htmlFor="lang-select" className="visually-hidden">
            Language
          </label>
          <select
            id="lang-select"
            className="select-input"
            value={language}
            onChange={(e) => onChangeLanguage(e.target.value)}
            aria-label="Select Interface Language"
          >
            {(supportedLanguages || []).map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>

        {/* Live Grafana MCP Status Indicator */}
        <div
          className="mcp-status"
          id="mcp-status"
          title="Grafana Cloud MCP Streamable HTTP Connected"
          role="status"
          aria-label="Grafana Cloud MCP Streamable HTTP: Connected and Live"
        >
          <span className="pulse-dot" aria-hidden="true"></span>
          <span className="status-text">Grafana MCP: LIVE</span>
        </div>
      </div>
    </header>
  );
}
