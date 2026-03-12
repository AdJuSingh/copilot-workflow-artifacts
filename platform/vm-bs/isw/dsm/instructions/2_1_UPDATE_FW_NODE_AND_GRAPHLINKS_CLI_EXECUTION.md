# Complete Diagnostic Database Update - CLI Execution Guide

## Overview
This document provides technical details for executing the **Diamant_Update_FailureNodeGraph_CLI.dpp** plugin, which performs comprehensive diagnostic database updates including FAILURE_WORD, NODE, and NODE_LINK (Graph Links) entries in a single execution.

**Purpose**: Create or update all three types of diagnostic database entries from structured text input files using DiamantPro's CLI interface.

**Target Users**: Build engineers, diagnostic configuration managers, automation scripts

---

## Quick Reference

### Plugin Location
```
CHRYSLER_IPB\rb\as\core\app\dsm\tools\DiamantPro\plugins\Diamant_Update_FailureNodeGraph_CLI.dpp
```

### Basic Command Template
```powershell
$env:DIAMANT_FW_INPUT_FILE="C:\path\to\Diamant_Generate_FWSplitter.txt"
$env:DIAMANT_NODE_INPUT_FILE="C:\path\to\Diamant_Generate_NodeSplitter.txt"
$env:DIAMANT_GRAPHLINK_INPUT_FILE="C:\path\to\Diamant_Generate_GraphLinks.txt"

& "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe" `
  --READSPLITTER="Gen/<Configuration>/make/Cfg_DBFiles_GenMake.csv" `
  --RUNPLUGIN="rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_FailureNodeGraph_CLI.dpp" `
  --WRITESPLITTERS `
  --CONSOLEOUTPUT=ALL
```

**Note**: All three environment variables are optional. Provide at least one. The plugin will skip processing for any missing input file.

---

## Environment Variables

### DIAMANT_FW_INPUT_FILE
**Purpose**: Path to FAILURE_WORD definitions text file  
**Required**: No (optional - skips FW processing if not provided)  
**Format**: Absolute Windows path  
**Example**: `C:\Workspace\GenFromCoPilot\splitter_input\Diamant_Generate_FWSplitter.txt`

### DIAMANT_NODE_INPUT_FILE
**Purpose**: Path to NODE definitions text file  
**Required**: No (optional - skips NODE processing if not provided)  
**Format**: Absolute Windows path  
**Example**: `C:\Workspace\GenFromCoPilot\splitter_input\Diamant_Generate_NodeSplitter.txt`

### DIAMANT_GRAPHLINK_INPUT_FILE
**Purpose**: Path to Graph Link (NODE_LINK) definitions text file  
**Required**: No (optional - skips Graph Link processing if not provided)  
**Format**: Absolute Windows path  
**Example**: `C:\Workspace\GenFromCoPilot\splitter_input\Diamant_Generate_GraphLinks.txt`

**Note**: At least ONE environment variable must be provided. You can provide any combination (1, 2, or all 3).

---

## Input File Formats

### 1. FAILURE_WORD Input Format

**File Structure**: Blank-line separated blocks with key:value pairs

**Global Configuration Block** (applies to all entries):
```
Customer: Cus_CHR
SW_GROUP_REF: DCOM
PRODUCT_LINE_REF: IPB
```

**Entry Block** (per FAILURE_WORD):
```
Failure Name: FW_HydraulicUndervoltage1
Category: ExternalFault
Description: Hydraulic system voltage below threshold
DebouncerType: CounterBased
PassedThreshold: 100
FailedThreshold: -50
RootCause: LowVoltageSupply
TcManeuver: TCM_VoltageTest
```

**Supported Keys**:
- **Global**: `Customer`, `Project`, `SW_GROUP_REF`, `PRODUCT_LINE_REF`
- **Entry**: `Failure Name` (required), `Category`, `Description`, `DebouncerType`, `PassedThreshold`, `FailedThreshold`, `RootCause`, `TcManeuver`

