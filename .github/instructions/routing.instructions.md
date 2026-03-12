# Artifact Routing & Discovery

> This instruction file helps Copilot locate the correct platform artifacts based on the developer's current context.

## Domain Mapping

| Domain Code | Full Name | Path |
|-------------|-----------|------|
| `vm-bs` | Brake Systems | `platform/vm-bs/` |
| `vm-oss` | Occupant Safety Systems | `platform/vm-oss/` |
| `vm-st` | Steering Systems | `platform/vm-st/` |

## Software Layer Mapping

| Layer Code | Full Name | Subfolder |
|------------|-----------|-----------|
| `asw` | Application Software | `asw/` |
| `hsw` | Hardware-Related Software | `hsw/` |
| `isw` | Infrastructure Software | `isw/` |

## ISW Sub-Domains

| Sub-Domain | Full Name | Subfolder |
|------------|-----------|-----------|
| `dcom` | Diagnostic Communication | `isw/dcom/` |
| `dsm` | Diagnostic Software Manager | `isw/dsm/` |
| `net` | Network Configuration | `isw/net/` |

## Artifact Type Folders

Each domain/layer combination contains:

| Folder | Artifact Type |
|--------|---------------|
| `instructions/` | Reusable rules, templates, checklists (`.instructions.md`) |
| `prompts/` | Agent task definitions (`.prompt.md`) |
| `templates/` | Output format templates (optional) |
| `plugins/` | External tool integrations (optional) |
| `tools/` | CLI tools and executables (optional) |

## Resolution Example

For a developer working on **Brake Systems → Infrastructure Software → DCOM**:

```
platform/vm-bs/isw/dcom/instructions/   ← domain-specific
platform/_shared/instructions/           ← shared fallback
```
