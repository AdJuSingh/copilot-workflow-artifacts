---
applyTo: "**/tst/**"
description: "Unit test specification writing guidelines"
---

# Unit Test Specification Writing Instructions

## Overview
This document provides instructions for writing unit test **SPECIFICATIONS ONLY** — specification documentation and design requirements, not actual code implementation.

**IMPORTANT**: Do not generate any actual test implementation code, test execution code, or functional code. Focus exclusively on specification documentation.

## Prerequisites

### Required Artifacts
The user must attach the following artifacts before specification generation can begin:
1. **Detailed Software Design (DSD) document** — the design document for the component under test
2. **Existing test file** (if updating) — the current test specification file for delta changes

Do NOT search the workspace for these files. If they are not attached, ask the user to provide them.

### Design Document Status Verification
Before generating unit test specifications, verify that the attached DSD document has a status of **REVIEWED** or **APPROVED**.

#### Status Check Process:
1. **Check Document Status**: Look for status indicators in the attached DSD document's header or metadata:
   - `DRAFT` — Document is still under development
   - `REVIEWED` — Document has been reviewed
   - `APPROVED` — Document is formally approved
   - `FINAL` — Document is complete and finalized

2. **Status-Based Response**:
   - **DRAFT**: Do NOT generate specifications. Respond with:
     ```
     ❌ **Unit Test Specification Generation Blocked**
     
     The detailed software design document has a status of "DRAFT" and has not yet been reviewed.
     
     **Required Action**: Have the DSD document reviewed and approved before proceeding.
     
     **Next Steps**:
     1. Submit the DSD document for technical review
     2. Address review comments
     3. Update status to "REVIEWED" or "APPROVED"
     4. Return for unit test specification generation
     ```
   - **REVIEWED/APPROVED/FINAL**: Proceed with specification generation.
   - **Missing or Unclear**: Request clarification from the developer before proceeding.

## File Structure and Organization

### File Header
Each unit test specification file should include:
- Module name and component identification
- Brief description of the test file purpose
- Copyright notice
- Proper documentation group tags

### Required Dependencies
Specify the following dependency categories:
- Test framework includes
- Configuration prevention defines
- Module-specific test configuration
- Stub file includes and test adaptors

## Test Function Specification Structure

### Function Naming Convention
Function naming must follow the pattern `T<COMPONENT>_<FunctionOrFeature>_<Scenario>` or `T<COMPONENT>_<DescriptiveName>`. Choose one based on project standards and use it consistently:

**Primary Pattern:**
- Format: `T<COMPONENT>_<FunctionOrFeature>_<Scenario>`
- Example: `TMyComp_Init_CheckDefaults(void)`

**Process Test Pattern:**
- Format: `T<COMPONENT>_PRC_<FunctionName>_<TestNumber>`
- Example: `TMyComp_PRC_ProcessData_001(void)`

**Function Test Pattern:**
- Format: `T<COMPONENT>_Fun_<FunctionName>_<Scenario>`
- Example: `TMyComp_Fun_HandleEvent_NominalCase(void)`

**Function Type Categories:**
- **PRC**: Process test — tests complete process flows
- **Fun/FUN**: Function test — tests individual functions
- **Check**: Validation test — tests specific checks or states
- **Set**: Configuration test — tests setup/configuration functions

### Test Function Documentation
Each test function must include a Doxygen-style comment block preceding the `SWTEST` function. Every block **must** contain these five tags **in order**:

| # | Tag | Description |
|---|-----|-------------|
| 1 | `\TestCaseName` | Unique identifier — **must exactly match** the function name. |
| 2 | `\Reference` | Traceability link — requirement ID(s) and/or function-under-test name. |
| 3 | `\Purpose` | One or two sentences describing **what** is being verified (not *how*). |
| 4 | `\Sequence` | Numbered list of **actions** (setup → call → observe) using `N)` format. |
| 5 | `\ExpectedResult` | What the test asserts — keyed to sequence step numbers with `@N)` annotations. |

> **Tag prefix convention:** Use unprefixed tags (`\TestCaseName`, `\Reference`, …) by default. The `\UT_` prefix (`\UT_TestCaseName`, `\UT_Reference`, …) is an accepted alternative; choose one style per file and remain consistent. Never mix prefixed and unprefixed tags in the same file.

#### Sequence Rules
- Use numbered steps with the format `N)` (e.g. `1)`, `2)`, `3)`).
- **Every step must use concrete names** — write the actual function names, variable names, and parameter values that appear in the test body. Never use vague descriptions like "set the voltage" or "read the status".
  - **Function calls:** include the full function name and arguments, e.g. `T<COMPONENT>_SetInput(5)` not "Set the input to 5".
  - **Variables:** name the variable being read or written, e.g. `l_ResultStatus` not "the result status".
  - **Values:** include the literal value being set, e.g. `8` not "a higher value".
- Each step describes one discrete action.
- Steps should map clearly to lines in the test body.

#### ExpectedResult Rules
- Tie each expected result to a **step number** from `\Sequence` using the `@N)` annotation prefix.
- Only reference steps that produce an observable check.
- **Include the SWT assertion macro** that will be used in the test body:

