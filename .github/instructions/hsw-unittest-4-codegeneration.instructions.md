# HSW Unit Test Code Implementation Instructions

## Overview

This instruction file covers **writing test function bodies** in the `T<COMPONENT>_<Feature>.c` test file.

**IMPORTANT**: Do NOT generate production / functional implementation code — only test function bodies.

---

## Step 0 — Mandatory: Scan Before You Write (ALWAYS DO THIS FIRST)

**This instruction file handles ONLY writing test function bodies.** It does NOT handle creating Adaptors, Stubs, `.bcfg` files, or production code. Before writing any test code, **scan the following sources** to discover the available API and conventions:

### 0.1 Read the Adaptor header (`T<COMPONENT>_<Feature>Adaptor.h`)

The Adaptor.h defines the **only** API you may use to access private (static) variables and functions from the test code. Scan it to discover:

1. **Available accessor functions** — `CallPrivate_`, `GetPrivate_`, `SetPrivate_` (or `T<COMP>_get`/`T<COMP>_set`, or `CP_`/`GP_` style)
2. **Function signatures and return types** — use these exactly as declared
3. **The prefix convention** already in use — match it consistently in all test code

### 0.2 Read the Stub header files (`T<COMPONENT>_<Dep>Stub.h`, `T<COMPONENT>_DEM.h`)

The Stub headers define the **controllable inputs** for your tests. Scan them to discover:

1. **Stub control variables** — e.g. `tstub_ret_<Dep>_<Function>`, `tstub_call_<Dep>_<Function>`
2. **DEM stub API** — reset functions (`T<COMPONENT>_DEM_ResetAll()`, `DemStub_EnvReset()`), query functions (`T<COMPONENT>_DEM_GetFailEntry()`, `DemStub_isFailed()`)
3. **Helper / reset functions** available for test isolation (e.g. `FUN_ResetRequestBuffer_v()`)
4. **DEM verification pattern** in use: structured vs indexed array vs per-event flags vs helper functions

### 0.3 Read any existing test `.c` file from the same component (or sibling feature)

Scan one existing test file to identify:

1. **Assertion style** used: `SWT_EvalEq` vs `SWT_EvalEqX` vs `SWT_Eval`
2. **Doxygen tag prefix** used: `\UT_TestCaseName` or `\TestCaseName` — never mix in the same file
3. **Test specification conventions** — how `\UT_Sequence` and `\UT_ExpectedResult` are formatted

### 0.4 Read the test specification / requirements (if provided)

If the user provides a test specification, requirement IDs, or design document, use them to determine:

1. **Which functions to test** and the scenarios to cover
2. **Requirement IDs** to reference in `\UT_Reference` tags
3. **Expected behavior** to encode as `SWT_EvalEq` assertions

> **All test code must use ONLY the API discovered from Adaptor.h and Stub files — never access private symbols directly. Every new test file must mirror the conventions already established in that component.**

---

## 1. Test File Structure

### 1.1 Required Includes — Order Matters

`SwTest_Global.h` **MUST be the first include** in every test `.c` file. This is mandatory for TListGen/SWT functionality.

```c
/**
 * @ingroup <MODULE_NAME>UnitTest
 * @{
 *
 * @file T<COMPONENT>_<Feature>.c
 * @brief Unit tests for <Feature> of <COMPONENT>
 *
 * @copyright
 * Robert Bosch GmbH reserves all rights even in the event of industrial property rights.
 * We reserve all rights of disposal such as copying and passing on to third parties.
 *
 * // ContainsGenAICopilot - This notice needs to remain attached to any reproduction of this file.
 */

#include "SwTest_Global.h"               /* MUST be first — provides SWTEST, SWT_Eval*, RBMESG */

/* Module under test API */
#include "<COMPONENT>_<Feature>.h"
#include "<COMPONENT>_Subsystem.h"

/* Component config (stubbed) */
#include "<COMPONENT>_Config.h"           /* or T<COMPONENT>_ConfigStub.h */

/* Adaptor — white-box access to privates */
#include "T<COMPONENT>_<Feature>Adaptor.h"

/* Stub control headers */
#include "T<COMPONENT>_<Dep>Stub.h"
#include "T<COMPONENT>_DEM.h"             /* or T<COMPONENT>_DEMStub.h */
```

