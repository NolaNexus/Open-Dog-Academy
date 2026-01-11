# AI output protocol (chat-safe)
Status: draft

This repo assumes AI tools can truncate long responses. So we work in *parts*.

## Rules of engagement

- Never paste an artifact bigger than the chat-safe budget.
- Always end parts with an explicit marker.
- Prefer *files* (zip/MD) for anything non-trivial.

## Chat-safe budget

Default:
- **Max characters per part:** 6,000
- **Max lines per part:** 200

## Required end markers

Every multi-part output must end with:

`<!-- END_OF_PART n/N -->`

Example:

`<!-- END_OF_PART 2/5 -->`

If the marker is missing, treat the part as truncated.

## How to export repo docs for chat

Use:

`python3 scripts/chunk_for_chat.py docs/path/to/file.md --expand-includes`

This produces:
- an index file
- part files sized for chat
- end markers included automatically

## When to refactor instead of chunk

Chunking is a delivery mechanism. Refactor when:

- the same content is reused across 2+ assemblies
- you’re repeating rubrics, checklists, or protocols
- a single doc keeps approaching caps

Refactor path:
- extract truth into atoms
- keep assemblies as playlists + glue text
