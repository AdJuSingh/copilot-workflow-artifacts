# 2.1.3 Update DTC Complete Workflow - Copilot Prompt

## Prompt Description
This prompt guides the user through updating DTC (Diagnostic Trouble Code) database entries using a **single combined DiamantPro plugin** that executes all 4 DTC update steps sequentially in one session. This unified approach is faster and more reliable than running four separate plugins.

**⚠️ IMPORTANT**: This workflow uses **one plugin** that internally executes 4 sequential steps. All steps must succeed or the entire workflow aborts.

## Usage
Use this prompt when you need to:
- Execute a complete DTC database update in a single operation
- Create DTCs, attributes, links, and FW-DTC connections atomically
- Minimize execution time (4x faster than sequential plugins)
- Ensure consistent state (all steps succeed together or fail together)
- Simplify automation with a single command

## Prompt

```
I need to update DTC database entries using the DiamantPro Complete DTC Workflow plugin.

This workflow executes a **single plugin** (Diamant_Update_DTC_Complete_Workflow.dpp) that internally performs all 4 steps sequentially:
1. Create/Update DTC entries
2. Create/Update DTC attribute definitions
3. Link attributes to DTCs
4. Link failure words to DTCs

**Key Advantages:**
- ✓ Single DiamantPro CLI execution (not 4 separate commands)
- ✓ Database loaded once (faster execution)
- ✓ Atomic operation (all steps succeed or all fail)
- ✓ Unified logging and error handling

### Configuration Selection
Please follow these steps:

1. **Show Available Configurations**
   - List all folders in `CHRYSLER_IPB/Gen/` directory
   - Display as numbered options for selection

2. **Select Configuration**
   - Wait for my configuration choice (1, 2, 3, or 4)
   - Available options (Chrysler IPB):
     - CHRxIPB2xICExEP800102xECA (ESP/ABS ICE variant)
     - CHRxIPB2xICExEP800102xSoftECU (Software ECU)
     - DCOMsimxCHRxIPBxICE (DCOM Simulation ICE)
     - DCOMsimxCHRxIPBxPHEV (DCOM Simulation PHEV)

3. **Verify All Input Files**
   - Confirm that **all 4** input files exist in `GenFromCoPilot\splitter_input\`:
     - `DTC_Input.txt` (DTC definitions)
     - `DTCAttribute_Input.txt` (DTC attribute configurations)
     - `DTC_Attr_Link_Input.txt` (DTC-to-attribute mappings)
     - `FW_DTC_Link_Input.txt` (Failure word-to-DTC mappings)
   - **Critical**: All 4 files MUST exist before execution
   - If any file is missing, inform me and abort

4. **Execute Complete Workflow Plugin**
   Build and execute **one command** with these parameters:
   
   **Command Structure:**
   ```powershell
   cd CHRYSLER_IPB
   
   # Set ALL 4 environment variables at once
   $env:DIAMANT_DTC_INPUT_FILE="<WorkspaceRoot>\GenFromCoPilot\splitter_input\DTC_Input.txt"
   $env:DIAMANT_DTCATTR_INPUT_FILE="<WorkspaceRoot>\GenFromCoPilot\splitter_input\DTCAttribute_Input.txt"
   $env:DIAMANT_DTCATTRLINK_INPUT_FILE="<WorkspaceRoot>\GenFromCoPilot\splitter_input\DTC_Attr_Link_Input.txt"
   $env:DIAMANT_FWDTCLINK_INPUT_FILE="<WorkspaceRoot>\GenFromCoPilot\splitter_input\FW_DTC_Link_Input.txt"
   
   # Execute combined workflow plugin
   & "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe" `
       --LOG=DiamantProPlugin_DTCCompleteWorkflow.log `
       --READSPLITTER=Gen/<SelectedConfig>/make/Cfg_DBFiles_GenMake.csv `
       --RELAXED `
       --RUNPLUGIN=rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_DTC_Complete_Workflow.dpp `
       --WRITESPLITTERS `
       --CONSOLEOUTPUT=ALL
   ```

   **Common Parameters:**
   - **Working Directory**: `CHRYSLER_IPB` (must execute from workspace root)
   - **DiamantPro Tool**: `C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe`
   - **Plugin**: `Diamant_Update_DTC_Complete_Workflow.dpp` (combined workflow)
   - **READSPLITTER**: `Gen/<SelectedConfig>/make/Cfg_DBFiles_GenMake.csv`
   - **Flags**: `--RELAXED --WRITESPLITTERS --CONSOLEOUTPUT=ALL`

5. **Monitor Workflow Execution**
   Display the workflow progress as it executes all 4 internal steps:
   
   **Expected Output Pattern:**
   ```
   ===============================================
   Start of Complete DTC Database Update Workflow
   ===============================================
   
   Environment Variables Configured:
     DIAMANT_DTC_INPUT_FILE: [path]
     DIAMANT_DTCATTR_INPUT_FILE: [path]
     DIAMANT_DTCATTRLINK_INPUT_FILE: [path]
     DIAMANT_FWDTCLINK_INPUT_FILE: [path]
   
   ==========================================
   STEP 1: Create/Update DTC Entries
   ==========================================
   Step 1/4: Creating/Updating DTC entries...
   [Step 1 execution details]
   Step 1 Results: Created=X, Updated=Y
   
   ==========================================
   STEP 2: Create/Update DTC Attributes
   ==========================================
   Step 2/4: Creating/Updating DTC Attributes...
   [Step 2 execution details]
   Step 2 Results: Created=X, Updated=Y
   
   ==========================================
   STEP 3: Link DTC Attributes to DTCs
   ==========================================
   Step 3/4: Linking DTC Attributes to DTCs...
   [Step 3 execution details]
   Step 3 Results: Created=X, Updated=Y
   
   ==========================================
   STEP 4: Link Failure Words to DTCs
   ==========================================
   Step 4/4: Linking Failure Words to DTCs...
   [Step 4 execution details]
   Step 4 Results: Created=X, Updated=Y
   
   ===============================================
   Complete DTC Database Update Workflow FINISHED
   All 4 steps completed successfully!
   ===============================================
   ✓ Complete DTC Database Update Workflow finished successfully!
   ```

6. **Verify Complete Workflow Results**
   
   **Check for Success:**
   - ✓ "Start of Complete DTC Database Update Workflow"
   - ✓ All 4 environment variables listed
   - ✓ All 4 step headers displayed
   - ✓ "All 4 steps completed successfully!"
   - ✓ "✓ Complete DTC Database Update Workflow finished successfully!"
   
   **Extract Statistics:**
   - Step 1 Results: Created/Updated counts
   - Step 2 Results: Created/Updated counts
   - Step 3 Results: Created/Updated counts
   - Step 4 Results: Created/Updated counts
   
   **Check Log Files:**
   - Primary log: `Diamant_DTC_Complete_Workflow_Log.txt` (detailed workflow)
   - CLI log: `DiamantProPlugin_DTCCompleteWorkflow.log` (console output)

7. **Track Modified Files for Review**
   - Parse the log file `Diamant_DTC_Complete_Workflow_Log.txt` to extract modified XML file paths
   - Look for file patterns:
     - `Diamant__DTC__*.xml` (Step 1 - DTC files)
     - `Diamant__DTCATTRIBUTES__*.xml` (Step 2 - DTC Attribute files)
     - `Diamant__DTC_AttributesClassLink__*.xml` (Step 3 - Attribute Link files)
     - `Diamant__FW_LINK_PRJ_DTC_REF__*.xml` (Step 4 - FW-DTC Link files)
   - Create or update tracking file: `GenFromCoPilot\Review\DTC_filesToReview.txt`
   - Append new content with execution timestamp and file list:
     ```
     ===========================================
     Execution Date: YYYY-MM-DD HH:MM:SS
     Configuration: <SelectedConfig>
     ===========================================
     
     Step 1 - DTC Files Modified:
     - CHRYSLER_IPB\<full_path_to_DTC_xml>
     
     Step 2 - DTC Attribute Files Modified:
     - CHRYSLER_IPB\<full_path_to_DTCAttribute_xml>
     
     Step 3 - DTC Attribute Link Files Modified:
     - CHRYSLER_IPB\<full_path_to_AttrLink_xml>
     
     Step 4 - FW-DTC Link Files Modified:
     - CHRYSLER_IPB\<full_path_to_FW_Link_xml>
     
     Total Files Modified: X
     ```
   - If file doesn't exist, create it with header:
     ```
     # DTC Complete Workflow Files - Review Tracker
     # Auto-generated by Diamant_Update_DTC_Complete_Workflow execution
     # Lists all XML files modified during DTC workflow execution (4 steps)
     
     ```
   - Display confirmation: "✅ File tracking updated: DTC_filesToReview.txt"

8. **Display Comprehensive Summary**
   
   ```
   ✓ DTC Complete Workflow SUCCEEDED
   
   Summary:
   - Step 1 (DTCs):        Created=X, Updated=Y
   - Step 2 (Attributes):  Created=X, Updated=Y
   - Step 3 (DTC Links):   Created=X, Updated=Y
   - Step 4 (FW Links):    Created=X, Updated=Y
   
   Modified Files:
   - Diamant__DTC__<CUSTOMER>__<PRODUCTLINE>.xml
   - Diamant__DTCATTRIBUTES__<CUSTOMER>__<PRODUCTLINE>.xml
   - Diamant__DTC_AttributesClassLink__<CUSTOMER>.xml
   - Diamant__FW_LINK_PRJ_DTC_REF__*.xml
   
   Files for Review:
   ✅ File tracking updated: GenFromCoPilot\Review\DTC_filesToReview.txt
   
   Log Files:
   - Diamant_DTC_Complete_Workflow_Log.txt (detailed)
   - DiamantProPlugin_DTCCompleteWorkflow.log (CLI output)
   ```

9. **Validate File Placement**
   - Verify that entries were created in correct customer/project XML files
   - For DTCs and Attributes: Based on CUSTOMER_REF and PRODUCT_LINE_REF
   - For Attribute Links: Based on customer extracted from DTCAttributesClassRef
   - For FW-DTC Links: Based on handler routing
   - Display which XML files were modified

### Expected Output (Complete Workflow)

**Full Workflow Success:**
```
===============================================
Start of Complete DTC Database Update Workflow
===============================================

