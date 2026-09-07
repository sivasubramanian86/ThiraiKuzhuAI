import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const MODEL_PRESETS = [
  {
    id: 'imagen-3',
    name: 'Google Imagen 3 Ultra',
    badge: 'Photoreal 4K',
    latency: '3.2s',
    cost: '$0.035 / gen',
    description: 'Ultra-photorealistic cinematic architectural rendering, natural volumetric lighting & high-fidelity materials.',
    specs: '4096x2304 DCI • 16-bit color depth • Ray-traced bounce lighting'
  },
  {
    id: 'nano-banana',
    name: 'Nano Banana Edge (v2.4)',
    badge: 'Edge 0.4s',
    latency: '0.42s',
    cost: '$0.00 (On-Device)',
    description: 'Ultra-fast low-bit quantized diffusion model for rapid brainstorming, live set sketching & instant CAD wireframes.',
    specs: '512-1024px dynamic • 4-bit INT4 weight quantization • 0.8GB VRAM footprint'
  }
];

const ART_WORKFLOWS = [
  { id: 'architecture', label: '📐 Set Architecture & Blueprints', icon: '📐' },
  { id: 'location', label: '🌄 Location Graphics & Matte Painting', icon: '🌄' },
  { id: 'materials', label: '🧱 Material Textures & Art Structure', icon: '🧱' }
];

const ASPECT_RATIOS = [
  { id: '16:9', label: '16:9 HD Broadcast', width: 640, height: 360 },
  { id: '2.39:1', label: '2.39:1 CinemaScope Anamorphic', width: 717, height: 300 },
  { id: '1.43:1', label: '1.43:1 IMAX 70mm Large Format', width: 572, height: 400 }
];

const CURATED_PROMPTS = [
  {
    category: 'Set Architecture',
    title: 'Cyberpunk Shinjuku Back-Alley Bar',
    prompt: 'Interior architectural section view of a subterranean neon noodle bar, exposed copper pipes, water-stained concrete, volumetric cyan and amber neon haze, 2.39:1 anamorphic lens flare.',
    workflow: 'architecture',
    materials: ['Brushed Copper', 'Stained Concrete', 'Wet Asphalt', 'Neon Tube Glass'],
    dimensions: 'Floor: 14m x 8m • Ceiling: 3.8m clearance • Stage Rig: Truss Grid 04'
  },
  {
    category: 'Location Graphics',
    title: 'Dravidian Granite Temple Courtyard',
    prompt: 'Aerial establishing matte painting of an ancient monolithic black granite gopuram courtyard at sunrise, godrays through sandalwood incense smoke, hand-carved pillars with intricate relief.',
    workflow: 'location',
    materials: ['Polished Black Granite', 'Brass Torches', 'Sandalwood Pillars', 'Terra Cotta Tile'],
    dimensions: 'Perimeter: 120m x 85m • Gopuram Height: 48m • Sun Angle: 18° Azimuth'
  },
  {
    category: 'Art Structure',
    title: 'Solarpunk Orbital Habitat Greenhouse',
    prompt: 'Orthographic cutaway diagram of a geodesic biosphere ring, kinetic solar louvers, aeroponic crop towers, translucent aerogel panels, engineered titanium trusses.',
    workflow: 'materials',
    materials: ['Aerogel Membrane', 'Anodized Titanium', 'Bamboo Laminate', 'Borosilicate Glass'],
    dimensions: 'Diameter: 65m • Structural Load: 450 kN/m² • Glazing Index: 0.88'
  },
  {
    category: 'Location Graphics',
    title: 'Neo-Victorian Steampunk Clocktower',
    prompt: 'Production design cross-section of a 7-story clock tower gear-room, brass clockwork escapement wheels, stained glass dials backlit by foggy moonlight, riveted steel beams.',
    workflow: 'architecture',
    materials: ['Aged Cast Iron', 'High-Tensile Brass', 'Leaded Stained Glass', 'Oak Flooring'],
    dimensions: 'Footprint: 18m x 18m • Gear Shaft: 22m vertical • Stage Floor Rating: 15 Ton'
  }
];

