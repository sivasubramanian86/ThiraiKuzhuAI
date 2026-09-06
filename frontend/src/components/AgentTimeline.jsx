import React from 'react';
import { DEPT_ICONS } from '../constants/departments';

/**
 * AgentTimeline Component
 * Renders the chronological reasoning steps of the multi-agent crew.
 */
export function AgentTimeline({ steps, i18n }) {
  return (
    <section className="timeline-section" aria-label="Crew Reasoning Timeline">
      <h3 className="section-heading">Multi-Agent Deliberation & MCP Triage</h3>
      <div className="agent-timeline" id="agent-timeline">
        {steps.length === 0 ? (
          <div className="timeline-placeholder">
            {i18n.timelinePlaceholder}
          </div>
        ) : (
          steps.map((step, idx) => {
            const icon = DEPT_ICONS[step.department] || DEPT_ICONS.DEFAULT;
            const timeFormatted = step.timestamp && typeof step.timestamp === 'string' && step.timestamp.includes('T')
              ? step.timestamp.split('T')[1].slice(0, 8)
              : `00:00:0${idx + 1}`;

            return (
              <div
                key={idx}
                className="timeline-card"
                role="article"
                aria-label={`${step.agent_name || 'Agent'} deliberation step`}
              >
                <div className="timeline-top">
                  <span className="dept-tag">
                    {icon} {step.agent_name}
                  </span>
                  <span className="step-label">T+{timeFormatted}</span>
                </div>
                <div className="timeline-content">{step.thought}</div>
                {step.telemetry_action && (
                  <div className="telemetry-snippet">{step.telemetry_action}</div>
                )}
              </div>
            );
          })
        )}
      </div>
    </section>
  );
}
