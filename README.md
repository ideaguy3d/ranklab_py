# ranklab_py

Monorepo for standalone RankLab Python AI subprojects.

Each subproject lives in its own folder, runs independently, and is deployed to its own Leapcell URL (for example `id1.leapcell.dev`, `id2.leapcell.dev`). Subprojects are intended to be embedded in `ranklab.org` via iframe, not to call each other.

## Architecture

- **Isolation first**: each app is self-contained.
- **Independent deployment**: each subproject gets its own URL and release lifecycle.
- **No inter-subproject communication**: keep boundaries clean and avoid shared runtime coupling.
- **Fast demo defaults**: simple in-memory chat stores are acceptable for early iterations.

## Current Subprojects

- `resume-customizer/`
- `rank-budget/`

Both currently follow a lightweight pattern:
- FastAPI backend
- ChatKit endpoint with streaming
- vanilla JS + HTML frontend
- multi-agent setup

## Repo Layout

```text
ranklab_py/
  .agents/
    skills/
      ranklab-subproject-starter/
        SKILL.md
        openai.yaml
        references/scaffold/
          main.py
          chatkit_store.py
          agents_general.py
          static/index.html
          static/main.js
  resume-customizer/
  rank-budget/
```

## Local Development

Run from inside a subproject folder (for example `resume-customizer/`):

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:
- `http://localhost:8000`

## New Subproject Workflow

1. Create a new subproject folder under `ranklab_py/`.
2. Copy scaffold files from:
   - `.agents/skills/ranklab-subproject-starter/references/scaffold/`
3. Start with generic `agents_general.py`.
4. Add domain-specific agents only when needed for that subproject.
5. Keep the app standalone and deployment-ready.

## Notes

- Keep changes project-local to avoid accidental cross-subproject coupling.
- Treat this repo as a collection of independent products sharing only development conventions.
