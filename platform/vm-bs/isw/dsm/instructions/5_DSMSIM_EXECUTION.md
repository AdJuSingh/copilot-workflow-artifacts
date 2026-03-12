# Instruction 2: DSMSIM Execution and Build Configuration Selection

## 🎯 CRITICAL PURPOSE & SCOPE

**DSMSIM (Diagnostic Service Message Simulator) execution provides automated diagnostic service testing and validation for ECU software builds, following UDS (Unified Diagnostic Services) standards and AUTOSAR specifications.**

### Execution Framework Standards
- **UDS (ISO 14229)**: Unified Diagnostic Services protocol compliance
- **AUTOSAR**: Automotive software architecture validation
- **ISO 26262**: Safety-critical automotive software testing
- **Build Configuration Management**: Multi-variant build support

---

## 🚨 MANDATORY PRE-EXECUTION REQUIREMENTS

**BEFORE STARTING DSMSIM EXECUTION:**

1. **Verify Gen Folder Structure**: Ensure the `Gen/` folder exists with build configurations
2. **Build Configuration Discovery**: List all available build configurations from `Gen/` folder
3. **User Selection**: Present available configurations and wait for user selection
4. **Build Validation**: Verify selected build has required artifacts
5. **DSMSIM Environment Setup**: Ensure DSMSIM tools and dependencies are available

---

## 📋 BUILD CONFIGURATION DISCOVERY PROCESS

### Step 1: Scan Gen Folder Structure

The `Gen/` folder contains multiple build configurations, typically named with variant identifiers:

```
Gen/
├── F332xEPBxNRx8500xBxECA/
├── F332xEPBxNRx8500xBxRBBLDR/
├── F332xEPBxNRx8500xBxRBBMGR/
├── F332xEPBxNRx8500xCxECC/
└── F332xEPBxNRx8500xDSMSIM/
```

### Step 2: List Available Build Configurations

**MANDATORY**: Before proceeding, discover and display all build configurations:

1. **Scan the Gen folder** for all subdirectories
2. **List all folder names** found under Gen/
3. **DO NOT check for build artifacts, timestamps, or status**
4. **Simply present the folder names** as numbered options

### Step 3: Present Configurations to User

**Display Format:**

```
Available Build Configurations in Gen/:

1. F332xEPBxNRx8500xBxECA
2. F332xEPBxNRx8500xBxRBBLDR
3. F332xEPBxNRx8500xBxRBBMGR
4. F332xEPBxNRx8500xCxECC
5. F332xEPBxNRx8500xDSMSIM

Please select a build configuration number (1-5):
```

### Step 4: Wait for User Selection

**CRITICAL**: Do NOT proceed without explicit user selection. Wait for user to provide:
- Configuration number, OR
- Configuration name, OR
- Confirmation to use default/latest configuration

---

## 🔧 BUILD CONFIGURATION VALIDATION AND EXECUTION

### Step 1: Identify Available Test Lists

After user selection, first identify the available test lists in the selected build configuration:

**Binary Location Pattern:**
```
Gen/<SelectedConfig>/out/Bin_<SelectedConfig>.exe
```

**Example:**
```
Gen/F332xEPBxNRx8500xDSMSIM/out/Bin_F332xEPBxNRx8500xDSMSIM.exe
```

**Command to List Test Names:**
```powershell
Bin_<SelectedConfig>.exe SwTest -Testlist=?
```

**Example:**
```powershell
C:\TSDE_Workarea\LNG1COB\Gen10_250_139_PSW\FIAT_GEN10\Gen\F332xEPBxNRx8500xDSMSIM\out\Bin_F332xEPBxNRx8500xDSMSIM.exe SwTest -Testlist=?
```

**Expected Output:**
```
ERROR: The desired test list <?> wasn't found ;FAIL; Available are:
0- LayoutMF_Tests
1- RBDSM_RBEnv_EnvGeneric
2- RBDSM_SMM_Tests
...
40- RBDSM_SWT_PRJ_Node
...
49- RBDSM_prj_PrepNvM
```

**Display this list to the user** and ask them to select test(s) by name or keyword.

### Step 2: Locate DSMSimHelper.exe (Alternative Execution Method)

Alternatively, locate the DSMSimHelper.exe in the selected build configuration:

**DSMSimHelper.exe Location Pattern:**
```
Gen/<SelectedConfig>/out/DSMSimHelper.exe
```

**Example:**
```
Gen/F332xEPBxNRx8500xDSMSIM/out/DSMSimHelper.exe
```

### Step 3: Execute Tests

**MANDATORY**: After listing available tests, execute the selected tests.

**Two Execution Methods:**

#### Method 1: Direct Binary Execution (Recommended)

