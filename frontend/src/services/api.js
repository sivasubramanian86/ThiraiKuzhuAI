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
