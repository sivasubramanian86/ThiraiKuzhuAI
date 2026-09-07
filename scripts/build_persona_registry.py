#!/usr/bin/env python3
"""Build and serialize the comprehensive 369-persona registry for Thirai Kuzhu AI.

Grounded in PHASE-05A and PHASE-05B specifications:
- 17 Bands (A through Q) with 348 seed personas
- 8 On-set physical reality additions (E23, C24, C25, M24, L20, J21, J22, M25)
- 8 Cross-band composite roles (COMP01-COMP08)
- 5 Adversarial red-team antagonists (ANTG01-ANTG05)
Total: 369 personas conforming strictly to Section 18 schema.
"""

import json
from pathlib import Path

def dump_clean_yaml(data: dict, indent: int = 0) -> str:
    """Pure-python clean YAML serializer conforming to YAML 1.2 specifications."""
    lines = []
    prefix = "  " * indent
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{prefix}{k}:")
                lines.append(dump_clean_yaml(v, indent + 1))
            elif isinstance(v, bool):
                lines.append(f"{prefix}{k}: {'true' if v else 'false'}")
            elif v is None:
                lines.append(f"{prefix}{k}: null")
            elif isinstance(v, (int, float)):
                lines.append(f"{prefix}{k}: {v}")
            else:
                # String escaping
                str_val = str(v).replace('"', '\\"')
                lines.append(f'{prefix}{k}: "{str_val}"')
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    if first:
                        if isinstance(v, (dict, list)):
                            lines.append(f"{prefix}- {k}:")
                            lines.append(dump_clean_yaml(v, indent + 2))
                        elif isinstance(v, bool):
                            lines.append(f"{prefix}- {k}: {'true' if v else 'false'}")
                        elif isinstance(v, (int, float)):
                            lines.append(f"{prefix}- {k}: {v}")
                        else:
                            str_val = str(v).replace('"', '\\"')
                            lines.append(f'{prefix}- {k}: "{str_val}"')
                        first = False
                    else:
                        sub_prefix = prefix + "  "
                        if isinstance(v, (dict, list)):
                            lines.append(f"{sub_prefix}{k}:")
                            lines.append(dump_clean_yaml(v, indent + 2))
                        elif isinstance(v, bool):
                            lines.append(f"{sub_prefix}{k}: {'true' if v else 'false'}")
                        elif isinstance(v, (int, float)):
                            lines.append(f"{sub_prefix}{k}: {v}")
                        else:
                            str_val = str(v).replace('"', '\\"')
                            lines.append(f'{sub_prefix}{k}: "{str_val}"')
            else:
                if isinstance(item, bool):
                    lines.append(f"{prefix}- {'true' if item else 'false'}")
                elif isinstance(item, (int, float)):
                    lines.append(f"{prefix}- {item}")
                else:
                    str_val = str(item).replace('"', '\\"')
                    lines.append(f'{prefix}- "{str_val}"')
    return "\n".join(lines)

# Base directory
ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_PERSONAS_DIR = ROOT_DIR / "backend" / "src" / "personas"
BACKEND_PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
ROOT_PERSONAS_DIR = ROOT_DIR / "personas"
ROOT_PERSONAS_DIR.mkdir(parents=True, exist_ok=True)

# Band definitions
BANDS_METADATA = {
    "A": {
        "name": "Story, Writing and Development",
        "budget_line": "ATL",
        "model_tier": "reasoning",
        "concurrency": "parallel",
        "default_phase": ["development", "prep"],
        "token_budget": 12000,
        "default_metrics": ["script_revision_backlog", "scene_lock_pct"],
        "dashboards": ["writing-room-throughput"]
    },
    "B": {
        "name": "Direction and the Direction Department",
        "budget_line": "ATL",
        "model_tier": "reasoning",
        "concurrency": "parallel",
        "default_phase": ["prep", "production", "post"],
        "token_budget": 14000,
        "default_metrics": ["shooting_pace_variance", "takes_per_scene"],
        "dashboards": ["set-operations-command"]
    },
    "C": {
        "name": "Producers and Production Management",
        "budget_line": "ATL",
        "model_tier": "standard",
        "concurrency": "parallel",
        "default_phase": ["development", "prep", "production", "post", "distribution"],
        "token_budget": 10000,
        "default_metrics": ["budget_burn_rate_usd", "schedule_overrun_hours"],
        "dashboards": ["producer-cost-guard"]
    },
    "D": {
        "name": "Cast and Performance",
        "budget_line": "ATL",
        "model_tier": "standard",
        "concurrency": "parallel",
        "default_phase": ["prep", "production"],
        "token_budget": 8000,
        "default_metrics": ["cast_call_sheet_adherence", "performance_take_efficiency"],
        "dashboards": ["cast-call-readiness"]
    },
    "E": {
        "name": "Camera, Lighting and Grip",
        "budget_line": "BTL",
        "model_tier": "standard",
        "concurrency": "parallel",
        "default_phase": ["prep", "production"],
        "token_budget": 8000,
        "default_metrics": ["lighting_rig_time_minutes", "dit_checksum_error_count"],
        "dashboards": ["camera-dit-live"]
    },
    "F": {
        "name": "Art, Production Design, Props, Costume, Makeup",
        "budget_line": "BTL",
        "model_tier": "cheap",
        "concurrency": "parallel",
        "default_phase": ["prep", "production"],
        "token_budget": 6000,
        "default_metrics": ["set_dressing_readiness_pct", "wardrobe_continuity_faults"],
        "dashboards": ["art-design-continuity"]
    },
    "G": {
        "name": "Music, Songs and Production Sound",
        "budget_line": "BTL",
        "model_tier": "standard",
        "concurrency": "parallel",
        "default_phase": ["prep", "production", "post"],
        "token_budget": 10000,
        "default_metrics": ["audio_clipping_events", "music_sync_latency_ms"],
        "dashboards": ["sound-music-master"]
    },
    "H": {
        "name": "Action, Stunts and Physical Effects",
        "budget_line": "BTL",
        "model_tier": "reasoning",
        "concurrency": "serial",
        "default_phase": ["prep", "production"],
        "token_budget": 12000,
        "default_metrics": ["stunt_risk_safety_index", "wire_rig_load_factor"],
        "dashboards": ["action-safety-telemetry"]
    },
    "I": {
        "name": "Subject Matter Experts and Technical Advisors",
        "budget_line": "ADVISORY",
        "model_tier": "reasoning",
        "concurrency": "parallel",
        "default_phase": ["development", "prep", "production"],
        "token_budget": 12000,
        "default_metrics": ["sme_review_backlog", "accuracy_flag_count"],
        "dashboards": ["domain-accuracy-matrix"]
    },
    "J": {
        "name": "Post-Production: Picture, Sound, Finishing",
        "budget_line": "POST",
        "model_tier": "standard",
        "concurrency": "parallel",
        "default_phase": ["post"],
        "token_budget": 10000,
        "default_metrics": ["edit_conform_error_rate", "atmos_render_latency_ms"],
        "dashboards": ["post-finishing-pipeline"]
    },
    "K": {
        "name": "VFX, CGI, Animation, Virtual Production",
        "budget_line": "POST",
        "model_tier": "reasoning",
        "concurrency": "burst",
        "default_phase": ["prep", "production", "post"],
        "token_budget": 15000,
        "default_metrics": ["render_farm_queue_depth", "gpu_vram_saturation_pct"],
        "dashboards": ["vfx-render-throughput"]
    },
    "L": {
        "name": "Distribution, Sales, OTT and Exhibition",
        "budget_line": "COMMERCIAL",
        "model_tier": "standard",
        "concurrency": "parallel",
        "default_phase": ["distribution"],
        "token_budget": 10000,
        "default_metrics": ["cdn_rebuffer_ratio_pct", "screen_count_booked"],
        "dashboards": ["cinema-stream-master"]
    },
    "M": {
        "name": "Marketing, Publicity, Promotion, Fandom",
        "budget_line": "COMMERCIAL",
        "model_tier": "standard",
        "concurrency": "burst",
        "default_phase": ["production", "distribution"],
        "token_budget": 10000,
        "default_metrics": ["social_engagement_velocity", "trailer_view_conversion"],
        "dashboards": ["fan-pulse-marketing"]
    },
    "N": {
        "name": "Legal, Rights, Copyright, Finance",
        "budget_line": "COMMERCIAL",
        "model_tier": "reasoning",
        "concurrency": "serial",
        "default_phase": ["development", "prep", "production", "post", "distribution"],
        "token_budget": 14000,
        "default_metrics": ["copyright_clearance_pct", "piracy_leak_takedown_latency"],
        "dashboards": ["legal-clearance-audit"]
    },
    "O": {
        "name": "Reception Ecosystem: Critics, Ratings, Festivals, Awards",
        "budget_line": "RECEPTION",
        "model_tier": "cheap",
        "concurrency": "parallel",
        "default_phase": ["distribution"],
        "token_budget": 6000,
        "default_metrics": ["aggregated_critic_score", "sentiment_polarity_index"],
        "dashboards": ["box-office-reception"]
    },
    "P": {
        "name": "Platform and Engineering Personas",
        "budget_line": "PLATFORM",
        "model_tier": "reasoning",
        "concurrency": "parallel",
        "default_phase": ["development", "prep", "production", "post", "distribution"],
        "token_budget": 16000,
        "default_metrics": ["mcp_tool_invocation_latency_ms", "agent_guardrail_trips"],
        "dashboards": ["agent-mesh-observability"]
    },
    "Q": {
        "name": "Genre, Theme and Budget Advisory Lenses",
        "budget_line": "ADVISORY",
        "model_tier": "reasoning",
        "concurrency": "parallel",
        "default_phase": ["development", "prep"],
        "token_budget": 12000,
        "default_metrics": ["genre_beat_compliance", "budget_tier_stress_factor"],
        "dashboards": ["genre-advisory-compass"]
    },
    "COMP": {
        "name": "Cross-Band Composite Personas",
        "budget_line": "PLATFORM",
        "model_tier": "reasoning",
        "concurrency": "parallel",
        "default_phase": ["prep", "production", "post"],
        "token_budget": 16000,
        "default_metrics": ["cross_band_variance_score", "composite_decision_latency"],
        "dashboards": ["composite-mesh-intelligence"]
    },
    "ANTG": {
        "name": "Adversarial Red-Team Antagonists",
        "budget_line": "PLATFORM",
        "model_tier": "reasoning",
        "concurrency": "serial",
        "default_phase": ["prep", "production", "post", "distribution"],
        "token_budget": 16000,
        "default_metrics": ["adversarial_risk_severity", "attack_vector_coverage"],
        "dashboards": ["antagonist-stress-testing"]
    }
}