Execute tests directly using Bin_<SelectedConfig>.exe:

```powershell
# Execute specific test list
Bin_<SelectedConfig>.exe SwTest -Testlist=<TestListName>

# Execute with custom verbosity
Bin_<SelectedConfig>.exe SwTest -Testlist=<TestListName> -Verbosity=3

# Execute with custom output directory
Bin_<SelectedConfig>.exe SwTest -Testlist=<TestListName> -OutputDir=<Path>
```

**Example:**
```powershell
C:\TSDE_Workarea\LNG1COB\Gen10_250_139_PSW\FIAT_GEN10\Gen\F332xEPBxNRx8500xDSMSIM\out\Bin_F332xEPBxNRx8500xDSMSIM.exe SwTest -Testlist=RBDSM_SWT_PRJ_Node
```

**SwTest Command Options:**
- `-Testlist=<Name>`: Execute specific test list
- `-Singletest=<ListName>=<TestName>`: Execute single test case
- `-Verbosity=<0-4>`: Set console output level (0=Result only, 3=Info default, 4=All)
- `-FileLog=<0-4>`: Set file log level (0=CSV only, 2=Eval default)
- `-OutputDir=<Path>`: Set output directory for reports
- `-TaskPattern=<0-3>`: Set task pattern (0=Default, 1-3=Jitter patterns)

#### Method 2: DSMSimHelper.exe Execution

Execute using DSMSimHelper.exe wrapper:

**Execution Command:**
```powershell
# Navigate to the selected configuration's out folder
cd Gen\<SelectedConfig>\out

# Execute DSMSimHelper.exe
.\DSMSimHelper.exe
```

**Example for DSMSIM configuration:**
```powershell
C:\TSDE_Workarea\LNG1COB\Gen10_250_139_PSW\FIAT_GEN10\Gen\F332xEPBxNRx8500xDSMSIM\out\DSMSimHelper.exe
```

### Step 4: Process User Test Selection with Intelligent Matching

**CRITICAL**: Process user test selection intelligently:

**For Direct Binary Execution (Method 1):**

1. **Display the available test lists** obtained from Step 1
2. **Wait for the user to provide test selection** (name, keyword, or number)
3. **Process user input intelligently**:
   - If user provides a **keyword** (e.g., "Node", "STM", "Dem"), **search the list** for matching test names (case-insensitive)
   - **Identify all matching test names** that contain the keyword
   - **Execute tests sequentially** or ask user to select one
   - If user provides **specific test name**, execute it directly
   - If user provides **test number**, use corresponding test name
4. **Execute the test** using: `Bin_<Config>.exe SwTest -Testlist=<MatchedTestName>`

**For DSMSimHelper.exe Execution (Method 2):**

1. **The tool will display prompts** requesting various inputs (test parameters, configuration options, etc.)
2. **Display the prompts to the user** exactly as they appear in the terminal
3. **Wait for the user to provide each input** - DO NOT proceed automatically
4. **Process user input intelligently**:
   - If user provides a **keyword** (e.g., "Node", "STM", "Dem"), **search the list** for matching test names
   - **Identify all matching test numbers** that contain the keyword (case-insensitive)
   - **Format the input** as comma-separated numbers (e.g., "30,34" for "Node")
   - If user provides **specific numbers**, pass them directly
   - If user provides **"All"** or **"0"**, pass "0"
5. **Pass the processed input to the terminal**
6. **Continue until DSMSimHelper.exe completes** or requests no more inputs

#### Example: Intelligent Keyword Matching for Direct Binary

**Available Test Lists:**
```
40- RBDSM_SWT_PRJ_Node
45- RBDSM_SWT_MS_Node
```

**User Input:** `Node`

**Agent Processing (Direct Binary):**
1. Search test list names for "Node"
2. Find: RBDSM_SWT_PRJ_Node, RBDSM_SWT_MS_Node
3. Execute: `Bin_<Config>.exe SwTest -Testlist=RBDSM_SWT_PRJ_Node`

#### Example: Intelligent Keyword Matching for DSMSimHelper.exe

**Terminal Output:**
```
Select test to execute from below list:

0 -     All
1 -     RBDSM_RBEnv_EnvGeneric
...
30 -    RBDSM_SWT_PRJ_Node
...
34 -    RBDSM_SWT_MS_Node
...
Enter your input:
```

**User Input:** `Node`

**Agent Processing:**
1. Search all test names for "Node" (case-insensitive)
2. Find matches: #30 (RBDSM_SWT_PRJ_Node), #34 (RBDSM_SWT_MS_Node)
3. Format as: `30,34`
4. Pass to terminal: `30,34`

**User Input:** `STM`

