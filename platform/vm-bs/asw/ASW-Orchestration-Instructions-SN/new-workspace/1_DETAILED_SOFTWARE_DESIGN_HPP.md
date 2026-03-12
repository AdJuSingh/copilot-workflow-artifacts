## Generate Detailed Software Design (.hpp file)
Create a header file (.hpp) with detailed software design based on functional requirements.
## Pre-Analysis Required
Before generating the header file:
**Requirements Analysis**: Review functional requirements and identify input/output interfaces

## Request Format
```
Based on the requirements in [REQUIREMENTS_FILE], create a detailed software design header file for [UNIT_NAME].
Requirements to implement:
- [LIST_KEY_REQUIREMENTS]
Expected complexity level: [SIMPLE/MODERATE/COMPLEX]
Special considerations: [ANY_SAFETY_OR_PERFORMANCE_REQUIREMENTS]
```

# Create Detailed Software Design (.hpp file)
Following Instructions should be followed without fail
## 🚨 CRITICAL: DESIGN FORMAT REQUIREMENT
**THE DETAILED SOFTWARE DESIGN MUST BE IMPLEMENTED AS THE `.hpp` HEADER FILE ITSELF**
- ❌ **DO NOT** create separate markdown design documents (`.md` files)
- ❌ **DO NOT** create design specifications in any other format
- ✅ **DO** implement the design directly as the `.hpp` header file
- ✅ **DO** use the header file documentation as the design specification
**The `.hpp` file serves as BOTH:**
1. **Detailed Software Design** (through comprehensive @unit documentation)
2. **Implementation Interface** (through class structure and function declarations)

**ONLY create this file:**
- ✅ `src/rbc_vdms_{domain}_{unit}.hpp` - The header file IS the design

## 📋 DESIGN COMPLETENESS REQUIREMENTS
**The `.hpp` file MUST contain all design information:**
- Algorithm descriptions in @unit documentation
- State machine logic in function comments
- Interface specifications in struct definitions
- Requirement traceability in @unit block
- Design decisions in comprehensive comments

## Critical Instructions for Header File Generation
### PRIORITY 1: Follow Existing Codebase Patterns
**BEFORE generating any code, examine the existing codebase for patterns:**
1. **Use of C++ Std Library functions**: If any of the implementation handled by std libraries, use it instead of creating redundent functions ex: use of fmin instead of ternary operator
2. **File naming**: Look for hyphens vs underscores in existing files
3. **Header extensions**: Check if existing files use `.h` or `.hpp`
4. **Code complexity**: Examine existing implementations for complexity level
5. **Documentation style**: Match the verbosity level of existing documentation
6. **Class structure**: Check if existing classes use helper functions or inline implementation
**Example Pattern Detection Process:**
```bash
# Check existing file patterns:
# If you see: rbc_vdms_{domain}_{unit-name}.hpp (with hyphens)
# Then use: rbc_vdms_{domain}_{unit-name}.hpp (NOT rbc_vdms_{domain}_{unitname}.hpp)
# 
# Examples:
# - rbc_vdms_dpb_input-conversion.hpp
# - rbc_vdms_dpb_brake-request.hpp  
# - rbc_vdms_multi_domain-control.hpp
```
### PRIORITY 2: Match Implementation Complexity
**Simple Requirements = Simple Implementation**
If the requirements can be implemented in 2-3 lines of code, DO NOT add:
- Input validation functions
- Multiple helper functions  
- Extensive error handling
- Complex documentation
**Complex Requirements = Structured Implementation**
Only add modular structure when:
- Algorithm has multiple decision branches
- Safety requirements explicitly demand validation
- State machines with multiple transitions
- Performance optimization is needed

### 🔍 PRIORITY 3: Detect Over-Engineering
**Red Flags to Avoid:**
- Creating helper functions for single `std::fminf()` calls
- Adding validation for basic mathematical operations
- Extensive documentation for simple calculations
- Breaking 2-line algorithms into multiple functions
**Green Flags for Simplicity:**
- Direct implementation in main function
- Inline comments explaining the algorithm
- Minimal but clear documentation
- Straightforward input/output handling
## Header File Structure Template
### File Naming Conventions
Follow existing codebase patterns:
- **Header files**: Use exact pattern from existing codebase (check for hyphens vs underscores)
- **Include guards**: Mirror the filename pattern exactly in uppercase
- **Class names**: Use PascalCase (e.g., `InputConversion`, `BrakeRequest`)
### Complete Header File Template
```cpp
///
/// @file
///
/// @copyright
/// Robert Bosch GmbH reserves all rights even in the event of industrial property rights.
/// We reserve all rights of disposal such as copying and passing on to third parties.
///
///
#ifndef RBC_VDMS_{UNIT_NAMESPACE_UPPER}_{UNIT_FILENAME_UPPER}_HPP__
#define RBC_VDMS_{UNIT_NAMESPACE_UPPER}_{UNIT_FILENAME_UPPER}_HPP__
#include "Platform_Types_h.hpp"
#include "rbc_VDMS_parameters_pdl.h"
#include "rbc_vdms_enumerations.h"
// Add unit-specific includes here
namespace rbc
{
namespace vdms
{
namespace {UNIT_NAMESPACE}
{
/// @unit
///   {UNIT_DESCRIPTION}
///
///   **Design decision:**
///   {CONCISE_DESIGN_DESCRIPTION}
///   
///   **Core algorithms:**
///   - {ALGORITHM_1_DESCRIPTION}
///   - {ALGORITHM_2_DESCRIPTION}
///   
///   **Requirements traceability:**
///   - {REQUIREMENT_ID_1}: {BRIEF_REQUIREMENT_DESCRIPTION}
///   - {REQUIREMENT_ID_2}: {BRIEF_REQUIREMENT_DESCRIPTION}
///   
///   // KEEP DOCUMENTATION BRIEF - focus on essential design decisions
///   // AVOID extensive requirement traceability unless explicitly needed
/// @endunit
/// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
/// @{

class {UNIT_CLASS_NAME}
{
  public:
    struct InStruct
    {
        {DATA_TYPE} {INPUT_NAME_1};     ///< {INPUT_DESCRIPTION_1}
        {DATA_TYPE} {INPUT_NAME_2};     ///< {INPUT_DESCRIPTION_2}
        // Add more inputs as needed - keep input structure simple
    };

    struct OutStruct
    {
        {DATA_TYPE} {OUTPUT_NAME_1};    ///< {OUTPUT_DESCRIPTION_1}
        {DATA_TYPE} {OUTPUT_NAME_2};    ///< {OUTPUT_DESCRIPTION_2}
        // Add more outputs as needed - keep output structure simple
    };

    /// @brief {MAIN_FUNCTION_DESCRIPTION}
    /// @param input Input structure containing {UNIT_DOMAIN} domain signals
    /// @return Output structure containing processed {UNIT_DOMAIN} signals
    static OutStruct calc(const InStruct& input);
    
    // AVOID private helper functions for simple calculations
    // ONLY add private methods if algorithm is genuinely complex
};

/// @}
} // namespace {UNIT_NAMESPACE}
} // namespace vdms
} // namespace rbc

#endif // RBC_VDMS_{UNIT_NAMESPACE_UPPER}_{UNIT_FILENAME_UPPER}_HPP__
```

