# STM Configuration Generation – Instruction File

This document provides detailed guidance for **Agent Mode in GHCP** to automatically generate an **STM Configuration File** based on node degradation requirements and state machine component specifications.

---

## 🎯 Objective

To generate a standardized STM Configuration file (.txt) that defines node degradation states for state machine components in compliance with **Diamant state machine architecture**.

---

## 📂 Input Requirements

The following attributes must be extracted or provided for each node-to-STM mapping:

### Node Degradation Information

| Attribute | Description | Source |
|-----------|-------------|--------|
| **Node Name** | The diagnostic node name (e.g., Node_VoltageHandler1, Node_BrakeTemperatureModel). | From node requirements (SWCS_*) |
| **Target States** | List of STM component degradation states in format: `<stm_ref> = <state_ref>`. | From STM configuration requirements (SWCS_*) |
| **STM Component (stm_ref)** | The state machine component reference (e.g., ESPBase, VLC_AD_Main, AEB, CCO_HDC). | From STM_PROJECTLINK definitions |
| **Degradation State (state_ref)** | The target state for node degradation (e.g., Off, EbdPumpless, RampOff, On). | From STM_VAR_STATE definitions |

### State Machine Component Information

| Attribute | Description | Source |
|-----------|-------------|--------|
| **STM Component Name** | Human-readable STM component name. | From STM requirements (SWCS_*) |
| **Available States** | List of valid states for this STM component. | From STM_COMPONENT definitions |
| **Description** | Purpose and behavior of the STM component. | From STM requirements (SWCS_*) |

---

## ⚙️ Output Format

The generated file must be a `.txt` structured STM Configuration file containing all node-to-STM mappings in the correct syntax.  
Each entry should follow the required format for Diamant STM configuration updates.

---

## 🧠 Processing Logic

1. **Parse input** – Extract node degradation information from Requirements.csv (SWCS_* entries for STM configuration).

2. **Group by node** – Collect all STM component degradation states for each node.

3. **Validate STM references** – Ensure each stm_ref exists in the STM_PROJECTLINK database. Valid components include:
   - ESPBase (ESP Base functions)
   - VLC_AD_Main (Vehicle Longitudinal Control - Autonomous Driving)
   - CCO_HDC (Hill Descent Control)
   - VLC_CDD_B (Comfort Deceleration Drive B)
   - AEB (Autonomous Emergency Braking)
   - HHC (Hill Hold Control)
   - HBA (Hydraulic Brake Assist)
   - And other project-specific STM components

4. **Validate state references** – Ensure each state_ref is valid for the corresponding STM component. Common states include:
   - Off (Component disabled)
   - On (Component enabled)
   - RampOff (Gradual transition to Off)
   - EbdOn, EbdPumpless (EBD-specific states)
   - AbsOnWithPMc (ABS with pressure modulation)
   - EspOnTcsExtended (ESP with extended TCS)

5. **Normalize state names** – Accept common input variants but normalize to canonical output values:
   - Variants mapping to `Off`: `off`, `Off`, `OFF`, `disabled`
   - Variants mapping to `On`: `on`, `On`, `ON`, `enabled`
   - Variants mapping to `RampOff`: `rampoff`, `RampOff`, `RAMP_OFF`, `ramp_off`

   If an input value does not match any known variant, add a comment `# AMBIGUOUS_STATE: original_value` and flag for manual review.

6. **Check for duplicates** – Ensure each node-STM pair appears only once. If duplicates exist, use the last occurrence and flag with comment `# DUPLICATE_ENTRY_FOUND: kept last occurrence`.

7. **Preserve source values** – To maintain traceability, include original verbatim text for normalized fields:
   - `State (source): <original>` as a comment if normalization occurred

8. **Assemble node sections** – Construct each node section with proper formatting:
   - Node name line: `Node name: <NodeName>`
   - Target states line: `Target states: <stm_ref1> = <state_ref1>; <stm_ref2> = <state_ref2>; ...`
   - Blank line separator between different nodes

9. **Generate output file** – Save the structured content into a `.txt` file named `Diamant_Generate_STMConfig.txt`.

10. **Verify syntax** – Confirm that the generated file adheres to expected Diamant STM configuration syntax rules.

---

## 📋 Notes

- Each node should appear only once in the output file, even if multiple STM components reference it.
- Target states are listed as semicolon-separated pairs for each node.
- The agent should not modify unrelated sections or metadata in the `.txt` file.
- **State names** must match the STM_VAR_STATE definitions in the STM_PROJECTLINK database.
- **STM references** must match the stm_ref attribute in STM_PROJECTLINK entries.
- The `delay_degradation` attribute is always set to "false" by the plugin (not in input file).

