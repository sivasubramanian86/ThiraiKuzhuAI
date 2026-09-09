import React from 'react';
import { getAboutContent } from '../i18n/aboutContent';

const BANDS_DATA = [
  {
    band: 'Band A',
    dept: 'Executive & Producing',
    authority: 'Greenlight, Budget, Production Insurance, Overages',
    veto: 'YES (A01)',
    vetoType: 'yes',
    model: 'Gemini 3.8 Flash (Reasoning)'
  },
  {
    band: 'Band B',
    dept: 'Direction',
    authority: 'Artistic Vision, Scene Staging, Sequence Halts',
    veto: 'YES (B01)',
    vetoType: 'yes',
    model: 'Gemini 3.8 Flash (Reasoning)'
  },
  {
    band: 'Band C',
    dept: 'Screenplay & Story',
    authority: 'Narrative Structure, Scene Dialogue, Fact-Checking',
    veto: 'NO (Advisory)',
    vetoType: 'no',
    model: 'Gemini 2.5 Pro (Standard)'
  },
  {
    band: 'Band D',
    dept: 'Casting & Talent',
    authority: 'Actor Availability, Star Riders, Intimacy Protocols',
    veto: 'YES (D01)',
    vetoType: 'yes',
    model: 'Gemini 2.5 Pro (Standard)'
  },
  {
    band: 'Band E',
    dept: 'Cinematography & Camera',
    authority: 'Lenses, Lighting, Sensor Calibration, DIT',
    veto: 'YES (E01)',
    vetoType: 'yes',
    model: 'Gemini 2.5 Pro (Standard)'
  },
  {
    band: 'Band F',
    dept: 'Production Design & Art',
    authority: 'Sets, Props, Construction Safety, Practical SFX',
    veto: 'YES (F01)',
    vetoType: 'yes',
    model: 'Gemini 2.5 Pro (Standard)'
  },
  {
    band: 'Band G',
    dept: 'Costume, Hair & Makeup',
    authority: 'Wardrobe Continuity, Prosthetics, Aging',
    veto: 'NO (Advisory)',
    vetoType: 'no',
    model: 'Gemini 2.5 Flash (Cheap)'
  },
  {
    band: 'Band H',
    dept: 'Sound & Foley',
    authority: 'Dolby Atmos, Production Audio, ADR, Desync Detect',
    veto: 'YES (H01)',
    vetoType: 'yes',
    model: 'Gemini 2.5 Pro (Standard)'
  },
  {
    band: 'Band I',
    dept: 'Stunts, Action & Armory',
    authority: 'Live Pyrotechnics, Wire Work, Stunt Safety',
    veto: 'YES (I01)',
    vetoType: 'yes',
    model: 'Gemini 3.8 Flash (Reasoning)'
  },
  {
    band: 'Band J',
    dept: 'VFX, CGI & Special FX',
    authority: 'Render Farms, Houdini Sims, Compositing',
    veto: 'YES (J01)',
    vetoType: 'yes',
    model: 'Gemini 2.5 Pro (Standard)'
  },
  {
    band: 'Band K',
    dept: 'Editorial & Post',
    authority: 'Rough Cuts, Dailies Assembly, Pacing',
    veto: 'NO (Advisory)',
    vetoType: 'no',
    model: 'Gemini 2.5 Pro (Standard)'
  },
  {
    band: 'Band L',
    dept: 'Music, Score & Songs',
    authority: 'Orchestral Score, Multilingual Songs, Tempo Locks',
    veto: 'NO (Advisory)',
    vetoType: 'no',
    model: 'Gemini 2.5 Pro (Standard)'
  },
  {
    band: 'Band M',
    dept: 'DI, Color & Mastering',
    authority: 'ACES Color Space, HDR10+, Dolby Vision Grade',
    veto: 'YES (M01)',
    vetoType: 'yes',
    model: 'Gemini 2.5 Pro (Standard)'
  },
  {
    band: 'Band N',
    dept: 'Distribution & Exhibition',
    authority: 'DCP Delivery, OTT CDN Failover, Theater Ratios',
    veto: 'YES (N01)',
    vetoType: 'yes',
    model: 'Gemini 2.5 Flash (Cheap)'
  },
  {
    band: 'Band O',
    dept: 'Legal, Rights & Censor',
    authority: 'CBFC Censor Clearance, IP Indemnity, Contracts',
    veto: 'YES (O01)',
    vetoType: 'yes',
    model: 'Gemini 3.8 Flash (Reasoning)'
  },
  {
    band: 'Band P',
    dept: 'Marketing, PR & Publicity',
    authority: 'Teaser Releases, Social Sentiment, Press Junkets',
    veto: 'NO (Advisory)',
    vetoType: 'no',
    model: 'Gemini 2.5 Flash (Cheap)'
  },
  {
    band: 'Band Q',
    dept: 'Virtual Production & GenAI',
    authority: 'LED Volume Tracking, Unreal Engine 5 nDisplay',
    veto: 'YES (Q01)',
    vetoType: 'yes',
    model: 'Gemini 3.8 Flash (Reasoning)'
  },
  {
    band: 'COMP',
    dept: 'Cross-Band Composites',
    authority: 'Hybrid Specializations (Stunt-Cam, VFX-DI, Audio-Score)',
    veto: 'Role-Specific',
    vetoType: 'mixed',
    model: 'Gemini 2.5 Pro / 3.8 Flash'
  },
  {
    band: 'ANTG',
    dept: 'Adversarial Red-Team',
    authority: 'Schedule Chaos, Copyright Litigation, Leak Probe',
    veto: 'Adversarial',
    vetoType: 'no',
    model: 'Gemini 3.8 Flash (Reasoning)'
  }
];