**Common mistakes to avoid:**
- Do NOT put `RBCMHSW_Global.h` before `SwTest_Global.h` (seen in RBEVP, RBHYDR — this is incorrect)
- Do NOT `#include` another `.c` file inside the test file (seen in RBWSS — use adaptors instead)
- Do NOT define stub functions inline inside the test file (seen in RBePedal, RBPTS, RBuCTEMP — use separate stub `.c/.h` files)

### 1.2 Test Function Signature

```c
SWTEST void T<COMPONENT>_<FunctionUnderTest>_<Scenario>(void)
```

- `SWTEST` is **mandatory** — TListGen uses it to auto-discover test functions.
- Always `void` return and `void` parameter.
- The function name must **exactly match** the `\UT_TestCaseName` in the Doxygen comment block above it.

---

## 2. SWT Assertion Macros

| Macro | When to use | Notes |
|-------|-------------|-------|
| `SWT_EvalEq(actual, expected)` | Equality check | **Preferred** for most assertions |
| `SWT_EvalEqX(actual, expected)` | Same, with hex output | Used in RBECM for register/ID values |
| `SWT_EvalEqF(actual, expectedf, tolerance)` | Float comparison | Used in RBuCTEMP |
| `SWT_EvalNeq(actual, notExpected)` | Inequality check | |
| `SWT_Eval(expr)` | Generic boolean | **Avoid** for equality — use `SWT_EvalEq` instead |
| `SWT_Info(fmt, ...)` | Diagnostic message | No pass/fail effect; use in table-driven loops |
| `SWT_AssertCheckStart(func, cond)` | Begin `cc_assert` capture | |
| `SWT_AssertCheckEnd()` | End `cc_assert` capture | |
| `SWT_EvalSystemFaultFree()` | No DEM FAILED event | Simulation builds only |

**Critical rule:** Always use `SWT_EvalEq(a, b)` instead of `SWT_Eval(a == b)` for equality checks. The `SWT_EvalEq` macro provides diagnostic output showing both actual and expected values on failure; `SWT_Eval` only shows `TRUE`/`FALSE`.

---

## 3. Test Patterns (from 12-Module Audit)

### 4.1 Normal / Happy-Path Test (RBECM pattern)

```c
/**
 * \UT_TestCaseName T<COMPONENT>_Process_Success
 *
 * \UT_Reference <COMPONENT>_Process,
 *               <RequirementID>
 *
 * \UT_Purpose Verify normal execution completes without DEM fault.
 *
 * \UT_Sequence
 *             1) Call T<COMPONENT>_DEM_ResetAll()
 *             2) Set tstub_ret_<Dep>_Function = VALID_VALUE
 *             3) Call SetPrivate_<COMPONENT>_state(<COMPONENT>_State_idle)
 *             4) Call <COMPONENT>_Process()
 *             5) Read state via GetPrivate_<COMPONENT>_state()
 *
 * \UT_ExpectedResult
 *             @5) SWT_EvalEq(GetPrivate_<COMPONENT>_state(), <COMPONENT>_State_finished)
 *             @5) SWT_EvalEq(T<COMPONENT>_DEM_GetSystemStatus(), DEM_SYSTEM_FAIL_FREE)
 */
SWTEST void T<COMPONENT>_Process_Success(void)
{
  /* Arrange */
  T<COMPONENT>_DEM_ResetAll();
  tstub_ret_<Dep>_Function = VALID_VALUE;
  SetPrivate_<COMPONENT>_state(<COMPONENT>_State_idle);

  /* Act */
  <COMPONENT>_Process();

  /* Assert */
  SWT_EvalEq(GetPrivate_<COMPONENT>_state(), <COMPONENT>_State_finished);
  SWT_EvalEq(T<COMPONENT>_DEM_GetSystemStatus(), DEM_SYSTEM_FAIL_FREE);
}
```

### 4.2 Error / Failure-Path Test — DEM Verification (RBuCWatchdog pattern)

When testing error-reporting functions, **always verify both EventId AND EventStatus**:

