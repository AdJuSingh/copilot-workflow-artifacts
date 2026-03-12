# Instruction 0: Create DEM Failure Analysis (DEM_Requirements.md)

## OPERATIONAL MODES

### Mode 1: Complete Document Analysis (Default)
**When to Use**: User does not specify particular failure names in the prompt

**Behavior**:
- Parse the ENTIRE Requirements.csv document (all lines)
- **Filter for failure information ONLY**: Ignore non-failure content such as:
  - Document headers, reviews, section descriptions
  - Signal descriptions without associated failure definitions
  - Navigation/structure elements
  - Any row without "FailureWord:" or "Failure name:" identifier
- Extract ALL failures found in the document
- **FILTER FOR FAILURES ONLY**: Document ONLY failure information, ignore all other content (headers, reviews, signals without failures, navigation elements, etc.)
- For each failure, check for ALL mandatory and optional parameters per the instruction template
- **CRITICAL VALIDATION**: If ANY mandatory field is missing (Failure Name, Node Name, Priority, Operation Cycle, Debouncer Type, etc.), document the missing fields in a dedicated section within DEM_Requirements.md
- **NO ASSUMPTIONS ALLOWED**: Do not infer, assume, or generate any missing data
- **ALWAYS Generate DEM_Requirements.md**: Even if mandatory fields are missing, generate the file with:
  - Complete information for failures with all mandatory fields
  - Partial information for failures with missing mandatory fields
  - Missing fields documented at the end of each individual failure (not in a separate upfront section)

### Mode 2: Specific Failure Analysis
**When to Use**: User explicitly mentions one or more failure names in the prompt

**Behavior**:
- Search Requirements.csv for ONLY the specifically mentioned failure(s)
- Examples of user prompts that trigger this mode:
  - "Analyze FW_RBNet_Scl_CBC_PT1_IGN_OFF_TIME_LNG_Invalid"
  - "Generate DEM requirements for RBNet_ComScl_CBC_PT1_Timeout and RBNet_ComScl_CBC_PT2_TimeOut"
  - "Extract failure RBNet_ComScl_CBC_PT1_DataCorrupt"
- Extract information ONLY for the named failure(s)
- **FILTER FOR FAILURES ONLY**: Document ONLY the specified failure(s), ignore all other content
- For each specified failure, check for ALL mandatory and optional parameters
- **CRITICAL VALIDATION**: If ANY mandatory field is missing, document the missing fields in a dedicated section within DEM_Requirements.md
- **NO ASSUMPTIONS ALLOWED**: Do not infer, assume, or generate any missing data
- **ALWAYS Generate DEM_Requirements.md**: Even if mandatory fields are missing, generate the file with missing information clearly documented

### Failure Identification Patterns
A requirement row is considered a **failure** if it contains ANY of these patterns:
- "FailureWord:" followed by failure name
- "Failure name :" followed by failure name
- "General Requirements to FW_" followed by failure name

**Non-Failure Content to Ignore**:
- Rows with CP_Status_RB = "no_req" and MS_Status_RB = "no_req"
- Section headers (e.g., "3.1.2.1 Requirements Related to Required Interfaces")
- Signal descriptions without failure definitions (e.g., "Signal: IGN_OFF_TIME_LNG" without subsequent failure details)
- Review information, templates, checklists

## CRITICAL: DEM FAILURE ANALYSIS FORMAT & STANDARDS
- The analysis must be implemented as a `.md` text file, based strictly on the requirements in `GenFromCoPilot/requirements/Requirements.csv`.
- Extract only available information from requirements - do not assume or elaborate.
- **The accepted output is `GenFromCoPilot/requirements/DEM_Requirements.md`**.
- **CRITICAL FILE PLACEMENT**: All requirement analysis files must be placed in the `requirements/` folder.

## ESSENTIAL PARAMETERS TO EXTRACT
Extract only the following parameters from Requirements.csv:

### MANDATORY FIELDS (Cannot Proceed Without These)
The following fields are MANDATORY for each failure. If ANY of these are missing, analysis MUST STOP with error report:

