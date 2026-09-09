import React, { useState, useMemo } from 'react';
import { getLocalizedFaqs } from '../i18n/faqs';

const SEARCH_PLACEHOLDERS = {
  en: 'Search questions by keyword (e.g. can_block, SME, debate, Grafana, red-team)...',
  ta: 'முக்கிய வார்த்தை மூலம் கேள்விகளைத் தேடுங்கள் (எ.கா. can_block, SME, விவாதம், Grafana)...',
  hi: 'कीवर्ड द्वारा प्रश्न खोजें (उदा. can_block, SME, बहस, Grafana)...',
  ja: 'キーワードで質問を検索（例：can_block, SME, ディベート, Grafana）...',
  fr: 'Rechercher par mot-clé (ex: can_block, SME, débat, Grafana)...',
  de: 'Fragen nach Stichwort suchen (z.B. can_block, SME, Debatte, Grafana)...',
  es: 'Buscar preguntas por palabra clave (ej. can_block, SME, debate, Grafana)...',
  te: 'కీవర్డ్ ద్వారా ప్రశ్నలను శోధించండి (ఉదా. can_block, SME, చర్చ, Grafana)...',
  ko: '키워드로 질문 검색 (예: can_block, SME, 토론, Grafana)...',
  zh: '按关键词搜索问题（例如：can_block、SME、辩论、Grafana）...',
  ar: 'البحث عن الأسئلة بالكلمات الرئيسية (مثل can_block، SME، مناظرة، Grafana)...'
};

export function FAQHelp({ i18n = {}, language = 'en' }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [openIndex, setOpenIndex] = useState(0);

  const activeFaqs = useMemo(() => getLocalizedFaqs(language), [language]);

  const filteredFaqs = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    if (!q) return activeFaqs;
    return activeFaqs.filter(
      (f) =>
        f.question.toLowerCase().includes(q) ||
        f.answer.toLowerCase().includes(q) ||
        f.category.toLowerCase().includes(q)
    );
  }, [searchQuery, activeFaqs]);

  const searchPlaceholder = SEARCH_PLACEHOLDERS[language] || SEARCH_PLACEHOLDERS.en;

  return (
    <div className="faq-container">
      {/* Header */}
      <div className="faq-header-glass">
        <div className="faq-title-group">
          <h2>❓ {i18n.faqTitle || i18n.faq_title || 'Frequently Asked Questions & Studio Help'}</h2>
          <p>
            {i18n.faqDesc || i18n.faq_desc || 'Find comprehensive explanations of Thirai Kuzhu AI architecture, 17-band crew hierarchy, dialectical debate rules, and Grafana telemetry.'}
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
            placeholder={searchPlaceholder}
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