**Key Notes**:
- `SW_GROUP_REF` auto-prefixes with `SwGrp_` if not present (DCOM → SwGrp_DCOM)
- Global config applies to all entries unless overridden at entry level
- Blank lines separate entries

### 2. NODE Input Format

**File Structure**: Blank-line separated blocks with key:value pairs

**Global Configuration Block**:
```
Customer: Cus_CHR
SW_GROUP_REF: SwGrp_DCOM
PRODUCT_LINE_REF: IPB
```

**Entry Block** (per NODE):
```
Node name: Node_VoltageHandler1
Description: Voltage monitoring and control node
Failure: FW_HydraulicUndervoltage1,100
Failure: FW_HydraulicUndervoltage2,90
Failure: FW_HydraulicUndervoltage3,80
```

**Supported Keys**:
- **Global**: `Customer`, `SW_GROUP_REF`, `PRODUCT_LINE_REF`
- **Entry**: `Node name` (required), `Description`, `Failure` (can have multiple)

**Failure Format**: `FW_Name,Priority` where Priority is an integer (higher = more important)

**Key Notes**:
- `SW_GROUP_REF` auto-prefixes with `SwGrp_` if not present
- Multiple `Failure` lines create multiple FW_REF entries
- Entry-level config overrides global config

### 3. Graph Link Input Format

**File Structure**: Multiple format options supported

**Option 1: Node/Parent Format** (Recommended):
```
Node name: Node_VoltageHandler1
Parent: Node_Ecu

Node name: Node_PressureMonitor
Parent: Node_Ecu
```

**Option 2: Source/Target Format**:
```
Source: Node_Ecu
Target: Node_VoltageHandler1

Source: Node_Ecu
Target: Node_PressureMonitor
```

**Option 3: Single-Line Arrow Format**:
```
Link: Node_Ecu -> Node_VoltageHandler1
Link: Node_Ecu -> Node_PressureMonitor
```

**Supported Keys**:
- **Node/Parent**: `Node name`, `Node`, `Name`, `Parent`, `Parent Node`, `ParentNode`, `Parent node`
- **Source/Target**: `Source`, `Target`
- **Arrow**: `Link: <Source> -> <Target>`

**Key Notes**:
- All three formats can be mixed in the same file
- Blank lines separate link entries (except for arrow format)
- Duplicate links are detected and skipped

---

## Execution Order

The plugin processes input files in this sequence:

1. **FAILURE_WORD Processing** (if `DIAMANT_FW_INPUT_FILE` provided)
   - Parse FW input file
   - Load existing FAILURE_WORD entries from database
   - Create or update each FAILURE_WORD
   - Apply properties, debouncer, monitoring, test complete settings

2. **NODE Processing** (if `DIAMANT_NODE_INPUT_FILE` provided)
   - Parse NODE input file
   - Load existing NODE entries from database
   - Create or update each NODE
   - Apply properties and link FAILURE_WORDs via FW_REFS

3. **Graph Link Processing** (if `DIAMANT_GRAPHLINK_INPUT_FILE` provided)
   - Parse Graph Link input file
   - Load existing NODE_LINK entries from database
   - Create new links (skip duplicates)
   - Establish parent-child relationships

**Rationale**: Process FW first (prerequisites for NODEs), then NODEs (prerequisites for Graph Links), then Graph Links (connects NODEs).

---

## Console Output

### Success Indicators
```
Using FW input file from environment variable: C:\...\Diamant_Generate_FWSplitter.txt
Using NODE input file from environment variable: C:\...\Diamant_Generate_NodeSplitter.txt
Using Graph Link input file from environment variable: C:\...\Diamant_Generate_GraphLinks.txt

Parsed 3 failure word entries from input file.
FAILURE_WORD processing completed! Created: 3, Updated: 0

Parsed 1 node entries from input file.
NODE processing completed! Created: 1, Updated: 0

Parsed 1 link entries from input file.
Graph Link processing completed! Created: 1, Existing: 0

Splitter [rb\as\ms\core\app\dcom\RBAPLCust\cfg\Diamant__FW__CHR__DCOM__DCOM__IPB.xml] written
Splitter [.\Diamant__NODE__CHR__DCOM__IPB.xml] written
Splitter [rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\Diamant_Spec_Project_NonRoPP\Diamant__Graph__PROJECT.xml] written
```

