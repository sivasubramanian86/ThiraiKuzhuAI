import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { AuthModal } from './AuthModal';

const NAV_ITEMS = [
  { id: 'control_room', label: 'Control Room', icon: '🎬', badge: 'LIVE' },
  { id: 'crew_lounge', label: 'Crew Lounge', icon: '👥', badge: '369' },
  { id: 'anime_vault', label: 'Anime Vault', icon: '🎌', badge: 'OS Data' },
  { id: 'art_director', label: 'Art Department', icon: '🎨', badge: 'Imagen 3' },
  { id: 'sme_studio', label: 'Dynamic SME', icon: '🧬', badge: 'Sec 19' },
  { id: 'antagonist_lab', label: 'Red-Team Lab', icon: '🛡️', badge: 'Chaos' },
  { id: 'multimodal_studio', label: 'MultiModal Studio', icon: '👁️', badge: 'Veo/Lyria' },
  { id: 'content_shield', label: 'IP & Content Shield', icon: '🔒', badge: 'SynthID' },
  { id: 'observability', label: 'Grafana Telemetry', icon: '📊', badge: 'MCP' },
  { id: 'faq_help', label: 'FAQ & Help', icon: '❓' },
  { id: 'about', label: 'About', icon: 'ℹ️' },
  { id: 'settings', label: 'Settings', icon: '⚙️' }
];