```c
SWTEST void T<COMPONENT>_Process_Failure(void)
{
  /* Arrange */
  T<COMPONENT>_DEM_ResetAll();
  tstub_ret_<Dep>_IsValid = FALSE;   /* inject error condition */
  SetPrivate_<COMPONENT>_state(<COMPONENT>_State_validate);

  /* Act */
  <COMPONENT>_Process();

  /* Assert — verify DEM event ID and status together */
  SWT_EvalEq(T<COMPONENT>_DEM_GetFailEntry().id,     DemConf_DemEventParameter_<EVENT>);
  SWT_EvalEq(T<COMPONENT>_DEM_GetFailEntry().status, DEM_EVENT_STATUS_FAILED);
  SWT_EvalEq(T<COMPONENT>_DEM_GetFailEntry().debug0, <ExpectedDebug0>);
  SWT_EvalEq(T<COMPONENT>_DEM_GetFailEntry().debug1, <ExpectedDebug1>);
  SWT_EvalEq(GetPrivate_<COMPONENT>_state(),          <COMPONENT>_State_error);
}
```

### 4.3 Table-Driven Test (RBADC C5PTest pattern — Gold Standard)

Use for functions with many input/output combinations. **Always include `SWT_Info` for diagnosability.**

```c
SWTEST void T<COMPONENT>_Function_TableDriven(void)
{
  int i;

  typedef struct
  {
    InputType_t  input1;
    uint32       input2;
    boolean      expectedReturn;
  } TestEntry_t;

  const TestEntry_t testTable[] =
  {
    /* input1,          input2,    expectedReturn */
    { ENUM_VAL_A,       0x000u,    TRUE  },   /* lower bound (included) */
    { ENUM_VAL_A,       0x400u,    TRUE  },   /* in range               */
    { ENUM_VAL_A,       0x401u,    FALSE },   /* out of bound           */
    { ENUM_VAL_B,       0xFFFu,    TRUE  },   /* upper bound (included) */
  };

  for (i = 0; i < (int)(sizeof(testTable) / sizeof(testTable[0])); i++)
  {
    boolean result;
    SWT_Info("Index %d — input: %u\n", i, (uint32)testTable[i].input2);

    result = <COMPONENT>_Function(testTable[i].input1, testTable[i].input2);
    SWT_EvalEq(result, testTable[i].expectedReturn);
  }
}
```

### 4.4 State-Machine Multi-Step Test (RBTaskMon pattern)

```c
SWTEST void T<COMPONENT>_StateMachine_FullCycle(void)
{
  /* Step 1: idle → running */
  SetPrivate_<COMPONENT>_state(<COMPONENT>_State_idle);
  <COMPONENT>_Process();
  SWT_EvalEq(GetPrivate_<COMPONENT>_state(), <COMPONENT>_State_running);

  /* Step 2: running → validate */
  <COMPONENT>_Process();
  SWT_EvalEq(GetPrivate_<COMPONENT>_state(), <COMPONENT>_State_validate);

  /* Step 3: validate → finish (inject good condition) */
  tstub_ret_<Dep>_Check = TRUE;
  <COMPONENT>_Process();
  SWT_EvalEq(GetPrivate_<COMPONENT>_state(), <COMPONENT>_State_finish);
  SWT_EvalEq(T<COMPONENT>_DEM_GetSystemStatus(), DEM_SYSTEM_FAIL_FREE);
}
```

### 4.5 RBMESG Injection Test (RBCDI / RBTaskMon pattern)

```c
SWTEST void T<COMPONENT>_GetCounter_ReturnsInjectedValue(void)
{
  uint32 task_counter = 0x1234u;
  uint32 result = 0u;

  /* Inject message value */
  RBMESG_SendMESG(RBMESG_Task1msCnt_u32, task_counter);

  /* Call function under test */
  result = CallPrivate_<COMPONENT>_Get1msTaskCounter();

  /* Verify */
  SWT_EvalEq(result, task_counter);
}
```

### 4.6 RBMESG Receive Verification Test (RBCDI pattern)

```c
SWTEST void T<COMPONENT>_Process_SendsCorrectMessage(void)
{
  uint16 received = 0;

  <COMPONENT>_Process();

  RBMESG_RcvMESG(received, RBMESG_<COMPONENT>_<Signal>_u16);

  SWT_EvalEq(received, <ExpectedValue>);
}
```

