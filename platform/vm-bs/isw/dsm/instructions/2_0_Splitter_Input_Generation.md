<!-- Combined splitter input generation instructions -->
# Splitter Input Generation – Combined Instruction File

This document combines the Failure Splitter, Node Splitter, and Graph Links instruction files into a single reference for automated agents generating Diamant-compatible splitter input files.

Contents:
- Failure Splitter Generation
- DTC Splitter Generation
- Node Splitter Generation
- Graph Links Generation
- STM Configuration Generation

-------------------------------------------------------------------------------

## Failure Splitter Generation – Instruction

This section provides detailed guidance for an automated agent to generate a Failure Splitter file (.txt) based on input data and parameters.

Objective
---------
To generate a standardized Failure Splitter file (.txt) that defines failure-related diagnostic events in compliance with AUTOSAR DEM guidelines.

Input Requirements
------------------
The following attributes must be extracted or provided for each failure entry:

| Attribute | Description |
|-----------|-------------|
| Failure name | The unique identifier or symbolic name of the failure. |
| Description | A clear and concise summary of the failure’s purpose or condition. |
| Rootcause | Explanation of the underlying issue that triggers the failure. |
| Algorithm description | Logic or algorithm used to detect the failure (detection method). |
| Good check description | Steps or conditions under which the failure is cleared. |
| **Customer** | **MANDATORY - Customer reference (e.g., Cus_RB, Cus_CHR). Used by DiamantPro for XML file routing.** |
| **SW_GROUP_REF** | **OPTIONAL - Software group reference. Used by DiamantPro for XML file routing.** |
| **PROJECT_REF** | **OPTIONAL - Project reference (e.g., Prj_iPB). Used by DiamantPro for XML file routing.** |
| **PRODUCT_LINE_REF** | **OPTIONAL - Product line reference (e.g., IPB). Used by DiamantPro for XML file routing.** |
| Debouncer type | Specifies the debouncing method used. Input variants must be normalized to `CounterBased` or `MonitoringInternal`. |

**CRITICAL KEYLIST Requirements:**
- **Customer, SW_GROUP_REF, PROJECT_REF, PRODUCT_LINE_REF** are used by DiamantPro's ModifyAdd() function to determine which XML file to write the FAILURE_WORD to.
- Without proper KEYLIST values, failures cannot be persisted to the database.
- If not provided in source data, leave PROJECT_REF, SW_GROUP_REF, and PRODUCT_LINE_REF empty (will emit as empty elements).
- Customer should always be provided; if missing from source, agent should request from user or note in warnings.
| Curable | Indicates whether the failure can be automatically cured (Yes/No). |
| Restore event to Next OC | Defines if the event is restored at the next operation cycle (True/False). |
| Detection time | The expected detection duration for the failure. |
| Task cycle | Execution frequency of the diagnostic task (e.g., 10ms, 100ms). |
| Import from ASCET | States if the failure configuration is imported from ASCET. |
| Export from ASCET | States if the configuration is exported back to ASCET. |
| Operation Cycle | The operation cycle or life-cycle context in which the failure is qualified. |
| Failed threshold | Threshold at which the failure is triggered. |
| Passed threshold | Threshold at which the failure is considered resolved. |
| Increment step size | Step increase value used in the debounce logic. |
| Decrement step size | Step decrease value used in the debounce logic. |
| Jump up value | Instant increase in counter/debounce level on failure detection. |
| Jump down value | Instant decrease on passing condition. |
| Category | Defines the diagnostic category (e.g., Class A/B/C). |

Output Format
-------------
The generated file must be a `.txt` structured Failure Splitter file containing all failure entries in the correct syntax. Each entry should follow the required AUTOSAR DEM-compliant structure and formatting.

Processing Logic
----------------
1. Parse input – Extract required attributes for each failure from the provided source (CSV, Excel, or structured text).
2. Validate fields – Ensure no mandatory field is empty. Normalize Debouncer type to one of the canonical values `CounterBased` or `MonitoringInternal` using the mapping rules below. If ambiguous, annotate the generated `.txt` near the entry and preserve the original debouncer text in `Debouncer type (source): <original>`.

