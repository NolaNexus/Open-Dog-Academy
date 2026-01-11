# Interface truncation runbook
Status: draft

Truncation can happen *even when repo documents are within limits* because the **chat interface** (and model output budgets) may cut off long outputs.

This runbook treats truncation as an *interface reliability problem* and defines how we detect it, recover cleanly, and prevent it.

## What truncation usually looks like

- Output ends mid-sentence or mid-list
- A section is missing its closing rubric/checklist
- A file or YAML shown in chat contains “missing middle” content
- The assistant claims it ran something, but the pasted artifact is incomplete (red flag)

## Root causes (practical model)

1. **Output budget / token limits**: models have a maximum combined token budget (input + output). When you exceed it, output can be cut or shortened.  
2. **Context window pressure**: long conversations reduce room for new output.  
3. **UI/render limits**: the interface may shorten or omit long blocks even when the model generated more.

## Detection and confirmation

Use at least one of these:

- Look for a deliberate end marker like `<!-- END -->` or `END_OF_PART n/N`. If it’s missing, assume truncation.
- Count parts: if you requested `PART 1/4` and only got 1–2, assume truncation.
- If code/YAML is involved, run validators locally (CI will also catch most cases).

## Recovery protocol (no drama)

1. **Freeze**: do not “patch over” missing text by guessing.
2. Ask for **resume from the last intact heading** (H2/H3), not “continue”.
3. Prefer **file artifacts** (zip/MD exports) over pasting huge blocks into chat.
4. If the content is meant to live in the repo, refactor into **atoms + assemblies** instead of making one bigger doc.

## Prevention protocol (default)

### A) Use a chat-safe budget
For chat output, keep any single response **small enough** that the UI won’t choke.

- Prefer: <= ~6,000 characters per part
- Always include an end marker.

### B) Export in parts when needed
Use the repo tool:

- `scripts/chunk_for_chat.py` — turns one doc (optionally with expanded includes) into multiple chat-safe parts + an index.

### C) Modularize proactively
If a document consistently needs to be pasted around, it’s a sign it should be:

- split into modules, and/or
- extracted into reusable atoms

## Tools

- `scripts/validate_doc_limits.py` — hard caps + warning threshold
- `scripts/suggest_doc_split.py` — suggests how to split a too-large doc
- `scripts/chunk_for_chat.py` — creates chat-safe chunks (optionally expands atom includes)

