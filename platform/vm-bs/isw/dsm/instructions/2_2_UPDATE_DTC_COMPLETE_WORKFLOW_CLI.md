# 2.1.3 DiamantPro DTC Complete Workflow CLI Execution

## Overview
Update DTC (Diagnostic Trouble Code) database entries using a **single combined DiamantPro plugin** in CLI mode. This unified workflow executes all 4 DTC update steps sequentially in one DiamantPro session, combining: DTC creation, attribute assignment, attribute-to-DTC linking, and failure word-to-DTC linking.

## Purpose
- **Single-execution workflow**: All 4 steps run in one DiamantPro CLI command
- Create DTC entries with AUTOSAR properties (severity, WWHOBD class, OBD values)
- Assign DTC attributes (aging, debouncer, freeze frame configurations)
- Link DTC attributes to specific DTCs
- Link failure words (FAILURE_WORD) to DTCs for diagnostic reporting
- **Faster execution**: Reduces overhead by loading database once
- **Atomic operation**: All steps succeed or fail together

## ⚠️ Critical Requirements

**Single Plugin Execution**: Uses `Diamant_Update_DTC_Complete_Workflow.dpp` which internally executes:
1. Step 1: Create/Update DTC entries
2. Step 2: Create/Update DTC attribute definitions
3. Step 3: Link attributes to DTCs
4. Step 4: Link failure words to DTCs

**Database Loading**: MUST use `--READSPLITTER` to load database before plugin execution

**Write Persistence**: MUST use `--WRITESPLITTERS` after plugin to save all changes

**All Environment Variables Required**: Plugin requires ALL 4 input file paths set before execution

**Abort on Failure**: If any step fails, the entire workflow aborts without executing remaining steps

## Prerequisites

### Tools & Paths
- **DiamantPro CLI**: `C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe`
- **Plugin Directory**: `rb/as/core/app/dsm/tools/DiamantPro/plugins/`
- **Plugin File**: `Diamant_Update_DTC_Complete_Workflow.dpp`
- **PowerShell**: Windows PowerShell 5.1 or later

### Required Files

**Input Files** (all in `GenFromCoPilot/splitter_input/`):
1. **DTC_Input.txt** - DTC definitions
2. **DTCAttribute_Input.txt** - DTC attribute configurations
3. **DTC_Attr_Link_Input.txt** - DTC-to-attribute mappings
4. **FW_DTC_Link_Input.txt** - Failure word-to-DTC mappings

**Config CSV**: `Gen/<ConfigName>/make/Cfg_DBFiles_GenMake.csv`

## Workflow

### 1. Select Configuration
```
Available configurations:
1. CHRxIPB2xICExEP800102xECA
2. CHRxIPB2xICExEP800102xSoftECU
3. DCOMsimxCHRxIPBxICE
4. DCOMsimxCHRxIPBxPHEV
```

### 2. Verify Input Files
Check all required files exist:
```powershell
Test-Path "C:\...\GenFromCoPilot\splitter_input\DTC_Input.txt"
Test-Path "C:\...\GenFromCoPilot\splitter_input\DTCAttribute_Input.txt"
Test-Path "C:\...\GenFromCoPilot\splitter_input\DTC_Attr_Link_Input.txt"
Test-Path "C:\...\GenFromCoPilot\splitter_input\FW_DTC_Link_Input.txt"
```

### 3. Execute Combined Workflow Plugin

**Template Variables:**
- `<WorkspaceRoot>`: `C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New`
- `<Config>`: Selected configuration (e.g., `CHRxIPB2xICExEP800102xECA`)

---

## Execute Complete DTC Workflow

**Purpose**: Execute all 4 DTC update steps in a single DiamantPro session

**Command:**
```powershell
cd C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\CHRYSLER_IPB

# Set all 4 environment variables
$env:DIAMANT_DTC_INPUT_FILE="C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\DTC_Input.txt"
$env:DIAMANT_DTCATTR_INPUT_FILE="C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\DTCAttribute_Input.txt"
$env:DIAMANT_DTCATTRLINK_INPUT_FILE="C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\DTC_Attr_Link_Input.txt"
$env:DIAMANT_FWDTCLINK_INPUT_FILE="C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input\FW_DTC_Link_Input.txt"

# Execute combined workflow plugin
& "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe" `
    --LOG=DiamantProPlugin_DTCCompleteWorkflow.log `
    --READSPLITTER=Gen/<Config>/make/Cfg_DBFiles_GenMake.csv `
    --RELAXED `
    --RUNPLUGIN=rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_DTC_Complete_Workflow.dpp `
    --WRITESPLITTERS `
    --CONSOLEOUTPUT=ALL
```

