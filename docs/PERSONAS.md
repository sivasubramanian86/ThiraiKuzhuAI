# Thirai Kuzhu AI (திரை குழு AI) — Comprehensive Persona Registry Documentation

This document specifies the complete **369-persona cinematic crew and agent registry** for **Thirai Kuzhu AI**, built for the Agentic Cinema hackathon in the Grafana Labs partner track.

---

## 1. Coverage Verification Table

| Band | Description | Catalog Seed | Additions | Total | Highlights |
|---|---|---|---|---|---|
| **A** | Story, Writing & Development | 17 | 0 | 17 | Story (A01), Screenplay (A02), Dialogue (A03), Lyricist (A10), Showrunner (A09). |
| **B** | Direction & Direction Dept | 15 | 0 | 15 | Director (B01), Chief Co-Director, 1st AD (B07), Script Supervisor (B11). |
| **C** | Producers & Production Management | 23 | 2 | 25 | Producer (C01), Line Producer (C04), Completion Guarantor (C22), Unit Hand (C24), Junior Artist Supplier (C25). |
| **D** | Cast & Performance | 14 | 0 | 14 | Principal Cast (D01), Comedian (D03), Playback Singer (D10), Dialect Coach (D12). |
| **E** | Camera, Lighting & Grip | 22 | 1 | 23 | DP (E01), DIT (E11), Gaffer (E13), Lightman (E15), Light Boy Helper (E23). |
| **F** | Art, Design, Costume, Makeup | 28 | 0 | 28 | Production Designer (F01), Art Director (F02), Armourer (F14), SFX Makeup (F27). |
| **G** | Music, Songs & Sound | 20 | 0 | 20 | Music Director (G01), Music Supervisor (G09), Dance Master (G18), Sound Designer (G17). |
| **H** | Action, Stunts & Physical FX | 12 | 0 | 12 | Fight Master (H01) with absolute set stop authority, Wire Specialist (H06), Pyro (H09). |
| **I** | Subject Matter Experts (SMEs) | 36 | 0 | 36 | 35 domain advisors (Police, Law, Medicine, Sangam, etc.) + Dynamic SME Spawner (I36). |
| **J** | Post-Production & Finishing | 20 | 2 | 22 | Editor (J03), Colorist (J08), Atmos Mix (J15), Subtitle QC (J21), Dubbing Studio Mgr (J22). |
| **K** | VFX, CGI, Virtual Production | 25 | 0 | 25 | VFX Supervisor (K01), Virtual Production (K20), Brain Bar (K21), Digital Human (K23). |
| **L** | Distribution, Sales, OTT | 19 | 1 | 20 | Distribution Head (L01), OTT Acquisition (L08), Single-Screen Rep (L20). |
| **M** | Marketing, Promotion, Fandom | 23 | 2 | 25 | Marketing Dir (M01), Publicity Designer (M02), Fan Club Coord (M15), Audio Launch Stage Dir (M24). |
| **N** | Legal, Rights, Finance | 19 | 0 | 19 | Production Legal (N01), Script Registration (N05), Anti-Piracy (N09), Responsible AI (N18). |
| **O** | Reception, Critics, Festivals | 16 | 0 | 16 | Trade Critic (O01), Rotten Tomatoes Analyst (O04), Festival Programmer (O09). |
| **P** | Platform & Studio Reliability | 15 | 0 | 15 | SRE (P01), Observability Director (P02), FinOps (P08), Security Engineer (P09). |
| **Q** | Genre & Budget Advisory Lenses | 24 | 0 | 24 | Comedy, Horror, Mythic Epic, Pan-India, Micro-Budget, Tentpole Advisors. |
| **COMP** | Cross-Band Composite Personas | 0 | 8 | 8 | Multi-agent fused roles (Continuity Guardian, Budget Reality Checker, etc.). |
| **ANTG** | Adversarial Red-Team Personas | 0 | 5 | 5 | Schedule Breaker, Copyright Attacker, Sceptical Critic, Piracy Simulator, Weather Agent. |
| **Total** | | **348** | **21** | **369** | Complete cinematic studio ecosystem with zero omissions. |

---

## 2. Creative Extensions

### A. Cross-Band Composite Personas
1. **COMP01: Continuity Guardian** — Fuses Script Supervisor (B11) + Assistant Editor (J06) + VFX Editor (K04).
2. **COMP02: Budget Reality Checker** — Fuses Line Producer (C04) + VFX Producer (K02) + Render Farm Capacity Planner (P03).
3. **COMP03: Sensory Immersion Architect** — Fuses Cinematographer (E01) + Sound Designer (G17) + Colorist (J08).
4. **COMP04: Cultural Authenticity Anchor** — Fuses Dialogue Writer (A03) + Dialect Advisor (I24) + Anthropology Advisor (I25).
5. **COMP05: Stunt Safety Governor** — Fuses Fight Master (H01) + Set Medic (C21) + Completion Guarantor (C22). Holds unconditional veto.
6. **COMP06: Viral Trailer Pulse** — Fuses Trailer Editor (J07) + Social Media Manager (M13) + Creative Advertising Lead (M04).
7. **COMP07: Box Office Recovery Engine** — Fuses Windowing Analyst (L06) + Revenue Forecast Analyst (N15) + Exhibitor Relations (L16).
8. **COMP08: Synthetic Likeness Guardian** — Fuses Digital Human Specialist (K23) + Responsible AI Officer (N18) + Production Counsel (N01).

### B. Adversarial Red-Team Antagonists
1. **ANTG01: Schedule Breaker** — Attacks shoot schedule with lead actor illness, permit expirations and cascade delays.
2. **ANTG02: Copyright Attacker** — Attacks screenplay, score and background art for IP infringements.
3. **ANTG03: Sceptical Critic** — Audits plot holes, moral motivation flaws and second-half pacing sags.
4. **ANTG04: Piracy Simulator** — Simulates VIP screener leaks, torrent uploads and watermark destruction attacks.
5. **ANTG05: Worst-Case Weather Agent** — Injects sudden monsoon bursts and high-voltage lighting cable submergence hazards.

---

## 3. Dynamic Subject Matter Expert Spawner (I36)
- Meta-persona that ingests raw screenplay snippets.
- Extracts specialized domain entities (e.g., naval warfare, Vedic metallurgy, neurosurgery).
- Matches entities against seed taxonomy `I01..I35` and synthesizes dynamic new SME advisors on the fly.
- Enforces strict advisory-only authority (`can_block: false`) per Section 19 contract.

---

## 4. Grafana MCP Signals Binding
Each persona declares active telemetry signal bindings:
- **Metrics**: `script_revision_backlog`, `shooting_pace_variance`, `stunt_risk_safety_index`, `gpu_vram_saturation_pct`, `cdn_rebuffer_ratio_pct`.
- **Logs**: Loki queries filtered by application, band, and persona slug.
- **Traces**: Distributed OpenTelemetry / Tempo trace IDs tracking subagent handoffs.
- **Dashboards**: Grafana UID embeds (`set-operations-command`, `cinema-stream-master`, `action-safety-telemetry`).
