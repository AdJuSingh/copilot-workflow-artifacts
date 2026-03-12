
# Instructions for Codebase Modifications

Explicitly prompt the user to input an {Implementation_plan} and specify the workspace to make the edits {Codebase_for_edits}.
With the context of the {Implementation_plan}, {codebase_for_edit} perform modifications in the directory. Clearly understand the files given in the implementation plan and perform the modifications keeping a workspace-level view in mind. Your job is to follow the implementation plan, don't make any decisions or direct away from the implementation plan

Implementation instructions

# Avoid making assumptions. If you need additional context to be accurate, ask the user for the missing information. Be specific about which context you need.
# Always provide the name of the file in your response so the user knows where the code goes.

# Always do the multi-turn codebase modification systematically.
# Don't get caught in infinite loops, perform modification with planning
# Important: Ask for user consent before modifying each and every file - involve the user in the loop every time, ask for user consent before modifying any file. Don't modify everything together.

# Workflow
1) Suggest a unit specification and let the user review the same
2) Write down the unit specification in the corresponding test file as comments
3) Read and understand the .hpp file to be modified
4) Suggest changes for the .hpp file design document and make changes with user approval
5) Read and understand the cpp file to be modified - especially map the key functions and classes to avoid repetition
6) Suggest changes for the .cpp implementation file and make changes with user approval
7) Read and understand the corresponding test file to be modified
8) Create test implementation

Note: Repeat the same steps if multiple test, cpp, hpp files need to be modified
Note: Unit spec is not actual test implementation with Test_F, it focuses on documentation and planning.

Analyze the following before generating the unit specification:
1. **Requirements Analysis**: Identify test scenarios, state transitions, boundary conditions, edge cases, and input/output relationships.
2. **Existing Test Pattern Analysis**: Review existing test files for structure, complexity, mock parameter patterns, and documentation style.
3. **Test Planning**: Plan core functionality, boundary value, state machine transitions, parameter dependency, and error handling scenarios.

4. **Unit Specification Template**: Use the following template, compress the unit_spec for multiple TEST_F to a single block:
'''cpp
/// @unitspec{<Title>}
/// @derives{requirement_id}
///   <Content: break down the requirement to design aspects.
///    Design the desired dynamic behavior.
///    Ensure it is sufficient to derive the test from,
///    including e.g. relevant parameter values.>
/// @endunitspec'''

General Instructions
1) Follow Guidelines
    -> MISRA C++ 2008 
    -> Autosar C++ 2014
    -> Cert C++
2) Code is clean, readable, and maintainable - use DRY(Don't Repeat Yourself) Coding principle
3) No over-engineering - don't complicate the workspace modification, keep it as simple as possible by trying to understand what the file does and then doing conservative modification.
4) In newly created code, follow the existing coding pattern strictly
5) Use existing C/C++ functions, or the functions that the user has already declared. avoid declaring new functions - if a built-in function can help with the task, you must use it.
Example: If the function max(a,b,c) can be used in place of [if (a>b), else if (b>c) else a>c], use max
6) **Clean includes**: Add proper include statements in main implementation files

### Adapting an Existing `@unitspec`

When modifying an existing `@unitspec`:
- Keep the existing `@derives` links unless they are incorrect.
- Add new `@derives` links separated by `;` if multiple requirements apply: `@derives{TSC-339;TSC-318}`
- Update the content text to reflect the changed or extended behavior.
- Do NOT remove existing test cases below the `@unitspec` unless they are wrong.

### Do's
1) Make the modifications as per plan and strictly follow the workflow defined
2) Add extra comments that this code segment has been modified based on the updated requirements provided by the user in timestamp (HH:MM-MM-DD-YY),
3) Use tag "//ContainsAIGeneratedcode"
4) Keep the code clean

### Don'ts
1) Do not modify any file that's out of the main code directory
2) Do not hallucinate if any information is missing from the context or not in KG, Directory, Doors, DoxyGen; be confident to ask the user for clarification.

# Best practices
1) Declare variables in the smallest scope possible
2) C++ enums shall be scoped when used
3) Yoda condition - Place the constant or literal on the left side of the comparison operator
4) To improve code clarity, maintainability, and thread safety by making communication between methods explicit through return values and parameters, rather than relying on hidden communication via modification of member variables
5) Prefer const over non-const by default.
6) Never use the "at" function for accessing std::array elements
7) Do function declaration without default values
8) Do not pass outputs as parameters/arguments
9) The multiple usage of a pdl function call within the same scope should not be done because it is not guaranteed that the compiler will inline it. Without inlining there will be a higher resource consumption. Instead of calling the same pdl function multiple times, assign it to a constant.
10) When to use struct
    Simple Data Structures (Plain Old Data Object - PODO):
        When you need a simple collection of related data without complex behavior.
        When you primarily want to group data and make it easily accessible (e.g., coordinate points, configuration settings).
        When you want all members to be accessible by default.

    Use class primarily for:
    Objects with encapsulation and behavior:
        When you need to implement data hiding (encapsulation), protecting the internal state of your object.
        When you need to define methods (functions) that operate on the data and maintain the object’s integrity.
        When you want to control access to the object’s data members, allowing modification only through specific methods.

    Object-Oriented Programming (OOP): When you are designing classes that will be used in an object-oriented context, but avoid Inheritance

    Enforcing invariants: When it’s crucial to maintain certain properties or relationships between data members, and you want to enforce these through methods and constructors.

