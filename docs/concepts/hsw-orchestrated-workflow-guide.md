# ≡ƒöº HSW Orchestrated Workflow Guide

**Orchestrated Workflow for Hardware-Related Software (HSW) ΓÇö Brake Systems (VM-BS)**

> 9 Prompts &nbsp;|&nbsp; 9 Instructions &nbsp;|&nbsp; 6 Workflow Stages

---

## ≡ƒôæ Contents

1. [Overview ΓÇö How to Work with HSW Orchestrated Workflow](#overview)
2. [Orchestrated Workflow Pipeline](#workflow)
3. [Stage 1 ΓÇö DSD Generation](#stage1)
4. [Stage 1R ΓÇö DSD Review](#stage1r)
5. [Stage 2 ΓÇö Unit Test Specification](#stage2)
6. [Stage 2R ΓÇö UT Spec Review](#stage2r)
7. [Stage 3 ΓÇö Unit Test Environment Setup](#stage3)
8. [Stage 4 ΓÇö Unit Test Code Generation](#stage4)
9. [Stage 5 ΓÇö Unit Test Execution](#stage5)
10. [Implementation Assist](#impl)
11. [Memory Orchestrator & Learnings](#memory)

---

## ≡ƒÅù∩╕Å Overview ΓÇö How to Work with HSW Orchestrated Workflow <a id="overview"></a>

This guide walks HSW developers through the **Orchestrated Agent Workflow** ΓÇö a concept aligned with the existing HSW development workflow, covering the end-to-end pipeline from DSD generation through unit test execution. This workflow orchestration keeps the human in the loop, helping to speed up the development process while bringing consistency and alignment across each stage.

> **≡ƒÆí Key Principle**
> This guide covers the AI-assisted orchestrated workflow for HSW development using GitHub Copilot Agent Mode. Each stage is **developer-triggered** ΓÇö you decide when and whether to proceed.

---

## ≡ƒöä Orchestrated Workflow Pipeline <a id="workflow"></a>

The HSW orchestrated workflow consists of multiple developer-triggered stages. Each stage has a dedicated **prompt** and **instruction file**. Review stages (1R, 2R) intentionally use different LLMs to reduce confirmation bias during review.

> **≡ƒôî Two Supported Approaches**
>
> The workflow supports both development approaches:
> - **Test-Driven Development (TDD):** DSD ΓåÆ UT Spec ΓåÆ UT Code ΓåÆ Production Code (Implementation Assist)
> - **Code-to-Spec:** DSD ΓåÆ Production Code (Implementation Assist) ΓåÆ UT Spec ΓåÆ UT Code
>
> The stages remain the same ΓÇö only the **order** changes based on team preference. Developers who already have production code can jump directly to UT Specification after DSD Review.

### Pipeline Overview

```
[1] DSD Generation ΓåÆ [1R] DSD Review ΓåÆ [2] UT Spec Gen ΓåÆ [2R] UT Spec Review ΓåÆ [3] UT Env Setup ΓåÆ [4] UT Code Gen ΓåÆ [5] UT Execution
```

### Artifact Flow & Traceability

```
Requirements (*_Req.md)
      Γåô
DSD Document (*.md)
      Γåô
Production Code (*.c / *.h)
      Γåô
UT Specification (T{unitname}.c)
      Γåô
UT Code (T{unitname}.c)
```

> Each artifact traces back to its predecessor. Bidirectional traceability is achieved.

---

## ≡ƒô¥ Stage 1 ΓÇö Detailed Software Design (DSD) Generation <a id="stage1"></a>

**Prompt:** `/hsw-dsd-generator`
**Model:** Claude Sonnet 4.6 &nbsp;|&nbsp; **Instruction:** `hsw_dsd_generator.instructions.md`

### Purpose

Generates a complete Detailed Software Design document for an HSW unit by assembling context from requirements, design decisions (interface contracts), and prior learnings (optional).

### Required Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Requirements | `doc/req-as-code/` | `*_Req.md` ΓÇö must have **approved** status |
| Detailed Design | `src/` | `*.md` ΓÇö existing detailed design documents |
| CCB Minutes | `doc/ccb_minutes/` | Architectural context and change decisions |
| Agent Memory | `.github/memory/` | `dsdLearnings.memory.md` (optional) |

### DSD Template Sections (16 sections)

1. Document Header & Identification
2. Revision History & Approvals
3. References & Dependencies
4. Component Purpose & Scope
5. Requirements Traceability Matrix
6. System Architecture & Integration
7. Data Model & Type Definitions
8. Interface Contracts & Message Exchange
9. Process Scheduling & Timing
10. Control Flow & Algorithm Design
11. Safety Architecture & Diagnostics
12. Hardware Abstraction & Drivers
13. Configuration & Calibration
14. Memory Architecture & Resources
15. Testing Infrastructure & Observability
16. Implementation Standards & Coding Guidelines

> **≡ƒÜ¿ Execution Gate ΓÇö Requirements Status**
> DSD creation is **blocked** unless the requirements document has an **approved/reviewed/baseline/accepted** status. The agent validates this before proceeding.

### How to Run

```
1. Open VS Code ΓåÆ Copilot Agent Mode
2. Type: /hsw-dsd-generator
3. Attach your Requirement file, DSD File and interface contract file (if applicable)
4. The agent will:
   Γ£à Read instructions + coding rules + memory file (MANDATORY FIRST STEP)
   Γ£à Validate requirements status (GATE ΓÇö blocks if DRAFT)
   Γ£à Scan component structure and Read the relevant context (requirements, design decisions, CCB minutes, memory)
   Γ£à Generate DSD following all 16 template sections
   Γ£à Cross-verify against requirements & CCB minutes
```

### Verification Criteria

- All 16 DSD template sections are present and complete
- Every requirement from `*_Req.md` is traced to a design element
- Interface contracts match the component's `api/` headers
- Safety-relevant functions are tagged with the correct ASIL classification
- No DRAFT-status requirements were used as input
- CCB minutes and design decisions are reflected in the design rationale
- Memory file learnings from previous DSD cycles are incorporated (if applicable)

---

## ≡ƒöì Stage 1R ΓÇö DSD Review Checklist <a id="stage1r"></a>

**Prompt:** `/hsw-dsd-reviewchecklist`
**Model:** Claude Opus 4.6 *(different from generation!)* &nbsp;|&nbsp; **Instruction:** `hsw_dsd_reviewchecklist.instructions.md`

### Purpose

Reviews and validates the generated DSD against defined quality checklists. Uses a **different LLM model** than Stage 1 to reduce confirmation bias.

### Review Checklist Categories

| Category | Key Items |
|----------|-----------|
| **Architecture & Design** | Component scope, interface completeness, message protocols, data model, task architecture |
| **Safety & Reliability** | ASIL mapping, fault handling, diagnostic coverage, recovery procedures, HW dependencies |
| **Implementation Readiness** | MISRA C compliance, header dependencies, concurrency safety, resource management |
| **Documentation Quality** | Traceability, visual clarity, technical accuracy, maintainability, completeness |

### Finding Severity Levels

| Severity | Description |
|----------|-------------|
| ≡ƒö┤ **Critical** | Blocks approval ΓÇö gaps in critical areas |
| ≡ƒƒá **Major** | Must be addressed ΓÇö incomplete content |
| ≡ƒƒí **Minor** | Should be addressed ΓÇö formatting issues |
| ≡ƒö╡ **Observation** | Optional improvement suggestions |

### Verdict Options

- **Approved** ΓÇö All critical and major items pass
- **Approved with Conditions** ΓÇö No critical issues; major items have remediation plan
- **Rejected** ΓÇö Critical failures or multiple unresolved major items

### How to Run

```
1. Open VS Code ΓåÆ Copilot Agent Mode
2. Type: /hsw-dsd-reviewchecklist
3. Attach the generated DSD document, the corresponding requirements file and interface contract file (if applicable)
4. The agent will:
   Γ£à Read instructions + review checklist criteria
   Γ£à Evaluate DSD against all review checklist categories
   Γ£à Classify findings by severity (Critical / Major / Minor / Observation)
   Γ£à Produce a verdict: Approved, Approved with Conditions, or Rejected
```

---

## ≡ƒº¬ Stage 2 ΓÇö Unit Test (UT) Specification Generation <a id="stage2"></a>

**Prompt:** `/hsw-unittest-1-spec-generaor`
**Model:** Claude Sonnet 4.6 &nbsp;|&nbsp; **Instruction:** `hsw_unittest_spec_generator.instructions.md`

### Purpose

Generates unit test **specifications** ΓÇö the test design documentation describing what to test, how to test, and expected outcomes. This stage produces specification artifacts only, not executable test code. It supports both approaches: deriving specs purely from the DSD (TDD), or additionally leveraging existing production code to extract precise test scenarios (Code-to-Spec).

### Required Inputs ΓÇö Based on Development Approach

| Input | TDD (Spec First) | Code-to-Spec (Code First) |
|-------|-----------------|--------------------------|
| DSD Document (REVIEWED/APPROVED) | Γ£à Required | Γ£à If available |
| Requirements (`*_Req.md`) | Γ£à Required | Γ£à Required |
| Testable Unit (`T{unitname}` `*.c`) | Γ£à Required ΓÇö the source file(s) under test | Γ£à Required ΓÇö the source file(s) under test |
| Production Code (`*.c / *.h`) | ΓÇö Not available yet | Γ£à Required ΓÇö used for deriving test scenarios from actual implementation |
| Agent Memory | Optional | Optional |

> **≡ƒôî Code-to-Spec: Production Code as Input**
> If you are **not following TDD** and already have production code, attach the source files (`*.c / *.h`) alongside the DSD. The agent will use the actual implementation to derive more precise and complete test specifications ΓÇö covering real branches, boundary conditions, and error paths present in the code.

> **≡ƒÜ¿ DSD Status Gate**
> The DSD document must have **REVIEWED** or **APPROVED** status. If **DRAFT**, specification generation is blocked.

### How to Run

```
1. Open VS Code ΓåÆ Copilot Agent Mode
2. Type: /hsw-unittest-1-spec-generaor
3. Attach the following based on your approach:
   ΓÇö TDD: DSD document (REVIEWED/APPROVED) + Requirements file + Testable unit (*.c)
   ΓÇö Code-to-Spec: Requirements file + Testable unit + Production code (*.c)
4. The agent will:
   Γ£à Read instructions + memory file (if applicable)
   Γ£à Validate DSD status (GATE ΓÇö blocks if DRAFT)
   Γ£à Analyze the testable unit and derive test scenarios
   Γ£à Generate UT specifications with proper naming and Doxygen tags
   Γ£à Ensure traceability back to requirements and DSD
```

---

## ≡ƒöì Stage 2R ΓÇö Unit Test (UT) Specification Review <a id="stage2r"></a>

**Prompt:** `/hsw-unittest-2-spec-reviewchecklist`
**Model:** Claude Opus 4.6 *(different from generation!)* &nbsp;|&nbsp; **Instruction:** `hsw_unittest_spec_reviewchecklist.instructions.md`

### Review Categories

| Category | Description |
|----------|-------------|
| ≡ƒôä **File Structure** | Standardized header, dependencies, framework includes, consistent patterns |
| ≡ƒÅ╖∩╕Å **Naming Compliance** | Accepted patterns (Primary/Process/Function), PRC/Fun/Check prefixes |
| ≡ƒô¥ **Documentation** | All 5 Doxygen tags present: TestCaseName, Reference, Purpose, Sequence, ExpectedResult |
| ≡ƒöù **Traceability** | Forward + backward traceability, requirement ID format, coverage check |
| ≡ƒº¬ **Test Design Quality** | Positive, negative, boundary, state transitions, fault injection scenarios |
| ≡ƒöÇ **Variant Coverage** | Feature flags, hardware variants, conditional compilation guards |

### How to Run

```
1. Open VS Code ΓåÆ Copilot Agent Mode
2. Type: /hsw-unittest-2-spec-reviewchecklist
3. Attach the generated UT specification file and the corresponding DSD document &/or production code (if Code-to-Spec)
4. The agent will:
   Γ£à Read instructions + review checklist criteria
   Γ£à Validate file structure, naming compliance, and Doxygen tags
   Γ£à Check traceability (forward + backward) against requirements
   Γ£à Assess test design quality (positive, negative, boundary, fault injection)
   Γ£à Verify variant coverage and produce a review verdict
```

---

## ΓÜÖ∩╕Å Stage 3 ΓÇö Unit Test Environment Setup <a id="stage3"></a>

**Prompt:** `/hsw-unittest-3-environmentsetup`
**Model:** Claude Sonnet 4.6 &nbsp;|&nbsp; **Instruction:** `hsw_unittest_environmentsetup.instructions.md`

### Purpose

Creates the complete test infrastructure for a delta change in the existing feature or a new feature ΓÇö **all three artifacts must be created together**:

| Artifact | File | Purpose |
|----------|------|---------|
| **.bcfg** | `cfg/T<COMP><Feature>_BuildConfig.bcfg` | Build configuration with 3 sub-modules: UnitUnderTest, TestCase, Stub |
| **Adaptor** | `T<COMP>_<Feature>Adaptor.c/.h` | White-box access to `static` variables and functions |
| **Stubs** | `stubs/T<COMP>_<Dep>Stub.c/.h` | Controllable replacements for external dependencies |

> **ΓÜá∩╕Å Critical ΓÇö Scan Before You Create**
> Folder layouts, naming conventions, adaptor prefix styles, and stub directory names **vary significantly** across HSW components. The agent must scan the target component's existing `tst/` directory before creating any file.

### How to Run

```
1. Open VS Code ΓåÆ Copilot Agent Mode
2. Type: /hsw-unittest-3-environmentsetup
3. Attach the UT specification file (testable unit .c file)
4. The agent will:
   Γ£à Scan the existing tst/ directory for naming conventions and folder structure
   Γ£à Create the .bcfg build configuration with three sub-modules
   Γ£à Generate the Adaptor files (*.c / *.h) for white-box access
   Γ£à Generate Stub files for external dependencies
```

---

## ≡ƒÆ╗ Stage 4 ΓÇö Unit Test Code Generation <a id="stage4"></a>

**Prompt:** `/hsw-unittest-4-codegeneration`
**Model:** Claude Sonnet 4.6 &nbsp;|&nbsp; **Instruction:** `hsw_unittest_codegeneration.instructions.md`

### Purpose

Implements actual unit test function bodies ΓÇö **test code only, not production code**. Follows Arrange/Act/Assert structure.

### Mandatory Discovery ΓÇö Step 0

Before writing any code, the agent **must** scan:

1. **Adaptor header** ΓÇö discover `CallPrivate_`, `GetPrivate_`, `SetPrivate_` functions
2. **Stub headers** ΓÇö discover `tstub_ret_`, `tstub_call_` variables and DEM API
3. **Existing test files** ΓÇö discover assertion style and Doxygen convention
4. **Test specifications** ΓÇö map requirement IDs and expected behaviors

### Test Patterns

| Pattern | Description |
|---------|-------------|
| Γ£à **Happy Path** | Normal execution, verify DEM_SYSTEM_FAIL_FREE |
| Γ¥î **Failure Path** | Verify EventId + EventStatus + debug data |
| ≡ƒôè **Table-Driven** | Input/output combos with SWT_Info for diagnosability |
| ≡ƒöä **State Machine** | Multi-step cycle through all reachable states |
| ≡ƒô¿ **RBMESG Injection** | Inject + call + verify message values |
| ≡ƒ¢í∩╕Å **Assert/Defensive** | SWT_AssertCheckStart ΓåÆ invalid input ΓåÆ SWT_AssertCheckEnd |

### How to Run

```
1. Open VS Code ΓåÆ Copilot Agent Mode
2. Type: /hsw-unittest-4-codegeneration
3. Attach the UT specification file (testable unit) .c file
4. The agent will:
   Γ£à Discover Adaptor functions (CallPrivate_, GetPrivate_, SetPrivate_)
   Γ£à Discover Stub variables and DEM API patterns (if applicable)
   Γ£à Scan existing test files for assertion style and conventions
   Γ£à Implement test function bodies following Arrange/Act/Assert
   Γ£à Use correct SWT assertion macros
```

---

## Γû╢∩╕Å Stage 5 ΓÇö Unit Test Execution <a id="stage5"></a>

**Prompt:** `/hsw-unittest-5-execution`
**Model:** Claude Sonnet 4.6 &nbsp;|&nbsp; **Instruction:** `hsw_unittest_execution.instructions.md`

### Purpose

Discovers, builds, executes, and analyzes unit test results via the **LightlyBuild** automation framework. **No code modifications** ΓÇö read-only execution and analysis.

### Execution Command

```bat
rb\as\core\tools\libu\LightlyBuild.cmd ^
    --gendir=Gen ^
    --config=<TEST_CONFIG_NAME> ^
    --test ^
    --clean-first ^
    --not-parallel ^
    --simplexmlconfig_file=<PATH_TO_UNITTEST_XML>
```

### 6-Gate Execution Flow

| Gate | Action |
|------|--------|
| ≡ƒöì **Discovery** | Locate component, find `*_unittests.xml`, parse config names |
| Γ£à **Validation** | Verify project root, `LightlyBuild.cmd`, `.bcfg`, MTC tools |
| ≡ƒÜ¿ **Confirmation** | Present command to user, wait for approval |
| Γû╢∩╕Å **Execution** | Run LightlyBuild, monitor output |
| ≡ƒôè **Analysis** | Parse results, diagnose failures, check `Gen/` logs |
| ≡ƒôï **Reporting** | Summary: config, build status, test counts, root cause analysis |

> **≡ƒÆí Common Failure Causes**
> Missing stubs, incorrect include paths in `.bcfg`, config name mismatch, forward vs backslash path issues.

### How to Run

```
1. Open VS Code ΓåÆ Copilot Agent Mode
2. Type: /hsw-unittest-5-execution
3. Attach or point to the component's unit test directory along with testable unit
4. The agent will:
   Γ£à Discover the component and locate *_unittests.xml
   Γ£à Validate project root, LightlyBuild.cmd, and .bcfg files
   Γ£à Present the execution command for your approval
   Γ£à Run LightlyBuild and monitor output
   Γ£à Parse results, diagnose failures, and produce a summary report
```

---

## ≡ƒö¿ Implementation Assist ΓÇö Production Code <a id="impl"></a>

**Prompt:** `/hsw-implementation-assist`
**Model:** Claude Sonnet 4.6 &nbsp;|&nbsp; **Instruction:** `hsw_implementationAssist.instructions.md`

### Purpose

Implements production C code from validated DSD documents with full ISO 26262 ASIL D compliance. Requires a **REVIEWED/APPROVED** DSD.

### Key Features

- **GenAI Code Tagging**: `// ContainsGenAICopilot` on all original generated code
- **Mandatory Copyright Header**: Every `.c` and `.h` file starts with Bosch copyright
- **Process Scheduling**: Correct SPG placement in `*_Subsystem.proc`
- **MISRA C Compliance**: Automotive safety-critical coding standard

### GenAI Tagging Example

```c
/**
 * @brief Motor actuation control algorithm
 *
 * // ContainsGenAICopilot - This notice needs to remain
 * // attached to any reproduction of this function.
 */
void RBRFPEC_PRC_ActuationControl_1ms(void)
{
    /* Implementation */
}
```

### How to Run

```
1. Open VS Code ΓåÆ Copilot Agent Mode
2. Type: /hsw-implementation-assist
3. Attach the REVIEWED/APPROVED DSD document and the target source files (*.c / *.h)
4. The agent will:
   Γ£à Read instructions + coding rules
   Γ£à Validate DSD status (GATE ΓÇö blocks if DRAFT)
   Γ£à Implement production C code following DSD specifications
   Γ£à Apply GenAI tagging (// ContainsGenAICopilot) to generated code
   Γ£à Ensure MISRA C compliance and correct process scheduling
```

---

## ≡ƒºá Memory Orchestrator & Learnings <a id="memory"></a>

**Prompt:** `/hsw-memory-orchestrator`
**Model:** Claude Sonnet 4.6 &nbsp;|&nbsp; **User-triggered only** ΓÇö never invoked autonomously

### Purpose

Routes user-provided learnings to the correct memory file based on the activity context. Captures corrections, insights, and preferences for future sessions.

### Activity ΓåÆ Memory File Routing

| Activity | Memory File |
|----------|-------------|
| DSD Creation / Review | `dsdLearnings.memory.md` |
| UT Specification | `unitTestSpecLearnings.memory.md` |
| UT Code Generation | `unitTestCodeLearnings.memory.md` |
| Implementation | `implementationLearnings.memory.md` |
| Cross-cutting | All relevant files |

### Memory Entry Format

```markdown
### 2026-03-08 ΓÇö Short descriptive title
**Activity**: DSD Creation
**Context**: Working on RBRFPEC motor actuation design
**Learning**: What was learned and why it matters for future sessions
```

### When to Trigger

- You provided corrections during Stage 1 or Stage 2 not already in instructions
- The agent made assumptions that should be guided differently next time
- A pattern or convention was clarified that benefits future runs

> **Γ£à Best Practice**
> Keep memory files lean ΓÇö only record genuinely new learnings that aren't covered by instruction files. Periodically graduate stable learnings into instruction files.

### How to Run

```
1. Open VS Code ΓåÆ Copilot Agent Mode
2. Type: /hsw-memory-orchestrator
3. Describe the learning or correction you want to record
4. The agent will:
   Γ£à Identify the activity context (DSD, UT Spec, UT Code, Implementation)
   Γ£à Route the learning to the correct memory file
   Γ£à Format the entry with date, activity, context, and learning
   Γ£à Append to the appropriate memory file
```

---

## ≡ƒÄ» Key Principles to Remember

| Principle | Description |
|-----------|-------------|
| ≡ƒöÆ **Local-First Execution** | All prompt execution happens locally. No source code leaves your machine during agent execution. |
| ≡ƒÜª **Gate-Driven Quality** | Every stage has mandatory execution gates ΓÇö prerequisite checks, template compliance, accuracy verification. |
| ≡ƒºá **Model Diversity** | Generation uses Sonnet, Review uses Opus ΓÇö different models reduce confirmation bias in quality checks. |
| ≡ƒæñ **Developer Control** | All stages are developer-triggered. You decide when to proceed, skip, or iterate. No automatic chaining. |
| ≡ƒöì **Scan Before You Create** | Module conventions vary. The agent must discover existing patterns before generating any new files. |
| ≡ƒô¥ **Memory is Optional** | Only capture learnings worth persisting. Keep memory lean for focused context in future sessions. |

---

*HSW Orchestrated Workflow Guide ΓÇö VM-BS Hardware-Related Software*

*Part of the [Orchestrated Agent Workflow](OrchestratedAgentWorkflow_ConceptAndArchitecture.md) ΓÇó Platform: `platform/vm-bs/hsw/`*

*Author: Harish Desai*

*┬⌐ Robert Bosch GmbH ΓÇö Created with assistance from GitHub Copilot, human-reviewed and adapted ΓÇó Last updated: March 2026*
