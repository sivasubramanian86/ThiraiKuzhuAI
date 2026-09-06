import React from 'react';

/**
 * MitigationPanel Component
 * Displays actionable director recommendations and executes one-click Grafana annotation.
 */
export function MitigationPanel({
  mitigationPlan,
  boxOfficeRisk,
  isApplying,
  mitigationApplied,
  statusMessage,
  onApplyMitigation,
  i18n
}) {
  if (!mitigationPlan || mitigationPlan.length === 0) return null;

  return (
    <section className="mitigation-section card-glass" id="mitigation-section" aria-labelledby="mitigation-heading">
      <div className="mitigation-header">
        <h3 className="section-heading" id="mitigation-heading">{i18n.mitigationHeading}</h3>
        <span className="box-office-pill" id="box-office-protected">
          {i18n.boxOfficeProtected}: ${boxOfficeRisk ? boxOfficeRisk.toLocaleString() : '38,500'}
        </span>
      </div>

      <ul className="mitigation-list" id="mitigation-list">
        {mitigationPlan.map((action, idx) => (
          <li key={idx} className="mitigation-item">
            <span className="step-num">#{idx + 1}</span>
            <span className="step-text">{action}</span>
          </li>
        ))}
      </ul>

      <div className="mitigation-actions">
        <button
          id="btn-apply-mitigation"
          className="btn btn-accent"
          onClick={onApplyMitigation}
          disabled={isApplying || mitigationApplied}
          aria-busy={isApplying}
          aria-label="Apply mitigation and annotate Grafana"
        >
          {isApplying
            ? i18n.applyingBtn
            : mitigationApplied
            ? i18n.appliedBtn
            : i18n.applyBtn}
        </button>
        {statusMessage && (
          <span className="annotation-status-text" id="annotation-status-text" role="status" aria-live="polite">
            {statusMessage}
          </span>
        )}
      </div>
    </section>
  );
}
