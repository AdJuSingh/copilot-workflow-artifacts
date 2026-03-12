
# Instructions for Unit Test File Creation From Scratch

**Pre-requisite**: Prompt user to input source files for test generation. Wait for user input before proceeding.

# Workflow
Generate comprehensive unit test files from scratch for existing source files. Analyze .hpp and .cpp files to create a completely new test file with thorough coverage. Do not run Unit tests since it will be taken care in the next step

**IMPORTANT**: Create NEW test files only - do NOT modify existing source or test files.

### C++11 Compatibility Requirements
**CRITICAL**: This project uses C++11 standard.

#### C++11 Do's:
- Use `unique_ptr.reset(new ClassName())` instead of `std::make_unique<ClassName>()`

#### C++11 Don'ts:
- **NEVER** use `std::make_unique` (C++14+)
- **NEVER** use `std::make_shared` with direct initialization
- **AVOID** auto return types without trailing return type
- **AVOID** variable template syntax or structured bindings (C++17+)

#### Platform Type Safety Requirements:
**MANDATORY**: Use platform types, never standard types

✅ **CORRECT:**                    ❌ **WRONG:**
- `float32`                       - `float`
- `boolean`                       - `bool`  
- `uint8, uint16, uint32`         - `unsigned int`
- `sint8, sint16, sint32`         - `int`

**Literal Suffixes:**
- `float32 value{1.0F};`          // F suffix mandatory
- `uint32 count{100U};`           // U suffix for unsigned
- `const boolean flag{true};`     // No suffix for boolean

#### Integer Overflow Prevention:
- Use explicit type suffixes: `1000U` for uint16, `1000UL` for uint32
- Use `static_cast<target_type>()` for safe conversions
- Check MAX_COUNTER_VALUE definitions for appropriate test values 


## Core Principles
- Analyze source files thoroughly before generating tests
- Create NEW test files only - never modify existing source or test files
- Generate complete test file structure with proper includes and setup
- Follow project naming conventions and patterns

## Unit Test File Creation Workflow
1) **Source Code Analysis**: Analyze .hpp/.cpp files for interfaces, logic, algorithms, and edge cases
2) **Requirements Analysis**: Extract functional requirements from documentation and comments
3) **MANDATORY: Logic Flow Analysis**: Trace through source code execution step by step
4) **Test Strategy Planning**: Determine test approach priority (TEST_P primary, TEST_F secondary)
5) **Test File Creation**: Create new test file with proper headers, includes, and boilerplate
6) **Parameter Table Design**: Plan comprehensive parameter combinations for TEST_P coverage
7) **Primary Test Implementation**: Generate TEST_P functions with parameter tables and markdown documentation
8) **Secondary Test Implementation**: Generate TEST_F functions with sequence loops where needed
9) **Test Execution Validation**: Run tests and verify all pass successfully

### Pre-Test Validation Process
**Before writing any test, validate understanding:**

1. **Manual Trace Examples**:
   - Walk through 2-3 example scenarios manually
   - Document expected state changes at each step
   - Verify understanding of conditional logic
   - Confirm parameter interaction effects

2. **Logic Flow Verification**:
   - Draw out state machine transitions
   - Map parameter influences on state
   - Identify potential edge cases
   - Confirm reset/trigger conditions

3. **Boundary Condition Identification**:
   - List all threshold comparisons
   - Note exact comparison operators used
   - Identify off-by-one potential errors
   - Plan boundary and boundary+1 test cases

### **Systematic Edge Case Analysis Framework**
**Before writing any test, complete this structured edge case analysis:**

1. **Boundary Values**:
   - Minimum/Maximum values for each parameter type
   - Zero values and negative values where applicable
   - Threshold values (exactly at threshold, threshold±1)

2. **Equivalence Classes**:
   - Valid input ranges (low, medium, high)
   - Invalid input ranges
   - Special states (uninitialized, error states)

3. **State Transitions**:
   - All possible state machine transitions
   - Concurrent state changes within single function call
   - State persistence across function calls

4. **Parameter Interactions**:
   - Parameter combinations that trigger different logic paths
   - Order of parameter evaluation
   - Parameter precedence rules

**CRITICAL**: See "Ensuring Test Success - Validation Strategy" section for complete pre-implementation checklist.

## Analysis Framework

### Mandatory Source Code Logic Analysis
**BEFORE writing any test, perform detailed logic flow analysis:**

1. **Line-by-Line Execution Flow**:
   - Trace through function execution step by step
   - Identify conditional branches and exact conditions
   - Note order of state modifications vs. condition checks
   - Map variable state changes throughout execution

2. **State Machine Analysis**:
   - Identify state variables and transitions
   - Document conditions that trigger state changes
   - Understand reset/clear conditions and timing
   - Note state persistence across function calls

3. **Parameter Interaction Analysis**:
   - How parameters affect internal state
   - Parameter evaluation timing in execution flow
   - Threshold comparisons and exact operators
   - Parameter dependencies and logical combinations

4. **Counter/Timer Logic Analysis**:
   - Increment/decrement timing and conditions
   - Overflow protection mechanisms
   - Reset conditions and precedence
   - Boundary value behavior (equal vs. greater than)

