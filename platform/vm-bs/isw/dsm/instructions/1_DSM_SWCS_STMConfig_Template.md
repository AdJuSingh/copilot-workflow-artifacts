# DSM SWCS STM Requirements Template

## Overview
Template for creating SWCS STM (State Machine) Configuration requirements from DEM analysis. Each node degradation mapping from DEM analysis becomes a separate SWCS STM requirement.

## SWCS STM Configuration Approach

### Requirement Generation Strategy
- **One Requirement per Node Degradation**: Each node degradation state mapping from DEM analysis generates a separate SWCS STM requirement
- **System/Controller Headers**: Additional requirements for system configuration headers
- **Simplified CSV Population**: Only populate essential columns, leave others empty

### Required CSV Columns to Populate
- `Requirements_ID_RB`: Generated using existing ID pattern
- `Description_of_requirement_RB`: Derived from template content below  
- `CP_Status_RB_RS`: "accepted" for implementation requirements, "no_req" for headers
- `MS_Status_RB_RS`: "new" for all generated requirements
- `Realizing_SWComponent_RB`: "<<component>>DEM" for all requirements

## Requirement Types and Templates

### 1. System Header Requirement
- **Purpose**: Main section header for system/controller configuration
- **Description Template**: "3.2.X General Requirements to configure <SystemName>"
- **CP_Status_RB_RS**: "no_req"
- **MS_Status_RB_RS**: "new"

### 2. System Description Requirement  
- **Purpose**: System characteristics and configuration parameters
- **Description Template**:
```
Configuration for <SystemName>: State machine configuration for system <SystemName> including degradation states and node dependencies.
Activation Conditions: System activation conditions and release criteria
Core Behavior: State transitions and degradation logic
Node Dependencies: Dependencies on failure monitoring nodes
```
- **CP_Status_RB_RS**: "accepted"
- **MS_Status_RB_RS**: "new"

### 3. Individual Node Degradation Requirements (One per Node)
- **Purpose**: Configuration for each specific node degradation state mapping
- **Description Template**:
```
<NodeName> <DegradationState>

```
- **CP_Status_RB_RS**: "accepted" (always use "accepted" for new STM degradation mappings)
- **MS_Status_RB_RS**: "new"

### 4. Node Degradation Specification Header
- **Purpose**: Section header for node degradation mappings
- **Description Template**: "NodeDegradation_Specification_<SystemName>"
- **CP_Status_RB_RS**: "no_req"
- **MS_Status_RB_RS**: "new"

## STM Configuration Hierarchy

### System Structure
```
3.2.X General Requirements to configure <SystemName>
├── 3.2.X.1 Functional Requirements
│   ├── 3.2.X.1.1 Activation/Release Conditions
│   ├── 3.2.X.1.2 Core Behavior
│   │   ├── 3.2.X.1.2.1 States
│   │   ├── 3.2.X.1.2.2 Dependency of States On <SystemName>
│   │   └── 3.2.X.1.2.3 Dependency on nodes
├── NodeDegradation_Specification_<SystemName>
└── [Individual Node Degradation Mappings]
```

## Implementation Guidelines

### Section Numbering
- Use next available section number (e.g., 3.2.X)
- Generate sequential requirement IDs following existing pattern

### Requirement Generation Per System
For each system with N node degradations, generate N+M requirements:
1. **1 System Header**: Section header requirement
2. **M Structure Requirements**: Functional requirements hierarchy (typically 6-7)
3. **1 Degradation Header**: NodeDegradation_Specification header
4. **N Node Degradation Requirements**: One requirement per node degradation mapping

### CSV Format Requirements
- **Only populate 5 columns**: Requirements_ID_RB, Description_of_requirement_RB, CP_Status_RB_RS, MS_Status_RB_RS, Realizing_SWComponent_RB
- **Leave other columns empty**: All other CSV columns should remain empty
- **Standard Values**: 
  - MS_Status_RB_RS: Always "new"
  - Realizing_SWComponent_RB: Always "<<component>>DEM"
  - CP_Status_RB_RS: "no_req" for headers, "accepted" for implementations

### Content Population
- **System Name**: Extract from DEM analysis (e.g., "ESPBase", "DTC", "DTF")
- **Node Names**: Extract from DEM node information  
- **Degradation States**: Extract degradation state for each node
- **System Strategy**: Use from DEM analysis for configuration mapping

## STM-Specific Requirements

### Node Degradation Mapping Format
Each node degradation requirement follows this pattern:
```
<NodeName> <DegradationState>

```

### Example Node Degradation Mappings
- `Node_AxsNet ESPBase_AbsOnTcsDegraded`
- `Node_Sas ESPBase_AbsOnTcsDegraded` 
- `Node_WssFl ESPBase_EbdOn`
- `Node_Varcode ESPBase_EbdOn`

### System Types
Common STM systems include:
- **ESPBase**: Master system with multiple degradation states
- **DTC/DTF**: Diagnostic systems
- **HBA/HFC**: Brake assist systems  
- **VLC**: Vehicle logic control
- **AVH/ABA/ABP**: Advanced brake systems
- **HSM**: Hill start management

This template ensures each node degradation gets individual traceability while maintaining system structure requirements for STM configuration.