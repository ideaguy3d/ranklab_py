---
name: ranklab-subproject-starter
description: Create or refine standalone RankLab Python subprojects inside ranklab_py that are independently deployed (for example to separate leapcell.dev URLs) and embedded in ranklab.org via iframe. Use when starting a new subproject, adapting the FastAPI + ChatKit template, defining project-specific vs generic multi-agent files, fixing template regressions, or applying consistent baseline conventions across subprojects.
---

# RankLab Subproject Starter

## Overview

Build project-local, standalone AI subprojects with a consistent baseline and minimal overhead.
Treat each subproject as isolated: no cross-subproject communication and independent deployment.

## Workflow

### 1. Confirm Subproject Scope

- Identify subproject name and target purpose.
- Keep the architecture self-contained within one folder under `ranklab_py/`.
- Assume independent deploy target (one URL per subproject).

### 2. Bootstrap Minimal App Skeleton

Create or maintain these baseline files:
- `main.py`: FastAPI app, ChatKit endpoint, static mount.
- `chatkit_store.py`: simple in-memory store for demo stage.
- `static/index.html` and `static/main.js`: minimal UI.
- `agents_general.py`: reusable generic agents + generic tools.

Use canonical scaffold references from this skill:
- `references/scaffold/main.py`
- `references/scaffold/chatkit_store.py`
- `references/scaffold/agents_general.py`
- `references/scaffold/static/index.html`
- `references/scaffold/static/main.js`

### 3. Preserve Baseline Runtime Behavior

Default local run command:
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Finish With Concrete Deliverables

At the end of each task:
- State what changed and why.
- Run a lightweight validity check (`py_compile` or equivalent) when applicable.
- Keep next steps small and numbered when useful.

## Conventions

- Keep code simple and explicit over clever abstractions.
- Avoid cross-subproject dependencies.
- Keep files project-local; prefer edits in the current subproject directory.

## Quick Start Checklist

Use this checklist when creating a new subproject:
1. Create subproject folder and baseline files.
2. Copy scaffold references from `references/scaffold/`.
3. Keep one generic router in `agents_general.py` initially.
4. Verify local run command works.
5. Compile-check modified Python files.