Debouncer normalization mapping (defaults):
- Map common variants to `CounterBased` (e.g., `counter`, `counter-based`, `counter based`, `counterbased`, `counter_based`, `counter-based debounce`, `counter debouncer`, `countertype`).
- Map common variants to `MonitoringInternal` (e.g., `monitoring`, `monitoring internal`, `monitoringinternal`, `monitoring-internal`, `internal`).

Sign convention for counter-based thresholds:
- Failed threshold must be positive (+round(DetectionTime/TaskCycle))
- Passed threshold must be negative (-round(RecoveryTime/TaskCycle))

Jump value behavior:
- If non-zero Jump up or Jump down values exist, include `Jump up: True` and/or `Jump down: True` in the .txt; downstream XML emission should include jump values only when the flags are true.

Operation Cycle normalization:
- Supported canonical values: `OtherCycle`, `PowerCycle`, `OBD_DCY`, `PFCCycle`, `WarmUp`.
- Map common variants to these canonical values using the rules in the original Failure instructions. If absent, default to `PowerCycle` and annotate with `# DEFAULT_OPERATION_CYCLE: PowerCycle` and `Operation Cycle (source): <missing>`.

Assemble and generate:
1. Construct each failure section with key:value lines and blank-line separation.
2. **Include KEYLIST fields (Customer, SW_GROUP_REF, PROJECT_REF, PRODUCT_LINE_REF) immediately after Good check description and before Debouncer type.**
3. Save file as `Diamant_Generate_FWSplitter.txt`.
4. Include `Operation Cycle: <value>` and `Operation Cycle (source): <original>` when different.
5. Verify that the generated file adheres to expected Diamant/DEM syntax rules.

Notes
-----
- **KEYLIST attributes (Customer, SW_GROUP_REF, PROJECT_REF, PRODUCT_LINE_REF) are CRITICAL** for DiamantPro database persistence.
- Attributes like DTC, Node name, Parent Node, Requirement ID, Node Priority, and Category Justification are not required in the FW Splitter file.
- Preserve original debouncer and operation cycle texts in source-comment lines for traceability.

Example Entry
-------------
```
Failure Name: Engine_Overheat
Description: Detects when engine temperature exceeds safe operating limit.
Rootcause: Cooling system malfunction.
Algorithm description: Compares temperature sensor reading to threshold.
Good check description: Temperature returns below safe limit for 3 cycles.
Customer: Cus_CHR
SW_GROUP_REF: DCOM
PROJECT_REF: Prj_iPB
PRODUCT_LINE_REF: IPB
Debouncer type: CounterBased
Curable: Yes
Restore event to Next OC: True
Detection time: 2000ms
Task cycle: 100ms
Operation Cycle: Power cycle
Import from ASCET: Yes
Export from ASCET: No
Failed threshold: 10
Passed threshold: -5
Increment step size: 2
Decrement step size: 1
Jump up value: 3
Jump down value: 2
Jump up: True
Jump down: True
Category: Class B
Debouncer type (source): counter-based
Operation Cycle: PowerCycle
```

-------------------------------------------------------------------------------

## Node Splitter Generation – Instruction

This section provides guidance to generate a Node Splitter file (.txt) that maps nodes to failures.

Objective
---------
To generate a standardized Node Splitter file (.txt) that defines node-to-failure mappings for diagnostic hierarchy in compliance with AUTOSAR DEM guidelines.

Input Requirements
------------------
Attributes for each node entry:

- Node name (required). Accepted aliases: `Node name`, `NAME`, `Name`.
- Failure (repeatable): `FW_ShortName[,priority]`. At least one required.
- **Customer (MANDATORY)** - Customer reference (e.g., Cus_RB, Cus_CHR). Used by DiamantPro for XML file routing.
- **SW_GROUP_REF (optional)** - Software group reference. Used by DiamantPro for XML file routing. Emit empty element if not provided.
- **PROJECT_REF (optional)** - Project reference. Used by DiamantPro for XML file routing. Emit empty element if not provided.
- **PRODUCT_LINE_REF (optional)** - Product line reference. Used by DiamantPro for XML file routing. Emit empty element if not provided.
- Desc (optional).
- STATUSEXPORTTOASW (optional, default `false`).
- ASWSETSINIT (optional, default `false`).
- ALLOWEDRECOVERIES (optional, default `0xFF`).
- HWShutdown (optional, default `NoHWShutdown`).
- FW_Priorities_Disabled (optional, default `false`).

