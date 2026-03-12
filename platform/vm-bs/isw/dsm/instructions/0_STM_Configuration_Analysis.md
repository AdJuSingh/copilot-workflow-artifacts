# Instruction 0: STM Configuration Analysis

## OVERVIEW: SYSTEM STATE MANAGEMENT (STM)

System State Management (STM) is a centralized mechanism that defines, monitors, and controls all system states in a structured and hierarchical manner. It evaluates system health by continuously checking signal availability and diagnostic information, and determines the highest possible functional state that can be safely achieved.

### Key Concepts

**System State Calculator (SSC)**
- Computes the target system state by combining three factors:
  1. Degradation caused by unusable or invalid signals
  2. Artificial state limitations applied through external limiters
  3. Master-system dependencies (for slave systems)
- Each signal or node is mapped to a predefined shutdown strategy
- In case of multiple failures, the system degrades to the lowest functional state with the highest safety priority
- Records detailed degradation reasons for clear diagnosis

**TargetState**
- Each state in STM is called a **TargetState**
- Examples: ESPBase, AEB, HHC, HBA, etc.
- TargetStates can be degraded to specific functional levels based on failure conditions

**Master-Slave Architecture**
- STM supports master–slave system architectures
- **Master System**: ESPBase (primary system that controls overall functional state)
- **Slave Systems**: AEB, HHC, HBA, and other TargetStates (depend on master system state)
- Slave systems depend on both their own signal requirements and the current state of the master system
- **Dependency Rule**: Slave systems can only be active (ON) if the master system is in a sufficiently high functional state
- **Example Dependency**: AEB can only be ON when ESPBase is at least ESPOnTcsExtended or higher
- **Degradation Impact**: When ESPBase is degraded to a lower state (e.g., EbdPumpless), slave systems that require higher master states must be OFF or degraded accordingly

**Scheduler and System Mode Manager**
- Ensure controlled and deterministic transitions between system states and modes
- State transitions are handshake-based
- Components confirm reaching their target states before further integration proceeds
- Handles multiple mode requests (e.g., Normal, NetOn, Off) through a defined state machine

## CRITICAL: STM ANALYSIS FORMAT & STANDARDS

- The STM analysis must be extracted from the **System strategy** field in `GenFromCoPilot/requirements/Requirements.csv`
- Extract only available information from requirements - do not assume or elaborate
- **The accepted output is included within `GenFromCoPilot/requirements/DEM_Requirements.md`** as part of the failure analysis
- All STM configurations must be validated and formatted consistently

## ESSENTIAL PARAMETERS TO EXTRACT

### System Strategy Field
The **System strategy** field in Requirements.csv defines which TargetStates should be degraded when a failure occurs.

**Field Format Examples:**
- `ESPBase_EbdPumpless`
- `ESPBase_EbdPumpless, AEB_Off, HHC = Off, TargetStateHBA = Off`
- `ESPBase_*, AEB_*, HHC_*`

### Parsing Rules

**Rule 1: Single TargetState Degradation**
- If System Strategy contains only one TargetState (e.g., `ESPBase_*` or `ESPBase_EbdPumpless`)
- Then ONLY that TargetState should be degraded
- Example: `ESPBase_EbdPumpless` → Only ESPBase degrades to EbdPumpless state

**Rule 2: Multiple TargetState Degradation**
- If System Strategy contains multiple TargetStates (e.g., `ESPBase_*, AEB_*, HHC_*`)
- Then ALL mentioned TargetStates should be degraded to their respective states
- Example: `ESPBase_EbdPumpless, AEB_Off, HHC = Off` → Three TargetStates degrade:
  - ESPBase → EbdPumpless
  - AEB → Off
  - HHC → Off

**Rule 3: Flexible Notation Support**
The System Strategy field may use different notations. Support all formats:
- Underscore notation: `ESPBase_EbdPumpless`
- Equal sign notation: `HHC = Off`
- Mixed notation: `ESPBase_EbdPumpless, HHC = Off`
- Explicit TargetState prefix: `TargetStateHBA = Off`

**Rule 4: TargetState Name Extraction**
- **First, extract the TargetState name** (before the underscore `_` or equal sign `=`)
- **If TargetState name starts with "TargetState" prefix**, strip this prefix to get the actual name
  - Example: `TargetStateAEB` → `AEB`
  - Example: `TargetStateHBA` → `HBA`
  - Example: `TargetStateESPBase` → `ESPBase`
