# Unit Test with Unit Specification

Create a unit specification document and test file structure (WITHOUT TEST_F implementations) that provides the foundation for comprehensive testing. This phase focuses on documentation and planning, with actual test implementation occurring in Phase 3.

## Context Requirements
Analyze the following before generating the unit specification:
1. **Requirements Analysis**: Identify test scenarios, state transitions, boundary conditions, edge cases, and input/output relationships.
2. **Existing Test Pattern Analysis**: Review existing test files for structure, complexity, mock parameter patterns, and documentation style.
3. **Test Planning**: Plan core functionality, boundary value, state machine transitions, parameter dependency, and error handling scenarios.

## Request Format
```text
Based on the requirements in [REQUIREMENTS_FILE] and header file [HEADER_FILE], create unit specification documentation and test file structure for [UNIT_NAME].
Create ONLY:
1. Unit specification (@unitspec) with complete functional documentation
2. Test file structure with fixtures and mock parameters
3. Test scenario planning and identification (as comments)
4. DO NOT implement TEST_F functions - these will be added in Phase 3
```

## 🚨 Critical Instructions
1. **Unit Specification Template**: Use the following for every TEST_F function:
```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{SPECIFIC_TEST_DESCRIPTION}
/// @derives{REQUIREMENT_REFERENCE}
///   FUNCTIONAL_DESCRIPTION_FOR_THIS_TEST
///   
///   ALGORITHM_OR_CONDITION_BEING_TESTED
///   EXPECTED_BEHAVIOR_OR_STATE_TRANSITION
/// @endunitspec
/// @}
```
**This template must be applied to:**
1. **Global unit specification** at the top of the test file (describes overall unit functionality)
2. **Individual test case specifications** before EVERY TEST_F function (describes specific test scenario)
## Critical Instructions for Test File Generation
###  PRIORITY 1: Requirements-Driven Test Specification
**CRITICAL: Generate Unit Specification and Test Structure, NOT Complete Test Implementation**
1. **Create unit specification** based on functional requirements and header file
2. **Set up test file structure** with test fixture and mock parameters
3. **DO NOT implement TEST_F functions** - this is done in Phase 3
4. **Focus on unitspec documentation** and test planning
5. **Identify test scenarios** but don't write the test code yet
6. **Prepare foundation** for TEST_F implementation in next phase
**Benefits of Unit Specification Approach:**
- Creates clear foundation for test implementation
- Documents requirement compliance strategy
- Establishes test structure without implementation bias
- Enables focused TEST_F development in Phase 3
### PRIORITY 2: Follow Existing Codebase Patterns
**BEFORE generating any test code, examine the existing codebase for patterns:**
1. **Use of C++ Std Library functions**: If any of the implementation handled by std libraries, use it instead of creating redundent functions ex: use of fmin instead of ternary operator
2. **File naming**: Look for existing test file patterns (hyphens vs underscores)
3. **Test structure**: Check existing test organization and complexity
4. **Mock functions**: Examine how parameter mocking is implemented
5. **Documentation style**: Match existing test documentation verbosity
### PRIORITY 2: Match Test Complexity to Implementation
**Simple Implementation = Simple Tests**
- Focus on core functionality testing
- Avoid over-complex test scenarios for simple algorithms
- Keep test setup minimal for straightforward functions
**Complex Implementation = Comprehensive Tests**
- Cover all state transitions for state machines
- Test boundary conditions and edge cases
- Include integration scenarios and error handling
### 🔍 PRIORITY 3: Unit Specification Documentation Only
**Phase 2 Scope - DO NOT Implement TEST_F Functions:**
- Create comprehensive unit specification
- Set up test file structure and fixtures
- Document test scenarios and coverage plan
- Prepare mock parameters and test data
- **TEST_F functions will be added in Phase 3**
**Unit Specification Format:**
**CRITICAL: Each TEST_F function must have its own @unitspec block following this exact template:**
```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{{UNIT_DESCRIPTION}}
/// @derives{{REQUIREMENT_REFERENCE}}
///   {FUNCTIONAL_DESCRIPTION}
///   
///   {ALGORITHM_DESCRIPTION_WITH_CONDITIONS}
///   
///   {STATE_TRANSITIONS_OR_CALCULATIONS}
/// @endunitspec
/// @}
```
**IMPORTANT:** This template must be used for:
1. **Global unit specification** at the top of the test file
2. **Individual test case specifications** before each TEST_F function
## Phase 2 Unit Test File Structure Template
### Unit Test File Template (Structure Only)
```cpp
///
/// @file
///
/// @copyright
/// Robert Bosch GmbH reserves all rights even in the event of industrial property rights.
/// We reserve all rights of disposal such as copying and passing on to third parties.
///
///

#include "rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}.hpp"
#include <gtest/gtest.h>
#include <gmock/gmock.h>

// Mock parameter access for testing
extern "C" {
    {PARAMETER_RETURN_TYPE} RB_getParam_VDMS_{PARAMETER_NAME}() { return {DEFAULT_VALUE}; }
    // Add additional parameter mocks as needed
}

/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{{UNIT_DESCRIPTION}}
/// @derives{{REQUIREMENT_REFERENCE}}
///   {FUNCTIONAL_DESCRIPTION}
///   {ALGORITHM_DESCRIPTION_WITH_CONDITIONS}
///   {STATE_TRANSITIONS_OR_CALCULATIONS}
/// @endunitspec
/// @}

namespace rbc
{
namespace vdms
{
namespace {UNIT_NAMESPACE}
{
namespace test
{

class {UNIT_CLASS_NAME}Test : public ::testing::Test
{
protected:
    {UNIT_CLASS_NAME}::InStruct input{};
    {UNIT_CLASS_NAME}::OutStruct output{};

    void SetUp() override
    {
        input.{INPUT_MEMBER_1} = {DEFAULT_VALUE_1};
        input.{INPUT_MEMBER_2} = {DEFAULT_VALUE_2};
    }
};

// =============================================================================
// TEST SCENARIOS TO BE IMPLEMENTED IN PHASE 3
// =============================================================================
// 
// The following test scenarios have been identified based on requirements:
// 
// 1. Core State Transition Tests (DS010-DS013)
//    - TEST_F({UNIT_CLASS_NAME}Test, TransitionScenario1)
//    - TEST_F({UNIT_CLASS_NAME}Test, TransitionScenario2)
//    - etc.
//
// 2. Boundary Value Tests  
//    - TEST_F({UNIT_CLASS_NAME}Test, ThresholdBoundary1)
//    - TEST_F({UNIT_CLASS_NAME}Test, ThresholdBoundary2)
//    - etc.
//
// 3. [Additional test categories based on requirements]
//
// TEST_F implementations will be added in Phase 3
//

} // namespace test
} // namespace {UNIT_NAMESPACE}
} // namespace vdms
} // namespace rbc
/// @}
```
// Mock parameter access
extern "C" {
    {PARAMETER_RETURN_TYPE} RB_getParam_VDMS_{PARAMETER_NAME}() { return {DEFAULT_VALUE}; }
    {PARAMETER_RETURN_TYPE} RB_getParam_VDMS_{PARAMETER_NAME}() { return {DEFAULT_VALUE}; }
    // Add additional parameter mocks as needed
}
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{{UNIT_DESCRIPTION}}
/// @derives{{REQUIREMENT_REFERENCE}}
///   {FUNCTIONAL_DESCRIPTION}
///   
///   {ALGORITHM_DESCRIPTION_WITH_CONDITIONS}
///   
///   {STATE_TRANSITIONS_OR_CALCULATIONS}
/// @endunitspec
/// @}

