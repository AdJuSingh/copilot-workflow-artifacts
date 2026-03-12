# Generic HSW Module Delta Change Implementation Instructions

## Overview
This instruction file provides comprehensive guidelines for implementing delta changes in HSW (Hardware Software) modules using GitHub Copilot. These instructions are designed to be module-agnostic and can be applied to any HSW component (rbrfpec, rbblm, rbvlv, etc.).

## GenAI Code Tagging Requirements

### Intellectual Property Protection for Generated Code

**MANDATORY REQUIREMENT**: All generated code that reaches a threshold of originality ("geistige Schöpfungshöhe") must be properly tagged to protect Bosch intellectual property as recommended by RB OSS CoC (Code of Conduct) and regularly reevaluated.

#### When Tagging is Required
- Generated code which is more than a "line completion" or a standard code structure
- Any substantial algorithm implementation, complex logic, or creative code solutions
- Custom HSW module implementations with innovative approaches
- Original interface implementations with significant functionality
- Complex configuration logic or data structures

#### When Tagging is NOT Required  
- Simple line completions or auto-completions
- Standard boilerplate code patterns (headers, includes, basic function signatures)
- Trivial variable declarations or basic assignments
- Standard HSW framework usage patterns
- Basic configuration parameter definitions

#### Tagging Methods

**Function-Level Tagging** (Preferred for individual functions):
```c
/**
 * @brief Function description
 * 
 * // ContainsGenAICopilot - This notice needs to remain attached to any reproduction of this function.
 * 
 * @param[in] parameter Description
 * @return Return description
 */
ReturnType FunctionName(ParameterType parameter)
{
    // Function implementation
}
```

**File-Level Tagging** (Use when multiple functions contain generated code):
```c
/**
 * @ingroup <MODULE_NAME>
 * @{
 *
 * \file <MODULE_PREFIX>_<FunctionName>.c
 * \brief Implementation description
 *
 * \copyright
 * Robert Bosch GmbH reserves all rights even in the event of industrial property rights.
 * We reserve all rights of disposal such as copying and passing on to third parties.
 * 
 * // ContainsGenAICopilot - This notice needs to remain attached to any reproduction of this file.
 */
```

#### Implementation Guidelines for HSW Modules
1. **Assessment**: Evaluate each generated code segment for originality threshold
2. **Placement**: Add tags to function headers or file headers as appropriate
3. **Consistency**: Use file-level tagging when multiple functions contain generated code
4. **Preservation**: Ensure tags remain with any reproduction or distribution of the code
5. **Integration**: Include tagging in delta change documentation

#### Examples of HSW Code Requiring Tagging
- Complex control algorithms with unique logic flow
- Custom safety function implementations
- Original process scheduling implementations
- Innovative driver interface patterns
- Complex multiplexer coordination logic
- Custom diagnostic or monitoring algorithms

#### Examples of HSW Code NOT Requiring Tagging
- Standard process function signatures (RBPRC_*)
- Basic message interface definitions (RBMESG_*)
- Standard configuration constant definitions
- Typical include guard patterns
- Standard copyright headers and file structures

### Compliance and Review for HSW Implementation
- Code reviewers must verify appropriate tagging during delta change reviews
- Regular audits may be conducted to ensure compliance with tagging requirements
- Tags must be preserved during any code modifications or refactoring
- Documentation of tagging decisions should be maintained for audit purposes
- Delta change documentation should reference tagged code sections

## HSW Architecture Context

The Hardware-related Software (HSW) provides an abstraction layer for electronic hardware, including microcontrollers and other electronic components. The main goal is to provide a **Safe Execution Platform (SEP)** compliant with ISO 26262 ASIL D.

### HSW Layer Structure
- **MicroController**: Abstraction for the uC (functional and safety)
- **Ecu**: Electronic Control Unit layers
- **DeviceDriver**: Sensor and actuator drivers
- **Control**: Higher-level control logic
- **Library**: Common functionalities
- **Architecture**: Configuration and glue code
- **Testing**: Test infrastructure

## Standard HSW Module Structure

### Typical Module Organization
```
<module_name>/
├── api/                    # Public interfaces
│   ├── cfg/               # Configuration headers (common)
│   ├── csw/ or CSW/       # Core software interfaces (some modules)
│   └── hsw/ or HSW/       # Hardware software interfaces (some modules)
├── src/                   # Source implementation (subdirectory structure varies per module)
├── design/                # Design documentation (optional - not all modules have this)
├── cfg/                   # Configuration files (_Subsystem.proc, config headers)
├── doc/                   # Documentation
├── tst/                   # Unit tests
├── tools/                 # Build and utility tools (optional)
├── _metadata/             # Metadata (optional)
├── CMakeLists.txt         # Build configuration (some modules)
├── Build_Config.bcfg      # Build configuration (some modules)
└── README.md              # Module documentation
```