## Template Variables for Header Files

### Basic Unit Information
- `{UNIT_NAME}`: Human-readable unit name
- `{UNIT_NAMESPACE}`: Namespace identifier (lowercase, e.g., dpb, multi, abs)
- `{UNIT_FILENAME}`: Base filename (lowercase, e.g., input-conversion, brake-request)
- `{UNIT_DESCRIPTION}`: Brief description of unit functionality
- `{UNIT_CLASS_NAME}`: Main class name (PascalCase, e.g., InputConversion, BrakeRequest)
- `{UNIT_DOMAIN}`: Domain name (e.g., DPB, Multi-Domain, ABS)
### File Naming
- `{UNIT_NAMESPACE_UPPER}`: Uppercase namespace for header guards
- `{UNIT_FILENAME_UPPER}`: Uppercase filename for header guards
### Interface Elements
- `{INPUT_NAME_1}`, `{INPUT_NAME_2}`: Input signal names
- `{INPUT_DESCRIPTION_1}`, `{INPUT_DESCRIPTION_2}`: Input signal descriptions
- `{OUTPUT_NAME_1}`, `{OUTPUT_NAME_2}`: Output signal names
- `{OUTPUT_DESCRIPTION_1}`, `{OUTPUT_DESCRIPTION_2}`: Output signal descriptions
- `{DATA_TYPE}`: Data type (float32, boolean, enum, etc.)
- `{MAIN_FUNCTION_DESCRIPTION}`: Description of main calc function
### Design Documentation
- `{CONCISE_DESIGN_DESCRIPTION}`: Brief design rationale
- `{DESIGN_SPEC_REFERENCES}`: Design specification references (if needed)
## Header File Design Guidelines
### Documentation Requirements
**Keep It Simple:**
- Focus on essential design decisions
- Avoid extensive requirement traceability unless explicitly needed
- Use minimal but clear documentation
- Include brief parameter descriptions
### Interface Design
**Input/Output Structures:**
- Use clear, descriptive member names
- Include brief comments for each member
- Group related inputs/outputs logically
- Use appropriate data types
**Function Interface:**
- Static calc() function as main entry point
- Clear parameter and return documentation
- Avoid complex function signatures
### Include Strategy
**Standard Includes:**
- `Platform_Types_h.hpp` for basic types
- `rbc_VDMS_parameters_pdl.h` for parameter access
- `rbc_vdms_enumerations.h` for enumerations
- Add unit-specific includes as needed
**Pattern Consistency:**
- Match existing file extension patterns (`.h` vs `.hpp`)
- Follow existing include order
- Use same header guard style
### Class Structure Guidelines
**When to Keep Simple:**
- Mathematical conversion functions
- Simple state assignments
- Direct parameter lookups
- Basic arithmetic operations
**When to Add Structure:**
- Complex state machines with multiple transitions
- Functions with multiple algorithm branches
- Safety-critical functions requiring validation

### Copilot Self-Review Checklist:
- [ ] ✅ All functional requirements are reflected in the interface design
- [ ] ✅ Input/output structures cover all required data elements
- [ ] ✅ Algorithm logic is clearly documented in comments
- [ ] ✅ Design decisions are justified and traceable to requirements
- [ ] ✅ Interface follows consistent naming conventions
- [ ] ✅ @unit documentation block provides comprehensive overview
- [ ] ✅ Implementation complexity matches requirements complexity
- [ ] ✅ No over-engineering or unnecessary helper functions
- [ ] ✅ Code patterns match existing codebase style

### Common Mistakes to Avoid:
- Adding helper functions for simple calculations
- Over-documenting simple interfaces
- Using inconsistent naming patterns
- Adding unnecessary validation interfaces
- Breaking simple algorithms into complex class hierarchies


Allow the user to verify the implementation, If the User provides any feedback follow the same and make chanegs accordingly, if the user is satisfied - prompt to move to the next step and if the user approves load the 2_UNIT_TEST_WITH_UNITSPEC.md and follow the instructions written there