**CRITICAL:** KEYLIST fields (Customer, SW_GROUP_REF, PROJECT_REF, PRODUCT_LINE_REF) determine which XML file the NODE object is written to. Nodes should typically inherit the same KEYLIST values as their failures.

Output Format
-------------
The generated file must be a `.txt` Node Splitter file where each node block is separated by one or more blank lines. Use `Key: Value` syntax; keys are case-insensitive.

Processing Logic
----------------
1. Parse input and extract attributes for each node.
2. Validate that each node block includes a `Node name` and at least one `Failure:` line.
3. Parse `Failure:` lines in the format `FW_NAME[,priority]`:
   - If priority is missing or invalid, default to `255` and log a warning.
   - Failure names must not contain commas; if commas are required, escape them externally.
4. Apply defaults for omitted optional attributes as listed above.
5. Construct node blocks and save as `Diamant_Generate_NodeSplitter.txt`.
6. Verify syntax: ensure no duplicate node names and correct key:value formatting.

Notes
-----
- Continuation lines (lines without `:`) are treated as continuations for the previous key.
- `PROJECT_REF` and `SW_GROUP_REF` should emit as empty elements when not provided.
- The plugin emits `FW_REF` elements in the order provided. If priority sorting is required, request plugin enhancement.
- Keys are case-insensitive.

Example Node Block
------------------
```
Node name: Node_HydraulicSupply
Customer: Cus_CHR
SW_GROUP_REF: DCOM
PROJECT_REF: 
PRODUCT_LINE_REF: 
Desc: Malfunction related to voltage supply path for pump motor.
Failure: FW_RBHydraulicUndervoltage,51
Failure: FW_HydraulicSupplyUndervoltage,32
Failure: FW_HydraulicSupplyACMHUndervoltage,30
Failure: FW_RBOvervoltage,21
```

-------------------------------------------------------------------------------

## Graph Links Generation – Instruction

This section instructs the agent how to create a Graph Links `.txt` input file used by `Diamant_Generate_GraphLinks.dpp`.

Objective
---------
Generate a `.txt` file that maps parent/source nodes to target/child nodes for building `Diamant__GraphLinks__Generated.xml`.

Supported Input Formats
-----------------------
The plugin accepts several formats; multiple entries are supported and separated by blank lines.

1) Preferred Block Form (Node-based):

```
Node name: <TargetNode>
Parent: <SourceNode>
```

Accepted key variants for target: `Node name`, `Node`, `Name` (case-insensitive).
Accepted key variants for source: `Parent`, `Parent Node`, `ParentNode`, `Parent node` (case-insensitive).

2) Explicit Source/Target Block:

```
Source: <SourceNode>
Target: <TargetNode>
```

3) Single-Line Shorthand:

```
Link: <SourceNode> -> <TargetNode>
```

Processing Rules
----------------
1. Block-based parsing: collect key:value pairs until blank line; each block yields a candidate link.
2. Case-insensitive key matching; trim values.
3. Precedence: prefer explicit `Source`/`Target` keys; otherwise use `Node name`/`Parent` variants.
4. Validation: skip block and log a warning if source or target missing.
5. Output: emit one `<NODE_LINK .../>` XML element per valid block.

XML Output Format
-----------------
Each link generates a `NODE_LINK` element with attributes:

```
<NODE_LINK key="_UjY_<sanitized_source>_UjY_<sanitized_target>" source="<original_source>" target="<original_target>"/>
```

Key sanitization rules (applies only to the `key` attribute):
1. Replace spaces with underscores.
2. Keep letters, digits, underscores, and dashes only; remove other characters.

Examples
--------
Input:
```
Node name: Node_VoltageHandler1
Parent: Node_Ecu
```

Output XML:
```
<NODE_LINK key="_UjY_Node_Ecu_UjY_Node_VoltageHandler1" source="Node_Ecu" target="Node_VoltageHandler1"/>
```

Notes and Validation
--------------------
- Ensure blocks are blank-line separated.
- Node names should ideally not contain commas. If present, normalize or escape prior to running the plugin.
- Optionally validate that each referenced node exists in `Diamant_Generate_NodeSplitter.txt`.
- The plugin will emit duplicates if duplicate blocks exist; de-duplicate beforehand if needed.