> **Note on `api/` structure**: Only some modules (e.g., rbrfpec) have all three subdirectories (`cfg/`, `csw/`, `hsw/`). Many modules place header files directly in `api/` with only `cfg/` as a subdirectory; some use uppercase (`CSW/`, `HSW/`). Follow the existing pattern of the target module.

> **Note on `src/` structure**: Subdirectory organization varies significantly by module. Examples include `act/`, `Mux/`, `safety/`, `service/` (rbrfpec), `comm/`, `functional/` (rbblm), `ControlApp/`, `ControlMotor/` (rbhydr), or a flat structure with no subdirectories (rbevp). Always examine the existing module layout before adding new files.

## Coding Standards and Conventions

### File Naming Conventions
- **Source files**: `<MODULE_PREFIX>_<FunctionName>.c`
- **Header files**: `<MODULE_PREFIX>_<FunctionName>.h`

### Mandatory Copyright Header
**CRITICAL REQUIREMENT**: Every source file (.c) and header file (.h) must start with the standard Bosch copyright header. This is non-negotiable and must be the very first content in every file.

#### Standard File Header Template
```c
/**
 * @ingroup <MODULE_NAME>
 * @{
 *
 * \file <filename>
 * \brief <brief description>
 *
 * \copyright
 * Robert Bosch GmbH reserves all rights even in the event of industrial property rights.
 * We reserve all rights of disposal such as copying and passing on to third parties.
 */
```

> **Note**: Both backslash-style (`\file`, `\brief`, `\copyright`) and at-style (`@file`, `@brief`, `@copyright`) Doxygen tags are used across the codebase. Backslash-style is more common in production code. Use whichever style is already established in the target module for consistency. The `@ingroup` and `@{` tags consistently use at-style.

#### Header Usage Guidelines
- **Always place first**: Copyright header must be the first content in every file
- **Module name**: Replace `<MODULE_NAME>` with actual module name (e.g., RBRFPEC)
- **Filename**: Replace `<filename>` with actual filename including extension
- **Brief description**: Provide concise description of file purpose
- **No modifications**: Do not modify the copyright text
- **Consistent formatting**: Maintain exact spacing and formatting

### Code Structure Standards
- **Mandatory copyright header**: Must be first content in every file
- Include proper Doxygen documentation after copyright
- Follow MISRA C coding standards
- Use consistent indentation (spaces, not tabs)
- Include proper include guard patterns

## Implementation Guidelines

### 1. Pre-Implementation Analysis
- Examine current module structure and patterns
- Identify similar existing functions for consistency
- Check configuration files and dependencies
- Understand component hierarchy and interfaces

### 2. Source Code Implementation Pattern
```c
/* realized interfaces */
#include "<MODULE_PREFIX>_<Interface>.h"

/* used interfaces */
#include "RBCMHSW_Global.h"
#include "<MODULE_PREFIX>_Config.h"

/* used interfaces (external) */
/* used interfaces (internal) */

/*************************************************************************************************
**********  Assert supported configurations: switches, parameters, constants, ...  ***************
*************************************************************************************************/

/*************************************************************************************************
***************************************  Defines  ************************************************
*************************************************************************************************/

/*************************************************************************************************
**************************************  Variables  ***********************************************
*************************************************************************************************/

/*************************************************************************************************
**************************************  Functions  ***********************************************
*************************************************************************************************/

/** \brief <Function description>
 *
 *  @param[in,out] <param>  <description>
 *  @param[in]     <param>  <description>
 *  @return                 <return description>
 */
```

### 3. API Header Structure
```c
#ifndef <MODULE_PREFIX>_<INTERFACE>_H__
#define <MODULE_PREFIX>_<INTERFACE>_H__

/* Include dependencies */
#include "RBCMHSW_Global.h"
#include "<MODULE_PREFIX>_Config.h"

/* Type definitions */
/* Function declarations */
/* Configuration mappings */

#endif /* <MODULE_PREFIX>_<INTERFACE>_H__ */
```

> **Note on include guards**: The dominant convention is double underscore suffix (`_H__`), used in ~85% of modules. Some modules use `_H` without trailing underscores. Follow the existing convention in the target module.

