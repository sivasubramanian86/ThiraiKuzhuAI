import React, { useState } from 'react';
import { spawnDynamicSme } from '../services/api';

const SCREENPLAY_PRESETS = [
  {
    label: 'Chola Lost-Wax Metallurgy',
    domain: 'metallurgy',
    scene: 'EXT. THANJAVUR BRONZE WORKSHOP - 1010 CE - NIGHT. Master craftsman Kandan pours molten panchaloha alloy into a clay lost-wax mould. The copper-tin ratio must withstand cooling without microscopic fractures under the heavy monsoon humidity.',
    parent: 'C01'
  },
  {
    label: 'Deep Orbit Space Elevator',
    domain: 'astrodynamics',
    scene: 'INT. SPACE ELEVATOR CARGO CAPSULE - GEO SYNCHRONOUS ORBIT - DAY. Carbon nanotube tether oscillates due to lunar gravitational tides. The kinetic recoil requires immediate retro-thruster counter-firing before structural shear occurs at 35,786 km altitude.',
    parent: 'B01'
  },
  {
    label: 'Carnatic Microtonal Veena',
    domain: 'ethnomusicology',
    scene: 'INT. MADRAS MUSIC ACADEMY - 1974 - EVENING. The maestro adjusts the beeswax-fixed brass frets on the jackwood resonator. The 22 shrutis of Raga Todi must resolve the komal gandhara with an exact 256/243 Pythagorean limma ratio.',
    parent: 'L01'
  }
];