---

## ✅ Example Entry

```
Node name: Node_VoltageHandler1
Target states: ESPBase = EbdPumpless; AEB = Off; HHC = Off; HBA = Off

Node name: Node_BrakeTemperatureModel
Target states: VLC_AD_Main = Off; CCO_HDC = RampOff

Node name: Node_WssDirFr
Target states: VLC_AD_Main = Off; VLC_CDD_B = Off; CCO_HDC = RampOff
```

---

## 🧩 Agent Mode Behavior Summary

| Step | Agent Action |
|------|---------------|
| 1 | Read Requirements.csv and parse SWCS_* (STM configuration) entries |
| 2 | Extract node names and their target STM degradation states |
| 3 | Group all STM component states by node |
| 4 | Validate stm_ref values against known STM_PROJECTLINK components |
| 5 | Validate state_ref values against known STM_VAR_STATE definitions |
| 6 | Normalize state names to canonical values |
| 7 | Check for duplicate node-STM pairs |
| 8 | Generate structured node entries with target states |
| 9 | Assemble into `.txt` output format |
| 10 | Save file to configured workspace (splitter_input/ folder) |
| 11 | Log summary report for generation result |

---

## 🔍 Validation Checklist

Before generating the output file, verify:

- [ ] All node names extracted from STM configuration requirements
- [ ] All STM component references (stm_ref) are valid
- [ ] All state references (state_ref) are valid for their respective STM components
- [ ] No duplicate node entries exist
- [ ] State names normalized to canonical values
- [ ] Each node has at least one target state defined
- [ ] Format matches expected syntax (Node name: / Target states: pattern)

---

## 🎨 Example Full File

```
Node name: Node_VoltageHandler1
Target states: ESPBase = EbdPumpless; AEB = Off; HHC = Off; HBA = Off

Node name: Node_BrakeTemperatureModel
Target states: VLC_AD_Main = Off; CCO_HDC = RampOff

Node name: Node_WssDirRr
Target states: VLC_AD_Main = Off

Node name: Node_WssDirRl
Target states: VLC_AD_Main = Off

Node name: Node_WssDirGeneric
Target states: VLC_AD_Main = Off

Node name: Node_WssDirFr
Target states: VLC_AD_Main = Off; VLC_CDD_B = Off; CCO_HDC = RampOff

Node name: Node_WssDirFl
Target states: VLC_AD_Main = Off

Node name: Node_EmergencyBrake_Abs
Target states: VLC_AD_Main = Off; CCO_HDC = Off; VLC_CDD_B = Off
```

---

## 📊 Expected Metrics

After generation, the file should contain:
- **Node Count**: Total number of nodes configured (e.g., 8 nodes)
- **STM Component Coverage**: Number of different STM components referenced (e.g., 5 components)
- **Total Mappings**: Total node-to-STM state mappings (e.g., 15 mappings)
- **Validation Status**: All entries validated against database

---

## 🚨 Error Conditions

The agent should flag these conditions:

| Condition | Action |
|-----------|--------|
| Invalid stm_ref | Add comment `# INVALID_STM_REF: <name>` and flag for review |
| Invalid state_ref | Add comment `# INVALID_STATE_REF: <name> for <stm_ref>` |
| Duplicate node entry | Keep last occurrence, add comment `# DUPLICATE_ENTRY` |
| Missing target states | Skip entry, log warning |
| Ambiguous state name | Normalize if possible, else add `# AMBIGUOUS_STATE` comment |

---

## � Post-Execution File Tracking

After successful CLI execution, all modified STM XML files should be tracked in a review file for downstream review processes.

### Tracking File Location
```
GenFromCoPilot\Review\STM_filesToReview.txt
```

### Tracking File Format
```
# STM Configuration Files - Review Tracker
# Auto-generated by Diamant_Update_STMConfig_CLI execution
# Lists all STM XML files modified during workflow execution

===========================================
Execution Date: 2026-02-02 16:45:30
Configuration: CHRxIPB2xICExEP800102xECA
===========================================

STM Configuration Files Modified:
- CHRYSLER_IPB\rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\Diamant_Spec_Project_NonRoPP\JLR_IPACE\NonHAD\Diamant__STM__PROJECT.xml

Nodes Updated/Added: 6
STM_PROJECTLINKs Modified: 8

Total Files Modified: 1

```

### Implementation Steps

1. **Parse Console Output**: Extract file path from "Splitter [...] written" message
2. **Extract Statistics**: Parse log file for node update/add counts and STM_PROJECTLINK modifications
3. **Create/Append Tracking File**: 
   - If file doesn't exist, create with header
   - Append new execution block with timestamp, configuration, and file path