### 4. Configuration Integration
- Update config files in `/cfg/` and `/api/cfg/`
- Ensure proper lock definitions in config headers
- Add necessary feature switches and parameters
- Map component locks to common SYS locks



## Delta Change Implementation Process

### Step 1: Preparation and Analysis
1. **Module Assessment**
   - Identify target module and affected components
   - Review existing similar implementations
   - Understand dependencies and interface contracts
   - Check configuration requirements and constraints

2. **Architecture Alignment**
   - Verify component's place in HSW hierarchy
   - Ensure changes align with defined purpose and interfaces
   - Review approved interface users
   - Check for protected interface requirements

### Step 2: Design Documentation
Follow the "design-as-code" workflow:

1. **Component Design Updates**
   - Update `<Component>.xml` design files if needed (component design models use XML format, not YAML)
   - Define new interfaces and their approved users
   - Document internal structure changes

2. **Unit Design Documentation**
   - Create/update `<Unit>.md` files in the `design/` directory (if the module has one)
   - Document functional behavior and design choices
   - Include implementation rationale
   - Note: Some modules use `.xml` files (component-level design models) alongside `.md` files

### Step 3: Implementation
1. **Interface Contracts**
   - Define interfaces in header files with Doxygen comments
   - Include purpose, agreement, and parameter documentation
   - Ensure proper include guards and dependencies

2. **Source Implementation**
   - Add/modify functions in appropriate `/src/` subdirectories
   - Follow established patterns and coding standards
   - Include proper error handling and safety checks
   - Maintain thread safety with appropriate locking

3. **Configuration Updates**
   - Update configuration files to support new functionality
   - Add feature flags and switches as needed
   - Ensure proper lock mappings

### Step 4: Integration and Validation
1. **Build System Updates**
   - Update all relevant build configuration files
   - Ensure proper dependency management
   - Verify compilation across all configurations

2. **Documentation Updates**
   - Update README.md and design documentation
   - Include inline code documentation
   - Update interface documentation

3. **Validation**
   - Perform static analysis checks
   - Verify MISRA C compliance
   - Validate functionality through code review

## Process Scheduling and Task Placement

### Process File Structure (.proc)
Each HSW module must have a `<MODULE_PREFIX>_Subsystem.proc` file that defines the scheduling of processes within specific SPG (Scheduling Process Groups) sections. This is critical for proper real-time execution and timing compliance.

**IMPORTANT**: Process files (.proc) must also start with the standard Bosch copyright header before any process definitions.

#### Standard SPG Sections Structure

The SPG (Scheduling Process Group) sections vary by module. Below is a representative example from rbrfpec, but each module defines its own set of SPG sections based on its specific scheduling needs:

```plaintext
/*PROC_SECTION: <MODULE_PREFIX>_Subsystem */
<MODULE_PREFIX>_Subsystem.h
/*PROC_SECTION_END: */

/*PROC_SECTION: SPG_<MODULE_PREFIX>_Driver_Init */
/* Initialization processes */
/*PROC_SECTION_END: */

/*PROC_SECTION: SPG_<MODULE_PREFIX>_Control_CM1ms */
/* 1ms control processes */
/*PROC_SECTION_END: */

/*PROC_SECTION: SPG_<MODULE_PREFIX>_Handling_CMx1 */
/* High-frequency handling processes */
/*PROC_SECTION_END: */

/*PROC_SECTION: SPG_<MODULE_PREFIX>_x1H */
/* High priority X1 task processes */
/*PROC_SECTION_END: */

/*PROC_SECTION: SPG_<MODULE_PREFIX>_BeforeHydrMux_x1L */
/* Pre-multiplexer processes */
/*PROC_SECTION_END: */

/*PROC_SECTION: SPG_<MODULE_PREFIX>_AfterHydrMux_x1L */
/* Post-multiplexer processes */
/*PROC_SECTION_END: */
```

