import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { AgentTimeline } from "../components/AgentTimeline.jsx";
import { IncidentHero } from "../components/IncidentHero.jsx";
import { GrafanaPanelEmbed } from "../components/GrafanaPanelEmbed.jsx";
import { DEPT_ICONS } from "../constants/departments.js";

describe("AgentTimeline Component", () => {
  it("renders placeholder when steps is empty", () => {
    render(<AgentTimeline steps={[]} i18n={{ timelinePlaceholder: "No steps yet." }} />);
    expect(screen.getByText("No steps yet.")).toBeInTheDocument();
  });

  it("renders steps with icons and thought content", () => {
    const steps = [
      {
        agent_name: "ProducerOps",
        department: "PRODUCER",
        thought: "Analyzing box-office risk on Asia-South1.",
        telemetry_action: "query_metrics(cdn_requests_total)",
        timestamp: "2026-09-07T01:30:00Z",
      },
    ];

    render(<AgentTimeline steps={steps} i18n={{ timelinePlaceholder: "No steps" }} />);
    expect(screen.getByText(/ProducerOps/)).toBeInTheDocument();
    expect(screen.getByText("Analyzing box-office risk on Asia-South1.")).toBeInTheDocument();
    expect(screen.getByText("query_metrics(cdn_requests_total)")).toBeInTheDocument();
  });
});

describe("IncidentHero Component", () => {
  const mockIncident = {
    severity: "CRITICAL",
    genre_track: "sci_fi_epic",
    sequence_affected: "Climax Battle VFX",
    cinematic_narrative: "Climax battle scene dropping frames due to memory exhaustion.",
    telemetry: {
      grafana_alert_uid: "ALERT-VFX-001",
      promql_metric: 'rate(container_gpu_memory_used[5m]) > 95%',
      tempo_trace_id: "trace-9876",
    },
  };

  const mockI18n = {
    dispatchBtn: "Dispatch Screen Crew",
    dispatching: "Deliberating On-Set Radio...",
  };

  it("renders incident narrative and telemetry bar", () => {
    render(
      <IncidentHero
        incident={mockIncident}
        isInvestigating={false}
        onDispatch={vi.fn()}
        i18n={mockI18n}
      />
    );

    expect(screen.getByText("CRITICAL")).toBeInTheDocument();
    expect(screen.getByText(/Climax Battle VFX/)).toBeInTheDocument();
    expect(screen.getByText("ALERT-VFX-001")).toBeInTheDocument();
    expect(screen.getByText("trace-9876")).toBeInTheDocument();
  });

  it("calls onDispatch when clicking the dispatch button", () => {
    const onDispatch = vi.fn();
    render(
      <IncidentHero
        incident={mockIncident}
        isInvestigating={false}
        onDispatch={onDispatch}
        i18n={mockI18n}
      />
    );

    const button = screen.getByRole("button", { name: "Dispatch Screen Crew" });
    fireEvent.click(button);
    expect(onDispatch).toHaveBeenCalled();
  });
});

describe("GrafanaPanelEmbed Component", () => {
  it("renders SVG telemetry chart and query text", () => {
    render(
      <GrafanaPanelEmbed
        promqlQuery="sum(rate(cdn_requests_total[2m]))"
        alertLabel="504 Spike: 12%"
      />
    );

    expect(screen.getByText("Grafana Live Panel")).toBeInTheDocument();
    expect(screen.getByText("504 Spike: 12%")).toBeInTheDocument();
    expect(screen.getByText("sum(rate(cdn_requests_total[2m]))")).toBeInTheDocument();
  });
});

describe("Department Constants", () => {
  it("defines standard cinema department icons", () => {
    expect(DEPT_ICONS.PRODUCING).toBeDefined();
    expect(DEPT_ICONS.DIRECTING).toBeDefined();
    expect(DEPT_ICONS.VFX_CGI).toBeDefined();
    expect(DEPT_ICONS.DEFAULT).toBeDefined();
  });
});
