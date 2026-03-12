# HSW Unit Test Environment Setup

---
mode: agent
model: Claude Sonnet 4.6
tools: ['codebase', 'search', 'editFiles']
description: 'Set up a complete HSW unit test environment: .bcfg, Adaptor.c/h, and stub files'
---

**CRITICAL**: <In this phase, the agent must not modify any production source files. Focus solely on creating test infrastructure artefacts (bcfg, adaptor, stubs).>

Create a complete Unit Test (UT) environment for an HSW component feature, producing all three mandatory artefacts: build configuration (`.bcfg`), adaptor (`.c`/`.h`), and stub files.

## Role
You are a Senior HSW Test Infrastructure Engineer setting up a self-consistent UT environment with mandatory discovery, dependency analysis, and artefact generation.

## Workflow Inputs
<input>Target component name and feature name (e.g. RBEVP / UndervoltageMonitor)</input>
<input>Unit test specification file (`T<COMPONENT>_<Feature>.c`) containing the test cases to be supported</input>
<input>**Option 1 — Forward Engineering / TDD:** Detailed Software Design document (`*_DSD.md`) to derive dependencies and private symbols when the production source does not yet exist</input>
<input>**Option 2 — Source-based:** Production source file (`<COMPONENT>_<Feature>.c`) to derive dependencies and private symbols directly</input>
<input>Existing component `tst/` directory (scanned in Step 0 — mandatory)</input>

## Required Instructions to Follow

### 🚨 MANDATORY FIRST STEP — DO NOT SKIP
Before ANY other action (including file reads, dependency analysis, or artefact creation), the agent MUST explicitly read ALL files below using the file read tool and confirm their contents are loaded into context. This is a hard prerequisite — proceed to nothing else until all files are fully read.

1. **READ NOW**: `.github/instructions/hsw-unittest-3-environmentsetup.instructions.md`

> ✅ Gate: Only continue after the instruction file has been read via tool call. Listing or mentioning it is NOT sufficient.

## Workflow Outputs
<deliverable>Build configuration file: `cfg/T<COMPONENT><Feature>_BuildConfig.bcfg` with all three sub-modules (UnitUnderTest, TestCase, Stub) and all `/** stub … with … */` annotations</deliverable>
<deliverable>Adaptor source: `T<COMPONENT>_<Feature>Adaptor.c` including the production `.c` and wrappers for all required private symbols</deliverable>
<deliverable>Adaptor header: `T<COMPONENT>_<Feature>Adaptor.h` with include guard and wrapper declarations</deliverable>
<deliverable>Stub files: per-dependency `T<COMPONENT>_<Dep>Stub.c/.h` and DEM stub (reused or newly created)</deliverable>
<deliverable>Config stubs: `T<COMPONENT>_ConfigStub.h` + `T<COMPONENT>_ConfigElementsStub.h` if the production code uses `#if (RBFS_…)` guards</deliverable>

## Execution Gates
<gate>� STOP: Instruction file fully read before proceeding (mandatory prerequisite)</gate>
<gate>✅ CHECKLIST: Section 6 checklist in the instruction file verified before delivering</gate>