### 4.7 Assert / Defensive-Check Test

```c
SWTEST void T<COMPONENT>_Function_CheckAssert(void)
{
  SWT_AssertCheckStart("<COMPONENT>_Function", "validConditionExpr");

  <COMPONENT>_Function(INVALID_INPUT);   /* must trigger cc_assert */

  SWT_AssertCheckEnd();
}
```

### 4.8 Feature-Switch Variant Test (RBCDI / RBEVP pattern)

Wrap variant-specific tests in `#if(RBFS_…)` guards, matching the production code's conditionals:

```c
#if (RBFS_Task0p5ms == RBFS_Task0p5ms_ON)
SWTEST void T<COMPONENT>_500usTask_Test(void)
{
  /* test body for 0.5ms task variant */
  <COMPONENT>_PRC_0p5ms();
  SWT_EvalEq(...);
}
#endif
```

---

## 4. Adaptor Usage Rules

> Full adaptor file creation is covered in `7_UnitTest_EnvironmentSetup.instructions.md`. Here are the rules for **using** adaptors from test code.

- **Never access `static` variables or functions directly** from the test file — always go through adaptors
- **Match the existing component's prefix convention** (discovered in Step 0):

| Access type | PascalCase (preferred) | `T<COMP>_set/get` style | `CP_`/`GP_` style |
|-------------|----------------------|-------------------------|---------------------|
| Wrap static function | `CallPrivate_<COMP>_<Func>()` | — | `CP_<COMP>_<Func>()` |
| Read private variable | `GetPrivate_<COMP>_<Var>()` | `T<COMP>_get<Var>()` | `GP_<COMP>_<Var>()` |
| Write private variable | `SetPrivate_<COMP>_<Var>()` | `T<COMP>_set<Var>()` | — |

- The adaptor is placed in **`UnitUnderTest`** module in the `.bcfg`, not in `TestCase`

---

## 5. DEM Stub Verification Patterns

Three DEM stub styles exist across modules. Use whichever is **already established** in the component:

### Style A — Structured (RBADC, RBuCWatchdog — recommended for new code)

```c
T<COMPONENT>_DEM_ResetAll();                    /* reset before each test */
<COMPONENT>_Process();                          /* call function under test */
SWT_EvalEq(T<COMPONENT>_DEM_GetFailEntry().id,     DemConf_DemEventParameter_<EVENT>);
SWT_EvalEq(T<COMPONENT>_DEM_GetFailEntry().status, DEM_EVENT_STATUS_FAILED);
SWT_EvalEq(T<COMPONENT>_DEM_GetSystemStatus(),     DEM_SYSTEM_FAILED);
```

### Style B — Indexed array (RBECM)

```c
SWT_EvalEqX(TRBECM_FailureEntry_ID, DemConf_DemEventParameter_<EVENT>);
SWT_EvalEqX(TRBECM_FailureEntry_Status, DEM_EVENT_STATUS_FAILED);
SWT_EvalEqX(TRBECM_FailureEntry_debug0, 0xDEAD);
SWT_EvalEqX(TRBECM_FailureEntry_debug1, 0xBEEF);
```

### Style C — Per-event flags (RBEVP)

```c
SWT_Eval(DemStubTest_EventStatus[DemConf_DemEventParameter_<EVENT>] == DEM_EVENT_STATUS_PREFAILED);
```

### Style D — Helper functions (RBuCWatchdog)

```c
DemStub_EnvReset();
<COMPONENT>_Function(input);
SWT_EvalEq(DemStub_isFailed(DemConf_DemEventParameter_<EVENT>), true);
SWT_EvalEq(DemStub_GetLastReportedDebugData0(DemConf_DemEventParameter_<EVENT>), expectedDebug0);
```

---

## 6. Stub Reset Discipline

Reset stub state **at the beginning of each test** to ensure test isolation:

```c
SWTEST void T<COMPONENT>_Test_001(void)
{
  /* Reset all stubs first */
  T<COMPONENT>_DEM_ResetAll();
  tstub_ret_<Dep>_Function = <DefaultValue>;
  tstub_call_<Dep>_Function = 0u;

  /* ... rest of test */
}
```