### Example Analysis Process:
```cpp
// For a function like:
if ((condition1) && (condition2)) {
    counter++; // Step 1: Increment
    if (resetFlag || (state && counter > threshold)) {
        state = false; // Step 2: Reset
    }
    if (counter > trigger) {
        state = true; // Step 3: Trigger
    }
}
```
**Analysis Notes:**
- Step 1 happens first (increment)
- Step 2 can reset state based on current counter value
- Step 3 can immediately re-trigger state in same call
- Tests must account for this execution order

### Analysis Framework:
1. **Code Analysis**: 
   - Public interfaces, parameters, return types
   - Core algorithms, business logic, state machines
   - **CRITICAL: Execution Order Analysis** - Understand exact operation sequence
   - **State Management** - Track internal state changes
   - **Boundary Conditions** - Identify threshold values and operators

2. **Test Strategy Planning**: 
   - Positive/negative scenarios and boundary conditions
   - State transitions and edge cases

3. **Pattern Analysis**: 
   - Existing test structure and naming conventions

4. **Unit Test Specification Template**: Use this template for comprehensive test documentation:
```cpp
/// @addtogroup rbc_tcs_{UNIT_NAMESPACE}
/// @{
/// @unitspec{SPECIFIC_TEST_DESCRIPTION}
/// @derives{REQUIREMENT_REFERENCE}
///   FUNCTIONAL_DESCRIPTION: Detailed description of what this test validates
///   - Bullet point format for multiple behaviors
///   - Clear, concise functional requirements
///   - Focus on WHAT the unit does, not HOW
/// @endunitspec
/// @}
```

### **Requirement ID Format Requirements:**
- **Use Real Requirement IDs**: Format `REQ_TCS_XXXXXX` where XXXXXX is 6-digit number
- **Multiple Requirements**: Comma-separated list for comprehensive coverage
- **Examples**: `REQ_TCS_044156, REQ_TCS_524796, REQ_TCS_908226`
- **NO Made-up IDs**: Never use placeholder or invented requirement references

### Common Test Failure Issues to Avoid:
1. Execution Order Misunderstanding
2. Parameter Relationship Misanalysis  
3. State Transition Validation Error
4. Logic Flow Validation Gap

## Ensuring Test Success - Validation Strategy

### **Pre-Implementation Validation (MANDATORY)**
**Before writing ANY test, complete these verification steps:**

#### **1. Source Code Logic Tracing**
- [ ] **Manual walkthrough**: Trace 3+ scenarios with concrete values
- [ ] **State tracking**: Document state changes at each execution step
- [ ] **Counter arithmetic**: Verify calculations with calculator
- [ ] **Boundary verification**: Test exact threshold values (>, >=, ==)
- [ ] **Parameter interaction**: Map how parameters affect execution flow

#### **2. Execution Order Verification**
- [ ] **Step sequence**: Understand increment → reset → trigger order
- [ ] **Same-call effects**: Identify when reset and trigger occur together
- [ ] **State persistence**: Verify state retention between function calls
- [ ] **Timing dependencies**: Map when conditions are evaluated

#### **3. Test Logic Validation**
- [ ] **Expected vs actual**: Compare manual trace results with test expectations
- [ ] **Edge case analysis**: Identify off-by-one and boundary conditions
- [ ] **Parameter combinations**: Test interaction between timeHandBag/timeHold
- [ ] **State machine paths**: Verify all state transitions are testable

### **Implementation Validation (During Test Writing)**

#### **4. Test Structure Verification**
- [ ] **Setup correctness**: Verify parameter initialization in SetUp()
- [ ] **Helper function accuracy**: Validate callMultipleTimes() logic
- [ ] **Assertion precision**: Use exact values, avoid ranges when possible
- [ ] **Test isolation**: Ensure tests don't depend on execution order

#### **5. Compilation and Runtime Checks**
- [ ] **Header paths verified**: All includes use correct workspace-relative paths
- [ ] **Type safety**: Use explicit type suffixes (U, UL) for constants
- [ ] **C++11 compliance**: No C++14+ features (std::make_unique, etc.)
- [ ] **Parameter stub usage**: Verify RB_setParam_* functions work correctly

### **Post-Implementation Validation (After Test Writing)**

#### **6. Test Execution Verification**
- [ ] **Compilation success**: All tests compile without errors/warnings
- [ ] **Individual test runs**: Each test passes in isolation
- [ ] **Test suite runs**: All tests pass when run together
- [ ] **Parameter reset verification**: Tests don't interfere with each other

#### **7. Test Quality Assessment**
- [ ] **Coverage completeness**: All public methods tested
- [ ] **Boundary coverage**: Edge cases and thresholds tested
- [ ] **State machine coverage**: All transitions validated
- [ ] **Error path coverage**: Invalid inputs and error conditions tested



## Ensuring Test Success - Validation Strategy

### **Pre-Implementation Validation (MANDATORY)**
**Before writing ANY test, complete these verification steps:**

#### **1. Source Code Logic Tracing**
- [ ] **Manual walkthrough**: Trace 3+ scenarios with concrete values
- [ ] **State tracking**: Document state changes at each execution step
- [ ] **Counter arithmetic**: Verify calculations with calculator
- [ ] **Boundary verification**: Test exact threshold values (>, >=, ==)
- [ ] **Parameter interaction**: Map how parameters affect execution flow

#### **2. Execution Order Verification**
- [ ] **Step sequence**: Understand increment → reset → trigger order
- [ ] **Same-call effects**: Identify when reset and trigger occur together
- [ ] **State persistence**: Verify state retention between function calls
- [ ] **Timing dependencies**: Map when conditions are evaluated

