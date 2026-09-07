import React, { useState } from 'react';
import { runAntagonistSimulation } from '../services/api';

const ANTAGONISTS = [
  {
    id: 'ANTG01',
    title: 'Schedule Breaker',
    badge: '⏳ Chaos Logistics',
    mandate: 'Stress-tests call sheets and critical path schedules against cascading delays, talent unavailability, and logistical breakdown.',
    attack_vectors: ['Cast Date Collision', 'Location Permit Revocation', 'Equipment Transit Stall']
  },
  {
    id: 'ANTG02',
    title: 'Copyright Infringement Attacker',
    badge: '⚖️ IP Litigation',
    mandate: 'Simulates hostile copyright, trademark, and likeness claims against screenplay sequences, melodies, and prop designs.',
    attack_vectors: ['Melodic Chord Similarity', 'Screenplay Premise Plagiarism', 'Prop Trademark Infringement']
  },
  {
    id: 'ANTG03',
    title: 'Sceptical Film Critic',
    badge: '🖋️ Ruthless Reviewer',
    mandate: 'Relentlessly interrogates narrative logic, character motivation holes, pacing lulls, and genre cliches before shooting.',
    attack_vectors: ['Act II Pacing Collapse', 'Exposition Monologue Overload', 'Deus Ex Machina Climax']
  },
  {
    id: 'ANTG04',
    title: 'Piracy & Exfiltration Simulator',
    badge: '🏴‍☠️ Digital Leak',
    mandate: 'Probes daily screening links, post-production render farms, and subtitle pipelines for leak vulnerabilities.',
    attack_vectors: ['Invisible Watermark Removal', 'Unencrypted Dailies Upload', 'Pre-Release Screenplay Leak']
  },
  {
    id: 'ANTG05',
    title: 'Force Majeure Weather Agent',
    badge: '⛈️ Environmental Hazard',
    mandate: 'Simulates catastrophic weather events, sudden monsoons, and extreme environmental threats to open-air productions.',
    attack_vectors: ['Catastrophic Set Flooding', 'Lightning Strike on Crane', 'Heatstroke Warning for Extras']
  }
];

