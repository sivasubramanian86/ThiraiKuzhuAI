import React from 'react';

export function AboutThiraiKuzhu({ i18n = {} }) {
  return (
    <div className="about-container">
      {/* Hero Banner */}
      <div className="about-hero-glass">
        <div className="hero-badge">🎬 Google Cloud AI & Gemini 2026 Hackathon</div>
        <h1>
          Thirai Kuzhu AI <span className="tamil-accent">({i18n.tamil_title || 'திரை குழு AI'})</span>
        </h1>
        <p className="hero-lead">
          {i18n.about_desc || 'The World’s First Autonomous Multi-Agent Film Production Operating System and Incident Command Center. Built for Indian, Hollywood, and Global Epic Cinema.'}
        </p>
      </div>

      {/* Pillars Grid */}
      <div className="about-pillars-grid">
        <div className="pillar-card-glass">
          <div className="pillar-icon">🏛️</div>
          <h3>17-Band Crew Topology</h3>
          <p>
            Models 369 specialized cinematic personas spanning Executive, Direction, Cinematography, Stunts, VFX, Music, DI, Legal, and Virtual Production with strict authority contracts and cycle-free escalation.
          </p>
        </div>

        <div className="pillar-card-glass">
          <div className="pillar-icon">⚖️</div>
          <h3>Dialectical Arbitration</h3>
          <p>
            Resolves creative conflicts through multi-turn dialectical debates arbitrated by Executive Directors and Producers, maintaining artistic vision while guarding budgets and release dates.
          </p>
        </div>

        <div className="pillar-card-glass">
          <div className="pillar-icon">🧬</div>
          <h3>Section 19 Dynamic SMEs</h3>
          <p>
            Synthesizes on-demand specialized advisors directly from screenplay scenes (metallurgy, orbital astrodynamics, microtonal ragas) with a guaranteed non-blocking contract.
          </p>
        </div>

        <div className="pillar-card-glass">
          <div className="pillar-icon">📊</div>
          <h3>Grafana Cloud Observability</h3>
          <p>
            Streamable HTTP Model Context Protocol (MCP) telemetry tracking Prometheus metrics, Tempo distributed traces, and Loki logs with automated Director mitigation annotations.
          </p>
        </div>
      </div>

      {/* 17 Bands Breakdown Table */}
      <div className="bands-breakdown-card-glass">
        <h3>Comprehensive 17-Band Crew Model</h3>
        <p className="hint-text">Every phase of filmmaking modeled with specialized authority, tools, and escalation:</p>

        <div className="table-responsive">
          <table className="bands-table">
            <thead>
              <tr>
                <th>Band</th>
                <th>Department Name</th>
                <th>Core Authority</th>
                <th>Veto Power</th>
                <th>Key Model Tier</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Band A</strong></td>
                <td>Executive & Producing</td>
                <td>Greenlight, Budget, Production Insurance, Overages</td>
                <td><span className="pill-yes">YES (A01)</span></td>
                <td>Gemini 3.8 Flash (Reasoning)</td>
              </tr>
              <tr>
                <td><strong>Band B</strong></td>
                <td>Direction</td>
                <td>Artistic Vision, Scene Staging, Sequence Halts</td>
                <td><span className="pill-yes">YES (B01)</span></td>
                <td>Gemini 3.8 Flash (Reasoning)</td>
              </tr>
              <tr>
                <td><strong>Band C</strong></td>
                <td>Screenplay & Story</td>
                <td>Narrative Structure, Scene Dialogue, Fact-Checking</td>
                <td><span className="pill-no">NO (Advisory)</span></td>
                <td>Gemini 2.5 Pro (Standard)</td>
              </tr>
              <tr>
                <td><strong>Band D</strong></td>
                <td>Casting & Talent</td>
                <td>Actor Availability, Star Riders, Intimacy Protocols</td>
                <td><span className="pill-yes">YES (D01)</span></td>
                <td>Gemini 2.5 Pro (Standard)</td>
              </tr>
              <tr>
                <td><strong>Band E</strong></td>
                <td>Cinematography & Camera</td>
                <td>Lenses, Lighting, Sensor Calibration, DIT</td>
                <td><span className="pill-yes">YES (E01)</span></td>
                <td>Gemini 2.5 Pro (Standard)</td>
              </tr>
              <tr>
                <td><strong>Band F</strong></td>
                <td>Production Design & Art</td>
                <td>Sets, Props, Construction Safety, Practical SFX</td>
                <td><span className="pill-yes">YES (F01)</span></td>
                <td>Gemini 2.5 Pro (Standard)</td>
              </tr>
              <tr>
                <td><strong>Band G</strong></td>
                <td>Costume, Hair & Makeup</td>
                <td>Wardrobe Continuity, Prosthetics, Aging</td>
                <td><span className="pill-no">NO (Advisory)</span></td>
                <td>Gemini 2.5 Flash (Cheap)</td>
              </tr>
              <tr>
                <td><strong>Band H</strong></td>
                <td>Sound & Foley</td>
                <td>Dolby Atmos, Production Audio, ADR, Desync Detect</td>
                <td><span className="pill-yes">YES (H01)</span></td>
                <td>Gemini 2.5 Pro (Standard)</td>
              </tr>
              <tr>
                <td><strong>Band I</strong></td>
                <td>Stunts, Action & Armory</td>
                <td>Live Pyrotechnics, Wire Work, Stunt Safety</td>
                <td><span className="pill-yes">YES (I01)</span></td>
                <td>Gemini 3.8 Flash (Reasoning)</td>
              </tr>
              <tr>
                <td><strong>Band J</strong></td>
                <td>VFX, CGI & Special FX</td>
                <td>Render Farms, Houdini Sims, Compositing</td>
                <td><span className="pill-yes">YES (J01)</span></td>
                <td>Gemini 2.5 Pro (Standard)</td>
              </tr>
              <tr>
                <td><strong>Band K</strong></td>
                <td>Editorial & Post</td>
                <td>Rough Cuts, Dailies Assembly, Pacing</td>
                <td><span className="pill-no">NO (Advisory)</span></td>
                <td>Gemini 2.5 Pro (Standard)</td>
              </tr>
              <tr>
                <td><strong>Band L</strong></td>
                <td>Music, Score & Songs</td>
                <td>Orchestral Score, Multilingual Songs, Tempo Locks</td>
                <td><span className="pill-no">NO (Advisory)</span></td>
                <td>Gemini 2.5 Pro (Standard)</td>
              </tr>
              <tr>
                <td><strong>Band M</strong></td>
                <td>DI, Color & Mastering</td>
                <td>ACES Color Space, HDR10+, Dolby Vision Grade</td>
                <td><span className="pill-yes">YES (M01)</span></td>
                <td>Gemini 2.5 Pro (Standard)</td>
              </tr>
              <tr>
                <td><strong>Band N</strong></td>
                <td>Distribution & Exhibition</td>
                <td>DCP Delivery, OTT CDN Failover, Theater Ratios</td>
                <td><span className="pill-yes">YES (N01)</span></td>
                <td>Gemini 2.5 Flash (Cheap)</td>
              </tr>
              <tr>
                <td><strong>Band O</strong></td>
                <td>Legal, Rights & Censor</td>
                <td>CBFC Censor Clearance, IP Indemnity, Contracts</td>
                <td><span className="pill-yes">YES (O01)</span></td>
                <td>Gemini 3.8 Flash (Reasoning)</td>
              </tr>
              <tr>
                <td><strong>Band P</strong></td>
                <td>Marketing, PR & Publicity</td>
                <td>Teaser Releases, Social Sentiment, Press Junkets</td>
                <td><span className="pill-no">NO (Advisory)</span></td>
                <td>Gemini 2.5 Flash (Cheap)</td>
              </tr>
              <tr>
                <td><strong>Band Q</strong></td>
                <td>Virtual Production & GenAI</td>
                <td>LED Volume Tracking, Unreal Engine 5 nDisplay</td>
                <td><span className="pill-yes">YES (Q01)</span></td>
                <td>Gemini 3.8 Flash (Reasoning)</td>
              </tr>
              <tr>
                <td><strong>COMP</strong></td>
                <td>Cross-Band Composites</td>
                <td>Hybrid Specializations (Stunt-Cam, VFX-DI, Audio-Score)</td>
                <td><span className="pill-mixed">Role-Specific</span></td>
                <td>Gemini 2.5 Pro / 3.8 Flash</td>
              </tr>
              <tr>
                <td><strong>ANTG</strong></td>
                <td>Adversarial Red-Team</td>
                <td>Schedule Chaos, Copyright Litigation, Leak Probe</td>
                <td><span className="pill-no">Adversarial</span></td>
                <td>Gemini 3.8 Flash (Reasoning)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Tech Stack Specs */}
      <div className="tech-specs-card-glass">
        <h3>Technical Architecture & Specifications</h3>
        <div className="specs-grid">
          <div className="spec-card">
            <h4>Frontend</h4>
            <p>React 18 + Vite, OKLCH Glassmorphic Cinema Theme, Firebase Auth Context, EventSource SSE Stream</p>
          </div>
          <div className="spec-card">
            <h4>Backend</h4>
            <p>Python 3.12, FastAPI, Pydantic v2, Google ADK & Vertex AI, YAML/JSON Persona Registry</p>
          </div>
          <div className="spec-card">
            <h4>AI & Models</h4>
            <p>Gemini 2.5 Flash (High-throughput), Gemini 2.5 Pro (Deep analysis), Gemini 3.8 Flash (Reasoning & Debate)</p>
          </div>
          <div className="spec-card">
            <h4>Observability</h4>
            <p>Grafana Cloud MCP Streamable HTTP, Prometheus Metrics, Tempo Distributed Tracing, Loki Logs</p>
          </div>
        </div>
      </div>
    </div>
  );
}