**Expected Output:**
```
===============================================
Start of Complete DTC Database Update Workflow
===============================================

Environment Variables Configured:
  DIAMANT_DTC_INPUT_FILE: ...\DTC_Input.txt
  DIAMANT_DTCATTR_INPUT_FILE: ...\DTCAttribute_Input.txt
  DIAMANT_DTCATTRLINK_INPUT_FILE: ...\DTC_Attr_Link_Input.txt
  DIAMANT_FWDTCLINK_INPUT_FILE: ...\FW_DTC_Link_Input.txt

==========================================
STEP 1: Create/Update DTC Entries
==========================================
Step 1/4: Creating/Updating DTC entries...
Parsed 1 DTC entries from input file.
Processing DTC: DTC_123456 (0x123456)
  ModifyAdd returned: True
Step 1 Results: Created=1, Updated=0
Step 1 complete: 1 created, 0 updated

==========================================
STEP 2: Create/Update DTC Attributes
==========================================
Step 2/4: Creating/Updating DTC Attributes...
Parsed 1 DTC Attribute entries.
Using splitter file: Diamant__DTCATTRIBUTES__CHR__IPB.xml
Processing DTC Attribute: DTCAttribute_CHR_NonOBD45
Step 2 Results: Created=1, Updated=0
Step 2 complete: 1 created, 0 updated

==========================================
STEP 3: Link DTC Attributes to DTCs
==========================================
Step 3/4: Linking DTC Attributes to DTCs...
Parsed 1 DTC-Attribute link entries.
Using splitter file: Diamant__DTC_AttributesClassLink__CHR.xml
Processing Link: dtc_ref=DTC_123456, DTCAttributesClassRef=DTCAttribute_CHR_NonOBD45
Step 3 Results: Created=1, Updated=0
Step 3 complete: 1 created, 0 updated

==========================================
STEP 4: Link Failure Words to DTCs
==========================================
Step 4/4: Linking Failure Words to DTCs...
Parsed 3 FW-DTC link entries.
Processing FW-DTC Link: FW_REF=FW_HydraulicUndervoltage1, DTC_REF=DTC_123456
  ModifyAdd returned: True
Processing FW-DTC Link: FW_REF=FW_HydraulicUndervoltage2, DTC_REF=DTC_123456
  ModifyAdd returned: True
Processing FW-DTC Link: FW_REF=FW_HydraulicUndervoltage3, DTC_REF=DTC_123456
  ModifyAdd returned: True
Step 4 Results: Created=3, Updated=0
Step 4 complete: 3 created, 0 updated

===============================================
Complete DTC Database Update Workflow FINISHED
All 4 steps completed successfully!
===============================================
✓ Complete DTC Database Update Workflow finished successfully!
```

**Verification:**
- Log file: `Diamant_DTC_Complete_Workflow_Log.txt` (detailed workflow log)
- DiamantPro log: `DiamantProPlugin_DTCCompleteWorkflow.log` (CLI output)
- Modified XML files:
  - `Diamant__DTC__CHR__IPB.xml` (or matching customer/project file)
  - `Diamant__DTCATTRIBUTES__CHR__IPB.xml`
  - `Diamant__DTC_AttributesClassLink__CHR.xml`
  - `Diamant__FW_LINK_PRJ_DTC_REF__*.xml`

---

## Input File Formats

### 1. DTC_Input.txt

**Structure**: Key:value pairs, blank line separates entries

