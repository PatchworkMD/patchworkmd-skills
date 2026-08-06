---
name: patchworkmd-skill-release
description: Prepare reviewable PatchworkMD-branded open-source skill release packages with provenance, licenses, privacy scans, documentation, tests, and ship gates. Use when packaging Codex or Hermes skills for GitHub or maintainer programs; never publish or push without explicit approval.
---

# PatchworkMD Skill Release

## Purpose

Turn a local skill into a small, auditable release candidate. Keep source provenance and license decisions explicit, remove private material, and stop at a reviewable export unless publication is separately authorized.

## Release workflow

1. Inventory the existing skill and related canonical skills. Do not duplicate an existing `record-replay` or Hermes skill; package or improve the existing one instead.
2. Preserve the source skill in place. Build a separate export candidate under a user-approved export folder.
3. Include only `SKILL.md`, `agents/openai.yaml`, required references/scripts/assets, a license decision, provenance manifest, and test evidence.
4. Scan for credentials, private paths, donor/contact/financial rows, local tokens, machine identifiers, and copied third-party source.
5. Run the skill validator and deterministic tests. Record toolchain versions and known environment blockers.
6. Write plain-language README/release notes only in the export package when needed for the target program; keep the canonical skill lean.
7. Mark `READY FOR REVIEW`, `HOLD`, or `NOT CLEARED FOR PUBLICATION`. Do not push, create a release, publish, or enroll in a program.

## Hermes Agent Record Replay

Use the existing `record-replay` skill as the canonical implementation for Hermes/Codex record-and-replay behavior. Package it only after checking provenance, permissions, trace redaction, replay approval, and runtime dependencies. Do not create a competing owner or silently replay a trace.

## PatchworkMD positioning

- Lead with the user outcome, supported platforms, safety boundary, evidence, and limitations.
- Explain what is useful to an average user before implementation details.
- Keep claims tied to tests or mark them as estimates.
- Separate “works locally,” “ready for review,” and “published.”

## Ship checklist

- [ ] No private/auth/credential material.
- [ ] No unlicensed third-party source or unclear copied assets.
- [ ] `SKILL.md` frontmatter and `agents/openai.yaml` validate.
- [ ] Tests and fixtures pass; failures are explained.
- [ ] Provenance and hashes are recorded.
- [ ] Human review of wording, license, destination, and publication is complete.
- [ ] Push/publication is separately approved.

## Resource

See [release-manifest.md](references/release-manifest.md) for candidate manifest fields.
