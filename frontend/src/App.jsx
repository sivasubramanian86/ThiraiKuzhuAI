import React, { useState, useEffect, useRef, useCallback } from 'react';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { AppShell } from './components/AppShell';
import { StudioControlRoom } from './components/StudioControlRoom';
import { CrewPersonaLounge } from './components/CrewPersonaLounge';
import { DynamicSmeStudio } from './components/DynamicSmeStudio';
import { AntagonistLab } from './components/AntagonistLab';
import { MultiModalMediaStudio } from './components/MultiModalMediaStudio';
import { GrafanaObservability } from './components/GrafanaObservability';
import { FAQHelp } from './components/FAQHelp';
import { AboutThiraiKuzhu } from './components/AboutThiraiKuzhu';
import { SettingsStudio } from './components/SettingsStudio';
import { ContentShieldStudio } from './components/ContentShieldStudio';
import AnimationCharacterStudio from './components/AnimationCharacterStudio';
import VirtualArtStudio from './components/VirtualArtStudio';
import {
  fetchProjects,
  fetchProjectCRI,
  fetchIncidents,
  dispatchInvestigation,
  applyMitigation,
  streamMission
} from './services/api';
import { getTranslations, SUPPORTED_LANGUAGES } from './i18n';
import { DEPT_ICONS } from './constants/departments';

