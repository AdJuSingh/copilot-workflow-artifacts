# Prompt Evaluation Framework

This directory contains regression tests and format checks for prompt and instruction artifacts.

## Structure

```
evals/
├── datasets/     # Input test cases (requirements, code snippets, etc.)
├── expected/     # Golden-file expected outputs for comparison
├── scripts/      # Evaluation runner scripts
└── README.md     # This file
```

## Purpose

- **Regression testing**: Detect when prompt changes produce unexpected output shifts
- **Format validation**: Verify generated artifacts conform to required templates
- **Quality gates**: Automated checks before merging prompt/instruction changes

## Usage

```powershell
# Run all evaluations
.\scripts\run-evals.ps1

# Run a specific eval suite
.\scripts\run-evals.ps1 -Suite "format-check"
```