### Error Indicators
```
ERROR: No input files selected. At least one input file must be provided.
ERROR: FW input file not found: C:\path\to\file.txt
ERROR: No valid failure word entries found in FW input file.
WARNING: Skipping entry without Failure Name.
WARNING: Invalid link format: malformed_link
```

---

## Log File

### Location
```
CHRYSLER_IPB\Diamant_Update_FailureNodeGraph_CLI_Log.txt
```

### Content Structure
```
===================================================================================
Start of Diamant_Update_FailureNodeGraph_CLI Execution...
Complete plugin for FAILURE_WORD, NODE, and GRAPH LINK database updates
===================================================================================

Using FW input file from DIAMANT_FW_INPUT_FILE environment variable: C:\...
Using NODE input file from DIAMANT_NODE_INPUT_FILE environment variable: C:\...
Using Graph Link input file from DIAMANT_GRAPHLINK_INPUT_FILE environment variable: C:\...

Input files:
  FAILURE_WORD: C:\...\Diamant_Generate_FWSplitter.txt
  NODE: C:\...\Diamant_Generate_NodeSplitter.txt
  GRAPH LINK: C:\...\Diamant_Generate_GraphLinks.txt

###########################################################################
PROCESSING FAILURE_WORD ENTRIES
###########################################################################

Parsed 3 failure word entries from input file.

Global Configuration (from FW input file):
  Customer: Cus_CHR
  SW_GROUP_REF: DCOM
  PRODUCT_LINE_REF: IPB

Retrieved 2547 existing FAILURE_WORD entries from database.

Processing FAILURE_WORD: FW_HydraulicUndervoltage1
  'FW_HydraulicUndervoltage1' not found in database. Creating new FAILURE_WORD object.
  Set CUSTOMER: Cus_CHR
  Set SW_GROUP_REF: SwGrp_DCOM
  Set PRODUCT_LINE_REF: IPB
  Set PassedThreshold: 100
  Set FailedThreshold: -50
  Updated AUTOSAR_DEBOUNCER for 'FW_HydraulicUndervoltage1'.
  ModifyAdd for 'FW_HydraulicUndervoltage1' returned: True

[... similar for FW_HydraulicUndervoltage2, FW_HydraulicUndervoltage3 ...]

Total FAILURE_WORDs created: 3
Total FAILURE_WORDs updated: 0

###########################################################################
PROCESSING NODE ENTRIES
###########################################################################

Parsed 1 node entries from input file.

Global Configuration (from NODE input file):
  Customer: Cus_CHR
  SW_GROUP_REF: SwGrp_DCOM
  PRODUCT_LINE_REF: IPB

Retrieved 354 existing NODE entries from database.

Processing NODE: Node_VoltageHandler1
  'Node_VoltageHandler1' not found in database. Creating new NODE object.
  Set CUSTOMER: Cus_CHR
  Set SW_GROUP_REF from entry: SwGrp_DCOM
  Set PRODUCT_LINE_REF: IPB
  Updated properties and KEYLIST for NODE 'Node_VoltageHandler1'.
  Attempting to access FW_REFS using reflection...
  Found property: FW_REFS (Type: LIST`1)
  Cleared existing FW_REFS.
  Processing 3 failure(s) for node 'Node_VoltageHandler1':
    Added FW_REF: FW_HydraulicUndervoltage1 with priority: 100
    Added FW_REF: FW_HydraulicUndervoltage2 with priority: 90
    Added FW_REF: FW_HydraulicUndervoltage3 with priority: 80
  ModifyAdd for NODE 'Node_VoltageHandler1' returned: True