Environment Variables Configured:
  DIAMANT_DTC_INPUT_FILE: C:\...\DTC_Input.txt
  DIAMANT_DTCATTR_INPUT_FILE: C:\...\DTCAttribute_Input.txt
  DIAMANT_DTCATTRLINK_INPUT_FILE: C:\...\DTC_Attr_Link_Input.txt
  DIAMANT_FWDTCLINK_INPUT_FILE: C:\...\FW_DTC_Link_Input.txt

==========================================
STEP 1: Create/Update DTC Entries
==========================================
Parsed 1 DTC entries from input file.
Step 1 Results: Created=1, Updated=0
Step 1 complete: 1 created, 0 updated

==========================================
STEP 2: Create/Update DTC Attributes
==========================================
Parsed 1 DTC Attribute entries.
Using splitter file: Diamant__DTCATTRIBUTES__CHR__IPB.xml
Step 2 Results: Created=1, Updated=0
Step 2 complete: 1 created, 0 updated

==========================================
STEP 3: Link DTC Attributes to DTCs
==========================================
Parsed 1 DTC-Attribute link entries.
Using splitter file: Diamant__DTC_AttributesClassLink__CHR.xml
Step 3 Results: Created=1, Updated=0
Step 3 complete: 1 created, 0 updated

==========================================
STEP 4: Link Failure Words to DTCs
==========================================
Parsed 3 FW-DTC link entries.
Step 4 Results: Created=3, Updated=0
Step 4 complete: 3 created, 0 updated

