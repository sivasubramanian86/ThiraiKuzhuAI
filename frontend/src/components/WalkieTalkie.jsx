import React, { useEffect, useRef } from 'react';

/**
 * WalkieTalkie Component
 * Real-time radio channel showing on-set crew communications with auto-scroll.
 */
export function WalkieTalkie({ messages, i18n }) {
  const streamRef = useRef(null);

  // Auto-scroll to bottom as new messages arrive
  useEffect(() => {
    if (streamRef.current) {
      streamRef.current.scrollTop = streamRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <section className="card-glass walkie-talkie-card">
      <div className="card-header">
        <div className="radio-header">
          <span className="radio-icon" aria-hidden="true">📻</span>
          <h3 className="panel-subheading">{i18n.walkieTitle}</h3>
        </div>
        <span className="radio-freq">462.5625 MHz</span>
      </div>
      <p className="panel-caption">{i18n.walkieDesc}</p>

      <div className="walkie-stream" id="walkie-stream" ref={streamRef} role="log" aria-live="polite" aria-relevant="additions" aria-label="On-set crew communications log">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`walkie-entry ${msg.isStatic ? 'radio-static' : 'active-radio'}`}
          >
            <span className="radio-speaker">{msg.speaker}:</span> {msg.text}
          </div>
        ))}
      </div>
    </section>
  );
}
