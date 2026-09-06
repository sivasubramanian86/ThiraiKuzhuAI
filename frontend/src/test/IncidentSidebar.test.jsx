import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { IncidentSidebar } from "../components/IncidentSidebar.jsx";

describe("IncidentSidebar Component", () => {
  const mockIncidents = [
    {
      id: "INC-2026-001",
      sequence_affected: "Climax Battle VFX",
      severity: "CRITICAL",
      project_title: "Project Kalki",
      box_office_at_risk_usd: 125000,
    },
    {
      id: "INC-2026-002",
      sequence_affected: "Interval Bamboo Duel Foley",
      severity: "HIGH",
      project_title: "Dragon Blade",
      box_office_at_risk_usd: 45000,
    },
  ];

  const mockI18n = {
    incidentHeading: "Studio Pipeline Incidents",
    chaosTitle: "Synthetic Studio Chaos",
    chaosDesc: "Simulate live incidents",
    chaosBtn: "Inject Chaos Telemetry",
  };

  it("renders incident list and count", () => {
    render(
      <IncidentSidebar
        incidents={mockIncidents}
        selectedIncidentId="INC-2026-001"
        onSelectIncident={vi.fn()}
        onInjectChaos={vi.fn()}
        i18n={mockI18n}
      />
    );

    expect(screen.getByText("Studio Pipeline Incidents")).toBeInTheDocument();
    expect(screen.getByText("2 Active")).toBeInTheDocument();
    expect(screen.getByText("Climax Battle VFX")).toBeInTheDocument();
  });

  it("calls onSelectIncident when clicking an incident card", () => {
    const onSelect = vi.fn();
    render(
      <IncidentSidebar
        incidents={mockIncidents}
        selectedIncidentId="INC-2026-001"
        onSelectIncident={onSelect}
        onInjectChaos={vi.fn()}
        i18n={mockI18n}
      />
    );

    const card = screen.getByText("Interval Bamboo Duel Foley");
    fireEvent.click(card);
    expect(onSelect).toHaveBeenCalledWith(mockIncidents[1]);
  });

  it("calls onInjectChaos when clicking the chaos button", () => {
    const onInject = vi.fn();
    render(
      <IncidentSidebar
        incidents={mockIncidents}
        selectedIncidentId="INC-2026-001"
        onSelectIncident={vi.fn()}
        onInjectChaos={onInject}
        i18n={mockI18n}
      />
    );

    const chaosButton = screen.getByText("Inject Chaos Telemetry");
    fireEvent.click(chaosButton);
    expect(onInject).toHaveBeenCalledWith("ott_premiere_spike");
  });
});
