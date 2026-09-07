import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AuthProvider } from '../context/AuthContext';
import { ThemeProvider } from '../context/ThemeContext';
import { CrewPersonaLounge } from '../components/CrewPersonaLounge';
import { DynamicSmeStudio } from '../components/DynamicSmeStudio';
import { AntagonistLab } from '../components/AntagonistLab';
import { MultiModalMediaStudio } from '../components/MultiModalMediaStudio';
import { FAQHelp } from '../components/FAQHelp';
import { AboutThiraiKuzhu } from '../components/AboutThiraiKuzhu';
import { SettingsStudio } from '../components/SettingsStudio';
import { ContentShieldStudio } from '../components/ContentShieldStudio';
import { AuthModal } from '../components/AuthModal';
import * as api from '../services/api';

function renderWithProviders(ui) {
  return render(
    <AuthProvider>
      <ThemeProvider>
        {ui}
      </ThemeProvider>
    </AuthProvider>
  );
}

describe('CrewPersonaLounge Component', () => {
  it('renders stats ribbon with 369 personas and 17 bands', () => {
    renderWithProviders(<CrewPersonaLounge />);
    expect(screen.getByRole('heading', { name: /Crew Personas Lounge/i })).toBeInTheDocument();
    expect(screen.getAllByText('369').length).toBeGreaterThan(0);
    expect(screen.getByText('Studio Bands')).toBeInTheDocument();
  });


  it('filters personas when typing in search input', () => {
    renderWithProviders(<CrewPersonaLounge />);
    const searchInput = screen.getByPlaceholderText(/Search by ID/i);
    fireEvent.change(searchInput, { target: { value: 'E23' } });
    expect(screen.getAllByText('E23')[0]).toBeInTheDocument();
  });


  it('opens persona detail modal on click', () => {
    renderWithProviders(<CrewPersonaLounge />);
    const searchInput = screen.getByPlaceholderText(/Search by ID/i);
    fireEvent.change(searchInput, { target: { value: 'A01' } });
    
    const inspectBtn = screen.getAllByRole('button', { name: /Inspect Role/i })[0];
    fireEvent.click(inspectBtn);

    expect(screen.getByText(/Operational Mandate/i)).toBeInTheDocument();
  });
});

describe('DynamicSmeStudio Component', () => {
  it('renders Section 19 contract banner and presets', () => {
    renderWithProviders(<DynamicSmeStudio />);
    expect(screen.getByText(/Dynamic Subject Matter Expert/i)).toBeInTheDocument();
    expect(screen.getByText(/Section 19 Contract: STRICT can_block=false/i)).toBeInTheDocument();
    expect(screen.getByText('Chola Lost-Wax Metallurgy')).toBeInTheDocument();
  });

  it('triggers dynamic SME spawning on button click', async () => {
    vi.spyOn(api, 'spawnDynamicSme').mockResolvedValue({
      id: 'SME-METALLURGY-001',
      title: 'Chola Metallurgy Advisor',
      band: 'SME',
      mandate: 'Validate bronze casting authenticity.',
      authority_scope: 'advisory',
      can_block: false,
      model_tier: 'standard',
      tools: ['web_search', 'domain_knowledge_vault'],
      system_prompt: 'You are an elite bronze casting historian.'
    });

    renderWithProviders(<DynamicSmeStudio />);
    const spawnBtn = screen.getByRole('button', { name: /Spawn Dynamic Advisor/i });
    fireEvent.click(spawnBtn);

    await waitFor(() => {
      expect(screen.getByText('SME-METALLURGY-001')).toBeInTheDocument();
      expect(screen.getByText(/can_block: false/i)).toBeInTheDocument();
    });
  });
});

describe('AntagonistLab Component', () => {
  it('renders all 5 red-team antagonist cards', () => {
    renderWithProviders(<AntagonistLab />);
    expect(screen.getByText(/Red-Team Adversarial Antagonist Lab/i)).toBeInTheDocument();
    expect(screen.getByText('Schedule Breaker')).toBeInTheDocument();
    expect(screen.getByText('Copyright Infringement Attacker')).toBeInTheDocument();
    expect(screen.getByText('Sceptical Film Critic')).toBeInTheDocument();
    expect(screen.getByText('Piracy & Exfiltration Simulator')).toBeInTheDocument();
    expect(screen.getByText('Force Majeure Weather Agent')).toBeInTheDocument();
  });

  it('runs adversarial simulation and displays telemetry report', async () => {
    vi.spyOn(api, 'runAntagonistSimulation').mockResolvedValue({
      antagonist_id: 'ANTG01',
      target_production: 'Baahubali III: The Eternal Realm',
      attack_vector: 'Cast Date Collision',
      intensity: 'HIGH',
      impact_score: 84,
      box_office_risk_usd: 45000,
      breached_bands: ['Band A: Executive', 'Band D: Casting'],
      attack_log: ['Simulated cast date collision.'],
      counter_measures: ['Activate cast contingency buffer.']
    });

    renderWithProviders(<AntagonistLab />);
    const runBtn = screen.getByRole('button', { name: /Run Schedule Breaker Attack/i });
    fireEvent.click(runBtn);

    await waitFor(() => {
      expect(screen.getByText('84/100')).toBeInTheDocument();
      expect(screen.getByText('$45,000 USD')).toBeInTheDocument();
    });
  });
});