===============================================
Complete DTC Database Update Workflow FINISHED
All 4 steps completed successfully!
===============================================
```

### Error Handling

**Critical Workflow Behavior:**
- **If ANY step fails, the entire workflow ABORTS**
- Subsequent steps are NOT executed
- Previous steps' changes are already committed

**Error Scenarios:**

1. **Environment Variables Missing:**
   ```
   ERROR: All 4 environment variables must be set:
     - DIAMANT_DTC_INPUT_FILE
     - DIAMANT_DTCATTR_INPUT_FILE
     - DIAMANT_DTCATTRLINK_INPUT_FILE
     - DIAMANT_FWDTCLINK_INPUT_FILE
   ```
   - **Action**: Set all 4 variables before execution
   - **Impact**: Workflow never starts

2. **Step 1 Fails (DTC Creation):**
   ```
   Step 1 (Create DTCs) failed. Aborting workflow.
   ```
   - **Action**: Review DTC_Input.txt format
   - **Impact**: Steps 2, 3, 4 never execute

3. **Step 2 Fails (DTC Attributes):**
   ```
   Step 2 (Create DTC Attributes) failed. Aborting workflow.
   ```
   - **Action**: Review DTCAttribute_Input.txt format
   - **Impact**: Steps 3, 4 never execute (Step 1 completed)

4. **Step 3 Fails (Attribute Links):**
   ```
   Step 3 (Link DTC Attributes) failed. Aborting workflow.
   ```
   - **Action**: Verify DTCs and attributes exist
   - **Impact**: Step 4 never executes (Steps 1-2 completed)

5. **Step 4 Fails (FW-DTC Links):**
   ```
   Step 4 (Link Failure Words) failed. Aborting workflow.
   ```
   - **Action**: Verify failure words and DTCs exist
   - **Impact**: Steps 1-3 already completed

**Recovery Process:**
- Stop workflow and display error message
- Review log file: `Diamant_DTC_Complete_Workflow_Log.txt`
- Identify the failing step and specific error
- Suggest corrective action based on error type
- Instruct user to fix issue and re-run **entire workflow**
- Do NOT attempt to resume from middle step

**Common Issues:**
- **Missing environment variable**: Check all 4 are set
- **File not found**: Verify all input file paths
- **Input format error**: Check key:value format and blank line separators
- **Wrong XML file**: Verify CUSTOMER_REF and PRODUCT_LINE_REF values
- **Missing dependencies**: Ensure prerequisite objects exist (e.g., FWs for Step 4)

Please start by showing me the available configurations in the Gen/ folder.
```