Total NODEs created: 1
Total NODEs updated: 0

###########################################################################
PROCESSING GRAPH LINK ENTRIES
###########################################################################

Parsed 1 link entries from input file.

Retrieved 379 existing NODE_LINK entries from database.

Processing NODE_LINK: Node_Ecu -> Node_VoltageHandler1
  'Node_Ecu -> Node_VoltageHandler1' not found in database. Creating new NODE_LINK object.
  ModifyAdd operation for NODE_LINK 'Node_Ecu -> Node_VoltageHandler1' returned: True

Total NODE_LINKs created: 1
Total NODE_LINKs already existing: 0

===================================================================================
End of Diamant_Update_FailureNodeGraph_CLI Execution
Overall Status: SUCCESS
NOTE: Use --WRITESPLITTERS flag in CLI to persist changes to XML files.
===================================================================================
```

---

## Output XML Files

### FAILURE_WORD Files
**Location Pattern**: `rb\as\ms\core\app\<sw_group>\RBAPLCust\cfg\Diamant__FW__<CUSTOMER>__<SW_GROUP>__<SW_GROUP>__<PRODUCT_LINE>.xml`

**Example**: `rb\as\ms\core\app\dcom\RBAPLCust\cfg\Diamant__FW__CHR__DCOM__DCOM__IPB.xml`

**Routing**: Determined by `CUSTOMER`, `SW_GROUP_REF`, and `PRODUCT_LINE_REF` KEYLIST values

### NODE Files
**Location Pattern**: Varies based on `CUSTOMER`, `SW_GROUP_REF`, and `PRODUCT_LINE_REF`

**Common Pattern**: `Diamant__NODE__<CUSTOMER>__<SW_GROUP>__<PRODUCT_LINE>.xml`

**Example**: `CHRYSLER_IPB\Diamant__NODE__CHR__DCOM__IPB.xml`

**Note**: May be created in current directory initially, then routed by DiamantPro

### Graph Link Files
**Location Pattern**: `rb\as\mb\<product_line>\dsmpr\cfg\Diamant_Cfg\<Variant>\Diamant__Graph__PROJECT.xml`

**Example**: `rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\Diamant_Spec_Project_NonRoPP\Diamant__Graph__PROJECT.xml`

**Routing**: Based on target node's KEYLIST values (primarily PRODUCT_LINE_REF)

---

## Typical Console Output Example

```
This is DiamantPro Core Library - 4.3 (1/26/2026 1:30:47 PM)
*** Processing LOG Value: DiamantProPlugin_CompleteUpdate.log
*** Processing READSPLITTER Value: Gen/CHRxIPB2xICExEP800102xECA/make/Cfg_DBFiles_GenMake.csv

[... unrelated plugin compilation errors ...]

*** Processing RUNPLUGIN Value: rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_FailureNodeGraph_CLI.dpp

Using FW input file from environment variable: C:\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\Diamant_Generate_FWSplitter.txt (Plugin Output) []
Using NODE input file from environment variable: C:\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\Diamant_Generate_NodeSplitter.txt (Plugin Output) []
Using Graph Link input file from environment variable: C:\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\Diamant_Generate_GraphLinks.txt (Plugin Output) []

Parsed 3 failure word entries from input file. (Plugin Output) []
FAILURE_WORD processing completed! Created: 3, Updated: 0 (Plugin Output) []

Parsed 1 node entries from input file. (Plugin Output) []
NODE processing completed! Created: 1, Updated: 0 (Plugin Output) []

Parsed 1 link entries from input file. (Plugin Output) []
Graph Link processing completed! Created: 1, Existing: 0 (Plugin Output) []

*** Processing WRITESPLITTERS Value: True
Splitter [rb\as\ms\core\app\dcom\RBAPLCust\cfg\Diamant__FW__CHR__DCOM__DCOM__IPB.xml] written
Splitter [.\Diamant__NODE__CHR__DCOM__IPB.xml] written
Splitter [rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\Diamant_Spec_Project_NonRoPP\Diamant__Graph__PROJECT.xml] written