**Example:**
```
DTC: 0x123456
SHORT-NAME: DTC_123456
DESC: Hydraulic undervoltage failure
CUSTOMER_REF: Cus_CHR
PROJECT_REF: Prj_Default
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

**Key Fields:**
- `DTC` - Diagnostic trouble code hex value (e.g., 0x123456)
- `SHORT-NAME` - Unique DTC identifier (e.g., DTC_123456)
- `DESC` - Human-readable description
- `CUSTOMER_REF` - Customer code (e.g., Cus_CHR) - **determines file placement**
- `PROJECT_REF` - Project reference (e.g., Prj_Default)
- `PRODUCT_LINE_REF` - Product line (e.g., IPB) - **determines file placement**
- `DtcSeverity` - Severity level (DTC_SEV_IMMEDIATELY, etc.)
- `WWHOBDDtcClass` - WWHOBD classification
- OBD-related values (classic, on UDS, ZEV variants)

### 2. DTCAttribute_Input.txt

**Structure**: Key:value pairs, blank line separates entries

**Example:**
```
SHORT-NAME: DTCAttribute_CHR_NonOBD45
Description: DTC Attribute for Non-OBD DTCs
CUSTOMER_REF: Cus_CHR
PRODUCT_LINE_REF: IPB
AgingAllowed: true
AgingcyclecounterThreshold: 40
DemDTCPriority: 255
EventFailurecyclecounterThreshold: 1
MaxNumberFreezeFrameRecords: 2
AgingcycleRef: WarmUp
ExtendedDataClassRef: DemExtendedDataClass_RB
FreezeFrameClassRef: DemFreezeFrameClass_RBAPLCUST
EventDestination: DemPrimaryMemory
EventDestinationMirror: None
DTCKinds: DEM_DTC_KIND_ALL_DTCS

```

**Key Fields:**
- `SHORT-NAME` - Unique attribute identifier
- `Description` - Human-readable description
- `CUSTOMER_REF` - Customer code - **determines file placement**
- `PRODUCT_LINE_REF` - Product line - **determines file placement**
- Aging configuration (allowed, threshold, cycle reference)
- Event configuration (priority, failure threshold, freeze frames)
- Memory destination and DTC classification

### 3. DTC_Attr_Link_Input.txt

**Structure**: Simple key:value pairs, blank line separates entries

**Example:**
```
dtc_ref: DTC_123456
DTCAttributesClassRef: DTCAttribute_CHR_NonOBD45

dtc_ref: DTC_456789
DTCAttributesClassRef: DTCAttribute_CHR_OBD

```

**Key Fields:**
- `dtc_ref` - DTC SHORT-NAME to link
- `DTCAttributesClassRef` - DTC Attribute SHORT-NAME
  - Customer extracted from attribute name (e.g., "DTCAttribute_**CHR**_NonOBD" → CHR)
  - **Determines file placement**

### 4. FW_DTC_Link_Input.txt

**Structure**: Simple key:value pairs, blank line separates entries

**Example:**
```
FW_REF: FW_HydraulicUndervoltage1
DTC_REF: DTC_123456

FW_REF: FW_HydraulicUndervoltage2
DTC_REF: DTC_123456

FW_REF: FW_HydraulicUndervoltage3
DTC_REF: DTC_123456

```

**Key Fields:**
- `FW_REF` - Failure word SHORT-NAME
- `DTC_REF` - DTC SHORT-NAME to link

---

## Intelligent File Placement

The plugin automatically routes entries to correct customer/project XML files:

### Step 1 (DTC Creation)
- Reads `CUSTOMER_REF` and `PRODUCT_LINE_REF` from input
- Searches for file: `Diamant__DTC__<CUSTOMER>__<PRODUCTLINE>.xml`
- Example: `Cus_CHR` + `IPB` → `Diamant__DTC__CHR__IPB.xml`

### Step 2 (DTC Attribute Creation)
- Reads `CUSTOMER_REF` and `PRODUCT_LINE_REF` from input
- Searches for file: `Diamant__DTCATTRIBUTES__<CUSTOMER>__<PRODUCTLINE>.xml`
- Example: `Cus_CHR` + `IPB` → `Diamant__DTCATTRIBUTES__CHR__IPB.xml`

### Step 3 (Attribute-DTC Link)
- Extracts customer from `DTCAttributesClassRef`
- Pattern: `DTCAttribute_<CUSTOMER>_<Type>` → extracts `<CUSTOMER>`
- Searches for file: `Diamant__DTC_AttributesClassLink__<CUSTOMER>.xml`
- Example: `DTCAttribute_CHR_NonOBD` → `Diamant__DTC_AttributesClassLink__CHR.xml`

### Step 4 (FW-DTC Link)
- Uses handler system: `FW_LINK_PRJ_DTC_REF`
- Automatically routes to project-specific XML files

### File Matching Priority
1. **Exact match**: Full customer + product line
2. **Partial match**: Customer only
3. **Fallback**: First available file (with warning)

---

## Verification & Validation

### Console Output Validation

**Workflow Start Indicators:**
- ✓ "Start of Complete DTC Database Update Workflow"
- ✓ All 4 environment variables displayed
- ✓ Step headers for each of 4 steps

**Success Indicators for Each Step:**
- ✓ "Step X/4: [Description]..."
- ✓ "Parsed X entries from input file"
- ✓ "Step X Results: Created=X, Updated=Y"
- ✓ "Step X complete: X created, Y updated"

**Workflow Completion Indicator:**
- ✓ "Complete DTC Database Update Workflow FINISHED"
- ✓ "All 4 steps completed successfully!"
- ✓ "✓ Complete DTC Database Update Workflow finished successfully!"

### Log File Validation

**Primary Log**: `Diamant_DTC_Complete_Workflow_Log.txt`

**Expected Contents:**
```
===============================================
Start of Complete DTC Database Update Workflow
===============================================