export default function VirtualArtStudio() {
  const { currentPersona } = useAuth();
  const [selectedModel, setSelectedModel] = useState('imagen-3');
  const [selectedWorkflow, setSelectedWorkflow] = useState('architecture');
  const [selectedRatio, setSelectedRatio] = useState('2.39:1');
  const [activePrompt, setActivePrompt] = useState(CURATED_PROMPTS[0].prompt);
  const [activePreset, setActivePreset] = useState(CURATED_PROMPTS[0]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [blueprintOverlay, setBlueprintOverlay] = useState(true);
  const [generationCount, setGenerationCount] = useState(1);
  const [slateStatus, setSlateStatus] = useState(null);

  const activeModelMeta = MODEL_PRESETS.find(m => m.id === selectedModel);
  const activeRatioMeta = ASPECT_RATIOS.find(r => r.id === selectedRatio);

  const handleSelectPreset = (preset) => {
    setActivePreset(preset);
    setActivePrompt(preset.prompt);
    setSelectedWorkflow(preset.workflow);
  };

  const handleGenerateArt = () => {
    setIsGenerating(true);
    setSlateStatus(null);
    setTimeout(() => {
      setIsGenerating(false);
      setGenerationCount(prev => prev + 1);
    }, selectedModel === 'nano-banana' ? 420 : 1100);
  };

  const handleBindToSlate = () => {
    setSlateStatus(`Artwork bound to Production Slate Scene #AR-10${generationCount} for Art Director approval.`);
    setTimeout(() => setSlateStatus(null), 4000);
  };

  return (
    <div className="virtual-art-studio-root" style={{ padding: '1.5rem', color: '#f1f5f9' }}>
      {/* Studio Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: '1.5rem',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        paddingBottom: '1rem',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span style={{ fontSize: '2rem' }}>🎨</span>
            <div>
              <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: '800', background: 'linear-gradient(135deg, #f59e0b, #ef4444)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                Virtual Art Department &amp; Production Design Studio
              </h2>
              <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.85rem', color: '#94a3b8' }}>
                CAD-grade set blueprints, location matte paintings &amp; material shaders driven by Google Imagen 3 &amp; Nano Banana edge models
              </p>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            background: 'rgba(245, 158, 11, 0.15)',
            border: '1px solid rgba(245, 158, 11, 0.3)',
            padding: '0.35rem 0.75rem',
            borderRadius: '6px',
            fontSize: '0.8rem',
            color: '#fbbf24',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem'
          }}>
            <span>🎭 Active Persona:</span>
            <strong>{currentPersona?.title || 'Art Director / Production Designer'}</strong>
          </div>
        </div>
      </div>

      {/* Model Selection Bar */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '1rem',
        marginBottom: '1.5rem'
      }}>
        {MODEL_PRESETS.map((model) => {
          const isSelected = selectedModel === model.id;
          return (
            <div
              key={model.id}
              data-testid={`model-card-${model.id}`}
              onClick={() => setSelectedModel(model.id)}
              style={{
                background: isSelected ? 'rgba(245, 158, 11, 0.12)' : 'rgba(15, 23, 42, 0.6)',
                border: isSelected ? '2px solid #f59e0b' : '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '10px',
                padding: '1rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                position: 'relative'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '1.25rem' }}>{model.id === 'imagen-3' ? '⚡' : '🍌'}</span>
                  <span style={{ fontWeight: '700', fontSize: '0.95rem', color: isSelected ? '#fbbf24' : '#e2e8f0' }}>{model.name}</span>
                </div>
                <span style={{
                  fontSize: '0.7rem',
                  padding: '0.2rem 0.5rem',
                  borderRadius: '999px',
                  background: isSelected ? '#f59e0b' : 'rgba(255, 255, 255, 0.1)',
                  color: isSelected ? '#000' : '#cbd5e1',
                  fontWeight: '700'
                }}>
                  {model.badge}
                </span>
              </div>
              <p style={{ margin: '0 0 0.5rem 0', fontSize: '0.8rem', color: '#94a3b8', lineHeight: '1.3' }}>
                {model.description}
              </p>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#64748b', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '0.5rem' }}>
                <span>⏱️ Latency: <strong style={{ color: '#38bdf8' }}>{model.latency}</strong></span>
                <span>💰 Budget: <strong style={{ color: '#10b981' }}>{model.cost}</strong></span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Studio Grid: Controls & Visual Canvas */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(320px, 1fr) minmax(400px, 1.4fr)', gap: '1.5rem', alignItems: 'start' }}>
        {/* Left Column: Prompt & Architectural Controls */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Workflow Tabs */}
          <div style={{ display: 'flex', gap: '0.5rem', background: 'rgba(15, 23, 42, 0.7)', padding: '0.35rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.08)' }}>
            {ART_WORKFLOWS.map((wf) => (
              <button
                key={wf.id}
                onClick={() => setSelectedWorkflow(wf.id)}
                style={{
                  flex: 1,
                  padding: '0.5rem',
                  fontSize: '0.75rem',
                  borderRadius: '6px',
                  border: 'none',
                  background: selectedWorkflow === wf.id ? '#f59e0b' : 'transparent',
                  color: selectedWorkflow === wf.id ? '#0f172a' : '#94a3b8',
                  fontWeight: selectedWorkflow === wf.id ? '700' : '500',
                  cursor: 'pointer',
                  transition: 'background 0.2s'
                }}
              >
                {wf.label}
              </button>
            ))}
          </div>

          {/* Aspect Ratio Selector */}
          <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.08)' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '700', color: '#cbd5e1', marginBottom: '0.5rem' }}>
              📐 Frame Aspect Ratio &amp; Sensor Standard:
            </label>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {ASPECT_RATIOS.map((ratio) => (
                <button
                  key={ratio.id}
                  onClick={() => setSelectedRatio(ratio.id)}
                  style={{
                    padding: '0.4rem 0.75rem',
                    fontSize: '0.75rem',
                    borderRadius: '6px',
                    border: selectedRatio === ratio.id ? '1px solid #f59e0b' : '1px solid rgba(255,255,255,0.1)',
                    background: selectedRatio === ratio.id ? 'rgba(245, 158, 11, 0.2)' : 'rgba(30, 41, 59, 0.5)',
                    color: selectedRatio === ratio.id ? '#fbbf24' : '#94a3b8',
                    cursor: 'pointer'
                  }}
                >
                  {ratio.label}
                </button>
              ))}
            </div>
          </div>

          {/* Curated Architecture Presets */}
          <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.08)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: '700', color: '#cbd5e1' }}>
                🏛️ Production Design Presets:
              </label>
              <span style={{ fontSize: '0.7rem', color: '#64748b' }}>Click to apply prompt &amp; specs</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
              {CURATED_PROMPTS.map((preset, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSelectPreset(preset)}
                  style={{
                    padding: '0.5rem',
                    fontSize: '0.75rem',
                    textAlign: 'left',
                    borderRadius: '6px',
                    background: activePreset.title === preset.title ? 'rgba(245, 158, 11, 0.2)' : 'rgba(30, 41, 59, 0.4)',
                    border: activePreset.title === preset.title ? '1px solid #f59e0b' : '1px solid rgba(255,255,255,0.06)',
                    color: activePreset.title === preset.title ? '#fef08a' : '#cbd5e1',
                    cursor: 'pointer'
                  }}
                >
                  <div style={{ fontWeight: '600' }}>{preset.title}</div>
                  <div style={{ fontSize: '0.65rem', color: '#94a3b8' }}>{preset.category}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Prompt Editor & Generation CTA */}
          <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.08)' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '700', color: '#cbd5e1', marginBottom: '0.5rem' }}>
              ✍️ Art Director Prompt &amp; Lighting Directives:
            </label>
            <textarea
              rows={4}
              value={activePrompt}
              onChange={(e) => setActivePrompt(e.target.value)}
              style={{
                width: '100%',
                background: 'rgba(15, 23, 42, 0.9)',
                border: '1px solid rgba(255,255,255,0.15)',
                borderRadius: '6px',
                color: '#f8fafc',
                padding: '0.75rem',
                fontSize: '0.85rem',
                fontFamily: 'monospace',
                resize: 'vertical',
                boxSizing: 'border-box'
              }}
            />

            <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.75rem', alignItems: 'center' }}>
              <button
                onClick={handleGenerateArt}
                disabled={isGenerating}
                style={{
                  flex: 1,
                  background: isGenerating ? '#64748b' : 'linear-gradient(135deg, #f59e0b, #d97706)',
                  color: '#0f172a',
                  fontWeight: '800',
                  fontSize: '0.85rem',
                  padding: '0.7rem 1.25rem',
                  borderRadius: '6px',
                  border: 'none',
                  cursor: isGenerating ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem',
                  boxShadow: '0 4px 12px rgba(245, 158, 11, 0.3)'
                }}
              >
                {isGenerating ? (
                  <>🔄 Synthesizing with {activeModelMeta.name}...</>
                ) : (
                  <>⚡ Render Architecture with {activeModelMeta.name}</>
                )}
              </button>

              <button
                onClick={() => setBlueprintOverlay(!blueprintOverlay)}
                title="Toggle CAD Grid & Dimension Overlay"
                style={{
                  padding: '0.65rem 0.9rem',
                  fontSize: '0.8rem',
                  borderRadius: '6px',
                  border: '1px solid rgba(255,255,255,0.15)',
                  background: blueprintOverlay ? 'rgba(56, 189, 248, 0.2)' : 'rgba(30, 41, 59, 0.6)',
                  color: blueprintOverlay ? '#38bdf8' : '#94a3b8',
                  cursor: 'pointer'
                }}
              >
                📏 CAD Grid: {blueprintOverlay ? 'ON' : 'OFF'}
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Visual Stage / CAD Blueprint Viewport */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {/* Main Viewport Container */}
          <div style={{
            background: 'radial-gradient(circle at center, #1e293b 0%, #090d16 100%)',
            borderRadius: '12px',
            border: '1px solid rgba(245, 158, 11, 0.3)',
            padding: '1rem',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            boxShadow: '0 8px 30px rgba(0,0,0,0.5)',
            position: 'relative',
            overflow: 'hidden'
          }}>
            {/* Viewport Header Bar */}
            <div style={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', fontSize: '0.75rem', color: '#94a3b8' }}>
              <div>
                <span style={{ color: '#f59e0b', fontWeight: '700' }}>RENDER CAM #01</span> • {selectedRatio} • {activePreset.title}
              </div>
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <span>Engine: <strong style={{ color: '#38bdf8' }}>{activeModelMeta.name}</strong></span>
                <span>Pass: <strong style={{ color: '#10b981' }}>#{generationCount}</strong></span>
              </div>
            </div>

            {/* Simulated Generative Canvas with CAD Architectural SVG */}
            <div style={{
              width: '100%',
              maxWidth: `${activeRatioMeta.width}px`,
              aspectRatio: selectedRatio === '2.39:1' ? '2.39 / 1' : selectedRatio === '1.43:1' ? '1.43 / 1' : '16 / 9',
              background: '#040711',
              borderRadius: '8px',
              border: '2px solid rgba(56, 189, 248, 0.4)',
              position: 'relative',
              overflow: 'hidden',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              {/* Dynamic SVG Blueprint / Scenic Render */}
              <svg width="100%" height="100%" viewBox="0 0 800 400" preserveAspectRatio="none" style={{ position: 'absolute', top: 0, left: 0 }}>
                <defs>
                  {/* Grid Pattern */}
                  <pattern id="cadGrid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(56, 189, 248, 0.15)" strokeWidth="0.8" />
                  </pattern>
                  <linearGradient id="skyAtmosphere" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#0b132b" />
                    <stop offset="50%" stopColor="#1c2541" />
                    <stop offset="100%" stopColor="#3a506b" />
                  </linearGradient>
                  <linearGradient id="neonGlow" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.8" />
                    <stop offset="50%" stopColor="#ef4444" stopOpacity="0.8" />
                    <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.8" />
                  </linearGradient>
                </defs>

                {/* Base Scenery Gradient */}
                <rect width="800" height="400" fill="url(#skyAtmosphere)" />

                {/* Architectural Structures based on workflow */}
                {selectedWorkflow === 'architecture' && (
                  <g>
                    {/* Horizon & Floor Line */}
                    <line x1="0" y1="320" x2="800" y2="320" stroke="#38bdf8" strokeWidth="2" strokeDasharray="4 2" />

                    {/* Column / Trusses */}
                    <rect x="60" y="80" width="40" height="240" fill="rgba(15, 23, 42, 0.8)" stroke="#38bdf8" strokeWidth="1.5" />
                    <rect x="220" y="60" width="360" height="40" fill="rgba(245, 158, 11, 0.2)" stroke="#f59e0b" strokeWidth="1.5" />
                    <rect x="700" y="80" width="40" height="240" fill="rgba(15, 23, 42, 0.8)" stroke="#38bdf8" strokeWidth="1.5" />

                    {/* Architectural Cross Braces */}
                    <line x1="60" y1="80" x2="220" y2="100" stroke="#06b6d4" strokeWidth="1.5" />
                    <line x1="220" y1="80" x2="60" y2="100" stroke="#06b6d4" strokeWidth="1.5" />
                    <line x1="580" y1="80" x2="740" y2="100" stroke="#06b6d4" strokeWidth="1.5" />

                    {/* Center Arched Entrance / Set Portal */}
                    <path d="M 320 320 L 320 180 Q 400 130 480 180 L 480 320 Z" fill="rgba(6, 182, 212, 0.15)" stroke="#06b6d4" strokeWidth="2" />
                    <circle cx="400" cy="160" r="16" fill="none" stroke="#f59e0b" strokeWidth="1.5" />

                    {/* Neon Lighting Tubes */}
                    <path d="M 280 210 L 520 210" stroke="url(#neonGlow)" strokeWidth="4" strokeLinecap="round" />
                    <path d="M 300 225 L 500 225" stroke="#f59e0b" strokeWidth="2" strokeLinecap="round" />
                  </g>
                )}

                {selectedWorkflow === 'location' && (
                  <g>
                    {/* Distant Temple / Fortress Mountain Silhouette */}
                    <polygon points="0,320 120,160 220,240 380,100 520,230 680,120 800,320" fill="rgba(30, 41, 59, 0.8)" stroke="#38bdf8" strokeWidth="1" />
                    {/* Gopuram / Spire Outline */}
                    <path d="M 360 320 L 375 140 L 400 80 L 425 140 L 440 320 Z" fill="rgba(245, 158, 11, 0.3)" stroke="#f59e0b" strokeWidth="2" />
                    {/* Sun Disc & Volumetric Rays */}
                    <circle cx="400" cy="80" r="30" fill="url(#neonGlow)" opacity="0.6" />
                    <line x1="400" y1="80" x2="100" y2="360" stroke="#fbbf24" strokeWidth="0.75" opacity="0.4" />
                    <line x1="400" y1="80" x2="300" y2="360" stroke="#fbbf24" strokeWidth="0.75" opacity="0.4" />
                    <line x1="400" y1="80" x2="500" y2="360" stroke="#fbbf24" strokeWidth="0.75" opacity="0.4" />
                    <line x1="400" y1="80" x2="700" y2="360" stroke="#fbbf24" strokeWidth="0.75" opacity="0.4" />
                  </g>
                )}

                {selectedWorkflow === 'materials' && (
                  <g>
                    {/* Material Texture Swatches & Surface Specular Grid */}
                    <rect x="100" y="80" width="160" height="200" rx="8" fill="rgba(245, 158, 11, 0.2)" stroke="#f59e0b" strokeWidth="2" />
                    <text x="180" y="190" fill="#fef08a" fontSize="14" textAnchor="middle" fontWeight="bold">ANODIZED METAL</text>

                    <rect x="320" y="80" width="160" height="200" rx="8" fill="rgba(56, 189, 248, 0.2)" stroke="#38bdf8" strokeWidth="2" />
                    <text x="400" y="190" fill="#bae6fd" fontSize="14" textAnchor="middle" fontWeight="bold">WEATHERED STONE</text>

                    <rect x="540" y="80" width="160" height="200" rx="8" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="2" />
                    <text x="620" y="190" fill="#a7f3d0" fontSize="14" textAnchor="middle" fontWeight="bold">AEROGEL MEMBRANE</text>
                  </g>
                )}

                {/* CAD Grid Overlay */}
                {blueprintOverlay && (
                  <g>
                    <rect width="800" height="400" fill="url(#cadGrid)" />
                    {/* Dimension lines & callouts */}
                    <line x1="60" y1="40" x2="740" y2="40" stroke="#38bdf8" strokeWidth="1" strokeDasharray="3 3" />
                    <text x="400" y="32" fill="#38bdf8" fontSize="10" textAnchor="middle" fontFamily="monospace">STAGE CLEARANCE: 14.80 METERS [±0.05m]</text>

                    <line x1="30" y1="80" x2="30" y2="320" stroke="#38bdf8" strokeWidth="1" strokeDasharray="3 3" />
                    <text x="25" y="200" fill="#38bdf8" fontSize="10" textAnchor="middle" transform="rotate(-90 25 200)" fontFamily="monospace">GRID HEIGHT: 4.80m</text>

                    {/* Corner Crosshairs */}
                    <circle cx="60" cy="80" r="4" fill="none" stroke="#f59e0b" strokeWidth="1" />
                    <circle cx="740" cy="80" r="4" fill="none" stroke="#f59e0b" strokeWidth="1" />
                    <circle cx="400" cy="320" r="4" fill="none" stroke="#f59e0b" strokeWidth="1" />
                  </g>
                )}
              </svg>

              {/* Generation Loading Overlay */}
              {isGenerating && (
                <div style={{
                  position: 'absolute',
                  inset: 0,
                  background: 'rgba(4, 7, 17, 0.85)',
                  backdropFilter: 'blur(4px)',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.75rem',
                  zIndex: 10
                }}>
                  <div style={{ fontSize: '2.5rem', animation: 'spin 1s linear infinite' }}>⚙️</div>
                  <div style={{ fontSize: '0.9rem', color: '#fbbf24', fontWeight: '700' }}>
                    {selectedModel === 'nano-banana' ? '⚡ 0.4s Quantized Edge Pass...' : '🎨 Imagen 3 4K Diffusion Pass...'}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Resolving surface normals, bounce irradiance &amp; material reflectance</div>
                </div>
              )}
            </div>

            {/* Viewport Meta Footer */}
            <div style={{
              width: '100%',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginTop: '0.75rem',
              fontSize: '0.75rem',
              color: '#94a3b8',
              flexWrap: 'wrap',
              gap: '0.5rem'
            }}>
              <div>
                <span>📐 Dimensions: </span>
                <strong style={{ color: '#e2e8f0' }}>{activePreset.dimensions}</strong>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  onClick={handleBindToSlate}
                  style={{
                    padding: '0.35rem 0.75rem',
                    borderRadius: '4px',
                    border: '1px solid #10b981',
                    background: 'rgba(16, 185, 129, 0.15)',
                    color: '#34d399',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    cursor: 'pointer'
                  }}
                >
                  📌 Bind to Production Slate
                </button>
              </div>
            </div>

            {/* Slate Confirmation Alert */}
            {slateStatus && (
              <div style={{
                marginTop: '0.5rem',
                width: '100%',
                padding: '0.5rem 0.75rem',
                borderRadius: '6px',
                background: 'rgba(16, 185, 129, 0.2)',
                border: '1px solid #10b981',
                color: '#6ee7b7',
                fontSize: '0.75rem',
                textAlign: 'center'
              }}>
                ✅ {slateStatus}
              </div>
            )}
          </div>

          {/* Material Palette & Physical Specifications Card */}
          <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.08)' }}>
            <div style={{ fontSize: '0.8rem', fontWeight: '700', color: '#cbd5e1', marginBottom: '0.5rem' }}>
              🧱 Art Director Material Board &amp; Surface Textures:
            </div>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {activePreset.materials.map((mat, i) => (
                <div
                  key={i}
                  style={{
                    background: 'rgba(30, 41, 59, 0.8)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '6px',
                    padding: '0.35rem 0.65rem',
                    fontSize: '0.75rem',
                    color: '#e2e8f0',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.35rem'
                  }}
                >
                  <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: i === 0 ? '#f59e0b' : i === 1 ? '#06b6d4' : i === 2 ? '#10b981' : '#a855f7' }}></span>
                  <span>{mat}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
