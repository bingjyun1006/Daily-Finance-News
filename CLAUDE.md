# Training Project

This is the primary workspace for development and research.

## Scope
All experimental code, data exploration, and learning work happens here.
Do **not** write to paths outside this directory unless explicitly instructed.

## Directory Layout
- `src/`         — code and scripts under development
- `data/`        — datasets and processed outputs
- `experiments/` — one-off experiments and exploratory notebooks
- `notes/`       — findings, references, and working notes

## Rules
- New files go into the appropriate subdirectory above.
- Global Claude config (`.md/`, `.skill/`, `settings.json`) lives in `~/.claude/` and is shared across all projects — do not duplicate it here.
- Prefer modifying files inside this folder; flag it explicitly if a task requires touching files elsewhere.
