
# Instructions for Unit Test Case Generation for Existing Source Files

Pre-requisite- prompt the user to input the source file/sourcefiles (Workspace/src/*) that needs to be considered for generation of Test cases and the existing test file to add the Test cases.[Test files will be in Workspace/tst/*/gtest/*/ut/*]

Wait for the User input and only proceed with the same. 

# Workflow
Generate comprehensive unit test cases for existing source files. Analyze .hpp and .cpp [Either Both Or One of them as per availablity] files to create thorough test coverage.

## Core Principles
- Analyze existing source files thoroughly before generating tests
- Focus exclusively on test generation - do NOT modify source files
- Ask for user consent before creating or modifying test files
- Generate tests systematically with proper planning

## Unit Test Generation Workflow
1) **Source Code Analysis**: Analyze .hpp files for interfaces, functions, classes, and parameters
2) **Implementation Analysis**: Analyze .cpp files for core logic, algorithms, and edge cases
3) **Requirements Analysis**: Extract functional requirements from documentation and comments
4) **Test Planning**: Identify test scenarios, coverage gaps, and testing strategy
5) **Unit Specification Creation**: Generate comprehensive unit specifications
6) **Test Implementation**: Generate TEST_F and TEST_P functions with comprehensive coverage
7) **Test Validation**: Ensure all tests compile and provide meaningful validation

## Analysis Framework

1. **Code Analysis**: 
   - Public interfaces, parameters, return types, exception handling
   - Class hierarchies, inheritance, virtual functions
   - Core algorithms, business logic, state machines
   - Decision trees, loop conditions, preconditions/postconditions

2. **Test Strategy Planning**: 
   - Positive scenarios (happy path)
   - Boundary conditions and edge cases
   - Negative scenarios (error conditions)
   - State transitions, integration points
   - Thread safety and performance requirements

3. **Pattern Analysis**: 
   - Existing test structure and naming conventions
   - Mock strategies and fixture setup
   - Documentation style and test isolation

4. **Unit Test Specification Template**: Use this template for comprehensive test documentation:
```cpp
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{
/// @unitspec{SPECIFIC_TEST_DESCRIPTION}
/// @derives{REQUIREMENT_REFERENCE}
///   FUNCTIONAL_DESCRIPTION: Detailed description of what this test validates
///   SOURCE_FUNCTION: Name of source function/method being tested
///   
///   TEST_SCENARIO: Specific scenario being tested (positive/negative/boundary/edge)
///   INPUT_CONDITIONS: Description of input parameters and their values
///   EXPECTED_BEHAVIOR: Expected output, state changes, or behavior
///   COVERAGE_FOCUS: What aspect of the code this test covers (logic path, error handling, etc.)
/// @endunitspec
/// @}
```

### Unit Specification Requirements
A Unit Spec Must:
- **Describe Input/Output Behavior**: Focus on behavior, avoid copying code
- **Consider All Use Cases**: Cover different scenarios and edge cases
- **Use Independent Parameters**: From application point of view
- **Be Testable & Precise**: Clear, measurable expectations
- **Be Atomic**: Single, focused responsibility per specification
- **Keep Comment Lines**: 80-100 characters for readability

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
- Follow C++ 11 standard, not the higher versions and dont' use std::make_unique etc. 

### Critical Don'ts
- Do NOT modify existing .hpp or .cpp files
- Don't assume functionality - analyze thoroughly
- Don't leave test gaps or use magic numbers
- Avoid brittle tests coupled to implementation details

## C++ Testing Guidelines
1) **Scope Analysis**: Understand variable scope and lifetime in source functions
2) **Enum Handling**: Ensure proper scoped enum usage in test scenarios  
3) **Comparison Logic**: Use Yoda conditions in test assertions (constant on left side)
4) **Thread Safety**: Analyze and test thread safety aspects of source code
5) **Const Correctness**: Validate const-correctness in function parameters and return values
6) **Array Access**: Test array bounds and avoid "at" function usage patterns
7) **Function Signatures**: Test functions with proper parameter validation (no default values in declarations)
8) **Output Handling**: Validate return values rather than output parameters
9) **PDL Functions**: Test repeated function calls and resource consumption patterns
10) **Data Structure Choice**: Understand when source code uses struct vs class patterns for appropriate test strategy
    Simple Data Structures (Plain Old Data Object - PODO):
        When you need a simple collection of related data without complex behavior.
        When you primarily want to group data and make it easily accessible (e.g., coordinate points, configuration settings).
        When you want all members to be accessible by default.

    Use class primarily for:
    Objects with encapsulation and behavior:
        When you need to implement data hiding (encapsulation), protecting the internal state of your object.
        When you need to define methods (functions) that operate on the data and maintain the object’s integrity.
        When you want to control access to the object’s data members, allowing modification only through specific methods.

    Object-Oriented Programming (OOP): When you are designing classes that will be used in an object-oriented context, involving concepts like inheritance, polymorphism, and abstract classes.

    Enforcing invariants: When it’s crucial to maintain certain properties or relationships between data members, and you want to enforce these through methods and constructors.

11) When to implement a constructor for a class
    1) Initializing member variables
    2) Ensuring valid object state


# Comprehensive Unit Test File Generation Guidelines

## GTEST Framework Requirements
1) **Framework Standard**: Use GTEST framework exclusively for all unit test implementations
2) **Test Structure**: Every TEST_F and TEST_P must have corresponding unit_spec documentation block
3) **Requirements Traceability**: Requirements should drive test specification and implementation
4) **Global Documentation**: Provide comprehensive unit overview with requirements traceability
    **CRITICAL: Individual @unitspec block created for EVERY planned test scenario**
    **CRITICAL: Each @unitspec follows exact template format with proper @addtogroup/@endunitspec structure**

### Unit Test Goals
- **Test Requirements**: Validate all functional requirements
- **Reach 100% Coverage**: Complete code path coverage
- **Find Bugs**: Identify defects and edge case failures

### Test Type Selection Guidelines
**TEST**: Simple self-contained tests
- All information visible in the test
- Use for straightforward, isolated functionality

**TEST_F**: Share common code between tests
- Use SetUp() for: common inputs, expected outputs, initialization sequences
- Use TearDown() for: parameter reset and cleanup
- Ideal for related test scenarios with shared setup

**TEST_P**: Parameterized tests (extends TEST_F)
- Execute same test with different parameters
- **Vary Main Inputs**: Test different operating points (vx, mue)
- **Test Different Cases**: left/right turn, forward/backward
- **Test Different Datasets**: front/rear axle variations
- Mix and match based on unit requirements

## Coverage Requirements
- **Complete Coverage**: All public interfaces, functional requirements, boundary conditions
- **Test Structure**: Proper fixture design, mock management, requirements traceability
- **Quality Assurance**: State machine testing, error handling, parameter validation
- **Zero Gaps**: All public interfaces tested with appropriate complexity matching

## Test Design Principles

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


# Example: Unit Test Generation Workflow

## Unit Test Generation Process Example:

### Step 1: Source Code Analysis
**Read and analyze existing source files:**
- rbc_vdms_core-espmode-arbitration.hpp (interface analysis)
- rbc_vdms_core-espmode-arbitration.cpp (implementation analysis)

### Step 2: Unit Specification Creation
```cpp
/// @addtogroup rbc_vdms_core-espmode-arbitration
/// @{
/// @unitspec{Vehicle Speed Based Mode Change Control Test Suite}
/// @derives{VDMS-XXX}
///   FUNCTIONAL_DESCRIPTION: Validate mode change arbitration logic based on vehicle speed conditions
///   SOURCE_FUNCTION: sendVDMSmode() and categorizeVehicleSpeed() functions
///   
///   TEST_SCENARIO: Comprehensive testing of speed-based mode change restrictions
///   INPUT_CONDITIONS: Various vehicle speeds, mode requests, and environmental conditions
///   EXPECTED_BEHAVIOR: Proper mode change prevention at high speeds, normal arbitration at low/medium speeds
///   COVERAGE_FOCUS: State transitions, boundary conditions, and safety-critical logic paths
/// @endunitspec
/// @}
```

### Step 3: Test File Structure Creation
Create/update test file: `test_rbc_vdms_core-espmode-arbitration.cpp`

### Step 4: Test Case Implementation
```cpp
// Individual test specifications and implementations
/// @unitspec{High Speed Mode Change Prevention}
/// @derives{VDMS-XXX}
///   TEST_SCENARIO: Verify mode change requests are blocked when vehicle speed is HIGH_SPEED
///   INPUT_CONDITIONS: Vehicle speed > high_speed_threshold, valid mode change request
///   EXPECTED_BEHAVIOR: Mode change request denied, current mode maintained
///   COVERAGE_FOCUS: Safety-critical high-speed restriction logic
/// @endunitspec
TEST_F(VDMSArbitrationTest, HighSpeedModeChangeBlocked) {
    // Test implementation with proper mocks and assertions
}
```

### Step 5: Test Coverage Validation
- Validate all public methods are tested
- Confirm boundary conditions covered
- Verify error handling scenarios included
## Test Implementation Summary

### Completed Unit Test Generation:

**Test File Created/Modified:**
- test_rbc_vdms_core-espmode-arbitration.cpp - Comprehensive unit test suite

**Test Coverage Implemented:**
- Speed-based mode change validation tests
- Boundary condition testing for speed thresholds  
- State machine transition validation
- Error handling and edge case scenarios
- Parameter dependency testing
- Safety-critical logic path validation

**Test Quality Metrics:**
- All public interface methods covered
- Comprehensive boundary testing implemented
- State machine transitions validated
- Requirements traceability maintained
- Test isolation and independence ensured
- Mock strategies properly implemented

## Unit Test Generation Best Practices Applied:
1. **Source-First Analysis**: Thorough analysis of existing .hpp and .cpp files before test creation
2. **Requirements Traceability**: All tests linked to specific functional requirements
3. **Comprehensive Coverage**: Zero gaps in public interface testing
4. **Documentation Standards**: Proper @unitspec blocks for every test scenario
5. **GTest Framework**: Standard testing framework usage throughout
6. **Pattern Consistency**: Following existing codebase testing patterns
7. **AI Code Identification**: Proper tagging with "//ContainsAIGeneratedcode"

After adding the Test cases and the verifications. With user consent load the #Run_Unit_Tests.md and then run the tests as instructed in it