#### Core Mandatory Fields
- **Failure Name**: Unique identifier for the failure (e.g., FW_RBNet_Scl_CBC_PT1_IGN_OFF_TIME_LNG_Invalid)
- **Node Name**: Node where failure belongs (e.g., Node_Ign_OffTime_Scl)
- **Parent Node**: Parent node reference in hierarchy (e.g., Node_ComScl_CBC_PT1)
- **Priority**: Failure priority within the node (e.g., 100, 90, 80)

#### Monitoring Mandatory Fields
- **System Strategy**: System strategy information (e.g., ESPBase_AbsOnWithPMc, Master controller : EspExtendedTcsExtended)
- **Debouncer Type**: CounterBased or MonitoringInternal (refer to 0_Debouncer_Configuration.md)
- **Operation Cycle**: Operation cycle reference (e.g., Power cycle, Ignition cycle)

#### Debouncer-Specific Mandatory Fields
**If Debouncer Type = CounterBased**, the following are also MANDATORY:
- **Detection Time**: Time threshold for failure detection (e.g., 1000ms)
- **Recovery Time**: Time threshold for failure recovery (e.g., 500ms)
- **Task Cycle**: Monitoring task cycle time (e.g., 10ms)

#### Operational Mandatory Fields
- **Curable in Current Operation Cycle**: Yes/No - Whether failure can be cured within same operation cycle
- **Restore Event to Next OC**: Yes/No - Whether testfailed bit updates to next operation cycle

#### DTC Mandatory Fields
- **DTC**: Diagnostic Trouble Code (can be "TBD" if pending assignment)
- **DTC Description**: Description of the DTC

**CRITICAL BEHAVIOR**: If any mandatory field is missing:
1. Continue processing all failures (do NOT stop)
2. Extract all available information for each failure
3. Document the missing field(s) with failure name in "❌ Missing Mandatory Information" section
4. ALWAYS generate DEM_Requirements.md with complete and partial failure information
5. Include clear warnings about which failures cannot proceed to implementation phase due to missing mandatory fields

### OPTIONAL FIELDS (Can Proceed Without These)

### Core Failure Information
- **Failure Name**: From requirements
- **DTC**: Diagnostic Trouble Code
- **DTC Description**: Description of the DTC
- **Node Name**: Node where failure belongs
- **Parent Node**: Parent node reference

### KEYLIST Information (for DiamantPro XML routing)
- **Customer**: MANDATORY - Customer reference (e.g., Cus_RB, Cus_CHR)
- **Project**: OPTIONAL - Project reference (e.g., Prj_iPB)
- **Software Group**: OPTIONAL - Software group reference
- **Product Line**: OPTIONAL - Product line reference (e.g., IPB)

**CRITICAL**: If Customer information is not provided in Requirements.csv:
- DEFAULT to `Cus_RB`
- Add a warning in the DEM_Requirements.md file in a "⚠️ Configuration Warnings" section at the end
- Warning format: "⚠️ Customer information not provided for failure [FailureName] - defaulted to Cus_RB"

**NOTE**: These KEYLIST values are used by DiamantPro to determine which XML file to write the FAILURE_WORD to. Without proper values, the failure cannot be persisted to the database.

