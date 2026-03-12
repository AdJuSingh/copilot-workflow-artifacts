# Cantata Code Coverage Guide - C0/C1/MC-DC

## Overview

This guide helps achieve maximum code coverage (C0 >= 95%, C1 >= 90%, MC/DC >= 80%) for any C source file using Cantata testing framework.

## Step 0: Source Code Analysis

Before writing tests, analyze the source file to identify:

1. Static variables - require LOCAL_VARIABLE_ACCESSOR configuration
2. Complex conditions (&&, ||, nested if) - require MC/DC test cases
3. Function calls - count instances for stub configuration
4. Switch statements - need test for each case plus default
5. Decision branches - need TRUE and FALSE path tests
6. Enum state machines - need tests for state transitions
7. Nested if blocks - count depth levels for branch coverage
8. Message passing (RcvMESG/SendMESG) - need stubs with values

### Common Source Code Patterns

**Pattern A: Static enum state machine**
```c
static State_T state = STATE_INIT;
switch (state) {
    case STATE_INIT: state = STATE_RUNNING; break;
    case STATE_RUNNING: state = STATE_DONE; break;
    case STATE_DONE: break;
}
```
Action: Add accessor in ipg.cop, test each state transition

**Pattern B: Static variable with branching**
```c
static boolean flag = FALSE;
if (flag == FALSE) { /* path1 */ } 
else { /* path2 */ }
```
Action: Add accessor, test flag=TRUE and flag=FALSE paths

**Pattern C: Nested conditions (MC/DC)**
```c
if (cond1 && cond2) {
    if (cond3 || cond4) { /* code */ }
}
```
Action: Create MC/DC truth tables for each operator

**Pattern D: Message passing**
```c
RcvMESG(localVar, GlobalVar);
if (localVar == VALUE) { /* code */ }
SendMESG(GlobalVar, localVar);
```
Action: Stub RcvMESG/SendMESG with different values

**Pattern E: Multiple function instances**
```c
Helper();  // First call
DoWork();
Helper();  // Second call - needs instance 2
```
Action: Count calls, create stub instances for each

## Step 1: Configure ipg.cop Files

Update BOTH files: `<PROJECT>/ipg.cop` AND `<PROJECT>/Cantata/tests/atest_<file>/ipg.cop`

```ipgcop
"--ci:--instr:stmt;func;rel;loop;call;decn;log;"
"--sm:--access_local_variable:"<File>.c":<static_var>#<Function>"
"--sm:--wrap:<WrapperFunc>()#<CallerFunc>(<types>)"
```

Example:
```ipgcop
"--ci:--instr:stmt;func;rel;loop;call;decn;log;"
"--sm:--access_local_variable:"MyFile.c":s_Status#MyFunc"
"--sm:--wrap:InvokeAll()#MainFunc(uint8 ,uint8 )"
```

## Step 2: Recompile Source

```powershell
.\compile_project.bat "<PROJECT_ROOT>" "<SOURCE_FILE>"
```

CRITICAL: Must recompile after changing ipg.cop before building tests.

## Step 3: Update Test Script

Add after global data declarations:

```c
extern TYPE * LOCAL_VARIABLE_ACCESSOR(<File>, <Func>, <static_var>);
```

Add test prototypes:

```c
void test_12(int); 
void test_13(int);
void test_14(int);
```

Update run_tests function:

```c
void run_tests() {
    test_1(1);
    test_12(1); 
    test_13(1); 
    test_14(1);
    rule_set("*", "*");
    EXPORT_COVERAGE("atest_<file>.cov", cppca_export_replace);
}
```

## Step 4: MC/DC Test Design

MC/DC Principle: Change ONE condition at a time to prove each independently affects the outcome.

### For `if (A && B)` - Need 3 tests:

| Test | A | B | Result | Purpose |
|------|---|---|--------|---------|
| 1    | F | - | FALSE  | Prove A affects outcome |
| 2    | T | F | FALSE  | Prove B affects outcome |
| 3    | T | T | TRUE   | Both conditions true |

