# Project Template Structure

## Project Organization

Each project can have its own approach to organizing agentic artifacts while following the VM organization SW architecture.

### Project Structure Options

1. **By Feature** - Group all SW layers for a specific feature
2. **By Development Phase** - Organize by design, implementation, testing phases
3. **By Team** - Align with development team responsibilities
4. **Hybrid** - Combination of approaches based on project needs

### Example Project Structure

```
project-name/
├── requirements/
│   ├── hsw-requirements/
│   ├── asw-requirements/
│   └── isw-requirements/
├── design/
│   ├── architecture-prompts/
│   ├── interface-definitions/
│   └── safety-analysis/
├── implementation/
│   ├── code-generation/
│   ├── testing-artifacts/
│   └── integration-guides/
└── variants/
    ├── variant-a/
    └── variant-b/
```