# Repository Guidelines

## Project Structure & Module Organization
- `modeler-skills/` holds the main documentation set, with `00_index.md` as the entry point and numbered topical guides (e.g., `10_...md`, `20_...md`).
- Root-level markdown files (`pigment-formula-guide.md`, `formula-fetch.md`, `workspace-service-endpoints.md`) provide standalone reference material.
- Python utilities live at the root (`time-input-setup.py`, `time-input-finish.py`).

## Build, Test, and Development Commands
This repo is documentation-first and does not define a build system or test suite. If you add tooling, document it here with concrete commands. Examples:
- `python time-input-setup.py` — runs the setup script (if needed for local workflows).
- `python time-input-finish.py` — runs the finish script (if needed for local workflows).

## Coding Style & Naming Conventions
- Markdown files use descriptive, topic-first names and a numeric prefix ordering in `modeler-skills/` (e.g., `30_lists_dimensions_blocks.md`).
- Keep headings concise and use sentence-case prose.
- For Python, prefer standard PEP 8 formatting, 4-space indentation, and clear function naming.

## Testing Guidelines
No automated tests are currently configured. If you introduce tests, add the framework, naming rules, and how to run them here.

## Commit & Pull Request Guidelines
This directory is not a Git repository, so commit conventions cannot be inferred. If you add version control, define:
- Commit message format (e.g., `type: short summary`).
- PR requirements (scope description, linked issues, and any screenshots for doc layout changes).

## Agent-Specific Instructions
- Keep updates concise and consistent with the existing documentation style.
- When adding new skill docs, update `modeler-skills/00_index.md` to link them in order.
