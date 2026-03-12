# DSM SWCS Requirements Generation Instructions

## Purpose
Generate SWCS Node Configuration and STM Configuration requirements by analyzing DEM requirements and comparing against existing SWCS documentation to identify new nodes, system strategies, or changes requiring updates.

## Input Files

### Primary Input
- **Source**: `GenFromCoPilot/requirements/DEM_Requirements.md`
- **Purpose**: Extract node configuration data from completed DEM analysis

### Reference Input  
- **Source**: `GenFromCoPilot/requirements/*SWCS*_DSM_Node_Config*.csv`
- **Purpose**: Check for existing nodes and validate against current configuration
- **Note**: Filename pattern may vary by project (e.g., 000000_SWCS_DSM_Node_Config_ESP_Europium.csv)

### STM Reference Input
- **Source**: `GenFromCoPilot/requirements/*SWCS*_DSM_STM_Config*.csv`
- **Purpose**: Check for existing system strategies and node degradation mappings
- **Note**: Filename pattern may vary by project (e.g., 000000_SWCS_DSM_STM_Config_ESP_Europium.csv)

### Template References
- **Source**: `1_DSM_SWCS_NodeConfig_Template.md`
- **Purpose**: Format structure for new SWCS Node requirements
- **Source**: `1_DSM_SWCS_STMConfig_Template.md`  
- **Purpose**: Format structure for new SWCS STM requirements

## Data Extraction Process

### Step 1: Parse DEM Requirements
From `DEM_Requirements.md`, extract the following for each node:

#### Required Node Data
```
- Node Name: (e.g., "Node_VoltageHandler1")
- Node Description: (from Node Information section)
- Failure Names and Priorities: (from Failure Priority Mapping table)
- Parent Node: (from Node Information table)
- System Strategy: (from Node Information section)
```

#### Extraction Example
```markdown
## Node: Node_VoltageHandler1

### Node Information
| **Parent Node** | Node_Ecu |

### Failure Priority Mapping
| Failure Name | Priority | Source |
| HydraulicUndervoltage1 | 100 | From Requirements.csv |
| HydraulicUndervoltage2 | 90 | From Requirements.csv |
```

**Extracted Data:**
- Node Name: "Node_VoltageHandler1"
- Parent Node: "Node_Ecu"  
- System Strategy: "ESPBase_EbdPumpless"
- Failures: ["HydraulicUndervoltage1":100, "HydraulicUndervoltage2":90]

### Step 2: Validate Against Existing SWCS
For each extracted node, check both SWCS CSV files:

#### Step 2A: Node Configuration Validation
Check the project's Node Config CSV file (`*SWCS*_DSM_Node_Config*.csv`):

#### Node Existence Check
Search CSV for entries containing:
```
"3.2.X General Requirements to configure Node_<NodeName>"
```

#### If Node EXISTS - Validate Content
1. **Extract Current Failures**: Find entries with failure word tables
2. **Compare Failure Lists**: Check if failure names and priorities match
3. **Validate Parent Node**: Verify parent node relationships
4. **Decision**: 
   - If **NO CHANGES**: Skip node (no updates needed)
   - If **CHANGES FOUND**: Flag for update (manual review required)

#### If Node NOT FOUND - Generate New Requirements
Proceed to Step 3 for new node generation.

#### Step 2B: STM Configuration Validation
Check the project's STM Config CSV file (`*SWCS*_DSM_STM_Config*.csv`):

##### System Strategy Existence Check
For each extracted node's system strategy, search CSV for:
```
"3.2.X General Requirements to configure <SystemName>"
```
Where `<SystemName>` is derived from system strategy (e.g., "ESPBase" from "ESPBase_EbdPumpless")

##### Node Degradation Mapping Check
Within the system section, search for node degradation entries:
```
"<NodeName> <DegradationState>"
```

##### STM Decision Logic
- **System EXISTS + Node Mapping EXISTS**: Skip STM generation for this node
- **System EXISTS + Node Mapping NOT FOUND**: Generate only node degradation requirement
- **System NOT EXISTS**: Generate complete system configuration with node degradation mappings
- **No System Strategy**: Skip STM generation for this node

## Step 3: Generate New SWCS Requirements

### Step 3A: Node Configuration Generation
For new nodes only, create complete node configuration following the template structure:

#### Requirement Generation Strategy
Generate individual requirements for each failure word plus node structure requirements:
- **One requirement per failure word** from DEM analysis
- **Additional node structure requirements** (header, description, hierarchy)
- Refer to `1_DSM_SWCS_NodeConfig_Template.md` for detailed templates and content formats

#### Requirement ID Generation
Extract and follow existing ID pattern from project's SWCS CSV file:
```
1. Parse existing CSV requirement IDs from *SWCS*_DSM_Node_Config*.csv
2. Identify pattern (e.g., "[ProjectPrefix]_SWCS_DSM_Node_[ProjectSuffix]-XXX")
3. Extract base prefix and numbering scheme specific to current project
4. Generate new IDs using same pattern with next sequential numbers
```