# Raw catalog seed data
RAW_PERSONAS = [
    # Band A
    ("A01", "story_writer", "Story Writer / Story Concept", "கதை ஆசிரியர்", "कहानी लेखक", "A", "story", "ATL", ["development"], "Originates core story, characters and themes.", False, ["C01", "B01"], ["A02", "A03", "A06"]),
    ("A02", "screenplay_writer", "Screenplay Writer", "திரைக்கதை எழுத்தாளர்", "पटकथा लेखक", "A", "screenplay", "ATL", ["development", "prep"], "Converts story into structural blueprint - scenes, act structure.", False, ["B01", "C01"], ["A01", "A03", "B07"]),
    ("A03", "dialogue_writer", "Dialogue Writer", "வசனகர்த்தா", "संवाद लेखक", "A", "dialogue", "ATL", ["development", "prep", "production"], "Writes spoken lines in correct register, dialect and punch lines.", False, ["B01", "A02"], ["A01", "A02", "A10", "D09", "I24"]),
    ("A04", "additional_writer", "Additional Story / Dialogue Writer", "கூடுதல் கதை / வசன எழுத்தாளர்", "अतिरिक्त कहानी / संवाद लेखक", "A", "dialogue", "ATL", ["development"], "Polishes or expands specific sequence sections.", False, ["A02", "A03"], ["A02", "A03"]),
    ("A05", "adaptation_writer", "Scenario Writer / Adaptation Writer", "தழுவல் கதை எழுத்தாளர்", "रूपांतरण लेखक", "A", "screenplay", "ATL", ["development"], "Reshapes underlying source material into filmable scenario.", False, ["A02", "C01"], ["A01", "N03"]),
    ("A06", "script_doctor", "Story Advisor / Script Doctor", "கதை ஆலோசகர் / ஸ்கிரிப்ட் டாக்டர்", "कहानी सलाहकार", "A", "story", "ATL", ["development"], "Diagnoses structural issues and prescribes dramaturgical fixes.", False, ["B01", "C01"], ["A01", "A02"]),
    ("A07", "script_editor", "Screenplay Consultant / Script Editor", "திரைக்கதை ஆசிரியர்", "पटकथा संपादक", "A", "screenplay", "ATL", ["development", "prep"], "Maintains continuity of structure and theme across revisions.", False, ["A02", "B01"], ["A02", "B12"]),
    ("A08", "writers_room_writer", "Writers Room Writer (OTT / Series)", "எழுத்தாளர் அறை எழுத்தாளர்", "राइटर्स रूम लेखक", "A", "screenplay", "ATL", ["development"], "Shared episodic writing under lead creator retainers.", False, ["A09"], ["A09", "A02", "A03"]),
    ("A09", "showrunner", "Showrunner / Series Creator", "ஷோரன்னர் / தொடர் படைப்பாளி", "शोरनर / श्रृंखला निर्माता", "A", "story", "ATL", ["development", "prep", "production", "post"], "Top creative and management authority over multi-episode series.", True, ["C01"], ["B01", "A08", "C04", "L08"]),
    ("A10", "lyricist", "Lyricist / Songwriter", "பாடலாசிரியர்", "गीतकार", "A", "lyrics", "ATL", ["development", "production"], "Writes poetic song lyrics aligned with scene emotions.", False, ["B01", "G01"], ["G01", "G02", "B01"]),
    ("A11", "bilingual_script_adapter", "Translator / Bilingual Script Adapter", "இருமொழி ஸ்கிரிப்ட் மொழிபெயர்ப்பாளர்", "द्विभाषी पटकथा अनुवादक", "A", "screenplay", "ATL", ["development", "prep"], "Prepares culturally parallel scripts for pan-India releases.", False, ["A02", "A03"], ["A03", "L24", "I24"]),
    ("A12", "script_researcher", "Script Researcher", "திரைக்கதை ஆய்வாளர்", "पटकथा शोधकर्ता", "A", "none", "ATL", ["development"], "Conducts period, technical, forensic and historical research.", False, ["A01", "A02"], ["A01", "A02", "I17"]),
    ("A13", "script_reader", "Script Reader / Coverage Analyst", "கதை மதிப்பீட்டாளர்", "स्क्रिप्ट समीक्षक", "A", "none", "ATL", ["development"], "Scores incoming submissions and drafts studio coverage reports.", False, ["C01", "C02"], ["A14", "C01"]),
    ("A14", "development_producer", "Development Producer", "வளர்ச்சி தயாரிப்பாளர்", "विकास निर्माता", "A", "none", "ATL", ["development"], "Sources, option-purchases and packages intellectual property.", False, ["C01", "C02"], ["A01", "N03", "C01"]),
    ("A15", "concept_artist", "Concept Artist / Illustrator", "கருத்து கலைஞர்", "कॉन्सेप्ट आर्टिस्ट", "A", "none", "ATL", ["development", "prep"], "Visualizes world, environments and tone before physical design.", False, ["B01", "F01"], ["B01", "F01", "A16"]),
    ("A16", "storyboard_artist", "Storyboard Artist", "ஸ்டோரிபோர்டு கலைஞர்", "स्टोरीबोर्ड आर्टिस्ट", "A", "none", "ATL", ["prep"], "Draws scenes shot by shot with lens and camera moves.", False, ["B01", "E01"], ["B01", "E01", "B07"]),
    ("A17", "previz_artist", "Previz / Techviz Artist", "ப்ரீவிஸ் கலைஞர்", "प्रीविज़ कलाकार", "A", "none", "ATL", ["prep"], "Builds 3D technical camera and stunt pre-visualizations.", False, ["B01", "K01"], ["B01", "E01", "H01", "K01"]),

    # Band B
    ("B01", "director", "Director", "இயக்குநர்", "निर्देशक", "B", "none", "ATL", ["prep", "production", "post"], "Artistic captain owning the cinematic visualization of script.", True, ["C01"], ["C01", "B07", "E01", "J03", "F01"]),
    ("B02", "chief_co_director", "Chief Co-Director", "தலைமை இணை இயக்குநர்", "मुख्य सह-निर्देशक", "B", "none", "ATL", ["prep", "production"], "Senior deputy directing major creative and parallel sequence blocks.", False, ["B01"], ["B01", "B04", "B07"]),
    ("B03", "co_director", "Co-Director", "இணை இயக்குநர்", "सह-निर्देशक", "B", "none", "ATL", ["prep", "production"], "Executes designated sub-units or second unit dramatic blocks.", False, ["B01", "B02"], ["B01", "B06", "B10"]),
    ("B04", "chief_associate_director", "Chief Associate Director", "தலைமை உதவி இயக்குநர்", "मुख्य एसोसिएट निर्देशक", "B", "none", "ATL", ["prep", "production"], "Manages day-to-day coordination of direction department.", False, ["B01", "B02"], ["B05", "B06", "B07"]),
    ("B05", "associate_director", "Associate Director", "அசோசியேட் இயக்குநர்", "एसोसिएट निर्देशक", "B", "none", "ATL", ["prep", "production"], "Sequence-level shot execution and performance support.", False, ["B04", "B01"], ["B04", "B06", "B11"]),
    ("B06", "assistant_director", "Assistant Director (AD Pool)", "உதவி இயக்குநர்", "सहायक निर्देशक", "B", "none", "BTL", ["prep", "production"], "Scene breakdown, actor prep and continuity liaison on set.", False, ["B04", "B07"], ["B04", "B08", "B11"]),
    ("B07", "first_ad", "1st Assistant Director", "முதல் உதவி இயக்குநர்", "प्रथम सहायक निर्देशक", "B", "none", "ATL", ["prep", "production"], "Runs set discipline, daily schedule, and cross-department comms.", True, ["B01", "C04"], ["B01", "C04", "E01", "H01", "B08"]),
    ("B08", "second_ad", "2nd Assistant Director", "இரண்டாம் உதவி இயக்குநர்", "द्वितीय सहायक निर्देशक", "B", "none", "BTL", ["production"], "Generates daily call sheets, manages cast arrivals and extras.", False, ["B07"], ["B07", "D01", "D05", "B09"]),
    ("B09", "second_second_ad", "2nd 2nd Assistant Director", "கூடுதல் உதவி இயக்குநர்", "अतिरिक्त सहायक निर्देशक", "B", "none", "BTL", ["production"], "Handles overflow background crowd wrangling and logistics.", False, ["B08"], ["B08", "D06"]),
    ("B10", "second_unit_director", "Second Unit Director", "இரண்டாம் யூனிட் இயக்குநர்", "सेकंड यूनिट निर्देशक", "B", "none", "ATL", ["production"], "Directs stunts, pickups, drone plates and inserts.", False, ["B01"], ["B01", "H01", "E01"]),
    ("B11", "script_supervisor", "Script Supervisor / Continuity", "ஸ்கிரிப்ட் சூப்பர்வைசர்", "स्क्रिप्ट सुपरवाइजर", "B", "none", "BTL", ["production"], "Monitors visual continuity, screen direction and lines the script.", False, ["B01", "B07"], ["B01", "E04", "J03"]),
    ("B12", "script_coordinator", "Script Coordinator", "ஸ்கிரிப்ட் ஒருங்கிணைப்பாளர்", "स्क्रिप्ट समन्वयक", "B", "none", "BTL", ["prep", "production"], "Tracks script revisions, colored page releases and distribution.", False, ["B07"], ["A02", "B07", "C09"]),
    ("B13", "dubbing_director", "Dubbing Director", "டப்பிங் இயக்குநர்", "डबिंग निर्देशक", "B", "none", "POST", ["post"], "Directs voice actors across multiple localized language tracks.", False, ["B01"], ["D09", "J12", "J13"]),
    ("B14", "casting_director", "Casting Director", "நடிகர் தேர்வு இயக்குநர்", "कास्टिंग निर्देशक", "B", "none", "ATL", ["prep"], "Auditions, packages and recommends cast for characters.", False, ["B01", "C01"], ["B01", "C01", "D14", "B15"]),
    ("B15", "casting_assistant", "Casting Assistant", "நடிகர் தேர்வு உதவியாளர்", "कास्टिंग सहायक", "B", "none", "BTL", ["prep"], "Coordinates open calls, talent schedules, and self-tapes.", False, ["B14"], ["B14", "D01", "D02"]),

    # Band C
    ("C01", "producer", "Producer", "தயாரிப்பாளர்", "निर्माता", "C", "none", "ATL", ["development", "prep", "production", "post", "distribution"], "Primary production fiduciary and project overseer.", True, ["C02"], ["C02", "B01", "C04", "L01"]),
    ("C02", "executive_producer", "Executive Producer", "நிர்வாகத் தயாரிப்பாளர்", "कार्यकारी निर्माता", "C", "none", "ATL", ["development", "prep", "production", "post", "distribution"], "Controls project financing, bank guarantees and executive greenlight.", True, [], ["C01", "N13", "C22"]),
    ("C03", "co_producer", "Co-Producer / Associate Producer", "இணைத் தயாரிப்பாளர்", "सह-निर्माता", "C", "none", "ATL", ["prep", "production", "post"], "Delegated managerial slices of physical production.", False, ["C01"], ["C01", "C04"]),
    ("C04", "line_producer", "Line Producer", "லைன் தயாரிப்பாளர்", "लाइन प्रोड्यूसर", "C", "none", "ATL", ["prep", "production", "post"], "Guards the financial budget, shoot days, vendor hires and schedule.", True, ["C01"], ["C01", "B07", "C05", "C06", "C12"]),
    ("C05", "unit_production_manager", "Unit Production Manager (UPM)", "யூனிட் தயாரிப்பு மேலாளர்", "यूनिट प्रोडक्शन मैनेजर", "C", "none", "BTL", ["prep", "production"], "Executes daily set expenditures, crew bookings and logistics.", False, ["C04"], ["C04", "C08", "C09"]),
    ("C06", "production_controller", "Production Controller", "தயாரிப்புக் கட்டுப்பாட்டாளர்", "प्रोडक्शन कंट्रोलर", "C", "none", "ATL", ["prep", "production"], "Indian-unit cost guardian managing physical resource allocations.", True, ["C01", "C04"], ["C04", "C07", "C13"]),
    ("C07", "production_executive", "Production Executive", "தயாரிப்பு நிர்வாகி", "उत्पादन कार्यकारी", "C", "none", "BTL", ["prep", "production"], "Executes producer and controller decisions across field teams.", False, ["C06"], ["C06", "C08"]),
    ("C08", "production_manager", "Production Manager", "தயாரிப்பு மேலாளர்", "उत्पादन प्रबंधक", "C", "none", "BTL", ["production"], "Runs shooting unit ground logistics, vehicle movements and facilities.", False, ["C05"], ["C05", "C09", "C19"]),
    ("C09", "production_coordinator", "Production Coordinator", "தயாரிப்பு ஒருங்கிணைப்பாளர்", "उत्पादन समन्वयक", "C", "none", "BTL", ["prep", "production"], "Information nexus: crew contracts, rental gear and logistics.", False, ["C05"], ["C05", "C10", "C11"]),
    ("C10", "assistant_production_coordinator", "Assistant Production Coordinator", "உதவி தயாரிப்பு ஒருங்கிணைப்பாளர்", "सहायक उत्पादन समन्वयक", "C", "none", "BTL", ["production"], "Volume coordination for equipment pickups and daily POs.", False, ["C09"], ["C09"]),
    ("C11", "production_secretary", "Production Secretary", "தயாரிப்புச் செயலாளர்", "उत्पादन सचिव", "C", "none", "BTL", ["production"], "Unit logs, incoming communications and vendor filings.", False, ["C09"], ["C09"]),
    ("C12", "production_accountant", "Production Accountant", "தயாரிப்புக் கணக்காளர்", "उत्पादन लेखाकार", "C", "none", "BTL", ["prep", "production", "post"], "Cost report ledgering, escrow tracking and vendor reconciliations.", False, ["C04"], ["C04", "C13", "N15"]),
    ("C13", "set_accountant", "Set Accountant / Cashier", "செட் கணக்காளர்", "सेट खजांची", "C", "none", "BTL", ["production"], "On-set petty cash, per diem disbursements and daily vouchers.", False, ["C12", "C06"], ["C12", "C06"]),
    ("C14", "key_pa", "Key Production Assistant", "முதன்மை தயாரிப்பு உதவியாளர்", "प्रमुख उत्पादन सहायक", "C", "none", "BTL", ["production"], "Leads on-set PA squad and walkie distribution.", False, ["B07", "C08"], ["C15", "B07"]),
    ("C15", "production_assistant", "Production Assistant (Set / Office)", "தயாரிப்பு உதவியாளர்", "उत्पादन सहायक", "C", "none", "BTL", ["production"], "Lockups, runs, water supply and field errands.", False, ["C14"], ["C14"]),
    ("C16", "location_manager", "Location Manager", "படப்பிடிப்பு தள மேலாளர்", "स्थान प्रबंधक", "C", "none", "BTL", ["prep", "production"], "Negotiates location leases, permits, police clearances and neighbours.", False, ["C04"], ["C17", "C18", "B07"]),
    ("C17", "location_scout", "Location Scout", "படப்பிடிப்பு தள ஆய்வாளர்", "स्थान अन्वेषक", "C", "none", "BTL", ["prep"], "Finds, photographs and recces candidate shooting sites.", False, ["C16"], ["C16", "B01", "E01"]),
    ("C18", "locations_assistant", "Locations Assistant", "தள உதவியாளர்", "स्थान सहायक", "C", "none", "BTL", ["production"], "On-ground site parking, trash cleanup, power tie-ins.", False, ["C16"], ["C16"]),
    ("C19", "transportation_coordinator", "Transportation Coordinator / Captain", "போக்குவரத்து ஒருங்கிணைப்பாளர்", "परिवहन समन्वयक", "C", "none", "BTL", ["production"], "Fleet scheduling for star vans, grip trucks and crew shuttles.", False, ["C08"], ["C08", "B08"]),
    ("C20", "catering_manager", "Catering / Craft Services Manager", "உணவு ஏற்பாட்டு மேலாளர்", "खानपान प्रबंधक", "C", "none", "BTL", ["production"], "Hot meals, beverage stations and hydration for 200+ unit members.", False, ["C08"], ["C08", "C24"]),
    ("C21", "set_medic", "Set Medic / Unit Nurse", "செட் மருத்துவர்", "सेट चिकित्सक", "C", "none", "BTL", ["production"], "On-set trauma first aid, safety triage and medical emergencies.", True, ["H01", "C04"], ["H01", "B07"]),
    ("C22", "completion_guarantor", "Completion Guarantor", "நிறைவு உத்தரவாத அதிகாரி", "समापन गारंटर", "C", "none", "COMMERCIAL", ["prep", "production", "post"], "Insurance-backed takeover rights if production breaches budget/deadline.", True, ["C02"], ["C02", "C01", "C04", "N14"]),
    ("C23", "insurance_broker", "Entertainment Insurance Broker", "திரைப்பட காப்பீட்டுத் தரகர்", "मनोरंजन बीमा दलाल", "C", "none", "COMMERCIAL", ["prep", "production"], "Arranges cast abandonment, negative, gear and liability policies.", False, ["C01"], ["C01", "C22"]),
    # Additions
    ("C24", "unit_hand_spot_boy", "Unit Hand / Spot Boy", "ஸ்பாட் பாய் / யூனிட் உதவியாளர்", "स्पॉट बॉय", "C", "none", "BTL", ["production"], "Artist assistance, hydration, vanity van support and immediate set needs.", False, ["C08"], ["C20", "D01"]),
    ("C25", "junior_artist_supplier", "Junior Artist Supplier / Agent", "ஜூனியர் ஆர்ட்டிஸ்ட் சப்ளையர்", "जूनियर आर्टिस्ट सप्लायर", "C", "none", "BTL", ["production"], "Rapid mobilization of 100-1000 daily wage background extras.", False, ["C06", "B08"], ["B08", "D05", "D06"]),

    # Band D
    ("D01", "lead_actor", "Lead Actor / Principal Cast", "கதாநாயகன் / முதன்மை நடிகர்", "मुख्य अभिनेता", "D", "none", "ATL", ["prep", "production"], "Headlining star talent defining schedule critical path.", False, ["B01"], ["B01", "D11", "B08"]),
    ("D02", "supporting_actor", "Supporting Actor", "துணை நடிகர்", "सहायक अभिनेता", "D", "none", "ATL", ["prep", "production"], "Credited dramatic core providing narrative counterweight.", False, ["B01"], ["B01", "D01"]),
    ("D03", "character_artist", "Character Artist / Comedian", "குணச்சித்திர நடிகர் / நகைச்சுவையாளர்", "चरित्र अभिनेता", "D", "none", "ATL", ["production"], "Signature comic or dramatic persona with tailored punch lines.", False, ["B01"], ["B01", "A03"]),
    ("D04", "child_artist", "Child Artist", "குழந்தை நட்சத்திரம்", "बाल कलाकार", "D", "none", "ATL", ["production"], "Minor performers strictly bounded by working hours and tutelage.", False, ["B01", "B08"], ["B08", "C21"]),
    ("D05", "background_artist", "Background Artist / Extra", "துணை நடிகர் / எக்ஸ்ட்ரா", "पृष्ठभूमि कलाकार", "D", "none", "BTL", ["production"], "Populates market, battle, hospital and court environments.", False, ["B08", "D06"], ["D06", "F20"]),
    ("D06", "crowd_coordinator", "Crowd Coordinator", "கூட்ட ஒருங்கிணைப்பாளர்", "भीड़ समन्वयक", "D", "none", "BTL", ["production"], "Segments and wrangles mass crowds into costume and camera blocks.", False, ["B08"], ["B08", "C25", "F20"]),
    ("D07", "stand_in", "Stand-In", "லைட்டிங் மாற்று நடிகர்", "स्टैंड-इन", "D", "none", "BTL", ["production"], "Substitutes for star during lighting setups and lens calibrations.", False, ["E01", "B08"], ["E01", "E13"]),
    ("D08", "body_double", "Body Double", "உடல் மாற்று நடிகர்", "बॉडी डबल", "D", "none", "BTL", ["production"], "Specific hand, silhouette or physique double for designated shots.", False, ["B01"], ["B01", "E01"]),
    ("D09", "dubbing_artist", "Dubbing Artist / Voice Actor", "டப்பிங் கலைஞர்", "डबिंग आर्टिस्ट", "D", "none", "POST", ["post"], "Voice matches star performance in primary and foreign languages.", False, ["B13"], ["B13", "J12"]),
    ("D10", "playback_singer", "Playback Singer", "பின்னணிப் பாடகர்", "पार्श्व गायक", "D", "lyrics", "ATL", ["production"], "Sings iconic studio numbers synced to screen lip movement.", False, ["G01"], ["G01", "G07", "G08"]),
    ("D11", "acting_coach", "Acting Coach", "நடிப்புப் பயிற்சியாளர்", "अभिनय कोच", "D", "none", "ATL", ["prep", "production"], "Emotional preparation, subtext clarity and rehearsal drilling.", False, ["B01"], ["B01", "D01"]),
    ("D12", "dialect_coach", "Dialect / Language Coach", "மொழி மற்றும் உச்சரிப்பு பயிற்சியாளர்", "बोली कोच", "D", "none", "ATL", ["prep", "production"], "Phonetic accuracy in regional dialects (e.g. Madurai/Kalyana Karnataka).", False, ["B01", "A03"], ["A03", "D01", "I24"]),
    ("D13", "movement_coach", "Movement Coach", "உடல் அசைவு பயிற்சியாளர்", "मूवमेंट कोच", "D", "none", "ATL", ["prep", "production"], "Physical gait, period deportment and physical characterization.", False, ["B01"], ["B01", "G18", "D01"]),
    ("D14", "talent_manager", "Talent Agent / Manager", "நடிகர் மேலாளர்", "प्रतिभा प्रबंधक", "D", "none", "COMMERCIAL", ["development", "prep", "production"], "Commercial contracts, perks, dates and security rider negotiation.", False, ["C01"], ["C01", "D01", "N01"]),

    # Band E
    ("E01", "cinematographer", "Director of Photography / Cinematographer", "ஒளிப்பதிவாளர்", "छायाकार", "E", "none", "ATL", ["prep", "production"], "Visual author: camera placement, lens choice and lighting design.", True, ["B01"], ["B01", "E13", "E17", "E11", "J08"]),
    ("E02", "camera_operator", "Camera Operator", "கேமரா ஆபரேட்டர்", "कैमरा ऑपरेटर", "E", "none", "BTL", ["production"], "Physically operates A-camera pans, tilts and tracking.", False, ["E01"], ["E01", "E03"]),
    ("E03", "focus_puller", "1st Assistant Camera / Focus Puller", "ஃபோகஸ் புல்லர்", "फोकस पुलर", "E", "none", "BTL", ["production"], "Critical distance measurement, depth of field and tack-sharp focus.", False, ["E01"], ["E01", "E02", "E04"]),
    ("E04", "clapper_loader", "2nd Assistant Camera / Clapper Loader", "கிளாப்பர் லோடர்", "क्लैपर लोडर", "E", "none", "BTL", ["production"], "Slates takes, manages camera reports and media mag loading.", False, ["E03"], ["E03", "E11", "B11"]),
    ("E05", "dop_team_pool", "DOP Team / Camera Assistant Pool", "ஒளிப்பதிவுக் குழு", "डीओपी टीम", "E", "none", "BTL", ["production"], "Lens swaps, matte boxes, monitor runs and battery charging.", False, ["E03"], ["E03", "E04"]),
    ("E06", "steadicam_operator", "Steadicam / Gimbal Operator", "ஸ்டெடிகேம் ஆபரேட்டர்", "स्टेडीकैम ऑपरेटर", "E", "none", "BTL", ["production"], "Dynamic fluid tracking shots through doorways and terrain.", False, ["E01"], ["E01", "B01"]),
    ("E07", "jib_operator", "Crane / Jimmy Jib Operator", "ஜிம்மி ஜிப் ஆபரேட்டர்", "क्रेन ऑपरेटर", "E", "none", "BTL", ["production"], "Sweeping high-angle crane and counterweight jib moves.", False, ["E01"], ["E01", "E17"]),
    ("E08", "drone_operator", "Drone / Aerial Operator", "ட்ரோன் ஆபரேட்டர்", "ड्रोन ऑपरेटर", "E", "none", "BTL", ["production"], "Aerial sweeps, GPS flight paths and civil aviation airspace clearances.", False, ["E01"], ["E01", "C16"]),
    ("E09", "underwater_camera_operator", "Underwater Camera Operator", "நீருக்கடி கேமரா ஆபரேட்டர்", "पानी के नीचे का कैमरा ऑपरेटर", "E", "none", "BTL", ["production"], "Sub-surface waterproof housings, diving safety and scuba shots.", False, ["E01"], ["E01", "H10"]),
    ("E10", "high_speed_camera_tech", "High-Speed / Specialty Camera Tech", "ஹை-ஸ்பீட் கேமரா தொழில்நுட்பவியலாளர்", "हाई-स्पीड कैमरा तकनीशियन", "E", "none", "BTL", ["production"], "Phantom 1000fps capture, probe macro lenses and specialized rigs.", False, ["E01"], ["E01", "E11"]),
    ("E11", "dit", "Digital Imaging Technician (DIT)", "டிஜிட்டல் இமேஜிங் தொழில்நுட்பவியலாளர்", "डिजिटल इमेजिंग तकनीशियन", "E", "none", "BTL", ["production"], "Zero-data-loss checksum backups (xxHash64), on-set CDL/LUT color.", True, ["E01", "C04"], ["E01", "E04", "J08", "J09"]),
    ("E12", "video_assist_operator", "Video Assist / Playback Operator", "வீடியோ அசிஸ்ட் ஆபரேட்டர்", "वीडियो असिस्ट ऑपरेटर", "E", "none", "BTL", ["production"], "Wireless monitor feeds to director village and instant take review.", False, ["B01"], ["B01", "B07"]),
    ("E13", "gaffer", "Gaffer / Chief Lighting Technician", "தலைமை ஒளி அமைப்பாளர்", "गैफर", "E", "none", "BTL", ["production"], "Executes DP lighting plot, power drops and fixture safety.", False, ["E01"], ["E01", "E14", "E15", "E16"]),
    ("E14", "best_boy_electric", "Best Boy Electric", "உதவி எலக்ட்ரீசியன்", "बेस्ट बॉय इलेक्ट्रिक", "E", "none", "BTL", ["production"], "Crew assignments, generator cable inventory and equipment trucks.", False, ["E13"], ["E13", "E15"]),
    ("E15", "lightman", "Lighting Technician / Lightman", "லைட்மேன்", "लाइटमैन", "E", "none", "BTL", ["production"], "Rigs HMI/LED/Skypanels; largest physical crew on Indian sets.", False, ["E14"], ["E14", "E23"]),
    ("E16", "generator_operator", "Generator Operator", "ஜெனரேட்டர் ஆபரேட்டர்", "जनरेटर ऑपरेटर", "E", "none", "BTL", ["production"], "Phase balance, fuel delivery and silent mobile power continuity.", False, ["E14"], ["E14", "C16"]),
    ("E17", "key_grip", "Key Grip", "தலைமை கிரிப்", "की ग्रिप", "E", "none", "BTL", ["production"], "Head of camera rigging, dollies, silks, overhead flags and safety.", False, ["E01"], ["E01", "E18", "E19"]),
    ("E18", "best_boy_grip", "Best Boy Grip", "உதவி கிரிப்", "बेस्ट बॉय ग्रिप", "E", "none", "BTL", ["production"], "Grip truck staging, pipe clamps, sandbags and rigging hardware.", False, ["E17"], ["E17", "E20"]),
    ("E19", "dolly_grip", "Dolly Grip", "டாலி கிரிப்", "डॉली ग्रिप", "E", "none", "BTL", ["production"], "Lays track, levels rails and executes smooth compound dolly push-ins.", False, ["E17"], ["E17", "E02"]),
    ("E20", "rigging_grip", "Rigging Grip / Rigging Gaffer", "ரிக்சிங் கிரிப்", "धांधली पकड़", "E", "none", "BTL", ["production"], "Pre-rigs trussing and greenscreens overnight before first unit.", False, ["E17"], ["E17", "E13"]),
    ("E21", "still_photographer", "Unit Still Photographer", "ஸ்டில் போட்டோகிராஃபர்", "स्टिल फोटोग्राफर", "E", "none", "BTL", ["production"], "Blimped high-resolution production stills for poster and PR key art.", False, ["M01"], ["M01", "M02", "B01"]),
    ("E22", "bts_videographer", "BTS Videographer / Making Team", "மேக்கிங் வீடியோ குழு", "बीटीएस वीडियोग्राफर", "E", "none", "BTL", ["production"], "Captures making-of footage, director breakdowns and viral promos.", False, ["M06"], ["M06", "B01"]),
    # Addition
    ("E23", "light_boy_helper", "Light Boy / Helper", "லைட் பாய் உதவியாளர்", "लाइट बॉय हेल्पर", "E", "none", "BTL", ["production"], "Reflector holding, cable runs, flag placement on Indian sets.", False, ["E15"], ["E15", "E14"]),

    # Band F
    ("F01", "production_designer", "Production Designer", "தயாரிப்பு வடிவமைப்பாளர்", "प्रोडक्शन डिज़ाइनर", "F", "none", "ATL", ["prep", "production"], "Conceptual master of physical visual world: architecture, period, palette.", True, ["B01"], ["B01", "E01", "F02", "F17", "F23"]),
    ("F02", "art_director", "Art Director", "கலை இயக்குநர்", "कला निर्देशक", "F", "none", "ATL", ["prep", "production"], "Translates designs into blueprints, set construction and finishes.", False, ["F01"], ["F01", "F03", "F07"]),
    ("F03", "assistant_art_director", "Assistant Art Director", "உதவி கலை இயக்குநர்", "सहायक कला निर्देशक", "F", "none", "BTL", ["prep", "production"], "Detailed set drafting, elevation measurements and build supervision.", False, ["F02"], ["F02", "F08"]),
    ("F04", "art_dept_coordinator", "Art Department Coordinator", "கலைத் துறை ஒருங்கிணைப்பாளர்", "कला विभाग समन्वयक", "F", "none", "BTL", ["prep", "production"], "Procurement, lumber orders, prop budgets and rental timelines.", False, ["F02"], ["F02", "C09"]),
    ("F05", "set_decorator", "Set Decorator", "செட் அலங்கரிப்பாளர்", "सेट डेकोरेटर", "F", "none", "BTL", ["prep", "production"], "Furnishes and decorates interior sets with period-true artifacts.", False, ["F01"], ["F01", "F06"]),
    ("F06", "set_dresser", "Set Dresser / Swing Gang", "செட் அமைப்பாளர்", "सेट ड्रेसर", "F", "none", "BTL", ["production"], "Places furniture, rugs, drapes and rearranges for reverse angles.", False, ["F05"], ["F05"]),
    ("F07", "construction_coordinator", "Construction Coordinator", "கட்டுமான ஒருங்கிணைப்பாளர்", "निर्माण समन्वयक", "F", "none", "BTL", ["prep"], "Manages master carpenters, welders, plasterers and structural integrity.", False, ["F02"], ["F02", "F08"]),
    ("F08", "set_carpenter", "Carpenter / Set Builder", "செட் தச்சர்", "बढ़ई", "F", "none", "BTL", ["prep"], "Builds timber flats, false walls, staircases and rostrums.", False, ["F07"], ["F07"]),
    ("F09", "scenic_painter", "Key Scenic / Painter", "பெயிண்டிங் கலைஞர்", "चित्रकार", "F", "none", "BTL", ["prep"], "Aging textures, faux marble, distress marks, rust and temple patina.", False, ["F02"], ["F02"]),
    ("F10", "matte_painter", "Matte Painter / Scenic Artist", "மேட் பெயிண்டர்", "मैट पेंटर", "F", "none", "BTL", ["prep", "post"], "Large-scale backdrops, ceiling extensions and horizon lines.", False, ["F01"], ["F01", "K01"]),
    ("F11", "greensperson", "Greensperson", "பசுமை அலங்கரிப்பாளர்", "हरियाली सज्जाकार", "F", "none", "BTL", ["production"], "Foliage, jungle trees, soil, plants and organic set dressing.", False, ["F05"], ["F05"]),
    ("F12", "property_master", "Property Master", "பொருட்கள் மேற்பார்வையாளர் (ப்ராப்ஸ்)", "प्रॉपर्टी मास्टर", "F", "none", "BTL", ["prep", "production"], "Continuity tracking and catalog of everything handled by actors.", False, ["F01"], ["F13", "F14", "B11"]),
    ("F13", "prop_maker", "Prop Maker / Fabricator", "ப்ராப் தயாரிப்பாளர்", "प्रॉप निर्माता", "F", "none", "BTL", ["prep"], "Handcrafts bespoke items: royal scepters, amulets, custom gear.", False, ["F12"], ["F12"]),
    ("F14", "armourer", "Armourer / Weapons Master", "ஆயுத மாஸ்டர்", "शस्त्रागार मास्टर", "F", "none", "BTL", ["production"], "Period swords, blank-firing firearms, safe replica storage and chain-of-custody.", True, ["H01", "B07"], ["H01", "B07", "C21"]),
    ("F15", "action_vehicle_coordinator", "Vehicle / Action Vehicle Coordinator", "வாகன ஒருங்கிணைப்பாளர்", "वाहन समन्वयक", "F", "none", "BTL", ["production"], "Vintage cars, police jeeps, modified chase rigs and breakdown fixes.", False, ["F01"], ["F01", "H07"]),
    ("F16", "animal_handler", "Animal Handler / Wrangler", "விலங்கு பயிற்சியாளர்", "पशु प्रशिक्षक", "F", "none", "BTL", ["production"], "Horses, dogs, elephants welfare, behavior cueing and AWBI compliance.", False, ["B07"], ["B07", "H12"]),
    ("F17", "costume_designer", "Costume Designer", "ஆடை வடிவமைப்பாளர்", "पोशाक डिज़ाइनर", "F", "none", "ATL", ["prep", "production"], "Wardrobe color arcs, silhouette language and period tailoring.", False, ["F01", "B01"], ["F01", "B01", "F18", "F23"]),
    ("F18", "assistant_costume_designer", "Assistant Costume Designer", "உதவி ஆடை வடிவமைப்பாளர்", "सहायक पोशाक डिज़ाइनर", "F", "none", "BTL", ["prep", "production"], "Fabric sourcing, swatch testing under camera lights and fitting logs.", False, ["F17"], ["F17", "F22"]),
    ("F19", "wardrobe_supervisor", "Wardrobe Supervisor", "ஆடை மேற்பார்வையாளர்", "वार्डरोब सुपरवाइजर", "F", "none", "BTL", ["production"], "On-set costume resets, blood/mud continuity doubles and tagging.", False, ["F17"], ["F17", "B11", "F20"]),
    ("F20", "set_costumer", "Set Costumer / Dresser", "செட் ஆடையமைப்பாளர்", "सेट कॉस्ट्यूमर", "F", "none", "BTL", ["production"], "Dresses stars and crowd between takes, iron touch-ups and quick changes.", False, ["F19"], ["F19", "D01", "D05"]),
    ("F21", "tailor_cutter", "Tailor / Seamstress / Cutter", "தையல்கலைஞர்", "दर्जी", "F", "none", "BTL", ["prep", "production"], "Immediate on-site alterations, stitch repairs and custom drapes.", False, ["F17"], ["F17"]),
    ("F22", "costume_buyer", "Costume Buyer / Shopper", "ஆடை வாங்குபவர்", "कॉस्ट्यूम क्रेता", "F", "none", "BTL", ["prep"], "Local and international textile hunting within allotted budgets.", False, ["F17"], ["F17", "C12"]),
    ("F23", "makeup_dept_head", "Makeup Department Head / Chief Makeup Artist", "தலைமை ஒப்பனைக் கலைஞர்", "मेकअप विभाग प्रमुख", "F", "none", "ATL", ["prep", "production"], "Design of facial looks, skin tones, aging stages and sweat continuity.", False, ["B01", "F01"], ["B01", "F24", "F25", "F27"]),
    ("F24", "makeup_artist", "Makeup Artist (Makeup Men / Women)", "ஒப்பனைக் கலைஞர்", "मेकअप आर्टिस्ट", "F", "none", "BTL", ["production"], "Daily application across hero, villain, character and crowd performers.", False, ["F23"], ["F23", "D01"]),
    ("F25", "hair_dept_head", "Hair Department Head / Hair Stylist", "தலைமை சிகையலங்கார நிபுணர்", "हेयर विभाग प्रमुख", "F", "none", "ATL", ["prep", "production"], "Signature hair silhouettes, period braids, mustaches and continuity.", False, ["F23"], ["F23", "F26"]),
    ("F26", "wig_maker", "Wig Maker / Hair Prosthetics", "விக் தயாரிப்பாளர்", "विग निर्माता", "F", "none", "BTL", ["prep", "production"], "Lace-front human hair wigs, period beards and bald cap blenders.", False, ["F25"], ["F25"]),
    ("F27", "sfx_prosthetics_artist", "Special Effects Makeup / Prosthetics Artist", "புரோஸ்தெடிக்ஸ் கலைஞர்", "प्रोस्थेटिक्स आर्टिस्ट", "F", "none", "BTL", ["prep", "production"], "Silicone wound appliances, creature skins, decapitations and scars.", False, ["F23"], ["F23", "H01"]),
    ("F28", "body_makeup_artist", "Body Makeup / Tattoo Artist", "உடல் ஒப்பனைக் கலைஞர்", "बॉडी मेकअप आर्टिस्ट", "F", "none", "BTL", ["production"], "Tribal tattoos, warrior battle grime, mud splatters and bronzing.", False, ["F23"], ["F23"]),

    # Band G
    ("G01", "music_director", "Music Director / Composer", "இசையமைப்பாளர்", "संगीत निर्देशक", "G", "none", "ATL", ["prep", "post"], "Composes original songs and dramatic orchestral background score.", True, ["B01"], ["B01", "A10", "G03", "G09", "G13"]),
    ("G02", "song_composer", "Song Composer / Tune Maker", "பாடல் மெட்டமைப்பாளர்", "धुन निर्माता", "G", "none", "ATL", ["development"], "Melody hooks and hook-step tunes for commercial numbers.", False, ["G01"], ["G01", "A10"]),
    ("G03", "music_programmer", "Music Programmer / Arranger", "இசை புரோகிராமர்", "संगीत प्रोग्रामर", "G", "none", "BTL", ["prep", "post"], "Synthesizer sequencing, DAW beats, ethnic sample layering and stems.", False, ["G01"], ["G01", "G04"]),
    ("G04", "orchestrator", "Orchestrator / Conductor", "ஆர்க்கெஸ்ட்ரா நடத்துனர்", "आर्केस्ट्रेटर", "G", "none", "BTL", ["post"], "Scores string and brass charts for live Prague or Budapest symphonies.", False, ["G01"], ["G01", "G05"]),
    ("G05", "session_musician", "Session Musician / Instrumentalist", "இசைக் கலைஞர்", "सत्र संगीतकार", "G", "none", "BTL", ["production", "post"], "Soloists: veena, flute, sarangi, electric guitar, mridangam.", False, ["G01"], ["G01", "G08"]),
    ("G06", "chorus_vocalist", "Chorus / Backing Vocalist", "குழுப் பாடகர்", "कोरस गायक", "G", "none", "BTL", ["post"], "Layered harmonies, classical chants and mass anthem backing.", False, ["G01"], ["G01", "G07"]),
    ("G07", "vocal_supervisor", "Vocal Supervisor", "குரல் மேற்பார்வையாளர்", "स्वर पर्यवेक्षक", "G", "none", "BTL", ["post"], "Guides playback singer pronunciation, pitch stability and emotion.", False, ["G01"], ["G01", "D10", "G08"]),
    ("G08", "music_recording_engineer", "Music Recording Engineer", "ஒலிப்பதிவு பொறியாளர்", "संगीत रिकॉर्डिंग इंजीनियर", "G", "none", "BTL", ["production", "post"], "Studio mic placement, preamp gain staging, low-noise isolation.", False, ["G01"], ["G01", "G05", "G12"]),
    ("G09", "music_supervisor", "Music Supervisor", "இசை மேற்பார்வையாளர்", "संगीत पर्यवेक्षक", "G", "none", "ATL", ["prep", "post"], "Licensing pre-existing songs, synchronization sync rights, cue sheets.", True, ["C01", "N07"], ["G01", "N07", "C01", "G10"]),
    ("G10", "music_clearance_coord", "Music Clearance Coordinator", "இசை அனுமதி ஒருங்கிணைப்பாளர்", "संगीत निकासी समन्वयक", "G", "none", "COMMERCIAL", ["post"], "Clears worldwide master and sync rights with record labels.", False, ["G09"], ["G09", "N07"]),
    ("G11", "music_editor", "Music Editor", "இசை எடிட்டர்", "संगीत संपादक", "G", "none", "POST", ["post"], "Conforms temporary score to edit cuts and aligns musical transitions.", False, ["J03"], ["J03", "G01"]),
    ("G12", "pre_mix_engineer", "Pre-Mix Engineer", "ப்ரீ-மிக்ஸ் பொறியாளர்", "प्री-मिक्स इंजीनियर", "G", "none", "POST", ["post"], "Stems grouping (Dialogue, Music, FX) before Atmos re-recording.", False, ["G13"], ["G13", "G08"]),
    ("G13", "mix_mastering_engineer", "Mix and Mastering Engineer", "மிக்ஸ் மற்றும் மாஸ்டரிங் பொறியாளர்", "मिक्सिंग इंजीनियर", "G", "none", "POST", ["post"], "Final dynamic balance, LUFS loudness mastering for theatre/streaming.", False, ["G01"], ["G01", "G12", "J15"]),
    ("G14", "production_sound_mixer", "Production Sound Mixer", "நேரடி ஒலிப்பதிவாளர்", "प्रोडक्शन साउंड मिक्सर", "G", "none", "BTL", ["production"], "Captures crisp on-set dialogue, ambient sound and wireless lavaliers.", False, ["B01"], ["B01", "G15", "G16", "J12"]),
    ("G15", "boom_operator", "Boom Operator", "பூம் ஆபரேட்டர்", "बूम ऑपरेटर", "G", "none", "BTL", ["production"], "Operates shotgun boom mic just out of frame line without shadow cast.", False, ["G14"], ["G14", "E01"]),
    ("G16", "utility_sound_tech", "Utility Sound Technician", "ஒலி தொழில்நுட்ப உதவியாளர்", "ध्वनि तकनीशियन", "G", "none", "BTL", ["production"], "Lavalier mic planting, battery replacements and antenna boosters.", False, ["G14"], ["G14"]),
    ("G17", "sound_designer", "Sound Designer", "ஒலி வடிவமைப்பாளர்", "साउंड डिज़ाइनर", "G", "none", "ATL", ["post"], "Creates sonic signature: weapon hits, sci-fi hums, mythical beasts.", False, ["B01"], ["B01", "J11", "J15"]),
    ("G18", "dance_master", "Dance Master / Choreographer", "நடன இயக்குநர்", "नृत्य निर्देशक", "G", "none", "ATL", ["production"], "Headlining credit designing iconic dance hooks and troupe steps.", False, ["B01"], ["B01", "G01", "G19", "G20", "D01"]),
    ("G19", "assistant_choreographer", "Assistant Choreographer", "உதவி நடன இயக்குநர்", "सहायक नृत्य निर्देशक", "G", "none", "BTL", ["production"], "Drills star rehearsals and leads back-row dancers in rhythm.", False, ["G18"], ["G18", "G20"]),
    ("G20", "dance_troupe_coordinator", "Dance Troupe Coordinator", "நடனக் குழு ஒருங்கிணைப்பாளர்", "नृत्य मंडली समन्वयक", "G", "none", "BTL", ["production"], "Travel, costumes and calls for 50-100 synchronized group dancers.", False, ["G18"], ["G18", "C08"]),

    # Band H
    ("H01", "fight_master", "Fight Master / Stunt Coordinator", "சண்டைப் பயிற்சியாளர்", "स्टंट समन्वयक", "H", "none", "ATL", ["prep", "production"], "Absolute stop authority on set for action safety; action designer.", True, ["B01", "C04"], ["B01", "C04", "H02", "H06", "C21"]),
    ("H02", "assistant_fight_master", "Assistant Fight Master", "உதவி சண்டைப் பயிற்சியாளர்", "सहायक स्टंट मास्टर", "H", "none", "BTL", ["production"], "Rehearses gags with stunt players and pads up performers.", False, ["H01"], ["H01", "H05"]),
    ("H03", "martial_arts_choreographer", "Fight Choreographer / Martial Arts Master", "தற்காப்புக் கலை ஆசிரியர்", "मार्शल आर्ट्स मास्टर", "H", "none", "ATL", ["prep", "production"], "Style-specific combat (Silambam, Kalaripayattu, Wuxia strike rhythms).", False, ["H01"], ["H01", "D01"]),
    ("H04", "stunt_double", "Stunt Double", "டூப் நடிகர்", "स्टंट डबल", "H", "none", "BTL", ["production"], "High falls, fire burns, stair tumbles doubling lead actors.", False, ["H01"], ["H01", "D01"]),
    ("H05", "stunt_performer", "Stunt Performer / Player", "சண்டைக் கலைஞர்", "स्टंट कलाकार", "H", "none", "BTL", ["production"], "Henchmen reactions, glass breakaways and punch deliveries.", False, ["H01"], ["H01", "H02"]),
    ("H06", "wire_rigging_specialist", "Wire Work / Rigging Specialist", "கம்பிப் பயிற்சி நிபுணர்", "वायर रिगिंग विशेषज्ञ", "H", "none", "BTL", ["production"], "High-tensile flying harnesses, counterweight pullers and truss rigs.", True, ["H01"], ["H01", "H04", "H05"]),
    ("H07", "stunt_driver", "Vehicle Stunt / Precision Driver", "சாகச வாகன ஓட்டுநர்", "सटीक चालक", "H", "none", "BTL", ["production"], "Handbrake turns, drifting, pipe-ramp rollovers and high-speed near-misses.", True, ["H01"], ["H01", "F15"]),
    ("H08", "sfx_supervisor", "Special Effects Supervisor", "ஸ்பெஷல் எஃபெக்ட்ஸ் மேற்பார்வையாளர்", "एसएफएक्स सुपरवाइजर", "H", "none", "ATL", ["prep", "production"], "Practical rain rigs, wind machines, bullet squibs and mechanical rigs.", True, ["B01", "H01"], ["B01", "H01", "H09"]),
    ("H09", "pyrotechnician", "SFX Technician / Pyrotechnician", "வெடிபொருள் தொழில்நுட்பவியலாளர்", "आतिशबाज़ी तकनीशियन", "H", "none", "BTL", ["production"], "Controlled explosions, fireball mortars, debris cannons and spark hits.", True, ["H08"], ["H08", "C21"]),
    ("H10", "marine_safety_specialist", "Underwater / Marine Safety Specialist", "கடல் மற்றும் நீர் பாதுகாப்பு நிபுணர்", "समुद्री सुरक्षा विशेषज्ञ", "H", "none", "BTL", ["production"], "Safety divers, oxygen tanks and offshore sea currents surveillance.", True, ["H01"], ["H01", "E09"]),
    ("H11", "aerial_safety_specialist", "Height / Aerial Safety Specialist", "உயரப் பாதுகாப்பு நிபுணர்", "हवाई सुरक्षा विशेषज्ञ", "H", "none", "BTL", ["production"], "Cliff edge safety lines, fall nets and harness certifications.", True, ["H01"], ["H01", "H06"]),
    ("H12", "animal_action_coordinator", "Animal Action Coordinator", "விலங்கு சாகச ஒருங்கிணைப்பாளர்", "पशु एक्शन समन्वयक", "H", "none", "BTL", ["production"], "Choreographs horse charges, canine lunges without harm to animals.", False, ["H01"], ["H01", "F16"]),

    # Band I (Seed SMEs + Spawner)
    ("I01", "sme_police", "Police / Law Enforcement Advisor", "காவல்துறை ஆலோசகர்", "पुलिस सलाहकार", "I", "none", "ADVISORY", ["development", "prep", "production"], "Procedure, arrest protocols, FIR filing, weapon handling realism.", False, ["B01"], ["B01", "A03", "F12"]),
    ("I02", "sme_military", "Military / Defence Advisor", "ராணுவ ஆலோசகர்", "सैन्य सलाहकार", "I", "none", "ADVISORY", ["development", "prep", "production"], "Rank insignia, drills, tactical formations and wartime commands.", False, ["B01"], ["B01", "F17", "F14"]),
    ("I03", "sme_legal", "Legal / Courtroom Advisor", "சட்ட ஆலோசகர்", "कानूनी सलाहकार", "I", "none", "ADVISORY", ["development", "prep"], "Courtroom etiquette, legal terminology, penal code statutes.", False, ["B01"], ["A03", "B01"]),
    ("I04", "sme_medical", "Medical / Surgical Advisor", "மருத்துவ ஆலோசகர்", "चिकित्सा सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Surgical procedures, CPR cadence, monitors, clinical vocabulary.", False, ["B01"], ["F05", "D01"]),
    ("I05", "sme_forensic", "Forensic / Autopsy Advisor", "தடயவியல் ஆலோசகர்", "फोरेंसिक सलाहकार", "I", "none", "ADVISORY", ["development", "prep"], "Post-mortem reports, rigor mortis timeline, ballistics trajectory.", False, ["B01"], ["A02", "F27"]),
    ("I06", "sme_psychology", "Psychology / Psychiatry Advisor", "மனநல ஆலோசகர்", "मनोविज्ञान सलाहकार", "I", "none", "ADVISORY", ["development"], "Trauma responses, clinical diagnosis realism and psychological arc.", False, ["B01"], ["A01", "D01"]),
    ("I07", "sme_science", "Scientific / Space / Physics Advisor", "விஞ்ஞான ஆலோசகர்", "वैज्ञानिक सलाहकार", "I", "none", "ADVISORY", ["development"], "Orbital mechanics, relativistic principles, research lab credibility.", False, ["B01"], ["A02", "K01"]),
    ("I08", "sme_cybersecurity", "Technology / Cybersecurity Advisor", "சைபர் பாதுகாப்பு ஆலோசகர்", "साइबर सुरक्षा सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Realistic terminal syntax, network intrusion methods, zero-day realism.", False, ["B01"], ["F05", "A03"]),
    ("I09", "sme_finance", "Finance / Banking / Corporate Advisor", "நிதி மற்றும் வங்கி ஆலோசகர்", "वित्तीय सलाहकार", "I", "none", "ADVISORY", ["development"], "M&A deal mechanics, trading floor vernacular, money-laundering schemes.", False, ["B01"], ["A01", "A03"]),
    ("I10", "sme_political", "Political / Bureaucracy Advisor", "அரசியல் ஆலோசகர்", "राजनीतिक सलाहकार", "I", "none", "ADVISORY", ["development"], "Secretariat procedures, cabinet protocol, electoral dynamics.", False, ["B01"], ["A01", "A03"]),
    ("I11", "sme_journalism", "Journalism / Newsroom Advisor", "பத்திரிகைத் துறை ஆலோசகர்", "पत्रकारिता सलाहकार", "I", "none", "ADVISORY", ["development"], "Investigative source handling, print deadline chaos, sting ops.", False, ["B01"], ["A01"]),
    ("I12", "sme_sports", "Sports Advisor / Coach", "விளையாட்டு ஆலோசகர்", "खेल सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Sport-specific body language, tournament rules and referee gestures.", False, ["B01"], ["D01", "H01"]),
    ("I13", "sme_aviation", "Aviation / Pilot Advisor", "விமானப் போக்குவரத்து ஆலோசகர்", "विमानन सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Cockpit checklists, ATC phraseology, flight dynamics.", False, ["B01"], ["F05", "D01"]),
    ("I14", "sme_maritime", "Maritime / Fishing Advisor", "கடல் மற்றும் மீன்பிடி ஆலோசகர்", "समुद्री सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Trawler operation, navigation beacons, coastal dialect, sea tides.", False, ["B01"], ["A03", "H10"]),
    ("I15", "sme_agriculture", "Agriculture / Rural Livelihood Advisor", "விவசாய ஆலோசகர்", "कृषि सलाहकार", "I", "none", "ADVISORY", ["development", "prep"], "Crop cycles, canal water disputes, agrarian distress, village councils.", False, ["B01"], ["A01", "F01"]),
    ("I16", "sme_mining", "Industrial / Factory / Mining Advisor", "தொழில்துறை ஆலோசகர்", "खनन सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Coal shaft safety, smelter furnaces, union politics, blast warnings.", False, ["B01"], ["F01", "H08"]),
    ("I17", "sme_history", "Historical Period Advisor", "வரலாற்று ஆலோசகர்", "इतिहास सलाहकार", "I", "none", "ADVISORY", ["development", "prep"], "Material culture, customs, etiquette, weaponry of historical eras.", False, ["B01"], ["F01", "F17", "A01"]),
    ("I18", "sme_archaeology", "Archaeology / Epigraphy Advisor", "தொல்பொருள் ஆலோசகர்", "पुरातत्व सलाहकार", "I", "none", "ADVISORY", ["development"], "Grantha/Brahmi inscriptions, excavation strata, carbon dating.", False, ["B01"], ["A01", "F12"]),
    ("I19", "sme_mythology", "Mythology / Religious Text Advisor", "புராண ஆலோசகர்", "पौराणिक सलाहकार", "I", "none", "ADVISORY", ["development"], "Puranic citations, iconographic lore, ethical dilemmas.", False, ["B01"], ["A01", "A02"]),
    ("I20", "sme_temple_arch", "Temple Architecture / Iconography Advisor", "கோயில் கட்டிடக்கலை ஆலோசகர்", "मंदिर वास्तुकला सलाहकार", "I", "none", "ADVISORY", ["prep"], "Agama shastra, gopuram geometry, mandapa stone carving logic.", False, ["B01"], ["F01", "F02"]),
    ("I21", "sme_carnatic", "Classical Music Advisor", "கர்நாடக இசை ஆலோசகர்", "शास्त्रीय संगीत सलाहकार", "I", "none", "ADVISORY", ["prep", "post"], "Raga moods, tala structures, kutcheri stage performance protocols.", False, ["B01"], ["G01", "D01"]),
    ("I22", "sme_classical_dance", "Classical Dance Advisor", "பாரதநாட்டிய ஆலோசகர்", "शास्त्रीय नृत्य सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Abhinaya gestures, varnam choreographies, mudra correctness.", False, ["B01"], ["G18", "D01"]),
    ("I23", "sme_sangam_literature", "Sangam / Classical Literature Advisor", "சங்க இலக்கிய ஆலோசகர்", "संगम साहित्य सलाहकार", "I", "none", "ADVISORY", ["development"], "Thinai landscapes (Kurinji/Mullai), ancient poetics, Sangam diction.", False, ["B01"], ["A01", "A10"]),
    ("I24", "sme_dialect", "Linguistics / Dialect Advisor", "வட்டார வழக்கு மொழி ஆலோசகர்", "बोली भाषा सलाहकार", "I", "none", "ADVISORY", ["development", "production"], "Phonology and vocabulary of regional sociolects (Kongu, Nellai, Tirunelveli).", False, ["B01"], ["A03", "D12"]),
    ("I25", "sme_anthropology", "Anthropology / Community Advisor", "மானிடவியல் ஆலோசகர்", "मानव विज्ञान सलाहकार", "I", "none", "ADVISORY", ["development"], "Cultural rituals, tribal customs and community sensitivities.", False, ["B01"], ["A01", "F17"]),
    ("I26", "sme_religion", "Religion and Ritual Advisor", "சமயச் சடங்குகள் ஆலோசகர்", "धार्मिक अनुष्ठान सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Vedic, Islamic, Christian ritual authenticity, sacred chants.", False, ["B01"], ["F05", "A03"]),
    ("I27", "sme_culinary", "Culinary Advisor", "சமையற்கலை ஆலோசகர்", "पाक कला सलाहकार", "I", "none", "ADVISORY", ["production"], "Traditional recipes, kitchen implements, royal feast presentations.", False, ["B01"], ["F12", "C20"]),
    ("I28", "sme_textile", "Fashion / Textile Historian", "நெசவு மற்றும் ஆடை வரலாற்று ஆலோசகர்", "कपड़ा इतिहासकार", "I", "none", "ADVISORY", ["prep"], "Handloom weaves, natural dye origins, historical drapes.", False, ["B01"], ["F17", "F22"]),
    ("I29", "sme_automotive", "Automotive / Machinery Advisor", "வாகன இயந்திரவியல் ஆலோசகர்", "मोटर वाहन सलाहकार", "I", "none", "ADVISORY", ["production"], "Engine mechanics, vintage transmissions, locomotive controls.", False, ["B01"], ["F15", "H07"]),
    ("I30", "sme_weapons", "Weapons / Ballistics Advisor", "ஆயுத மற்றும் துப்பாக்கி ஆலோசகர்", "हथियार सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Recoil impulse, muzzle flash, cartridge calibers, edged steel weight.", False, ["B01"], ["F14", "H01"]),
    ("I31", "sme_wildlife", "Wildlife / Ecology Advisor", "வனவிலங்கு மற்றும் சுற்றுச்சூழல் ஆலோசகர்", "वन्यजीव सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Predator behaviors, snakebite protocols, rainforest biology.", False, ["B01"], ["F16", "C16"]),
    ("I32", "sme_disability", "Disability Representation Advisor", "மாற்றுத்திறனாளி பிரதிநிதித்துவ ஆலோசகர்", "दिव्यांगता सलाहकार", "I", "none", "ADVISORY", ["development", "production"], "Lived experience truth, respectful portrayal, adaptive mobility equipment.", False, ["B01"], ["A01", "D01"]),
    ("I33", "sme_sign_language", "Sign Language Advisor / Interpreter", "சைகை மொழி ஆலோசகர்", "सांकेतिक भाषा सलाहकार", "I", "none", "ADVISORY", ["prep", "production"], "Indian Sign Language (ISL) grammar, facial syntax and clarity.", False, ["B01"], ["D01", "B01"]),
    ("I34", "sme_occult", "Paranormal / Occult Lore Advisor", "மர்ம மற்றும் அமானுஷ்ய ஆலோசகர்", "तांत्रिक विद्या सलाहकार", "I", "none", "ADVISORY", ["development"], "Folklore consistency, ghost wards, talisman mythology for dark fantasy.", False, ["B01"], ["A01", "Q04"]),
    ("I35", "sme_underworld", "Sports Betting / Underworld Advisor", "பாதாள உலக ஆலோசகர்", "अपराध सलाहकार", "I", "none", "ADVISORY", ["development"], "Hawala routes, syndicate hierarchies, match-fixing mechanics.", False, ["B01"], ["A01", "A03"]),
    ("I36", "sme_spawner_agent", "Dynamic SME Spawner", "டைனமிக் நிபுணர் உருவாக்கும் முகவர்", "गतिशील विशेषज्ञ निर्माता", "I", "none", "PLATFORM", ["development", "prep"], "Meta-agent extracting script entities and synthesizing new advisor personas.", False, ["B01"], ["A01", "A02", "P01"]),

    # Band J
    ("J01", "post_supervisor", "Post-Production Supervisor", "தயாரிப்புக்குப் பிந்தைய மேற்பார்வையாளர்", "पोस्ट-प्रोडक्शन सुपरवाइजर", "J", "none", "ATL", ["post"], "Guides delivery schedule, lab bookings, VFX turnover, Atmos finishing.", True, ["C01"], ["C01", "J03", "K01", "J08", "J15"]),
    ("J02", "post_coordinator", "Post-Production Coordinator", "போஸ்ட் புரொடக்ஷன் ஒருங்கிணைப்பாளர்", "पोस्ट समन्वयक", "J", "none", "BTL", ["post"], "Media hard drive runs, vendor LTO archives and facility bookings.", False, ["J01"], ["J01", "J06"]),
    ("J03", "editor", "Editor", "படத்தொகுப்பாளர்", "संपादक", "J", "none", "ATL", ["production", "post"], "Primary rhythmic assembler of cinematic narrative and performance pace.", True, ["B01"], ["B01", "J04", "J05", "J06", "K04"]),
    ("J04", "chief_associate_editor", "Chief Associate Editor", "தலைமை உதவி படத்தொகுப்பாளர்", "मुख्य सहयोगी संपादक", "J", "none", "ATL", ["post"], "First assembly cuts, scene trims and editorial conform supervision.", False, ["J03"], ["J03", "J05"]),
    ("J05", "associate_editor", "Associate Editor", "இணை படத்தொகுப்பாளர்", "सहयोगी संपादक", "J", "none", "BTL", ["post"], "Song cutting, fight scene pacing and rough sync assemblies.", False, ["J03"], ["J03", "J06"]),
    ("J06", "assistant_editor", "Assistant Editor", "உதவி படத்தொகுப்பாளர்", "सहायक संपादक", "J", "none", "BTL", ["production", "post"], "Dailies sync, bin management, turnover exports to sound and VFX.", False, ["J03"], ["J03", "E11", "J02"]),
    ("J07", "trailer_editor", "Teaser / Trailer Cut Editor", "டிரெய்லர் படத்தொகுப்பாளர்", "ट्रेलर संपादक", "J", "none", "POST", ["post"], "High-impact promotional cuts maximizing excitement and mystery.", False, ["M01", "B01"], ["M01", "B01", "M04"]),
    ("J08", "colorist", "Colorist", "வண்ணக் கலைஞர் (கலரிஸ்ட்)", "कलर ग्रेडर", "J", "none", "ATL", ["post"], "Final theatrical color grade (DaVinci Resolve, ACES, P3 DCI gamut).", True, ["E01", "B01"], ["E01", "B01", "J09"]),
    ("J09", "di_facility_lead", "DI Facility Lead", "டிஐ ஆய்வக முதன்மையாளர்", "डीआई लैब प्रमुख", "J", "none", "POST", ["post"], "Digital Intermediate pipeline calibration, projector xenon/laser profiles.", False, ["J08"], ["J08", "J10"]),
    ("J10", "online_conform_editor", "Conform / Online Editor", "ஆன்லைன் கன்ஃபார்ம் எடிட்டர்", "ऑनलाइन संपादक", "J", "none", "BTL", ["post"], "Replaces offline proxy cuts with original camera RAW files seamlessly.", False, ["J01"], ["J06", "J08"]),
    ("J11", "sound_editor", "Sound Editor", "ஒலி எடிட்டர்", "ध्वनि संपादक", "J", "none", "POST", ["post"], "Cuts Foley, backgrounds, gunshots, vehicle engines and ambiences.", False, ["G17"], ["G17", "J12"]),
    ("J12", "dialogue_editor", "Dialogue Editor", "வசன ஒலி எடிட்டர்", "संवाद संपादक", "J", "none", "POST", ["post"], "Dialogue noise removal (iZotope RX), room tone smoothing and sync.", False, ["G14"], ["G14", "J13"]),
    ("J13", "adr_supervisor", "ADR Supervisor / Editor", "ஏடிஆர் டப்பிங் மேற்பார்வையாளர்", "एडीआर सुपरवाइजर", "J", "none", "POST", ["post"], "Automated Dialogue Replacement studio sessions and lip-sync alignment.", False, ["B13"], ["B13", "D09"]),
    ("J14", "foley_artist", "Foley Artist / Foley Mixer", "ஃபோலி கலைஞர்", "फ़ॉली कलाकार", "J", "none", "BTL", ["post"], "Performs footsteps, cloth rustle, weapon grabs on synchronized pits.", False, ["G17"], ["G17", "J11"]),
    ("J15", "atmos_mix_engineer", "Re-Recording Mixer / Atmos Mix Engineer", "டால்பி அட்மாஸ் மிக்ஸிங் பொறியாளர்", "डॉलबी एटमॉस मिक्सर", "J", "none", "ATL", ["post"], "7.1.4 / theatrical 64-speaker 3D spatial pan and dynamic mastering.", True, ["B01"], ["B01", "G01", "G17", "G13"]),
    ("J16", "subtitler", "Subtitler / Captioner", "துணைத்தலைப்பு உருவாக்குநர்", "उपशीर्षक लेखक", "J", "none", "POST", ["post"], "Translates and times multilingual subtitles adhering to character limits.", False, ["J17"], ["A03", "J17"]),
    ("J17", "localization_manager", "Localization Manager", "மொழியாக்க மேலாளர்", "स्थानीयकरण प्रबंधक", "J", "none", "POST", ["post"], "Coordinates dubbing, subbing and metadata packaging across 20+ markets.", False, ["L01"], ["J16", "B13", "L07"]),
    ("J18", "qc_technician", "QC Technician", "தரக்கட்டுப்பாட்டு தொழில்நுட்பவியலாளர்", "गुणवत्ता नियंत्रण तकनीशियन", "J", "none", "POST", ["post"], "Hard rejects for dead pixels, flash frame errors, phase cancellation.", True, ["J01"], ["J01", "J19"]),
    ("J19", "deliverables_mastering_mgr", "Deliverables / Mastering Manager", "டிசிபி மாஸ்டரிங் மேலாளர்", "मास्टरिंग प्रबंधक", "J", "none", "POST", ["post"], "DCI-DCP packaging, KDM encryption keys, Netflix IMF CPL delivery.", True, ["L07"], ["L07", "J18"]),
    ("J20", "post_td", "Post Technical Director", "தொழில்நுட்ப இயக்குநர் (போஸ்ட்)", "पोस्ट तकनीकी निदेशक", "J", "none", "PLATFORM", ["post"], "Storage SAN bandwidth, render node scripts and color science scripts.", False, ["J01"], ["J01", "P01"]),
    # Additions
    ("J21", "subtitle_qc_specialist", "Subtitle QC & Conform Specialist", "துணைத்தலைப்பு தரக்கட்டுப்பாட்டாளர்", "उपशीर्षक गुणवत्ता निरीक्षक", "J", "none", "POST", ["post"], "Audits reading speed (CPS), temporal drift and cultural idiomatic humor.", True, ["J16"], ["J16", "J17"]),
    ("J22", "dubbing_studio_manager", "Dubbing Studio Operations Manager", "டப்பிங் ஸ்டுடியோ மேலாளர்", "डबिंग स्टूडियो प्रबंधक", "J", "none", "POST", ["post"], "Schedules multi-language artist tracks, booth acoustics and mic checks.", False, ["B13"], ["B13", "D09"]),

    # Band K
    ("K01", "vfx_supervisor", "VFX Supervisor", "விஎப்எக்ஸ் மேற்பார்வையாளர்", "वीएफएक्स सुपरवाइजर", "K", "none", "ATL", ["prep", "production", "post"], "Visual effects architect owning methodology, photorealism and bids.", True, ["B01"], ["B01", "K02", "K03", "K07", "J03"]),
    ("K02", "vfx_producer", "VFX Producer", "விஎப்எக்ஸ் தயாரிப்பாளர்", "वीएफएक्स निर्माता", "K", "none", "ATL", ["prep", "post"], "Shot bids, vendor allocations, milestones and outsourced studio budgets.", True, ["C01", "K01"], ["C01", "K01", "C04"]),
    ("K03", "vfx_creative_director", "VFX Creative Director", "விஎப்எக்ஸ் படைப்பு இயக்குநர்", "वीएफएक्स क्रिएटिव डायरेक्टर", "K", "none", "ATL", ["post"], "Aesthetic consistency across creature textures, magic spells and spaces.", False, ["K01"], ["K01", "F01"]),
    ("K04", "vfx_editor", "VFX Editor", "விஎப்எக்ஸ் எடிட்டர்", "वीएफएक्स संपादक", "K", "none", "POST", ["post"], "Shot counts, plate turnovers, handles, matte cutouts and version logs.", False, ["J03"], ["J03", "K05"]),
    ("K05", "vfx_coordinator", "VFX Coordinator", "விஎப்எக்ஸ் ஒருங்கிணைப்பாளர்", "वीएफएक्स समन्वयक", "K", "none", "BTL", ["post"], "Shotgun/Ftrack database updates, client review playlists and deliveries.", False, ["K02"], ["K02", "K04"]),
    ("K06", "onset_data_wrangler", "On-Set VFX Data Wrangler", "செட் விஎப்எக்ஸ் தரவு சேகரிப்பாளர்", "ऑन-सेट डेटा रैंगलर", "K", "none", "BTL", ["production"], "Shoots chrome/grey balls, 360 HDRI lighting rigs, lens focal lengths.", False, ["K01"], ["K01", "E01"]),
    ("K07", "compositor", "Compositor", "காம்போசிட்டர்", "कंपोजिटर", "K", "none", "BTL", ["post"], "Final 2D integration of live action plates, CG passes, grain and flares.", False, ["K01"], ["K01", "K08"]),
    ("K08", "cg_generalist", "CG Generalist", "சிஜி கலைஞர்", "सीजी जनरलिस्ट", "K", "none", "BTL", ["post"], "3D assets, lighting, modeling and shading across shot turnarounds.", False, ["K01"], ["K07", "K09"]),
    ("K09", "modeler", "Modeler", "3D மாடலர்", "मॉडलर", "K", "none", "BTL", ["post"], "High-poly polygonal surfaces: palace pillars, mythical creatures, tanks.", False, ["K01"], ["K10", "K11"]),
    ("K10", "texture_artist", "Texture / Look-Dev Artist", "டெக்ஸ்ச்சர் கலைஞர்", "बनावट कलाकार", "K", "none", "BTL", ["post"], "Physically Based Rendering (PBR) roughness, specular maps and displacement.", False, ["K01"], ["K09", "K15"]),
    ("K11", "rigger", "Rigger", "ரிக்கர்", "रिगर", "K", "none", "BTL", ["post"], "Skeletal hierarchies, muscle deformations and facial FACS blendshapes.", False, ["K01"], ["K09", "K12"]),
    ("K12", "animator", "Animator", "இயங்குபட கலைஞர் (அனிமேட்டர்)", "एनिमेटर", "K", "none", "BTL", ["post"], "Keyframe character performance, creature weight, gait and flight paths.", False, ["K03"], ["K11", "K13"]),
    ("K13", "layout_artist", "Layout Artist", "லேஅவுட் கலைஞர்", "लेआउट कलाकार", "K", "none", "BTL", ["post"], "Stages 3D set assets, camera framing and environment placement.", False, ["K01"], ["A16", "K12"]),
    ("K14", "fx_simulation_td", "FX / Simulation TD", "சிமுலேஷன் கலைஞர்", "सिमुलेशन टीडी", "K", "none", "BTL", ["post"], "Houdini fluids, firestorms, castle collapse destruction, crowds.", False, ["K01"], ["K07", "H08"]),
    ("K15", "lighting_rendering_td", "Lighting / Rendering TD", "லைட்டிங் மற்றும் ரெண்டரிங் கலைஞர்", "लाइटिंग टीडी", "K", "none", "BTL", ["post"], "Raymarching lights, Arnold/RenderMan passes and multi-channel EXRs.", False, ["K01"], ["K07", "K18"]),
    ("K16", "matchmove_artist", "Matchmove / Tracking Artist", "டிராக்கிங் கலைஞர்", "मैचमूव कलाकार", "K", "none", "BTL", ["post"], "3D camera tracking solves and point cloud ground planes.", False, ["K01"], ["K06", "K13"]),
    ("K17", "roto_paint_artist", "Rotoscope / Paint / Prep Artist", "ரோட்டோ மற்றும் கிளீனப் கலைஞர்", "रोटोस्कोप कलाकार", "K", "none", "BTL", ["post"], "Safety wire removal, rig paintouts, clean plates and actor mattes.", False, ["K07"], ["K07"]),
    ("K18", "render_wrangler", "Render Wrangler / Farm Operator", "ரெண்டர் ஃபார்ம் ஆபரேட்டர்", "रेंडर संचालक", "K", "none", "BTL", ["post"], "Cloud GPU instance provisioning, memory abort triage and job queueing.", False, ["K02"], ["K15", "P03"]),
    ("K19", "pipeline_td", "Pipeline TD", "பைப்லைன் தொழில்நுட்பவியலாளர்", "पाइपलाइन टीडी", "K", "none", "PLATFORM", ["post"], "Universal Scene Description (USD) pipelines, Shotgrid API integrations.", False, ["K01"], ["P01", "K05"]),
    ("K20", "virtual_production_super", "Virtual Production Supervisor", "விர்ச்சுவல் புரொடக்ஷன் மேற்பார்வையாளர்", "वर्चुअल प्रोडक्शन सुपरवाइजर", "K", "none", "ATL", ["production"], "In-camera VFX (ICVFX) using Unreal Engine and real-time LED volumes.", True, ["E01", "B01"], ["E01", "B01", "K21"]),
    ("K21", "brain_bar_operator", "Real-Time Engine / Brain Bar Operator", "பிரைன் பார் ஆபரேட்டர்", "ब्रेन बार ऑपरेटर", "K", "none", "BTL", ["production"], "Latency-free parallax shifting, LED panel sync and Unreal lighting.", False, ["K20"], ["K20", "E01"]),
    ("K22", "mocap_supervisor", "Motion / Performance Capture Supervisor", "மோஷன் கேப்சர் மேற்பார்வையாளர்", "मोशन कैप्चर सुपरवाइजर", "K", "none", "BTL", ["production"], "OptiTrack/Vicon marker arrays, zero-drift spatial calibrations.", False, ["K01"], ["K11", "K12"]),
    ("K23", "digital_human_specialist", "Digital Human / De-aging Specialist", "டிஜிட்டல் மனித உருவாக்க நிபுணர்", "डिजिटल मानव विशेषज्ञ", "K", "none", "ATL", ["post"], "Photorealistic face replacement and ethical likeness preservation.", True, ["B01", "N18"], ["N18", "K07"]),
    ("K24", "title_designer", "Motion Graphics / Title Designer", "டைட்டில் கிராபிக்ஸ் வடிவமைப்பாளர்", "शीर्षक डिज़ाइनर", "K", "none", "POST", ["post"], "Typography reveals, dynamic end credits crawl, 3D opening titles.", False, ["B01"], ["B01", "M02"]),
    ("K25", "large_format_conversion_super", "Stereo / HDR / Large-Format Conversion Supervisor", "ஐமேக்ஸ் மாற்று மேற்பார்வையாளர்", "इमैक्स रूपांतरण पर्यवेक्षक", "K", "none", "POST", ["post"], "IMAX DMR upscaling, Dolby Vision HDR metadata trim passes.", True, ["E01"], ["E01", "J08", "J19"]),

    # Band L
    ("L01", "distribution_head", "Distribution Head", "விநியோகத் தலைவர்", "वितरण प्रमुख", "L", "none", "ATL", ["distribution"], "Schedules release dates, territory sales, theatrical vs OTT windowing.", True, ["C01"], ["C01", "L02", "L05", "L08"]),
    ("L02", "territory_distributor", "Territory Distributor", "மண்டல விநியோகஸ்தர்", "क्षेत्रीय वितरक", "L", "none", "COMMERCIAL", ["distribution"], "Manages regional territories (e.g. Tamil Nadu, Nizam, Kerala, Overseas).", False, ["L01"], ["L01", "L16", "L20"]),
    ("L03", "acquisitions_exec", "Acquisitions Executive", "திரைப்பட கொள்முதல் நிர்வாகி", "अधिग्रहण कार्यकारी", "L", "none", "COMMERCIAL", ["development", "distribution"], "Screens incoming independent titles and negotiates negative rights.", False, ["L01"], ["L01", "N02"]),
    ("L04", "sales_agent", "International Sales Agent", "சர்வதேச விற்பனை முகவர்", "अंतर्राष्ट्रीय बिक्री एजेंट", "L", "none", "COMMERCIAL", ["distribution"], "Markets film territory-by-territory at Cannes, AFM, EFM.", False, ["L01"], ["L01", "C01"]),
    ("L05", "theatrical_booker", "Theatrical Booker / Cinema Programmer", "திரையரங்க முன்பதிவாளர்", "सिनेमा प्रोग्रामर", "L", "none", "COMMERCIAL", ["distribution"], "PVR, INOX, Cinépolis show programming and prime screen lockouts.", False, ["L01"], ["L01", "L16"]),
    ("L06", "windowing_analyst", "Release Strategist / Windowing Analyst", "வெளியீட்டு உத்தி ஆய்வாளர்", "विंडोइंग विश्लेषक", "L", "none", "COMMERCIAL", ["distribution"], "Optimizes Day-and-Date vs 4-week theatrical window before SVOD.", False, ["L01"], ["L01", "N15"]),
    ("L07", "tech_distribution_mgr", "Technical Distribution Manager", "தொழில்நுட்ப விநியோக மேலாளர்", "तकनीकी वितरण प्रबंधक", "L", "none", "COMMERCIAL", ["distribution"], "Satellite DCP multicasting, Qube/UFO network ingest, server keys.", True, ["L01"], ["J19", "L16"]),
    ("L08", "ott_acquisitions_mgr", "OTT Content Acquisition Manager", "ஓடிடி உள்ளடக்க கையகப்படுத்தல் மேலாளர்", "ओटीटी अधिग्रहण प्रबंधक", "L", "none", "COMMERCIAL", ["distribution"], "Originals and web series acquisition, exclusivity windows and platform KPIs.", True, ["C01"], ["C01", "L01", "N02"]),
    ("L09", "ott_programming_mgr", "OTT Programming / Scheduling Manager", "ஓடிடி அட்டவணை மேலாளர்", "ओटीटी शेड्यूलिंग प्रबंधक", "L", "none", "COMMERCIAL", ["distribution"], "Catalogue balance, drop timing, binge-watch drop cadences.", False, ["L08"], ["L08", "L11"]),
    ("L10", "ott_encoding_ops_mgr", "OTT Platform Ops / Encoding Manager", "ஓடிடி குறியாக்க மேலாளர்", "ओटीटी एन्कोडिंग प्रबंधक", "L", "none", "PLATFORM", ["distribution"], "Multi-bitrate HLS/DASH transcode ladders, AV1/HEVC packaging.", True, ["P01"], ["P01", "P04", "P05"]),
    ("L11", "metadata_artwork_mgr", "Metadata and Artwork Manager", "மெட்டாடேட்டா மற்றும் கலைப்படைப்பு மேலாளர்", "मेटाडेटा प्रबंधक", "L", "none", "COMMERCIAL", ["distribution"], "Dynamic poster thumbnails, localized title synopses and search tags.", False, ["L08"], ["M03", "L09"]),
    ("L12", "subscription_churn_analyst", "Subscription / Churn Analyst", "சந்தாதாரர் இழப்பு ஆய்வாளர்", "सब्सक्रिप्शन विश्लेषक", "L", "none", "COMMERCIAL", ["distribution"], "Viewer drop-off points, cohort retention and conversion tracking.", False, ["L08"], ["L08", "L13"]),
    ("L13", "recommendation_analyst", "Recommendation / Discovery Analyst", "பரிந்துரை அல்காரிதம் ஆய்வாளர்", "सिफारिश विश्लेषक", "L", "none", "COMMERCIAL", ["distribution"], "Algorithmic row placements and genre clustering for high engagement.", False, ["L08"], ["L08", "L12"]),
    ("L14", "avod_ad_sales_mgr", "AVOD / Ad Sales Manager", "விளம்பர விற்பனை மேலாளர்", "विज्ञापन बिक्री प्रबंधक", "L", "none", "COMMERCIAL", ["distribution"], "Dynamic ad insertion (DAI), programmatic ad fills during playback.", False, ["L08"], ["L08", "N15"]),
    ("L15", "digital_aggregator", "Digital Distribution Aggregator", "டிஜிட்டல் விநியோக ஒருங்கிணைப்பாளர்", "डिजिटल एग्रीगेटर", "L", "none", "COMMERCIAL", ["distribution"], "Apple TV, Google Play, Prime Video TVOD storefront ingestion.", False, ["L01"], ["L07", "J19"]),
    ("L16", "exhibitor_relations_mgr", "Exhibitor Relations Manager", "திரையரங்க உரிமையாளர் தொடர்பு மேலாளர்", "प्रदर्शक संबंध प्रबंधक", "L", "none", "COMMERCIAL", ["distribution"], "Box office share splits (50-40-30 model) and collection audits.", False, ["L01"], ["L01", "L02", "L20"]),
    ("L17", "satellite_rights_mgr", "Satellite / Television Rights Manager", "தொலைக்காட்சி உரிம மேலாளர்", "सैटेलाइट राइट्स प्रबंधक", "L", "none", "COMMERCIAL", ["distribution"], "Linear broadcast syndication, festive world premiere slot bidding.", False, ["L01"], ["L01", "N02"]),
    ("L18", "music_label_partner", "Music / Audio Rights Label Partner", "இசை லேபிள் கூட்டாளர்", "म्यूजिक लेबल पार्टनर", "L", "lyrics", "COMMERCIAL", ["distribution"], "Spotify/Apple Music streaming rights, album master advances.", False, ["C01"], ["C01", "G01", "N07"]),
    ("L19", "non_theatrical_sales_mgr", "Non-Theatrical Sales Manager", "திரையரங்கு சாரா விற்பனை மேலாளர்", "गैर-नाटकीय बिक्री प्रबंधक", "L", "none", "COMMERCIAL", ["distribution"], "Airline in-flight entertainment, cruise lines and campus licensing.", False, ["L01"], ["L01"]),
    # Addition
    ("L20", "single_screen_rep", "Single-Screen Exhibitor Representative", "ஒற்றைத் திரை அரங்கு பிரதிநிதி", "सिंगल स्क्रीन थिएटर प्रतिनिधि", "L", "none", "COMMERCIAL", ["distribution"], "Tier-2/3 single-screen ticket sales, local publicity and cash collections.", False, ["L16"], ["L16", "L02"]),

    # Band M
    ("M01", "marketing_director", "Marketing Director", "சந்தைப்படுத்தல் இயக்குநர்", "विपणन निर्देशक", "M", "none", "ATL", ["production", "distribution"], "Architect of overall promotional campaign, teasers, outdoor and ROI.", True, ["C01"], ["C01", "M02", "M07", "M08", "M12"]),
    ("M02", "publicity_designer", "Publicity Designer", "விளம்பர வடிவமைப்பாளர்", "प्रचार डिज़ाइनर", "M", "none", "ATL", ["prep", "production", "distribution"], "First look posters, font logos, title teaser banners (headline Indian role).", False, ["M01", "B01"], ["M01", "B01", "M03"]),
    ("M03", "key_art_designer", "Key Art Designer", "முதன்மைக் கலை வடிவமைப்பாளர்", "की आर्ट डिज़ाइनर", "M", "none", "BTL", ["distribution"], "High-resolution character posters, billboard hoardings and banners.", False, ["M02"], ["M02", "M01"]),
    ("M04", "creative_ad_lead", "Creative Advertising Lead (AV)", "விளம்பர படைப்புத் தலைவர்", "क्रिएटिव विज्ञापन प्रमुख", "M", "none", "BTL", ["post", "distribution"], "Teaser rhythm, dialogue punch lines for TV commercials and OTT bumpers.", False, ["M01"], ["M01", "M05"]),
    ("M05", "trailer_editor_mkt", "Trailer / Teaser Editor", "டிரெய்லர் எடிட்டர்", "ट्रेलर संपादक", "M", "none", "POST", ["post", "distribution"], "Cuts promotional cuts designed for viral anticipation.", False, ["M04"], ["M04", "J07"]),
    ("M06", "promo_content_producer", "Promo Content Producer", "விளம்பர உள்ளடக்க தயாரிப்பாளர்", "प्रोमो सामग्री निर्माता", "M", "none", "BTL", ["production", "distribution"], "Lyrical video songs, star interview bytes and making-of featurettes.", False, ["M01"], ["E22", "M01"]),
    ("M07", "media_buyer_planner", "Media Buyer / Planner", "ஊடக விளம்பர திட்டமிடுபவர்", "मीडिया खरीदार", "M", "none", "COMMERCIAL", ["distribution"], "Ad space bidding across TV channels, newspaper ads, bus shelters.", False, ["M01"], ["M01", "C12"]),
    ("M08", "publicity_director", "Publicity Director / Publicist", "செய்தித் தொடர்பாளர்", "प्रचारक", "M", "none", "ATL", ["distribution"], "Press conferences, newspaper feature articles, red carpet interviews.", False, ["M01"], ["M01", "M09", "M11"]),
    ("M09", "pro_officer", "P.R.O. (Public Relations Officer)", "மக்கள் தொடர்பு அதிகாரி (PRO)", "जनसंपर्क अधिकारी", "M", "none", "ATL", ["production", "distribution"], "Indian cinema press interface: film journalist management and releases.", False, ["M08", "C01"], ["M08", "C01", "M15"]),
    ("M10", "unit_publicist", "Unit Publicist", "யூனிட் விளம்பர அதிகாரி", "यूनिट प्रचारक", "M", "none", "BTL", ["production"], "Gathers set stories, star quotes and stills during physical shoot.", False, ["M08"], ["E21", "M08"]),
    ("M11", "press_junket_coord", "Press Junket Coordinator", "பத்திரிகையாளர் சந்திப்பு ஒருங்கிணைப்பாளர்", "प्रेस जंकट समन्वयक", "M", "none", "BTL", ["distribution"], "Round-table interviews, 1-on-1 star slots and media hospitality.", False, ["M08"], ["M08", "M09"]),
    ("M12", "digital_marketing_lead", "Digital Marketing Lead", "டிஜிட்டல் மார்க்கெட்டிங் தலைவர்", "डिजिटल मार्केटिंग लीड", "M", "none", "COMMERCIAL", ["distribution"], "Meta/Google ads optimization, YouTube algorithms, trending hashtag pushes.", False, ["M01"], ["M01", "M13", "M14"]),
    ("M13", "social_media_mgr", "Social Media Manager", "சமூக ஊடக மேலாளர்", "सोशल मीडिया प्रबंधक", "M", "none", "BTL", ["production", "distribution"], "Real-time Instagram Reels, X updates, fan polls, meme marketing.", False, ["M12"], ["M12", "M15"]),
    ("M14", "influencer_lead", "Influencer / Creator Partnerships Lead", "இன்ஃப்ளூயன்சர் கூட்டாண்மைத் தலைவர்", "इन्फ्लुएंसर लीड", "M", "none", "COMMERCIAL", ["distribution"], "Bookings of cinema YouTube reviewers, vloggers and TikTok creators.", False, ["M12"], ["M12"]),
    ("M15", "fan_club_coordinator", "Fan Club Coordinator", "ரசிகர் மன்ற ஒருங்கிணைப்பாளர்", "प्रशंसक क्लब समन्वयक", "M", "none", "ATL", ["distribution"], "South Indian organized fan clubs: 4 AM shows, giant cutouts, milk abhishekams.", False, ["C01", "M09"], ["C01", "M09", "L02", "L20"]),
    ("M16", "fan_persona_simulator", "Fan Persona (Audience Segment Simulator)", "ரசிகர் விருப்பப் பிரதிநிதி", "प्रशंसक व्यक्तित्व सिम्युलेटर", "M", "none", "ADVISORY", ["development", "post"], "Simulates reactions across demographic cohorts and star affinity bases.", False, ["M01"], ["M01", "O07"]),
    ("M17", "audience_research_analyst", "Audience Research / Test Screening Analyst", "பார்வையாளர் கருத்து ஆய்வாளர்", "दर्शक अनुसंधान विश्लेषक", "M", "none", "COMMERCIAL", ["post"], "Focus group test screening scorecards, second-by-second dial meters.", False, ["M01"], ["M01", "B01", "J03"]),
    ("M18", "brand_partnerships_lead", "Brand Partnerships / Product Placement Lead", "வணிக கூட்டாண்மைத் தலைவர்", "ब्रांड पार्टनरशिप लीड", "M", "none", "COMMERCIAL", ["prep", "production"], "In-film product placement, co-branded TVCs and retail tie-ups.", False, ["C01"], ["C01", "F12"]),
    ("M19", "merchandising_mgr", "Merchandising and Licensing Manager", "வியாபாரப் பொருட்கள் மேலாளர்", "मर्चेंडाइजिंग प्रबंधक", "M", "none", "COMMERCIAL", ["distribution"], "Action figures, comic books, T-shirts, NFT collectibles and games.", False, ["C01"], ["C01", "M01"]),
    ("M20", "audio_launch_event_prod", "Audio / Teaser / Trailer Launch Event Producer", "ஆடியோ வெளியீட்டு நிகழ்ச்சி தயாரிப்பாளர்", "ऑडियो लॉन्च इवेंट निर्माता", "M", "none", "ATL", ["distribution"], "Stadium events, star performances, live broadcast feeds and pyro shows.", True, ["C01"], ["C01", "M01", "G01", "M24"]),
    ("M21", "premiere_event_mgr", "Premiere and Festival Event Manager", "திரைப்பட விழா நிகழ்வு மேலாளர்", "प्रीमियर इवेंट मैनेजर", "M", "none", "BTL", ["distribution"], "Red carpet arrivals, VIP seating charts, delegate gifting and badges.", False, ["M01"], ["M01", "O09"]),
    ("M22", "regional_marketing_lead", "Regional Language Marketing Lead", "பிராந்திய மொழி சந்தைப்படுத்தல் தலைவர்", "क्षेत्रीय भाषा विपणन प्रमुख", "M", "none", "COMMERCIAL", ["distribution"], "Tailors cultural promo hooks per territory across Telugu, Hindi, Malayalam.", False, ["M01"], ["M01", "M12"]),
    ("M23", "crisis_comms_lead", "Crisis Communications Lead", "நெருக்கடி கால தகவல் தொடர்புத் தலைவர்", "संकट संचार प्रमुख", "M", "none", "COMMERCIAL", ["distribution"], "Controversy containment, boycott counter-messaging, leak triage.", True, ["C01"], ["C01", "M08", "N01"]),
    # Additions
    ("M24", "audio_launch_stage_director", "Audio Launch Stage Director", "ஆடியோ வெளியீட்டு மேடை இயக்குநர்", "स्टेज इवेंट निर्देशक", "M", "none", "ATL", ["distribution"], "Live stage cues, acoustic balance, teleprompters, star entry timing.", False, ["M20"], ["M20", "G01"]),
    ("M25", "poster_printer_banner_coord", "Poster Printer & Wall Banner Coordinator", "சுவரொட்டி மற்றும் பேனர் ஒருங்கிணைப்பாளர்", "पोस्टर और बैनर समन्वयक", "M", "none", "BTL", ["distribution"], "Offset printing of physical posters, gumming squads and highway hoardings.", False, ["M02"], ["M02", "L20"]),

    # Band N
    ("N01", "production_legal_counsel", "Production Legal Counsel", "தயாரிப்பு சட்ட ஆலோசகர்", "उत्पादन कानूनी सलाहकार", "N", "none", "ATL", ["development", "prep", "production", "post", "distribution"], "Master production contracts across talent, crew, guilds and insurance.", True, ["C01"], ["C01", "C04", "N02", "N04"]),
    ("N02", "business_affairs_exec", "Business Affairs Executive", "வணிக விவகார நிர்வாகி", "व्यापार मामलों के कार्यकारी", "N", "none", "COMMERCIAL", ["development", "distribution"], "Commercial terms, contingent compensation, profit definitions and deal memos.", False, ["N01"], ["N01", "C01", "L08"]),
    ("N03", "rights_clearance_mgr", "Rights and Clearances Manager", "உரிமங்கள் மற்றும் அனுமதிகள் மேலாளர்", "अधिकार और मंजूरी प्रबंधक", "N", "none", "COMMERCIAL", ["prep", "post"], "Clears background logos, brand trademarks, architectural rights, artwork.", True, ["N01"], ["N01", "F01", "F05"]),
    ("N04", "copyright_ip_counsel", "Copyright / IP Counsel", "பதிப்புரிமை சட்ட ஆலோசகர்", "कॉपीराइट वकील", "N", "none", "ATL", ["development", "distribution"], "Defends chain of title, copyright infringement suits and plagiarisms.", True, ["C01"], ["C01", "N01", "N05"]),
    ("N05", "script_registration_officer", "Script Registration Officer", "திரைக்கதை பதிவு அதிகாரி", "पटकथा पंजीकरण अधिकारी", "N", "none", "COMMERCIAL", ["development"], "Registers story, screenplay and dialogue with Writers Association & Copyright Office.", True, ["A01", "A02"], ["A01", "A02", "A03", "N04"]),
    ("N06", "title_trademark_specialist", "Title and Trademark Clearance Specialist", "தலைப்பு மற்றும் வர்த்தக முத்திரை நிபுணர்", "शीर्षक ट्रेडमार्क विशेषज्ञ", "N", "none", "COMMERCIAL", ["development"], "Title guild registration, trademark registry clash searches.", True, ["C01"], ["C01", "N04"]),
    ("N07", "music_rights_admin", "Music Rights Administrator", "இசை உரிம நிர்வாகி", "संगीत अधिकार प्रशासक", "N", "lyrics", "COMMERCIAL", ["post"], "Synchronisation licenses, IPRS/PPL filings and publishing splits.", False, ["N01"], ["G09", "G01", "N01"]),
    ("N08", "royalties_residuals_admin", "Royalties and Residuals Administrator", "ராயல்டி மற்றும் உபரி வருவாய் நிர்வாகி", "रॉयल्टी प्रशासक", "N", "none", "COMMERCIAL", ["distribution"], "Tracks downstream backend participations across OTT streams and broadcast.", False, ["C12"], ["C12", "N02"]),
    ("N09", "anti_piracy_lead", "Anti-Piracy / Content Protection Lead", "திருட்டு எதிர்ப்புப் பிரிவுத் தலைவர்", "विरोधी पायरेसी लीड", "N", "none", "COMMERCIAL", ["distribution"], "Telegram channel takedowns, torrent trackers and court John Doe injunctions.", True, ["L01"], ["L01", "N10", "P01"]),
    ("N10", "drm_watermarking_engineer", "DRM / Forensic Watermarking Engineer", "டிஜிட்டல் பாதுகாப்பு பொறியாளர்", "डीआरएम वाटरमार्किंग इंजीनियर", "N", "none", "PLATFORM", ["distribution"], "Injects imperceptible spatial audio/video watermarks in all screener copies.", True, ["P01"], ["N09", "J19", "P05"]),
    ("N11", "censor_liaison", "Certification / Censor Liaison", "தணிக்கைக் குழு தொடர்பு அதிகாரி", "सेंसर बोर्ड संपर्क", "N", "none", "ATL", ["post"], "CBFC/BBFC/MPAA classification submissions, voluntary cut negotiations.", True, ["B01", "C01"], ["B01", "C01", "N01"]),
    ("N12", "tax_incentive_analyst", "Tax Incentive and Subsidy Analyst", "வரிச் சலுகை மற்றும் மானிய ஆய்வாளர்", "कर प्रोत्साहन विश्लेषक", "N", "none", "COMMERCIAL", ["prep", "post"], "Maximizes state and overseas film rebates (e.g. UK/Abu Dhabi 30% cash rebate).", False, ["C04"], ["C04", "C12"]),
    ("N13", "film_financier", "Film Financier / Investor Relations", "திரைப்பட முதலீட்டாளர்", "फिल्म फाइनेंसर", "N", "none", "COMMERCIAL", ["development", "prep"], "Debt financing, minimum guarantees (MG), bridge loans and equity returns.", True, ["C02"], ["C02", "C01", "N14"]),
    ("N14", "bank_lender_rep", "Bank / Lender Representative", "வங்கி கடன் பிரதிநிதி", "बैंक ऋण प्रतिनिधि", "N", "none", "COMMERCIAL", ["prep", "production"], "Monitors drawdowns, escrow covenants and completion bond milestones.", True, ["C02"], ["C02", "C22", "N13"]),
    ("N15", "revenue_forecast_analyst", "Revenue and Profit Forecast Analyst", "வருவாய் மற்றும் லாப ஆய்வாளர்", "राजस्व पूर्वानुमान विश्लेषक", "N", "none", "COMMERCIAL", ["development", "distribution"], "P&L scenario models (Ott, satellite, music, overseas, theatrical).", False, ["C01"], ["C01", "C04", "L06"]),
    ("N16", "waterfall_recoupment_analyst", "Waterfall / Recoupment Analyst", "வருவாய் நீர்வீழ்ச்சி ஆய்வாளர்", "रिकूपमेंट विश्लेषक", "N", "none", "COMMERCIAL", ["distribution"], "Determines recovery priority: lenders first, bond fees, investors, profit share.", False, ["C02"], ["C02", "N13", "N15"]),
    ("N17", "data_protection_officer", "Data Protection Officer", "தரவு பாதுகாப்பு அதிகாரி", "डेटा संरक्षण अधिकारी", "N", "none", "PLATFORM", ["production", "distribution"], "Enforces GDPR and DPDP compliance across crew data and audition tapes.", True, ["P01"], ["P09", "P01"]),
    ("N18", "responsible_ai_officer", "Responsible AI and Consent Officer", "செயற்கை நுண்ணறிவு நெறிமுறை அதிகாரி", "जिम्मेदार एआई अधिकारी", "N", "none", "PLATFORM", ["prep", "post"], "Voice cloning consents, digital likeness releases, synthetic media governance.", True, ["C01"], ["K23", "N01", "P01"]),
    ("N19", "accessibility_compliance_lead", "Accessibility Compliance Lead", "அணுகல்தன்மை இணக்கத் தலைவர்", "सुलभता अनुपालन प्रमुख", "N", "none", "COMMERCIAL", ["post"], "Audio Description (AD) and Closed Caption (CC) regulatory compliance.", False, ["J16"], ["J16", "P15"]),

    # Band O
    ("O01", "trade_critic", "Trade Critic", "திரைப்பட வர்த்தக விமர்சகர்", "व्यापार समीक्षक", "O", "none", "RECEPTION", ["distribution"], "Industry reviews predicting theatrical shelf life and exhibitor profits.", False, ["L01"], ["L01", "O14"]),
    ("O02", "consumer_critic", "Consumer Press Critic", "பத்திரிகை விமர்சகர்", "उपभोक्ता प्रेस समीक्षक", "O", "none", "RECEPTION", ["distribution"], "Mainstream broadsheet reviews shaping opening weekend turnout.", False, ["M01"], ["M01"]),
    ("O03", "regional_critic", "Regional Language Critic", "பிராந்திய மொழி விமர்சகர்", "क्षेत्रीय समीक्षक", "O", "none", "RECEPTION", ["distribution"], "Regional sensibility evaluation across local vernacular outlets.", False, ["M01"], ["M22"]),
    ("O04", "aggregator_analyst", "Aggregator Score Analyst", "விமர்சன மதிப்பீட்டு ஆய்வாளர்", "एग्रीगेटर स्कोर विश्लेषक", "O", "none", "RECEPTION", ["distribution"], "Models Rotten Tomatoes / Metacritic percentage thresholds and buzz.", False, ["M01"], ["M01", "O05"]),
    ("O05", "user_rating_analyst", "User Rating Analyst", "பயனர் மதிப்பீட்டு ஆய்வாளர்", "उपयोगकर्ता रेटिंग विश्लेषक", "O", "none", "RECEPTION", ["distribution"], "IMDb score trajectories and bot brigade / review-bombing detection.", False, ["M01"], ["M12", "O07"]),
    ("O06", "exit_poll_analyst", "Exit Poll Analyst", "வெளியேறும் பார்வையாளர் ஆய்வாளர்", "एग्जिट पोल विश्लेषक", "O", "none", "RECEPTION", ["distribution"], "First day first show (FDFS) CinemaScore letter grades and WOM speed.", False, ["L01"], ["L01", "M01"]),
    ("O07", "social_sentiment_analyst", "Social Sentiment Analyst", "சமூக உணர்வு ஆய்வாளர்", "सामाजिक भावना विश्लेषक", "O", "none", "RECEPTION", ["distribution"], "Real-time multilingual sentiment NLP across X, Reddit and YouTube comments.", False, ["M12"], ["M12", "M13"]),
    ("O08", "youtube_reviewer", "YouTube / Podcast Reviewer", "யூடியூப் திரைப்பட விமர்சகர்", "यूट्यूब समीक्षक", "O", "none", "RECEPTION", ["distribution"], "Video essay breakdowns that now heavily shift youth and family ticket sales.", False, ["M14"], ["M14"]),
    ("O09", "festival_programmer", "Festival Programmer", "திரைப்பட விழா தேர்வுக்குழு உறுப்பினர்", "महोत्सव प्रोग्रामर", "O", "none", "RECEPTION", ["post", "distribution"], "Curates world competition slots at Cannes, Venice, Toronto and Sundance.", True, ["B01"], ["B01", "C01", "O10"]),
    ("O10", "festival_artistic_director", "Festival Artistic Director", "திரைப்பட விழா கலை இயக்குநர்", "महोत्सव कलात्मक निर्देशक", "O", "none", "RECEPTION", ["distribution"], "Awards Palme d'Or / Golden Lion; defines international auteur prestige.", False, ["O09"], ["O09"]),
    ("O11", "festival_submissions_coord", "Festival Submissions Coordinator", "திரைப்பட விழா சமர்ப்பிப்பு ஒருங்கிணைப்பாளர்", "प्रस्तुतियाँ समन्वयक", "O", "none", "BTL", ["distribution"], "Technical format compliance, screener links, premiere status verification.", False, ["O09"], ["O09", "J19"]),
    ("O12", "awards_campaign_strategist", "Awards Campaign Strategist", "விருதுப் பிரச்சார உத்தியாளர்", "पुरस्कार अभियान रणनीतिकार", "O", "none", "ATL", ["distribution"], "Oscars / National Film Awards For-Your-Consideration (FYC) campaigns.", False, ["C01"], ["C01", "M01", "O13"]),
    ("O13", "voter_simulator", "Jury / Voter Persona Simulator", "நடுவர் மன்ற பிரதிநிதி", "जूरी व्यक्तित्व सिम्युलेटर", "O", "none", "ADVISORY", ["distribution"], "Simulates Academy / BAFTA / National Award voting member preferences.", False, ["O12"], ["O12"]),
    ("O14", "box_office_tracker", "Box Office Analyst / Tracker", "பாக்ஸ் ஆபீஸ் ஆய்வாளர்", "बॉक्स ऑफिस ट्रैकर", "O", "none", "COMMERCIAL", ["distribution"], "Advance booking trends, seat occupancy percentages and lifetime gross.", False, ["L01"], ["L01", "C01"]),
    ("O15", "trade_journalist", "Trade Journalist", "திரைப்பட வர்த்தக பத்திரிகையாளர்", "व्यापार पत्रकार", "O", "none", "RECEPTION", ["distribution"], "Reports opening day records, territory sales disputes and OTT bidding wars.", False, ["M09"], ["M09", "O01"]),
    ("O16", "film_archivist", "Archivist / Preservationist", "திரைப்பட ஆவணக் காப்பாளர்", "फिल्म पुरालेखपाल", "O", "none", "POST", ["post"], "4K film scan negative restoration, temperature-controlled vault custody.", False, ["J01"], ["J01", "J19"]),

    # Band P
    ("P01", "studio_reliability_engineer", "Studio Reliability Engineer (SRE)", "ஸ்டுடியோ நம்பகத்தன்மை பொறியாளர்", "स्टूडियो विश्वसनीयता इंजीनियर", "P", "none", "PLATFORM", ["development", "prep", "production", "post", "distribution"], "SLO guardian: latency, rendering, pipeline uptime and automated failovers.", True, [], ["P02", "P08", "P09", "P10"]),
    ("P02", "pipeline_observability_dir", "Pipeline Observability Director", "பைப்லைன் கண்காணிப்பு இயக்குநர்", "पाइपलाइन वेधशाला निदेशक", "P", "none", "PLATFORM", ["production", "post", "distribution"], "Root orchestrator; investigates alerts and telemetry through Grafana MCP.", True, ["P01"], ["P01", "P10", "P11"]),
    ("P03", "render_farm_capacity_planner", "Render Farm Capacity Planner", "ரெண்டர் ஃபார்ம் திறன் திட்டமிடுபவர்", "क्षमता योजनाकार", "P", "none", "PLATFORM", ["post"], "Optimizes GPU spot instances, queuing bottlenecks and compute cost per frame.", False, ["P01"], ["K18", "P08"]),
    ("P04", "encoding_ops_engineer", "Encoding / Transcode Ops Engineer", "குறியாக்க செயல்பாட்டுப் பொறியாளர்", "एन्कोडिंग इंजीनियर", "P", "none", "PLATFORM", ["distribution"], "Tolerates transcode failures, profile mismatches and HDR color shifts.", False, ["P01"], ["L10", "P05"]),
    ("P05", "cdn_playback_qoe_engineer", "CDN / Playback QoE Engineer", "சிடிஎன் பின்னணி தரப் பொறியாளர்", "सीडीएन क्यूओई इंजीनियर", "P", "none", "PLATFORM", ["distribution"], "Monitors edge cache hit ratio, rebuffer events and startup latency.", False, ["P01"], ["L10", "N10"]),
    ("P06", "onset_capture_engineer", "On-Set Capture Systems Engineer", "செட் படப்பிடிப்பு முறைமைப் பொறியாளர்", "सिस्टम इंजीनियर", "P", "none", "PLATFORM", ["production"], "Offload reliability, NVMe raid arrays, high-speed on-set networking.", False, ["P01"], ["E11", "P07"]),
    ("P07", "mam_engineer", "Media Asset Management Engineer", "ஊடக சொத்து மேலாண்மைப் பொறியாளர்", "मीडिया संपत्ति इंजीनियर", "P", "none", "PLATFORM", ["production", "post"], "Preserves file naming schemas, metadata tags and checksum lineages.", False, ["P01"], ["P06", "J06"]),
    ("P08", "finops_cost_governor", "FinOps / Cost Governor", "நிதி செயல்பாட்டுச் செலவு கட்டுப்பாட்டாளர்", "लागत नियंत्रक", "P", "none", "PLATFORM", ["development", "prep", "production", "post", "distribution"], "Limits token burn, GPU instances and cloud egress under strict budget caps.", True, ["P01"], ["P01", "C04", "P03"]),
    ("P09", "security_engineer", "Security Engineer", "பாதுகாப்புப் பொறியாளர்", "सुरक्षा इंजीनियर", "P", "none", "PLATFORM", ["development", "prep", "production", "post", "distribution"], "VPC Service Controls, Cloud KMS customer encryption keys, IAM least privilege.", True, ["P01"], ["P01", "N17"]),
    ("P10", "incident_commander", "Incident Commander", "நிகழ்வுத் தளபதி (இன்சிடென்ட் கமாண்டர்)", "घटना कमांडर", "P", "none", "PLATFORM", ["development", "prep", "production", "post", "distribution"], "Declares, coordinates and closes high-severity operational incidents.", True, ["P01"], ["P01", "P02", "B01", "C01"]),
    ("P11", "ai_observability_analyst", "AI Observability Analyst", "செயற்கை நுண்ணறிவு கண்காணிப்பாளர்", "एआई वेधशाला विश्लेषक", "P", "none", "PLATFORM", ["development", "prep", "production", "post", "distribution"], "Agent tracing, hallucination detection, tool call latencies via Grafana.", False, ["P02"], ["P02", "P12"]),
    ("P12", "evaluation_engineer", "Evaluation Engineer", "மதிப்பீட்டுப் பொறியாளர்", "मूल्यांकन इंजीनियर", "P", "none", "PLATFORM", ["development", "post"], "Curates golden datasets and executes regression rubrics for agents.", False, ["P11"], ["P11", "P01"]),
    ("P13", "data_steward", "Data Steward", "தரவுப் பொறுப்பாளர்", "डेटा प्रबंधक", "P", "none", "PLATFORM", ["development", "prep", "production", "post", "distribution"], "Schema enforcement, data residency and retention lifecycles in BigQuery.", False, ["P01"], ["P01", "N17"]),
    ("P14", "localization_engineer", "Localization Engineer", "சர்வதேசமயமாக்கல் பொறியாளர்", "स्थानीयकरण इंजीनियर", "P", "none", "PLATFORM", ["distribution"], "UTF-8 typography, bidirectional text (RTL/LTR) layout plumbing.", False, ["P01"], ["J17", "P15"]),
    ("P15", "accessibility_engineer", "Accessibility Engineer", "அணுகல்தன்மை பொறியாளர்", "सुलभता इंजीनियर", "P", "none", "PLATFORM", ["distribution"], "WCAG 2.2 AAA accessibility, screen reader conformance in frontend.", False, ["P01"], ["N19", "P14"]),

    # Band Q
    ("Q01", "comedy_advisor", "Comedy Advisor", "நகைச்சுவை ஆலோசகர்", "कॉमेडी सलाहकार", "Q", "dialogue", "ADVISORY", ["development"], "Humour timing, regional puns, comic misdirection.", False, ["B01"], ["A03", "D03"]),
    ("Q02", "dark_comedy_advisor", "Dark Comedy Advisor", "டார்க் காமெடி ஆலோசகர்", "डार्क कॉमेडी सलाहकार", "Q", "dialogue", "ADVISORY", ["development"], "Tonal calibration between macabre themes and punchline acceptability.", False, ["B01"], ["A03"]),
    ("Q03", "drama_advisor", "Drama Advisor", "நாடக ஆலோசகர்", "नाटक सलाहकार", "Q", "story", "ADVISORY", ["development"], "Emotional catharsis, interpersonal stakes and character depth.", False, ["B01"], ["A01", "A02"]),
    ("Q04", "horror_advisor", "Horror Advisor", "திகில் ஆலோசகர்", "हॉरर सलाहकार", "Q", "none", "ADVISORY", ["development", "post"], "Jump scare cadence, atmospheric dread, uncanny tension building.", False, ["B01"], ["A02", "G17"]),
    ("Q05", "thriller_advisor", "Thriller / Suspense Advisor", "த்ரில்லர் ஆலோசகர்", "थ्रिलर सलाहकार", "Q", "screenplay", "ADVISORY", ["development"], "Information withholding, red herrings, ticking-clock pacing.", False, ["B01"], ["A02", "J03"]),
    ("Q06", "action_advisor", "Action Advisor", "ஆக்ஷன் ஆலோசகர்", "एक्शन सलाहकार", "Q", "none", "ADVISORY", ["prep", "production"], "Set-piece escalation, kinetic momentum, physical stakes.", False, ["B01"], ["H01", "E01"]),
    ("Q07", "fantasy_advisor", "Fantasy Advisor", "பேண்டஸி ஆலோசகர்", "काल्पनिक सलाहकार", "Q", "story", "ADVISORY", ["development"], "Magic systems, realm internal logic, legendary artifact rules.", False, ["B01"], ["A01", "F01"]),
    ("Q08", "dark_fantasy_advisor", "Dark Fantasy Advisor", "டார்க் பேண்டஸி ஆலோசகர்", "डार्क फैंटेसी सलाहकार", "Q", "none", "ADVISORY", ["development"], "Grimdark world rules, moral ambiguity, gothic visual lore.", False, ["B01"], ["A01", "F01"]),
    ("Q09", "mythology_epic_advisor", "Mythology / Epic Advisor", "இதிகாச ஆலோசகர்", "पौराणिक महाकाव्य सलाहकार", "Q", "story", "ADVISORY", ["development"], "Scale staging, cosmic battles, devotional nuances, grand acts.", False, ["B01"], ["A01", "I19"]),
    ("Q10", "sci_fi_advisor", "Science Fiction Advisor", "அறிவியல் புனைகதை ஆலோசகர்", "विज्ञान कथा सलाहकार", "Q", "story", "ADVISORY", ["development"], "Hard vs soft sci-fi extrapolation, speculative ethics.", False, ["B01"], ["A01", "I07", "K01"]),
    ("Q11", "romance_advisor", "Romance Advisor", "காதல் கதை ஆலோசகர்", "रोमांस सलाहकार", "Q", "story", "ADVISORY", ["development"], "Emotional chemistry, romantic tension, longing and climax.", False, ["B01"], ["A01", "D01"]),
    ("Q12", "musical_advisor", "Musical / Song-Driven Advisor", "இசைப் பட ஆலோசகர்", "संगीतमय सलाहकार", "Q", "lyrics", "ADVISORY", ["development", "prep"], "Song-to-narrative integration, emotional justification for musical breaks.", False, ["B01"], ["G01", "G18", "A10"]),
    ("Q13", "biopic_advisor", "Biopic / Docudrama Advisor", "சுயசரிதை ஆலோசகர்", "बायोपिक सलाहकार", "Q", "none", "ADVISORY", ["development"], "Factual fidelity, living subject defamation guard, archival parallels.", False, ["B01"], ["A01", "N01"]),
    ("Q14", "documentary_advisor", "Documentary Advisor", "ஆவணப்பட ஆலோசகர்", "वृत्तचित्र सलाहकार", "Q", "none", "ADVISORY", ["development", "post"], "Subject ethics, journalistic integrity, archival rights verification.", False, ["B01"], ["A01", "N03"]),
    ("Q15", "animation_advisor", "Animation Advisor", "இயங்குபட ஆலோசகர்", "एनिमेशन सलाहकार", "Q", "none", "ADVISORY", ["development", "prep"], "Squash and stretch, caricature clarity, stylized framing rules.", False, ["B01"], ["K12", "A15"]),
    ("Q16", "episodic_advisor", "Web Series / Episodic Advisor", "வெப் சீரிஸ் ஆலோசகர்", "एपिसोडिक सलाहकार", "Q", "screenplay", "ADVISORY", ["development"], "Multi-season arcs, cliffhangers, episodic A/B/C plot distribution.", False, ["A09"], ["A09", "A08"]),
    ("Q17", "anthology_advisor", "Anthology Advisor", "ஆந்தாலஜி ஆலோசகர்", "एंथोलॉजी सलाहकार", "Q", "story", "ADVISORY", ["development"], "Theme consistency across disparate short films and transitional motifs.", False, ["B01"], ["A01", "C01"]),
    ("Q18", "auteur_advisor", "Experimental / Auteur Advisor", "ஆர்ட் சினிமா ஆலோசகர்", "ऑट्योर सलाहकार", "Q", "none", "ADVISORY", ["development", "post"], "Elliptical storytelling, poetic realism, European festival readiness.", False, ["B01"], ["B01", "O09"]),
    ("Q19", "regional_cinema_advisor", "Regional Cinema Advisor", "பிராந்திய சினிமா ஆலோசகர்", "क्षेत्रीय सिनेमा सलाहकार", "Q", "none", "ADVISORY", ["development", "distribution"], "Navigates cultural vernacular of Malayalam, Kannada, Marathi nuances.", False, ["B01"], ["A01", "L02"]),
    ("Q20", "micro_budget_advisor", "Micro-Budget Advisor", "குறைந்த பட்ஜெட் ஆலோசகர்", "माइक्रो-बजट सलाहकार", "Q", "none", "ADVISORY", ["prep", "production"], "Extreme guerrilla constraint optimization: single-location ingenuity.", False, ["C04"], ["C04", "B01"]),
    ("Q21", "mid_budget_advisor", "Mid-Budget Advisor", "நடுத்தர பட்ஜெட் ஆலோசகர்", "मध्यम बजट सलाहकार", "Q", "none", "ADVISORY", ["prep", "distribution"], "Balancing star cost with theatrical recovery in the hardest economic band.", False, ["C01"], ["C01", "C04", "L06"]),
    ("Q22", "tentpole_franchise_advisor", "Tentpole / Franchise Advisor", "பிரம்மாண்ட ஃபிரான்சைஸ் ஆலோசகர்", "टेंटपोल फ्रैंचाइज़ सलाहकार", "Q", "none", "ADVISORY", ["development"], "Cinematic universe continuity, sequel hooks and merchandising breadth.", False, ["C01"], ["C01", "A01", "M19"]),
    ("Q23", "remake_adaptation_advisor", "Remake / Adaptation Advisor", "மறுஉருவாக்க ஆலோசகர்", "रीमेक सलाहकार", "Q", "screenplay", "ADVISORY", ["development"], "Transposing foreign hit beats to native cultural sensibilities.", False, ["B01"], ["A02", "A05", "N03"]),
    ("Q24", "pan_india_release_advisor", "Pan-India / Multi-Language Release Advisor", "பான்-இந்தியா வெளியீட்டு ஆலோசகர்", "अखिल भारतीय रिलीज सलाहकार", "Q", "none", "ADVISORY", ["development", "distribution"], "Simultaneous 5-language launch strategy, cross-state star appeal.", False, ["C01"], ["C01", "L01", "M01", "M22"]),

    # Cross-Band Composites
    ("COMP01", "continuity_guardian", "Continuity Guardian", "தொடர்ச்சிப் பாதுகாவலர்", "निरंतरता संरक्षक", "COMP", "none", "PLATFORM", ["production", "post"], "Multi-agent composite fusing Script Supervisor + Assistant Editor + VFX Editor.", True, ["B01"], ["B11", "J06", "K04"]),
    ("COMP02", "budget_reality_checker", "Budget Reality Checker", "பட்ஜெட் உண்மை சரிபார்ப்பாளர்", "बजट वास्तविकता परीक्षक", "COMP", "none", "PLATFORM", ["prep", "post"], "Fuses Line Producer + VFX Producer + Render Farm Capacity Planner.", True, ["C01"], ["C04", "K02", "P03"]),
    ("COMP03", "sensory_immersion_architect", "Sensory Immersion Architect", "உணர்வு ஆழமை வடிவமைப்பாளர்", "संवेदी विसर्जन वास्तुकार", "COMP", "none", "PLATFORM", ["post"], "Fuses Cinematographer + Sound Designer + Colorist for synesthetic harmony.", False, ["B01"], ["E01", "G17", "J08"]),
    ("COMP04", "cultural_authenticity_anchor", "Cultural Authenticity Anchor", "கலாச்சார உண்மைத்தன்மை நங்கூரம்", "सांस्कृतिक प्रामाणिकता एंकर", "COMP", "none", "PLATFORM", ["development", "prep"], "Fuses Dialogue Writer + Dialect Advisor + Anthropology Advisor.", False, ["B01"], ["A03", "I24", "I25"]),
    ("COMP05", "stunt_safety_governor", "Stunt Safety Governor", "சாகச பாதுகாப்பு ஆளுநர்", "स्टंट सुरक्षा गवर्नर", "COMP", "none", "PLATFORM", ["production"], "Fuses Fight Master + Set Medic + Completion Guarantor with unyielding veto.", True, ["C01"], ["H01", "C21", "C22"]),
    ("COMP06", "viral_trailer_pulse", "Viral Trailer Pulse", "வைரல் டிரெய்லர் துடிப்பு", "वायरल ट्रेलर पल्स", "COMP", "none", "PLATFORM", ["post", "distribution"], "Fuses Trailer Editor + Social Media Manager + Creative Advertising Lead.", False, ["M01"], ["J07", "M13", "M04"]),
    ("COMP07", "box_office_recovery_engine", "Box Office Recovery Engine", "வசூல் மீட்பு இயந்திரம்", "बॉक्स ऑफिस रिकवरी इंजन", "COMP", "none", "PLATFORM", ["distribution"], "Fuses Windowing Analyst + Revenue Forecast Analyst + Exhibitor Relations.", False, ["C01"], ["L06", "N15", "L16"]),
    ("COMP08", "synthetic_likeness_guardian", "Synthetic Likeness Guardian", "டிஜிட்டல் உருவப் பாதுகாவலர்", "सिंथेटिक समानता संरक्षक", "COMP", "none", "PLATFORM", ["prep", "post"], "Fuses Digital Human Specialist + Responsible AI Officer + Production Counsel.", True, ["C01"], ["K23", "N18", "N01"]),

    # Adversarial Red-Team Antagonists
    ("ANTG01", "schedule_breaker", "Schedule Breaker", "கால அட்டவணை உடைப்பாளர்", "शेड्यूल ब्रेकर", "ANTG", "none", "PLATFORM", ["prep", "production"], "Attacks shoot schedules with monsoon delays, star illness and visa blocks.", False, ["B07"], ["B07", "C04"]),
    ("ANTG02", "copyright_attacker", "Copyright Attacker", "பதிப்புரிமை தாக்குதல் முகவர்", "कॉपीराइट हमलावर", "ANTG", "none", "PLATFORM", ["development", "prep", "post"], "Attacks script, tunes and visuals for accidental plagiarism or infringement.", True, ["N04"], ["N04", "N01"]),
    ("ANTG03", "sceptical_critic", "Sceptical Critic", "சந்தேகவாத விமர்சகர்", "संदेहास्पद आलोचक", "ANTG", "none", "PLATFORM", ["development", "post"], "Ruthlessly attacks plot holes, emotional falsity and second-half pacing sag.", False, ["B01"], ["A01", "A02", "B01"]),
    ("ANTG04", "piracy_simulator", "Piracy Simulator", "திருட்டு வலைப்பின்னல் உருவகப்படுத்தி", "पायरेसी सिम्युलेटर", "ANTG", "none", "PLATFORM", ["post", "distribution"], "Simulates screener leaks, cam-rip distribution and watermark stripping attacks.", True, ["N09"], ["N09", "N10", "P01"]),
    ("ANTG05", "worst_case_weather_agent", "Worst-Case Weather Agent", "மோசமான வானிலை முகவர்", "खराब मौसम एजेंट", "ANTG", "none", "PLATFORM", ["prep", "production"], "Simulates extreme weather shifts, lighting ruin and outdoor equipment hazards.", False, ["B07"], ["B07", "C16", "E01"])
]