11) When to implement a constructor for a class
    1) Initializing member variables
    2) Ensuring valid object state
       
## Naming Conventions
### File Naming

- **File names** may only contain: lowercase letters, `-`, and `_`.
- **Source files**: `rbc_<component_namespace>_[<module-name>_]<unit-name>.<ext>` (e.g., `rbc_tsc_pt1-filter.hpp`)
- **Test files**: `test_rbc_<component_namespace>_[<module-name>_]<unit-name>.cpp` — **one test file per unit**
- **Mock files**: `mock_rbc_<component_namespace>.<ext>`
- **Unit suffixes** (only if >1 class per unit): `_types` for types, `_func` for implementation. **Do not use suffixes for test files.**
- **Unit names** may only contain lowercase letters and `-`.

### Code Naming

- **Classes**: PascalCase: `Pt1Filter`, `OffsetCompensation`
- **Functions/Methods**: camelCase: `calc()`, `addNumbers()`
- **Parameters**: camelCase: `inputValue`, `timeConstant`
- **Member variables**: camelCase without prefix: `previousOutput`, `filterCoefficient`
- **Namespaces**: lowercase: `rbc::tsc`


- Use platform types: `float32`, `boolean`, `uint8`, `uint16`, `uint32`, `sint8`, `sint16`, `sint32`.
- Mark local variables as `const` when they don't change.
- Use explicit parentheses for operator precedence.
- One test file per unit.
- Link requirements via `@derives{TSC-xxx}` in each `@unitspec`.

#### Pre-Implementation Validation
1. **Parameter Type**: Verify `RB_getCurve()` for 1-D parameters, `RB_getParam()` for scalars
2. **Data Type Compatibility**: Ensure parameter output type matches target variable type
3. **Unit Consistency**: Validate unit conversions are mathematically correct
4. **Range/Overflow**: Calculate max_value * conversion_factor ≤ target_type_max
5. **Project Standards**: Use RB_FloatConversion.h instead of standard C++ casting

#### Post-Implementation Validation
- Verify PDL stub and DCM file generation for new parameters
- Test boundary conditions and maximum parameter values
- Validate dependent file updates in build system

#### Enhanced Don'ts
- Never use `static_cast` - use project-specific conversion utilities
- Never assume parameter dimensions - verify in .pdl files
- Never skip overflow analysis for unit conversions
- Never proceed without confirming dependent file generation

# Instructions for editing .hpp files

1) .hpp is a detailed software design document
2) .hpp file must contain:
    - Algorithm description @unit documentation
    - State machine logic function comments
    - Design decisions in comprehensive comments
3) All functional requirements are reflected in the interface design
4) Input/output structures cover all required data elements
5) Algorithm logic is clearly documented in comments
6) Design decisions are justified and traceable to requirements
7) Interface follows consistent naming conventions
8) @unit documentation block provides a comprehensive overview



# Instructions for editing .cpp files


1) Code follows TDD principle: minimal implementation that makes tests pass
2) All test cases should pass successfully
3) State machine logic correctly implements requirements (if applicable)
4) Threshold comparisons use correct operators
5) Hysteresis behavior properly implemented (if applicable)
6) Edge cases and boundary conditions handled correctly
7) In DEM communication Failure words, uses only 0 and 1, 0U, 1U,(Binary(0,1) appended with U) not 2U etc.
8) Parameter definition in .pdl file must be referred and reused


# Instructions for editing unit test files

1) Use GTEST framework
2) Every TEST_F, TEST_P should have its own unit_spec block
3) Expect requirements to drive test_specification
4) Global @unitspec provides a comprehensive unit overview with requirements traceability
    **CRITICAL: Individual @unitspec block created for EVERY planned test scenario**
    **CRITICAL: Each @unitspec follows exact template format with proper @addtogroup/@endunitspec structure**

5)  All functional requirements covered by planned test scenarios
    Boundary conditions and edge cases identified and planned
    Test fixture properly designed with appropriate setup methods
    Mock parameters and dependencies identified and stubbed
    NO TEST_F functions implemented (planning phase only)
    Clear requirements traceability in each @unitspec block
    Test file structure follows existing codebase patterns
    Test complexity matches implementation complexity

6)  All core functionality is tested with clear scenarios
    Boundary conditions and thresholds are thoroughly tested
    State machine transitions are validated (if applicable)
    Parameter dependencies are properly tested
    Edge cases and error conditions are covered
    Test complexity matches implementation complexity
    Tests follow existing patterns and naming conventions
    All tests pass and validate correct implementation behavior

7) There should be no test coverage gaps
8) Consider the impact of added test cases in existing Test Files