export function AntagonistLab() {
  const [selectedAntagonist, setSelectedAntagonist] = useState(ANTAGONISTS[0]);
  const [targetProduction, setTargetProduction] = useState('Chronicles of Surya: The Solar Gate');
  const [attackVector, setAttackVector] = useState(ANTAGONISTS[0].attack_vectors[0]);
  const [intensity, setIntensity] = useState('HIGH');
  const [isSimulating, setIsSimulating] = useState(false);
  const [simReport, setSimReport] = useState(null);

  const handleSelectAntagonist = (antg) => {
    setSelectedAntagonist(antg);
    setAttackVector(antg.attack_vectors[0]);
    setSimReport(null);
  };

  const handleRunSimulation = async () => {
    setIsSimulating(true);
    setSimReport(null);

    try {
      const res = await runAntagonistSimulation({
        antagonist_id: selectedAntagonist.id,
        target_production: targetProduction,
        attack_vector: attackVector,
        simulation_intensity: intensity
      });
      setSimReport(res);
    } catch (err) {
      console.warn('[Antagonist Simulation Fallback]', err);
      // Local fallback simulation report
      setSimReport({
        antagonist_id: selectedAntagonist.id,
        target_production: targetProduction,
        attack_vector: attackVector,
        intensity: intensity,
        impact_score: intensity === 'EXTREME' ? 92 : intensity === 'HIGH' ? 76 : 54,
        box_office_risk_usd: intensity === 'EXTREME' ? 85000 : 38000,
        breached_bands: ['Band A: Executive', 'Band E: Camera', 'Band O: Legal'],
        attack_log: [
          `[T+00:00] Injected ${attackVector} into ${targetProduction} sequence schedule.`,
          `[T+00:03] Detected critical vulnerability: Buffer margin less than 48 hours.`,
          `[T+00:07] Cascading impact: 14 crew departments stalled without clear contingency.`
        ],
        counter_measures: [
          'Pre-book 2 alternate weather cover indoor studio sets.',
          'Execute digital rights indemnity escrow with primary distributor.',
          'Activate dynamic backup scheduling buffer across primary cast members.'
        ]
      });
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="antagonist-lab-container">
      {/* Header */}
      <div className="antagonist-header-glass">
        <div className="antagonist-title-group">
          <h2>🛡️ Red-Team Adversarial Antagonist Lab</h2>
          <p>
            Subject production plans, schedules, scripts, and media workflows to ruthless synthetic attack vectors to discover vulnerabilities before cameras roll.
          </p>
        </div>
        <div className="lab-badge-pill">
          <span>5 Adversarial Red-Team Personas Active</span>
        </div>
      </div>

      {/* Antagonists Grid */}
      <div className="antagonist-selection-grid">
        {ANTAGONISTS.map((antg) => {
          const isSelected = selectedAntagonist.id === antg.id;
          return (
            <div
              key={antg.id}
              className={`antagonist-card-glass ${isSelected ? 'selected-antagonist' : ''}`}
              onClick={() => handleSelectAntagonist(antg)}
            >
              <div className="antg-header">
                <span className="antg-badge">{antg.badge}</span>
                <span className="antg-id">{antg.id}</span>
              </div>
              <h4>{antg.title}</h4>
              <p className="antg-mandate">{antg.mandate}</p>
              <div className="vectors-mini-list">
                {antg.attack_vectors.map((vec, idx) => (
                  <span key={idx} className="vector-pill">⚡ {vec}</span>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Simulation Controls & Output */}
      <div className="sim-control-workspace">
        {/* Controls Card */}
        <div className="sim-config-card-glass">
          <h3>Simulation Attack Parameters</h3>
          <div className="sim-config-form">
            <div className="form-group">
              <label htmlFor="target-prod">Target Production:</label>
              <select
                id="target-prod"
                className="select-input"
                value={targetProduction}
                onChange={(e) => setTargetProduction(e.target.value)}
              >
                <option value="Chronicles of Surya: The Solar Gate">Chronicles of Surya: The Solar Gate</option>
                <option value="Abyssal Frontier: Deep Recon">Abyssal Frontier: Deep Recon</option>
                <option value="Whisper of the Crane: Wuxia Chronicles">Whisper of the Crane: Wuxia Chronicles</option>
              </select>

            </div>

            <div className="form-group">
              <label htmlFor="attack-vec">Primary Attack Vector:</label>
              <select
                id="attack-vec"
                className="select-input"
                value={attackVector}
                onChange={(e) => setAttackVector(e.target.value)}
              >
                {selectedAntagonist.attack_vectors.map((vec, idx) => (
                  <option key={idx} value={vec}>{vec}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="intensity-select">Simulation Intensity:</label>
              <select
                id="intensity-select"
                className="select-input"
                value={intensity}
                onChange={(e) => setIntensity(e.target.value)}
              >
                <option value="MODERATE">Moderate (Normal Studio Risk)</option>
                <option value="HIGH">High (Severe Disruption)</option>
                <option value="EXTREME">Extreme (Catastrophic Black Swan)</option>
              </select>
            </div>

            <button
              className="btn-launch-attack"
              disabled={isSimulating}
              onClick={handleRunSimulation}
            >
              {isSimulating ? 'Executing Attack Simulation...' : `⚔️ Run ${selectedAntagonist.title} Attack`}
            </button>
          </div>
        </div>

        {/* Results Card */}
        <div className="sim-results-card-glass">
          <h3>Adversarial Simulation Telemetry</h3>
          {simReport ? (
            <div className="sim-report-content">
              <div className="sim-metrics-row">
                <div className="sim-metric-box">
                  <span className="metric-label">Vulnerability Score</span>
                  <span className="metric-number text-critical">{simReport.impact_score}/100</span>
                </div>
                <div className="sim-metric-box">
                  <span className="metric-label">Box Office Risk</span>
                  <span className="metric-number text-warning">
                    ${(simReport.box_office_risk_usd || 0).toLocaleString()} USD
                  </span>
                </div>
                <div className="sim-metric-box">
                  <span className="metric-label">Adversary ID</span>
                  <span className="metric-number text-accent">{simReport.antagonist_id}</span>
                </div>
              </div>

              <div className="report-section">
                <h5>Breached Studio Departments</h5>
                <div className="breached-tags-row">
                  {(simReport.breached_bands || []).map((b, idx) => (
                    <span key={idx} className="breach-tag">⚠️ {b}</span>
                  ))}
                </div>
              </div>

              <div className="report-section">
                <h5>Adversary Attack Log</h5>
                <div className="sim-attack-log">
                  {(simReport.attack_log || []).map((line, idx) => (
                    <div key={idx} className="log-line">{line}</div>
                  ))}
                </div>
              </div>

              <div className="report-section">
                <h5>🛡️ Automated Counter-Measures & Hardening</h5>
                <ul className="counter-measures-list">
                  {(simReport.counter_measures || []).map((cm, idx) => (
                    <li key={idx}>✓ {cm}</li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <div className="sim-empty-state">
              <div className="empty-shield">🛡️</div>
              <p>Ready to launch red-team attack simulation.</p>
              <p className="empty-subtext">
                Select an antagonist agent above, configure the target production and vector, and launch the adversarial stress-test.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