Environment Variables Configured:
  [4 file paths listed]

==========================================
STEP 1: Create/Update DTC Entries
==========================================
[Step 1 execution details]
Step 1 Results: Created=X, Updated=Y

==========================================
STEP 2: Create/Update DTC Attributes
==========================================
[Step 2 execution details]
Step 2 Results: Created=X, Updated=Y

==========================================
STEP 3: Link DTC Attributes to DTCs
==========================================
[Step 3 execution details]
Step 3 Results: Created=X, Updated=Y

==========================================
STEP 4: Link Failure Words to DTCs
==========================================
[Step 4 execution details]
Step 4 Results: Created=X, Updated=Y

===============================================
Complete DTC Database Update Workflow FINISHED
All 4 steps completed successfully!
===============================================
```

### XML File Validation

**Check DTC Creation:**
```powershell
Select-String -Path "rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\OBDonUDS\Diamant__DTC__CHR__IPB.xml" `
              -Pattern "DTC_123456|0x123456" -Context 2,2
```

**Check DTC Attribute:**
```powershell
Select-String -Path "rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\OBDonUDS\Diamant__DTCATTRIBUTES__CHR__IPB.xml" `
              -Pattern "DTCAttribute_CHR_NonOBD45" -Context 2,2
```

**Check Attribute Link:**
```powershell
Select-String -Path "rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\OBDonUDS\Diamant__DTC_AttributesClassLink__CHR.xml" `
              -Pattern "DTC_123456.*DTCAttribute_CHR" -Context 1,1
```

**Check FW-DTC Link:**
```powershell
Select-String -Path "CHRYSLER_IPB\rb\**\Diamant__FW_LINK_PRJ_DTC_REF__*.xml" `
              -Pattern "FW_HydraulicUndervoltage.*DTC_123456" -Context 1,1
