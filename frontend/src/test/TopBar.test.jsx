import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { TopBar } from "../components/TopBar.jsx";

describe("TopBar Component", () => {
  const mockProjects = [
    { id: "proj-1", title: "Project Kalki", genre_track: "sci_fi_epic" },
    { id: "proj-2", title: "Jailer 2", genre_track: "action_masala" },
  ];

  const mockLanguages = [
    { code: "en", name: "English" },
    { code: "ta", name: "Tamil" },
  ];

  const mockI18n = {
    brandSubtitle: "Autonomous Screen Crew AI for Cinematic Observability",
  };

  it("renders branding, CRI score, and MCP status badge", () => {
    render(
      <TopBar
        projects={mockProjects}
        selectedProject="proj-1"
        onSelectProject={vi.fn()}
        criScore={94.5}
        language="en"
        onChangeLanguage={vi.fn()}
        supportedLanguages={mockLanguages}
        i18n={mockI18n}
      />
    );

    expect(screen.getByText("Thirai Kuzhu AI")).toBeInTheDocument();
    expect(screen.getByText("94.5%")).toBeInTheDocument();
    expect(screen.getByText("Grafana MCP: LIVE")).toBeInTheDocument();
  });

  it("renders studio slate badge with active stage and track", () => {
    render(
      <TopBar
        projects={mockProjects}
        selectedProject="proj-1"
        onSelectProject={vi.fn()}
        criScore={90}
        language="en"
        onChangeLanguage={vi.fn()}
        supportedLanguages={mockLanguages}
        i18n={mockI18n}
      />
    );

    expect(screen.getByText("STUDIO STAGE A")).toBeInTheDocument();
    expect(screen.getByText("Live Production Stream")).toBeInTheDocument();
  });

  it("calls onChangeLanguage when switching language", () => {
    const onLang = vi.fn();
    render(
      <TopBar
        projects={mockProjects}
        selectedProject="proj-1"
        onSelectProject={vi.fn()}
        criScore={90}
        language="en"
        onChangeLanguage={onLang}
        supportedLanguages={mockLanguages}
        i18n={mockI18n}
      />
    );

    const langSelect = screen.getByLabelText("Select Interface Language");
    fireEvent.change(langSelect, { target: { value: "ta" } });
    expect(onLang).toHaveBeenCalledWith("ta");
  });
});
