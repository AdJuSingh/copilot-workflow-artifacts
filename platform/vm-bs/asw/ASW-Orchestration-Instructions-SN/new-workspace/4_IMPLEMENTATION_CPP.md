# Create Implementation (.cpp file)
# Prompt 4: Create TDD Implementation (.cpp file)
## Objective
Create a clean, efficient implementation file using Test-Driven Development (TDD) principles. The implementation should make all existing unit tests pass, following the KISS principle and matching the complexity required by the tests.

## Context Requirements
### 1. Header File and Design Analysis
- Review the header file structure and function declarations.
- Understand input/output data structures defined in the design.
- Check for any special requirements or constraints from design specifications.

### 2. Test-Driven Implementation Planning
- Review existing unit tests to understand expected behavior.
- Identify algorithm patterns from test cases and assertions.
- Plan for appropriate use of standard library functions.

### 3. Design Specification Implementation
- Implement only what is specified in the header file and design documents.
- Keep implementation minimal and focused on design contracts.

## Request Format
```text
Based on the header file [HEADER_FILE], detailed software design specifications, and existing unit tests [TEST_FILE], create the implementation for [UNIT_NAME].
Implementation approach: [TEST_DRIVEN_DEVELOPMENT]
Key algorithms to implement (from tests and design):
- [LIST_CORE_ALGORITHMS_FROM_TESTS]
- [LIST_STATE_LOGIC_FROM_DESIGN]
- [LIST_CALCULATIONS_FROM_TEST_CASES]
Design specifications: [REFERENCE_TO_DETAILED_SOFTWARE_DESIGN]
Test requirements: [BEHAVIOR_EXPECTED_BY_UNIT_TESTS]
Standard library usage: [PREFER_STD_FUNCTIONS_WHERE_APPLICABLE]
```

# Instruction 4: Create TDD Implementation (.cpp file)
## Critical Instructions for Test-Driven Implementation
### 🚨 PRIORITY 1: Follow Existing Codebase Patterns
1. **Use of C++ Std Library functions**: Prefer std libraries over redundant functions (e.g., `std::fminf`).
2. **File naming**: Match existing file naming conventions.
3. **Code complexity**: Align with existing implementations.
4. **Documentation style**: Match verbosity of existing documentation.
5. **Function structure**: Follow existing codebase preference for helper or inline functions.

### 🚨 PRIORITY 1.5: Test-Driven Development Approach
- **Primary Reference**: Unit test file to understand expected behavior.
- **Secondary Reference**: Header file (.hpp) and design specification.
- **Implementation Goal**: Make all existing tests pass with minimal, clean code.

### 🎯 PRIORITY 2: Match Implementation Complexity
**Simple Requirements = Simple Implementation**
- Avoid input validation functions or multiple helper functions unless explicitly required.
**Complex Requirements = Structured Implementation**
- Add modular structure only for algorithms with multiple decision branches or safety-critical requirements.

### 🔍 PRIORITY 3: Code Simplicity and Over-Engineering Prevention
Keep It Simple (KISS Principle):
- Prefer direct implementation over helper functions for simple calculations.
- Avoid input validation unless explicitly required by safety standards.
- Use minimal documentation—focus on essential design decisions.
- Implement algorithms inline rather than breaking them into multiple private functions.
- Choose aggregate initialization (`OutStruct output{};`) over default initialization when possible.
- Avoid unnecessary abstraction layers for straightforward mathematical operations.
Red Flags:
- Creating helper functions for single `std::fminf()` calls.
- Adding validation for basic mathematical operations.
- Extensive documentation for simple calculations.
- Breaking 2-line algorithms into multiple functions.
Green Flags:
- Direct implementation in main function.
- Inline comments explaining the algorithm.
- Minimal but clear documentation.
- Use of standard library functions where appropriate.
When to Keep It Simple:
- Mathematical conversion functions (min/max selections, unit conversions).
- Simple state assignments.
- Direct parameter lookups.
- Basic arithmetic operations.
- Straightforward boolean logic.
When Additional Complexity May Be Justified:
- Complex state machines with multiple transitions.
- Safety-critical functions requiring validation.
- Functions with multiple algorithm branches.
- Performance-critical code requiring optimization.
- Functions explicitly requiring error handling per requirements.

# Best practices
1) Declare variables in the smallest scope possible
2) C enums shall be scoped when used
3) Yoda condition - Place the constant or literal on the left side of the comparison operator 
4) To improve code clarity, maintainability, and thread safety by making communication between methods explicit through return values and parameters, rather than relying on hidden communication via modification of member variables
5) Prefer const over non-const by default.
6) Never use the "at" function for accessing std::array elements 
7) Do Function declaration without default values
8) Don't pass outputs as parameters/arguments
9) The multiple usage of a pdl function call within the same scope should not be done because it is not guaranteed that the compiler will inline it. Without inlining there will be a higher resource consumption. Instead of calling the same pdl function multiple times, assign it to a constant.
10) When to use struct
    Simple Data Structures (Plain Old Data Object - PODO):
        When you need a simple collection of related data without complex behavior.
        When you primarily want to group data and make it easily accessible (e.g., coordinate points, configuration settings).
        When you want all members to be accessible by default.

    Use class primarily for:
    Objects with Encapsulation and Behavior:
        When you need to implement data hiding (encapsulation), protecting the internal state of your object.
        When you need to define methods (functions) that operate on the data and maintain the object’s integrity.
        When you want to control access to the object’s data members, allowing modification only through specific methods.

    Object-Oriented Programming (OOP): When you are designing classes that will be used in an object-oriented context, involving concepts like inheritance, polymorphism, and abstract classes.

    Enforcing Invariants: When it’s crucial to maintain certain properties or relationships between data members, and you want to enforce these through methods and constructors.

