# Truncation workarounds (chat + copy/paste)

Status: stable

ODA is intentionally structured to avoid “turncation” (interface truncation), but some chat UIs will still silently cut off long outputs.

This page documents the *reliable* workflow for moving content through chat without losing bytes.

---

## The problem
Chat interfaces can:
- drop the tail end of long responses
- collapse hidden content
- clip very long code blocks

If you copy/paste a large doc and it truncates, you may not notice until later.

---

## The fix: chunk + hash + markers
Use `scripts/chunk_for_chat.py` to split a Markdown doc into small parts.
Each part includes:
- character/word/line counts
- a SHA-256 digest of the **body only**
- `<!-- ODA_CHUNK_BEGIN_BODY -->` and `<!-- ODA_CHUNK_END_BODY -->` markers
- `<!-- END_OF_PART n/N -->` end markers

This gives you a mechanical way to detect truncation.

---

## Create chat-safe chunks
From repo root:

```bash
python3 scripts/chunk_for_chat.py docs/manuals/manual-socialization.md \
  --expand-includes \
  --max-chars 6000 \
  --digest-lines 5
```

Output goes to:
- `docs/reference/exports_YYYY-MM-DD/chat_chunks/<doc_stem>/`

It includes:
- `index.md`
- `part-01.md`, `part-02.md`, ...
- `manifest.json`

---

## Verify you didn’t lose bytes
After copy/paste or moving parts around:

```bash
python3 scripts/verify_chat_chunks.py docs/reference/exports_YYYY-MM-DD/chat_chunks/<doc_stem>
```

Optional: rebuild the original file:

```bash
python3 scripts/verify_chat_chunks.py docs/reference/exports_YYYY-MM-DD/chat_chunks/<doc_stem> \
  --rebuild /tmp/rebuilt.md
```

Optional: compare to the original source:

```bash
python3 scripts/verify_chat_chunks.py docs/reference/exports_YYYY-MM-DD/chat_chunks/<doc_stem> \
  --compare-original docs/manuals/manual-socialization.md
```

---

## When to use this (rule of thumb)
- Any doc you plan to move through chat
- Any doc approaching the repo’s doc limits
- Any doc with many snippet includes

---

## What *not* to do
- Don’t copy/paste a whole manual as one block.
- Don’t trust “looks fine” — verify with hashes.