### Failure Descriptions (Derived from Requirements.csv)
- **Description**: Extract one-sentence description from failure set/reset conditions
- **Rootcause**: Derive potential error sources from failure conditions (only what's mentioned)
- **Algorithm Description**: Extract monitoring algorithm details from failure set/reset conditions text
- **Good Check Description**: Extract reset/recovery maneuver from failure conditions text

**CRITICAL**: All descriptions must be derived only from the "failure set and reset conditions" text in Requirements.csv. Do not add information not explicitly mentioned in the requirements.

### Additional Optional Fields
The following fields should be extracted if present, but their absence does not block DEM_Requirements.md generation:

#### KEYLIST Information (for DiamantPro XML routing)
- **Customer**: Can default to `Cus_RB` if not provided (add warning)
- **Project**: OPTIONAL - Project reference (e.g., Prj_iPB)
- **Software Group**: OPTIONAL - Software group reference
- **Product Line**: OPTIONAL - Product line reference (e.g., IPB)

#### Monitoring Configuration (Optional)
- **Good Check Description**: Maneuver necessary to reset monitoring state (extract from conditions if available)
- **Enable Condition**: Enable condition information
- **Warning Bit Indicator**: True/False - Whether warning bit is set

#### Additional Requirements Information (Optional)
- **VariantCode**: Variant-specific code
- **SituationFilter**: Situation filter information
- **OBD Relevance**: OBD relevance classification (e.g., RELEVANT_1_TRIP_FAULT)
- **Lamp Information**: Lamp status information (e.g., ABS = OFF, EBD = OFF, VDC = ON)
- **DTC Severity**: Severity level (e.g., Check Immediately)
- **Failure Reset Type**: Reset type (e.g., Permanent failure)
- **Import from ASCET**: Yes/No
- **Export to ASCET**: Yes/No

### DTC Attribute KEYLIST Information
**CRITICAL**: DTC Attributes have their OWN separate KEYLIST values (independent from Failure KEYLIST)
- **DTC Attribute Customer**: MANDATORY - Customer reference for DTC Attribute (may differ from Failure Customer)
- **DTC Attribute Project**: OPTIONAL - Project reference for DTC Attribute (may differ from Failure Project)
- **DTC Attribute Software Group**: OPTIONAL - Software group for DTC Attribute
- **DTC Attribute Product Line**: OPTIONAL - Product line for DTC Attribute

**CRITICAL VALIDATION**: DTC Operation Cycle Consistency
- **All failures sharing the same DTC value MUST have identical Operation Cycles**
- If multiple failures with different operation cycles are mapped to the same DTC, this is an **ERROR** that must be flagged in the DEM_Requirements.md
- Add validation error in "⚠️ Configuration Warnings" section with format: "❌ ERROR: DTC [DTCValue] is shared by failures with different Operation Cycles: [List failures with their operation cycles]. Each DTC must have a consistent operation cycle across all associated failures."
- User must either: (1) Create separate DTCs for each operation cycle, or (2) Align all failures to use the same operation cycle

**DTC Attribute AgingcycleRef Handling**:
- **AgingcycleRef should be LEFT EMPTY in DTC Attribute configurations**
- When AgingcycleRef is empty, the system automatically uses the Operation Cycle from the associated failure
- This allows the same DTC Attribute to be used with different DTCs that may have different operation cycles

**CRITICAL**: If DTC Attribute Customer information is not provided in Requirements.csv:
- DEFAULT to `Cus_RB`
- Add a warning in the DEM_Requirements.md file in the "⚠️ Configuration Warnings" section
- Warning format: "⚠️ DTC Attribute Customer information not provided for [DTCAttributeName] - defaulted to Cus_RB"

**NOTE**: DTC Attribute KEYLIST values can be completely different from the associated Failure KEYLIST values. They are used separately for routing DTC Attribute objects to appropriate XML files.

### Additional Requirements.csv Information
- All other fields present in Requirements.csv must be included in analysis

## MANDATORY FIELD VALIDATION & REPORTING

### When Mandatory Fields Are Missing
If ANY mandatory field is missing for ANY failure (in either Mode 1 or Mode 2), you MUST:

1. **Continue processing** - Do NOT stop, process all failures
2. **Extract all available information** for each failure regardless of missing fields
3. **Document missing fields** at the end of each individual failure in the "⚠️ Missing Mandatory Fields" section
4. **Generate DEM_Requirements.md** always, with complete and incomplete failure data
5. **Group failures by Node** as specified in Requirements.csv

### Per-Failure Missing Fields Format
**For each failure with missing mandatory fields, include this section after "Additional Information":**

### Per-Failure Missing Fields Format
**For each failure with missing mandatory fields, include this section after "Additional Information":**

```markdown
#### ⚠️ Missing Mandatory Fields
| Missing Parameter | Required For | Status |
|-------------------|--------------|--------|
| Operation Cycle | Failure lifecycle management | ❌ MISSING |
| Debouncer Type | Monitoring algorithm selection | ❌ MISSING |

#### Implementation Status
❌ BLOCKED - Cannot proceed to implementation until missing mandatory fields are provided
```

**For failures with all mandatory fields present:**

```markdown
#### ⚠️ Missing Mandatory Fields
N/A - All mandatory fields present

#### Implementation Status
✅ READY - All mandatory fields present, ready for implementation phase
```

**CRITICAL CLARIFICATION - What Counts as "Missing Mandatory Fields":**
- **ONLY** list fields from the "MANDATORY FIELDS" section above (lines 63-93)
- **DO NOT** list optional fields (OBD Relevance, Lamp Information, Failure Reset Type, Export2ASCET, etc.) as missing
- **Optional fields** should be captured in "Additional Information" section with "Not specified" if absent
- **KEYLIST optional fields** (Project, Software Group, Product Line) are NOT mandatory - their absence does NOT block ✅ READY status
- **Customer field**: If missing, default to "Cus_RB" and add warning to Configuration Warnings section (NOT a blocking error)

**Status Determination Rules:**
- ✅ READY: All 11-14 mandatory fields present (even if optional fields or KEYLIST optional fields are missing)
- ❌ BLOCKED: One or more mandatory fields from lines 63-93 are missing

## ANALYSIS REQUIREMENTS
- Read and parse all requirements from `Requirements.csv`.
- **STM Configuration Analysis**: Follow 0_STM_Configuration_Analysis.md for STM-specific analysis requirements.
- **Node Configuration**: Follow 0_Node_Priority_Configuration.md completely for all node-related structure, validation, and priority management.
- **Extract Only Available Information**: Do not assume or elaborate on missing information.
- **Request User Input**: For missing mandatory fields not in requirements.
- **No Assumptions**: If information is missing, explicitly request from user.
- **Debouncing**: Follow 0_Debouncer_Configuration.md for debouncer type handling.
- **Category**: Use 0_BFM_Category_Reference.md for failure category selection.
- **Complete Extraction**: Include all fields present in Requirements.csv.
- **Structure**: Start with Node information (per 0_Node_Priority_Configuration.md), then list all failures within that node.
- Add version, author, and change history for traceability.

## Output File Template
```markdown
# DEM Failure Analysis

<!-- Version: <version> | Author: <author> | Change History: <history> -->
<!-- Reviewer/Approver: <name(s)>, <date(s)> -->

## Node: <Node_Name>

### Node Configuration (Follow 0_Node_Priority_Configuration.md template exactly)
*Refer to 0_Node_Priority_Configuration.md for complete node structure, validation rules, and priority management*

### Failure: <Failure_Name> ⚠️ **<If_Missing_Mandatory_Fields_Add_This_Warning_Indicator>**

**Note**: Add ⚠️ indicator in failure heading if ANY mandatory field is missing for this failure.

#### Core Information
| Parameter | Value |
|-----------|--------|
| **Failure Name** | <From_requirements> |
| **DTC** | <DTC_code> |
| **DTC Description** | <DTC_description> |
| **Node Name** | <Node_name> |
| **Parent Node** | <Parent_node> |

#### KEYLIST Configuration
| Parameter | Value |
|-----------|--------|
| **Customer** | <Cus_XXX (MANDATORY, default: Cus_RB if not provided)> |
| **Project** | <Prj_XXX (OPTIONAL)> |
| **Software Group** | <SW_GROUP_XXX (OPTIONAL)> |
| **Product Line** | <PRODUCT_LINE (OPTIONAL)> |

#### Descriptions (Extracted from Failure Conditions)
| Parameter | Value |
|-----------|--------|
| **Description** | <Extract_one_sentence_from_failure_set_reset_conditions> |
| **Rootcause** | <Extract_error_sources_mentioned_in_failure_conditions> |
| **Algorithm Description** | <Extract_monitoring_algorithm_from_failure_conditions> |
| **Good Check Description** | <Extract_reset_maneuver_from_failure_conditions> |

#### Monitoring Configuration
| Parameter | Value |
|-----------|--------|
| **Good Check Description** | <Reset_maneuver_description> |
| **System Strategy** | <System_strategy> |
| **Debouncer Type** | <CounterBased_or_MonitoringInternal> |

#### Operational Parameters
| Parameter | Value |
|-----------|--------|
| **Curable** | <Curable_in_same_operation_cycle> |
| **Restore Event to Next OC** | <Testfailed_bit_next_OC> |

#### Additional Requirements Information
| Parameter | Value |
|-----------|--------|
| <All_other_fields_from_Requirements.csv> | <Values_from_requirements> |

#### Debouncer Analysis (per 0_Debouncer_Configuration.md)
**CRITICAL: Consult 0_Debouncer_Configuration.md for complete debouncer analysis**
| Parameter | Value/Analysis |
|-----------|----------------|
| **Debouncer Type** | <CounterBased or MonitoringInternal> |
| **Debouncer Validation** | <Analysis from 0_Debouncer_Configuration.md> |
| **Configuration Completeness** | <Check all required parameters present per type> |

#### Node Priority Analysis (per 0_Node_Priority_Configuration.md)
**CRITICAL: Consult 0_Node_Priority_Configuration.md for node structure validation**
| Parameter | Value/Analysis |
|-----------|----------------|
| **Priority within Node** | <priority_value> |
| **Priority Validation** | <Validate no conflicts, check range per 0_Node_Priority_Configuration.md> |
| **System Strategy Validation** | <Check against allowed values per node configuration> |

#### STM Configuration Analysis (per 0_STM_Configuration_Analysis.md)
**CRITICAL: System Strategy IS the STM Configuration**
- The "System Strategy" field from Requirements.csv contains the STM (State Transition Matrix) configuration
- Parse the System Strategy value to extract TargetStates and their degradation states
- Follow 0_STM_Configuration_Analysis.md parsing rules for extraction

| Parameter | Value/Analysis |
|-----------|----------------|
| **System Strategy (STM Configuration)** | <Extract System Strategy value from requirements> |
| **STM State Degradation** | <Parse TargetStates from System Strategy per 0_STM_Configuration_Analysis.md> |
| **Target States** | <List all TargetStates with their degradation levels (e.g., ESPBase → EbdPumpless, AEB → Off)> |
| **STM Parsing Validation** | <✅ Successfully parsed or ❌ Invalid format> |

#### DTC Configuration Analysis
| Parameter | Value/Analysis |
|-----------|----------------|
| **DTC Code** | <DTC_value> |
| **DTC Shared with Other Failures** | <List other failures sharing same DTC> |
| **Operation Cycle Consistency** | <✅ CONSISTENT or ❌ INCONSISTENT across failures sharing this DTC> |
| **DTC Attribute Configuration** | <Link to DTC Attribute if applicable> |

#### BFM Category Analysis (per 0_BFM_Category_Reference.md)
**CRITICAL: Consult 0_BFM_Category_Reference.md for category selection**
| Parameter | Value/Analysis |
|-----------|----------------|
| **BFM Category** | <Category per 0_BFM_Category_Reference.md> |
| **Category Justification** | <Why this category based on failure characteristics> |
| **Category Validation** | <Verify category matches failure type and behavior> |

#### ⚠️ Missing Mandatory Fields (If Any)
**If this failure has missing mandatory fields, list them here:**
| Missing Parameter | Required For | Status |
|-------------------|--------------|--------|
| <Parameter_Name> | <Reason_Required> | ❌ MISSING |

**Implementation Status**: 
- ❌ BLOCKED - Cannot proceed to implementation until missing mandatory fields are provided
- OR ✅ READY - All mandatory fields present

#### Category Information
| Parameter | Value |
|-----------|--------|
| **Category** | <BFM_Category> |
| **Category Justification** | <Brief_reasoning> |

## DTC Attribute Configuration: <DTCAttributeName>

### DTC Attribute KEYLIST Configuration
| Parameter | Value |
|-----------|--------|
| **DTC Attribute Customer** | <Cus_XXX (MANDATORY, default: Cus_RB if not provided)> |
| **DTC Attribute Project** | <Prj_XXX (OPTIONAL)> |
| **DTC Attribute Software Group** | <SW_GROUP_XXX (OPTIONAL)> |
| **DTC Attribute Product Line** | <PRODUCT_LINE (OPTIONAL)> |

### DTC Attribute Information
<All DTC Attribute parameters from Requirements.csv>

---

## ⚠️ Configuration Warnings

**Missing Customer Information:**
- <List all failures/DTC attributes with missing customer info that defaulted to Cus_RB>

**DTC Operation Cycle Inconsistencies:**
- <List any DTCs shared by failures with different operation cycles - THIS IS AN ERROR>

**Example:**
- ⚠️ Customer information not provided for failure FW_HydraulicUndervoltage1 - defaulted to Cus_RB
- ⚠️ DTC Attribute Customer information not provided for DTCAttribute_CHR_NonOBD - defaulted to Cus_RB
- ❌ ERROR: DTC 0x123456 is shared by failures with different Operation Cycles: FW_Failure1 (PowerCycle), FW_Failure2 (WarmUp). Each DTC must have a consistent operation cycle across all associated failures.

---

#### Missing Information Requests
| Parameter | Request from User |
|-----------|-------------------|
| <List_missing_fields> | <Request_description> |

...repeat for each failure...
```

# ANALYSIS WORKFLOW

**Step 0: Determine Operational Mode**
- Check if user has explicitly mentioned specific failure name(s) in the prompt
- If YES → Mode 2 (Specific Failure Analysis): Extract only the mentioned failure(s)
- If NO → Mode 1 (Complete Document Analysis): Parse entire document, filter for failure information only

**Processing Steps:**
1. **Apply 0_Node_Priority_Configuration.md completely**: Extract node information, validate system strategy, manage priorities
2. **Parse Requirements.csv**:
   - Mode 1: Parse entire document, identify all failures (ignore non-failure content)
   - Mode 2: Search for specifically mentioned failure(s) only
3. **Extract KEYLIST information**: Customer (mandatory, default Cus_RB), Project, Software Group, Product Line for each failure
4. **Extract DTC Attribute KEYLIST**: Separate Customer/Project/Software Group/Product Line for DTC Attributes (independent from failure values)
5. **Validate Mandatory Fields**: Check if ALL required fields are present for each failure
   - If ANY mandatory field is missing → Document in "❌ Missing Mandatory Information" section
   - Mark failure with ⚠️ WARNING indicator in the detailed analysis
   - ALWAYS generate DEM_Requirements.md with both complete and incomplete failures documented
6. **Perform Debouncer Analysis** per 0_Debouncer_Configuration.md:
   - Determine debouncer type (CounterBased or MonitoringInternal)
   - Validate all required parameters for the debouncer type
   - Check timing parameters (Detection Time, Recovery Time, Task Cycle for CounterBased)
   - Verify debouncer configuration completeness
7. **Perform Node Priority Analysis** per 0_Node_Priority_Configuration.md:
   - Validate priority values within node (no conflicts, valid range)
   - Check system strategy against allowed values
   - Verify node hierarchy (parent-child relationships)
   - Validate failure priority ordering within node
8. **Perform STM Configuration Analysis** per 0_STM_Configuration_Analysis.md:
   - Extract STM state degradation configuration if present
   - Validate state transition matrix configuration
   - Check target states for each failure
   - Verify STM_NODE linkages
9. **Perform DTC Analysis**:
   - Validate DTC code format
   - Identify all failures sharing same DTC
   - **CRITICAL**: Verify operation cycle consistency across failures sharing same DTC (flag ERROR if inconsistent)
   - Check DTC Attribute configuration
   - Validate DTC-to-Failure linkages
10. **Perform BFM Category Analysis** per 0_BFM_Category_Reference.md:
   - Determine appropriate BFM category for each failure
   - Provide justification for category selection
   - Validate category matches failure type and behavior
11. Group failures by Node based on 0_Node_Priority_Configuration.md
12. Extract all available parameters (no assumptions)
13. Identify missing information and request from user
14. **Add Configuration Warnings section**: List all failures/DTC attributes with missing customer info that defaulted to Cus_RB, and any DTC operation cycle inconsistencies
15. Create structured analysis per template (Node first, then failures)

## Reference Files
- **0_BFM_Category_Reference.md**: For failure category selection
- **0_Debouncer_Configuration.md**: For debouncer type configuration
- **0_Node_Priority_Configuration.md**: For node grouping and failure priority management

## Copilot No-Assumption Checklist
**CRITICAL: Never assume missing information - Always request from user**

- [ ] ✅ **Debouncer Type**: If not explicitly specified in Requirements.csv, request from user - do NOT assume based on timing parameters
- [ ] ✅ **Missing Core Fields**: If Failure Name, DTC, Node Name, etc. are missing, explicitly request from user
- [ ] ✅ **Derive from Available Text**: Extract Description, Rootcause, Algorithm Description, Good Check Description from "failure set and reset conditions" text in Requirements.csv - do NOT add information not present in the requirements
- [ ] ✅ **No Invention**: Only use information explicitly stated in Requirements.csv failure conditions - do NOT create or assume details not mentioned
- [ ] ✅ **Missing Configuration**: If System Strategy or other configuration fields are missing, request from user
- [ ] ✅ **Missing Operational Parameters**: If Curable or Restore Event to Next OC are missing, request from user
- [ ] ✅ **Task Cycle for Counter-Based**: If Debouncer Type is CounterBased but Task Cycle is missing, request from user
- [ ] ✅ **Detection/Recovery Times**: If CounterBased debouncer but timing parameters missing, request from user
- [ ] ✅ **Customer References**: If Customer field is missing in Requirements.csv, default to `Cus_RB` and add warning to end of document
- [ ] ✅ **DTC Attribute Customer**: If DTC Attribute Customer field is missing, default to `Cus_RB` and add warning to end of document
- [ ] ✅ **KEYLIST Completeness**: Extract Project, Software Group, Product Line if provided; leave empty if not in Requirements.csv
- [ ] ✅ **Node KEYLIST**: Node objects should inherit the same Customer/Project/Software Group/Product Line as their failures (or use most common values if failures differ)
- [ ] ✅ **DTC Operation Cycle Validation**: Verify all failures sharing the same DTC value have identical Operation Cycles. Flag as ERROR if inconsistent.
- [ ] ✅ **No Default Values**: Do not provide default values for any missing fields except Customer (Cus_RB) - always request user input for other fields
- [ ] ✅ **No Elaboration**: Do not expand on brief descriptions - use exactly what's in Requirements.csv
- [ ] ✅ **Clear Missing Requests**: Use clear format: "Parameter [X] not found in Requirements.csv. Please provide: [specific request]"
- [ ] ✅ **Status Tracking**: Mark each parameter as either "From Requirements.csv" or "Requested from user"
- [ ] ✅ **Node Configuration Compliance**: Follow ALL rules in 0_Node_Priority_Configuration.md (system strategy validation, priority management, node structure)

## Quality Checklist
- [ ] All available parameters extracted from Requirements.csv
- [ ] Missing information clearly identified and requested from user
- [ ] Debouncer type handling per 0_Debouncer_Configuration.md
- [ ] Category selection per 0_BFM_Category_Reference.md
- [ ] Node priority configuration per 0_Node_Priority_Configuration.md
- [ ] DTC operation cycle consistency validated (all failures per DTC must have same operation cycle)
- [ ] No assumptions made about missing data
- [ ] All Requirements.csv fields included in analysis

