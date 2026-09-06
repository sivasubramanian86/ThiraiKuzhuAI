import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { App } from "../App.jsx";
import * as api from "../services/api.js";

describe("App Root Component Integration", () => {
  const mockProjects = [
    { id: "p1", title: "Project Kalki", genre_track: "sci_fi_epic" },
  ];

  const mockIncidents = [
    {
      id: "INC-001",
      sequence_affected: "Climax Battle VFX",
      severity: "CRITICAL",
      project_title: "Project Kalki",
      box_office_at_risk_usd: 85000,
      cinematic_narrative: "VFX render node memory leak detected.",
      telemetry: {
        grafana_alert_uid: "ALERT-VFX-001",
        promql_metric: "rate(container_gpu_memory[5m]) > 95%",
        tempo_trace_id: "trace-1234",
      },
    },
  ];

  beforeEach(() => {
    vi.spyOn(api, "fetchProjects").mockResolvedValue(mockProjects);
    vi.spyOn(api, "fetchIncidents").mockResolvedValue(mockIncidents);
    vi.spyOn(api, "fetchProjectCRI").mockResolvedValue({
      project_id: "p1",
      composite_cri_score: 96.5,
    });
    vi.spyOn(api, "dispatchInvestigation").mockResolvedValue({
      incident_id: "INC-001",
      status: "mitigated",
      mitigation_plan: ["Evacuate GPU pod"],
      thought_steps: [
        {
          agent_name: "DirectorOps",
          department: "DIRECTING",
          thought: "Directing stunt crew to hold while memory clears.",
        },
      ],
    });
    vi.spyOn(api, "applyMitigation").mockResolvedValue({ success: true });
  });

  it("renders TopBar and hydrates projects and incidents", async () => {
    render(<App />);

    expect(screen.getByText("Thirai Kuzhu AI")).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText("Climax Battle VFX")).toBeInTheDocument();
    });
  });

  it("triggers investigation dispatch on button click", async () => {
    vi.spyOn(api, "streamMission").mockImplementation((id, onStep, onComplete) => {
      onStep({
        agent_name: "DirectorOps",
        department: "DIRECTING",
        thought: "Holding scene.",
        walkie_talkie_dialogue: "Cut! Reset camera.",
      });
      onComplete({ mitigation_plan: ["Evacuate GPU pod"] });
      return vi.fn();
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Dispatch Screen Crew" })).toBeInTheDocument();
    });

    const dispatchBtn = screen.getByRole("button", { name: "Dispatch Screen Crew" });
    fireEvent.click(dispatchBtn);

    await waitFor(() => {
      expect(api.streamMission).toHaveBeenCalledWith(
        "INC-001",
        expect.any(Function),
        expect.any(Function),
        expect.any(Function)
      );
    });
  });
});