> **Module-specific SPG examples**:
> - **RBBLM**: `SPG_RBBLM_Init`, `SPG_RBBLM_1st_500us`, `SPG_RBBLM_2nd_500us`, `SPG_RBBLM_BaseOS_x1L`, `SPG_RBBLM_BaseOS_x1H`, `SPG_RBBLM_TransmitReceive_x1H`, `SPG_RBBLM_BeforeHydrMux_1ms`
> - **RBVLV**: `SPG_RBVLV_Init_BOS`, `SPG_RBVLV_Init_CM`, `SPG_RBVLV_State_CM_1ms`, `SPG_RBVLV_Supply_CM_x1H`, `SPG_RBVLV_BeforeHydrMux_x1L`
> - **RBHYDR**: `SPG_RBHYDR_Init`, `SPG_RBHYDR_PreASW_x1`, `SPG_RBHYDR_Mux_x1L`, `SPG_RBHYDR_Mux_1ms`
> - **RBEVP**: `SPG_RBEVP_x4` (single SPG for 4Hz task)
> - **RBSYS**: `SPG_RBSYS_ClearColdStartResetFlags`, `SPG_RBSYS_JitterMonitoring_x1`, `SPG_RBSYS_LockMonitoring_x2`, `SPG_RBSYS_StackCheck_x4`
> - **RBBUTSWI**: `SPG_RBBUTSWI_x1`, `SPG_ButSwi_CYCx24`, `SPG_RBBUTSWI_x4`
>
> Always examine the existing `.proc` file of the target module to understand its specific SPG structure before adding new processes.

#### Process Naming Convention
- **Initialization**: `<MODULE_PREFIX>_PRC_<FunctionName>_Init` or `<MODULE_PREFIX>_PRC_<FunctionName>_CM_init`
- **500us processes**: `<MODULE_PREFIX>_PRC_<FunctionName>_500us`
- **1ms processes**: `<MODULE_PREFIX>_PRC_<FunctionName>_1ms` or `<MODULE_PREFIX>_PRC_<FunctionName>_CM_1ms`
- **X1 High processes**: `<MODULE_PREFIX>_PRC_<FunctionName>_x1H`
- **X1 Low processes**: `<MODULE_PREFIX>_PRC_<FunctionName>_x1L`
- **X1 General**: `<MODULE_PREFIX>_PRC_<FunctionName>_x1` or `<MODULE_PREFIX>_PRC_<FunctionName>_CMx1`
- **X2 processes**: `<MODULE_PREFIX>_PRC_<FunctionName>_x2`
- **X4 processes**: `<MODULE_PREFIX>_PRC_<FunctionName>_x4`
- **X24 processes**: `<MODULE_PREFIX>_PRC_<FunctionName>_x24`
- **Boot-On-Shutdown**: `<MODULE_PREFIX>_PRC_<FunctionName>_BOS`

> **Note**: The `_CM_` infix (Control Module) is used in some modules (e.g., RBVLV) to denote control-module-specific processes. Additional timing variants (e.g., `_500us`, `_x2`, `_x4`, `_x24`) exist beyond the core set. Always check the existing module .proc file for the target module's conventions.

#### Process Placement Guidelines

1. **Driver Initialization** (`SPG_<MODULE_PREFIX>_Driver_Init` or `SPG_<MODULE_PREFIX>_Init`)
   - Hardware initialization processes
   - Bridge driver initialization
   - Configuration setup processes
   - Boot-On-Shutdown initialization (some modules use `_Init_BOS`, `_Init_CM`)

2. **Sub-millisecond Loops** (`SPG_<MODULE_PREFIX>_*_500us`)
   - High-frequency measurement and control (e.g., current measurement)
   - Used in modules requiring faster-than-1ms processing (e.g., RBBLM)

3. **1ms Control Loop** (`SPG_<MODULE_PREFIX>_Control_CM1ms` or `SPG_<MODULE_PREFIX>_*_1ms`)
   - **Feedback Collection**: Signal conditioning, measurement, feedback processing
   - **Monitoring**: Safety monitoring functions
   - **Task Synchronization**: Data sync between tasks
   - **Actuation Control**: Motor control and actuation requests

4. **High-Frequency Handling** (`SPG_<MODULE_PREFIX>_Handling_CMx1`)
   - Time-critical bridge driver operations
   - Fast control loops

5. **X1 High Priority** (`SPG_<MODULE_PREFIX>_x1H`)
   - Critical data processing
   - High-priority feedback collection
   - Bridge driver high-priority operations
   - Base OS operations (some modules use `SPG_<MODULE_PREFIX>_BaseOS_x1H`)

6. **Before Hydraulic Multiplexer** (`SPG_<MODULE_PREFIX>_BeforeHydrMux_x1L`)
   - Multiplexer coordination setup
   - Control-to-Monitor (CoToM) mediator updates
   - Pre-multiplexer state management
   - Some modules also have `SPG_<MODULE_PREFIX>_BeforeHydrMux_1ms`

7. **After Hydraulic Multiplexer** (`SPG_<MODULE_PREFIX>_AfterHydrMux_x1L`)
   - Safety monitoring and diagnostics
   - Bridge driver monitoring
   - Configuration monitoring
   - Self-tests and diagnostics
   - Voltage and current monitoring
   - Motor protection functions
   - Data synchronization for next cycle