export function AppShell({
  activeTab,
  onTabChange,
  _projects,
  _selectedProject,
  _onSelectProject,
  criScore,
  language,
  onChangeLanguage,
  supportedLanguages,
  i18n = {},
  children
}) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  const { currentUser, userRole, currentPersona } = useAuth();
  const { mode, toggleMode, cinemaTheme, setCinemaTheme, CINEMA_PALETTES } = useTheme();

  const navItems = [
    { id: 'control_room', label: i18n.navControlRoom || 'Control Room', icon: '🎬', badge: 'LIVE' },
    { id: 'crew_lounge', label: i18n.navCrewLounge || 'Crew Lounge', icon: '👥', badge: '369' },
    { id: 'anime_vault', label: i18n.navAnimeVault || 'Anime Vault', icon: '🎌', badge: 'OS Data' },
    { id: 'art_director', label: i18n.navArtDirector || 'Art Department', icon: '🎨', badge: 'Imagen 3' },
    { id: 'sme_studio', label: i18n.navSmeStudio || 'Dynamic SME', icon: '🧬', badge: 'Sec 19' },
    { id: 'antagonist_lab', label: i18n.navAntagonistLab || 'Red-Team Lab', icon: '🛡️', badge: 'Chaos' },
    { id: 'multimodal_studio', label: i18n.navMultimodalStudio || 'MultiModal Studio', icon: '👁️', badge: 'Veo/Lyria' },
    { id: 'content_shield', label: i18n.navContentShield || 'IP & Content Shield', icon: '🔒', badge: 'SynthID' },
    { id: 'observability', label: i18n.navObservability || 'Grafana Telemetry', icon: '📊', badge: 'MCP' },
    { id: 'faq_help', label: i18n.navFaqHelp || 'FAQ & Help', icon: '❓' },
    { id: 'about', label: i18n.navAbout || 'About', icon: 'ℹ️' },
    { id: 'settings', label: i18n.navSettings || 'Settings', icon: '⚙️' }
  ];

  return (
    <div className="app-shell-container" data-sidebar-collapsed={sidebarCollapsed}>
      {/* Top Header Bar */}
      <header className="topbar" role="banner">
        <div className="topbar-left-cluster">
          <button
            className="sidebar-toggle-btn"
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            aria-label={sidebarCollapsed ? 'Expand navigation sidebar' : 'Collapse navigation sidebar'}
            title="Toggle Sidebar"
          >
            ☰
          </button>

          <div className="brand-cluster">
            <div className="brand-logo" aria-hidden="true">🎬</div>
            <div>
              <h1 className="brand-title">
                Thirai Kuzhu AI <span className="tamil-title">(திரை குழு AI)</span>
              </h1>
              <p className="brand-subtitle">{i18n.brandSubtitle || "Autonomous Multi-Agent Cinema Production OS"}</p>
            </div>
          </div>
        </div>

        <div className="header-controls">
          {/* Active Production Slate (No external movie references) */}
          <div className="studio-slate-badge" title="Active Studio Stage & Scene Slate">
            <span className="slate-clapper" aria-hidden="true">🎬</span>
            <div className="slate-info">
              <span className="slate-label">{i18n.studioStageA || 'STUDIO STAGE A'}</span>
              <span className="slate-track">{i18n.liveProduction || 'Live Production Stream'}</span>
            </div>
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

          {/* Theme Quick Selector */}
          <div className="control-group theme-quick-group">
            <button
              className="mode-icon-btn"
              onClick={toggleMode}
              title={`Switch to ${mode === 'dark' ? 'Light' : 'Dark'} Mode`}
              aria-label="Toggle Theme Mode"
            >
              {mode === 'dark' ? '🌙' : '☀️'}
            </button>
            <select
              className="select-input select-theme-mini"
              value={cinemaTheme}
              onChange={(e) => setCinemaTheme(e.target.value)}
              aria-label="Select Cinema Palette"
              title="Cinema Color Palette"
            >
              {Object.entries(CINEMA_PALETTES || {}).map(([k, pal]) => (
                <option key={k} value={k}>{pal.name}</option>
              ))}
            </select>
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

          {/* User / Persona Login Quick Badge */}
          <button
            className="user-profile-badge-btn"
            onClick={() => setIsAuthModalOpen(true)}
            title="Switch Crew Persona or Sign In"
            aria-label="User and Persona Profile Switcher"
          >
            <div className="user-avatar-mini">
              {currentUser?.photoURL ? (
                <img src={currentUser.photoURL} alt="" />
              ) : (
                <span>🎭</span>
              )}
            </div>
            <div className="user-persona-names">
              <span className="user-role-label">
                {currentPersona ? currentPersona.id : userRole}
              </span>
              <span className="user-name-label">
                {currentPersona ? currentPersona.title : (currentUser?.displayName || 'Sign In')}
              </span>
            </div>
          </button>

          {/* Live Grafana MCP Status Indicator */}
          <div
            className="mcp-status"
            id="mcp-status"
            title="Grafana Cloud MCP Streamable HTTP Connected"
            role="status"
            aria-label="Grafana Cloud MCP Streamable HTTP: Connected and Live"
          >
            <span className="pulse-dot" aria-hidden="true"></span>
            <span className="status-text">{i18n.grafanaMcpLive || 'Grafana MCP: LIVE'}</span>
          </div>
        </div>
      </header>

      {/* Body with Sidebar and Main Content */}
      <div className="app-shell-body">
        {/* Collapsible Left Navigation Sidebar */}
        <aside
          className={`app-sidebar-nav ${sidebarCollapsed ? 'collapsed' : ''}`}
          role="navigation"
          aria-label="Studio Main Navigation"
        >
          <div className="sidebar-nav-list">
            {navItems.map((item) => {
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  className={`nav-tab-item ${isActive ? 'active' : ''}`}
                  onClick={() => onTabChange(item.id)}
                  title={item.label}
                  role="tab"
                  aria-selected={isActive}
                >
                  <span className="nav-icon" aria-hidden="true">{item.icon}</span>
                  {!sidebarCollapsed && <span className="nav-label">{item.label}</span>}
                  {!sidebarCollapsed && item.badge && (
                    <span className="nav-badge-pill">{item.badge}</span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Sidebar Footer: Active Crew Persona Status */}
          <div className="sidebar-footer-card">
            <div className="arrival-status-row">
              <span className="arrival-dot" aria-hidden="true"></span>
              {!sidebarCollapsed && (
                <span className="arrival-text">Arrival: On-Set Verified</span>
              )}
            </div>
            {!sidebarCollapsed && currentPersona && (
              <div className="active-persona-snippet">
                <span className="persona-id-bubble">{currentPersona.id}</span>
                <span className="persona-name-snip">{currentPersona.title}</span>
              </div>
            )}
          </div>
        </aside>

        {/* Main Content Workspace */}
        <main className="app-workspace-content" role="main">
          {children}
        </main>
      </div>

      {/* Auth & Persona Switcher Modal */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
      />
    </div>
  );
}