Agent Mode Behavior Summary
---------------------------
| Step | Agent Action |
|------|--------------|
| 1 | Read input source containing node hierarchy data (e.g., `DEM_Requirements.md`) |
| 2 | Extract parent-child relationships |
| 3 | Create blocks with `Node name` (child) and `Parent` (parent) |
| 4 | Separate blocks with blank lines |
| 5 | Ensure referenced nodes exist in Node Splitter file (optional) |
| 6 | Save content as `Diamant_Generate_GraphLinks.txt` |
| 7 | Log summary (link count, warnings) |

Common Issues and Solutions
---------------------------
- Links not appearing: verify blank-line separation and check plugin logs for missing keys.
- Wrong key format: ensure sanitization rules are applied and supported by plugin.
- Node names with spaces: spaces are preserved in source/target attributes, converted to underscores in key.

-------------------------------------------------------------------------------

## DTC Splitter Generation – Instruction

This section provides guidance to generate **FOUR separate DTC-related input files** from DEM_Requirements.md that will be used to update the DiamantPro database.

Objective
---------
To generate four standardized `.txt` input files that define:
1. DTC entries (core properties and KEYLIST items)
2. DTC Attribute configurations
3. Failure-to-DTC links
4. DTC-to-Attribute links

These files are consumed by four DiamantPro plugins:
- `Diamant_Update_DTC.dpp`
- `Diamant_Update_DTCAttribute.dpp`
- `Diamant_Update_FW_LINK_PRJ_DTC_REF.dpp`
- `Diamant_Update_DTC_ATTRIBUTES_CLASS_LINK.dpp`

Input Source
------------
Extract DTC information from **DEM_Requirements.md** file which contains:
- DTC Configuration Summary section
- Individual failure sections with DTC Configuration subsections
- DTC Attribute Configuration details

Output Files Overview
---------------------
**File 1: DTC_Input.txt** - DTC core entries
**File 2: DTCAttribute_Input.txt** - DTC Attribute configurations
**File 3: FW_DTC_Link_Input.txt** - Failure-to-DTC mappings
**File 4: DTC_Attr_Link_Input.txt** - DTC-to-Attribute mappings

-------------------------------------------------------------------------------

### File 1: DTC_Input.txt (DTC Core Entries)

**Purpose:** Creates DTC database entries with KEYLIST properties and AUTOSAR_DTC fields.

**Required Fields:**

| Field | Description | Example |
|-------|-------------|---------|
| DTC | Hex code | 0xFFFFAA |
| SHORT-NAME | DTC identifier | DTC_TBD_OBD_OtherCycle |
| DESC | Description | Dummy DTC OBD Trip1 |
| **CUSTOMER_REF** | **MANDATORY - Customer reference. Used by DiamantPro for XML routing.** | Cus_CHR |
| **PROJECT_REF** | **OPTIONAL - Project reference. Used by DiamantPro for XML routing.** | Prj_iPB or (empty) |
| **PRODUCT_LINE_REF** | **OPTIONAL - Product line. Used by DiamantPro for XML routing.** | IPB or (empty) |
| DtcSeverity | Severity level | DTC_SEV_IMMEDIATELY |
| WWHOBDDtcClass | WWHOBD class (DEFAULT) | DEM_DTC_WWHOBD_CLASS_NOCLASS |
| WarningIndicatorDeactTrigger | Warning indicator (DERIVED) | NO_INDICATOR or DEACT_TF |
| DemWWHOBDFreezeFrameClassRef | Freeze frame ref (can be empty) | (empty) |
| ENDRelevant | END relevance (DEFAULT) | false |
| OBDReadinessGroup | OBD readiness (DEFAULT) | NO_RDY_GRP |
| DTCTripInfo | Trip information (DEFAULT) | NON_OBD |
| OBDClassicDtcValue | OBD classic value (DEFAULT) | 0x0000 |
| DemRbAlternativeDTC | Alternative DTC (DEFAULT) | 0x000000 |
| OBDonUDSDtcValue | OBD on UDS value (DEFAULT) | 0x000000 |
| OBDonUDSReadinessGroup | OBD on UDS readiness (DEFAULT) | NO_RDY_GRP |
| ZEVonUDSDtcValue | ZEV on UDS value (DEFAULT) | 0x000000 |
| ZEVonUDSReadinessGroup | ZEV on UDS readiness (DEFAULT) | NO_RDY_GRP |

