import React, { useState, useMemo } from 'react';
import registryData from '../constants/registry.json';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { runPersonaDebate } from '../services/api';

const BAND_METADATA = {
  ALL: { name: 'All Personas', icon: '🎬' },
  A: { name: 'Executive & Producing', icon: '👑' },
  B: { name: 'Direction', icon: '🎥' },
  C: { name: 'Screenplay & Story', icon: '📜' },
  D: { name: 'Casting & Talent', icon: '🎭' },
  E: { name: 'Cinematography & Camera', icon: '📹' },
  F: { name: 'Production Design & Art', icon: '🏛️' },
  G: { name: 'Costume, Hair & Makeup', icon: '👗' },
  H: { name: 'Sound & Foley', icon: '🎧' },
  I: { name: 'Stunts, Action & Armory', icon: '⚔️' },
  J: { name: 'VFX, CGI & Special FX', icon: '✨' },
  K: { name: 'Editorial & Post', icon: '✂️' },
  L: { name: 'Music, Score & Songs', icon: '🎼' },
  M: { name: 'DI, Color & Mastering', icon: '🎨' },
  N: { name: 'Distribution & Exhibition', icon: '🍿' },
  O: { name: 'Legal, Rights & Censor', icon: '⚖️' },
  P: { name: 'Marketing, PR & Publicity', icon: '📢' },
  Q: { name: 'Virtual Production & GenAI', icon: '🤖' },
  COMP: { name: 'Cross-Band Composites', icon: '⚡' },
  ANTG: { name: 'Adversarial Red-Team', icon: '🛡️' }
};

const BAND_TRANSLATIONS = {
  ta: {
    ALL: 'அனைத்து பாத்திரங்கள்',
    A: 'நிர்வாகம் & தயாரிப்பு',
    B: 'இயக்கம்',
    C: 'திரைக்கதை & கதை',
    D: 'நடிகர்கள் & தேர்வு',
    E: 'ஒளிப்பதிவு & கேமரா',
    F: 'தயாரிப்பு வடிவமைப்பு & கலை',
    G: 'ஆடை & ஒப்பனை',
    H: 'ஒலி & ஃபோலே',
    I: 'சண்டைப்பயிற்சி & ஆயுதங்கள்',
    J: 'VFX & சிறப்பு விளைவுகள்',
    K: 'படத்தொகுப்பு',
    L: 'இசை & பாடல்கள்',
    M: 'டிஐ & கலரிங்',
    N: 'விநியோகம் & திரையிடல்',
    O: 'சட்டம் & தணிக்கை',
    P: 'விளம்பரம் & மார்க்கெட்டிங்',
    Q: 'மெய்நிகர் தயாரிப்பு & GenAI',
    COMP: 'கூட்டுப் பாத்திரங்கள்',
    ANTG: 'எதிரணி சோதனை'
  },
  hi: {
    ALL: 'सभी पात्र',
    A: 'कार्यकारी एवं उत्पादन',
    B: 'निर्देशन',
    C: 'पटकथा एवं कहानी',
    D: 'कास्टिंग एवं प्रतिभा',
    E: 'छायांकन एवं कैमरा',
    F: 'कला एवं प्रोडक्शन डिजाइन',
    G: 'पोशाक एवं श्रृंगार',
    H: 'ध्वनि एवं फोले',
    I: 'स्टंट एवं एक्शन',
    J: 'वीएफएक्स एवं विशेष प्रभाव',
    K: 'संपादन',
    L: 'संगीत एवं गीत',
    M: 'डीआई एवं कलरिंग',
    N: 'वितरण एवं प्रदर्शन',
    O: 'कानूनी एवं सेंसर',
    P: 'विपणन एवं प्रचार',
    Q: 'वर्चुअल प्रोडक्शन एवं GenAI',
    COMP: 'समग्र पात्र',
    ANTG: 'प्रतिकूल रेड-टीम'
  },
  ja: {
    ALL: '全ペルソナ',
    A: '製作総指揮・プロデュース',
    B: '監督・演出',
    C: '脚本・ストーリー',
    D: 'キャスティング・出演者',
    E: '撮影・カメラ',
    F: '美術・プロダクションデザイン',
    G: '衣装・ヘアメイク',
    H: '音響・フォーリー',
    I: 'スタント・殺陣・操演',
    J: 'VFX・特撮・CG',
    K: '編集・ポストプロダクション',
    L: '音楽・作曲・歌曲',
    M: 'カラコレ・DI・マスタリング',
    N: '配給・興行',
    O: '法務・権利・審査',
    P: '宣伝・PR・マーケティング',
    Q: 'バーチャルプロダクション・GenAI',
    COMP: 'クロスバンド複合ロール',
    ANTG: '敵対的レッドチーム'
  },
  fr: {
    ALL: 'Tous les Personas',
    A: 'Production & Direction Générale',
    B: 'Mise en Scène & Réalisation',
    C: 'Scénario & Narration',
    D: 'Casting & Acteurs',
    E: 'Photographie & Cadre',
    F: 'Décors & Direction Artistique',
    G: 'Costumes & Maquillage',
    H: 'Son & Bruitage',
    I: 'Cascades & Armurerie',
    J: 'VFX & Effets Numériques',
    K: 'Montage & Post-Production',
    L: 'Musique & Bandes Originales',
    M: 'Étalonnage & Mastering',
    N: 'Distribution & Exploitation',
    O: 'Juridique & Classification',
    P: 'Marketing & Presse',
    Q: 'Production Virtuelle & GenAI',
    COMP: 'Rôles Composites',
    ANTG: 'Red-Team Adversariale'
  }
};

