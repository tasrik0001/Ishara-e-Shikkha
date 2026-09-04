# Ishara-e-Shikkha — Project Summary & Current State

## Project Idea

**Ishara-e-Shikkha (ইশারায় শিক্ষা)** is a real-time classroom/lecture translation tool for
deaf students in Bangladesh. It listens to a teacher's spoken Bangla, transcribes it, matches
the transcribed words against a known vocabulary of Bangla Sign Language (BdSL) signs, and
plays back the corresponding sign clips — so a deaf student can follow a live lecture through
sign language instead of only text or lip-reading.

The scope is deliberately narrowed to a a single chapter rather than
general-purpose translation, since BdSL sign data is scarce and a closed vocabulary is far
more achievable in a short build window.

### Core problems being solved
1. **Data scarcity** — sourcing enough sign data for the target vocabulary.
2. **Word segmentation** — correctly breaking down complex/compound Bangla words
   (e.g. আমগাছ → আম + গাছ) and case-suffixed words (e.g. গাছের → গাছ + এর) so they map
   onto the fixed vocabulary correctly.
3. **Real-time performance** — doing all of the above from live speech.

---

## Current State of the Repo

Very early stage — **6 commits total**, no description/topics set, 0 stars/forks
(expected for a fresh hackathon repo).

### Repo structure
| Path | Status |
|---|---|
| `src/` | Source code folder — exists |
| `data/` | Data folder — exists, presumably for datasets/vocabulary |
| `words.csv` | **Header row only** (`id`, `bangla_word`) — no data rows populated yet |
| `PROJECT.md`, `README.md` | Present *(excluded from this summary per instruction)* |
| `.python-version`, `pyproject.toml`, `uv.lock` | Standard Python project config |

**Bottom line:** scaffolding is in place, but the vocabulary CSV is empty and no
implementation logic has been reviewed beyond folder structure.

---

## Infra / Stack (pulled directly from `pyproject.toml`)

| Component | Detail |
|---|---|
| **Language** | Python `>=3.14` |
| **Package manager / build backend** | `uv` (via `uv_build`), with `uv.lock` for locked dependencies |
| **Backend framework** | FastAPI (`fastapi>=0.141.1`) + `uvicorn[standard]>=0.52.4` as ASGI server |
| **Speech-to-text** | `openai-whisper>=20250625` |
| **Data handling** | `pandas>=3.0.5` (likely vocabulary/words.csv matching logic) |
| **Web/scraping utility** | `beautifulsoup4>=4.15.0` + `requests>=2.34.2` (likely data-sourcing/scraping step) |
| **TLS/certs** | `certifi` |
| **Dev tooling** | `pytest` (testing), `ruff` (linting) |
| **Entry point** | CLI script `ishara-e-shikkha` → `ishara_e_shikkha:main` |

Confirmed directly from the repo's dependency list — matches the Python/FastAPI +
Whisper stack discussed earlier in this conversation.