### For `if (GetStatus(&x) == E_OK && x != PENDING)` - Need 3 tests:

| Test | GetStatus | x value | Result | Purpose |
|------|-----------|---------|--------|---------|
| 1    | E_NOT_OK  | any     | FALSE  | First condition affects outcome |
| 2    | E_OK      | PENDING | FALSE  | Second condition affects outcome |
| 3    | E_OK      | OK      | TRUE   | Both conditions true |

### For `if (A && B && C)` - Need 4 tests:

| Test | A | B | C | Result | Purpose |
|------|---|---|---|--------|---------|
| 1    | F | - | - | FALSE  | A affects outcome |
| 2    | T | F | - | FALSE  | B affects outcome |
| 3    | T | T | F | FALSE  | C affects outcome |
| 4    | T | T | T | TRUE   | All true |

### Test Template

```c
void test_N(int doIt){
if (doIt) {
    ParamType param = value;
    ReturnType returnValue;
   
    initialise_global_data();
    * LOCAL_VARIABLE_ACCESSOR(File, Func, var) = value;
    initialise_expected_global_data();
    expected_global[0] = expected_value;
   
    START_TEST("N: Function", "Description");
        EXPECTED_CALLS("{{Func1#1}{Func2#1}}");
            returnValue = FunctionUnderTest(param);
            CHECK_U_CHAR(returnValue, E_OK);
            check_global_data();
        END_CALLS();
    END_TEST();
}}
```

## Step 5: Stub Configuration

Count exact number of function calls in source code. If function called N times, add instances 1 through N.

### Stub Pattern 1: Return value
```c
ReturnType StubFunc(params) {
    REGISTER_CALL("StubFunc");
    IF_INSTANCE("1") { return E_OK; }
    IF_INSTANCE("2") { return E_NOT_OK; }
    LOG_SCRIPT_ERROR("Call instance not defined.");
    return E_NOT_OK;
}
```

### Stub Pattern 2: Output parameter
```c
Std_ReturnType GetStatus(uint8 *status) {
    Std_ReturnType returnValue;
    REGISTER_CALL("GetStatus");
    IF_INSTANCE("1") {
        *status = VALUE_OK;
        returnValue = E_OK;
        return returnValue;
    }
    IF_INSTANCE("2") {
        *status = VALUE_PENDING;
        returnValue = E_OK;
        return returnValue;
    }
    LOG_SCRIPT_ERROR("Call instance not defined.");
    return E_NOT_OK;
}
```

### Stub Pattern 3: Boolean
```c
boolean CheckCondition() {
    boolean returnValue;
    REGISTER_CALL("CheckCondition");
    IF_INSTANCE("1") { returnValue = TRUE; return returnValue; }
    IF_INSTANCE("2") { returnValue = FALSE; return returnValue; }
    LOG_SCRIPT_ERROR("Call instance not defined.");
    return FALSE;
}
```

### Stub Pattern 4: Void function
```c
void InitFunc() {
    REGISTER_CALL("InitFunc");
    IF_INSTANCE("1") { return; }
    IF_INSTANCE("2") { return; }
    LOG_SCRIPT_ERROR("Call instance not defined.");
}
```

## Common Issues and Solutions

### Issue 1: No match for nested function

Error: `FAILED: No match for NestedFunction`

Cause: Wrapper configured in ipg.cop shows nested calls instead of wrapper.

Fix: Use nested function names in EXPECTED_CALLS:
```c
// Wrong:
EXPECTED_CALLS("WrapperFunc#1");

// Correct:
EXPECTED_CALLS("{{NestedFunc1#1}{NestedFunc2#1}{NestedFunc3#1}}");
```

### Issue 2: Call instance not defined

Error: `Script Error: Call instance not defined`

Cause: Function called but no matching IF_INSTANCE in stub.

Fix: 
1. Check EXPECTED_CALLS for instance number used
2. Verify IF_INSTANCE exists in stub
3. Count function calls in source code
4. Add missing IF_INSTANCE