namespace rbc
{
namespace vdms
{
namespace {UNIT_NAMESPACE}
{
namespace test
{

class {UNIT_CLASS_NAME}Test : public ::testing::Test
{
protected:
    {UNIT_CLASS_NAME}::InStruct input{};
    {UNIT_CLASS_NAME}::OutStruct output{};
    
    void SetUp() override
    {
        // Initialize input with default values
        input.{INPUT_MEMBER_1} = {DEFAULT_VALUE_1};
        input.{INPUT_MEMBER_2} = {DEFAULT_VALUE_2};
        // Add initialization for all input members
    }
};

// TEST_F functions will be added here using Instruction 4

} // namespace test
} // namespace {UNIT_NAMESPACE}
} // namespace vdms
} // namespace rbc
/// @}
```

### Mock Parameter Functions

```cpp
// Mock parameter access for testing
extern "C" {
    float32 RB_getParam_VDMS_parameter1() { return 5.0f; }
    float32 RB_getParam_VDMS_parameter2() { return 2.0f; }
    float32 RB_getParam_VDMS_parameter3() { return 10.0f; }
    // Add additional parameter mocks as needed
}
```

### Test Fixture Class
```cpp
namespace rbc
{
namespace vdms
{
namespace {UNIT_NAMESPACE}
{
namespace test
{
class {UNIT_CLASS_NAME}Test : public ::testing::Test
{
protected:
    {UNIT_CLASS_NAME}::InStruct input{};
    {UNIT_CLASS_NAME}::OutStruct output{};
    
