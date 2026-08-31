# ইশারায় শিক্ষা (Ishara-e-Shikkha)
### Education Through Signs

**Track:** A — Education (EdTech)
**Event:** RoboFest Bangladesh 2026, BuildAthon Competition
**Team size:** 3

## Problem
Deaf and hard-of-hearing students in mainstream Bangladeshi classrooms lack
real-time access to spoken lessons. Existing solutions (live captioning apps)
require students to split attention between the teacher and a separate screen,
increasing cognitive load. Bangla Sign Language (BdSL) tooling for education
is also nearly nonexistent compared to spoken-language captioning tools.

## Solution
ইশারায় শিক্ষা listens to a teacher's spoken lesson (Bangla), converts speech
to simplified text matched against a fixed classroom vocabulary, and plays
back corresponding Bangla Sign Language video clips in sequence — displayed
near the teacher (laptop/tablet), so students don't have to look away.

Scope is deliberately fixed to one curriculum unit (Class 6 Science —
"Our Solar System") and a fixed vocabulary (~80-100 words), rather than
attempting general-purpose sign language translation.

## Pipeline
1. Mic audio → Whisper (Bangla ASR)
2. Transcribed text → simplification + fixed-vocabulary matching
3. Matched words → sign video clip queue (WebSocket push to frontend)
4. Display: simplified captions + sign video playback, side by side

## Tech Stack
- **Backend:** Python, FastAPI, WebSocket, OpenAI Whisper
- **Frontend:** Plain HTML/CSS/JS (no framework) — video element + caption
  panel, kept simple by design for reliability during live demo
- **Matching:** rule-based tokenization + hand-written synonym map against
  a fixed vocabulary CSV — no ML required for this step

## Deployment Model
Two-tier by design:
- **Cloud/primary (demo):** larger Whisper model, laptop-hosted, used for
  the live pitch demo — prioritizes accuracy.
- **Lite/offline (concept, scalability story):** smaller local Whisper
  model intended for low-connectivity/phone deployment — proof-of-concept
  only within this build window, documented as the deployment roadmap for
  real-world scale-up.

## Data Sources
- Sign video clips: Ishaara.ai (used with permission — data source only,
  not a project partner)
- Sign video clips: BdSLW401 / BdSLW60 academic datasets (cite paper)
- ASR: OpenAI Whisper (open-source, disclosed)
- No self-recorded sign clips — vocabulary is scoped to what these two
  sources actually cover (see vocab.csv for per-word source tracking)

## Core Pillars
- **Sustainability:** rule-based matching (no extra model training/inference
  beyond ASR); lite-mode roadmap targets low-power/offline deployment.
- **Feasibility:** fixed vocabulary + curriculum scope + reliance on existing
  open/permitted datasets rather than building new ones from scratch.
- **Scalability:** vocabulary/clip library is modular (CSV + clip folder) —
  new units or subjects can be added without retraining any model; cloud/lite
  split shows a clear path to handling more users and lower-end devices.

## Team & Roles
- Person A — ASR pipeline, backend (FastAPI, WebSocket), word matching
- Person B — Frontend (HTML/CSS/JS), video sequencer, UI
- Person C — Vocabulary coverage, clip sourcing/tagging, docs, demo video

## Disclosure
- Ishaara.ai sign clips used with explicit permission (data source only)
- BdSLW401 / BdSLW60 datasets cited per academic license
- OpenAI Whisper used as pre-existing open-source ASR

## Status
🚧 In progress — BuildAthon Competition, 5-day build window
