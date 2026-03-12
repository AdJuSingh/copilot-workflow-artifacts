# Onboarding Guide

## Getting Started with the Orchestrated Workflow

### Prerequisites

- VS Code with GitHub Copilot extension
- Access to the Agent Artifacts repository on GitHub (BoschDevCloud)

### Quick Start

1. **Clone this repository** into your workspace
2. **Identify your domain and layer**:
   - Domain: `vm-bs` (Brake Systems), `vm-oss` (Occupant Safety), `vm-st` (Steering)
   - Layer: `asw` (Application SW), `hsw` (Hardware SW), `isw` (Infrastructure SW)
3. **Navigate to your artifacts**: `platform/<domain>/<layer>/prompts/`
4. **Execute prompts** in VS Code: Type `/<promptName>` in Copilot Agent Mode

### Repository Structure Overview

```
platform/          → Reusable platform-level artifacts (prompts, instructions, templates)
  _shared/         → Cross-domain defaults
  vm-bs/           → Brake Systems
  vm-oss/          → Occupant Safety Systems
  vm-st/           → Steering Systems

projects/          → Project-specific overrides and configurations
  _project-template/  → Copy this to start a new project

evals/             → Prompt regression testing and format validation
```

### Creating a New Project

1. Copy `projects/_project-template/` to `projects/<your-project-name>/`
2. Edit `project-config.yaml` to set your domain and layers
3. Add project-specific prompt or instruction overrides under `.github/`

### Layer Resolution

When Copilot resolves artifacts, it follows this priority (highest first):

1. `projects/<project>/.github/instructions/` — your project overrides
2. `platform/<domain>/<layer>/instructions/` — domain-specific rules
3. `platform/_shared/instructions/` — shared defaults

### Further Reading

- [Architecture Document](../OrchestratedAgentWorkflow_ConceptAndArchitecture.md)
- [README](../README.md)