**Agent Processing:**
1. Search all test names for "STM" (case-insensitive)
2. Find matches: #4, #5, #6, #8, #12, #14, #15
3. Format as: `4,5,6,8,12,14,15`
4. Pass to terminal: `4,5,6,8,12,14,15`

### Input Processing Guidelines

**Valid Input Types:**

1. **Keyword Matching** (e.g., "Node", "STM", "Dem"):
   - Search test names (case-insensitive)
   - Identify all matching test numbers
   - Format as comma-separated list
   - Example: "Node" → "30,34"

2. **Direct Numbers** (e.g., "5", "10,15,20"):
   - Pass directly to terminal
   - No processing needed

3. **All Tests** (e.g., "All", "0"):
   - Pass "0" to terminal
   - Executes all available tests

4. **Multiple Keywords** (e.g., "Node STM"):
   - Search for each keyword separately
   - Combine all matching numbers
   - Remove duplicates
   - Format as comma-separated list

**Error Handling:**

- If keyword matches **no tests**: Inform user and request valid input
- If keyword matches **too many tests**: Confirm with user before proceeding
- If input is **ambiguous**: Ask user for clarification

### Validation Process

```powershell
# Step 1: Build the path to DSMSimHelper.exe
$selectedConfig = "<UserSelectedConfig>"  # e.g., F332xEPBxNRx8500xDSMSIM
$dsmSimPath = "C:\TSDE_Workarea\LNG1COB\Gen10_250_139_PSW\FIAT_GEN10\Gen\$selectedConfig\out\DSMSimHelper.exe"

# Step 2: Verify the executable exists
if (-not (Test-Path $dsmSimPath)) {
    Write-Error "DSMSimHelper.exe not found at: $dsmSimPath"
    exit 1
}

# Step 3: Execute DSMSimHelper.exe
Write-Host "Launching DSMSimHelper.exe..."
Write-Host "Please provide inputs as prompted by the tool."
& $dsmSimPath

# Step 4: Tool will prompt for inputs interactively
# Wait for user to provide all inputs and let the tool complete
```

---

## 🚀 DSMSIM EXECUTION PROCESS

### Environment Setup

1. **Set Build Configuration Path**:
   ```powershell
   $DSMSIM_BUILD_PATH = "c:\TSDE_Workarea\LNG1COB\Gen10_250_139_PSW\FIAT_GEN10\Gen\<SelectedConfig>\out"
   ```

2. **Locate DSMSimHelper.exe**:
   - Path: `Gen\<SelectedConfig>\out\DSMSimHelper.exe`
   - Verify executable exists before proceeding

3. **Execute DSMSimHelper.exe**:
   - Run the executable in terminal
   - Tool will prompt for required inputs
   - User provides inputs interactively

### Execution Steps

#### Step 1: Launch DSMSimHelper.exe

```powershell
# Execute DSMSimHelper.exe
C:\TSDE_Workarea\LNG1COB\Gen10_250_139_PSW\FIAT_GEN10\Gen\<SelectedConfig>\out\DSMSimHelper.exe
```

#### Step 2: Interactive Input Collection

**DSMSimHelper.exe will prompt for inputs such as:**
- Test configuration parameters
- Diagnostic session types
- Test case selection
- Execution mode options
- Output report preferences

**Wait for user to provide each input as prompted by the tool.**

#### Step 3: Execute Test Suite

**DSMSimHelper.exe will automatically:**
- Load ECU software configuration
- Initialize diagnostic environment
- Execute selected test cases
- Generate test results
- Create execution report

**Monitor terminal output for:**
- Test execution progress
- Pass/fail status for each test
- Error messages or warnings
- Completion confirmation

---

## 📊 TEST EXECUTION REPORTING

### Test Report Structure

Generate comprehensive test execution report:

```markdown
# DSMSIM Test Execution Report

**Build Configuration**: <SelectedConfig>
**Build Timestamp**: <Build_YYYYMMDD_HHMMSS>
**Test Execution Date**: <CurrentDate>
**Tester**: GitHub Copilot

## Build Artifacts
- HEX File: ✅ <filename>.hex
- A2L File: ✅ <filename>.a2l
- DCM File: ✅ <filename>.dcm

## Test Summary
- Total Test Cases: <N>
- Passed: <P>
- Failed: <F>
- Skipped: <S>
- Pass Rate: <P/N * 100>%

## Test Results by Service

### Service 0x22 (ReadDataByIdentifier)
| DID | Test Case | Status | Response | Comments |
|-----|-----------|--------|----------|----------|
| 1002 | TC_22_1002_01 | ✅ PASS | 62 10 02 <data> | Vehicle speed read successful |
| 3002 | TC_22_3002_01 | ✅ PASS | 62 30 02 <data> | Roll bench mode read successful |

### Service 0x2E (WriteDataByIdentifier)
| DID | Test Case | Status | Response | Comments |
|-----|-----------|--------|----------|----------|
| 3002 | TC_2E_3002_01 | ✅ PASS | 6E 30 02 | Roll bench mode write successful |

## Failed Tests
<List of failed tests with detailed error information>

## Test Coverage
- Requirements Coverage: <X>%
- Code Coverage: <Y>%
- MCDC Coverage: <Z>%
```