11) When to implement a constructor for a class
    1) Initializing Member Variables
    2) Ensuring Valid Object State
    
## Implementation File Structure Template
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

namespace rbc
{
namespace vdms
{
namespace {UNIT_NAMESPACE}
{

{UNIT_CLASS_NAME}::OutStruct {UNIT_CLASS_NAME}::calc(const InStruct& input)
{
    OutStruct output{};
    
    // PREFER DIRECT IMPLEMENTATION - avoid helper functions for simple calculations
    // Example: output.result = std::fminf(input.value1, input.value2);
    
    // AVOID input validation unless explicitly required by safety standards
    // AVOID breaking simple calculations into multiple private functions
    
    {ALGORITHM_IMPLEMENTATION}
    
    return output;
}

// ONLY add helper functions if algorithm is genuinely complex
// For simple mathematical operations, keep everything inline

} // namespace {UNIT_NAMESPACE}
} // namespace vdms
} // namespace rbc
```

## Template Variables for Implementation

### Basic Structure
- `{UNIT_NAMESPACE}`: Namespace identifier (lowercase)
- `{UNIT_FILENAME}`: Base filename (lowercase)
- `{UNIT_CLASS_NAME}`: Main class name (PascalCase)

### Function Implementation
- `{ALGORITHM_IMPLEMENTATION}`: Core algorithm code
- `{PARAM_TYPE}`: Parameter data type (usually float32)
- `{paramName}`: Parameter variable name
- `{PARAMETER_NAME}`: Parameter name for PDL access

### Algorithm Elements
- `{threshold}`: Threshold values from parameters
- `{STATE_X}`: State enumeration values
- `{condition}`: Conditional expressions
- `{calculation}`: Mathematical calculations

## Implementation Guidelines
### For Simple Calculations
- Use std library functions (e.g., `std::fminf`, `std::fmaxf`).
- Keep parameter access simple.
- Use aggregate initialization.

### For Complex Algorithms
- Use clear algorithm structure.
- Add meaningful variable names.
- Include state transition comments.

## Common Patterns to Follow
### Parameter Access
```cpp
// Get parameters once at function start
const float32 param1 = RB_getParam_VDMS_Parameter1();
const float32 param2 = RB_getParam_VDMS_Parameter2();
```

### Output Initialization
```cpp
// Use aggregate initialization
OutStruct output{};
```

### Standard Library Usage
```cpp
// Prefer std functions over custom implementation
result = std::fminf(value1, value2);
result = std::fmaxf(value1, value2);
```

### Error Handling
```cpp
// Simple default behavior for invalid cases
default:
    output.state = SAFE_DEFAULT_STATE;
    break;
```

## Quality Checklist
- [ ] Implementation follows existing code patterns
- [ ] Uses standard library functions where appropriate
- [ ] Avoids unnecessary helper functions
- [ ] Has minimal but clear documentation
- [ ] Handles invalid states gracefully
- [ ] Uses aggregate initialization
- [ ] Parameters accessed via PDL interface
- [ ] No over-engineering for simple requirements
- [ ] Clear algorithm structure for complex logic
- [ ] Consistent namespace and naming conventions
## Copilot Self-Review Checklist
### Phase 4 Completion Checklist
- [ ] ✅ Implementation satisfies all test requirements from Phase 3
- [ ] ✅ Code follows TDD principle: minimal implementation that makes tests pass
- [ ] ✅ All test cases pass successfully
- [ ] ✅ State machine logic correctly implements requirements (if applicable)
- [ ] ✅ Threshold comparisons use correct operators
- [ ] ✅ Hysteresis behavior properly implemented (if applicable)
- [ ] ✅ Edge cases and boundary conditions handled correctly
- [ ] ✅ Code is clean, readable, and maintainable
- [ ] ✅ No over-engineering beyond test and design requirements
- [ ] ✅ Implementation complexity matches requirements complexity
### TDD Validation Checklist
- [ ] ✅ All tests pass successfully
- [ ] ✅ Implementation follows TDD principles (minimal code to pass tests)
- [ ] ✅ Code satisfies all requirements from test specifications
- [ ] ✅ No over-engineering beyond test and design requirements
- [ ] ✅ Code is clean, maintainable, and follows project standards
- [ ] ✅ Primary reference: unit test file expectations met
- [ ] ✅ Secondary reference: header file design specifications implemented


Allow the user to verify the implementation, If the User provides any feedback follow the same and make chanegs accordingly

# End of workflow Orchestration