*** Processing CONSOLEOUTPUT Value: ALL
Finished in (16.5s) with (156)Errors and (7)Warnings
```

**Note**: Exit code 1 with error messages is **EXPECTED AND NORMAL** - these are unrelated plugin compilation errors that don't affect the combined plugin execution.

---

## Troubleshooting

### Issue: "No input files selected"
**Cause**: All three environment variables are undefined or empty  
**Solution**: Set at least one of `DIAMANT_FW_INPUT_FILE`, `DIAMANT_NODE_INPUT_FILE`, or `DIAMANT_GRAPHLINK_INPUT_FILE`

### Issue: "FW/NODE/Graph Link input file not found"
**Cause**: File path is incorrect or relative instead of absolute  
**Solution**: 
1. Use absolute Windows paths (e.g., `C:\Workspaces\...`)
2. Verify file exists at specified location using `Test-Path` in PowerShell
3. Check for typos in filename

### Issue: "No valid entries found in input file"
**Cause**: Input file format is incorrect or missing required keys  
**Solutions**:
- **FW**: Ensure each entry has `Failure Name: <name>` line
- **NODE**: Ensure each entry has `Node name: <name>` line
- **Graph Link**: Ensure each entry has both Source/Target or Node name/Parent
- Check for blank lines between entries

### Issue: "Skipping entry without Failure Name / Node name"
**Cause**: Entry block is missing the required identifier line  
**Solution**: Add `Failure Name:` or `Node name:` line to each entry block

### Issue: "Skipping entry missing Source or Target"
**Cause**: Graph Link entry doesn't specify both endpoints  
**Solution**: Provide both source and target using one of the supported formats

### Issue: ModifyAdd returns False
**Cause**: Usually indicates successful in-place update, not a failure  
**Solution**: Check log file for details. Verify entry exists in database. This often means the entry was already present and updated successfully.

### Issue: New XML file created in current directory
**Cause**: DiamantPro couldn't determine proper routing location  
**Solution**: 
1. Check if file appears in plugin output: `Splitter [.\Filename.xml]`
2. Move file to appropriate location based on KEYLIST values
3. Verify CUSTOMER, SW_GROUP_REF, PRODUCT_LINE_REF are correct

### Issue: Exit code 1 reported
**Cause**: Unrelated plugin compilation errors in DiamantPro environment  
**Solution**: This is **NORMAL** - check console output for plugin-specific success messages. If plugin shows "SUCCESS" and files are written, operation completed successfully.

---

## Command Examples

### Example 1: Update All Three (FW, NODE, Graph Links)
```powershell
cd C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\CHRYSLER_IPB

$env:DIAMANT_FW_INPUT_FILE="C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\Diamant_Generate_FWSplitter.txt"
$env:DIAMANT_NODE_INPUT_FILE="C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\Diamant_Generate_NodeSplitter.txt"
$env:DIAMANT_GRAPHLINK_INPUT_FILE="C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\Diamant_Generate_GraphLinks.txt"

& "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe" `
  --READSPLITTER="Gen/CHRxIPB2xICExEP800102xECA/make/Cfg_DBFiles_GenMake.csv" `
  --RUNPLUGIN="rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_FailureNodeGraph_CLI.dpp" `
  --WRITESPLITTERS `
  --CONSOLEOUTPUT=ALL
```

### Example 2: Update Only FAILURE_WORD and NODE (Skip Graph Links)
```powershell
$env:DIAMANT_FW_INPUT_FILE="C:\Workspaces\input\FWSplitter.txt"
$env:DIAMANT_NODE_INPUT_FILE="C:\Workspaces\input\NodeSplitter.txt"
# Don't set DIAMANT_GRAPHLINK_INPUT_FILE - Graph Link processing will be skipped