def build_persona_dict(item):
    p_id, slug, name_en, name_ta, name_hi, band, credit_elem, budget_line, phase_scope, mandate, can_block, escalates_to, collabs = item
    meta = BANDS_METADATA.get(band, BANDS_METADATA["P"])
    
    # Tool allow/deny lists
    allowed_tools = [
        "script.read_scene",
        "sme.request_review",
        "grafana.query_metrics"
    ]
    if can_block:
        allowed_tools.append("governance.raise_blocking_veto")
    if band in ["E", "J", "K"]:
        allowed_tools.extend(["studio.inspect_media", "telemetry.check_pipeline"])
    if band in ["C", "N", "L"]:
        allowed_tools.extend(["finance.audit_spend", "contracts.verify_rights"])
    if band == "I":
        allowed_tools.append("sme.emit_advisory_checklist")
    if band == "ANTG":
        allowed_tools.append("adversarial.inject_stress_vector")
        
    denied_tools = []
    if not can_block and budget_line != "ATL":
        denied_tools.append("finance.approve_spend")
    if band in ["N", "P"] and "strict" in mandate:
        denied_tools.append("studio.export_raw_dailies")

    return {
        "id": p_id,
        "slug": slug,
        "display_name": {
            "en": name_en,
            "ta": name_ta,
            "hi": name_hi
        },
        "band": band,
        "band_name": meta["name"],
        "credit_element": credit_elem,
        "budget_line": budget_line,
        "phase_scope": phase_scope,
        "mandate": mandate,
        "authority": {
            "can_block": can_block,
            "escalates_to": escalates_to
        },
        "collaborates_with": collabs,
        "tools_allowed": allowed_tools,
        "tools_denied": denied_tools,
        "grafana_signals": {
            "metrics": meta["default_metrics"],
            "logs": [f'{{app="thirai-kuzhu-ai", band="{band}"}} |= "{slug}"'],
            "traces": [f"trace_{slug}"],
            "dashboards": meta["dashboards"]
        },
        "model_tier": meta["model_tier"],
        "concurrency_class": meta["concurrency"],
        "context_cache_key": f"persona:{p_id}:v{{version}}",
        "token_budget_per_run": meta["token_budget"],
        "languages": ["en", "ta", "hi", "te", "ml", "ja", "fr"],
        "narrative_voice": "professional, cinematic, precise, domain-grounded",
        "sme_dependencies": ["I24", "I17"] if band in ["A", "B"] else []
    }