export function AboutThiraiKuzhu({ i18n = {}, language = 'en' }) {
  const content = getAboutContent(language);

  return (
    <div className="about-container">
      {/* Hero Banner */}
      <div className="about-hero-glass">
        <div className="hero-badge">{content.heroBadge || '🎬 Google Cloud AI & Gemini 2026 Hackathon'}</div>
        <h1>
          Thirai Kuzhu AI <span className="tamil-accent">({i18n.tamilTitle || i18n.tamil_title || 'திரை குழு AI'})</span>
        </h1>
        <p className="hero-lead">
          {content.heroLead || i18n.aboutDesc || i18n.about_desc || 'The World’s First Autonomous Multi-Agent Film Production Operating System and Incident Command Center. Built for Indian, Hollywood, and Global Epic Cinema.'}
        </p>
      </div>

      {/* Pillars Grid */}
      <div className="about-pillars-grid">
        {(content.pillars || []).map((pillar, idx) => (
          <div key={idx} className="pillar-card-glass">
            <div className="pillar-icon">{pillar.icon}</div>
            <h3>{pillar.title}</h3>
            <p>{pillar.desc}</p>
          </div>
        ))}
      </div>

      {/* 17 Bands Breakdown Table */}
      <div className="bands-breakdown-card-glass">
        <h3>{content.bandsTitle || 'Comprehensive 17-Band Crew Model'}</h3>
        <p className="hint-text">{content.bandsHint || 'Every phase of filmmaking modeled with specialized authority, tools, and escalation:'}</p>

        <div className="table-responsive">
          <table className="bands-table">
            <thead>
              <tr>
                <th>{content.tableHeaders ? content.tableHeaders[0] : 'Band'}</th>
                <th>{content.tableHeaders ? content.tableHeaders[1] : 'Department Name'}</th>
                <th>{content.tableHeaders ? content.tableHeaders[2] : 'Core Authority'}</th>
                <th>{content.tableHeaders ? content.tableHeaders[3] : 'Veto Power'}</th>
                <th>{content.tableHeaders ? content.tableHeaders[4] : 'Key Model Tier'}</th>
              </tr>
            </thead>
            <tbody>
              {BANDS_DATA.map((row, idx) => (
                <tr key={idx}>
                  <td><strong>{row.band}</strong></td>
                  <td>{row.dept}</td>
                  <td>{row.authority}</td>
                  <td>
                    <span className={`pill-${row.vetoType}`}>
                      {row.veto}
                    </span>
                  </td>
                  <td>{row.model}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Tech Stack Specs */}
      <div className="tech-specs-card-glass">
        <h3>{content.techSpecsTitle || 'Technical Architecture & Specifications'}</h3>
        <div className="specs-grid">
          {(content.specs || [
            { title: 'Frontend', desc: 'React 18 + Vite, OKLCH Glassmorphic Cinema Theme, Firebase Auth Context, EventSource SSE Stream' },
            { title: 'Backend', desc: 'Python 3.12, FastAPI, Pydantic v2, Google ADK & Vertex AI, YAML/JSON Persona Registry' },
            { title: 'AI & Models', desc: 'Gemini 2.5 Flash (High-throughput), Gemini 2.5 Pro (Deep analysis), Gemini 3.8 Flash (Reasoning & Debate)' },
            { title: 'Observability', desc: 'Grafana Cloud MCP Streamable HTTP, Prometheus Metrics, Tempo Distributed Tracing, Loki Logs' }
          ]).map((spec, idx) => (
            <div key={idx} className="spec-card">
              <h4>{spec.title}</h4>
              <p>{spec.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