#### **3. Test Logic Validation**
- [ ] **Expected vs actual**: Compare manual trace results with test expectations
- [ ] **Edge case analysis**: Identify off-by-one and boundary conditions
- [ ] **Parameter combinations**: Test interaction between timeHandBag/timeHold
- [ ] **State machine paths**: Verify all state transitions are testable

### **Implementation Validation (During Test Writing)**

#### **4. Test Structure Verification**
- [ ] **Setup correctness**: Verify parameter initialization in SetUp()
- [ ] **Helper function accuracy**: Validate callMultipleTimes() logic
- [ ] **Assertion precision**: Use exact values, avoid ranges when possible
- [ ] **Test isolation**: Ensure tests don't depend on execution order

#### **5. Compilation and Runtime Checks**
- [ ] **Header paths verified**: All includes use correct workspace-relative paths
- [ ] **Type safety**: Use explicit type suffixes (U, UL) for constants
- [ ] **C++11 compliance**: No C++14+ features (std::make_unique, etc.)
- [ ] **Parameter stub usage**: Verify RB_setParam_* functions work correctly

### **Enhanced Pre-Implementation Validation Checklist**
**MANDATORY: Complete this comprehensive validation before writing ANY test:**

**Source Analysis:**
- [ ] .hpp file analyzed for public interfaces, parameters, return types
- [ ] .cpp file analyzed for implementation logic, state machines
- [ ] All state transitions mapped and understood
- [ ] Parameter interaction effects documented
- [ ] Execution flow traced with concrete example values

**Test Strategy:**
- [ ] Test strategy planned (TEST_F vs TEST_P vs TEST)
- [ ] Edge cases identified using equivalence partitioning  
- [ ] Boundary conditions identified (>, >=, ==, <, <=)
- [ ] Expected behavior verified against source implementation
- [ ] Unit specifications drafted with requirement traceability

**Technical Compliance:**
- [ ] All include paths verified relative to test file location
- [ ] Platform types selected correctly (float32, boolean, etc.)
- [ ] ASSERT_* vs EXPECT_* decision made consciously
- [ ] C++11 compliance verified (no std::make_unique, etc.)
- [ ] Const correctness planned for test variables
- [ ] Brace initialization planned for all variables

### Unit Specification Requirements
A Unit Spec Must:
- **Describe Input/Output Behavior**: Focus on behavior, avoid copying code
- **Consider All Use Cases**: Cover different scenarios and edge cases
- **Use Independent Parameters**: From application point of view
- **Be Testable & Precise**: Clear, measurable expectations
- **Be Atomic**: Single, focused responsibility per specification
- **Keep Comment Lines**: 80-100 characters for readability

### **Test Documentation Requirements:**

#### **Markdown Parameter Tables (MANDATORY for TEST_P):**
Add comprehensive parameter documentation after each parameterized test:
```cpp
/// @brief Input Values for Test:
/// | input1  | input2  | expected |                Comments                    |
/// |:-------:|:-------:|:--------:|:------------------------------------------|
/// |  true   |  false  |   true   | FlipFlop is set                           |
/// |  false  |  true   |   false  | FlipFlop is reset                         |
/// |  false  |  false  |   false  | Both set and reset false, output holds   |
/// |  true   |  true   |   false  | Both set and reset true, reset wins      |
```

#### **Sequence Documentation (MANDATORY for loop tests):**
Add iteration explanation for sequence tests:
```cpp
/// @brief Additional information for loop iterations:
/// | input1  | input2  | expected |          Comments             |
/// |:-------:|:-------:|:--------:|:-----------------------------:|
/// |  false  |  false  |   false  | Initial state stays false     |
/// |  true   |  false  |   true   | Set flipflop state to true   |
/// |  false  |  false  |   true   | Keep flipflop state at true  |
```

### Unit Specification Writing Order
1. **Code Order**: Follow same sequence as source code
2. **Journalist Style**: Most important requirements first, details later
3. **Class Hierarchy**: Normal classes to special classes
4. **Complexity**: Simple cases to more complicated cases

## Best Practices

### Essential Guidelines
- **MISRA Compliance**: Follow MISRA guidelines
- **Pattern Consistency**: Match existing coding patterns and naming conventions
- **Comprehensive Coverage**: Test all public methods, edge cases, and error conditions
- **Test Isolation**: Ensure tests are independent
- **Clear Documentation**: Add detailed comments and proper @unitspec blocks
- **AI Code Tagging**: Use "//ContainsAIGeneratedcode" tag with timestamp

### Critical Don'ts
- Do NOT modify existing .hpp or .cpp source files
- Do NOT modify or append to existing test files
- Don't assume functionality - analyze thoroughly before creating new test file
- Don't leave test gaps or use magic numbers in new test file
- Avoid brittle tests coupled to implementation details
- Don't skip proper file headers and includes in new test file
- **DO NOT assume state transitions without source code analysis**
- **DO NOT use arithmetic assumptions for counter progressions**
- **DO NOT test expected behavior without understanding actual logic flow**
- **DO NOT ignore execution order in complex functions**

### Test Failure Prevention
**Common failure patterns to avoid:**