8. **Lower-Frequency Tasks** (`SPG_<MODULE_PREFIX>_x2`, `SPG_<MODULE_PREFIX>_x4`, `SPG_<MODULE_PREFIX>_CYCx24`)
   - Used for periodic tasks at lower frequencies (2Hz, 4Hz, 24ms cycles)
   - Stack checking, lock monitoring, button evaluation, etc.
   - Not all modules have these; they are module-specific

#### Process Execution Order Dependencies

When adding new processes, consider these execution order requirements:

1. **Data Dependencies**: Processes that produce data must execute before consumers
2. **Safety Chain**: Monitoring processes should execute after the functions they monitor
3. **Synchronization**: Data sync processes must be placed appropriately in the execution cycle
4. **Hardware Dependencies**: Hardware operations must follow proper sequencing

Example execution order considerations:
```plaintext
/* Data conditioning must come before users of conditioned data */
<MODULE_PREFIX>_PRC_iSumB6Conditioning_X1
<MODULE_PREFIX>_PRC_CollectAndProvideActuationFeedback_x1H

/* Monitoring must come after the monitored function */
<MODULE_PREFIX>_PRC_MotorSupplyReverseVoltageProtection_x1  /* After actuation */
<MODULE_PREFIX>_PRC_Ub6UbmrVoltageMon_x1L  /* After RVP calculation */

/* Sync must be at end of cycle */
<MODULE_PREFIX>_PRC_GetToSyncDataFor1ms_x1L  /* After all requesters */
```

### Implementation Guidelines for Process Changes

#### Adding New Processes
1. **Identify Correct SPG Section**: Determine appropriate scheduling group based on:
   - Execution frequency requirements
   - Priority level
   - Dependencies on other processes
   - Safety criticality

2. **Consider Execution Order**: Place new processes considering:
   - Data flow dependencies
   - Hardware access sequences
   - Safety monitoring chains
   - Timing constraints

3. **Update Process File**: Add process entry to appropriate SPG section
4. **Verify Dependencies**: Ensure all required data is available when process executes
5. **Validate Timing**: Ensure timing requirements are met through static analysis

#### Process Placement Best Practices
- **Group Related Functions**: Keep related processes in the same SPG section when possible
- **Minimize Inter-Task Communication**: Reduce data passing between different task levels
- **Respect Hardware Constraints**: Follow hardware access patterns and restrictions
- **Maintain Safety Chains**: Ensure safety monitoring processes execute after monitored functions
- **Consider Resource Usage**: Balance CPU load across different scheduling groups

#### Process Documentation Requirements
When adding new processes, document:
- Purpose and functionality
- Execution frequency and timing requirements
- Input and output data dependencies
- Safety classification and requirements
- Inter-process dependencies and ordering constraints

## Safety and Quality Requirements

### Safety-Critical Implementation
- Follow ISO 26262 ASIL D requirements
- Include proper safety monitoring and fault detection
- Implement redundancy where required
- Document safety rationale and analysis

### Real-Time Constraints
- Consider timing requirements and execution cycles
- Implement efficient algorithms
- Avoid blocking operations in time-critical paths
- Use appropriate scheduling and priority mechanisms

### Hardware Abstraction
- Maintain proper abstraction layers
- Use standardized hardware interfaces
- Ensure portability across hardware variants
- Handle hardware-specific configuration properly

## Common Patterns and Best Practices

### Do's
- Follow established module patterns and conventions
- Use consistent naming across all files
- Include comprehensive error handling
- Maintain thread safety with proper locking
- Update all relevant documentation
- Verify interface contracts and approved users
- Consider component hierarchy and dependencies

### Don'ts
- Don't break existing interfaces without proper versioning
- Don't introduce new dependencies without justification
- Don't ignore MISRA C compliance
- Don't hardcode values - use configuration parameters
- Don't modify files outside target module without coordination
- Don't bypass safety requirements
- Don't ignore real-time constraints

## Self Review Checklist

Before considering delta change complete:

**Code Quality**
- [ ] **Copyright header present**: All files start with mandatory Bosch copyright header
- [ ] All source files compile without warnings
- [ ] MISRA C compliance maintained
- [ ] Proper error handling implemented
- [ ] Thread safety ensured with appropriate locking

**Documentation**
- [ ] Interface contracts properly documented
- [ ] Design documentation updated
- [ ] README.md updated
- [ ] Inline code documentation complete

**Integration**
- [ ] Configuration properly integrated
- [ ] Build system updated
- [ ] Dependencies correctly managed
- [ ] No regression in existing functionality
