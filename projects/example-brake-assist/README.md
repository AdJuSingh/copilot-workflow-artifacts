# Example Project: Advanced Brake Assist System

## Project Overview

This project demonstrates a hybrid approach to organizing agentic artifacts for a multi-BU project involving brake assist with steering and safety system integration.

## Project-Specific Approach

### Organization Strategy
- **Feature-Based Structure** - Organized by functional features
- **Cross-BU Integration** - Coordinates VM-BS, VM-ST, and VM-OSS components
- **Agile Development** - Supports iterative development cycles

### Custom Artifact Structure

```
example-brake-assist/
├── features/
│   ├── emergency-braking/
│   │   ├── vm-bs-integration/    # Brake-specific prompts
│   │   ├── vm-st-integration/    # Steering coordination prompts  
│   │   └── vm-oss-integration/   # Safety system prompts
│   ├── adaptive-cruise/
│   └── collision-avoidance/
├── integration/
│   ├── cross-bu-interfaces/
│   ├── system-validation/
│   └── safety-analysis/
└── variants/
    ├── highway-assist/
    ├── city-assist/
    └── parking-assist/
```

## Deviation from Platform Standards

1. **Feature-First Organization** - Groups by functionality rather than SW layer
2. **Cross-BU Integration Focus** - Emphasizes inter-system coordination
3. **Use Case Variants** - Organized by driving scenarios rather than hardware variants

This approach is suitable for projects that span multiple business units and require tight integration between traditionally separate systems.