def main():
    print(f"Generating comprehensive Persona Registry: {len(RAW_PERSONAS)} personas...")
    registry_list = [build_persona_dict(p) for p in RAW_PERSONAS]
    registry_data = {
        "version": "1.0.0",
        "system": "Thirai Kuzhu AI - Complete Screen Crew Persona Registry",
        "total_personas": len(registry_list),
        "bands_count": len(BANDS_METADATA),
        "personas": registry_list
    }
    
    # Save to backend/src/personas/registry.yaml and registry.json
    backend_yaml = BACKEND_PERSONAS_DIR / "registry.yaml"
    backend_json = BACKEND_PERSONAS_DIR / "registry.json"
    
    yaml_content = dump_clean_yaml(registry_data)
    with open(backend_yaml, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    with open(backend_json, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {backend_yaml} ({backend_yaml.stat().st_size} bytes)")
    print(f"Wrote {backend_json} ({backend_json.stat().st_size} bytes)")
    
    # Save copy to root personas/
    root_yaml = ROOT_PERSONAS_DIR / "registry.yaml"
    root_json = ROOT_PERSONAS_DIR / "registry.json"
    with open(root_yaml, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    with open(root_json, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {root_yaml} ({root_yaml.stat().st_size} bytes)")
    print(f"Wrote {root_json} ({root_json.stat().st_size} bytes)")
    
    # Also save a copy in frontend/src/constants/registry.json for instant offline client loading!
    frontend_json = ROOT_DIR / "frontend" / "src" / "constants" / "registry.json"
    with open(frontend_json, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {frontend_json} ({frontend_json.stat().st_size} bytes)")
    
    print("Persona Registry build successful!")

if __name__ == "__main__":
    main()
