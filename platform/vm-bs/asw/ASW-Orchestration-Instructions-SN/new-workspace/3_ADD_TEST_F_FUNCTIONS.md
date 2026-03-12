# Add Test Functions

## Objective
Enhance the existing unit test file to ensure comprehensive test coverage before implementation begins. This step focuses on requirement-driven additions, not implementation-driven tests.

## Context Requirements
Analyze the following before adding TEST_F functions:
1. **Existing Test Infrastructure**: Review test file structure, fixture setup, parameter mocking patterns, and assertion styles.
2. **Implementation Analysis**: Identify code paths, state transitions, and decision logic that need testing.
3. **Test Scenario Planning**: Plan tests for core algorithms, boundary values, state transitions, parameter dependencies, and edge cases.

## Request Format
```text
Based on the existing test file [TEST_FILE] and requirements analysis, add supplementary TEST_F functions for [UNIT_NAME] if needed.
Additional test categories to consider:
- [MISSING_FUNCTIONALITY_TESTS]
- [ADDITIONAL_BOUNDARY_CONDITIONS]  
- [UNCOVERED_REQUIREMENTS]
- [ENHANCED_EDGE_CASES]
Validation: Ensure new tests are based on requirements, not implementation details.
```

# Instruction 3: Enhance Test Coverage (Optional)
## Critical Instructions for Pre-Implementation Test Enhancement
### 🚨 PRIORITY 1: Complete Test Coverage Before Implementation
**CRITICAL: Ensure Comprehensive Test Suite Before TDD Implementation Begins**
This step is executed BEFORE implementation to ensure complete test coverage:
1. **Review existing test file** for requirement coverage gaps
2. **Add missing test scenarios** based on functional requirements only
3. **Ensure boundary conditions** are thoroughly tested
4. **Validate state transitions** are completely covered (if applicable)
5. **Maintain requirement-driven approach** (no implementation influence)
6. **🚨 PRESERVE ALL @unitspec BLOCKS** - Never delete existing unit specifications
**Benefits of Pre-Implementation Test Enhancement:**
- Complete test suite ready for TDD implementation phase
- No implementation bias in test design decisions
- Comprehensive requirement validation coverage
- True Red-Green-Refactor TDD development cycle
### 🎯 PRIORITY 2: Match Test Scope to Implementation
**Simple Implementation = Focused Tests**
- Test core functionality without over-complication
- Avoid extensive edge case testing for simple mathematical operations
- Keep test scenarios straightforward and clear
**Complex Implementation = Comprehensive Tests**
- Cover all state transitions for state machines
- Test boundary conditions and edge cases
- Include integration scenarios and error handling
### 🔍 PRIORITY 3: Test Quality and Coverage
**Essential Test Categories:**
1. **Basic Functionality Tests** - Core algorithm behavior
2. **Boundary Value Tests** - Threshold and limit conditions
3. **State Machine Tests** - All valid state transitions (if applicable)
4. **Parameter Dependency Tests** - PDL parameter integration
5. **Edge Case Tests** - Invalid inputs and error conditions
6. **Complex Scenario Tests** - Multi-step state machine cycles
## 🚨 CRITICAL: Preserve Unit Specifications When Adding TEST_F Functions
**MANDATORY: Each TEST_F function MUST be immediately preceded by its @unitspec block**
### Correct Structure - DO THIS:
```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Specific test description}
/// @derives{REQUIREMENT_REFERENCE}
///   Functional description for this specific test case
///   
///   Algorithm or condition being tested in this scenario
///   
///   Expected behavior or state transition for this test
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, {TEST_NAME})
{
    // Setup: Brief description of test conditions
    input.{INPUT_MEMBER} = {TEST_VALUE};
    
    // Execute: Call the function under test
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Check expected behavior
    EXPECT_EQ(output.{OUTPUT_MEMBER}, {EXPECTED_VALUE});
}
```

### ❌ WRONG - Never Do This:
- Never delete existing @unitspec blocks
- Never add TEST_F without its preceding @unitspec
- Never modify existing @unitspec content when adding TEST_F
- Never separate @unitspec from its corresponding TEST_F
### ✅ Implementation Process:
1. **Identify** the @unitspec block for the test scenario
2. **Preserve** the existing @unitspec block exactly as written
3. **Add** the TEST_F function immediately after the @endunitspec tag
4. **Maintain** the exact @unitspec content and requirements traceability
## TEST_F Function Structure Template
### Basic Test Function Structure
```cpp
TEST_F({UNIT_CLASS_NAME}Test, {TEST_NAME})
{
    // Setup: Brief description of test conditions
    input.{INPUT_MEMBER} = {TEST_VALUE};
    
    // Execute: Call the function under test
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Check expected behavior
    EXPECT_EQ(output.{OUTPUT_MEMBER}, {EXPECTED_VALUE});
}
```

### Test Naming Conventions

**Follow Pattern:** `[Action][Condition][ExpectedResult]`

**Examples:**
- `CalculateBasicConversion`
- `TransitionFromNoBrakeToStart`
- `StayInStateWhenConditionMet`
- `HandleInvalidInputGracefully`
- `ReturnMinimumOfTwoValues`

