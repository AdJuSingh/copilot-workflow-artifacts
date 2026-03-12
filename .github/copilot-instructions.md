# Copilot Repository-Wide Instructions

> This file is automatically attached to every Copilot chat and agent session in this repository.

## Repository Purpose

This repository contains **orchestrated workflow artifacts** (prompts, instructions, templates, and memory files) for AI-assisted software development across VM domains.

## Directory Convention

| Path | Contains |
|------|----------|
| `platform/_shared/` | Cross-domain reusable instructions, prompts, and templates |
| `platform/vm-bs/` | Brake Systems domain artifacts (asw / hsw / isw) |
| `platform/vm-oss/` | Occupant Safety Systems domain artifacts |
| `platform/vm-st/` | Steering Systems domain artifacts |
| `projects/<name>/` | Project-specific overrides and memory |
| `evals/` | Prompt regression datasets and evaluation scripts |

## Artifact Naming

- Prompts: `<number>_<Name>.prompt.md`
- Instructions: `<number>_<Name>.instructions.md`
- Memory: `<name>.memory.md` (local only, gitignored)

## Layer Resolution Order

When resolving instructions or prompts, precedence is (highest → lowest):

1. `projects/<project>/.github/instructions/` — project-specific overrides
2. `platform/<domain>/<layer>/instructions/` — domain + layer specific
3. `platform/_shared/instructions/` — cross-domain defaults

## Coding Standards

- Target language is **C** (embedded automotive)
- Follow MISRA-C guidelines unless stated otherwise in domain-specific instructions
- All generated artifacts must include traceability to requirements