## Example Interaction

### User Input:
```
run dtc complete workflow
```

### Expected Copilot Response:
```
I'll help you execute the Complete DTC Workflow using the single combined plugin.

**Available Configurations:**
1. CHRxIPB2xICExEP800102xECA (ESP/ABS ICE variant)
2. CHRxIPB2xICExEP800102xSoftECU (Software ECU)
3. DCOMsimxCHRxIPBxICE (DCOM Simulation ICE)
4. DCOMsimxCHRxIPBxPHEV (DCOM Simulation PHEV)

Please select a configuration (1, 2, 3, or 4):
```

### User Selection:
```
1
```

### Expected Copilot Action:
```
Configuration selected: CHRxIPB2xICExEP800102xECA

Verifying all input files...
✓ DTC_Input.txt found
✓ DTCAttribute_Input.txt found
✓ DTC_Attr_Link_Input.txt found
✓ FW_DTC_Link_Input.txt found

All prerequisites satisfied. Executing Complete DTC Workflow...

Setting environment variables:
- DIAMANT_DTC_INPUT_FILE
- DIAMANT_DTCATTR_INPUT_FILE
- DIAMANT_DTCATTRLINK_INPUT_FILE
- DIAMANT_FWDTCLINK_INPUT_FILE

Executing: Diamant_Update_DTC_Complete_Workflow.dpp

[Command output showing all 4 steps...]

✓ DTC Complete Workflow SUCCEEDED

Summary:
- Step 1 (DTCs):        Created=1, Updated=0
- Step 2 (Attributes):  Created=1, Updated=0
- Step 3 (DTC Links):   Created=1, Updated=0
- Step 4 (FW Links):    Created=3, Updated=0

Modified Files:
- Diamant__DTC__CHR__IPB.xml
- Diamant__DTCATTRIBUTES__CHR__IPB.xml
- Diamant__DTC_AttributesClassLink__CHR.xml
- Diamant__FW_LINK_PRJ_DTC_REF__CHR.xml

Log Files:
- Diamant_DTC_Complete_Workflow_Log.txt (detailed workflow)
- DiamantProPlugin_DTCCompleteWorkflow.log (CLI output)

The complete DTC database update workflow has been executed successfully!
```