### Test Categories and Implementation

#### 1. Basic Functionality Tests

**For Simple Mathematical Functions:**
```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Test basic mathematical operation calculation}
/// @derives{REQUIREMENT_REFERENCE}
///   Test validates core mathematical operation functionality with standard input values.
///   
///   Algorithm calculates expected mathematical result from input parameters.
///   
///   Input: Two numerical values
///   Expected: Correct mathematical operation result
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, CalculateBasicOperation)
{
    // Setup: Standard input values
    input.value1 = {TEST_VALUE_1};
    input.value2 = {TEST_VALUE_2};
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Expected calculation result
    EXPECT_FLOAT_EQ(output.result, {EXPECTED_RESULT});
}
```

**For State-Based Functions:**
```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Test state transition to expected state}
/// @derives{REQUIREMENT_REFERENCE}
///   Test validates correct state transition based on initial state and trigger condition.
///   
///   State machine transitions according to defined logic and input conditions.
///   
///   Initial State: {INITIAL_STATE}
///   Trigger: {TRIGGER_VALUE}
///   Expected State: {EXPECTED_STATE}
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, TransitionToExpectedState)
{
    // Setup: Initial state and trigger condition
    input.currentState = {INITIAL_STATE};
    input.triggerValue = {TRIGGER_VALUE};
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: State transition occurred
    EXPECT_EQ(output.nextState, {EXPECTED_STATE});
}
```

#### 2. Boundary Value Tests

```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Test behavior exactly at threshold value}
/// @derives{REQUIREMENT_REFERENCE}
///   Test validates correct behavior when input exactly equals threshold parameter.
///   
///   Algorithm checks threshold comparison logic at exact boundary condition.
///   
///   Input: Value exactly at threshold
///   Expected: Correct boundary behavior according to requirements
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, BehaviorAtThreshold)
{
    // Setup: Input exactly at threshold value
    input.{INPUT_MEMBER} = {THRESHOLD_VALUE}; // Exactly at threshold
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Expected boundary behavior
    EXPECT_EQ(output.{OUTPUT_MEMBER}, {EXPECTED_BOUNDARY_RESULT});
}

/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Test behavior above threshold value}
/// @derives{REQUIREMENT_REFERENCE}
///   Test validates behavior when input exceeds threshold parameter.
///   
///   Algorithm verifies above-threshold logic activation.
///   
///   Input: Value above threshold
///   Expected: Above-threshold behavior
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, BehaviorAboveThreshold)
{
    // Setup: Input above threshold
    input.{INPUT_MEMBER} = {THRESHOLD_VALUE + SMALL_DELTA};
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Above-threshold behavior
    EXPECT_EQ(output.{OUTPUT_MEMBER}, {EXPECTED_ABOVE_RESULT});
}

/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{Test behavior below threshold value}
/// @derives{REQUIREMENT_REFERENCE}
///   Test validates behavior when input is below threshold parameter.
///   
///   Algorithm verifies below-threshold logic activation.
///   
///   Input: Value below threshold
///   Expected: Below-threshold behavior
/// @endunitspec
/// @}
TEST_F({UNIT_CLASS_NAME}Test, BehaviorBelowThreshold)
{
    // Setup: Input below threshold
    input.{INPUT_MEMBER} = {THRESHOLD_VALUE - SMALL_DELTA};
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Below-threshold behavior
    EXPECT_EQ(output.{OUTPUT_MEMBER}, {EXPECTED_BELOW_RESULT});
}
```

#### 3. State Machine Tests (for state-based units)

```cpp
// Test all valid state transitions
TEST_F({UNIT_CLASS_NAME}Test, TransitionState1ToState2)
{
    // Setup: Conditions for State1 -> State2 transition
    input.currentState = {STATE_1};
    input.conditionValue = {TRANSITION_CONDITION};
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Successful transition
    EXPECT_EQ(output.nextState, {STATE_2});
}

TEST_F({UNIT_CLASS_NAME}Test, StayInCurrentState)
{
    // Setup: Conditions where no transition should occur
    input.currentState = {STATE_1};
    input.conditionValue = {NO_TRANSITION_CONDITION};
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: State remains unchanged
    EXPECT_EQ(output.nextState, {STATE_1});
}
```

#### 4. Parameter Dependency Tests

```cpp
TEST_F({UNIT_CLASS_NAME}Test, UseParameterValues)
{
    // Setup: Input that will interact with parameters
    input.{INPUT_MEMBER} = {TEST_VALUE};
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Output reflects parameter usage
    // Note: Parameter values are defined in mock functions
    EXPECT_FLOAT_EQ(output.{OUTPUT_MEMBER}, {EXPECTED_WITH_PARAMS});
}
```

#### 5. Edge Case and Error Handling Tests