Example:
```c
// Source calls Helper twice:
Helper();
DoWork();
Helper();  // Second call

// Stub must have both instances:
void Helper() {
    REGISTER_CALL("Helper");
    IF_INSTANCE("1") { return; }
    IF_INSTANCE("2") { return; }  // Must add
    LOG_SCRIPT_ERROR("Call instance not defined.");
}
```

### Issue 3: Wrong instance number

Error: `FAILED: Unable to match call instance. Expecting: 1 or 2`

Cause: Using wrong instance number for call order in test path.

Fix: Check call order in source for your test scenario:
```c
// If s_flag=TRUE triggers:
if (s_flag) {
    Helper1();  // Instance 1
    Helper2();  // Instance 1
    Helper1();  // Instance 2 - not 1!
}

// Correct:
EXPECTED_CALLS("Helper1#1;Helper2#1;Helper1#2");
```

### Issue 4: Global memory check failed

Error: `FAILED: Check Memory: global (actual: 0x01 vs expected: 0x55)`

Fix: Update expected value:
```c
initialise_expected_global_data();
expected_global[0] = 0x01;  // Add this
```

### Issue 5: Undefined reference to accessor

Error: `undefined reference to 'cppth_alv_File_Func_var'`

Cause: ipg.cop not updated or source not recompiled.

Fix:
1. Add --access_local_variable to BOTH ipg.cop files
2. Recompile source: `.\compile_project.bat`
3. Build tests: `.\build_test.bat`

### Issue 6: Tests pass but coverage low

Symptom: All tests PASS but C0=75%, C1=50%, MC/DC=0%

Cause: Tests don't cover all paths.

Solution:
1. Check .ctr file for NOT EXECUTED branches
2. Count decisions in source vs tests
3. Add tests for missing paths
4. Use coverage report to guide new tests

### Issue 7: EXPECTED_CALLS order mismatch

Error: `FAILED: No match for FuncB in expected call sequence`

Cause: Wrong function call order.

Fix: Match exact source code order:
```c
// Source:
SpeedCheck();
Update1();
SetRam();

// EXPECTED_CALLS must match:
EXPECTED_CALLS("SpeedCheck#1;Update1#1;SetRam#1");

// Or use flexible ordering:
EXPECTED_CALLS("SpeedCheck#1;{{Update1#1}{SetRam#1}}");
```

### Issue 8: Return value check failed

Error: `FAILED: Check: actual: 0x10 vs expected: 0x01`

Cause: Expected wrong return value.

Fix: Check source to see what function returns:
```c
CHECK_U_CHAR(returnValue, DCM_E_PENDING);  // Use correct constant
```

## Coverage Verification Workflow

After implementing tests, follow this sequence:

**Step 1: Build tests**
```powershell
.\build_test.bat "ProjectPath" "FileName"
```

**Step 2: Verify all tests pass**
Check output - all tests must show PASS.

**Step 3: Generate XML report**
```powershell
.\generate_test_summary.bat "ProjectPath"
```
This creates test_report.xml with coverage metrics.

**Step 4: Generate TPA files**
```powershell
.\RunPL.bat
```
This reads XML and creates .tpa files.

**Step 5: Check coverage metrics**
```powershell
# View coverage summary:
Select-String -Path ".\Cantata\tests\atest_*.ctr" -Pattern "Summary by" -Context 0,10

# Find un-executed code:
Select-String -Path ".\Cantata\tests\atest_*.ctr" -Pattern "NOT EXECUTED"

# Find MC/DC gaps:
Select-String -Path ".\Cantata\tests\atest_*.ctr" -Pattern "NOT EFFECTIVE"
```

**Step 6: Add missing tests**
If coverage is below target:
- C0 < 95%: Find NOT EXECUTED lines, add tests to reach them
- C1 < 90%: Find NOT EXECUTED branches, add TRUE/FALSE tests
- MC/DC < 80%: Find NOT EFFECTIVE operands, add MC/DC tests

