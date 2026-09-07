import React from 'react';
import { IncidentSidebar } from './IncidentSidebar';
import { IncidentHero } from './IncidentHero';
import { AgentTimeline } from './AgentTimeline';
import { MitigationPanel } from './MitigationPanel';
import { WalkieTalkie } from './WalkieTalkie';
import { GrafanaPanelEmbed } from './GrafanaPanelEmbed';

/**
 * StudioControlRoom Component
 * Encapsulates the live multi-agent incident investigation workspace.
 */
export function StudioControlRoom({
  incidents,
  activeIncident,
  onSelectIncident,
  onInjectChaos,
  isInvestigating,
  onDispatch,
  agentSteps,
  mitigationPlan,
  isApplying,
  mitigationApplied,
  statusMessage,
  onApplyMitigation,
  walkieMessages,
  i18n
}) {
  return (
    <div className="workspace-grid" role="region" aria-label="Studio Incident Control Room">
      {/* Left Column: Incident Queue & Chaos Injection */}
      <IncidentSidebar
        incidents={incidents}
        selectedIncidentId={activeIncident ? activeIncident.id : null}
        onSelectIncident={onSelectIncident}
        onInjectChaos={onInjectChaos}
        i18n={i18n}
      />

      {/* Center Column: Incident Hero, Agent Steps, Mitigation Actions */}
      <main id="main-content" className="main-canvas" role="main" aria-label="Incident Investigation Canvas">
        <IncidentHero
          incident={activeIncident}
          isInvestigating={isInvestigating}
          onDispatch={onDispatch}
          i18n={i18n}
        />

        <AgentTimeline steps={agentSteps} i18n={i18n} />

        <MitigationPanel
          mitigationPlan={mitigationPlan}
          boxOfficeRisk={activeIncident ? activeIncident.box_office_at_risk_usd : 0}
          isApplying={isApplying}
          mitigationApplied={mitigationApplied}
          statusMessage={statusMessage}
          onApplyMitigation={onApplyMitigation}
          i18n={i18n}
        />
      </main>

      {/* Right Column: Radio Walkie-Talkie & Live Grafana Panel */}
      <aside className="right-rail" role="complementary" aria-label="Studio Walkie Talkie and Telemetry">
        <WalkieTalkie messages={walkieMessages} i18n={i18n} />
        <GrafanaPanelEmbed
          promqlQuery={activeIncident?.telemetry?.promql_metric}
          alertLabel={
            activeIncident?.telemetry?.grafana_alert_uid
              ? `${activeIncident.telemetry.grafana_alert_uid.split('-')[1] || 'Alert'} Spike`
              : '504 Spike: 8.4%'
          }
        />
      </aside>
    </div>
  );
}
