import React, { useState } from 'react';

const SHIELD_TABS = [
  { id: 'piracy', label: '🏴‍☠️ Piracy & Watermark Detection' },
  { id: 'deepfake', label: '🔍 AI Deepfake & SynthID Provenance' },
  { id: 'patent', label: '⚖️ Patent & Copyright Protection' }
];

export function ContentShieldStudio() {
  const [activeTab, setActiveTab] = useState('piracy');
  const [isRunningAudit, setIsRunningAudit] = useState(false);
  const [auditResults, setAuditResults] = useState(null);

  const handleRunAudit = () => {
    setIsRunningAudit(true);
    setAuditResults(null);
    setTimeout(() => {
      setIsRunningAudit(false);
      if (activeTab === 'piracy') {
        setAuditResults({
          title: 'Piracy & Watermark Telemetry Report',
          status: 'SECURE',
          watermark_payload: 'THIRAI-WM-2026-B01-STAGE_A',
          survivability: '99.4% Robustness against H.265 Transcode, Cropping & Audio Highpass',
          active_leak_probes: 14,
          leaks_detected: 0,
          swarm_status: 'No matching forensic hashes in unauthorized p2p networks.'
        });
      } else if (activeTab === 'deepfake') {
        setAuditResults({
          title: 'AI Synthetic Content & C2PA Provenance Report',
          status: 'AUTHENTIC',
          authenticity_score: '99.8% Certified Human Performance',
          c2pa_manifest_id: 'urn:c2pa:thirai:2026:camera_sensor_arri_09914',
          signature_valid: true,
          face_swap_risk: 'LOW (0.02) — Natural micro-expression & ocular jitter confirmed',
          voice_clone_risk: 'LOW (0.01) — Natural vocal tract biomechanics validated'
        });
      } else {
        setAuditResults({
          title: 'Patent & Copyright Collision Clearance',
          status: 'CLEARED',
          copyright_similarity_index: '0.04% (Well below 15% infringement threshold)',
          wipo_patent_search: '0 blocking cinema staging utility patents identified',
          melodic_plagiarism_risk: 'CLEARED — Chord progression registered with ASCAP/IPRS',
          cbfc_compliance: 'U/A 13+ Projected Certification with zero mandatory cuts'
        });
      }
    }, 900);
  };

  return (
    <div className="content-shield-container">
      {/* Header */}
      <div className="obs-header-glass">
        <div className="obs-title-group">
          <h2>🛡️ Content Shield & IP Governance Studio</h2>
          <p>
            Autonomous anti-piracy leak tracking, Google SynthID watermark detection, AI deepfake provenance verification, and patent/copyright collision clearance.
          </p>
        </div>
        <div className="mcp-badge-pill">
          <span className="pulse-dot" aria-hidden="true"></span>
          <span>SynthID & C2PA Cryptographic Ledger Active</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="shield-tabs-bar" role="tablist">
        {SHIELD_TABS.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            aria-selected={activeTab === tab.id}
            className={`shield-tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => {
              setActiveTab(tab.id);
              setAuditResults(null);
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Workspace layout */}
      <div className="shield-workspace-grid">
        {/* Left Column: Interactive Telemetry & Controls */}
        <div className="shield-card-glass">
          {activeTab === 'piracy' && (
            <div className="watermark-demo-box">
              <h3>SynthID Forensic Watermarking & Leak Guard</h3>
              <p className="hint-text">
                Embeds invisible psychoacoustic and perceptual frequency watermarks into master dailies and screener links to trace unauthorized leaks back to the exact recipient.
              </p>

              <div className="shield-meta-row">
                <span>Active Watermark ID:</span>
                <strong className="code-text">THIRAI-WM-2026-B01-STAGE_A</strong>
              </div>
              <div className="shield-meta-row">
                <span>Robustness Profile:</span>
                <span>Survives 720p Re-encoding, 1.5x Speedup & Camcorder Capture</span>
              </div>
              <div className="shield-meta-row">
                <span>Dark Web & OTT Swarm Prober:</span>
                <span className="text-success">● 14 BitTorrent & Streaming Nodes Monitored</span>
              </div>
            </div>
          )}

          {activeTab === 'deepfake' && (
            <div className="deepfake-demo-box">
              <h3>AI Deepfake Detection & C2PA Provenance Manifest</h3>
              <p className="hint-text">
                Cryptographically validates camera hardware signatures and detects unauthorized generative AI face-swaps or cloned voice synthesis in actor dailies.
              </p>

              <div className="shield-meta-row">
                <span>C2PA Camera Certificate:</span>
                <span className="code-text">ARRI Alexa 65 Hard-Key #88219</span>
              </div>
              <div className="shield-meta-row">
                <span>SynthID Watermark Verification:</span>
                <span className="text-success">Verified Original In-Camera Capture</span>
              </div>

              <h4>Cryptographic C2PA Manifest (Live Inspection):</h4>
              <pre className="c2pa-manifest-preview">
{`{
  "c2pa_version": "2.1.0",
  "claim_generator": "ThiraiKuzhuAI_ContentShield/1.0",
  "title": "Scene 12 Take 4 Master Rush",
  "assertions": [
    {
      "label": "c2pa.actions",
      "data": { "actions": [{ "action": "c2pa.created", "softwareAgent": "ARRI Alexa 65 Firmware 7.2" }] }
    },
    {
      "label": "c2pa.ai_detection",
      "data": { "synthid_score": 0.001, "is_generative": false, "biometric_valid": true }
    }
  ],
  "signature": "ES256_RSA_HARDWARE_KEY_VALID"
}`}
              </pre>
            </div>
          )}

          {activeTab === 'patent' && (
            <div className="patent-demo-box">
              <h3>Patent & Copyright Collision Clearance</h3>
              <p className="hint-text">
                Cross-references screenplay narrative arcs, novel filming apparatus rigs, and musical scores against global patent, copyright, and censor databases.
              </p>

              <div className="shield-meta-row">
                <span>Global Patent Registers:</span>
                <span>WIPO, USPTO & Indian Patent Office Cleared</span>
              </div>
              <div className="shield-meta-row">
                <span>Musical Score Infringement Engine:</span>
                <span>Scans 12M Recorded Tracks (ASCAP, BMI, IPRS)</span>
              </div>
              <div className="shield-meta-row">
                <span>CBFC / MPAA Censor Prediction:</span>
                <span>AI Automated Violence & Cultural Sensitivity Screening</span>
              </div>
            </div>
          )}

          <button
            className="btn-primary"
            disabled={isRunningAudit}
            onClick={handleRunAudit}
          >
            {isRunningAudit ? 'Scanning Global Repositories...' : '🛡️ Run Real-Time IP & Security Audit'}
          </button>
        </div>

        {/* Right Column: Live Audit Results */}
        <div className="shield-card-glass">
          <h3>Security & Rights Audit Report</h3>
          {auditResults ? (
            <div className="audit-results-card">
              <div className="audit-header-badge">
                <h4>{auditResults.title}</h4>
                <span className="pill-yes">{auditResults.status}</span>
              </div>

              {activeTab === 'piracy' && (
                <div className="audit-details-list">
                  <p><strong>Forensic Watermark:</strong> <code>{auditResults.watermark_payload}</code></p>
                  <p><strong>Anti-Tamper Integrity:</strong> {auditResults.survivability}</p>
                  <p><strong>Active Leak Sensors:</strong> {auditResults.active_leak_probes} Regional Web Crawlers</p>
                  <p><strong>Swarm Status:</strong> <span className="text-success">{auditResults.swarm_status}</span></p>
                </div>
              )}

              {activeTab === 'deepfake' && (
                <div className="audit-details-list">
                  <p><strong>Human Performance Authenticity:</strong> <span className="text-success">{auditResults.authenticity_score}</span></p>
                  <p><strong>Hardware Signature:</strong> <code>{auditResults.c2pa_manifest_id}</code></p>
                  <p><strong>Face-Swap Risk:</strong> {auditResults.face_swap_risk}</p>
                  <p><strong>Voice Clone Risk:</strong> {auditResults.voice_clone_risk}</p>
                </div>
              )}

              {activeTab === 'patent' && (
                <div className="audit-details-list">
                  <p><strong>Copyright Similarity:</strong> <span className="text-success">{auditResults.copyright_similarity_index}</span></p>
                  <p><strong>Rig Staging Patents:</strong> {auditResults.wipo_patent_search}</p>
                  <p><strong>Melodic Plagiarism Risk:</strong> <span className="text-success">{auditResults.melodic_plagiarism_risk}</span></p>
                  <p><strong>Censor Board Forecast:</strong> {auditResults.cbfc_compliance}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="empty-state-card text-center p-6 text-slate-400">
              <div className="text-4xl mb-2">🔒</div>
              <p>No active audit in progress.</p>
              <p className="text-xs text-slate-500 mt-1">
                Click "Run Real-Time IP & Security Audit" to perform full spectrum forensic analysis.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