& "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe" `
  --READSPLITTER="Gen/<Config>/make/Cfg_DBFiles_GenMake.csv" `
  --RUNPLUGIN="rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_FailureNodeGraph_CLI.dpp" `
  --WRITESPLITTERS `
  --CONSOLEOUTPUT=ALL
```

### Example 3: Update Only Graph Links (FW and NODE Already Created)
```powershell
# Only set Graph Link input file
$env:DIAMANT_GRAPHLINK_INPUT_FILE="C:\Workspaces\input\GraphLinks.txt"

& "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe" `
  --READSPLITTER="Gen/<Config>/make/Cfg_DBFiles_GenMake.csv" `
  --RUNPLUGIN="rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_FailureNodeGraph_CLI.dpp" `
  --WRITESPLITTERS `
  --CONSOLEOUTPUT=ALL
```

### Example 4: Filter Console Output for Summary
```powershell
$env:DIAMANT_FW_INPUT_FILE="C:\path\to\FWSplitter.txt"
$env:DIAMANT_NODE_INPUT_FILE="C:\path\to\NodeSplitter.txt"
$env:DIAMANT_GRAPHLINK_INPUT_FILE="C:\path\to\GraphLinks.txt"

& "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe" `
  --READSPLITTER="Gen/<Config>/make/Cfg_DBFiles_GenMake.csv" `
  --RUNPLUGIN="rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_FailureNodeGraph_CLI.dpp" `
  --WRITESPLITTERS `
  --CONSOLEOUTPUT=ALL 2>&1 | `
  Select-String -Pattern "Using.*input file|Parsed.*entries|processing completed|Splitter.*written"
```

---

## Post-Execution File Tracking

After successful CLI execution, all modified XML files should be tracked in a review file for downstream review processes.

### Tracking File Location
```
GenFromCoPilot\Review\Failure_Node_Graph_filesToReview.txt
```

### Tracking File Format
```
# Failure Word, Node, and Graph Link Files - Review Tracker
# Auto-generated by Diamant_Update_FailureNodeGraph_CLI execution
# Lists all XML files modified during workflow execution

===========================================
Execution Date: 2026-02-02 14:35:22
Configuration: CHRxIPB2xICExEP800102xECA
===========================================

FAILURE_WORD Files Modified:
- CHRYSLER_IPB\rb\as\ms\core\app\dcom\RBAPLCust\cfg\Diamant__FW__CHR__DCOM__DCOM__IPB.xml

NODE Files Modified:
- CHRYSLER_IPB\Diamant__NODE__CHR__DCOM__IPB.xml

Graph Link Files Modified:
- CHRYSLER_IPB\rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\Diamant_Spec_Project_NonRoPP\Diamant__Graph__PROJECT.xml

Total Files Modified: 3

```

### Implementation Steps

1. **Parse Console Output**: Extract file paths from "Splitter [...] written" messages
2. **Categorize Files**: Group by type (FAILURE_WORD, NODE, Graph Link) based on filename patterns:
   - `Diamant__FW__*.xml` → FAILURE_WORD
   - `Diamant__NODE__*.xml` → NODE
   - `Diamant__Graph__*.xml` or `Diamant__GraphLink__*.xml` → Graph Link
3. **Create/Append Tracking File**: 
   - If file doesn't exist, create with header
   - Append new execution block with timestamp and file list
4. **Verify Tracking**: Confirm file created/updated successfully

### PowerShell Example for File Tracking

```powershell
# After CLI execution, extract modified files
$output = & "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe" <params> 2>&1
$splitterLines = $output | Select-String -Pattern "Splitter \[(.+)\] written"

# Extract file paths
$modifiedFiles = $splitterLines | ForEach-Object {
    if ($_.Line -match "Splitter \[(.+)\] written") {
        $matches[1].Trim()
    }
}

# Categorize files
$fwFiles = $modifiedFiles | Where-Object { $_ -match "Diamant__FW__" }
$nodeFiles = $modifiedFiles | Where-Object { $_ -match "Diamant__NODE__" }
$graphFiles = $modifiedFiles | Where-Object { $_ -match "Diamant__(Graph|GraphLink)__" }

# Create tracking content
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$trackingContent = @"
===========================================
Execution Date: $timestamp
Configuration: $selectedConfig
===========================================

"@

if ($fwFiles) {
    $trackingContent += "FAILURE_WORD Files Modified:`n"
    $fwFiles | ForEach-Object { $trackingContent += "- CHRYSLER_IPB\$_`n" }
    $trackingContent += "`n"
}