If the component provides a bulk reset (e.g. `DemStub_EnvReset()`, `FUN_ResetRequestBuffer_v()`), use it.

---

## 7. Coverage Requirements

Each test file should cover at least:

| Category | Minimum |
|----------|---------|
| **Normal / happy path** | All main-path branches |
| **Boundary values** | Min/max of ranges, enum boundaries |
| **Error / invalid input** | Values that trigger DEM FAILED, early return, or `cc_assert` |
| **State transitions** | All reachable state changes for state machines |
| **Feature-switch variants** | Wrap in `#if(RBFS_…)` guards matching production code |
| **Multi-core behavior** | Test with different core IDs if function is core-aware |

---

## 8. GenAI Code Tagging Requirements

### Tagging Methods

**File-Level Tagging** (use when multiple functions contain generated code):
```c
 * // ContainsGenAICopilot - This notice needs to remain attached to any reproduction of this file.
```

**Function-Level Tagging** (use for individual functions):
```c
 * // ContainsGenAICopilot - This notice needs to remain attached to any reproduction of this function.
```

### Code Requiring Tagging
- Complex test algorithms with unique logic flow
- Custom stub implementations with sophisticated behavior simulation
- Original wrapper patterns not found in existing codebase
- Innovative test data structures or validation approaches

### Code NOT Requiring Tagging
- Standard `SWT_EvalEq()` assertions
- Basic stub function signatures matching standard patterns
- Standard copyright headers and include guards
- Standard message interface definitions

---

## 9. Self Review Checklist

Before considering unit test code complete:

**Mandatory — Test File Structure**
- [ ] `SwTest_Global.h` is the **first** include — no exceptions
- [ ] Every test function has the `SWTEST` decorator
- [ ] No stub functions defined inline in the test `.c` file — stubs are in separate stub files
- [ ] Bosch copyright header present

**Mandatory — Test Specification**
- [ ] Every test function has `\UT_TestCaseName` (or `\TestCaseName`) matching the function name exactly
- [ ] Every test function has `\UT_Reference` with at least one requirement ID or function-under-test
- [ ] `\UT_Sequence` uses numbered steps (`1)`, `2)`, ...) with concrete function/variable names
- [ ] `\UT_ExpectedResult` uses `@N)` annotations tied to sequence steps with SWT macro names
- [ ] Tag prefix (`\UT_` vs unprefixed) is consistent within the entire file — never mixed

**Mandatory — Assertions**
- [ ] `SWT_EvalEq` used for equality checks (not `SWT_Eval(a == b)`)
- [ ] DEM tests verify **both** `EventId` **and** `EventStatus`
- [ ] Table-driven tests use `SWT_Info` to log the current index

**Mandatory — Test Isolation**
- [ ] Stubs are reset at the start of each test function
- [ ] Private state accessed only through adaptors — production source is not modified
- [ ] Tests are independent — no test depends on the execution order of another test

**Quality — Test Coverage**
- [ ] Normal path, boundary, and error paths covered
- [ ] Feature-switch variants wrapped in `#if(RBFS_…)` guards
- [ ] Multi-core behavior tested where applicable

---

## IMPORTANT REMINDER

**This instruction file is for TEST CODE IMPLEMENTATION ONLY:**

✅ **DO GENERATE:**
- `SWTEST` test function bodies with Arrange/Act/Assert structure
- Doxygen test specification comment blocks directly above each function
- `SWT_EvalEq` / `SWT_Eval` assertion statements
- `RBMESG_SendMESG` / `RBMESG_RcvMESG` for message injection/verification
- Feature-switch `#if(RBFS_…)` guards around variant-specific tests

❌ **DO NOT GENERATE from this instruction (handled elsewhere):**
- Production / functional implementation code
- Adaptor `.c/.h` files → use `7_UnitTest_EnvironmentSetup.instructions.md`
- Stub `.c/.h` files → use `5_UnitTest_Stubs.instructions.md`
- `.bcfg` build config → use `4_UnitTest_BuildConfig.instructions.md`
- Test specification rules → use `8_UnitTest_TestSpecification.instructions.md`
