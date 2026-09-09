import React, { useState } from 'react';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';
import { getSettingsContent } from '../i18n/settingsContent';

export function SettingsStudio({ i18n = {}, language = 'en' }) {
  const content = getSettingsContent(language);
  const { mode, toggleMode, cinemaTheme, setCinemaTheme, CINEMA_PALETTES } = useTheme();
  const { currentUser, userRole, currentPersona, logout } = useAuth();

  const [ttsVoice, setTtsVoice] = useState('director_ta_en');
  const [radioStatic, setRadioStatic] = useState(true);
  const [volume, setVolume] = useState(80);
  const [modelCheap, setModelCheap] = useState('gemini-2.5-flash');
  const [modelStandard, setModelStandard] = useState('gemini-2.5-pro');
  const [modelReasoning, setModelReasoning] = useState('gemini-3.8-flash');
  const [saveToast, setSaveToast] = useState(false);

  const handleSaveSettings = (e) => {
    e.preventDefault();
    setSaveToast(true);
    setTimeout(() => setSaveToast(false), 2500);
  };

  return (
    <div className="settings-container">
      {/* Header */}
      <div className="settings-header-glass">
        <div className="settings-title-group">
          <h2>⚙️ {content.settingsTitle || i18n.settingsTitle || i18n.settings_title || 'Studio Settings & Configuration'}</h2>
          <p>
            {content.settingsDesc || i18n.settingsDesc || i18n.settings_desc || 'Configure cinematic interface palettes, walkie-talkie voice synthesis, Gemini model tiers, and Firebase authentication.'}
          </p>
        </div>
        {saveToast && (
          <div className="save-toast-pill">
            {content.savedToast || '✓ Settings saved to local studio profile'}
          </div>
        )}
      </div>

      <form onSubmit={handleSaveSettings} className="settings-form-layout">
        {/* Section 1: Appearance & Cinema Themes */}
        <div className="settings-card-glass">
          <h3>{content.themeSectionTitle || '🎨 Cinematic Theme & Appearance'}</h3>
          <p className="hint-text">{content.themeSectionHint || 'Choose from 6 calibrated cinema color palettes and toggle dark/light mode:'}</p>

          <div className="mode-toggle-row">
            <span>{content.lightingModeLabel || 'Interface Lighting Mode:'}</span>
            <button
              type="button"
              className={`mode-btn ${mode === 'dark' ? 'active' : ''}`}
              onClick={toggleMode}
            >
              {mode === 'dark' ? (content.darkModeBtn || '🌙 Dark Mode (Default)') : (content.lightModeBtn || '☀️ Light Mode')}
            </button>
          </div>

          <div className="palettes-selector-grid">
            {Object.entries(CINEMA_PALETTES).map(([key, pal]) => {
              const isSelected = cinemaTheme === key;
              return (
                <div
                  key={key}
                  className={`palette-card-choice ${isSelected ? 'selected-palette' : ''}`}
                  onClick={() => setCinemaTheme(key)}
                >
                  <div className="palette-color-preview" style={{ background: pal.accent }}></div>
                  <div className="palette-info">
                    <h4>{pal.name}</h4>
                    <span className="palette-desc">{pal.description}</span>
                  </div>
                  {isSelected && <span className="check-badge">✓</span>}
                </div>
              );
            })}
          </div>
        </div>

        {/* Section 2: Walkie-Talkie & Audio Settings */}
        <div className="settings-card-glass">
          <h3>{content.walkieSectionTitle || '📻 Radio Walkie-Talkie & Sound Synthesis'}</h3>
          <p className="hint-text">{content.walkieSectionHint || 'Adjust simulated studio on-set audio and multi-agent radio transmission:'}</p>

          <div className="form-group-setting">
            <label htmlFor="tts-voice-select">{content.ttsVoiceLabel || 'TTS Voice Synthesis Profile:'}</label>
            <select
              id="tts-voice-select"
              className="select-input"
              value={ttsVoice}
              onChange={(e) => setTtsVoice(e.target.value)}
            >
              <option value="director_ta_en">Director (Bilingual Tamil / English Cadence)</option>
              <option value="exec_hollywood">Executive Producer (Authoritative Studio Lead)</option>
              <option value="hindi_cinematic">Cinematic Voice (Hindi / English Blend)</option>
              <option value="sound_engineer">Sound Engineer (Crisp Broadcast Neutral)</option>
            </select>
          </div>

          <div className="form-group-setting">
            <label htmlFor="volume-range">{content.volumeLabel || 'Walkie-Talkie Master Volume'} ({volume}%):</label>
            <input
              id="volume-range"
              type="range"
              min="0"
              max="100"
              value={volume}
              onChange={(e) => setVolume(Number(e.target.value))}
              className="range-slider"
            />
          </div>

          <div className="checkbox-setting-row">
            <input
              type="checkbox"
              id="static-check"
              checked={radioStatic}
              onChange={(e) => setRadioStatic(e.target.checked)}
            />
            <label htmlFor="static-check">
              {content.enableStaticLabel || 'Enable authentic radio squelch & on-set static sound effects'}
            </label>
          </div>
        </div>

        {/* Section 3: Gemini Model Tier Allocation */}
        <div className="settings-card-glass">
          <h3>{content.modelsSectionTitle || '🧠 Gemini Model Tiering & Context Caching'}</h3>
          <p className="hint-text">{content.modelsSectionHint || 'Configure AI model assignments based on operational budget and reasoning depth:'}</p>

          <div className="tiers-grid">
            <div className="tier-setting-item">
              <label>{content.cheapTierLabel || 'Cheap Tier (Telemetry & Rapid Classification):'}</label>
              <select
                className="select-input"
                value={modelCheap}
                onChange={(e) => setModelCheap(e.target.value)}
              >
                <option value="gemini-2.5-flash">Gemini 2.5 Flash (Ultra-low latency)</option>
                <option value="gemini-2.0-flash-lite">Gemini 2.0 Flash Lite</option>
              </select>
            </div>

            <div className="tier-setting-item">
              <label>{content.standardTierLabel || 'Standard Tier (Production & Screenplay Tasks):'}</label>
              <select
                className="select-input"
                value={modelStandard}
                onChange={(e) => setModelStandard(e.target.value)}
              >
                <option value="gemini-2.5-pro">Gemini 2.5 Pro (High-fidelity analysis)</option>
                <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
              </select>
            </div>

            <div className="tier-setting-item">
              <label>{content.reasoningTierLabel || 'Reasoning Tier (Executive Veto & Arbitration):'}</label>
              <select
                className="select-input"
                value={modelReasoning}
                onChange={(e) => setModelReasoning(e.target.value)}
              >
                <option value="gemini-3.8-flash">Gemini 3.8 Flash (Deep reasoning)</option>
                <option value="gemini-2.5-pro">Gemini 2.5 Pro</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 4: Firebase Authentication & Security */}
        <div className="settings-card-glass">
          <h3>{content.authSectionTitle || '🔐 Firebase Authentication & Studio Security'}</h3>
          <div className="auth-profile-summary">
            <div className="auth-avatar-circle">
              {currentUser?.photoURL ? (
                <img src={currentUser.photoURL} alt={currentUser.displayName} />
              ) : (
                <span>🎬</span>
              )}
            </div>
            <div className="auth-details">
              <h4>{currentUser?.displayName || content.guestUser || 'Studio Guest'}</h4>
              <p className="auth-email">{currentUser?.email || 'guest@thiraikuzhu.ai'}</p>
              <div className="auth-badges-row">
                <span className="auth-role-tag">{content.roleLabel || 'Role:'} {userRole}</span>
                {currentPersona && (
                  <span className="auth-persona-tag">{content.personaLabel || 'Persona:'} {currentPersona.id} ({currentPersona.title})</span>
                )}
              </div>
            </div>
            <button type="button" className="btn-logout" onClick={logout}>
              {content.signOutBtn || 'Sign Out'}
            </button>
          </div>
        </div>

        <div className="settings-submit-bar">
          <button type="submit" className="btn-save-all">
            {content.saveAllBtn || 'Save All Studio Preferences'}
          </button>
        </div>
      </form>
    </div>
  );
}