if ($nodeFiles) {
    $trackingContent += "NODE Files Modified:`n"
    $nodeFiles | ForEach-Object { $trackingContent += "- CHRYSLER_IPB\$_`n" }
    $trackingContent += "`n"
}

if ($graphFiles) {
    $trackingContent += "Graph Link Files Modified:`n"
    $graphFiles | ForEach-Object { $trackingContent += "- CHRYSLER_IPB\$_`n" }
    $trackingContent += "`n"
}

$trackingContent += "Total Files Modified: $($modifiedFiles.Count)`n`n"

# Append to tracking file
$trackingFile = "GenFromCoPilot\Review\Failure_Node_Graph_filesToReview.txt"

if (!(Test-Path $trackingFile)) {
    $header = @"
# Failure Word, Node, and Graph Link Files - Review Tracker
# Auto-generated by Diamant_Update_FailureNodeGraph_CLI execution
# Lists all XML files modified during workflow execution

"@
    Set-Content -Path $trackingFile -Value $header
}

Add-Content -Path $trackingFile -Value $trackingContent

Write-Host "✅ File tracking updated: $trackingFile" -ForegroundColor Green
```

### Integration with Review Workflow

The tracking file serves as input for the review process:
1. Review tools read `Failure_Node_Graph_filesToReview.txt` to identify files requiring review
2. Each listed file is validated against the review checklist
3. Review report references specific execution dates and configurations
4. Tracking history provides audit trail for configuration changes

---

## Best Practices

1. **Use Absolute Paths**: Always provide absolute Windows paths for input files to avoid path resolution issues

2. **Verify Input Files First**: Use `Test-Path` to confirm all input files exist before executing plugin

3. **Check Log File**: Always review `Diamant_Update_FailureNodeGraph_CLI_Log.txt` for detailed execution trace

4. **Update File Tracking**: Always update `Failure_Node_Graph_filesToReview.txt` after successful execution

4. **Process in Order**: For new entries, provide all three input files in a single execution to ensure proper dependencies

5. **Validate KEYLIST Values**: Verify `CUSTOMER`, `SW_GROUP_REF`, `PRODUCT_LINE_REF` are consistent across FW, NODE, and configuration

6. **Handle New Files**: If XML files appear in current directory, relocate them to proper paths based on KEYLIST routing

7. **Filter Console Output**: Use PowerShell filtering to extract relevant plugin messages from verbose DiamantPro output

8. **Test with Subset First**: For large updates, test with a small subset of entries to verify format and routing

9. **Backup Database**: Consider backing up XML files before major updates

10. **Document Changes**: Keep input files in version control for traceability

---

## Related Documentation

- **Related Prompt**: [2_1_update_fw_node_and_graphlinks.prompt.md](../.github/prompts/2_1_update_fw_node_and_graphlinks.prompt.md)
- **Related Instructions**:
  - [2_2_UPDATE_DTC_COMPLETE_WORKFLOW_CLI.md](2_2_UPDATE_DTC_COMPLETE_WORKFLOW_CLI.md) - DTC complete workflow
  - [2_3_STM_Config_generation_Instructions.md](2_3_STM_Config_generation_Instructions.md) - STM configuration

---

## Version History
- **Version 1.1** (February 2, 2026): Added file tracking requirement with `Failure_Node_Graph_filesToReview.txt` for review workflow integration
- **Version 1.0** (January 26, 2026): Initial comprehensive plugin combining FW, NODE, and Graph Links processing