## Code Consistency Rules

### Function Signature Changes
- **ALWAYS verify all call sites** when modifying function signatures
- Search for all usages using `list_code_usages` tool before and after changing parameters
- Update ALL call sites in the same commit/session as the signature change
- Add TODO comments at call sites when proper input values are not yet available

### Compilation Error Handling
- Read the FULL error message including file paths and line numbers
- Check function declarations vs implementations for parameter count/type mismatches
- When function requires new parameter without available input:
  - Use safe default value (e.g., LOW_SPEED for safety-critical features)
  - Document with inline TODO comment explaining missing integration
  - Log as technical debt for future sprint

### Verification Steps
1. After editing function signatures: grep search for function name across codebase
2. Count parameters in declaration vs all call sites
3. Run build task immediately after changes
4. If build fails, read error logs completely before attempting fix

## Workflow for Multi-File Changes
- Make related changes atomically using `multi_replace_string_in_file`
- Declaration change + all call site updates = single operation
- Never leave partial updates that would break compilation

# Take care of the security aspect
# For the modifications made, update the relevant elements in the Knowledge_graph to reflect the changes made if applicable


# Example
Response from codebase modification step:

1. Unit specification suggestion
/// @addtogroup rbc_vdms_core-espmode-arbitration
/// @{

/// @unitspec{Vehicle Speed Based Mode Change Control}
/// @derives{VDMS-XXX}
/// Driver's request to change VDMS operating mode shall be checked against vehicle speed conditions.
/// 
/// When vehicle speed is categorized as HIGH_SPEED, mode change requests shall be prevented.
/// When vehicle speed is LOW_SPEED or MEDIUM_SPEED, normal arbitration logic shall apply.
/// Speed categorization converts continuous speed values to enumerated categories for safety decisions.
/// @endunitspec

/// @}

User feedback: Okay
2. Writing unit specification in test file
test_rbc_vdms_core-espmode-arbitration.cpp+9-0

3. Reading and understanding .hpp file
rbc_vdms_core-espmode-arbitration.hpp

4. Suggesting changes for .hpp file
    Current Understanding:

    File contains the sendVDMSmode function declaration
    Function currently takes 5 parameters for environmental checks
    Need to add vehicle speed categorization support
    Proposed Changes for rbc_vdms_core-espmode-arbitration.hpp:

    Add Vehicle Speed Category Enum (will be added to rbc_vdms_enums.h)
    Add Speed Categorization Function Declaration
    Update sendVDMSmode Function to include vehicle speed category parameter
    Update @unit Documentation to reflect new speed-based checks
    Add comprehensive algorithm description for speed categorization
    Specific modifications:

    Add categorizeVehicleSpeed() function declaration
    Update sendVDMSmode() signature to include VehicleSpeedCategory vehicleSpeedCategory parameter
    Update @unit documentation to include vehicle speed conditions
    Add algorithm documentation for speed-based mode change prevention

5. Implementing changes for .hpp file

    rbc_vdms_enums.h+8-0
    Step 4b: Modifying the Header File
    rbc_vdms_core-espmode-arbitration.hpp+5-1
    rbc_vdms_core-espmode-arbitration.hpp+9-1

6. Reading and understanding .cpp file
    Read rbc_vdms_core-espmode-arbitration.cpp
7. Suggest changes for the .cpp file
    Proposed Changes:
    Add categorizeVehicleSpeed() function implementation
    Update sendVDMSmode() function signature and add speed-based logic
    Integrate high-speed restriction as primary safety check
8. Implement changes if approved for the .cpp file
    rbc_vdms_core-espmode-arbitration.cpp+42-6
9. Reading and understanding the test file
    Read test_rbc_vdms_core-espmode-arbitration.cpp, lines 1 to 100
10. Create test implementation and ask for user feedback
    Suggested TEST_F, TEST_P

11. Modify the test files
    test_rbc_vdms_core-espmode-arbitration.cpp+56-1

Summary of codebase modifications completed
✅ Files modified:

rbc_vdms_enums.h - Added VehicleSpeedCategory enum
rbc_vdms_core-espmode-arbitration.hpp - Updated function signatures and documentation
rbc_vdms_core-espmode-arbitration.cpp - Implemented speed categorization and updated arbitration logic
test_rbc_vdms_core-espmode-arbitration.cpp - Added unit specification and new test cases
✅ Key changes implemented:

Vehicle speed categorization with LOW_SPEED, MEDIUM_SPEED, HIGH_SPEED enums
Updated sendVDMSmode function to prevent mode changes at high speeds
Added categorizeVehicleSpeed function for speed-to-enum conversion
Enhanced test coverage with speed-specific scenarios
Maintained existing functionality while adding new safety restrictions

### Implementation Quality Checklist
- ✅ Extract complex conditionals into const boolean variables
- ✅ Use meaningful variable names (systemDegraded vs repeated conditions)  
- ✅ Limit function complexity (max 20 lines of logic)
- ✅ Create reusable components for cross-variant functionality