- **Then, extract the state value** after the underscore `_` or equal sign `=`
- Remove extra spaces and normalize formatting
- If using asterisk `*` wildcard, specify "as defined in system strategy"

**Parsing Examples:**
- `AEB_Off` → TargetState: `AEB`, State: `Off`
- `AEB = Off` → TargetState: `AEB`, State: `Off`
- `TargetStateAEB = Off` → TargetState: `AEB`, State: `Off`
- `TargetStateHBA_Off` → TargetState: `HBA`, State: `Off`

## STM CONFIGURATION OUTPUT FORMAT

### Template 1: Single TargetState (Recommended Format)
```
**STM Configuration:**
- ESPBase = EbdPumpless
```

### Template 2: Multiple TargetStates (Recommended Format)
```
**STM Configuration:**
- ESPBase = EbdPumpless
- AEB = Off
- HHC = Off
- HBA = Off
```

### Template 3: Alternative Compact Format
```
**STM Configuration:**
ESPBase_EbdPumpless, AEB_Off, HHC_Off, HBA_Off
```

### Template 4: Detailed Format (For Complex Cases)
```
**STM Configuration:**
| TargetState | Degraded State | Description |
|-------------|----------------|-------------|
| ESPBase | EbdPumpless | ESP Base degraded to EBD Pumpless mode |
| AEB | Off | Autonomous Emergency Braking disabled |
| HHC | Off | Hill Hold Control disabled |
| HBA | Off | Hydraulic Brake Assist disabled |
```

## INTEGRATION WITH DEM REQUIREMENTS

The STM configuration should be included in the `DEM_Requirements.md` file as part of each failure's analysis.

**Recommended Placement:**
Add STM configuration in the **Monitoring Configuration** section:

```markdown
#### Monitoring Configuration
| Parameter | Value |
|-----------|--------|
| **Good Check Description** | <Reset_maneuver_description> |
| **System Strategy** | <Raw_system_strategy_from_csv> |
| **STM Configuration** | <Parsed_STM_configuration_per_templates> |
| **Debouncer Type** | <CounterBased_or_MonitoringInternal> |
```

## VALIDATION REQUIREMENTS

1. **Field Existence Check**
   - Verify that System strategy field exists in Requirements.csv
   - If missing, mark as "Not Specified" and request user input

2. **TargetState Identification**
   - Parse all TargetState names before underscore or equal sign
   - Validate that TargetState names are valid (ESPBase, AEB, HHC, HBA, etc.)
   - Flag unknown TargetState names for user review

3. **State Name Validation**
   - Extract state names (EbdPumpless, Off, etc.)
   - Validate that state names are meaningful and not malformed
   - Common states: Off, EbdPumpless, Degraded, Limited, etc.

4. **Consistency Check**
   - Ensure all failures within the same node have consistent STM configurations
   - Flag inconsistencies for user review

5. **Format Normalization**
   - Normalize all notation variations to consistent format
   - Remove extra spaces and punctuation
   - Use recommended format (Template 1 or 2) for output

6. **Master-Slave Dependency Validation**
   - **Master System Identification**: ESPBase is the master system
   - **Slave System Identification**: AEB, HHC, HBA, and other TargetStates are slave systems
   - **Dependency Rule Validation**: 
     - Slave systems have state dependencies on the master system state
     - Slave systems can only be in active/ON states if the master system is in a sufficiently high functional state
     - Example: AEB can be ON only when ESPBase is at least ESPOnTcsExtended or higher
   - **Inconsistency Detection**:
     - If ESPBase is degraded to a low state (e.g., EbdPumpless) AND a slave system is specified as ON or active state
     - This represents a logical inconsistency that must be flagged
   - **Validation Action**:
     - Parse both master (ESPBase) state and all slave system states
     - Check for incompatible combinations (e.g., ESPBase = EbdPumpless + AEB = ON)
     - Flag inconsistencies to user during analysis phase with clear explanation
     - Request user to verify and correct System Strategy in Requirements.csv
   - **Example Inconsistency**:
     ```
     ⚠️ STM Dependency Inconsistency Detected:
     - Master System: ESPBase = EbdPumpless (low degraded state)
     - Slave System: AEB = ON (active state)
     - Issue: AEB requires ESPBase to be at least ESPOnTcsExtended to be ON
     - Action Required: Please verify System Strategy in Requirements.csv
     ```
   - **Note**: Specific dependency rules (which master states are required for each slave state) will be documented in future updates to this instruction file