4. **Include Metrics**: Add nodes updated/added and STM_PROJECTLINKs modified counts
5. **Verify Tracking**: Confirm file created/updated successfully

### PowerShell Example for File Tracking

```powershell
# After CLI execution, extract modified file from console output
$output = & "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe" <params> 2>&1
$splitterLine = $output | Select-String -Pattern "Splitter \[(.+)\] written"

if ($splitterLine) {
    $stmFile = $null
    if ($splitterLine.Line -match "Splitter \[(.+)\] written") {
        $stmFile = $matches[1].Trim()
    }
    
    # Parse log file for statistics
    $logFile = "CHRYSLER_IPB\Diamant_Update_STMConfig_Log.txt"
    $nodesUpdated = 0
    $nodesAdded = 0
    $projectLinksModified = 0
    
    if (Test-Path $logFile) {
        $logContent = Get-Content $logFile -Raw
        if ($logContent -match "Total nodes updated: (\d+)") { $nodesUpdated = $matches[1] }
        if ($logContent -match "Total nodes added: (\d+)") { $nodesAdded = $matches[1] }
        if ($logContent -match "Found (\d+) STM_PROJECTLINK\(s\)") { $projectLinksModified = $matches[1] }
    }
    
    # Create tracking content
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $trackingContent = @"
===========================================
Execution Date: $timestamp
Configuration: $selectedConfig
===========================================

"@
    
    if ($stmFile) {
        $trackingContent += "STM Configuration Files Modified:`n"
        $trackingContent += "- CHRYSLER_IPB\$stmFile`n`n"
    }
    
    $totalNodes = [int]$nodesUpdated + [int]$nodesAdded
    $trackingContent += "Nodes Updated/Added: $totalNodes`n"
    $trackingContent += "STM_PROJECTLINKs Modified: $projectLinksModified`n`n"
    $trackingContent += "Total Files Modified: 1`n`n"
    
    # Append to tracking file
    $trackingFile = "GenFromCoPilot\Review\STM_filesToReview.txt"
    
    if (!(Test-Path $trackingFile)) {
        $header = @"
# STM Configuration Files - Review Tracker
# Auto-generated by Diamant_Update_STMConfig_CLI execution
# Lists all STM XML files modified during workflow execution

"@
        Set-Content -Path $trackingFile -Value $header
    }
    
    Add-Content -Path $trackingFile -Value $trackingContent
    
    Write-Host "✅ File tracking updated: $trackingFile" -ForegroundColor Green
}
```

### Integration with Review Workflow

The tracking file serves as input for the review process:
1. Review tools read `STM_filesToReview.txt` to identify files requiring review
2. Each listed STM_PROJECT file is validated against the STM review checklist
3. Review report references specific execution dates and configurations
4. Tracking history provides audit trail for STM configuration changes
5. Metrics (nodes updated/added) help assess scope of changes

---

## �🔄 Integration Points

This instruction file integrates with:
- **Node Database Update**: Nodes must exist before STM configuration
- **STM Component Definitions**: stm_ref values from STM_PROJECTLINK
- **State Definitions**: state_ref values from STM_VAR_STATE
- **Requirements Analysis**: Source data from SWCS_* entries

---

## 📝 Format Specification

### Node Entry Format
```
Node name: <NodeName>
Target states: <stm_ref1> = <state_ref1>; <stm_ref2> = <state_ref2>; ...

```

### Rules:
1. Each node entry must start with "Node name: "
2. Followed by "Target states: " on the next line
3. Target states are semicolon-separated pairs in format: `<stm_ref> = <state_ref>`
4. Blank line after each node entry
5. No trailing spaces or tabs
6. UTF-8 encoding
7. Windows line endings (CRLF) or Unix line endings (LF) both acceptable

---

## ✅ Quality Checks

Before finalizing the output:

1. **Syntax Check**: Verify every line follows the pattern
2. **Reference Check**: All stm_ref values exist in database
3. **State Check**: All state_ref values valid for their STM component
4. **Completeness Check**: All required nodes from requirements included
5. **Duplicate Check**: No node appears twice
6. **Format Check**: Consistent spacing and separators

---

## Version History
- **Version 1.1** (February 2, 2026): Added file tracking requirement with `STM_filesToReview.txt` for review workflow integration
- **Version 1.0** (January 19, 2026): Initial instruction file created
  - STM configuration file generation
  - Node-to-STM state mapping
  - Validation and normalization rules
  - Integration with DiamantPro workflow