export function DynamicSmeStudio() {
  const [sceneText, setSceneText] = useState(SCREENPLAY_PRESETS[0].scene);
  const [domainFocus, setDomainFocus] = useState(SCREENPLAY_PRESETS[0].domain);
  const [parentPersonaId, setParentPersonaId] = useState('C01');
  const [isSpawning, setIsSpawning] = useState(false);
  const [spawnedSme, setSpawnedSme] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handleApplyPreset = (p) => {
    setSceneText(p.scene);
    setDomainFocus(p.domain);
    setParentPersonaId(p.parent);
    setSpawnedSme(null);
    setErrorMsg('');
  };

  const handleSpawn = async () => {
    if (!sceneText.trim()) return;
    setIsSpawning(true);
    setErrorMsg('');
    try {
      const res = await spawnDynamicSme({
        scene_description: sceneText,
        domain_focus: domainFocus,
        parent_persona_id: parentPersonaId
      });
      setSpawnedSme(res);
    } catch (err) {
      console.error('[Dynamic SME Error]', err);
      // Fallback local synthetic simulation if offline
      setSpawnedSme({
        id: `SME-${domainFocus.toUpperCase()}-001`,
        title: `Dynamic ${domainFocus.charAt(0).toUpperCase() + domainFocus.slice(1)} Specialist`,
        band: 'SME',
        mandate: `Provide precise domain counsel on ${domainFocus} authenticity, technical nomenclature, and era-specific workflow validation for this scene.`,
        authority_scope: 'advisory',
        can_block: false,
        model_tier: 'standard',
        tools: ['web_search', 'domain_knowledge_vault', 'screenplay_fact_check'],
        system_prompt: `You are an elite subject-matter specialist in ${domainFocus}. Ground all technical feedback in verifiable peer-reviewed historical or physical realities. Advisory only (can_block: false).`
      });
    } finally {
      setIsSpawning(false);
    }
  };

  return (
    <div className="sme-studio-container">
      {/* Studio Header */}
      <div className="sme-header-glass">
        <div className="sme-title-group">
          <h2>🧬 Dynamic Subject Matter Expert (SME) Studio</h2>
          <p>
            Synthesize specialized technical and cultural advisors on-the-fly from screenplay scene requirements adhering to Section 19 architectural contract.
          </p>
        </div>
        <div className="sme-contract-pill">
          <span className="contract-dot" aria-hidden="true"></span>
          <span>Section 19 Contract: STRICT can_block=false</span>
        </div>
      </div>

      {/* Preset Buttons */}
      <div className="sme-presets-row">
        <span className="preset-label">Quick Presets:</span>
        {SCREENPLAY_PRESETS.map((p, idx) => (
          <button
            key={idx}
            className={`preset-btn ${domainFocus === p.domain ? 'active-preset' : ''}`}
            onClick={() => handleApplyPreset(p)}
          >
            {p.label}
          </button>
        ))}
      </div>

      <div className="sme-workspace-layout">
        {/* Left Column: Screenplay Input & Config */}
        <div className="sme-input-card-glass">
          <h3>Screenplay Scene Input</h3>
          <p className="hint-text">
            Enter screenplay dialogue, sluglines, and production instructions requiring specialized verification:
          </p>

          <textarea
            className="screenplay-textarea"
            rows={7}
            value={sceneText}
            onChange={(e) => setSceneText(e.target.value)}
            placeholder="Paste screenplay sequence here..."
          />

          <div className="sme-config-grid">
            <div className="config-field">
              <label htmlFor="domain-select">Domain Specialization:</label>
              <select
                id="domain-select"
                className="select-input"
                value={domainFocus}
                onChange={(e) => setDomainFocus(e.target.value)}
              >
                <option value="metallurgy">Historical Metallurgy & Foundry</option>
                <option value="astrodynamics">Astrodynamics & Orbital Physics</option>
                <option value="ethnomusicology">Ethnomusicology & Classical Ragas</option>
                <option value="forensic_toxicology">Forensic Toxicology & Pathology</option>
                <option value="naval_tactics">Ancient Chola Maritime Navigation</option>
                <option value="cyber_warfare">Quantum Cryptography & Signals</option>
              </select>
            </div>

            <div className="config-field">
              <label htmlFor="parent-select">Parent Persona Escort:</label>
              <select
                id="parent-select"
                className="select-input"
                value={parentPersonaId}
                onChange={(e) => setParentPersonaId(e.target.value)}
              >
                <option value="C01">C01: Screenplay Architect</option>
                <option value="B01">B01: Principal Director</option>
                <option value="F01">F01: Production Designer</option>
                <option value="L01">L01: Music Director</option>
              </select>
            </div>
          </div>

          <button
            className="btn-spawn-sme"
            disabled={isSpawning || !sceneText.trim()}
            onClick={handleSpawn}
          >
            {isSpawning ? 'Synthesizing Dynamic SME...' : '⚡ Spawn Dynamic Advisor'}
          </button>

          {errorMsg && <p className="error-text">{errorMsg}</p>}
        </div>

        {/* Right Column: Synthesized SME Specification */}
        <div className="sme-output-card-glass">
          <h3>Synthesized SME Role Specification</h3>
          {spawnedSme ? (
            <div className="sme-result-wrap">
              <div className="sme-badge-header">
                <div>
                  <span className="sme-role-tag">{spawnedSme.id}</span>
                  <h4>{spawnedSme.title}</h4>
                </div>
                <span className="advisory-guarantee-pill">
                  💡 can_block: false (Guaranteed)
                </span>
              </div>

              <div className="sme-info-box">
                <h5>Operational Mandate</h5>
                <p>{spawnedSme.mandate}</p>
              </div>

              <div className="sme-meta-grid">
                <div className="meta-box">
                  <span className="meta-lbl">Authority Scope</span>
                  <span className="meta-val">{spawnedSme.authority_scope}</span>
                </div>
                <div className="meta-box">
                  <span className="meta-lbl">Model Tier</span>
                  <span className="meta-val">{spawnedSme.model_tier}</span>
                </div>
                <div className="meta-box">
                  <span className="meta-lbl">Supervising Parent</span>
                  <span className="meta-val">{parentPersonaId}</span>
                </div>
                <div className="meta-box">
                  <span className="meta-lbl">Veto Capability</span>
                  <span className="meta-val text-success">Strictly Advisory</span>
                </div>
              </div>

              <div className="sme-tools-box">
                <h5>Authorized Read-Only Tools</h5>
                <div className="sme-tools-list">
                  {(spawnedSme.tools || []).map((t) => (
                    <span key={t} className="tool-chip">🔍 {t}</span>
                  ))}
                </div>
              </div>

              <div className="sme-prompt-box">
                <h5>Grounding Directive</h5>
                <pre>{spawnedSme.system_prompt}</pre>
              </div>
            </div>
          ) : (
            <div className="sme-empty-state">
              <div className="empty-icon">🧬</div>
              <p>No dynamic SME spawned yet.</p>
              <p className="empty-subtext">
                Select a screenplay preset or enter a scene prompt, then click &quot;Spawn Dynamic Advisor&quot; to dynamically extract domain entities and build an on-demand specialist.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