**Example Entry:**
```
DTC: 0xFFFFAA
SHORT-NAME: DTC_TBD_OBD_OtherCycle
DESC: Dummy DTC OBD Trip1
CUSTOMER_REF: Cus_CHR
PROJECT_REF: Prj_iPB
PRODUCT_LINE_REF: IPB
DtcSeverity: DTC_SEV_IMMEDIATELY
WWHOBDDtcClass: DEM_DTC_WWHOBD_CLASS_NOCLASS
WarningIndicatorDeactTrigger: DEACT_TF
DemWWHOBDFreezeFrameClassRef: 
ENDRelevant: false
OBDReadinessGroup: NO_RDY_GRP
DTCTripInfo: NON_OBD
OBDClassicDtcValue: 0x0000
DemRbAlternativeDTC: 0x000000
OBDonUDSDtcValue: 0x000000
OBDonUDSReadinessGroup: NO_RDY_GRP
ZEVonUDSDtcValue: 0x000000
ZEVonUDSReadinessGroup: NO_RDY_GRP

```
(blank line separates entries)

-------------------------------------------------------------------------------

### File 2: DTCAttribute_Input.txt (DTC Attribute Configurations)

**Purpose:** Creates DtcAttribute database entries with all configuration parameters.

**Required Fields:**

| Field | Description | Example |
|-------|-------------|---------|
| SHORT-NAME | Attribute identifier | DTCAttribute_DTC_C055D62 |
| Description | Description | DTC Attribute for DTC_C055D62 |
| **CUSTOMER_REF** | **MANDATORY - Customer reference. Used by DiamantPro for XML routing.** | Cus_CHR |
| **PROJECT_REF** | **OPTIONAL - Project reference. Used by DiamantPro for XML routing.** | Prj_iPB or (empty) |
| **PRODUCT_LINE_REF** | **MANDATORY/OPTIONAL - Product line. Used by DiamantPro for XML routing.** | IPB |
| AgingAllowed | Aging allowed | true |
| AgingcyclecounterThreshold | Aging threshold | 40 |
| DemDTCPriority | DTC priority | 1 |
| EventFailurecyclecounterThreshold | Failure threshold | 1 |
| MaxNumberFreezeFrameRecords | Max freeze frames | 1 |
| AgingcycleRef | Aging cycle (LEAVE EMPTY - system auto-uses Operation Cycle from failure) | (empty) |
| ExtendedDataClassRef | Extended data class | ExtData_DemExtendedDataClass_RB_OBDonUDS |
| FreezeFrameClassRef | Freeze frame class | FFrame_DemFreezeFrameClass_RBAPLCUST |
| EventDestination | Event destination | DemPrimaryMemory |
| EventDestinationMirror | Mirror destination | None |
| DTCKinds | DTC kinds | DEM_DTC_KIND_EMISSION_REL_DTCS |

**Example Entry:**
```
SHORT-NAME: DTCAttribute_DTC_C055D62
Description: DTC Attribute for DTC_C055D62
CUSTOMER_REF: Cus_CHR
PROJECT_REF: 
PRODUCT_LINE_REF: IPB
AgingAllowed: true
AgingcyclecounterThreshold: 40
DemDTCPriority: 1
EventFailurecyclecounterThreshold: 1
MaxNumberFreezeFrameRecords: 1
AgingcycleRef: 
ExtendedDataClassRef: ExtData_DemExtendedDataClass_RB_OBDonUDS
FreezeFrameClassRef: FFrame_DemFreezeFrameClass_RBAPLCUST
EventDestination: DemPrimaryMemory
EventDestinationMirror: None
DTCKinds: DEM_DTC_KIND_EMISSION_REL_DTCS

```
(blank line separates entries)

-------------------------------------------------------------------------------

### File 3: FW_DTC_Link_Input.txt (Failure-to-DTC Links)

**Purpose:** Creates FW_LINK_PRJ_DTC_REF entries linking failures to DTCs.

**Required Fields:**

| Field | Description | Example |
|-------|-------------|---------|
| FW_REF | Failure name | FW_RBNet_Scl_CBC_PT3_AMB_TEMP_AVG_Invalid |
| DTC_REF | DTC name | DTC_TBD_OTHERCYCLE |