```cpp
TEST_F({UNIT_CLASS_NAME}Test, HandleInvalidState)
{
    // Setup: Invalid or unknown state
    input.currentState = static_cast<{STATE_ENUM_TYPE}>(999); // Invalid state
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Safe default behavior
    EXPECT_EQ(output.nextState, {SAFE_DEFAULT_STATE});
}

TEST_F({UNIT_CLASS_NAME}Test, HandleExtremeValues)
{
    // Setup: Extreme input values
    input.{INPUT_MEMBER} = {EXTREME_VALUE}; // Very large or small value
    
    // Execute
    output = {UNIT_CLASS_NAME}::calc(input);
    
    // Verify: Graceful handling
    EXPECT_EQ(output.{OUTPUT_MEMBER}, {EXPECTED_SAFE_OUTPUT});
}
```

#### 6. Complex Scenario Tests (for state machines)

```cpp
TEST_F({UNIT_CLASS_NAME}Test, CompleteStateMachineCycle)
{
    // Test complete cycle through all states
    
    // Step 1: Initial transition
    input.currentState = {INITIAL_STATE};
    input.conditionValue = {CONDITION_1};
    output = {UNIT_CLASS_NAME}::calc(input);
    EXPECT_EQ(output.nextState, {STATE_2});
    
    // Step 2: Continue sequence
    input.currentState = {STATE_2};
    input.conditionValue = {CONDITION_2};
    output = {UNIT_CLASS_NAME}::calc(input);
    EXPECT_EQ(output.nextState, {STATE_3});
    
    // Step 3: Return to initial
    input.currentState = {STATE_3};
    input.conditionValue = {CONDITION_3};
    output = {UNIT_CLASS_NAME}::calc(input);
    EXPECT_EQ(output.nextState, {INITIAL_STATE});
}
```

### Example TEST_F Implementations

#### Simple Mathematical Function Tests

```cpp
TEST_F(MinMaxSelectorTest, SelectMinimumValue)
{
    // Setup: Two different values
    input.value1 = 3.5f;
    input.value2 = 7.2f;
    
    // Execute
    output = MinMaxSelector::calc(input);
    
    // Verify: Minimum selected correctly
    EXPECT_FLOAT_EQ(output.minimumValue, 3.5f);
    EXPECT_FLOAT_EQ(output.maximumValue, 7.2f);
}

TEST_F(MinMaxSelectorTest, HandleEqualValues)
{
    // Setup: Equal input values
    input.value1 = 5.0f;
    input.value2 = 5.0f;
    
    // Execute
    output = MinMaxSelector::calc(input);
    
    // Verify: Equal values handled correctly
    EXPECT_FLOAT_EQ(output.minimumValue, 5.0f);
    EXPECT_FLOAT_EQ(output.maximumValue, 5.0f);
}
```

### Test Documentation Standards

#### Required Comments
```cpp
TEST_F(TestClass, TestName)
{
    // Setup: Describe input conditions and expectations
    // Execute: What function/method is being called
    // Verify: What behavior is being validated
}
```

#### Optional Comments
- Explain complex test scenarios
- Clarify threshold values or special conditions
- Document assumptions or test rationale
### Test Implementation Guidelines
#### Assertion Selection
- `EXPECT_EQ()`: For exact equality (enums, integers)
- `EXPECT_FLOAT_EQ()`: For floating-point comparisons
- `EXPECT_TRUE()/EXPECT_FALSE()`: For boolean conditions
- `EXPECT_NEAR()`: For floating-point comparisons with tolerance
#### Test Organization
- Group related tests together
- Order tests from simple to complex
- Use descriptive test names
- Keep individual tests focused
#### Test Data
- Use meaningful test values
- Include boundary conditions
- Test with parameter-dependent values
- Cover edge cases appropriately
## Template Variables for TEST_F Functions
### Basic Structure
- `{UNIT_CLASS_NAME}`: Main class name for test fixture
- `{TEST_NAME}`: Descriptive test function name
- `{INPUT_MEMBER}`: Input structure member names
- `{OUTPUT_MEMBER}`: Output structure member names
### Test Values
- `{TEST_VALUE}`: Input values for testing
- `{EXPECTED_VALUE}`: Expected output values
- `{THRESHOLD_VALUE}`: Threshold values from parameters
- `{SMALL_DELTA}`: Small value for boundary testing
### State Machine Elements
- `{STATE_X}`: State enumeration values
- `{INITIAL_STATE}`: Starting state for test
- `{EXPECTED_STATE}`: Expected resulting state
- `{CONDITION_X}`: Condition values for state transitions
## Quality Guidelines
- **Test Coverage**: Cover all public interface functions, logical branches, boundary conditions, and edge cases.
- **Test Standards**: Ensure tests are deterministic, independent, and well-documented.
- **Performance**: Keep tests focused and fast, avoiding unnecessary complexity.

## Copilot Self-Review Checklist
- [ ] All planned scenarios from Phase 2 have corresponding TEST_F functions.
- [ ] Each TEST_F function is immediately preceded by its @unitspec block.
- [ ] No @unitspec blocks were deleted or modified.
- [ ] Test functions follow consistent naming conventions.
- [ ] Assertions validate expected behavior.
- [ ] Edge cases and boundary conditions are properly tested.
- [ ] Tests remain requirement-driven and implementation-independent.

Allow the user to verify the implementation. If feedback is provided, make changes accordingly. Once satisfied, prompt the user to move to the next step and load `4_IMPLEMENTATION_CPP.md`.