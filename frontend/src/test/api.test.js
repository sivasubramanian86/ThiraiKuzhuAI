import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import {
  fetchProjects,
  fetchProjectCRI,
  fetchIncidents,
  dispatchInvestigation,
  applyMitigation,
  streamMission,
} from "../services/api.js";

describe("API Client Service", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("fetchProjects should call /api/projects and return json", async () => {
    const mockData = [{ project_id: "p1", title: "Kalki 2898 AD" }];
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    const result = await fetchProjects();
    expect(global.fetch).toHaveBeenCalledWith("/api/projects", { signal: undefined });
    expect(result).toEqual(mockData);
  });

  it("fetchProjects throws when response is not ok", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    await expect(fetchProjects()).rejects.toThrow("Failed to fetch projects: 500");
  });

  it("fetchProjectCRI should fetch specific CRI report", async () => {
    const mockCri = { project_id: "p1", composite_cri_score: 94.2 };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockCri,
    });

    const result = await fetchProjectCRI("p1");
    expect(global.fetch).toHaveBeenCalledWith("/api/evaluation/cri/p1", { signal: undefined });
    expect(result).toEqual(mockCri);
  });

  it("fetchProjectCRI throws on error", async () => {
    global.fetch.mockResolvedValueOnce({ ok: false, status: 404 });
    await expect(fetchProjectCRI("unknown")).rejects.toThrow("Failed to fetch CRI evaluation: 404");
  });

  it("fetchIncidents should call /api/incidents", async () => {
    const mockIncidents = [{ incident_id: "inc-1", title: "CDN 504 Storm" }];
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockIncidents,
    });

    const result = await fetchIncidents();
    expect(global.fetch).toHaveBeenCalledWith("/api/incidents", { signal: undefined });
    expect(result).toEqual(mockIncidents);
  });

  it("fetchIncidents throws on error", async () => {
    global.fetch.mockResolvedValueOnce({ ok: false, status: 503 });
    await expect(fetchIncidents()).rejects.toThrow("Failed to fetch incidents: 503");
  });

  it("dispatchInvestigation should post incident investigation request", async () => {
    const mockRes = { incident_id: "inc-1", status: "mitigated" };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockRes,
    });

    const result = await dispatchInvestigation("inc-1", "ta");
    expect(global.fetch).toHaveBeenCalledWith("/api/missions/investigate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ incident_id: "inc-1", target_language: "ta" }),
      signal: undefined,
    });
    expect(result).toEqual(mockRes);
  });

  it("dispatchInvestigation throws when not ok", async () => {
    global.fetch.mockResolvedValueOnce({ ok: false, status: 400 });
    await expect(dispatchInvestigation("inc-1")).rejects.toThrow("Investigation request failed: 400");
  });

  it("applyMitigation should post mitigation payload", async () => {
    const payload = {
      incident_id: "inc-1",
      action_taken: "reroute",
      annotation_text: "Rerouted to origin",
      dashboard_uid: "dash-1",
    };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true }),
    });

    const result = await applyMitigation(payload);
    expect(global.fetch).toHaveBeenCalledWith("/api/mitigations/apply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: undefined,
    });
    expect(result).toEqual({ success: true });
  });

  it("applyMitigation throws on failure", async () => {
    global.fetch.mockResolvedValueOnce({ ok: false, status: 500 });
    await expect(applyMitigation({})).rejects.toThrow("Apply mitigation failed: 500");
  });

  it("streamMission initializes and returns cleanup function", () => {
    const onStep = vi.fn();
    const onComplete = vi.fn();
    const onError = vi.fn();

    const cleanup = streamMission("inc-1", onStep, onComplete, onError);
    expect(typeof cleanup).toBe("function");
    cleanup();
  });
});