**Example Entry:**
```
FW_REF: FW_RBNet_Scl_CBC_PT3_AMB_TEMP_AVG_Invalid
DTC_REF: DTC_TBD_OTHERCYCLE

FW_REF: FW_HydraulicUndervoltage1
DTC_REF: DTC_123456

```
(blank line separates entries)

-------------------------------------------------------------------------------

### File 4: DTC_Attr_Link_Input.txt (DTC-to-Attribute Links)

**Purpose:** Creates DTC_ATTRIBUTES_CLASS_LINK entries linking DTCs to DTC Attributes.

**Required Fields:**

| Field | Description | Example |
|-------|-------------|---------|
| dtc_ref | DTC name | DTC_TBD_OBD_OtherCycle |
| DTCAttributesClassRef | DTC Attribute name | DTCAttribute_CHR_OBD |

**Example Entry:**
```
dtc_ref: DTC_TBD_OBD_OtherCycle
DTCAttributesClassRef: DTCAttribute_CHR_OBD

dtc_ref: DTC_123456
DTCAttributesClassRef: DTCAttribute_CHR_NonOBD

```
(blank line separates entries)

-------------------------------------------------------------------------------

Processing Logic
----------------
1. **Parse DEM_Requirements.md** – Extract DTC Configuration Summary and individual failure DTC configurations.
2. **Extract DTC entries** – From DTC Configuration Summary section, extract DTC code, name, and **KEYLIST fields (CUSTOMER_REF, PROJECT_REF, PRODUCT_LINE_REF)**. Generate File 1.
3. **Derive WarningIndicatorDeactTrigger** – Read "Warning Bit Indicator" from DEM_Requirements.md:
   - If "Warning Bit Indicator: True" → Set `WarningIndicatorDeactTrigger: DEACT_TF`
   - If "Warning Bit Indicator: False" → Set `WarningIndicatorDeactTrigger: NO_INDICATOR`
   - If not specified → Default to `NO_INDICATOR`
4. **Apply default values** – For fields not specified in DEM_Requirements.md, use these defaults:
   - `WWHOBDDtcClass: DEM_DTC_WWHOBD_CLASS_NOCLASS`
   - `DemWWHOBDFreezeFrameClassRef:` (empty)
   - `ENDRelevant: false`
   - `OBDReadinessGroup: NO_RDY_GRP`
   - `DTCTripInfo: NON_OBD`
   - `OBDClassicDtcValue: 0x0000`
   - `DemRbAlternativeDTC: 0x000000` (do NOT derive from DTC value)
   - `OBDonUDSDtcValue: 0x000000`
   - `OBDonUDSReadinessGroup: NO_RDY_GRP`
   - `ZEVonUDSDtcValue: 0x000000`
   - `ZEVonUDSReadinessGroup: NO_RDY_GRP`
5. **Extract DTC Attributes** – From DTC Attribute Configuration sections, extract all 14 attribute parameters **and KEYLIST fields (CUSTOMER_REF, PROJECT_REF, PRODUCT_LINE_REF)**. Generate File 2.
   - **NOTE:** DTC Attribute KEYLIST values may differ from Failure KEYLIST values - extract them independently.
   - **CRITICAL:** `AgingcycleRef` should be LEFT EMPTY. The system automatically uses the Operation Cycle from the associated failure when this field is empty.
6. **Map Failures to DTCs** – From individual failure sections, extract failure name and DTC reference. Generate File 3.
   - **VALIDATION:** Verify all failures mapped to the same DTC have identical Operation Cycles. If different operation cycles map to same DTC, flag as ERROR.
7. **Map DTCs to Attributes** – From DTC Configuration Summary, extract DTC-to-Attribute relationships. Generate File 4.
8. **Validate completeness** – Ensure all referenced DTCs and Attributes exist in their respective files.
9. **Save files** – Write to workspace with naming convention: `DTC_Input.txt`, `DTCAttribute_Input.txt`, `FW_DTC_Link_Input.txt`, `DTC_Attr_Link_Input.txt`.