| Macro | When to use |
|-------|-------------|
| `SWT_EvalEq(actual, expected)` | Equality check — most common |
| `SWT_Eval(expr)` | Generic boolean assertion |
| `SWT_EvalSystemFaultFree()` | No DEM FAILED event reported |

- State the variable/expression, the expected value, and optionally a brief meaning.

### Comment Block Formatting Rules

| Rule | Detail |
|------|--------|
| **Opening** | Start with `/**` on its own line. |
| **Line prefix** | Every intermediate line starts with ` * ` (space-asterisk-space). |
| **Closing** | End with ` */` on its own line. |
| **Blank separator** | One blank comment line (` *`) between each tag section. |
| **Alignment** | Continuation lines of a tag are indented to align with the text of the first line of that tag. |
| **No trailing whitespace** | Trim trailing spaces on every line. |
| **Placement** | The comment block appears immediately before the `SWTEST void` line — no blank lines between `*/` and `SWTEST`. |

### Example Documentation Format

**Primary Pattern (\UT_ prefix):**
```c
/**
 * \UT_TestCaseName TMyComp_Init_CheckDefaults
 *
 * \UT_Reference MyComp_PRC_Init(),
 *              Gen_SWCS_ComponentName-100, Gen_SWCS_ComponentName-101
 *
 * \UT_Purpose Check if component is correctly initialized with default values.
 *
 * \UT_Sequence
 * 1) Call TMyComp_SetInitConditions(0)
 * 2) Call CallPrivate_MyComp_PRC_Init()
 * 3) Read l_OutputA via TMyComp_GetOutputA()
 * 4) Read l_OutputB via TMyComp_GetOutputB()
 *
 * \UT_ExpectedResult
 * @3) SWT_EvalEq(l_OutputA, 0) — OutputA is default.
 * @4) SWT_EvalEq(l_OutputB, FALSE) — OutputB is default.
 *
 */
SWTEST void TMyComp_Init_CheckDefaults(void)
```

**Alternative Pattern (unprefixed):**
```c
/**
 * \TestCaseName TMyComp_FUN_ProcessData_NominalCase
 *
 * \Reference  MyComp_FUN_ProcessData,
 *             Gen_SWCS_ComponentName-200
 *
 * \Purpose    Verify output state is updated correctly based on input.
 *
 * \Sequence   1) Call TMyComp_SetInput(0)
 *             2) Call CallPrivate_MyComp_FUN_ProcessData()
 *             3) Read l_Output via TMyComp_GetOutput()
 *             4) Call TMyComp_SetInput(1)
 *             5) Call CallPrivate_MyComp_FUN_ProcessData()
 *             6) Read l_Output via TMyComp_GetOutput()
 *
 * \ExpectedResult
 *             @3) SWT_EvalEq(l_Output, 0) — output off when input is 0.
 *             @6) SWT_EvalEq(l_Output, EXPECTED_VALUE) — output on when input is 1.
 *
 */
SWTEST void TMyComp_FUN_ProcessData_NominalCase(void)
```

## Delta Change Support

When updating an existing test specification file:

1. **Preserve existing tests** — never modify working test specs unless necessary.
2. **Add after existing content** — append new test function specifications; do not reorder.
3. **Mark changes** — use `NEW:` for additions and `UPDATED:` for modifications.
4. **Maintain traceability** — include requirement references for all new or changed specs.
5. **Use conditional compilation** for optional or variant-specific features.
6. **Keep backward compatibility** — preserve existing includes, globals, and compilation behaviour.

## Relationship to Test Body

The test specification is a contract with the test body. Ensure:

1. **Every `\Sequence` step** has corresponding code in the test function.
2. **Every `@N)` expected result** has a matching `SWT_EvalEq` / `SWT_Eval` assertion in the body.
3. **The `\TestCaseName`** exactly matches the function name.

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| `\TestCaseName` does not match the function name | Copy-paste the function name into the tag. |
| Missing `\Reference` — no traceability link | Always provide at least one requirement ID or the function under test. |
| `\Sequence` is a single prose paragraph | Break into numbered steps (`1)`, `2)`, …). |
| `\Sequence` uses vague descriptions ("set voltage", "read status") | Use concrete function names, variable names, and literal values from the test body. |
| `\ExpectedResult` has no link to sequence steps | Use `@N)` annotations referencing the step numbers. |
| `\ExpectedResult` omits the SWT assertion macro | Include the specific macro, e.g. `SWT_EvalEq(var, expected)`. |
| Mixing `\UT_` and non-prefixed tags in the same file | Pick one style per file and stay consistent. |
| Comment block separated from `SWTEST` by blank lines | Place `*/` directly before `SWTEST void`. |
| Double-backslash (`\\TestCaseName`) in source | Use a single backslash; double backslash is a documentation rendering artefact. |

## Final Notes

This instruction file guides the creation of unit test **SPECIFICATIONS ONLY**.

**REMINDER**:
- Only generate test function specifications and documentation
- Do NOT generate any actual code implementation
- Do NOT provide test execution code or functional code
- Focus solely on requirement specifications, documentation patterns, and test design descriptions