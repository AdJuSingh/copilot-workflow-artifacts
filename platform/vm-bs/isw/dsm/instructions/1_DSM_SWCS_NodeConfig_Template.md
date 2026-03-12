# DSM SWCS Requirements Template

## Overview
Template for creating SWCS (Software Component Specification) requirements from DEM analysis. Each failure from DEM analysis becomes a separate SWCS requirement.

## SWCS Node Configuration Approach

### Requirement Generation Strategy
- **One Requirement per Failure**: Each failure word from DEM analysis generates a separate SWCS requirement
- **Node Hierarchy Requirements**: Additional requirements for node structure and parent relationships
- **Simplified CSV Population**: Only populate essential columns, leave others empty

### Required CSV Columns to Populate
- `Requirements_ID_RB`: Generated using existing ID pattern
- `Description_of_requirement_RB`: Derived from template content below  
- `CP_Status_RB_RS`: "accepted" for implementation requirements, "no_req" for headers
- `MS_Status_RB_RS`: "new" for all generated requirements
- `Realizing_SWComponent_RB`: "<<component>>DEM" for all requirements

## Requirement Types and Templates

### 1. Node Header Requirement
- **Purpose**: Main section header for node configuration
- **Description Template**: "3.2.X General Requirements to configure Node_<NodeName>"
- **CP_Status_RB_RS**: "no_req"
- **MS_Status_RB_RS**: "new"

### 2. Description Section Header
- **Purpose**: Section header for description
- **Description Template**: "3.2.X.1 Description"
- **CP_Status_RB_RS**: "no_req"
- **MS_Status_RB_RS**: "new"

### 3. Node Description Requirement  
- **Purpose**: Node characteristics and configuration parameters
- **Description Template**:
```
Description of Node: 
Status Export to ASW: False
Node Initialisation by ASW: True
Allowed Recoveries: 0xFF
HWShutdown: NoHWShutdown
Priorities of FW Disabled: False
```
- **CP_Status_RB_RS**: "accepted"
- **MS_Status_RB_RS**: "new"
- **Note**: Use these default values unless explicitly specified otherwise in DEM requirements
- **CRITICAL**: Must be "accepted" for DSM_CT_Generator to recognize Node content

### 4. Functional Requirements Header
- **Purpose**: Section header for functional requirements
- **Description Template**: "3.2.X.2 Functional Requirements"
- **CP_Status_RB_RS**: "no_req"
- **MS_Status_RB_RS**: "new"

### 5. Core Behavior Header
- **Purpose**: Section header for core behavior
- **Description Template**: "3.2.X.2.1 Core Behavior"
- **CP_Status_RB_RS**: "no_req"
- **MS_Status_RB_RS**: "new"

### 6. Description of Node Header
- **Purpose**: Section header for node description
- **Description Template**: "3.2.X.2.1.1 Description of Node"
- **CP_Status_RB_RS**: "no_req"
- **MS_Status_RB_RS**: "new"

### 7. Failure Words Table Requirement
- **Purpose**: Main failure words table with first failure
- **Description Template**:
```
Description_of_Node_<NodeName>

Failure words assigned
Failure words	Priority
FW_<FirstFailureName>	<Priority>
 
```
- **CP_Status_RB_RS**: "accepted"
- **MS_Status_RB_RS**: "new"

### 8. Individual Failure Requirements (One per Additional Failure)
- **Purpose**: Each additional failure word as separate requirement
- **Description Template**:
```
FW_<FailureName>	<Priority>
 
```
- **CP_Status_RB_RS**: "accepted"  
- **MS_Status_RB_RS**: "new"

### 9. Hierarchy Header
- **Purpose**: Section header for hierarchy
- **Description Template**: "3.2.X.2.1.2 Hierarchy of Node"
- **CP_Status_RB_RS**: "no_req"
- **MS_Status_RB_RS**: "new"

### 10. Parent Nodes Requirement
- **Purpose**: Define parent-child relationships
- **Description Template**:
```
ParentNodes_of_Node_<NodeName>

ParentNodes
<ParentNodeName>

```
- **CP_Status_RB_RS**: "accepted"
- **MS_Status_RB_RS**: "new"

### 11. Performance Requirements Header
- **Purpose**: Section header for performance requirements
- **Description Template**: "3.2.X.2.2 Performance Requirements"
- **CP_Status_RB_RS**: "no_req"
- **MS_Status_RB_RS**: "new"

## Implementation Guidelines

### Section Numbering
- Use next available section number (e.g., 3.2.X)
- Generate sequential requirement IDs following existing pattern

### Requirement Generation Per Node
For each node with N failures, generate N+9 requirements:
1. **1 Node Header**: General Requirements to configure Node_X (no_req)
2. **1 Description Header**: 3.2.X.1 Description (no_req)
3. **1 Description Content**: Node configuration parameters (**accepted**)
4. **1 Functional Header**: 3.2.X.2 Functional Requirements (no_req)
5. **1 Core Behavior Header**: 3.2.X.2.1 Core Behavior (no_req)
6. **1 Description of Node Header**: 3.2.X.2.1.1 Description of Node (no_req)
7. **1 Failure Table**: Description_of_Node_X with first failure word (accepted)
8. **N-1 Individual Failures**: Each additional failure word (accepted)
9. **1 Hierarchy Header**: 3.2.X.2.1.2 Hierarchy of Node (no_req)
10. **1 Parent Nodes**: ParentNodes_of_Node_X (accepted)
11. **1 Performance Header**: 3.2.X.2.2 Performance Requirements (no_req)

### CSV Format Requirements
- **Only populate 5 columns**: Requirements_ID_RB, Description_of_requirement_RB, CP_Status_RB_RS, MS_Status_RB_RS, Realizing_SWComponent_RB
- **Leave other columns empty**: All other CSV columns should remain empty
- **Standard Values**: 
  - MS_Status_RB_RS: Always "new"
  - Realizing_SWComponent_RB: Always "<<component>>DEM"
  - CP_Status_RB_RS: "no_req" for headers, "accepted" for implementations

### Content Population
- **Node Name**: Extract from DEM analysis (e.g., "Node_VoltageHandler1")
- **Parent Node**: Extract from DEM node information (e.g., "Node_Ecu")
- **Failure Names**: Extract each failure individually with FW_ prefix
- **Failure Priorities**: Extract priority for each failure from DEM analysis
- **System Strategy**: Use from DEM analysis (e.g., "ESPBase_EbdPumpless")

### Default Node Configuration Values
**Always use these default values unless explicitly specified otherwise in DEM requirements:**
- **Status Export to ASW**: False
- **Node Initialisation by ASW**: True  
- **Allowed Recoveries**: 0xFF
- **HWShutdown**: NoHWShutdown
- **Priorities of FW Disabled**: False

### Critical Format Notes
- **Each failure word is a separate requirement** with format "FW_<FailureName> <Priority>"
- **First failure included in main failure table**, additional failures as individual requirements
- **Proper hierarchical section numbering** following 3.2.X.Y.Z pattern
- **CRITICAL STATUS VALUES**: 
  - Node Description requirement: **MUST be "accepted"** for DSM_CT_Generator to work
  - Failure words requirements: "accepted" for implementation
  - Parent nodes requirement: "accepted" for implementation  
  - Headers: "no_req" for section headers
- **Default configuration parameters**: Use standard defaults unless DEM specifies otherwise
- **DSM_CT_Generator Dependency**: Node Description, Failure Words, and Parent Nodes must have "accepted" status for successful testcase generation

This template ensures each failure gets individual traceability while maintaining proper node structure requirements following the established CSV format.