Agent Mode Behavior Summary
---------------------------
| Step | Agent Action |
|------|--------------|
| 1 | Read DEM_Requirements.md file |
| 2 | Parse DTC Configuration Summary section |
| 3 | Parse individual failure DTC Configuration sections |
| 4 | Extract unique DTCs with all KEYLIST fields → File 1 |
| 5 | Extract unique DTC Attributes with all 14 parameters → File 2 |
| 6 | Extract all Failure-to-DTC mappings → File 3 |
| 7 | Extract all DTC-to-Attribute mappings → File 4 |
| 8 | Validate cross-references between files |
| 9 | Save all 4 files to workspace |
| 10 | Log summary report (counts per file, warnings) |

Validation Checklist
--------------------
- All 4 files generated successfully
- Each DTC in File 1 has corresponding entry in File 4
- Each DTC Attribute in File 2 is referenced in File 4
- All failures in File 3 reference valid DTCs from File 1
- All DTCs in File 4 exist in File 1
- All DTC Attributes in File 4 exist in File 2
- Blank lines separate all entries
- No duplicate entries within each file
- All required fields present for each entry type

Error Handling
--------------
| Scenario | Agent Action |
|----------|--------------|
| DTC missing from DEM_Requirements.md | Log error, skip failure, add to missing list |
| DTC Attribute missing | Log warning, skip attribute link, add to missing list |
| Incomplete DTC configuration | Log warning, use defaults where possible, flag for review |
| Duplicate DTC codes | Log warning, use first occurrence, flag for review |
| Missing mandatory field | Log error, skip entry, add to error report |
| Invalid hex format for DTC | Log error, skip entry, add to error report

-------------------------------------------------------------------------------

## Final Notes

- When generating these files, adhere strictly to the normalization and sign conventions described above for debouncers, thresholds, and operation cycles.
- Preserve original source strings in `(source)` fields next to normalized fields for traceability.
- Save outputs to the configured workspace paths (for example: `GenFromCoPilot/splitter_input/` and `GenFromCoPilot/splitterOutput/`).

End of combined instruction file.

-------------------------------------------------------------------------------

## STM Configuration Generation – Instruction

This section provides guidance to generate an STM (State Machine) Configuration file that defines which nodes degrade which target states.

Objective
---------
To generate a standardized STM Configuration file (`Diamant_Generate_STMConfig.txt`) that maps diagnostic nodes to the target system states they degrade when failures occur.

Input Requirements
------------------
The following attributes must be extracted from the Requirements.md file:

| Attribute | Description |
|-----------|-------------|
| Node name | The unique identifier of the diagnostic node |
| Target states | List of system states/features that are degraded by this node, with their degradation levels |

Each target state entry should follow the format: `<FeatureName> = <State>`

Where:
- `<FeatureName>`: The system feature or function being degraded (e.g., ESPBase, AEB, HHC)
- `<State>`: The degradation state level (e.g., state, disabled, limited, degraded)

Output Format
-------------
The generated file must be a `.txt` file with the following structure:
- Each node entry starts with `Node name: <NodeName>`
- Followed by `Target states: <StateList>`
- Multiple target states are separated by semicolons (`;`)
- Each state follows the format `<FeatureName> = <State>`
- Node entries are separated by blank lines

Example Output Structure:
```
Node name: Node_VoltageHandler1
Target states: ESPBase = state; AEB = state

Node name: Node_HydraulicSupply
Target states: HHC = state; ESPBase = degraded

Node name: Node_BrakeSystem
Target states: ABS = disabled; ESC = limited; BrakeAssist = state
```

Processing Logic
----------------
1. **Parse input** – Read Requirements.md file and locate sections describing node-to-state-degradation mappings
   - Look for sections titled "STM Configuration", "State Degradation", "Target State Mapping", or similar
   - Extract node names and their associated target state degradations

2. **Extract node entries** – For each diagnostic node mentioned:
   - Identify the node name (must match node names from Node Splitter generation)
   - Extract all target states affected by the node
   - Parse state degradation levels

3. **Normalize state names** – Ensure consistency:
   - Trim whitespace from feature names and state values
   - Preserve original capitalization for feature names
   - Common state values: `state`, `disabled`, `limited`, `degraded`, `unavailable`, `off`

4. **Validate entries** – Ensure:
   - Each node name is unique
   - Each node has at least one target state
   - Target state format follows `<Feature> = <State>` pattern
   - Node names match those defined in Node Splitter file (cross-reference validation)