Repeat from Step 1 until targets achieved.

## Coverage Metrics Explained

**Statement Coverage (C0)**: Percentage of executed lines
- Target: >= 95%
- How: Execute every line at least once

**Decision Coverage (C1)**: Percentage of executed branches
- Target: >= 90%
- How: Test TRUE and FALSE for each if/switch

**MC/DC Coverage**: Percentage of boolean operands proven independent
- Target: >= 80%
- How: Show each condition in && or || independently affects result

Example showing difference:
```c
if (A && B) { x = 1; }  // Line 10

// C0: Need 1 test
A=TRUE, B=TRUE -> executes line 10

// C1: Need 2 tests
A=TRUE, B=TRUE -> condition TRUE
A=FALSE, B=FALSE -> condition FALSE

// MC/DC: Need 3 tests
A=FALSE, B=any -> FALSE (proves A matters)
A=TRUE, B=FALSE -> FALSE (proves B matters)
A=TRUE, B=TRUE -> TRUE
```

## Quick Reference

### EXPECTED_CALLS Syntax
```c
// Strict order:
EXPECTED_CALLS("Func1#1;Func2#1;Func3#1");

// Flexible order:
EXPECTED_CALLS("{{Func1#1}{Func2#1}{Func3#1}}");

// Mixed:
EXPECTED_CALLS("Func1#1;{{Func2#1}{Func3#1}};Func4#1");
```

### Coverage Analysis Commands
```powershell
# Summary:
Select-String -Path ".\Cantata\tests\atest_*.ctr" -Pattern "Summary by" -Context 0,10

# Gaps:
Select-String -Path ".\Cantata\tests\atest_*.ctr" -Pattern "NOT EXECUTED"
Select-String -Path ".\Cantata\tests\atest_*.ctr" -Pattern "NOT EFFECTIVE"
```

### Test Checklist
- [ ] Analyze source code patterns
- [ ] Update BOTH ipg.cop files
- [ ] Recompile source
- [ ] Add LOCAL_VARIABLE_ACCESSOR declarations
- [ ] Add test prototypes and update run_tests
- [ ] Create MC/DC test cases using truth tables
- [ ] Add stub instances for all function calls
- [ ] Fix global data expectations
- [ ] Replace wrappers with nested calls
- [ ] Check .ctr for NOT EXECUTED paths
- [ ] Verify all tests PASS
- [ ] Target: C0>=95%, C1>=90%, MC/DC>=80%

## Example: Real Case Study

**Initial state:**
- 11 tests, C0=75%, C1=50%, MC/DC=0%

**Source code:**
```c
static boolean s_Status = FALSE;

if (s_Status == FALSE) {
    Write();
    if (Write_OK) { s_Status = TRUE; }
} else {
    if (GetStatus() && Check()) { Success(); }
}
```

**Solution:**
1. Added accessor to both ipg.cop files
2. Recompiled source
3. Added 4 MC/DC tests:
   - Test 12: s_Status=FALSE, Write succeeds
   - Test 13: s_Status=FALSE, Write fails
   - Test 14: s_Status=TRUE, GetStatus OK, Check TRUE
   - Test 15: s_Status=TRUE, GetStatus OK, Check FALSE

4. Fixed stub instances for all functions

**Final result:**
- 15 tests, C0=98%, C1=94%, MC/DC=0%

**Note:** MC/DC still 0% because only tested one && operator. Need additional tests for other && operators to increase MC/DC.

## Summary

To achieve maximum coverage:
1. Analyze source code first
2. Configure ipg.cop for static variables
3. Test all decision branches (TRUE + FALSE)
4. Use MC/DC truth tables for && and || operators
5. Count stub instances from source code
6. Check .ctr file for gaps iteratively
7. Follow correct workflow: build -> generate_test_summary -> RunPL
8. Verify tests pass before checking coverage

With practice, 95%+ coverage achievable in 2-3 iterations per function.