#### Requirement ID Pattern Analysis
- **Extract ID Format**: Analyze existing CSV entries to identify the requirement ID pattern
- **Example Analysis**: From project-specific ID like `000000_SWCS_DSM_Node_ESP_Europium_ESP250-983` extract:
  - Base Pattern: `[ProjectPrefix]_SWCS_DSM_Node_[ProjectSuffix]-`
  - Sequential Number: `983`
- **Generate New IDs**: Use identified pattern with next sequential numbers
- **Format Preservation**: Maintain exact same prefix and numbering scheme as existing entries
- **Pattern Flexibility**: ID format varies by project but follows `*SWCS*_DSM_Node_*-XXX` structure

#### Section Number Assignment
- Find highest existing section number in CSV (e.g., 3.2.8)
- Assign next sequential number (e.g., 3.2.9) to new node
- Increment for each additional new node

### Step 3B: STM Configuration Generation
For new system strategies or missing node degradation mappings:

#### System Strategy Name Extraction
From system strategy (e.g., "ESPBase_EbdPumpless"):
- Extract system name: "ESPBase"
- Determine degradation state: "EbdPumpless" (or analyze based on failure types)

#### STM Requirement Generation Strategy
Generate requirements based on STM validation results:
- **New System**: Create complete system configuration (N+M requirements)
- **Existing System**: Create only node degradation requirement (1 requirement)
- Refer to `1_DSM_SWCS_STMConfig_Template.md` for detailed templates and content formats

#### STM Requirement ID Generation
Extract and follow existing ID pattern from project's STM CSV file:
```
1. Parse existing CSV requirement IDs from *SWCS*_DSM_STM_Config*.csv
2. Identify pattern (e.g., "[ProjectPrefix]_SWCS_DSM_STM_[ProjectSuffix]-XXX")
3. Extract base prefix and numbering scheme specific to current project
4. Generate new IDs using same pattern with next sequential numbers
```

#### STM Section Number Assignment
- Find highest existing section number in STM CSV (e.g., 3.2.15)
- Assign next sequential number (e.g., 3.2.16) to new system
- For existing systems, add node degradation within existing section

## Content Generation Templates

Refer to the detailed template content and CSV examples in:
- `1_DSM_SWCS_NodeConfig_Template.md` for Node Configuration requirements
- `1_DSM_SWCS_STMConfig_Template.md` for STM Configuration requirements

## Processing Workflow

### Phase 1: Analysis
1. **Read DEM Requirements**: Parse all node sections
2. **Extract Node Data**: Collect name, description, failures, parent
3. **Load Existing SWCS**: Read current CSV content
4. **Compare Nodes**: Check existence and validate content

### Phase 2: Decision Making
For each DEM node:
- **EXISTS + NO CHANGES**: Skip (log: "Node unchanged")
- **EXISTS + HAS CHANGES**: Flag for review (log: "Node requires update") 
- **NOT EXISTS**: Add to generation queue (log: "New node identified")

### Phase 3: Generation
For new nodes and system strategies:

#### Node Configuration Generation
1. **Assign Section Number**: Next available 3.2.X in Node Config CSV
2. **Generate Requirements**: Create N+9 CSV entries per node (where N = number of failures)
   - 1 Node Header requirement (no_req)
   - 1 Description Header requirement (no_req)
   - 1 Description Content requirement (no_req)
   - 1 Functional Requirements Header (no_req)
   - 1 Core Behavior Header (no_req)
   - 1 Description of Node Header (no_req)
   - 1 Failure Table requirement with first failure (accepted)
   - N-1 Individual Failure requirements (accepted, one per additional failure)
   - 1 Hierarchy Header requirement (no_req)
   - 1 Parent Nodes requirement (accepted)
   - 1 Performance Requirements Header (no_req)
3. **Apply Templates**: Use extracted data to populate templates from `1_DSM_SWCS_NodeConfig_Template.md`

#### STM Configuration Generation
1. **Assign Section Number**: Next available 3.2.X in STM Config CSV (for new systems)
2. **Generate Requirements**: Based on system existence:
   - **New System**: Create N+M CSV entries (N node degradations + M system structure)
   - **Existing System**: Create 1 node degradation requirement only
3. **Apply Templates**: Use extracted data to populate templates from `1_DSM_SWCS_STMConfig_Template.md`

#### Common Requirements
4. **Populate Only Essential Columns**: Requirements_ID_RB, Description_of_requirement_RB, CP_Status_RB_RS, MS_Status_RB_RS, Realizing_SWComponent_RB
5. **Validate Output**: Check format and completeness for both Node and STM configurations

## Placement Instructions

### Where to Insert New Node Requirements
Generated SWCS requirements must be placed in the correct location within the CSV file structure:

#### Target Section Location
- **Section**: "3.2 General Requirements to configure Nodes"
- **Placement**: At the END of section 3.2, before section 3.3 begins
- **NOT**: At the end of the entire CSV file