### **Key Pitfalls:**
❌ **Reset Expectations**: "External reset will leave failure = false"
✅ **Correct Understanding**: "Reset clears failure, but trigger logic can immediately reactivate it"

❌ **Arithmetic Errors**: `callMultipleTimes(timeHold - timeHandBag, ...)`
✅ **Correct Calculation**: Account for current counter position when calculating remaining calls

❌ **State Transition Timing**: "Reset happens after all other logic"
✅ **Correct Understanding**: "Reset happens between increment and trigger check"

### **Solutions:**
1. **Logic Flow**: Trace through source code line by line, map exact sequence of state changes
2. **Counter State**: Use actual return values, store and verify intermediate states
3. **Boundary Conditions**: Verify exact threshold conditions, test boundary value and boundary+1
4. **Reset Logic Timing**: Understand reset vs. trigger execution, account for immediate re-triggering
5. **Parameter Interaction**: Analyze evaluation order, test parameter combinations systematically

### Pre-Implementation Test Design Validation
For EVERY test involving reset or trigger logic:

- [ ] Manual trace with concrete values completed
- [ ] Counter arithmetic verified with calculator
- [ ] All three execution steps (increment → reset → trigger) considered
- [ ] Expected vs actual state documented for each step
- [ ] Edge case where reset and trigger both occur in same call analyzed
- [ ] Alternative test approach considered if expectations seem counterintuitive

### **Critical Test Anti-Patterns Prevention**
**Avoid these common failure patterns that lead to incorrect test implementations:**

1. **Execution Order Misunderstanding:**
   - ❌ Assuming reset happens after trigger logic
   - ✅ Trace actual source code execution sequence

2. **State Persistence Errors:**
   - ❌ Assuming state resets between function calls
   - ✅ Test actual state retention behavior

3. **Arithmetic Boundary Errors:**
   - ❌ Using threshold + 1 without understanding comparison operator  
   - ✅ Test exact threshold value and understand >, >=, ==

4. **Parameter Interaction Blindness:**
   - ❌ Testing parameters in isolation
   - ✅ Test parameter combinations that affect logic flow

5. **Magic Number Dependencies:**
   - ❌ Using hardcoded values without source verification
   - ✅ Use constants from source or calculate from requirements

6. **Assertion Type Confusion:**
   - ❌ Using EXPECT_* as default assertion type
   - ✅ Use ASSERT_* as default, EXPECT_* only for diagnostic value

7. **Type Safety Violations:**
   - ❌ Using standard types (float, bool, int)
   - ✅ Use platform types (float32, boolean, uint32, etc.)

## New Test File Structure Requirements

### Test File Naming Convention
- **Pattern**: `test_{source_filename}.cpp`
- **Example**: For `rbc_vdms_core.cpp` → create `test_rbc_vdms_core.cpp`

### Essential Test File Components
1. **File Header**: Copyright, description, and purpose
2. **Include Statements**: 
   - **CRITICAL**: All header file paths must be relative to workspace root - Fetch the exact .hpp, .h file path with respect to the relevant workspace and gie teh exact precise path in the header file loading part
   - Source headers: `"../../../src/rbc_vdms_[filename].hpp"` 
   - Constants: `"../../../src/rbc_vdms_constants.hpp"`
   - Parameters: `"rbc_vdms_parameters_pdl.h"` and `"rbc_vdms_parameters_pdl_stub.h"`
   - GTest framework: `"gtest/gtest.h"`
   - Standard libraries: `<array>` for sequence testing, others as needed
   - **Path Validation Required**: Verify each include path exists from test file location
3. **Test Fixture Classes**: SetUp() and TearDown() methods
4. **Unit Specifications**: Complete @unitspec documentation blocks
5. **Test Implementations**: All TEST, TEST_F, and TEST_P functions

### Test File Template Structure
```cpp
/**
 * @file test_{source_filename}.cpp
 * @brief Unit tests for {source_filename}.cpp
 * @copyright
 * Robert Bosch GmbH reserves all rights even in the event of industrial property rights.
 * We reserve all rights of disposal such as copying and passing on to third parties.
 * @author AI Generated - {timestamp}
 * @date {current_date}
 */

// ContainsGenAICopilot - This notice needs to remain attached to any reproduction of this file.

#include "gtest/gtest.h"
#include "../../../src/{source_header}.hpp" // MANDATORY: Full workspace-relative path
#include <array> // For sequence testing
#include "../../../src/rbc_vdms_constants.hpp" // If constants needed
#include "rbc_vdms_parameters_pdl.h" // If parameters needed
#include "rbc_vdms_parameters_pdl_stub.h" // If parameter stubs needed
// Additional includes as needed - ALL PATHS MUST BE WORKSPACE-RELATIVE

namespace rbc
{
namespace {component}  // e.g., vdms, tsc
{

/// @addtogroup rbc_{component}_{unit_name}
/// @{

// Test fixture classes - Follow project naming patterns:
// For parameterized tests: {FunctionName}FixParam
// For regular tests: {FunctionName}FixParam or {ClassName}Test
class {FunctionName}FixParam : public ::testing::TestWithParam<std::tuple<type1, type2, type3>>
{
};

// Alternative: Regular test fixture
class {FunctionName}FixParam : public ::testing::Test
{
protected:
    void SetUp() override {
        // Common setup code
    }

    void TearDown() override {
        // Common cleanup code
    }

    // Test helper methods and data members
};

// Refer to PRIMARY and SECONDARY patterns above for comprehensive test implementation

/// @}

} // namespace {component}
} // namespace rbc
```

