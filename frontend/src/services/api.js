/**
 * Thirai Kuzhu AI — API Client Service
 * 
 * Strict Resource Lifecycle & Memory Leak Prevention:
 * - Uses AbortController signals for cancellation of stale async fetches.
 * - Manages EventSource streams with explicit close() lifecycle handles.
 */

const BASE_URL = '';

/**
 * Fetches all registered studio projects.
 * @param {AbortSignal} [signal] Optional abort signal for cancellation.
 * @returns {Promise<Array>} List of projects.
 */
export async function fetchProjects(signal) {
  const res = await fetch(`${BASE_URL}/api/projects`, { signal });
  if (!res.ok) {
    throw new Error(`Failed to fetch projects: ${res.status}`);
  }
  return await res.json();
}

/**
 * Fetches Cinematic Readiness Index (CRI) report for a project.
 * @param {string} projectId Target production identifier.
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Object>} CRI assessment.
 */
export async function fetchProjectCRI(projectId, signal) {
  const res = await fetch(`${BASE_URL}/api/evaluation/cri/${projectId}`, { signal });
  if (!res.ok) {
    throw new Error(`Failed to fetch CRI evaluation: ${res.status}`);
  }
  return await res.json();
}

/**
 * Fetches all tracked studio incidents.
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Array>} List of incidents.
 */
export async function fetchIncidents(signal) {
  const res = await fetch(`${BASE_URL}/api/incidents`, { signal });
  if (!res.ok) {
    throw new Error(`Failed to fetch incidents: ${res.status}`);
  }
  return await res.json();
}

/**
 * Dispatches an incident investigation mission via REST.
 * @param {string} incidentId Target incident identifier.
 * @param {string} [language='en'] Desired localization language.
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Object>} Investigation results.
 */
export async function dispatchInvestigation(incidentId, language = 'en', signal) {
  const res = await fetch(`${BASE_URL}/api/missions/investigate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ incident_id: incidentId, target_language: language }),
    signal
  });
  if (!res.ok) {
    throw new Error(`Investigation request failed: ${res.status}`);
  }
  return await res.json();
}

/**
 * Applies director mitigation action and registers Grafana annotation.
 * @param {Object} payload Mitigation payload {incident_id, action_taken, annotation_text, dashboard_uid}.
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Object>} Mitigation result.
 */
export async function applyMitigation(payload, signal) {
  const res = await fetch(`${BASE_URL}/api/mitigations/apply`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    signal
  });
  if (!res.ok) {
    throw new Error(`Apply mitigation failed: ${res.status}`);
  }
  return await res.json();
}

/**
 * Connects to live SSE mission stream with explicit cleanup handle.
 * 
 * @param {string} incidentId Target incident identifier.
 * @param {Function} onStep Callback invoked for each agent thought step.
 * @param {Function} onComplete Callback invoked when investigation completes.
 * @param {Function} onError Callback invoked on stream errors.
 * @returns {Function} Cleanup function that guarantees the EventSource is closed.
 */
export function streamMission(incidentId, onStep, onComplete, onError) {
  const eventSource = new EventSource(`${BASE_URL}/api/missions/${incidentId}/stream`);

  eventSource.onmessage = (event) => {
    try {
      const step = JSON.parse(event.data);
      if (step.agent_name) {
        onStep(step);
      }
    } catch (err) {
      console.warn('[Thirai Kuzhu AI] SSE JSON parse warning:', err);
    }
  };

  eventSource.addEventListener('complete', (event) => {
    try {
      const completion = JSON.parse(event.data);
      onComplete(completion);
    } catch {
      onComplete(null);
    }
    eventSource.close();
  });

  eventSource.onerror = (err) => {
    eventSource.close();
    if (onError) onError(err);
  };

  // Return unsubscribe / cleanup function
  return () => {
    if (eventSource.readyState !== EventSource.CLOSED) {
      eventSource.close();
    }
  };
}

/**
 * Fetches persona catalog from the backend registry.
 * @param {string} [band] Optional band filter ('A'..'Q', 'COMP', 'ANTG').
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Object>} Object with count and personas array.
 */
export async function fetchPersonas(band = '', signal) {
  const query = band ? `?band=${encodeURIComponent(band)}` : '';
  const res = await fetch(`${BASE_URL}/api/v1/personas${query}`, { signal });
  if (!res.ok) {
    throw new Error(`Failed to fetch personas: ${res.status}`);
  }
  return await res.json();
}

/**
 * Fetches a single persona by ID.
 * @param {string} personaId Unique persona ID (e.g. 'A01', 'COMP01', 'ANTG01').
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Object>} Persona definition.
 */
export async function fetchPersonaById(personaId, signal) {
  const res = await fetch(`${BASE_URL}/api/v1/personas/${encodeURIComponent(personaId)}`, { signal });
  if (!res.ok) {
    throw new Error(`Failed to fetch persona ${personaId}: ${res.status}`);
  }
  return await res.json();
}

/**
 * Dynamically spawns a subject-matter expert persona for screenplay requirements.
 * @param {Object} payload {scene_description, domain_focus, parent_persona_id}
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Object>} Spawned SME specification.
 */
export async function spawnDynamicSme(payload, signal) {
  const res = await fetch(`${BASE_URL}/api/v1/personas/sme/spawn`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    signal
  });
  if (!res.ok) {
    throw new Error(`Failed to spawn SME: ${res.status}`);
  }
  return await res.json();
}

/**
 * Runs a dialectical arbitration debate between two opposing personas.
 * @param {Object} payload {persona_a_id, persona_b_id, arbitrator_id, topic, rounds}
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Object>} Debate outcome and verdict.
 */
export async function runPersonaDebate(payload, signal) {
  const res = await fetch(`${BASE_URL}/api/v1/personas/debate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    signal
  });
  if (!res.ok) {
    throw new Error(`Debate execution failed: ${res.status}`);
  }
  return await res.json();
}

/**
 * Simulates red-team adversary attacks against film production.
 * @param {Object} payload {antagonist_id, target_production, attack_vector, simulation_intensity}
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Object>} Adversary simulation report.
 */
export async function runAntagonistSimulation(payload, signal) {
  const res = await fetch(`${BASE_URL}/api/v1/personas/antagonist/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    signal
  });
  if (!res.ok) {
    throw new Error(`Antagonist simulation failed: ${res.status}`);
  }
  return await res.json();
}

/**
 * Triggers multimodal asset analysis (Script, Storyboard, Foley/Audio, Rushes/Video).
 * @param {Object} payload {modality, sample_id, filename, analysis_depth}
 * @param {AbortSignal} [signal] Optional abort signal.
 * @returns {Promise<Object>} Multimodal analysis verdict.
 */
export async function analyzeMultimodalSample(payload, signal) {
  const res = await fetch(`${BASE_URL}/api/v1/multimodal/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    signal
  });
  if (!res.ok) {
    throw new Error(`Multimodal analysis failed: ${res.status}`);
  }
  return await res.json();
}