---

## 🔍 TROUBLESHOOTING COMMON ISSUES

### Issue 1: Build Configuration Not Found

**Symptoms**: Selected configuration folder is empty or missing Build_* subdirectory

**Resolution**:
1. Verify build was completed successfully
2. Check build logs for errors
3. Re-run build process if necessary
4. Select different configuration

### Issue 2: Missing Artifacts

**Symptoms**: Required files (.hex, .a2l, .dcm) not present

**Resolution**:
1. Check build logs for generation failures
2. Verify build configuration settings
3. Re-build with correct configuration
4. Contact build system administrator

### Issue 3: DSMSIM Connection Failure

**Symptoms**: Cannot load software or connect to simulator

**Resolution**:
1. Verify DSMSIM tools are installed and accessible
2. Check network connection (if remote simulator)
3. Restart DSMSIM environment
4. Verify ECU power and communication

### Issue 4: Test Execution Errors

**Symptoms**: Test cases fail or timeout

**Resolution**:
1. Verify diagnostic session is active
2. Check security access if required
3. Review test case request format
4. Verify ECU state and preconditions

---

## 📁 OUTPUT FILES AND ARTIFACTS

### Generated Files

- **Test Execution Report**: `review/DSMSIM_TestReport_<Timestamp>.html`
- **Test Results Log**: `review/DSMSIM_TestResults_<Timestamp>.log`
- **Coverage Report**: `review/DSMSIM_Coverage_<Timestamp>.xml`
- **Execution Trace**: `review/DSMSIM_Trace_<Timestamp>.trc`

### File Locations

```
GenFromCopilot_DCOM/DCOM_DID/
├── review/
│   ├── DSMSIM_TestReport_20251109_120000.html
│   ├── DSMSIM_TestResults_20251109_120000.log
│   ├── DSMSIM_Coverage_20251109_120000.xml
│   └── DSMSIM_Trace_20251109_120000.trc
└── tst/
    ├── DCOM_CT_Service22_1002_VehicleSpeed.ct
    └── DCOM_CT_Service22_3002_RollBenchMode.ct
```

---

## ✅ QUALITY CHECKLIST

### Pre-Execution Checklist

- [ ] Gen folder structure verified
- [ ] Build configurations discovered and listed
- [ ] User selection obtained
- [ ] Selected build validated
- [ ] Required artifacts present (.hex, .a2l, .dcm)
- [ ] DSMSIM environment initialized
- [ ] Test cases identified and loaded

### Execution Checklist

- [ ] ECU software loaded successfully
- [ ] Diagnostic configuration loaded
- [ ] Calibration database loaded
- [ ] All test cases executed
- [ ] Test results captured
- [ ] Coverage data collected
- [ ] No execution errors or crashes

### Post-Execution Checklist

- [ ] Test report generated
- [ ] Test results analyzed
- [ ] Failed tests documented
- [ ] Coverage metrics calculated
- [ ] Execution artifacts saved
- [ ] Report reviewed and approved

---

## 🎯 SUCCESS CRITERIA

### Execution Success

- ✅ Build configuration selected by user
- ✅ All required artifacts validated
- ✅ DSMSIM environment initialized
- ✅ All test cases executed without errors
- ✅ Test report generated with complete results
- ✅ Coverage metrics meet targets
- ✅ No blocking issues identified

### Acceptance Criteria

- **Pass Rate**: ≥ 95% of test cases pass
- **Requirements Coverage**: ≥ 100% of SWCS requirements covered
- **Code Coverage**: ≥ 90% statement coverage
- **MCDC Coverage**: ≥ 80% for safety-critical functions
- **No Critical Failures**: No safety-related test failures

---

## 📚 REFERENCES

- **UDS Standard**: ISO 14229-1:2020
- **AUTOSAR Diagnostic Specification**: AUTOSAR_SWS_DiagnosticCommunicationManager
- **Build System Documentation**: Internal build process guide
- **DSMSIM User Manual**: DSMSIM tool documentation

---

## 🔄 VERSION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-09 | GitHub Copilot | Initial creation |

---

**END OF INSTRUCTION FILE**