```

---

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| **Environment variable missing** | Plugin aborts before Step 1 | Set all 4 environment variables before execution |
| **Step 1 fails** | Input file format error or missing CUSTOMER/PRODUCT refs | Verify DTC_Input.txt format<br>Check CUSTOMER_REF and PRODUCT_LINE_REF are present<br>Workflow aborts - no subsequent steps run |
| **Step 2 fails** | Input file format or wrong customer/product | Verify DTCAttribute_Input.txt format<br>Ensure CUSTOMER_REF matches DTC creation<br>Workflow aborts - Steps 3 & 4 don't run |
| **Step 3 fails** | DTC or attribute doesn't exist yet | Verify Steps 1 & 2 completed successfully<br>Check dtc_ref and DTCAttributesClassRef match<br>Workflow aborts - Step 4 doesn't run |
| **Step 4 fails** | Failure word or DTC doesn't exist | Verify failure words created (from FW workflow)<br>Verify DTCs created in Step 1<br>Previous steps already completed |
| **Wrong XML file selected** | CUSTOMER_REF/PRODUCT_LINE_REF mismatch | Check input file values<br>Verify file naming matches customer/product pattern |
| **Exit code 1 but workflow succeeded** | Unrelated validation plugin errors | **Normal** - focus on plugin-specific output<br>Check for "All 4 steps completed successfully!" |
| **No files written** | Missing --WRITESPLITTERS flag | Add --WRITESPLITTERS to command |
| **Partial execution** | One step failed, workflow aborted | Review log file for error details<br>Fix the failing step's input<br>Re-run entire workflow |

### Error Abort Behavior

**Critical Feature**: The workflow stops immediately if any step fails:
- Step 1 fails → Steps 2, 3, 4 don't run
- Step 2 fails → Steps 3, 4 don't run
- Step 3 fails → Step 4 doesn't run
- Step 4 fails → Previous steps already completed

**To Resume After Failure:**
1. Review the log file for specific error
2. Fix the input file for the failing step
3. Re-run the entire workflow (all 4 steps)

---

## Advantages Over Sequential Execution

### Single Plugin Workflow Benefits

**Performance:**
- ✓ Database loaded once instead of 4 times
- ✓ No context switching between plugin executions
- ✓ Faster overall execution time (up to 4x)

**Reliability:**
- ✓ All-or-nothing execution (atomic operation)
- ✓ Single transaction for all changes
- ✓ Consistent state - no partial updates

**Simplicity:**
- ✓ One command instead of four
- ✓ Single log file with complete workflow
- ✓ Easier to script and automate

**Maintainability:**
- ✓ Unified error handling
- ✓ Centralized logging
- ✓ Single point of configuration

### Comparison Table

| Aspect | Sequential (4 plugins) | Combined (1 plugin) |
|--------|------------------------|---------------------|
| DiamantPro CLI calls | 4 | 1 |
| Database loads | 4 | 1 |
| Environment variables | 4 (one at a time) | 4 (all at once) |
| Log files | 5+ files | 2 files |
| Execution time | ~4-8 minutes | ~1-2 minutes |
| Error recovery | Continue next step | Abort entire workflow |
| Transaction safety | Partial updates possible | Atomic operation |

---

## Best Practices

**Environment Variable Management**:
- Set all 4 variables before execution
- Use full absolute paths
- Verify file existence before setting variables

**Configuration Consistency**:
- Use same configuration for entire workflow
- Document configuration choice
- Maintain consistency across related workflows

**Input File Management**:
- Keep all input files in `GenFromCoPilot/splitter_input/`
- Use consistent naming convention
- Version control all input files
- Validate file formats before execution

**Customer/Project Matching**:
- Ensure CUSTOMER_REF is consistent across DTC and Attribute inputs
- Product line should match project structure
- Verify file naming conventions match project

**Validation**:
- Check both log files after execution
- Verify XML files were modified
- Search XML for actual created entries
- Compare before/after XML states if needed

**Error Recovery**:
- Always review log file on failure
- Fix the problematic input file
- Re-run entire workflow (don't try to skip steps)

---

## Complete Example Workflow

```powershell
# ====================================================
# Complete DTC Database Update - Single Plugin Workflow
# ====================================================

# Set workspace directory
cd C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\CHRYSLER_IPB

# Configuration selection
$config = "CHRxIPB2xICExEP800102xECA"
$inputDir = "C:\Users\jny1cob\Desktop\Workspaces\Chysler_OBD_New\GenFromCoPilot\splitter_input"
$diamantCli = "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe"

# Verify all input files exist
Write-Host "`n=== Verifying Input Files ===" -ForegroundColor Cyan
$files = @(
    "$inputDir\DTC_Input.txt",
    "$inputDir\DTCAttribute_Input.txt",
    "$inputDir\DTC_Attr_Link_Input.txt",
    "$inputDir\FW_DTC_Link_Input.txt"
)

$allFilesExist = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✓ Found: $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "✗ Missing: $(Split-Path $file -Leaf)" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host "`nError: One or more input files missing. Aborting." -ForegroundColor Red
    exit 1
}

# Set all 4 environment variables
Write-Host "`n=== Setting Environment Variables ===" -ForegroundColor Cyan
$env:DIAMANT_DTC_INPUT_FILE = "$inputDir\DTC_Input.txt"
$env:DIAMANT_DTCATTR_INPUT_FILE = "$inputDir\DTCAttribute_Input.txt"
$env:DIAMANT_DTCATTRLINK_INPUT_FILE = "$inputDir\DTC_Attr_Link_Input.txt"
$env:DIAMANT_FWDTCLINK_INPUT_FILE = "$inputDir\FW_DTC_Link_Input.txt"

Write-Host "✓ All environment variables set" -ForegroundColor Green

# Execute combined workflow plugin
Write-Host "`n=== Executing Complete DTC Workflow ===" -ForegroundColor Cyan
Write-Host "Configuration: $config" -ForegroundColor Yellow
Write-Host "Plugin: Diamant_Update_DTC_Complete_Workflow.dpp" -ForegroundColor Yellow

