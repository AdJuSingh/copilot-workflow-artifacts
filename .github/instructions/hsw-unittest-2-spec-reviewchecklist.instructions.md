---
applyTo: "**/tst/**"
description: "HSW Unit Test Specification Review Checklist"
---

# HSW Unit Test Specification Review Checklist

## Purpose
This instruction file provides the review checklists and quality gate criteria for evaluating unit test specification documents for HSW (Hardware related Software) components.

**IMPORTANT**: This checklist is for reviewing unit test specifications only. It does not cover review of actual test implementation code.

---

## Technical Review Checklist

### File Structure and Organization
- [ ] **File Header**: Standardized header present with module name, component identification, description, copyright notice, and ingroup tags
- [ ] **Dependencies**: All required dependency categories specified (framework headers, test framework includes, configuration defines, stub files, test adaptors)
- [ ] **File Consistency**: Single documentation pattern used consistently throughout the file (no mixing of Primary and Alternative patterns)

### Function Naming Convention Compliance
- [ ] **Naming Pattern**: All test function names follow one of the accepted naming patterns:
  - Primary: `T[COMPONENT]_[MODULE/FUNCTION]_[TestCase]_[Number]`
  - Process: `T[MODULE]_PRC_[FunctionName]_[TestNumber]`
  - Function: `T[COMPONENT]_Fun_[FunctionName]_[TestCase]`
  - Legacy: `T[COMPONENT]_FUN_[function_name]`
- [ ] **Naming Consistency**: Consistent naming pattern used within the file
- [ ] **Function Type Categories**: Correct use of PRC, Fun/FUN, Check, Set prefixes matching test intent

### Test Function Documentation Completeness
- [ ] **Test Case Name**: Every test function has a `\UT_TestCaseName` (or `\TestCaseName`) matching the function name
- [ ] **Reference**: Every test function has `\UT_Reference` (or `\Reference`) linking to DSD functions and requirement IDs (e.g., Gen_SWCS_HSW_ECU_ComponentName-XXX)
- [ ] **Purpose**: Every test function has a clear `\UT_Purpose` (or `\Purpose`) explaining what the test validates
- [ ] **Sequence**: Every test function has `\UT_Sequence` (or `\Sequence`) with step-by-step execution description
- [ ] **Expected Result**: Every test function has `\UT_ExpectedResult` (or `\ExpectedResult`) with specific validation criteria

### Requirements Traceability
- [ ] **Forward Traceability**: Every DSD requirement referenced in the specifications maps to at least one test case
- [ ] **Backward Traceability**: Every test case references at least one DSD requirement or design element
- [ ] **Requirement ID Format**: Requirement references use correct format (Gen_SWCS_HSW_ECU_ComponentName-XXX)
- [ ] **Complete Coverage**: All functions described in the DSD have corresponding test specifications

### Test Design Quality
- [ ] **Setup Phase**: Test preconditions and initialization requirements are clearly specified
- [ ] **Positive Scenarios**: Normal/expected behavior test cases are specified for each function
- [ ] **Negative Scenarios**: Error/fault/boundary condition test cases are specified
- [ ] **State Transitions**: State machine transitions are tested (if applicable)
- [ ] **Boundary Conditions**: Edge cases and boundary values are addressed
- [ ] **Fault Injection**: Fault scenarios and recovery behavior are tested (if applicable)

### Conditional Compilation and Variants
- [ ] **Feature Flags**: Tests guarded by appropriate feature flags where needed
- [ ] **Hardware Variants**: All supported hardware configurations are addressed
- [ ] **Unsupported Variants**: Proper handling specified for unsupported unit variants

### Test Categories Coverage
- [ ] **Actuation Tests**: Actuation modes and relay configurations tested (if applicable)
- [ ] **State Transition Tests**: ON/OFF, running/stopped, failure states tested (if applicable)
- [ ] **Timing/Counter Tests**: Timing-dependent and counter behaviors tested (if applicable)
- [ ] **Fault Handling Tests**: Initial test, cyclic monitoring, GPIO, overcurrent faults tested (if applicable)
- [ ] **Configuration Variant Tests**: Hardware-specific test cases present (if applicable)

### Delta Change Compliance (for incremental updates only)
- [ ] **Existing Tests Preserved**: No unintended modifications to working test specifications
- [ ] **New Tests Properly Added**: New test cases added after existing ones
- [ ] **Change Comments**: DELTA_CHANGE or NEW/UPDATED markers present for changes
- [ ] **Backward Compatibility**: Existing test specifications remain valid
- [ ] **Feature Flags Updated**: Conditional compilation updated for new features

---

## Review Severity Classification

- 🔴 **Critical**: Blocks approval — missing required documentation fields, incorrect requirement references, DSD prerequisite not met
- 🟠 **Major**: Must be addressed — incomplete test coverage, missing test categories, inconsistent naming
- 🟡 **Minor**: Should be addressed — formatting issues, minor documentation gaps, style deviations
- 🔵 **Observation**: Optional improvement — suggestions for additional test cases, clarity enhancements

---

## Review Verdict Criteria

### Approved
All Critical and Major items pass. No outstanding blockers.

### Approved with Conditions
No Critical items. Major items have documented remediation plan with timeline.

### Rejected
One or more Critical items fail, OR multiple Major items remain unresolved.
