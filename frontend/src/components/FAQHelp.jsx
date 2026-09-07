import React, { useState, useMemo } from 'react';

const FAQS = [
  {
    category: 'Architecture & Personas',
    question: 'What is Thirai Kuzhu AI (திரை குழு AI)?',
    answer: 'Thirai Kuzhu AI is an autonomous, multi-agent film production operating system and incident command center designed for Indian and global cinema. It models the entire production hierarchy across 17 specialized studio departments (369 personas), automating triage, continuity, safety, multimodal asset review, and real-time observability.'
  },
  {
    category: 'Architecture & Personas',
    question: 'How are the 369 personas structured across the 17 Bands?',
    answer: 'Personas are organized into 17 Department Bands (A: Executive, B: Direction, C: Screenplay, D: Casting, E: Cinematography, F: Production Design, G: Costume/HMU, H: Sound, I: Stunts, J: VFX, K: Editorial, L: Music, M: DI/Color, N: Distribution, O: Legal/Censor, P: Marketing, Q: Virtual Production), plus Cross-Band Composites (COMP01..08) and Red-Team Antagonists (ANTG01..05).'
  },
  {
    category: 'Governance & Authority',
    question: 'What is the strict difference between can_block: true and can_block: false?',
    answer: 'Personas with can_block: true (such as B01 Director, I01 Stunt Director, O01 Legal Counsel) possess executive veto power to immediately halt sequences or shooting when safety, copyright, or continuity violations occur. In contrast, personas with can_block: false (and all dynamically spawned SMEs under Section 19) operate strictly in an advisory and consultative capacity.'
  },
  {
    category: 'Dynamic SMEs',
    question: 'How does Section 19 contract dynamic SME synthesis work?',
    answer: 'When a screenplay scene demands specialized domain verification (e.g. Chola bronze metallurgy, orbital astrodynamics, microtonal ragas), the Dynamic SME Studio extracts entities, selects a parent persona, and instantiates an ephemeral specialist with read-only tools and a guaranteed can_block: false contract.'
  },
  {
    category: 'Debate & Arbitration',
    question: 'How does the Dialectical Arbitration Debate engine resolve creative deadlocks?',
    answer: 'When two department heads hold opposing positions (e.g., Cinematographer requesting 8K 120fps IMAX vs Line Producer enforcing memory and budget limits), the system initiates a structured multi-round debate arbitrated by an executive persona (e.g., A01 Producer or B01 Director) to yield a binding, continuity-preserving compromise.'
  },
  {
    category: 'Adversarial Testing',
    question: 'What do the 5 Red-Team Antagonists simulate?',
    answer: 'The red-team agents stress-test production plans before shooting begins: ANTG01 breaks schedules with talent date collisions; ANTG02 injects copyright and plagiarism claims; ANTG03 exposes narrative pacing holes and cliches; ANTG04 probes dailies for piracy leaks; and ANTG05 simulates monsoons and force majeure events.'
  },
  {
    category: 'Multimodal Media',
    question: 'How does the MultiModal Media Studio inspect film assets?',
    answer: 'Powered by Gemini 2.5 and 3.8 Flash multimodal reasoning, it processes four distinct modalities: Screenplay call sheet scans (OCR/Vision), Storyboard concept stills (Framing/Color/Aspect Ratio), Foley and dialogue WAVs (Dolby Atmos spatial bed/frequency transients), and Video dailies (HFR frame drop/wire paint-out detection).'
  },
  {
    category: 'Observability',
    question: 'How does Grafana Cloud MCP Streamable HTTP transport function?',
    answer: 'Thirai Kuzhu AI streams real-time telemetry into Grafana Cloud using the Model Context Protocol (MCP) Streamable HTTP transport. It tracks Prometheus metrics (CDN 504 errors, CUDA VRAM, Atmos drift), correlates Tempo traces, and auto-injects director mitigation annotations directly onto Grafana production dashboards.'
  }
];

export function FAQHelp() {
  const [searchQuery, setSearchQuery] = useState('');
  const [openIndex, setOpenIndex] = useState(0);

  const filteredFaqs = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    if (!q) return FAQS;
    return FAQS.filter(
      (f) =>
        f.question.toLowerCase().includes(q) ||
        f.answer.toLowerCase().includes(q) ||
        f.category.toLowerCase().includes(q)
    );
  }, [searchQuery]);

  return (
    <div className="faq-container">
      {/* Header */}
      <div className="faq-header-glass">
        <div className="faq-title-group">
          <h2>❓ Frequently Asked Questions & Studio Help</h2>
          <p>
            Find comprehensive explanations of Thirai Kuzhu AI architecture, 17-band crew hierarchy, dialectical debate rules, and Grafana telemetry.
          </p>
        </div>
      </div>

      {/* Search Bar */}
      <div className="faq-search-card-glass">
        <div className="search-input-box">
          <span className="search-icon" aria-hidden="true">🔍</span>
          <input
            type="text"
            className="faq-search-input"
            placeholder="Search questions by keyword (e.g. can_block, SME, debate, Grafana, red-team)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {searchQuery && (
            <button className="search-clear-btn" onClick={() => setSearchQuery('')}>✕</button>
          )}
        </div>
      </div>

      {/* Accordion List */}
      <div className="faq-list">
        {filteredFaqs.map((faq, idx) => {
          const isOpen = openIndex === idx;
          return (
            <div key={idx} className={`faq-card-glass ${isOpen ? 'expanded' : ''}`}>
              <button
                className="faq-question-btn"
                onClick={() => setOpenIndex(isOpen ? -1 : idx)}
                aria-expanded={isOpen}
              >
                <div className="faq-q-left">
                  <span className="faq-cat-badge">{faq.category}</span>
                  <span className="faq-question-text">{faq.question}</span>
                </div>
                <span className="faq-toggle-icon">{isOpen ? '−' : '+'}</span>
              </button>

              {isOpen && (
                <div className="faq-answer-pane">
                  <p>{faq.answer}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Keyboard Shortcuts Cheatsheet */}
      <div className="shortcuts-card-glass">
        <h3>⌨️ Studio Keyboard Shortcuts</h3>
        <div className="shortcuts-grid">
          <div className="shortcut-item">
            <kbd className="key-cap">1</kbd> .. <kbd className="key-cap">9</kbd>
            <span className="shortcut-desc">Switch active studio workspace tabs</span>
          </div>
          <div className="shortcut-item">
            <kbd className="key-cap">Esc</kbd>
            <span className="shortcut-desc">Dismiss persona detail modal or dialog</span>
          </div>
          <div className="shortcut-item">
            <kbd className="key-cap">Ctrl</kbd> + <kbd className="key-cap">K</kbd>
            <span className="shortcut-desc">Instant focus on persona search input</span>
          </div>
          <div className="shortcut-item">
            <kbd className="key-cap">Alt</kbd> + <kbd className="key-cap">D</kbd>
            <span className="shortcut-desc">Dispatch incident multi-agent investigation</span>
          </div>
        </div>
      </div>
    </div>
  );
}