    void SetUp() override
    {
        // Initialize input with default values
        input.{INPUT_MEMBER_1} = {DEFAULT_VALUE_1};
        input.{INPUT_MEMBER_2} = {DEFAULT_VALUE_2};
        // Add initialization for all input members
    }
};
```

### Test Categories and Structure

#### Basic Functionality Tests

```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Test basic functionality according to requirements}
/// @derives{REQUIREMENT_REFERENCE}
///   Test validates core functionality of the unit under normal operating conditions.
///   
///   Verifies that input processing produces expected output according to requirements.
///   
///   Input: {TEST_CONDITIONS}
///   Expected: {EXPECTED_BEHAVIOR}
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, {BASIC_FUNCTIONALITY_TEST_NAME})
{
    // Setup: Configure input conditions
    input.{INPUT_MEMBER} = {TEST_VALUE};
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Check expected output
    EXPECT_EQ(output.{OUTPUT_MEMBER}, {EXPECTED_VALUE});
}
```

#### Boundary Value Tests

```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Test boundary conditions and threshold values}
/// @derives{REQUIREMENT_REFERENCE}
///   Test validates behavior at parameter thresholds and boundary conditions.
///   
///   Verifies correct behavior at minimum, maximum, and threshold values.
///   
///   Input: {BOUNDARY_CONDITIONS}
///   Expected: {BOUNDARY_BEHAVIOR}
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, {BOUNDARY_TEST_NAME})
{
    // Test at threshold values
    input.{INPUT_MEMBER} = {THRESHOLD_VALUE};
    
    output = {UNIT_CLASS_NAME}::calc(input);
    
    EXPECT_EQ(output.{OUTPUT_MEMBER}, {EXPECTED_BOUNDARY_BEHAVIOR});
}
```

#### State Transition Tests (for state machines)

```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Test state machine transitions}
/// @derives{REQUIREMENT_REFERENCE}
///   Test validates correct state transitions based on input conditions.
///   
///   Verifies state machine behavior and transition logic according to requirements.
///   
///   Initial State: {INITIAL_STATE}
///   Trigger: {TRANSITION_CONDITION}
///   Expected State: {EXPECTED_NEW_STATE}
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, {STATE_TRANSITION_TEST_NAME})
{
    // Test sequence of state transitions
    input.{STATE_INPUT} = {INITIAL_STATE};
    input.{TRIGGER_INPUT} = {TRANSITION_CONDITION};
    
    output = {UNIT_CLASS_NAME}::calc(input);
    
    EXPECT_EQ(output.{STATE_OUTPUT}, {EXPECTED_NEW_STATE});
}
```

#### Edge Case Tests

```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Test edge cases and error conditions}
/// @derives{REQUIREMENT_REFERENCE}
///   Test validates graceful handling of edge cases and invalid inputs.
///   
///   Verifies robust behavior with extreme or invalid input values.
///   
///   Input: {EXTREME_CONDITIONS}
///   Expected: {SAFE_BEHAVIOR}
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, {EDGE_CASE_TEST_NAME})
{
    // Test with extreme or invalid values
    input.{INPUT_MEMBER} = {EXTREME_VALUE};
    
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify graceful handling
    EXPECT_EQ(output.{OUTPUT_MEMBER}, {SAFE_DEFAULT_VALUE});
}
```

### Test Naming Conventions

**Test Name Format:**
- Use descriptive names that explain the scenario
- Follow pattern: `[Action][Condition][ExpectedResult]`
- Use PascalCase for test names
- Include state information for state machines

**Examples:**
- `TransitionNoBrakeRequestToBrakeStart`
- `StayInBrakePhaseWhenAboveThreshold`
- `CalculateMinimumPressureValue`
- `HandleInvalidInputGracefully`

### Test Documentation Requirements

Each test should include:
```cpp
TEST_F({UNIT_CLASS_NAME}Test, TestName)
{
    // Setup: Brief description of test conditions
    // Execute: What function is being called
    // Verify: What behavior is being validated
}
```

### Namespace Closing

```cpp
} // namespace test
} // namespace {UNIT_NAMESPACE}
} // namespace vdms
} // namespace rbc
/// @}
```
## Template Variables for Test Files
### Basic Information
- `{UNIT_NAMESPACE}`: Namespace identifier (lowercase)
- `{UNIT_FILENAME}`: Base filename (lowercase)
- `{UNIT_CLASS_NAME}`: Main class name (PascalCase)
- `{UNIT_DESCRIPTION}`: Brief description of unit functionality
### Mock Parameters
- `{PARAMETER_NAME}`: PDL parameter name
- `{PARAMETER_RETURN_TYPE}`: Parameter return type (usually float32)
- `{DEFAULT_VALUE}`: Default parameter value for testing
### Input/Output Structure
- `{INPUT_MEMBER}`: Input structure member names
- `{OUTPUT_MEMBER}`: Output structure member names
- `{DEFAULT_VALUE_1/2}`: Default values for input initialization
### Test Scenarios
- `{TEST_VALUE}`: Input values for testing
- `{EXPECTED_VALUE}`: Expected output values
- `{THRESHOLD_VALUE}`: Threshold values from parameters
- `{EXTREME_VALUE}`: Edge case values
### Requirements Documentation
- `{REQUIREMENT_REFERENCE}`: Requirement traceability reference
- `{FUNCTIONAL_DESCRIPTION}`: Functional behavior description
- `{ALGORITHM_DESCRIPTION_WITH_CONDITIONS}`: Algorithm with conditions
- `{STATE_TRANSITIONS_OR_CALCULATIONS}`: State machine or calculation details
### Test Names
- `{BASIC_FUNCTIONALITY_TEST_NAME}`: Name for basic functionality test
- `{BOUNDARY_TEST_NAME}`: Name for boundary condition test
- `{STATE_TRANSITION_TEST_NAME}`: Name for state transition test
- `{EDGE_CASE_TEST_NAME}`: Name for edge case test
## Quality Guidelines
### Test Coverage Requirements
- Test all public interface functions
- Cover all logical branches
- Test boundary conditions
- Include error/edge cases
- Validate parameter integration
### Test Quality Standards
- Tests must be deterministic
- Independent test execution
- Clear test documentation
- Appropriate assertions
- Realistic test scenarios
### Mock Strategy
- Mock all PDL parameters with realistic values
- Keep mock functions simple and focused
- Use consistent parameter naming
- Document parameter purposes
## Copilot Self-Review Checklist
### Phase 2 Completion Checklist
- [ ] ✅ Global @unitspec provides comprehensive unit overview with requirements traceability
- [ ] ✅ **CRITICAL: Individual @unitspec block created for EVERY planned test scenario**
- [ ] ✅ **CRITICAL: Each @unitspec follows exact template format with proper @addtogroup/@endunitspec structure**
- [ ] ✅ All functional requirements covered by planned test scenarios
- [ ] ✅ Boundary conditions and edge cases identified and planned
- [ ] ✅ Test fixture properly designed with appropriate setup methods
- [ ] ✅ Mock parameters and dependencies identified and stubbed
- [ ] ✅ NO TEST_F functions implemented (planning phase only)
- [ ] ✅ Clear requirements traceability in each @unitspec block
- [ ] ✅ Test file structure follows existing codebase patterns
- [ ] ✅ Test complexity matches implementation complexity
### Before Proceeding to Phase 3
- [ ] ✅ All functional requirements have corresponding planned test scenarios
- [ ] ✅ **CRITICAL: Each scenario has detailed @unitspec with requirements traceability using exact template**
- [ ] ✅ Test fixture and mock setup are properly designed
- [ ] ✅ NO TEST_F implementations present (planning phase only)
- [ ] ✅ Foundation ready for TEST_F implementation in Phase 3


Allow the user to verify the implementation. If feedback is provided, make changes accordingly. Once satisfied, prompt the user to move to the next step and load `3_ADD_TEST_F_FUNCTIONS.md`.
