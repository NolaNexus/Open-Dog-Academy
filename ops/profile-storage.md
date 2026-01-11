# Profiles + Household Specs (Out of Scope for This Repo)
Status: draft
Updated: 2026-01-10

This repo is designed to stay **dog-agnostic** and **safe to publish**.

One-dog/one-household specs (campus layouts, station hardware, schedules, logins, meetup coordination, personal constraints) tend to include:
- private details
- local logistics
- hardware that changes frequently

## Storage policy
- Store these documents in a separate **Profiles** location (private by default).
- If something becomes generally useful, **extract the principle** and promote it into ODA:
  - a non-negotiable rule → `docs/standards/`
  - a teachable how-to → `docs/manuals/`
  - a measurable behavior → `docs/skills/`

## Suggested external structure (example)
- `profiles/<dog_name>/`
  - `profile.md`
  - `training-log.md`
  - `environment-spec.md`
  - `gear.md`
  - `meetup-notes.md`