describe('MultiModalMediaStudio Component', () => {
  it('switches between all 4 modality tabs', () => {
    renderWithProviders(<MultiModalMediaStudio />);
    expect(screen.getByText(/MultiModal Media Studio/i)).toBeInTheDocument();

    // Storyboard tab
    const storyTab = screen.getByRole('tab', { name: /Storyboard & Art Stills/i });
    fireEvent.click(storyTab);
    expect(screen.getByText(/2.39:1 ANAMORPHIC CROP/i)).toBeInTheDocument();

    // Audio tab
    const audioTab = screen.getByRole('tab', { name: /Foley, Atmos & Audio WAVs/i });
    fireEvent.click(audioTab);
    expect(screen.getByText(/Play Sample \(Dolby Atmos Simulation\)/i)).toBeInTheDocument();

    // Video tab
    const videoTab = screen.getByRole('tab', { name: /Video Dailies & Rushes/i });
    fireEvent.click(videoTab);
    expect(screen.getByText(/FPS: 48.000 HFR/i)).toBeInTheDocument();
  });

  it('runs Gemini multimodal analysis', async () => {
    vi.spyOn(api, 'analyzeMultimodalSample').mockResolvedValue({
      sample_id: 'SAMPLE-SCRIPT-01',
      modality: 'SCRIPT',
      model: 'Gemini 3.8 Flash Multimodal',
      confidence_score: 0.985,
      key_insights: ['Script formatting verified.'],
      notified_departments: ['Band C: Screenplay'],
      cinematic_grade: 'AAA — Production Ready'
    });

    renderWithProviders(<MultiModalMediaStudio />);
    const analyzeBtn = screen.getByRole('button', { name: /Analyze with Gemini Multimodal/i });
    fireEvent.click(analyzeBtn);

    await waitFor(() => {
      expect(screen.getByText(/Confidence: 98.5%/i)).toBeInTheDocument();
      expect(screen.getByText('AAA — Production Ready')).toBeInTheDocument();
    });
  });
});

describe('FAQHelp & About Components', () => {
  it('renders FAQ questions and filters on keyword search', () => {
    renderWithProviders(<FAQHelp />);
    expect(screen.getByText(/Frequently Asked Questions/i)).toBeInTheDocument();
    const searchInput = screen.getByPlaceholderText(/Search questions by keyword/i);
    fireEvent.change(searchInput, { target: { value: 'can_block' } });
    expect(screen.getByText(/strict difference between can_block: true and can_block: false/i)).toBeInTheDocument();
  });

  it('renders 17-band breakdown in About component', () => {
    renderWithProviders(<AboutThiraiKuzhu />);
    expect(screen.getByText('Comprehensive 17-Band Crew Model')).toBeInTheDocument();
    expect(screen.getByText('Executive & Producing')).toBeInTheDocument();
    expect(screen.getByText('Virtual Production & GenAI')).toBeInTheDocument();
  });
});

describe('SettingsStudio Component', () => {
  it('renders cinema themes and toggles dark/light mode', () => {
    renderWithProviders(<SettingsStudio />);
    expect(screen.getByText(/Studio Settings & Configuration/i)).toBeInTheDocument();
    expect(screen.getByText('Director Noir')).toBeInTheDocument();
    expect(screen.getByText('VFX Cyberpunk')).toBeInTheDocument();
  });
});

