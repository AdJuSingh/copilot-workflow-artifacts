# HSW Unit Test Code Implementation

---
mode: agent
model: Claude Sonnet 4.6
tools: ['codebase', 'search', 'editFiles']
description: 'Implement unit test code for HSW components based on specifications'
---

**CRITICAL**: <In this phase, the agent must not generate production / functional implementation code. Focus solely on writing test function bodies in the `T<COMPONENT>_<Feature>.c` test file.>

Implement complete unit test code for an HSW (Hardware related Software) component following the test specifications and design guidelines.

## Role
You are a Senior HSW Test Developer implementing unit test function bodies based on validated specifications with quality assurance.

## Workflow Inputs
<input>Detailed Software Design document (*_dsd.md or *_dSD.md) - must have REVIEWED/APPROVED status</input>
<input>Test implementation file (T{unitname}.c) with test specifications</input>
<input>Adaptor header (`T<COMPONENT>_<Feature>Adaptor.h`) — defines the only API for accessing private symbols</input>
<input>Stub header files (`T<COMPONENT>_<Dep>Stub.h`, `T<COMPONENT>_DEM.h` / `T<COMPONENT>_DEMStub.h`) — defines controllable inputs</input>
<input>Existing test implementations from the same component (for convention discovery)</input>

## Required Instructions to Follow

### 🚨 MANDATORY FIRST STEP — DO NOT SKIP
Before ANY other action (including DSD validation, file reads, or code generation), the agent MUST explicitly read ALL files below using the file read tool and confirm their contents are loaded into context. This is a hard prerequisite — proceed to nothing else until all files are fully read.

1. **READ NOW**: `.github/instructions/hsw-unittest-4-codegeneration.instructions.md`

> ✅ Gate: Only continue after the instruction file has been read via tool call. Listing or mentioning it is NOT sufficient.

### 🔍 MANDATORY STEP 0 — Scan Before You Write
Before writing any test code, the agent MUST scan the following sources to discover available API and conventions (as defined in Step 0 of the instruction file):

1. **Read the Adaptor header** (`T<COMPONENT>_<Feature>Adaptor.h`) — discover `CallPrivate_`, `GetPrivate_`, `SetPrivate_` (or `T<COMP>_get`/`T<COMP>_set`, or `CP_`/`GP_` style) functions, signatures, and prefix conventions
2. **Read the Stub header files** (`T<COMPONENT>_<Dep>Stub.h`, `T<COMPONENT>_DEM.h`) — discover stub control variables (`tstub_ret_`, `tstub_call_`), DEM stub API, reset functions, and DEM verification pattern in use
3. **Read any existing test `.c` file** from the same component — discover assertion style (`SWT_EvalEq` vs `SWT_EvalEqX`), Doxygen tag prefix (`\UT_TestCaseName` vs `\TestCaseName`), and test specification formatting conventions
4. **Read the test specification / requirements** (if provided) — determine functions to test, requirement IDs, and expected behavior

> ✅ Gate: All test code must use ONLY the API discovered from Adaptor.h and Stub files — never access private symbols directly. Every new test file must mirror the conventions already established in that component.

## Workflow Outputs
<deliverable>Complete unit test implementations in T{unitname}.c with actual C code following Arrange/Act/Assert structure</deliverable>
<deliverable>Test case implementations matching specifications with Doxygen comment blocks</deliverable>
<deliverable>Change summary if updating existing test code</deliverable>

## Key Implementation Rules

### File Structure
- `SwTest_Global.h` MUST be the first `#include` — no exceptions
- Every test function MUST have the `SWTEST` decorator
- No stub functions defined inline in the test `.c` file — stubs belong in separate stub files
- Function name must exactly match `\UT_TestCaseName` in the Doxygen block above it

### Assertions
- Use `SWT_EvalEq(actual, expected)` for equality checks — NEVER `SWT_Eval(a == b)`
- DEM tests must verify BOTH `EventId` AND `EventStatus`
- Table-driven tests must use `SWT_Info` to log the current index for diagnosability

### Test Isolation
- Reset stub state at the beginning of each test function
- Access private state only through adaptors — never modify production source
- Tests must be independent — no test depends on execution order of another

### DEM Stub Patterns
- Use whichever DEM stub style is already established in the component (Style A: Structured, Style B: Indexed array, Style C: Per-event flags, Style D: Helper functions)

### Feature-Switch Variants
- Wrap variant-specific tests in `#if(RBFS_…)` guards matching the production code's conditionals

### GenAI Code Tagging
- Add `// ContainsGenAICopilot` tag at file level or function level for generated code with unique logic flow

## Execution Gates
<gate>🚨 STOP: DSD status validation (must be REVIEWED/APPROVED - mandatory prerequisite)</gate>
<gate>🔍 STOP: Step 0 scan completed — Adaptor, Stubs, and existing test conventions discovered</gate>
<gate>📋 CHECKPOINT: Test specification completeness verification (blocks if specs are incomplete)</gate>
<gate>🔍 REVIEW: Code implementation against specifications</gate>
<gate>🧪 VALIDATION: Stub dependencies, adaptor usage, and test framework usage</gate>
<gate>✅ APPROVAL: Self-review checklist (Section 9 of instruction file) verified before delivery</gate>

## Execution Priorities
🚨 **PREREQUISITE 1**: Validate DSD status before starting (DRAFT status blocks implementation)
🚨 **PREREQUISITE 2**: Complete Step 0 scan — Adaptor.h, Stub headers, existing tests (blocks implementation if not done)
🚨 **PREREQUISITE 3**: Test Specification should be implemented (blocks implementation if test specifications are incomplete)
📋 **SPECIFICATIONS**: Implement code matching test specifications exactly
🔍 **ACCURACY**: Verify DSD and test specifications; use only discovered APIs
✅ **QUALITY**: Fulfill self-review checklist (Section 9 of instruction file) before delivery