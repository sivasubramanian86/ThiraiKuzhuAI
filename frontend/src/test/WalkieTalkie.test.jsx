import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { WalkieTalkie } from "../components/WalkieTalkie.jsx";

describe("WalkieTalkie Component", () => {
  const mockMessages = [
    { speaker: "DIRECTOR", text: "Check camera rig 4 gyro calibration.", isStatic: false },
    { speaker: "AUDIO", text: "Dolby Atmos stem 14 latency restored.", isStatic: false },
    { speaker: "DISPATCH", text: "Static bursts cleared.", isStatic: true },
  ];

  const mockI18n = {
    walkieTitle: "Studio Walkie-Talkie (Ch 1)",
    walkieDesc: "Live on-set director & department radio communications.",
  };

  it("renders frequency and radio title", () => {
    render(<WalkieTalkie messages={mockMessages} i18n={mockI18n} />);
    expect(screen.getByText("Studio Walkie-Talkie (Ch 1)")).toBeInTheDocument();
    expect(screen.getByText("462.5625 MHz")).toBeInTheDocument();
  });

  it("renders all walkie messages with speakers", () => {
    render(<WalkieTalkie messages={mockMessages} i18n={mockI18n} />);
    expect(screen.getByText("DIRECTOR:")).toBeInTheDocument();
    expect(screen.getByText(/Check camera rig 4 gyro calibration/)).toBeInTheDocument();
    expect(screen.getByText("AUDIO:")).toBeInTheDocument();
  });
});