### **HEADER PATH VALIDATION CHECKLIST:**
Before creating test file, verify:
- [ ] Source header path: `../../../src/[filename].hpp` exists from `tst/gtest/ut/` location
- [ ] Constants path: `../../../src/rbc_vdms_constants.hpp` exists if needed
- [ ] Parameter paths: `rbc_vdms_parameters_pdl.h` accessible from test location
- [ ] No redundant or non-existent header files included
- [ ] All paths are workspace-relative, not absolute system paths
```

## C++ Testing Guidelines
1) **C++11 Smart Pointer Usage**: Use `ptr.reset(new Class())` instead of `std::make_unique<Class>()`
2) **Integer Type Safety**: Use explicit type suffixes and avoid overflow in test calculations
3) **Source Logic Tracing**: Always trace execution flow before writing test expectations
4) **State Persistence Testing**: Test state retention across multiple function calls
5) **Const Correctness**: Validate const-correctness in function parameters
6) **Scope Analysis**: Understand variable scope and lifetime in source functions

### C++11 Smart Pointer Best Practices
```cpp
// CORRECT C++11 approach:
std::unique_ptr<HandbagDetector> detector;
detector.reset(new HandbagDetector()); // In SetUp()

// WRONG - C++14+ only:
// detector = std::make_unique<HandbagDetector>();
```

### Integer Overflow Prevention Examples
```cpp
// WRONG - causes overflow:
SetHandbagParameters(MAX_COUNTER_VALUE + 100, 50);

// CORRECT - explicit typing:
constexpr const uint16 largeTimeHandBag{1000U};
SetHandbagParameters(largeTimeHandBag, 50);
```

10) **Data Structure Choice**: Use `struct` for simple data collections (PODO), `class` for encapsulation and OOP patterns
11) **Constructor Implementation**: Initialize member variables and ensure valid object state



# Test Implementation Guidelines

## GTEST Framework & Coverage Requirements
- Use GTEST framework with @unitspec documentation for every test
- Requirements drive test specification and implementation
- **CRITICAL:** Each @unitspec follows template format with proper @addtogroup/@endunitspec structure

### **Test Method Structure Priority:**
**CRITICAL: Follow this priority order for test implementation:**

1. **PRIMARY - TEST_P with Parameter Tables**: Use for comprehensive coverage of input combinations
   - Covers all equivalence classes and boundary conditions systematically
   - Includes markdown parameter tables for documentation
   - Most efficient for embedded systems testing

2. **SECONDARY - TEST_F with Loops**: Use for state sequence testing
   - Tests state machine transitions over time
   - Validates state persistence and complex sequences
   - Uses arrays and loops with SCOPED_TRACE for debugging

3. **LAST RESORT - Individual TEST_F**: Use only for unique scenarios
   - Special cases that don't fit parameter or sequence patterns
   - Initialization tests, error handling, edge cases

### **When to Define Test Class:**
Define test class for stateful source code with persistent member variables.

### **Test Types:**
- **TEST_P**: Parameterized tests - PRIMARY choice for comprehensive coverage
- **TEST_F**: Shared setup/teardown for stateful classes and sequence testing
- **TEST**: Simple, self-contained tests for stateless functions - use sparingly

### **PRIMARY Pattern: Parameterized Tests with Parameter Tables**
Use this pattern as the PRIMARY approach for comprehensive coverage:

```cpp
class {FunctionName}FixParam : public ::testing::TestWithParam<std::tuple<type1, type2, type3>>
{
};

/// @unitspec{Function Comprehensive Testing}
/// @derives{REQ_TCS_044156, REQ_TCS_524796, REQ_TCS_908226} // Use REAL requirement IDs
/// Comprehensive description of what the function shall do based on inputs.
/// - Condition 1: Behavior description
/// - Condition 2: Behavior description  
/// - Condition 3: Behavior description
/// @endunitspec
TEST_P({FunctionName}FixParam, {FunctionName})
{
    /// @par Scope / Purpose / Design:
    /// Check if the function returns correct output based on input combinations.

    // GIVEN
    // Input values
    {ClassName} unit;
    const type1 input1{std::get<0>(GetParam())};
    const type2 input2{std::get<1>(GetParam())};

    // Expected output values
    const type3 expectedValue{std::get<2>(GetParam())};

    // WHEN
    const type3 result{unit.method(input1, input2)};

    // THEN
    ASSERT_EQ(result, expectedValue);
}
/// @brief Input Values for Test:
/// | input1  | input2  | expected |                Comments                    |
/// |:-------:|:-------:|:--------:|:------------------------------------------|
/// |  true   |  false  |   true   | Description of test case                  |
/// |  false  |  true   |   false  | Description of test case                  |
/// |  false  |  false  |   false  | Both inputs false, maintains state       |
/// |  true   |  true   |   false  | Both inputs true, reset takes priority   |
INSTANTIATE_TEST_SUITE_P({TestSuiteName},
                         {FunctionName}FixParam,
                         ::testing::Values(std::make_tuple(true, false, true),
                                           std::make_tuple(false, true, false),
                                           std::make_tuple(false, false, false),
                                           std::make_tuple(true, true, false)));