export function App() {
  // Navigation Tab State
  const [activeTab, setActiveTab] = useState('control_room');

  // Localization & State
  const [language, setLanguage] = useState('en');
  const i18n = getTranslations(language);

  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState('baahubali-3');
  const [criScore, setCriScore] = useState(94.5);

  const [incidents, setIncidents] = useState([]);
  const [activeIncident, setActiveIncident] = useState(null);

  const [agentSteps, setAgentSteps] = useState([]);
  const [walkieMessages, setWalkieMessages] = useState([
    { speaker: '[Control Room]', text: 'Channel open. Ready for director directive.', isStatic: true }
  ]);

  const [mitigationPlan, setMitigationPlan] = useState([]);
  const [isInvestigating, setIsInvestigating] = useState(false);
  const [isApplying, setIsApplying] = useState(false);
  const [mitigationApplied, setMitigationApplied] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  // Symmetrical resource handles for ZERO memory leaks
  const sseCleanupRef = useRef(null);

  // 1. Initial hydration with AbortController
  useEffect(() => {
    const controller = new AbortController();

    async function initData() {
      try {
        const [projList, incList] = await Promise.all([
          fetchProjects(controller.signal),
          fetchIncidents(controller.signal)
        ]);

        if (projList && projList.length > 0) {
          setProjects(projList);
          setSelectedProjectId(projList[0].id);
        }

        if (incList && incList.length > 0) {
          setIncidents(incList);
          setActiveIncident(incList[0]);
        }
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.warn('[Thirai Kuzhu AI] Initial data load warning:', err);
        }
      }
    }

    initData();

    return () => {
      controller.abort(); // Cancel pending network requests on unmount
    };
  }, []);

  // 2. Fetch CRI whenever selected project changes
  useEffect(() => {
    if (!selectedProjectId) return;
    const controller = new AbortController();

    async function updateCRI() {
      try {
        const report = await fetchProjectCRI(selectedProjectId, controller.signal);
        if (report) {
          if (typeof report.cri_score === 'number') {
            setCriScore(report.cri_score);
          } else if (typeof report.composite_cri_score === 'number') {
            setCriScore(report.composite_cri_score);
          }
        }
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.warn('[Thirai Kuzhu AI] CRI fetch warning:', err);
        }
      }
    }

    updateCRI();

    return () => {
      controller.abort();
    };
  }, [selectedProjectId]);

  // 3. Clean up SSE stream on unmount
  useEffect(() => {
    return () => {
      if (sseCleanupRef.current) {
        sseCleanupRef.current();
        sseCleanupRef.current = null;
      }
    };
  }, []);

  // Handle incident selection
  const handleSelectIncident = useCallback((inc) => {
    setActiveIncident(inc);
    setAgentSteps([]);
    setMitigationPlan([]);
    setMitigationApplied(false);
    setStatusMessage('');
  }, []);

  // Append a walkie-talkie communication entry
  const appendWalkie = useCallback((speaker, text) => {
    setWalkieMessages((prev) => [...prev, { speaker, text, isStatic: false }]);
  }, []);

  // Dispatch multi-agent investigation
  const handleDispatch = useCallback(async () => {
    if (!activeIncident) return;

    setIsInvestigating(true);
    setAgentSteps([]);
    setMitigationPlan([]);
    setMitigationApplied(false);
    setStatusMessage('');

    appendWalkie(
      '[1st AD]',
      'Calling Thirai Kuzhu crew to active incident channel. Standby for director triage.'
    );

    // Close any previous SSE stream
    if (sseCleanupRef.current) {
      sseCleanupRef.current();
      sseCleanupRef.current = null;
    }

    let streamCompleted = false;

    // Connect to SSE stream
    const cleanup = streamMission(
      activeIncident.id,
      (step) => {
        setAgentSteps((prev) => [...prev, step]);
        const icon = DEPT_ICONS[step.department] || '📻';
        appendWalkie(`${icon} ${step.agent_name}`, step.walkie_talkie_dialogue || step.thought);
      },
      (completion) => {
        streamCompleted = true;
        setIsInvestigating(false);
        if (completion && completion.mitigation_plan) {
          setMitigationPlan(completion.mitigation_plan);
        } else {
          fallbackRestInvestigation(activeIncident.id);
        }
      },
      (err) => {
        console.warn('[Thirai Kuzhu AI] SSE stream ended/error:', err);
        if (!streamCompleted) {
          fallbackRestInvestigation(activeIncident.id);
        }
      }
    );

    sseCleanupRef.current = cleanup;
  }, [activeIncident, appendWalkie]);

  // Fallback REST investigation if SSE finishes without completion payload
  const fallbackRestInvestigation = useCallback(async (incidentId) => {
    try {
      const data = await dispatchInvestigation(incidentId, language);
      if (data) {
        if (data.agent_timeline && data.agent_timeline.length > 0) {
          setAgentSteps(data.agent_timeline);
        }
        if (data.mitigation_plan) {
          setMitigationPlan(data.mitigation_plan);
        }
      }
    } catch (err) {
      console.error('[Thirai Kuzhu AI] Fallback investigation error:', err);
    } finally {
      setIsInvestigating(false);
    }
  }, [language]);

  // Handle mitigation execution
  const handleApplyMitigation = useCallback(async () => {
    if (!activeIncident) return;

    setIsApplying(true);
    setStatusMessage('');

    try {
      const res = await applyMitigation({
        incident_id: activeIncident.id,
        action_taken: 'Re-routed origin transcoder pool to secondary node cluster and flushed cache.',
        annotation_text: 'Thirai Kuzhu AI: Applied transcode failover. CDN 504 stall averted.',
        dashboard_uid: 'cinema-stream-master'
      });

      if (res && res.success) {
        setMitigationApplied(true);
        setStatusMessage(`[SUCCESS] ${res.message || 'Mitigation applied'} (Grafana Annotation ID: ${res.grafana_annotation_id || 'ann-101'})`);
        appendWalkie(
          "🎬 Director's Cut",
          'All channels copy: Mitigation executed. Quality confirmed. Sequence preserved.'
        );
      }
    } catch (err) {
      console.error('[Thirai Kuzhu AI] Apply mitigation error:', err);
      setStatusMessage('Error applying mitigation.');
    } finally {
      setIsApplying(false);
    }
  }, [activeIncident, appendWalkie]);

  // Handle synthetic chaos injection
  const handleInjectChaos = useCallback((scenarioKey) => {
    const chaosScenarios = {
      ott_premiere_spike: {
        id: 'INC-2026-CHAOS-01',
        project_title: 'Chronicles of Surya: The Solar Gate',
        sequence_affected: 'Seq 22 - Waterfall Gate Invasion',
        culture: 'MYTHIC_EPIC',
        genre_track: 'EPIC_HISTORICAL',
        severity: 'CRITICAL',
        telemetry: {
          grafana_alert_uid: 'Alert-OTT-504-ChaosSpike',
          promql_metric: "sum(rate(cdn_requests_total{status=~'5..'}[1m])) > 12.5%",
          tempo_trace_id: 'chaos-trace-8a9b1c'
        },
        cinematic_narrative:
          'Massive CDN 504 error burst simulated during the high-stakes battle climax. 60,000 streams impacted.',
        box_office_at_risk_usd: 52000.0,
        director_directive: 'Switch CDN origin to backup region and execute edge cache invalidate.'
      },
      vfx_crash: {
        id: 'INC-2026-CHAOS-02',
        project_title: 'Abyssal Frontier: Trench Recon',
        sequence_affected: 'Seq 08 - Bioluminescent Biolab Strike',
        culture: 'HOLLYWOOD_TENTPOLE',
        genre_track: 'ACTION_STUNTS',
        severity: 'HIGH',
        telemetry: {
          grafana_alert_uid: 'Alert-VFX-CUDA-OOM',
          promql_metric: 'gpu_vram_usage_bytes / gpu_vram_total_bytes > 0.98',
          tempo_trace_id: 'vfx-cuda-oom-04f'
        },
        cinematic_narrative:
          'Simulated 8K IMAX render pipeline CUDA Out-Of-Memory failure across 14 GPU nodes.',
        box_office_at_risk_usd: 28000.0,
        director_directive: 'Downsample volumetric water particles by 15% and redistribute tile rendering.'
      },
      wuxia_foley_lag: {
        id: 'INC-2026-CHAOS-03',
        project_title: 'Whisper of the Crane: Wuxia Chronicles',
        sequence_affected: 'Seq 05 - Bamboo Forest Sword Duel',
        culture: 'EAST_ASIAN_ANIME',
        genre_track: 'MARTIAL_ARTS_WUXIA',
        severity: 'MEDIUM',
        telemetry: {
          grafana_alert_uid: 'Alert-Audio-Foley-Desync',
          promql_metric: 'dolby_atmos_clock_drift_ms > 45',
          tempo_trace_id: 'foley-desync-882'
        },
        cinematic_narrative:
          '48ms Dolby Atmos audio clock drift detected during bamboo combat sword clashes.',
        box_office_at_risk_usd: 15000.0,
        director_directive: 'Re-lock SMPTE timecode sync generator and re-bake Atmos spatial bed.'
      },
      anime_sakuga_stall: {
        id: 'INC-2026-CHAOS-04',
        project_title: 'Whisper of the Crane: Wuxia Chronicles',
        sequence_affected: 'Seq 19 - Moonlight Duel Sakuga Sequence',
        culture: 'EAST_ASIAN_ANIME',
        genre_track: 'MARTIAL_ARTS_WUXIA',
        severity: 'HIGH',
        telemetry: {
          grafana_alert_uid: 'Alert-Sakuga-Frame-Drop',
          promql_metric: 'playback_frame_drop_ratio > 0.05',
          tempo_trace_id: 'sakuga-drop-991'
        },
        cinematic_narrative:
          'Frame drop ratio spiked to 7.5% during high-energy keyframe animation cut.',
        box_office_at_risk_usd: 22000.0,

        director_directive:
          'Increase dynamic buffer window to 3000ms and pre-render keyframe interpolation.'
      }
    };

    const newInc = chaosScenarios[scenarioKey] || chaosScenarios.ott_premiere_spike;
    setActiveIncident(newInc);
    setAgentSteps([]);
    setMitigationPlan([]);
    setMitigationApplied(false);
    setStatusMessage('');
    appendWalkie('⚠️ Chaos Sim', `Injected ${newInc.sequence_affected} [${newInc.telemetry.grafana_alert_uid}]`);
  }, [appendWalkie]);

  return (
    <AuthProvider>
      <ThemeProvider>
        <div>
          <a href="#main-content" className="skip-link">
            Skip to main content
          </a>

          <AppShell
            activeTab={activeTab}
            onTabChange={setActiveTab}
            projects={projects}
            selectedProject={selectedProjectId}
            onSelectProject={setSelectedProjectId}
            criScore={criScore}
            language={language}
            onChangeLanguage={setLanguage}
            supportedLanguages={SUPPORTED_LANGUAGES}
            i18n={i18n}
          >
            {activeTab === 'control_room' && (
              <StudioControlRoom
                incidents={incidents}
                activeIncident={activeIncident}
                onSelectIncident={handleSelectIncident}
                onInjectChaos={handleInjectChaos}
                isInvestigating={isInvestigating}
                onDispatch={handleDispatch}
                agentSteps={agentSteps}
                mitigationPlan={mitigationPlan}
                isApplying={isApplying}
                mitigationApplied={mitigationApplied}
                statusMessage={statusMessage}
                onApplyMitigation={handleApplyMitigation}
                walkieMessages={walkieMessages}
                i18n={i18n}
              />
            )}

            {activeTab === 'crew_lounge' && <CrewPersonaLounge />}

            {activeTab === 'anime_vault' && <AnimationCharacterStudio />}

            {activeTab === 'art_director' && <VirtualArtStudio />}

            {activeTab === 'sme_studio' && <DynamicSmeStudio />}

            {activeTab === 'antagonist_lab' && <AntagonistLab />}

            {activeTab === 'multimodal_studio' && <MultiModalMediaStudio />}

            {activeTab === 'content_shield' && <ContentShieldStudio />}

            {activeTab === 'observability' && <GrafanaObservability />}

            {activeTab === 'faq_help' && <FAQHelp />}

            {activeTab === 'about' && <AboutThiraiKuzhu />}

            {activeTab === 'settings' && <SettingsStudio />}
          </AppShell>
        </div>
      </ThemeProvider>
    </AuthProvider>
  );
}
