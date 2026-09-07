import React, { useState, useEffect, useRef } from 'react';
import { useAuth, CREW_QUICK_LOGINS } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export function AuthModal({ isOpen, onClose }) {
  const { user, loginWithPersona, switchRole } = useAuth();
  const { setCinemaTheme } = useTheme();
  const [tab, setTab] = useState('personas');
  const [email, setEmail] = useState('director@thiraikuzhu.ai');
  const [password, setPassword] = useState('••••••••');
  const modalRef = useRef(null);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleSelectPersona = (crew) => {
    loginWithPersona(crew.id, crew.title, crew.dept);
    if (crew.theme) {
      setCinemaTheme(crew.theme);
    }
    onClose();
  };

  const handleAdminLogin = () => {
    switchRole('admin');
    setCinemaTheme('director-noir');
    onClose();
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="auth-modal-title"
      className="auth-modal-backdrop"
      onClick={onClose}
    >
      <div
        ref={modalRef}
        className="auth-modal-dialog"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="auth-modal-header">
          <div className="auth-header-title-group">
            <h2 id="auth-modal-title" className="auth-title">
              <span>🔐</span> Studio IAM & Crew Persona Login
            </h2>
            <p className="auth-subtitle">
              Role-Based Least Privilege Access & Firebase Authentication
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close modal"
            className="auth-close-btn"
          >
            ✕
          </button>
        </div>

        {/* Tab switcher */}
        <div className="auth-tab-bar" role="tablist">
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'personas'}
            onClick={() => setTab('personas')}
            className={`auth-tab-btn ${tab === 'personas' ? 'active' : ''}`}
          >
            🎭 1-Click Crew Persona Login
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'firebase'}
            onClick={() => setTab('firebase')}
            className={`auth-tab-btn ${tab === 'firebase' ? 'active' : ''}`}
          >
            🔥 Firebase Auth Sign In
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'iam_info'}
            onClick={() => setTab('iam_info')}
            className={`auth-tab-btn ${tab === 'iam_info' ? 'active' : ''}`}
          >
            ☁️ GCP IAM Architecture
          </button>
        </div>

        {/* Tab 1: Crew Persona Quick Login Grid */}
        {tab === 'personas' && (
          <div className="auth-tab-content">
            <p className="auth-helper-text">
              Select any crew persona to instantly assume their IAM role, dashboard view, and custom cinema theme:
            </p>
            <div className="crew-login-grid">
              {CREW_QUICK_LOGINS.map((crew) => {
                const isActive = user?.crewPersonaId === crew.id;
                return (
                  <button
                    key={crew.id}
                    type="button"
                    onClick={() => handleSelectPersona(crew)}
                    className={`crew-card-btn ${isActive ? 'active-crew-btn' : ''}`}
                  >
                    <span className="crew-icon">{crew.icon}</span>
                    <span className="crew-title">{crew.title}</span>
                    <span className="crew-id-tag">{crew.id}</span>
                  </button>
                );
              })}
            </div>

            <div className="auth-footer-bar">
              <span className="auth-footer-prompt">Need full administrative access?</span>
              <button
                type="button"
                onClick={handleAdminLogin}
                className="btn-admin-login"
              >
                👑 Log in as Studio Head (Admin)
              </button>
            </div>
          </div>
        )}

        {/* Tab 2: Standard Firebase Auth Simulation */}
        {tab === 'firebase' && (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              switchRole('admin');
              onClose();
            }}
            className="auth-form"
          >
            <div className="auth-field-group">
              <label htmlFor="auth-email-input">Production Email</label>
              <input
                id="auth-email-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="auth-text-input"
                required
              />
            </div>
            <div className="auth-field-group">
              <label htmlFor="auth-pwd-input">Studio Password</label>
              <input
                id="auth-pwd-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="auth-text-input"
                required
              />
            </div>
            <div className="auth-notice-box">
              ℹ️ Firebase Auth connected: Workload Identity Federation & GCP Secret Manager enforced for all authentication tokens.
            </div>
            <button
              type="submit"
              className="btn-firebase-submit"
            >
              Sign In via Firebase Auth
            </button>
          </form>
        )}

        {/* Tab 3: GCP IAM Architecture Details */}
        {tab === 'iam_info' && (
          <div className="auth-tab-content">
            <div className="iam-explainer-card">
              <h4>🛡️ Do we need 369 separate IAM identities in Google Cloud?</h4>
              <p className="iam-bold-answer">
                <strong>NO.</strong> Creating 369 separate GCP IAM users is an anti-pattern that violates the principle of least privilege and hits Google Cloud IAM policy member limits.
              </p>
              <div className="iam-features-list">
                <div className="iam-feature-row">
                  <span className="feature-bullet">1.</span>
                  <div>
                    <strong>Workload Identity Federation & Custom Claims:</strong>
                    <p>Each crew member authenticates via Firebase Auth. The issued JWT token contains signed Custom Claims (e.g. <code>band: &apos;E&apos;, persona: &apos;E01&apos;, can_block: true</code>).</p>
                  </div>
                </div>
                <div className="iam-feature-row">
                  <span className="feature-bullet">2.</span>
                  <div>
                    <strong>3 Core Google Cloud Service Accounts:</strong>
                    <p>All 369 personas map into 3 least-privilege service accounts: <code>sa-studio-admin</code>, <code>sa-studio-crew</code>, and <code>sa-studio-guest</code>.</p>
                  </div>
                </div>
                <div className="iam-feature-row">
                  <span className="feature-bullet">3.</span>
                  <div>
                    <strong>Fine-Grained Runtime Tool ACLs:</strong>
                    <p>Backend Pydantic registry enforces bind-time tool allow/deny lists (e.g. ffmpeg, GPU transcode, Grafana annotation) directly per persona ID.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