```

### **SECONDARY Pattern: Loop-Based Sequence Testing**
Use this pattern for state machine and temporal sequence validation:

```cpp
class {FunctionName}FixParam : public ::testing::Test
{
};

/// @unitspec{Function State Sequence Testing}
/// @derives{REQ_TCS_044156, REQ_TCS_524796, REQ_TCS_908226}
/// The function shall maintain correct state transitions over sequential calls.
/// State persistence and transition validation across multiple execution cycles.
/// @endunitspec
TEST_F({FunctionName}FixParam, {FunctionName}StateSequence)
{
    /// @par Scope / Purpose / Design:
    /// Check if the function maintains correct state over sequential operations.

    // GIVEN
    // Input sequences
    {ClassName} unit;
    const std::array<type1, 5U> input1Sequence{value1, value2, value3, value4, value5};
    const std::array<type2, 5U> input2Sequence{value1, value2, value3, value4, value5};

    // Expected output sequence
    const std::array<type3, 5U> expectedSequence{exp1, exp2, exp3, exp4, exp5};

    // WHEN
    for (uint8 i{0U}; i < expectedSequence.size(); i++)
    {
        type3 result{unit.method(input1Sequence[i], input2Sequence[i])};
        SCOPED_TRACE("Iteration " + std::to_string(i) + " failed");

        // THEN
        ASSERT_EQ(expectedSequence[i], result);
    }
}
/// @brief Additional information for loop iterations:
/// | input1  | input2  | expected |          Comments             |
/// |:-------:|:-------:|:--------:|:-----------------------------:|
/// |  false  |  false  |   false  | Initial state stays false     |
/// |  true   |  false  |   true   | Set state to true            |
/// |  false  |  false  |   true   | Keep state at true           |
/// |  false  |  true   |   false  | Reset state to false         |
/// |  true   |  true   |   false  | Keep state at false          |
```

### **Tuple-Based Parameterized Testing Pattern**
For mathematical functions requiring multiple inputs and outputs:

```cpp
class {FunctionName}FixParam : public ::testing::TestWithParam<std::tuple<float32, float32, float32>>
{
};

/// @unitspec{Function Mathematical Verification}
/// @derives{REQUIREMENT_ID}
///   Mathematical function verification across input ranges
/// @endunitspec
TEST_P({FunctionName}FixParam, {TestName})
{
    // GIVEN - Extract parameters from tuple
    const float32 input1{std::get<0>(GetParam())};
    const float32 input2{std::get<1>(GetParam())};
    const float32 expected{std::get<2>(GetParam())};

    // WHEN
    const float32 result{functionUnderTest(input1, input2)};

    // THEN
    ASSERT_FLOAT_EQ(expected, result);
}

///@brief Parameter mapping: input1, input2, expected
INSTANTIATE_TEST_SUITE_P({TestSuiteName}, {FunctionName}FixParam,
                         testing::Values(
                             std::make_tuple(0.0F, 0.0F, 0.0F),     // Zero case
                             std::make_tuple(100.0F, 10.0F, 1000.0F), // Positive boundary
                             std::make_tuple(-100.0F, 10.0F, -1000.0F) // Negative boundary
                         ));
```
```

### **Multi-Parameter Pattern (4+ inputs)**
```cpp
class {ComplexFunction}Test : public ::testing::TestWithParam<std::tuple<float32, float32, float32, float32, float32>>
{
};

TEST_P({ComplexFunction}Test, {TestName})
{
    // GIVEN - Extract parameters
    const float32 in1{std::get<0>(GetParam())}, in2{std::get<1>(GetParam())};
    const float32 in3{std::get<2>(GetParam())}, in4{std::get<3>(GetParam())};
    const float32 expected{std::get<4>(GetParam())};

    // WHEN
    const float32 result{complexFunction(in1, in2, in3, in4)};

    // THEN
    ASSERT_FLOAT_EQ(expected, result);
}

INSTANTIATE_TEST_SUITE_P({SuiteName}, {ComplexFunction}Test,
                         testing::Values(
                             std::make_tuple(0.0F, 0.0F, 0.0F, 0.0F, 0.0F),
                             std::make_tuple(1.0F, 2.0F, 3.0F, 4.0F, 10.0F)
                         ));
```

### **Test Implementation Strategy:**

#### **Step 1: Analyze Source for Test Approach**
- **Simple Functions**: Use TEST_P with comprehensive parameter tables
- **State Machines**: Use TEST_F with sequence loops + TEST_P for individual states
- **Complex Classes**: Combine TEST_P for methods + TEST_F for sequences
- **Initialization**: Use individual TEST_F only when necessary

#### **Step 2: Implement in Priority Order**
1. **TEST_P with Parameter Tables**: Cover all input combinations systematically
2. **TEST_F with Loops**: Validate state sequences and temporal behavior
3. **Individual TEST_F**: Only for unique scenarios that don't fit patterns

### **Coverage Standards:**
- All public interfaces, requirements, and boundary conditions
- State machine transitions and sequence validation
- Error handling, parameter validation, and edge cases
- Comprehensive parameter combinations with efficient table-driven testing

### **Tuple Best Practices:**
```cpp
// CORRECT: Descriptive variables with tuple access
const float32 controlDeviation{std::get<0>(GetParam())};
const float32 expectedResult{std::get<2>(GetParam())};

// WRONG: Direct tuple access in calls
function(std::get<0>(GetParam()), std::get<1>(GetParam()));
```