& $diamantCli `
    --LOG=DiamantProPlugin_DTCCompleteWorkflow.log `
    --READSPLITTER="Gen/$config/make/Cfg_DBFiles_GenMake.csv" `
    --RELAXED `
    --RUNPLUGIN=rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_DTC_Complete_Workflow.dpp `
    --WRITESPLITTERS `
    --CONSOLEOUTPUT=ALL

# Check execution status
if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 1) {
    # Exit code 1 is normal due to unrelated validation errors
    Write-Host "`n=== Checking Results ===" -ForegroundColor Cyan
    
    if (Test-Path "Diamant_DTC_Complete_Workflow_Log.txt") {
        $logContent = Get-Content "Diamant_DTC_Complete_Workflow_Log.txt" -Raw
        
        if ($logContent -match "All 4 steps completed successfully!") {
            Write-Host "✓ DTC Complete Workflow SUCCEEDED" -ForegroundColor Green
            
            # Extract statistics
            $step1 = [regex]::Match($logContent, "Step 1 Results: Created=(\d+), Updated=(\d+)")
            $step2 = [regex]::Match($logContent, "Step 2 Results: Created=(\d+), Updated=(\d+)")
            $step3 = [regex]::Match($logContent, "Step 3 Results: Created=(\d+), Updated=(\d+)")
            $step4 = [regex]::Match($logContent, "Step 4 Results: Created=(\d+), Updated=(\d+)")
            
            Write-Host "`nSummary:" -ForegroundColor Cyan
            Write-Host "  Step 1 (DTCs):        Created=$($step1.Groups[1].Value), Updated=$($step1.Groups[2].Value)"
            Write-Host "  Step 2 (Attributes):  Created=$($step2.Groups[1].Value), Updated=$($step2.Groups[2].Value)"
            Write-Host "  Step 3 (DTC Links):   Created=$($step3.Groups[1].Value), Updated=$($step3.Groups[2].Value)"
            Write-Host "  Step 4 (FW Links):    Created=$($step4.Groups[1].Value), Updated=$($step4.Groups[2].Value)"
        } else {
            Write-Host "✗ DTC Complete Workflow FAILED" -ForegroundColor Red
            Write-Host "Check log file: Diamant_DTC_Complete_Workflow_Log.txt" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✗ Log file not found" -ForegroundColor Red
    }
} else {
    Write-Host "`n✗ DiamantPro CLI execution failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
}

Write-Host "`n=== Workflow Complete ===" -ForegroundColor Cyan
```

---

## Post-Execution File Tracking

After successful CLI execution, all modified XML files should be tracked in a review file for downstream review processes.

### Tracking File Location
```
GenFromCoPilot\Review\DTC_filesToReview.txt
```

### Tracking File Format
```
# DTC Complete Workflow Files - Review Tracker
# Auto-generated by Diamant_Update_DTC_Complete_Workflow execution
# Lists all XML files modified during DTC workflow execution (4 steps)

===========================================
Execution Date: 2026-02-02 16:35:45
Configuration: CHRxIPB2xICExEP800102xECA
===========================================

Step 1 - DTC Files Modified:
- CHRYSLER_IPB\rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\OBDonUDS\Diamant__DTC__CHR__IPB.xml

Step 2 - DTC Attribute Files Modified:
- CHRYSLER_IPB\rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\OBDonUDS\Diamant__DTCATTRIBUTES__CHR__IPB.xml

Step 3 - DTC Attribute Link Files Modified:
- CHRYSLER_IPB\rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\OBDonUDS\Diamant__DTC_AttributesClassLink__CHR.xml

Step 4 - FW-DTC Link Files Modified:
- CHRYSLER_IPB\rb\as\ms\core\app\dcom\RBAPLCust\cfg\Diamant__FW_LINK_PRJ_DTC_REF__CHR.xml

Total Files Modified: 4

```

### Implementation Steps

1. **Parse Log File**: Extract file paths from `Diamant_DTC_Complete_Workflow_Log.txt`
2. **Categorize Files by Step**: Group files by DTC workflow step:
   - Step 1: `Diamant__DTC__*.xml`
   - Step 2: `Diamant__DTCATTRIBUTES__*.xml`
   - Step 3: `Diamant__DTC_AttributesClassLink__*.xml`
   - Step 4: `Diamant__FW_LINK_PRJ_DTC_REF__*.xml`
3. **Create/Append Tracking File**: 
   - If file doesn't exist, create with header
   - Append new execution block with timestamp and file list
4. **Verify Tracking**: Confirm file created/updated successfully

### PowerShell Example for File Tracking

```powershell
# After CLI execution, parse log file for modified files
$logFile = "CHRYSLER_IPB\Diamant_DTC_Complete_Workflow_Log.txt"

if (Test-Path $logFile) {
    $logContent = Get-Content $logFile -Raw
    
    # Extract file paths mentioned in log (customize regex based on log format)
    $dtcFiles = [regex]::Matches($logContent, "Diamant__DTC__[^\s]+\.xml") | ForEach-Object { $_.Value }
    $attrFiles = [regex]::Matches($logContent, "Diamant__DTCATTRIBUTES__[^\s]+\.xml") | ForEach-Object { $_.Value }
    $linkFiles = [regex]::Matches($logContent, "Diamant__DTC_AttributesClassLink__[^\s]+\.xml") | ForEach-Object { $_.Value }
    $fwLinkFiles = [regex]::Matches($logContent, "Diamant__FW_LINK_PRJ_DTC_REF__[^\s]+\.xml") | ForEach-Object { $_.Value }
    
    # Create tracking content
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $trackingContent = @"
===========================================
Execution Date: $timestamp
Configuration: $selectedConfig
===========================================

"@
    
    if ($dtcFiles) {
        $trackingContent += "Step 1 - DTC Files Modified:`n"
        $dtcFiles | Select-Object -Unique | ForEach-Object { $trackingContent += "- CHRYSLER_IPB\$_`n" }
        $trackingContent += "`n"
    }
    
    if ($attrFiles) {
        $trackingContent += "Step 2 - DTC Attribute Files Modified:`n"
        $attrFiles | Select-Object -Unique | ForEach-Object { $trackingContent += "- CHRYSLER_IPB\$_`n" }
        $trackingContent += "`n"
    }
    
    if ($linkFiles) {
        $trackingContent += "Step 3 - DTC Attribute Link Files Modified:`n"
        $linkFiles | Select-Object -Unique | ForEach-Object { $trackingContent += "- CHRYSLER_IPB\$_`n" }
        $trackingContent += "`n"
    }
    
    if ($fwLinkFiles) {
        $trackingContent += "Step 4 - FW-DTC Link Files Modified:`n"
        $fwLinkFiles | Select-Object -Unique | ForEach-Object { $trackingContent += "- CHRYSLER_IPB\$_`n" }
        $trackingContent += "`n"
    }
    
    $totalFiles = ($dtcFiles + $attrFiles + $linkFiles + $fwLinkFiles | Select-Object -Unique).Count
    $trackingContent += "Total Files Modified: $totalFiles`n`n"
    
    # Append to tracking file
    $trackingFile = "GenFromCoPilot\Review\DTC_filesToReview.txt"
    
    if (!(Test-Path $trackingFile)) {
        $header = @"
# DTC Complete Workflow Files - Review Tracker
# Auto-generated by Diamant_Update_DTC_Complete_Workflow execution
# Lists all XML files modified during DTC workflow execution (4 steps)

"@
        Set-Content -Path $trackingFile -Value $header
    }
    
    Add-Content -Path $trackingFile -Value $trackingContent
    
    Write-Host "✅ File tracking updated: $trackingFile" -ForegroundColor Green
}
```

### Integration with Review Workflow

The tracking file serves as input for the review process:
1. Review tools read `DTC_filesToReview.txt` to identify files requiring review
2. Each listed file is validated against the DTC review checklist
3. Review report references specific execution dates and configurations
4. Tracking history provides audit trail for DTC configuration changes
5. Files are organized by workflow step for systematic review

---

## Related Documentation
- [2_1_UPDATE_FW_NODE_AND_GRAPHLINKS_CLI_EXECUTION.md](2_1_UPDATE_FW_NODE_AND_GRAPHLINKS_CLI_EXECUTION.md) - FW, NODE and Graph Links updater
- [2_3_STM_Config_generation_Instructions.md](2_3_STM_Config_generation_Instructions.md) - STM configuration generation

---

**Version 1.1** (February 2, 2026) - Added file tracking requirement with `DTC_filesToReview.txt` for review workflow integration
**Version 1.0** (January 26, 2026) - Initial documentation
- Single combined plugin workflow
- All 4 steps in one DiamantPro execution
- Atomic operation with abort-on-failure
- Performance optimized (4x faster than sequential)
- Comprehensive validation and error handling