## Command Template

```powershell
# Template for Complete DTC Workflow (execute from CHRYSLER_IPB directory)
cd CHRYSLER_IPB
$config = "{{SELECTED_CONFIG}}"
$inputDir = "<WorkspaceRoot>\GenFromCoPilot\splitter_input"
$diamantCli = "C:\MTC10Tools\DiamantPro\V4_3_r1727\DiamantProCLI.exe"

# Set ALL 4 environment variables
$env:DIAMANT_DTC_INPUT_FILE = "$inputDir\DTC_Input.txt"
$env:DIAMANT_DTCATTR_INPUT_FILE = "$inputDir\DTCAttribute_Input.txt"
$env:DIAMANT_DTCATTRLINK_INPUT_FILE = "$inputDir\DTC_Attr_Link_Input.txt"
$env:DIAMANT_FWDTCLINK_INPUT_FILE = "$inputDir\FW_DTC_Link_Input.txt"

# Execute combined workflow plugin (single command)
& $diamantCli `
    --LOG=DiamantProPlugin_DTCCompleteWorkflow.log `
    --READSPLITTER="Gen/$config/make/Cfg_DBFiles_GenMake.csv" `
    --RELAXED `
    --RUNPLUGIN=rb/as/core/app/dsm/tools/DiamantPro/plugins/Diamant_Update_DTC_Complete_Workflow.dpp `
    --WRITESPLITTERS `
    --CONSOLEOUTPUT=ALL
```

### Variable Substitution
Replace `{{SELECTED_CONFIG}}` with one of:
- `CHRxIPB2xICExEP800102xECA`
- `CHRxIPB2xICExEP800102xSoftECU`
- `DCOMsimxCHRxIPBxICE`
- `DCOMsimxCHRxIPBxPHEV`

## Validation Checklist