### **Assertion Strategy Guidelines**
**Choose the correct assertion type based on data type and test intent:**

```cpp
/**
 * Assertion Selection Rules:
 * 
 * ASSERT_EQ(actual, expected)           // Integer, boolean equality
 * ASSERT_FLOAT_EQ(actual, expected)     // Exact float32 comparison  
 * ASSERT_NEAR(actual, expected, tolerance) // Approximate float32 comparison
 * ASSERT_TRUE/ASSERT_FALSE(condition)   // Boolean conditions
 * ASSERT_GT/ASSERT_LT(actual, threshold) // Range comparisons
 * 
 * Default: Use ASSERT_* (stops test on failure)
 * Exception: Use EXPECT_* only when subsequent assertions provide diagnostic value
 */
```

## Test Design Principles

### Logic Flow Validation
**CRITICAL**: Test design must match actual implementation logic flow

1. **State Transition Accuracy**:
   - Test state changes in exact order they occur in source code
   - Account for multiple state changes in single function call
   - Validate intermediate states, not just final outcomes
   - Test reset/trigger cycles that happen in same execution

2. **Counter State Tracking**:
   - Track actual counter values between test phases
   - Don't assume arithmetic differences - verify actual values
   - Account for overflow protection in test calculations
   - Test boundary conditions at exact threshold values

3. **Parameter Timing Considerations**:
   - Understand when parameters are evaluated vs. when state changes
   - Test parameter changes mid-test to isolate logic branches
   - Verify parameter precedence and interaction effects
   - Test edge cases where parameters equal boundary values

### Test Logic Validation Checklist
Before implementing tests, verify:
- [ ] Execution order understood correctly
- [ ] State transitions mapped accurately
- [ ] Counter progressions calculated correctly
- [ ] Reset conditions and timing identified
- [ ] Boundary comparisons (>, >=) verified
- [ ] Parameter interactions documented
- [ ] Edge cases identified and planned

### Test Input Strategy
- **Threshold Testing**: Values just above/below thresholds
- **Arbitrary Values**: Distinguish from default parameters
- **Boundary Values**: Min/max ranges and edge cases
- **Invalid Inputs**: Test error handling and validation

### Expected Output Validation
- **Special Values**: Use computed values from requirements
- **Complex Computations**: Test special cases computable by hand
- **General Cases**: Use unoptimized formulas for validation
- **Define Constants**: Store expected outputs in variables if computed
- **Smart Assertions**: Use Greater/Smaller comparisons when appropriate
- **Sequential Validation**: Compare with previous outputs when relevant

### Test Scope and Design Documentation
- **Delete if Trivial**: Skip documentation for standard tests
- **Requirement Mapping**: Specify which requirement part each test covers
- **Code Workarounds**: Explain deactivated code or workarounds
- **Quirks and Gotchas**: Document test peculiarities and reasons
- **Additional Context**: Provide information needed to understand test design
- **Avoid Repetition**: Don't repeat Unit Spec information

### Loop and Sequence Testing
- **Time Progression**: Use loops only to pass time or run sequences
- **Parameter Distinction**: Differentiate parameters with same default values
- **Constant Curves**: Set to varying values for better validation

### Initialization and Assertions
- **Pre-test Validation**: Use ASSERT() to check initialization before main test
- **Sequential Code**: Validate setup state before testing main functionality
- **Output Definition**: Define expected outputs before inputs if necessary


# Example: Complete Unit Test File Creation From Scratch

## New Test File Generation Process:

### Step 1: Source Code Analysis
**Analyze source files that need testing:**
- rbc_vdms_core-espmode-arbitration.hpp (interface analysis)
- rbc_vdms_core-espmode-arbitration.cpp (implementation analysis)

### Step 2: Test File Planning
**Determine new test file structure:**
- **File Name**: `test_rbc_vdms_core-espmode-arbitration.cpp`
- **Test Class**: `VDMSArbitrationTest`
- **Required Includes**: Source headers, GTest
- **Test Categories**: Speed control, mode changes, error handling