describe('MultiModalMediaStudio Veo 2 & Lyria Generation', () => {
  it('switches to Veo 2 and inspects video generation prompt', () => {
    renderWithProviders(<MultiModalMediaStudio />);
    const veoTab = screen.getByRole('tab', { name: /Google Veo 2 Video Gen/i });
    fireEvent.click(veoTab);

    expect(screen.getByText(/Google Veo 2 Prompt/i)).toBeInTheDocument();
    expect(screen.getByText(/VEO 2 GENERATIVE VIDEO STREAM/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Anamorphic Aerial Cloud Sweep/i).length).toBeGreaterThan(0);
  });

  it('switches to Lyria and inspects 4-stem Atmos score generator', () => {
    renderWithProviders(<MultiModalMediaStudio />);
    const lyriaTab = screen.getByRole('tab', { name: /Google Lyria AI Score Gen/i });
    fireEvent.click(lyriaTab);

    expect(screen.getByText(/Google DeepMind Lyria Prompt/i)).toBeInTheDocument();
    expect(screen.getByText(/4-Stem Master \(Dolby Atmos\)/i)).toBeInTheDocument();
    expect(screen.getByText(/Strings \/ Veena/i)).toBeInTheDocument();
  });
});

describe('ContentShieldStudio Component', () => {
  it('renders all 3 governance tabs and handles Piracy scan', async () => {
    renderWithProviders(<ContentShieldStudio />);
    expect(screen.getByText(/Content Shield & IP Governance Studio/i)).toBeInTheDocument();

    // Verify tabs
    expect(screen.getByRole('tab', { name: /Piracy & Watermark Detection/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /AI Deepfake & SynthID Provenance/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Patent & Copyright Protection/i })).toBeInTheDocument();

    // Run Piracy scan
    const auditBtn = screen.getByRole('button', { name: /Run Real-Time IP & Security Audit/i });
    fireEvent.click(auditBtn);

    await waitFor(() => {
      expect(screen.getByText(/Piracy & Watermark Telemetry Report/i)).toBeInTheDocument();
      expect(screen.getAllByText(/THIRAI-WM-2026-B01-STAGE_A/i).length).toBeGreaterThan(0);
    }, { timeout: 3000 });
  });

  it('verifies C2PA manifest in Deepfake Provenance tab', async () => {
    renderWithProviders(<ContentShieldStudio />);
    const deepfakeTab = screen.getByRole('tab', { name: /AI Deepfake & SynthID Provenance/i });
    fireEvent.click(deepfakeTab);

    expect(screen.getByText(/AI Deepfake Detection & C2PA Provenance Manifest/i)).toBeInTheDocument();

    const auditBtn = screen.getByRole('button', { name: /Run Real-Time IP & Security Audit/i });
    fireEvent.click(auditBtn);

    await waitFor(() => {
      expect(screen.getByText(/AI Synthetic Content & C2PA Provenance Report/i)).toBeInTheDocument();
      expect(screen.getByText(/99.8% Certified Human Performance/i)).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('runs patent & copyright clearance in Patent Protection tab', async () => {
    renderWithProviders(<ContentShieldStudio />);
    const patentTab = screen.getByRole('tab', { name: /Patent & Copyright Protection/i });
    fireEvent.click(patentTab);

    expect(screen.getByText(/Patent & Copyright Collision Clearance/i)).toBeInTheDocument();
    expect(screen.getByText(/WIPO, USPTO & Indian Patent Office Cleared/i)).toBeInTheDocument();

    const auditBtn = screen.getByRole('button', { name: /Run Real-Time IP & Security Audit/i });
    fireEvent.click(auditBtn);

    await waitFor(() => {
      expect(screen.getByText(/0 blocking cinema staging utility patents identified/i)).toBeInTheDocument();
    }, { timeout: 3000 });
  });
});

describe('AuthModal Component', () => {
  it('renders modal and switches tabs between Crew Login, Firebase Auth, and GCP IAM', () => {
    const onClose = vi.fn();
    renderWithProviders(<AuthModal isOpen={true} onClose={onClose} />);

    expect(screen.getByText(/Studio IAM & Crew Persona Login/i)).toBeInTheDocument();

    // Click on GCP IAM Explainer tab
    const iamTab = screen.getByRole('tab', { name: /GCP IAM Architecture/i });
    fireEvent.click(iamTab);

    expect(screen.getByText(/Do we need 369 separate IAM identities in Google Cloud/i)).toBeInTheDocument();
    expect(screen.getByText(/Workload Identity Federation/i)).toBeInTheDocument();
  });

  it('allows 1-click crew persona selection', () => {
    const onClose = vi.fn();
    renderWithProviders(<AuthModal isOpen={true} onClose={onClose} />);

    const directorBtn = screen.getByText('Director').closest('button');
    expect(directorBtn).not.toBeNull();
    fireEvent.click(directorBtn);
    expect(onClose).toHaveBeenCalled();
  });
});