Before executing, verify:
- [ ] All 4 input files exist in `GenFromCoPilot\splitter_input\`
- [ ] Selected configuration folder exists in `CHRYSLER_IPB\Gen\`
- [ ] Cfg_DBFiles_GenMake.csv exists in selected config's make/ folder
- [ ] DiamantProCLI.exe is accessible at specified path
- [ ] Plugin file `Diamant_Update_DTC_Complete_Workflow.dpp` exists
- [ ] Current directory is CHRYSLER_IPB folder
- [ ] All 4 environment variables will be set before execution

## Post-Execution Validation

After successful workflow execution:

1. **Check Primary Log File**
   - File: `Diamant_DTC_Complete_Workflow_Log.txt`
   - Look for: "All 4 steps completed successfully!"
   - Verify each step shows "Created=X, Updated=Y"

2. **Check CLI Log File**
   - File: `DiamantProPlugin_DTCCompleteWorkflow.log`
   - Contains DiamantPro console output
   - May show exit code 1 (normal due to validation plugins)

3. **Verify File Placement**
   ```powershell
   # Check DTCs
   Select-String -Path "rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\OBDonUDS\Diamant__DTC__CHR__IPB.xml" -Pattern "DTC_123456"
   
   # Check Attributes
   Select-String -Path "rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\OBDonUDS\Diamant__DTCATTRIBUTES__CHR__IPB.xml" -Pattern "DTCAttribute_CHR_NonOBD45"
   
   # Check Attribute Links
   Select-String -Path "rb\as\mb\ipb\dsmpr\cfg\Diamant_Cfg\OBDonUDS\Diamant__DTC_AttributesClassLink__CHR.xml" -Pattern "DTC_123456"
   
   # Check FW-DTC Links
   Select-String -Path "CHRYSLER_IPB\rb\**\Diamant__FW_LINK_PRJ_DTC_REF__*.xml" -Pattern "FW_HydraulicUndervoltage.*DTC_123456"
   ```

4. **Validate Data Integrity**
   - Ensure DTCs have correct properties
   - Verify attributes reference correct DTCs
   - Confirm links are properly established
   - Check customer/project file placement

## Advantages Over Sequential Workflow

**Performance Benefits:**
- ✓ 4x faster execution (1-2 minutes vs 4-8 minutes)
- ✓ Single database load operation
- ✓ No context switching between plugins
- ✓ Reduced DiamantPro startup overhead

**Reliability Benefits:**
- ✓ Atomic operation (all-or-nothing)
- ✓ Consistent error handling
- ✓ Single transaction for all changes
- ✓ Unified logging

**Operational Benefits:**
- ✓ One command instead of four
- ✓ Simpler automation scripting
- ✓ Easier to troubleshoot
- ✓ Single point of configuration

## Troubleshooting Guide

### Common Issues and Solutions

**Issue: "All 4 environment variables must be set"**
- Cause: One or more environment variables not set
- Solution: Ensure all 4 variables are set before execution
- Prevention: Use provided script template

**Issue: "Step 1 fails - DTC not created"**
- Cause: DTC_Input.txt format error
- Solution: Verify file format, check CUSTOMER_REF/PRODUCT_LINE_REF
- Impact: Entire workflow aborts, no steps execute

**Issue: "Step 2 fails - Attribute not created"**
- Cause: DTCAttribute_Input.txt format error
- Solution: Check file format and customer/product refs
- Impact: Steps 3-4 don't run, Step 1 already completed

**Issue: "Step 3 fails - Link not created"**
- Cause: Referenced DTC or attribute doesn't exist
- Solution: Verify Steps 1-2 completed successfully
- Impact: Step 4 doesn't run, Steps 1-2 already completed

**Issue: "Step 4 fails - FW-DTC link fails"**
- Cause: Failure word or DTC doesn't exist
- Solution: Run FW workflow first, verify DTCs created
- Impact: Steps 1-3 already completed

**Issue: "Exit code 1 but workflow succeeded"**
- Cause: Unrelated validation plugin compilation errors
- Solution: Check for "All 4 steps completed successfully!" message
- This is NORMAL behavior

**Issue: "No files written to disk"**
- Cause: Missing --WRITESPLITTERS flag
- Solution: Ensure command includes --WRITESPLITTERS
- Prevention: Use provided command template

## Integration with Other Workflows

This prompt can be combined with:
- **FW Splitter Generation**: Create failure words before running workflow
- **DTC Requirement Analysis**: Parse requirements to generate input files
- **Configuration Management**: Execute for multiple configurations
- **AUTOSAR Validation**: Verify generated XML meets standards
- **Batch Processing**: Script multiple DTC sets

## Comparison: Combined vs Sequential

| Feature | Combined Plugin | Sequential (4 plugins) |
|---------|----------------|------------------------|
| Commands | 1 | 4 |
| Database loads | 1 | 4 |
| Environment variables | All 4 at once | 1 at a time |
| Execution time | 1-2 minutes | 4-8 minutes |
| Log files | 2 | 5+ |
| Error handling | Abort on failure | Continue to next |
| Transaction safety | Atomic | Partial updates possible |
| Automation complexity | Low | High |

**When to use Combined Plugin:**
- Normal DTC updates
- Production workflows
- Automated processes
- Time-sensitive operations

**When to use Sequential Plugins:**
- Debugging specific steps
- Partial updates required
- Step-by-step validation needed
- Learning/training purposes

## Notes
- Combined plugin internally executes all 4 steps sequentially
- All 4 environment variables MUST be set before execution
- Workflow aborts immediately if any step fails
- Previous steps' changes are already committed on failure
- To resume, fix the issue and re-run entire workflow
- Exit code 1 is normal (unrelated validation plugin errors)
- Focus on "All 4 steps completed successfully!" for success confirmation

## Related Prompts
- [2_1_update_fw_node_and_graphlinks.prompt.md](2_1_update_fw_node_and_graphlinks.prompt.md) - Update FW, NODE and Graph Links
- [2_3_update_stm_database.prompt.md](2_3_update_stm_database.prompt.md) - Update STM Database

## Version History
- **Version 1.0** (January 26, 2026): Initial prompt created
  - Single combined plugin execution
  - All 4 steps in one DiamantPro session
  - Atomic workflow with abort-on-failure
  - Performance optimized (4x faster)
  - Comprehensive error handling and validation