### Step 3: Complete Test File Creation
```cpp
///
/// @file : test_rbc_vdms_core-espmode-arbitration.cpp
///
/// @copyright
/// Robert Bosch GmbH reserves all rights even in the event of industrial property rights.
/// We reserve all rights of disposal such as copying and passing on to third parties.
///
///

#include "../../../src/rbc_vdms_core-espmode-arbitration.hpp"
#include "rbc_vdms_enums.h"
#include "gtest/gtest.h"

namespace rbc
{
namespace vdms
{

/// @addtogroup rbc_vdms_core-espmode-arbitration
/// @{

/// @unitspec{Vehicle Speed Based Mode Change Control}
/// @derives{VDMS-SPEED-001}
/// Driver's request to change VDMS operating mode shall be checked against vehicle speed conditions.
/// 
/// When vehicle speed is categorized as HIGH_SPEED (>100 km/h), mode change requests shall be prevented
/// and system returns Pata_ModeNormal for safety. When vehicle speed is LOW_SPEED (<=50 km/h) or 
/// MEDIUM_SPEED (50-100 km/h), normal arbitration logic applies with existing environmental checks.
/// Speed categorization uses evaluateVehicleSpeedMode() to convert continuous speed values (m/s) to 
/// enumerated categories (LOW_SPEED, MEDIUM_SPEED, HIGH_SPEED) for deterministic safety decisions.
/// High-speed restriction takes priority over all other mode change conditions.
/// @endunitspec

/// @unitspec{Input arbitrtaion won by HW}
/// @derives{VDMS-324;VDMS-325;VDMS-326}
/// VDMS operating modes shall be switchable based on driver's request
/// @endunitspec

TEST(CoreEspmodeArbitrationTest, Handbagfailure)
{
    /// @par Scope / Purpose / Design: VDMS shall be in passive mode disable if handbag failure is detected.
    /// Describe the scope / purpose of the test: Testing to check if VDMS goes under passive disable mode even
    /// if transition is allowed under handbag detection scenerio.

    // GIVEN
    // Input values
    // Define here the inputs for the test
    constexpr const boolean handBagDetected{true};
    constexpr const Pata_Mode modeRequested{Pata_ModePassive};
    constexpr const boolean modeChangeIsAllowed{true};
    constexpr const boolean espIsReactivated{false};
    constexpr const boolean passiveModeIsAllowed{true};
    constexpr const VehicleSpeedMode vehicleSpeedMode{LOW_SPEED};

    // Expected output valueszl
    const Pata_Mode expmodeSelected = Pata_ModePassiveDisable;

    // WHEN
    // Assign input values to input signals
    const auto actmodeSelected =
        sendVDMSmode(modeRequested, modeChangeIsAllowed, passiveModeIsAllowed, espIsReactivated, handBagDetected, vehicleSpeedMode);

    // THEN
    // Check the output
    ASSERT_EQ(actmodeSelected, expmodeSelected);
}

TEST(CoreEspmodeArbitrationTest, LowSpeedAllowsSportMode)
{
    /// @par Scope / Purpose / Design: LOW_SPEED permits sport mode when conditions met
    /// Describe the scope / purpose of the test: Sport mode allowed at low speed

    // GIVEN
    constexpr const Pata_Mode modeRequested{Pata_ModeSport};
    constexpr const boolean modeChangeIsAllowed{true};
    constexpr const boolean passiveModeIsAllowed{true};
    constexpr const boolean espIsReactivated{false};
    constexpr const boolean handBagDetected{false};
    constexpr const VehicleSpeedMode vehicleSpeedMode{LOW_SPEED};

    // Expected output values
    const Pata_Mode expected{Pata_ModeSport};

    // WHEN
    const auto result =
        sendVDMSmode(modeRequested, modeChangeIsAllowed, passiveModeIsAllowed, espIsReactivated, handBagDetected, vehicleSpeedMode);

    // THEN
    ASSERT_EQ(result, expected);
}

/// @}

} // namespace vdms
} // namespace rbc

```

### Step 4: Complete Test File Validation
- Validate compilation, confirm public method coverage, verify boundary conditions

## New Test File Creation Summary

**New Test File Generated:** Complete unit test file created from scratch

**Test File Structure:** File header, includes, test fixture, unit specifications, test implementations, AI code tags

**Test Coverage:** Speed-based validation, boundary testing, state transitions, error handling, parameter dependencies

**Quality Metrics:** Public interface coverage, boundary testing, requirements traceability, test isolation

## Best Practices Applied:
1. **Source-First Analysis**: Thorough .hpp and .cpp analysis before test creation
2. **Requirements Traceability**: Tests linked to functional requirements
3. **Documentation Standards**: Proper @unitspec blocks for every test
4. **Pattern Consistency**: Following project testing patterns
5. **AI Code Identification**: Proper tagging with timestamps

## **Test Quality Assessment Framework**
**Post-implementation validation to ensure comprehensive test coverage:**

### **Coverage Metrics:**
- [ ] **Public Interface Coverage**: All public methods tested
- [ ] **State Transition Coverage**: All possible state transitions validated  
- [ ] **Boundary Coverage**: All threshold values and edge cases tested
- [ ] **Error Path Coverage**: Invalid inputs and error conditions tested
- [ ] **Parameter Combination Coverage**: All significant parameter interactions tested

### **Code Quality Metrics:**
- [ ] **Compilation Success**: All tests compile without errors/warnings
- [ ] **Test Independence**: All tests pass individually and as suite
- [ ] **Test Isolation**: Tests are isolated and independent
- [ ] **No Interdependencies**: No test ordering requirements or shared state
- [ ] **Assertion Quality**: Appropriate assertion types used (ASSERT_* vs EXPECT_*)

### **Documentation Quality:**
- [ ] **Test Documentation**: Every test has clear @par Scope/Purpose/Design
- [ ] **Requirement Traceability**: Every unitspec links to requirements via @derives
- [ ] **Test Naming**: Test names clearly indicate what is being tested
- [ ] **Edge Case Rationale**: Edge case selection and rationale documented
- [ ] **AI Code Marking**: ContainsGenAICopilot notice properly placed

### **Compliance Verification:**
- [ ] **Platform Types**: All variables use platform types (float32, boolean, etc.)
- [ ] **C++11 Compliance**: No C++14+ features used
- [ ] **Const Correctness**: Local variables marked const when appropriate
- [ ] **Brace Initialization**: All variables use brace initialization
- [ ] **MISRA Compliance**: Code follows MISRA guidelines where applicable

After adding the Test cases and the verifications. With user consent load the #Run_Unit_Tests.md and then run the tests as instructed in it