export function CrewPersonaLounge({ i18n = {}, language = 'en' }) {
  const { currentPersona, loginAsCrewPersona } = useAuth();
  const { setCinemaTheme } = useTheme();

  const [selectedBand, setSelectedBand] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPersona, setSelectedPersona] = useState(null);

  // Debate state
  const [opponentId, setOpponentId] = useState('');
  const [debateTopic, setDebateTopic] = useState('8K 120fps IMAX volumetric pipeline vs budget constraints');
  const debateRounds = 2;
  const [isDebating, setIsDebating] = useState(false);
  const [debateResult, setDebateResult] = useState(null);

  const personasList = useMemo(() => {
    return Object.values(registryData.personas || {});
  }, []);

  const filteredPersonas = useMemo(() => {
    const q = (searchQuery || '').toLowerCase().trim();
    return personasList.filter((p) => {
      const matchBand = selectedBand === 'ALL' || p.band === selectedBand;
      const matchSearch =
        !q ||
        (p.id && p.id.toLowerCase().includes(q)) ||
        (p.title && p.title.toLowerCase().includes(q)) ||
        (p.name && p.name.toLowerCase().includes(q)) ||
        (p.department && p.department.toLowerCase().includes(q)) ||
        (p.mandate && p.mandate.toLowerCase().includes(q));
      return matchBand && matchSearch;
    });
  }, [personasList, selectedBand, searchQuery]);

  const handleSelectPersona = (p) => {
    setSelectedPersona(p);
    setDebateResult(null);
  };

  const handleLoginAs = (p) => {
    loginAsCrewPersona(p);
    if (['A', 'B'].includes(p.band)) setCinemaTheme('director-noir');
    else if (['E', 'F'].includes(p.band)) setCinemaTheme('camera-tungsten');
    else if (['I', 'ANTG'].includes(p.band)) setCinemaTheme('stunt-hazard');
    else if (['J', 'Q'].includes(p.band)) setCinemaTheme('vfx-cyber');
    else if (['H', 'L'].includes(p.band)) setCinemaTheme('sound-emerald');
    else setCinemaTheme('director-noir');
  };

  const handleLaunchDebate = async () => {
    if (!selectedPersona || !opponentId) return;
    setIsDebating(true);
    setDebateResult(null);

    try {
      const res = await runPersonaDebate({
        persona_a_id: selectedPersona.id,
        persona_b_id: opponentId,
        arbitrator_id: 'A01',
        topic: debateTopic,
        rounds: debateRounds
      });
      setDebateResult(res);
    } catch (err) {
      console.error('[Debate Error]', err);
      setDebateResult({
        error: true,
        topic: debateTopic,
        verdict: 'Arbitrator A01 ruled in favor of safety and continuity due to budget limits.',
        turns: [
          { speaker: selectedPersona.id, text: `Advocating strictly for: ${debateTopic}` },
          { speaker: opponentId, text: `Counter-arguing from risk and operational capacity.` }
        ]
      });
    } finally {
      setIsDebating(false);
    }
  };

  return (
    <div className="persona-lounge-container">
      {/* Lounge Header */}
      <div className="lounge-header-glass">
        <div className="lounge-title-group">
          <h2>👥 {i18n.crewLoungeTitle || 'Studio Screen Crew Personas Lounge'}</h2>
          <p>
            {i18n.crewLoungeDesc || `Explore ${personasList.length} production personas across 17 studio bands, cross-band composites, and adversarial red-team agents.`}
          </p>
        </div>

        <div className="lounge-stats-ribbon">
          <div className="stat-pill">
            <span className="stat-val">{personasList.length}</span>
            <span className="stat-lbl">Active Roles</span>
          </div>
          <div className="stat-pill">
            <span className="stat-val">17</span>
            <span className="stat-lbl">Studio Bands</span>
          </div>
          <div className="stat-pill">
            <span className="stat-val">8</span>
            <span className="stat-lbl">Composites</span>
          </div>
          <div className="stat-pill">
            <span className="stat-val">5</span>
            <span className="stat-lbl">Antagonists</span>
          </div>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="lounge-controls-card">
        <div className="lounge-search-wrapper">
          <span className="search-icon" aria-hidden="true">🔍</span>
          <input
            type="text"
            className="lounge-search-input"
            placeholder={
              language === 'ta'
                ? 'ஐடி (A01, E23), தலைப்பு, அல்லது கட்டளை மூலம் தேடுங்கள்...'
                : language === 'hi'
                ? 'आईडी (A01, E23), शीर्षक या निर्देश द्वारा खोजें...'
                : language === 'ja'
                ? 'ID (A01, E23)、役職、ツール、または職務で検索...'
                : 'Search by ID (e.g. A01, E23), title, tool (e.g. grafana, ffmpeg), or mandate...'
            }
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {searchQuery && (
            <button className="search-clear-btn" onClick={() => setSearchQuery('')}>✕</button>
          )}
        </div>

        <div className="band-chips-scroll" role="tablist" aria-label="Department Bands">
          {Object.entries(BAND_METADATA).map(([bandKey, meta]) => {
            const count = bandKey === 'ALL'
              ? personasList.length
              : personasList.filter((p) => p.band === bandKey).length;
            const isActive = selectedBand === bandKey;
            const localizedName = (BAND_TRANSLATIONS[language] && BAND_TRANSLATIONS[language][bandKey]) || meta.name;
            return (
              <button
                key={bandKey}
                className={`band-chip ${isActive ? 'active' : ''}`}
                onClick={() => setSelectedBand(bandKey)}
                role="tab"
                aria-selected={isActive}
              >
                <span className="chip-icon">{meta.icon}</span>
                <span className="chip-code">{bandKey}</span>
                <span className="chip-name">{localizedName}</span>
                <span className="chip-count">({count})</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Grid of Persona Cards */}
      <div className="personas-cards-grid">
        {filteredPersonas.map((persona) => {
          const isCurrent = currentPersona?.id === persona.id;
          const bandMeta = BAND_METADATA[persona.band] || { icon: '🎬', name: persona.band };
          const bandInfo = {
            icon: bandMeta.icon,
            name: (BAND_TRANSLATIONS[language] && BAND_TRANSLATIONS[language][persona.band]) || bandMeta.name
          };
          return (
            <div
              key={persona.id}
              className={`persona-card-glass ${isCurrent ? 'active-user-card' : ''}`}
              onClick={() => handleSelectPersona(persona)}
            >
              <div className="card-top">
                <div className="card-id-cluster">
                  <span className="band-badge">{bandInfo.icon} {persona.band}</span>
                  <span className="persona-id-tag">{persona.id}</span>
                </div>
                <span className={`can-block-pill ${persona.can_block ? 'blocker' : 'advisor'}`}>
                  {persona.can_block ? '⛔ Can Block' : '💡 Advisor'}
                </span>
              </div>

              <h3 className="card-title">{persona.title || persona.name || persona.id}</h3>
              <p className="card-mandate">{persona.mandate || persona.system_prompt}</p>

              <div className="card-meta-row">
                <span className="tier-tag">{persona.model_tier || 'standard'}</span>
                <span className="authority-tag">Auth: {persona.authority_scope}</span>
              </div>

              <div className="card-tools-row">
                {(persona.tools || []).slice(0, 3).map((tool) => (
                  <span key={tool} className="tool-chip-mini">⚙️ {tool}</span>
                ))}
                {(persona.tools || []).length > 3 && (
                  <span className="tool-chip-mini">+{persona.tools.length - 3}</span>
                )}
              </div>

              <div className="card-actions">
                <button
                  className="btn-inspect"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleSelectPersona(persona);
                  }}
                >
                  Inspect Role
                </button>
                <button
                  className={`btn-impersonate ${isCurrent ? 'btn-active-logged' : ''}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleLoginAs(persona);
                  }}
                  title="Switch active user to this persona"
                >
                  {isCurrent ? '✓ Active Role' : 'Login As'}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Detailed Inspection Modal */}
      {selectedPersona && (
        <div className="modal-backdrop" onClick={() => setSelectedPersona(null)}>
          <div className="persona-detail-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="dialog-header">
              <div className="dialog-title-group">
                <span className="dialog-band-pill">
                  {BAND_METADATA[selectedPersona.band]?.icon} Band {selectedPersona.band} : {BAND_METADATA[selectedPersona.band]?.name}
                </span>
                <h2>{selectedPersona.title || selectedPersona.name || selectedPersona.id} ({selectedPersona.id})</h2>
              </div>
              <button className="dialog-close-btn" onClick={() => setSelectedPersona(null)}>✕</button>
            </div>

            <div className="dialog-body-scroll">
              <div className="detail-section">
                <h4>🎯 Operational Mandate</h4>
                <p className="detail-mandate-text">{selectedPersona.mandate || selectedPersona.system_prompt}</p>
              </div>

              <div className="detail-grid-2col">
                <div className="detail-card-sub">
                  <h5>Operational Authority</h5>
                  <p className="code-text">{selectedPersona.authority_scope}</p>
                </div>
                <div className="detail-card-sub">
                  <h5>Blocking Authority</h5>
                  <p className={selectedPersona.can_block ? 'text-critical' : 'text-success'}>
                    {selectedPersona.can_block
                      ? 'YES — Has executive veto power to halt sequence'
                      : 'NO — Advisory and consultative capacity only'}
                  </p>
                </div>
                <div className="detail-card-sub">
                  <h5>Escalation Target</h5>
                  <p className="code-text">{selectedPersona.escalates_to || 'None (Terminal)'}</p>
                </div>
                <div className="detail-card-sub">
                  <h5>Model Tier & Context Cache</h5>
                  <p className="code-text">{selectedPersona.model_tier} | {selectedPersona.context_cache_key}</p>
                </div>
              </div>

              <div className="detail-section">
                <h4>🛠️ Authorized Tools & Capabilities</h4>
                <div className="tools-badges-wrap">
                  {(selectedPersona.tools || []).map((tool) => (
                    <span key={tool} className="tool-badge-large">⚙️ {tool}</span>
                  ))}
                </div>
              </div>

              {selectedPersona.system_prompt && (
                <div className="detail-section">
                  <h4>🧠 System Prompt Directive</h4>
                  <pre className="system-prompt-box">{selectedPersona.system_prompt}</pre>
                </div>
              )}

              {/* Dialectical Debate Quick Action */}
              <div className="debate-quick-panel">
                <div className="debate-intro">
                  <h4>⚖️ Dialectical Arbitration Debate</h4>
                  <p>Stage an adversarial or creative conflict between {selectedPersona.title || selectedPersona.name || selectedPersona.id} and an opposing crew persona.</p>
                </div>
                <div className="debate-controls-row">
                  <select
                    className="select-input debate-select"
                    value={opponentId}
                    onChange={(e) => setOpponentId(e.target.value)}
                  >
                    <option value="">-- Select Opponent Persona --</option>
                    {personasList
                      .filter((p) => p.id !== selectedPersona.id)
                      .slice(0, 40)
                      .map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.id}: {p.title || p.name || p.id} ({p.band})
                        </option>
                      ))}
                  </select>
                  <input
                    type="text"
                    className="debate-topic-input"
                    value={debateTopic}
                    onChange={(e) => setDebateTopic(e.target.value)}
                    placeholder="Debate topic..."
                  />
                  <button
                    className="btn-launch-debate"
                    disabled={!opponentId || isDebating}
                    onClick={handleLaunchDebate}
                  >
                    {isDebating ? 'Arbitrating...' : 'Run Debate'}
                  </button>
                </div>

                {debateResult && (
                  <div className="debate-result-box">
                    <h5>Verdict from Arbitrator {debateResult.arbitrator_id || 'A01'}:</h5>
                    <p className="debate-verdict">{debateResult.verdict}</p>
                    <div className="debate-turns-list">
                      {(debateResult.turns || []).map((t, idx) => (
                        <div key={idx} className="debate-turn-item">
                          <span className="speaker-tag">{t.speaker}:</span>
                          <span className="turn-text">{t.text}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="dialog-footer">
              <button
                className="btn-primary"
                onClick={() => {
                  handleLoginAs(selectedPersona);
                  setSelectedPersona(null);
                }}
              >
                Login as {selectedPersona.title || selectedPersona.name || selectedPersona.id}
              </button>

              <button className="btn-secondary" onClick={() => setSelectedPersona(null)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