5. **Format output** – Structure the file:
   - Use `Node name:` prefix for each node entry
   - Use `Target states:` prefix for the state list
   - Separate multiple states with semicolon and space (`; `)
   - Add blank line between node entries

6. **Save file** – Write output to `GenFromCoPilot/splitter_input/Diamant_Generate_STMConfig.txt`

Input Source Parsing Guidelines
--------------------------------
When parsing Requirements.md, look for sections containing:
- Node degradation tables
- State transition mappings
- Functional safety degradation specifications
- Feature availability matrices
- Diagnostic response tables

Common section headers to search for:
- "STM Configuration"
- "State Degradation Mapping"
- "Target State Configuration"
- "Node Impact Analysis"
- "System State Degradation"
- "Feature Degradation Matrix"

Agent Mode Behavior Summary
---------------------------
| Step | Agent Action |
|------|--------------|
| 1 | Read Requirements.md file from workspace |
| 2 | Locate STM/state degradation sections |
| 3 | Extract node names and their target state impacts |
| 4 | Parse each node's target states in `Feature = State` format |
| 5 | Validate node names against Node Splitter file (optional) |
| 6 | Format entries with proper syntax and blank-line separation |
| 7 | Save as `GenFromCoPilot/splitter_input/Diamant_Generate_STMConfig.txt` |
| 8 | Log summary (node count, total target states, warnings) |

Example Entries
---------------

### Simple Entry (Single Target State)
```
Node name: Node_CoolantTemp
Target states: EngineProtection = state
```

### Multiple Target States
```
Node name: Node_VoltageHandler1
Target states: ESPBase = state; AEB = state; ADAS = limited
```

### Complex Degradation Scenario
```
Node name: Node_BrakePressureSensor
Target states: ABS = disabled; ESC = degraded; BrakeAssist = unavailable; HillHoldControl = off
```

Validation Rules
----------------
1. **Node name validation:**
   - Must not be empty
   - Should match pattern `Node_*` (recommended)
   - Must be unique within the file

2. **Target states validation:**
   - At least one target state required per node
   - Each state must follow `<Feature> = <State>` format
   - Feature names must not contain `=` or `;` characters
   - State values are case-sensitive

3. **Format validation:**
   - Entries must be separated by blank lines
   - Use `: ` (colon-space) after `Node name` and `Target states`
   - Use `; ` (semicolon-space) between multiple target states

Error Handling
--------------
| Scenario | Agent Action |
|----------|--------------|
| Node name missing | Log error, skip entry, add to error report |
| No target states found | Log error, skip entry, mark as incomplete |
| Invalid state format | Log warning, attempt to parse, flag for review |
| Duplicate node name | Log warning, merge target states or use first occurrence |
| Node not in Node Splitter | Log warning, include in output but flag for validation |
| Malformed Requirements.md | Log error, request clarification on section structure |

Cross-File Validation (Optional)
---------------------------------
When generating STM Configuration, optionally validate against other splitter files:

1. **Node Splitter cross-reference:**
   - Verify all nodes in STM Config exist in Node Splitter file
   - Log warnings for orphaned nodes

2. **Consistency check:**
   - Ensure node naming conventions match across files
   - Verify that critical nodes have STM configurations

Output File Location
--------------------
**Path:** `GenFromCoPilot/splitter_input/Diamant_Generate_STMConfig.txt`

**File structure:**
- Plain text file (.txt)
- UTF-8 encoding
- Windows line endings (CRLF)
- Blank line separated entries

Notes
-----
- STM Configuration defines system-level functional degradation behavior
- Target state assignments determine which features become unavailable when a node's failures are active
- Multiple nodes can degrade the same target state with different severity levels
- State values should align with system architecture definitions
- This configuration is typically used by State Manager components in the ECU software

Example Complete File
---------------------
```
Node name: Node_VoltageHandler1
Target states: ESPBase = state; AEB = state

Node name: Node_HydraulicSupply
Target states: HHC = state; BrakeAssist = degraded

Node name: Node_BrakePressureSensor
Target states: ABS = disabled; ESC = limited

Node name: Node_SteeringAngleSensor
Target states: LaneKeepAssist = unavailable; ADAS = degraded; ESPBase = limited

Node name: Node_CoolantTempSensor
Target states: EngineProtection = state; PerformanceMode = disabled
```

-------------------------------------------------------------------------------