## ANALYSIS WORKFLOW

1. **Read Requirements.csv**
   - Parse all rows containing failure requirements
   - Identify System strategy column

2. **Extract System Strategy for Each Failure**
   - Read System strategy field value
   - Apply parsing rules (Rules 1-4)
   - Identify single vs multiple TargetState configurations

3. **Parse TargetStates and States**
   - Extract TargetState names (before `_` or `=`)
   - Extract state names (after `_` or `=`)
   - Handle all notation variations

4. **Format STM Configuration**
   - Apply recommended template format
   - Ensure consistency across all failures
   - Add validation notes if needed

5. **Integrate with DEM Requirements**
   - Add STM configuration to appropriate section
   - Maintain traceability to original System strategy field
   - Flag any anomalies or missing information

6. **Validate Master-Slave Dependencies**
   - Check for incompatible master-slave state combinations
   - Flag any dependency violations to user
   - Request clarification/correction of System Strategy if inconsistencies found

## EXAMPLES

### Example 1: Single TargetState
**Input (from Requirements.csv):**
```
System strategy: ESPBase_EbdPumpless
```

**Output (in DEM_Requirements.md):**
```markdown
**STM Configuration:**
- ESPBase = EbdPumpless
```

### Example 2: Multiple TargetStates with Mixed Notation (Valid)
**Input (from Requirements.csv):**
```
System strategy: ESPBase_EbdPumpless, AEB_Off, HHC = Off, TargetStateHBA = Off
```

**Output (in DEM_Requirements.md):**
```markdown
**STM Configuration:**
- ESPBase = EbdPumpless
- AEB = Off
- HHC = Off
- HBA = Off

✅ Master-Slave Dependency Validation: PASSED
- ESPBase in EbdPumpless (degraded state)
- All slave systems (AEB, HHC, HBA) properly set to Off
```

### Example 3: Master-Slave Dependency Inconsistency (Invalid)
**Input (from Requirements.csv):**
```
System strategy: ESPBase_EbdPumpless, AEB_ON, HHC = Off
```

**Output (in DEM_Requirements.md):**
```markdown
**STM Configuration:**
- ESPBase = EbdPumpless
- AEB = ON
- HHC = Off

⚠️ Master-Slave Dependency Inconsistency Detected:
- Master System: ESPBase = EbdPumpless (low degraded state)
- Slave System: AEB = ON (active state)
- Issue: AEB requires ESPBase to be at least ESPOnTcsExtended to be ON
- Recommendation: When ESPBase is degraded to EbdPumpless, AEB should be OFF
- Action Required: Please verify and correct System Strategy in Requirements.csv
```

### Example 4: Wildcard Notation
**Input (from Requirements.csv):**
```
System strategy: ESPBase_*, AEB_*, HHC_*
```

**Output (in DEM_Requirements.md):**
```markdown
**STM Configuration:**
- ESPBase = (as defined in system strategy)
- AEB = (as defined in system strategy)
- HHC = (as defined in system strategy)

*Note: Wildcard (*) notation detected. Specific degraded states should be defined in system architecture.*
```

## CRITICAL REMINDERS

- **No Assumptions**: Extract only what is explicitly stated in System strategy field
- **Consistent Formatting**: Use recommended templates for all failures
- **Traceability**: Maintain clear link between parsed STM config and original System strategy text
- **Validation**: Flag any malformed or unclear System strategy entries
- **Master-Slave Dependencies**: Always validate master-slave state compatibility and flag inconsistencies to user
- **Integration**: Ensure STM configuration is properly integrated into DEM_Requirements.md structure
- **Future Updates**: Specific master-slave dependency rules (state-level requirements) will be documented in future updates

## DEPENDENCY RULES (TO BE EXPANDED)

**Note**: The following section will be populated with specific dependency rules in future updates:

### Master System: ESPBase
- State hierarchy (lowest to highest): TBD
- Example states: EbdPumpless, ESPOnTcsExtended, Full, etc.

### Slave System Dependencies
- **AEB (Autonomous Emergency Braking)**:
  - Minimum ESPBase state required for ON: ESPOnTcsExtended (or higher)
  - If ESPBase < ESPOnTcsExtended: AEB must be OFF
  
- **HHC (Hill Hold Control)**:
  - Dependency rules: TBD
  
- **HBA (Hydraulic Brake Assist)**:
  - Dependency rules: TBD

*This section will be expanded with complete dependency matrix and validation logic in future instruction updates.*
