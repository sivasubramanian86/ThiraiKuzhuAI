import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { MitigationPanel } from "../components/MitigationPanel.jsx";

describe("MitigationPanel Component", () => {
  const mockPlan = [
    "Evacuate failing transcode worker pod",
    "Reroute 4K live HLS streams to secondary edge POP",
  ];

  const mockI18n = {
    mitigationHeading: "Director's Cut Actionable Mitigation Plan",
    boxOfficeProtected: "Box Office Protected",
    applyBtn: "Apply Mitigation & Annotate Grafana Dashboard",
    applyingBtn: "Executing Mitigation & Annotating Grafana...",
    appliedBtn: "Mitigation Applied & Dashboard Annotated",
  };

  it("returns null when mitigationPlan is empty", () => {
    const { container } = render(
      <MitigationPanel
        mitigationPlan={[]}
        boxOfficeRisk={50000}
        isApplying={false}
        mitigationApplied={false}
        statusMessage=""
        onApplyMitigation={vi.fn()}
        i18n={mockI18n}
      />
    );
    expect(container.firstChild).toBeNull();
  });

  it("renders mitigation steps and protected amount", () => {
    render(
      <MitigationPanel
        mitigationPlan={mockPlan}
        boxOfficeRisk={75000}
        isApplying={false}
        mitigationApplied={false}
        statusMessage=""
        onApplyMitigation={vi.fn()}
        i18n={mockI18n}
      />
    );

    expect(screen.getByText("Director's Cut Actionable Mitigation Plan")).toBeInTheDocument();
    expect(screen.getByText(/75,000/)).toBeInTheDocument();
    expect(screen.getByText("Evacuate failing transcode worker pod")).toBeInTheDocument();
  });

  it("calls onApplyMitigation when clicking apply button", () => {
    const onApply = vi.fn();
    render(
      <MitigationPanel
        mitigationPlan={mockPlan}
        boxOfficeRisk={75000}
        isApplying={false}
        mitigationApplied={false}
        statusMessage=""
        onApplyMitigation={onApply}
        i18n={mockI18n}
      />
    );

    const button = screen.getByRole("button", { name: /Apply mitigation and annotate Grafana/i });
    fireEvent.click(button);
    expect(onApply).toHaveBeenCalled();
  });

  it("disables button when applying or already applied", () => {
    render(
      <MitigationPanel
        mitigationPlan={mockPlan}
        boxOfficeRisk={75000}
        isApplying={true}
        mitigationApplied={false}
        statusMessage="Applying..."
        onApplyMitigation={vi.fn()}
        i18n={mockI18n}
      />
    );

    const button = screen.getByRole("button");
    expect(button).toBeDisabled();
    expect(screen.getByText("Executing Mitigation & Annotating Grafana...")).toBeInTheDocument();
  });
});