#### Placement Process
1. **Locate Section Boundary**: Find where section 3.2 ends and section 3.3 begins
2. **Find Last Node**: Identify the last existing node requirement in section 3.2
3. **Insert Position**: Add new node requirements immediately after the last 3.2 requirement
4. **Maintain Structure**: Preserve sequential section numbering (3.2.X)

#### Example Placement
```
... (existing node requirements)
"ESP250-3731","3.2.114.2.2 Performance Requirements","no_req","no_req"...
[INSERT NEW NODE REQUIREMENTS HERE - Section 3.2.115, 3.2.116, etc.]
"ESP250-880","3.3 General Requirements to Enable Conditions","no_req","no_req"...
... (rest of file)
```

### Where to Insert New STM Requirements

#### System Strategy Placement Logic
STM requirements must be placed within the correct system section based on the system strategy:

1. **Extract System Strategy**: Parse the system strategy from DEM node data (e.g., "ESPBase_EbdPumpless")
2. **Identify System Section**: Match the system prefix to find the corresponding CSV section
   - "ESPBase_*" → Place under "General Requirements to configure ESPBase"
   - "DTC_*" → Place under "General Requirements to configure DTC"  
   - "HBA_*" → Place under "General Requirements to configure HBA"
3. **Find Node Section**: Within the identified system section, locate the node degradation mappings area
4. **Insert Position**: Add new node degradation requirement after the last existing node mapping for that system

#### STM Placement Process
1. **Parse System Strategy**: Extract system prefix from DEM data (e.g., "ESPBase" from "ESPBase_EbdPumpless")
2. **Search CSV for System Section**: Find section matching "General Requirements to configure [SystemPrefix]"
3. **Locate Node Mappings**: Within that system section, find existing node degradation mappings
4. **Insert After Last Node**: Add new node degradation requirement after the last node mapping in that system section
5. **Maintain System Structure**: Keep requirement within the system's section boundaries

#### STM Placement Example
```
"ESP250-104","3.2.1 General Requirements to configure ESPBase(MasterSystem)"...
... (system structure requirements)
"ESP250-892","Node_YawRate_Signal ESPBase_AbsOnWithPMC"...
[INSERT NEW STM REQUIREMENT HERE - Node_VoltageHandler1 ESPBase_EbdPumpless]
"ESP250-685","3.2.1.1.2.4 State Limiters"...
... (next section)
```

#### Critical STM Placement Rules
- **NEVER** place STM requirements at the end of the entire CSV file
- **ALWAYS** place within the appropriate system section based on system strategy prefix
- **MAINTAIN** system section boundaries and structure
- **PRESERVE** sequential numbering within each system section

## Output Requirements

### Generated Content
- **New CSV Entries**: Only for nodes not found in existing CSV
- **Change Log**: Summary of nodes analyzed, skipped, flagged, and generated
- **Validation Report**: Confirmation of data extraction and generation

### Quality Checks

#### Node Configuration Checks
- [ ] All DEM nodes processed for node configuration
- [ ] Existing nodes properly validated  
- [ ] Each failure word gets individual requirement with FW_ prefix and priority
- [ ] First failure included in main failure table, additional failures as separate requirements
- [ ] Proper hierarchical section numbering (3.2.X.1, 3.2.X.2.1.1, etc.)
- [ ] Node structure requirements included (11 total: headers + content)
- [ ] Parent relationships preserved in ParentNodes_of_Node_X format
- [ ] Correct status values: no_req for headers, accepted for content
- [ ] **Default configuration values applied**: Status Export to ASW: False, Node Initialisation by ASW: True, Allowed Recoveries: 0xFF, HWShutdown: NoHWShutdown, Priorities of FW Disabled: False (unless DEM_Requirements.md specifies otherwise)

#### STM Configuration Checks  
- [ ] All system strategies extracted and validated
- [ ] Existing systems and node mappings properly checked
- [ ] Node degradation mappings created for missing entries
- [ ] System structure requirements included for new systems
- [ ] System-to-node relationships preserved
- [ ] **STM Placement Validation**: Node degradation mappings placed within correct system section based on system strategy prefix
- [ ] **System Section Integrity**: Requirements inserted within system boundaries, not at end of CSV file

#### Common Quality Checks
- [ ] Only essential CSV columns populated (5 columns) in both files
- [ ] Sequential requirement ID numbering maintained in both files
- [ ] Standard values applied (MS_Status_RB_RS="new", Realizing_SWComponent_RB="<<component>>DEM")

## Success Criteria

### Complete Analysis
- All nodes from DEM_Requirements.md processed
- Comparison against existing SWCS completed
- Clear identification of new vs existing nodes

### Accurate Generation
- Only new/missing nodes and system strategies generate requirements
- Existing unchanged nodes and system mappings remain untouched
- Template structure properly applied for both Node and STM configurations
- Data integrity maintained throughout both generation processes

This process ensures incremental updates to both Node and STM SWCS documentation while preserving existing validated content and identifying nodes and system strategies requiring attention.