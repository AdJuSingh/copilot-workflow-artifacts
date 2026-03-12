---
applyTo: "**/doc/**/*.md"
description: "HSW Detailed Software Design (DSD) creation guidelines"
---

# Generic HSW Module Detailed Software Design (DSD) Instruction File

## Purpose
This instruction file provides comprehensive guidelines for writing Detailed Software Design (DSD) documents for HSW (Hardware related Software) modules.

**IMPORTANT**: This instruction file is for generating detailed design documentation ONLY. Implementation work should NOT be started at this level. The focus is on creating comprehensive design specifications that will guide subsequent implementation phases.

**PREREQUISITE**: Before creating a DSD, you MUST validate requirement status — see [Requirement Status Validation](#requirement-status-validation-mandatory) in the DSD Creation Process section.

**Note**: Most HSW components lack existing DSDs in workspaces. Use the guidance and templates below to create comprehensive DSDs that map requirements, architecture, behavior, and implementation details to existing source artifacts.

---

## High-Level Design Principles
- **Target Audience**: Software Component Responsibles
- **Documentation Style**: Concise, unambiguous, modular approach with emphasis on visual representations
- **Visual Elements**: Prioritize flow diagrams, sequence diagrams, state machines, and interface maps over lengthy text
- **Compliance Focus**: Include references to MISRA C, AUTOSAR standards, functional safety (ISO 26262), Vm Brakes coding guidelines and Naming Convention
- **Scope Definition**: Detail module-level behavior, inter-component communication, and system integration points without duplicating high-level system requirements
---

## Required DSD Sections Template

### 1. Document Header and Identification
- **Copyright Header** (must appear first in the document): 
Copyright (C) 2024 Robert Bosch GmbH.
The reproduction, distribution and utilization of this file as well as the communication of its contents to others without express authorization is prohibited. Offenders will be held liable for the payment of damages. All rights reserved in the event of the grant of a patent, utility model or design.
- **Title**: "Detailed Software Design - [COMPONENT_NAME] HSW Module"
- **Component Name**: Full component identifier (e.g., RBRFPEC, RBBLM, RBVLV)

### 2. Revision History and Approvals
Track document version, authorship, date, and approval status in a single revision table. Always set the status to "Draft" when creating or modifying DSD documents.

| Version | Date | Author | Changes Summary | Technical Reviewer | Safety Approver | Status |
|---------|------|--------|-----------------|-------------------|------------------|---------|
| 1.0     | YYYY-MM-DD | Name | Initial version | Reviewer Name | Safety Engineer | Draft |

### 3. References and Dependencies

**Component-Specific Artifacts:**
- UML design models: `design/[COMPONENT].xml`
- Process scheduling configuration: `cfg/[COMPONENT]_Subsystem.proc`
- API interface headers: `api/hsw/` and `api/csw/` directories
- Internal source structure: `src/` subdirectories
- Configuration data models: `cfg/*.pdm` files
- ARXML diagnostic descriptions: `doc/OBD/*.arxml`
- Customer documentation: `doc/doxygen/` generated PDFs

### 4. Component Purpose and Scope Definition
**Primary Responsibilities:**
- Concise description of component's role within HSW ecosystem
- Functional domain coverage (actuation, monitoring, diagnostics, safety)
- Hardware abstraction layer responsibilities
- Real-time constraints and performance requirements

**Scope Boundaries:**
- **Included**: Module-internal behavior, public API contracts, inter-task communication
- **Excluded**: Lower-level driver implementations, higher-level application logic
- **Interface Points**: Clearly define boundaries with adjacent HSW components and application layers

### 5. Requirements Traceability Matrix
Create comprehensive mapping between requirements, design, implementation, and tests. This is the single traceability artifact — cover both forward (Requirements → Tests) and backward (Tests → Requirements) directions here.

**Forward Traceability:** Requirements → Design → Implementation → Tests

| Requirement ID | Requirement Summary | DSD Section | Implementation File(s) | Test Case(s) | Verification Method |
|----------------|---------------------|-------------|------------------------|--------------|-------------------|
| REQ-FUNC-001 | Motor actuation control | Section 10.1 | `src/act/[COMPONENT]_ActuationRequestFlow.c` | `TEST_001_*` | Unit + Integration |
| REQ-SAFE-001 | Safety monitoring | Section 11.2 | `src/safety/[COMPONENT]_Safety.c` | `TEST_002_*` | Safety analysis |

**Backward Traceability Checks:**
- Ensure every test case traces back to specific requirements
- Verify all design elements have requirement justification
- Confirm implementation completeness against design

**Change Impact Analysis:**
- **Requirement Changes**: Impact assessment on design and implementation
- **Design Changes**: Affected requirements and implementation files
- **Implementation Changes**: Required test updates and verification

### 6. System Architecture and Component Integration

#### 6.1 Component Architecture Overview
**Visual Representation Requirements:**
- High-level component block diagram showing major functional units
- Message flow diagrams between internal modules
- External interface connection points
- Data flow direction indicators

**Module Decomposition Pattern:**
```
[COMPONENT_ROOT]/
├── api/                    # Public interface definitions
│   ├── hsw/               # HSW-level interfaces  
│   ├── csw/               # Control Software interfaces
│   └── testinjection/     # Test and diagnostic interfaces
├── src/                   # Implementation modules
│   ├── act/               # Actuation logic
│   ├── datamodel/         # Central data management
│   ├── drvIn/             # Input driver interfaces
│   ├── drvOut/            # Output driver interfaces
│   ├── safety/            # Safety and monitoring
│   ├── service/           # Service and utility functions
│   └── Mux/               # Task synchronization and multiplexing
└── cfg/                   # Configuration and calibration
```

#### 6.2 Process and Task Scheduling Architecture
Provide a summary SPG table here. For detailed process specifications, timing, and synchronization, see Section 9.

| SPG Name | Execution Rate | Process Functions | Dependencies | Purpose |
|----------|----------------|-------------------|--------------|---------|
| SPG_[COMPONENT]_Driver_Init | Init | `[COMPONENT]_PRC_*_Init` | Hardware drivers | Initialization |
| SPG_[COMPONENT]_Control_CM1ms | 1ms cyclic | `[COMPONENT]_PRC_*_1ms` | Sensor inputs | Control loops |
| SPG_[COMPONENT]_Safety_x1 | Event-driven | `[COMPONENT]_PRC_*_x1` | Monitoring data | Safety checks |

### 7. Data Model and Type Definitions

#### 7.1 Central Data Model Architecture
Document the component's central data repository (typically `src/datamodel/[COMPONENT]_DataModel.h`):

**Data Model Structure:**
```c
// Central data access pattern
[COMPONENT]_DataType_t [COMPONENT]_getData_[TaskRate](void);
void [COMPONENT]_setData_[TaskRate]([COMPONENT]_DataType_t data);
```

**Type Definition Categories:**
- **Core Data Types**: Primary structures in `src/datamodel/TypeDef/[COMPONENT]_*TypeDef.h`
- **Interface Types**: API-exposed types for external communication
- **Internal Types**: Module-private data structures
- **Configuration Types**: Calibration and parameter structures

#### 7.2 Data Ownership and Access Control
Create data ownership matrix:

| Data Element | Owner Task | Reader Tasks | Writer Tasks | Synchronization Method | Access Rules |
|--------------|------------|--------------|--------------|----------------------|--------------|
| ActuationRequest | 1ms Task | X1 Task | Application | Atomic copy | Single writer |
| FeedbackData | 1ms Task | Multiple | Driver callbacks | Double buffer | Lock-free read |

**Synchronization Mechanisms:** See Section 9.2 for the full list of inter-task communication and synchronization mechanisms. Document which mechanisms each data element uses in the matrix above.

#### 7.3 Persistent Data and Configuration
- **NVM Data**: Non-volatile memory structures and access patterns
- **Calibration Parameters**: Runtime configuration via PDM files
- **Factory Settings**: Default values and initialization procedures

### 8. Interface Contracts and Message Exchange

#### 8.1 Public API Interface Specification
For each interface header (`api/hsw/*.h`, `api/csw/*.h`), document:

| Interface Symbol | Header File | Purpose | Message Type | Direction | Timing Constraints |
|------------------|-------------|---------|--------------|-----------|-------------------|
| `[COMPONENT]_SetActuationInput` | `api/hsw/[COMPONENT]_Subsystem.h` | Actuation request | Command | Inbound | 1ms deadline |
| `[COMPONENT]_GetFeedbackData` | `api/hsw/[COMPONENT]_Feedback.h` | Status query | Query/Response | Outbound | Non-blocking |

#### 8.2 Interface Contract Details
**Function Signature Template:**
```c
/**
 * @brief [Purpose and behavior description]
 * @param[in] param1 [Description, valid range, units]
 * @param[out] param2 [Description, modification behavior]
 * @returns [Return value meaning, error codes]
 * @pre [Preconditions: system state, parameter validity]
 * @post [Postconditions: system changes, side effects]
 * @thread_safety [Concurrent access rules]
 * @real_time [Timing guarantees, WCET if known]
 */
ReturnType_t [COMPONENT]_FunctionName(InputType param1, OutputType* param2);
```

#### 8.3 Inter-Component Message Exchange Patterns

**Message Flow Categories:**
1. **Command Messages**: Control requests and actuation commands
2. **Status Messages**: Feedback and monitoring data
3. **Event Messages**: Diagnostic events and state changes
4. **Configuration Messages**: Parameter updates and calibration data

**Message Exchange Diagram Template:**
```
[Application Layer] 
        ↓ Command Messages
[Component Public API]
        ↓ Internal Processing
[Task Synchronization]
        ↓ Driver Calls
[Hardware Abstraction Layer]
        ↓ Physical Interface
[Hardware Drivers]
```

### 9. Process Scheduling and Timing Behavior

#### 9.1 Task and Process Architecture
Document all scheduled processes from `cfg/[COMPONENT]_Subsystem.proc`:

**Process Categories:**
- **Initialization Processes**: `SPG_[COMPONENT]_Driver_Init`
- **Cyclic Control Processes 1ms**: `SPG_[COMPONENT]_Control_CM1ms` 
- **Cyclic Control Processes 5ms**: `SPG_[COMPONENT]_Safety_x1`
- **Cyclic Control Processes 10ms**: `SPG_[COMPONENT]_Safety_x2`

**Process Specification Template:**
| Process Name | SPG Assignment | Execution Rate | WCET (μs) | Stack Usage (bytes) | Dependencies |
|--------------|----------------|----------------|-----------|-------------------|--------------|
| `[COMPONENT]_PRC_ActuationRequest_1ms` | Control_CM1ms | 1ms | 50μs | 256 | Input validation |

#### 9.2 Inter-Task Communication and Synchronization

**Communication Mechanisms:**
1. **Shared Data Model**: Central repository with accessor functions
2. **Task Synchronization**: Explicit sync points (e.g., `DataSyncWithX1Task_1ms`)
3. **Message Mailboxes**: Asynchronous message passing
4. **Event Flags**: State change notifications

**Synchronization Flow Diagram:**
```
1ms Task Cycle:
    ├── Read Input Data
    ├── Process Control Algorithm  
    ├── Update Shared Data Model
    ├── Trigger Sync Event
    └── Execute Output Actions

X1 Task (Event-Driven):
    ├── Wait for Sync Event
    ├── Read Synchronized Data
    ├── Execute Safety Monitoring
    ├── Update Status Flags
    └── Report Diagnostic Events
```

#### 9.3 Timing Constraints and Performance Requirements
- **Real-time Deadlines**: Maximum response times for critical functions
- **Jitter Tolerance**: Acceptable timing variations
- **Resource Budgets**: CPU utilization limits per task
- **Memory Constraints**: RAM and stack usage boundaries

### 10. Control Flow and Algorithm Design

#### 10.1 Functional Flow Diagrams
Create detailed flow diagrams for each major functional area:

**Actuation Control Flow:**
```
Actuation Request → Input Validation → Algorithm Processing → Safety Checks → Output Generation
     ↓                    ↓                    ↓                ↓              ↓
Error Handling ←    Parameter Check ←   State Machine ←   Monitor Status ← Driver Interface
```

**Monitoring and Safety Flow:**
```
Sensor Data → Filtering → Threshold Checks → Fault Detection → Reaction Strategy
     ↓           ↓            ↓                ↓               ↓
Data Logging ← Statistics ← Diagnostic ←   Safety State ←  Recovery Action
```

#### 10.2 State Machine Documentation
For components with state-based behavior, provide:

**State Machine Specification:**
- **States**: Enumerate all possible states with descriptions
- **Transitions**: Define triggers, conditions, and actions
- **State Diagram**: Visual representation of state relationships
- **Transition Table**: Tabular format for all state changes

| Current State | Event/Condition | Next State | Action | Guard Condition |
|---------------|-----------------|------------|--------|----------------|
| Idle | Actuation_Request | Active | Initialize_Control | Valid_Parameters |
| Active | Safety_Fault | SafeOff | Disable_Output | Fault_Confirmed |

#### 10.3 Algorithm Implementation Patterns

**Algorithm Categories:**
1. **Control Algorithms**: PID controllers, state estimators, signal processing
2. **Safety Algorithms**: Monitoring functions, fault detection, redundancy checks  
3. **Diagnostic Algorithms**: Self-test procedures, health monitoring
4. **Communication Algorithms**: Message handling, protocol processing

**Sequence Diagram Template:**
```
Application → Component → DataModel → Driver → Hardware
    |            |           |         |        |
Request ------→  |           |         |        |
    |       Validate ---→    |         |        |
    |            |      Store ---→     |        |
    |            |           |    Execute ---→  |
    |            |           |         |   Command -----→
    |            |      ←--- Get       |        |
    |       ←--- Response    |         |        |
Response ←---    |           |         |        |
```

### 11. Safety Architecture and Diagnostic Framework

#### 11.1 Safety Requirements Implementation Mapping
Document safety-critical functions in `src/safety/` directory:

| Safety Requirement | ASIL Level | Implementation File | Monitoring Function | Detection Time | Reaction Strategy |
|--------------------|------------|-------------------|-------------------|----------------|------------------|
| Motor disconnect detection | ASIL-B | `[COMPONENT]_Safety.c` | `UnexpectedStandstillMon` | <5ms | SafeOff activation |
| Voltage monitoring | ASIL-A | `mon/VoltageMon.c` | `UB6_UBMRVoltageCheck` | <10ms | Diagnostic event |

#### 11.2 Diagnostic Event Management
**Diagnostic Flow Architecture:**
```
Fault Detection → Event Classification → Filtering → Reporting → Reaction
     ↓                    ↓                ↓         ↓          ↓
Monitor Function ←  Severity Level ← Debounce ← DTC Code ← Recovery Action
```

**Event Categories:**
- **Critical Faults**: Immediate safety reaction required
- **Performance Degradation**: Functional limitation but safe operation
- **Information Events**: Status reporting, no immediate action needed

#### 11.3 Safety State Management
- **Safe States**: Define all safe operating modes (SafeOff, Limited Operation, Full Operation)
- **State Transitions**: Conditions for entering/exiting safe states
- **Recovery Procedures**: Automatic and manual recovery sequences
- **Redundancy Mechanisms**: Backup systems and cross-checks

#### 11.4 Hardware Availability and Integrity
Document `HardwareAvailabilityProvider` pattern:
- Hardware component status tracking
- Integrity checks and validation procedures
- Resource allocation and conflict resolution
- Hardware abstraction layer health monitoring

### 12. Hardware Abstraction and Driver Integration

#### 12.1 Physical Interface Architecture
Map hardware interfaces to software components:

| Physical Interface | Hardware Component | Driver Module | API Interface | Direction | Protocol |
|-------------------|-------------------|---------------|---------------|-----------|----------|
| GTM channels | Timer unit | `drvOut/GTM_*` | `api/hsw/[COMPONENT]_GTM.h` | Output | PWM signals |
| ADC inputs | Sensor interface | `drvIn/ADC_*` | `api/hsw/[COMPONENT]_Sensors.h` | Input | Analog conversion |

#### 12.2 Driver Abstraction Layers
**Abstraction Hierarchy:**
1. **Hardware Registers**: Direct hardware access (lowest level)
2. **Driver APIs**: Hardware-specific driver interfaces
3. **HSW Abstraction**: Component-specific hardware abstraction
4. **Component APIs**: High-level functional interfaces

**Driver Interface Contracts:**
- **Initialization**: Setup and configuration requirements
- **Runtime Behavior**: Expected response times and error handling
- **Resource Management**: Exclusive access and sharing rules
- **Error Propagation**: How driver errors are reported upward

#### 12.3 Hardware Dependency Management
Document all external dependencies:
- **Required Hardware Features**: Minimum hardware capabilities needed
- **Optional Features**: Enhanced functionality with advanced hardware
- **Hardware Variants**: Different hardware configurations supported
- **Compatibility Matrix**: Supported hardware/software combinations

### 13. Configuration Management and Calibration

#### 13.1 Configuration Data Architecture
**Configuration File Structure:**
```
cfg/
├── [COMPONENT]_Subsystem.proc     # Process scheduling configuration
├── [COMPONENT]_Parameters.pdm     # Calibration parameters
├── [COMPONENT]_Thresholds.pdm     # Safety and diagnostic thresholds
└── Diamant/                       # Hardware-specific configurations
```

#### 13.2 Parameter Management Framework
**Parameter Categories:**
- **Calibration Data**: Tunable parameters for performance optimization
- **Safety Thresholds**: Fault detection and monitoring limits
- **Hardware Configuration**: Device-specific setup parameters
- **Feature Flags**: Runtime behavior control switches

**Parameter Access Pattern:**
```c
// Parameter reading pattern
ParameterType_t value = [COMPONENT]_GetParameter(PARAM_ID);
boolean isValid = [COMPONENT]_ValidateParameter(PARAM_ID, value);
[COMPONENT]_Status_t status = [COMPONENT]_SetParameter(PARAM_ID, value);
```

#### 13.3 Runtime Configuration Management
- **Parameter Loading**: Initialization and update procedures
- **Validation Rules**: Range checks and consistency verification
- **Change Management**: Runtime parameter update protocols
- **Persistence**: NVM storage and retrieval mechanisms (see also Section 7.3 for persistent data structures)

### 14. Memory Architecture and Resource Management

#### 14.1 Memory Layout and Organization
**Memory Categories:**
- **Code Memory**: Flash/ROM for executable code
- **Data Memory**: RAM for runtime variables and buffers
- **Stack Memory**: Task-specific stack allocations  
- **NVM Memory**: Non-volatile parameter storage

**Memory Mapping Table:**
| Memory Region | Size (bytes) | Purpose | Access Pattern | Alignment |
|---------------|--------------|---------|----------------|-----------|
| Global Data | 2048 | Component variables | Read/Write | 4-byte |
| Stack (1ms task) | 512 | Local variables | Stack operations | 8-byte |
| Configuration | 1024 | Parameters | Read-only (runtime) | 4-byte |

#### 14.2 Resource Usage Constraints
**Performance Budgets:**
- **CPU Utilization**: Maximum percentage per task
- **Memory Footprint**: RAM and Flash usage limits
- **Stack Depth**: Maximum nesting levels
- **Interrupt Latency**: Response time requirements

**Resource Monitoring:**
- **Runtime Measurements**: Actual vs. budgeted resource usage
- **Peak Detection**: Worst-case resource consumption
- **Trend Analysis**: Resource usage over time
- **Limit Enforcement**: Actions when limits are exceeded

### 15. Testing Infrastructure and Observability

#### 15.1 Test Injection and Diagnostic Interfaces
**Test Interface Architecture:**
```
api/testinjection/
├── [COMPONENT]_TestInjection.h    # Test hooks and overrides
├── [COMPONENT]_Diagnostics.h      # Runtime diagnostic access
└── [COMPONENT]_Observability.h    # Monitoring and tracing
```

**Test Injection Categories:**
- **Parameter Overrides**: Runtime parameter modification for testing
- **Fault Injection**: Simulated error conditions and failures
- **State Manipulation**: Direct state machine control for testing
- **Timing Control**: Test-specific timing and scheduling overrides

#### 15.2 Observability and Monitoring Framework
**Monitoring Interfaces:**
- **State Visibility**: Real-time access to internal state variables
- **Performance Metrics**: Execution timing and resource usage
- **Event Logging**: Diagnostic event capture and analysis  
- **Data Tracing**: Signal flow monitoring and debugging

**Diagnostic Data Access Pattern:**
```c
// Diagnostic interface example
[COMPONENT]_DiagnosticData_t diagnostics = [COMPONENT]_GetDiagnosticData();
[COMPONENT]_RuntimeStats_t stats = [COMPONENT]_GetRuntimeStatistics();
boolean testMode = [COMPONENT]_SetTestMode(TEST_MODE_ENABLED);
```

#### 15.3 Unit Test Design Guidance
**Test Architecture Requirements:**
- **Stub Requirements**: Document all external dependencies requiring stubs
- **Test Data Access**: Define test-specific data accessors in DataModel
- **Isolation Strategies**: Methods for testing individual components
- **Coverage Requirements**: Minimum code and branch coverage targets

### 16. Implementation Standards and Coding Guidelines

#### 17.1 Bosch Automotive Coding Standards
**Mandatory Compliance:**
- **MISRA C 2012**: Automotive safety-critical coding standard
- **AUTOSAR Coding Guidelines**: Architecture-specific rules
- **Bosch Internal Standards**: Company-specific coding conventions
- **ISO 26262**: Functional safety development standards

#### 17.2 Naming Conventions and File Organization
**Function Naming Patterns:**
```c
// Process functions (scheduled tasks)
void [COMPONENT]_PRC_[FunctionName]_[Rate](void);

// API functions (public interfaces)  
ReturnType_t [COMPONENT]_[Action][Object](parameters);

// Internal functions (module-private)
static ReturnType_t [COMPONENT]_Local[FunctionName](parameters);

// Data access functions
DataType_t [COMPONENT]_get[DataName]_[Rate](void);
void [COMPONENT]_set[DataName]_[Rate](DataType_t data);
```

**File Organization Standards:**
- **Header Files**: Interface declarations, type definitions, constants
- **Source Files**: Implementation, static functions, local data
- **API Directory**: Public interfaces only, no implementation
- **Source Directory**: Organized by functional area (act, safety, etc.)

#### 17.3 Documentation and Header Requirements
**Mandatory Copyright Header:**
```c
/**
 * @file [filename].h
 * @brief [Brief description of file purpose]
 * 
 * @copyright
 * Robert Bosch GmbH reserves all rights even in the event of 
 * industrial property rights. We reserve all rights of disposal 
 * such as copying and passing on to third parties.
 *
 * @ingroup [COMPONENT_NAME]
 */
```

### 18. Supporting Documentation and Reference Materials

#### 18.1 Glossary and Acronym Definitions
**HSW-Specific Terms:**
- **HSW**: Hardware Software (automotive control layer)
- **SPG**: Scheduling Process Group (task organization)
- **CoToM**: Control-to-Monitoring (safety communication channel)
- **ASIL**: Automotive Safety Integrity Level (ISO 26262)
- **WCET**: Worst-Case Execution Time (timing analysis)

#### 18.2 Reference Diagrams and Templates
For detailed guidance on each diagram type (Component Architecture, Message Sequence, State Machine, Data Flow, Process Flow), see the **Flow Diagram Creation Guidelines** section.

#### 18.3 Implementation Mapping Reference
**DSD-to-Code Mapping Table:**
| DSD Section | Implementation Artifact | Verification Method |
|-------------|------------------------|-------------------|
| Interface Specification | `api/hsw/*.h` | Interface testing |
| Algorithm Design | `src/*/*.c` | Unit testing |
| Safety Requirements | `src/safety/*.c` | Safety analysis |
| Configuration Management | `cfg/*.pdm` | Integration testing |

#### 18.4 Tool and Environment Information
**Development Environment:**
- **Design Tools**: Enterprise Architect (UML modeling)
- **Build System**: CMake with MTC toolchain
- **Static Analysis**: Astrée MISRA checker
- **Version Control**: Git with component-level branching
- **Documentation**: Doxygen for API documentation generation

---

## Component Analysis Guidelines for DSD Creation

### Generic Component Structure Analysis (Applicable to all HSW modules)

#### Files and Directories to Examine (Exclude `tst/` directories):

**Design and Architecture Files:**
- `design/[COMPONENT].xml` - UML models and architectural diagrams (Enterprise Architect format)
- `cfg/[COMPONENT]_Subsystem.proc` - Process scheduling and SPG (Scheduling Process Groups) definitions
- `api/hsw/[COMPONENT]_Subsystem.h` - Main process entry points and task interfaces
- `README.md` - Component overview and documentation structure

**Core Implementation Structure:**
- `src/datamodel/[COMPONENT]_DataModel.h` - Central data repository and accessor functions
- `src/datamodel/TypeDef/` - Component-specific type definitions and structures
- `src/act/` - Actuation control logic and output handling
- `src/safety/` - Safety monitoring, fault detection, and diagnostic functions
- `src/drvIn/` - Input driver interfaces and sensor data processing
- `src/drvOut/` - Output driver interfaces and actuator control
- `src/service/` - Utility functions and helper services
- `src/Mux/` - Task synchronization and multiplexing logic

**Interface and Configuration Files:**
- `api/hsw/*.h` - Hardware Software layer public interfaces
- `api/csw/*.h` - Control Software layer interfaces  
- `api/testinjection/*.h` - Test hooks and diagnostic interfaces
- `cfg/*.pdm` - Parameter Data Management files (calibration and configuration)
- `cfg/Diamant/` - Hardware-specific configuration files

**Documentation and Specifications:**
- `doc/doxygen/` - Generated API documentation and customer documentation
- `doc/OBD/*.arxml` - Diagnostic event descriptions and fault handling
- `doc/requirements/` - Requirement linking and traceability information

#### Component-Specific Analysis Tasks:

**1. Process and Task Mapping:**
- Parse `cfg/[COMPONENT]_Subsystem.proc` to extract SPG assignments
- Identify initialization processes (`SPG_[COMPONENT]_Driver_Init`)
- Document periodic tasks (`SPG_[COMPONENT]_Control_CM1ms` - 1ms cyclic)
- Map event-driven processes (`SPG_[COMPONENT]_Safety_x1` - safety monitoring)
- List background and maintenance tasks

**2. Data Flow and Ownership Analysis:**
- Examine `src/datamodel/[COMPONENT]_DataModel.h` for data accessor patterns
- Identify `get*_1ms()` and `set*_1ms()` function pairs for 1ms task data
- Document `get*_x1()` and `set*_x1()` function pairs for event-driven data
- Find synchronization functions (e.g., `DataSyncWithX1Task_1ms`)
- Analyze double-buffering and atomic access mechanisms

**3. Safety Architecture Analysis:**
- Inspect `src/safety/[COMPONENT]_Safety.c` for main safety coordination
- Document safety monitoring functions in `src/safety/mon/` subdirectory
- Analyze hardware availability providers and integrity checks
- Map diagnostic event generation and fault reporting mechanisms
- Identify safe state definitions and transition conditions

**4. Interface Contract Extraction:**
- Parse all headers in `api/hsw/` for public function signatures
- Extract function documentation including parameters, return values, and preconditions
- Identify message exchange patterns between components
- Document error handling and exception propagation
- Map interface dependencies and include hierarchies

**5. Hardware Abstraction Analysis:**
- Examine driver interface files in `src/drvIn/` and `src/drvOut/`
- Document hardware-specific abstractions and protocols
- Identify physical interface mappings (GTM, ADC, GPIO, SPI, etc.)
- Analyze hardware variant support and configuration options

### Message Exchange and Communication Pattern Analysis

#### Inter-Component Communication Patterns:

**1. Synchronous API Calls:**
```
Component A → [COMPONENT]_PublicFunction() → Component B
    ↓
Parameter validation and processing
    ↓  
Return result or error code
```

**2. Asynchronous Message Passing:**
```
Sender Task → Message Queue → Receiver Task
     ↓              ↓             ↓
Set Event Flag → Buffer Message → Process Event
```

**3. Shared Data Model Access:**
```
Writer Task → DataModel_set*() → Central Repository
                                       ↓
Reader Task ← DataModel_get*() ← Synchronized Access
```

**4. CoToM (Control-to-Monitoring) Pattern:**
```
Control Task (1ms) → Execution Request → Monitoring Task (X1)
        ↓                                       ↓
Execute Control Logic                    Verify Execution
        ↓                                       ↓
Update Execution Status ←  Status Report ← Safety Validation
```

#### Header Dependency Analysis Steps:

**1. Include Hierarchy Mapping:**
- Start with lowest-level headers (AUTOSAR types, global definitions)
- Map component-specific type definitions (`TypeDef/*.h`)
- Document internal interface dependencies within `src/` directories
- Identify public API interfaces in `api/` directories
- Check for circular dependencies and resolve conflicts

**2. Interface Contract Documentation:**
- Extract function prototypes with complete parameter specifications
- Document input/output parameter directions and constraints
- Identify thread safety and concurrency requirements
- Map error codes and exception handling patterns
- Define call sequence requirements and usage examples

**3. Message Protocol Specification:**
- Document message formats for inter-component communication
- Define message sequence protocols and timing constraints
- Specify error handling and recovery procedures
- Map message routing and addressing schemes

### Flow Diagram Creation Guidelines

#### Recommended Diagram Types:

**1. Component Architecture Diagram:**
- Show major functional blocks within the component
- Indicate data flow directions between blocks
- Mark external interface connection points
- Highlight safety-critical paths and monitoring points

**2. Message Sequence Diagrams:**
- Document typical operational scenarios
- Show message exchange timing and ordering
- Include error handling and exception paths
- Demonstrate concurrent execution patterns

**3. State Machine Diagrams:**
- Model component operational states
- Define state transition triggers and conditions
- Show error states and recovery mechanisms
- Document timing constraints and timeouts

**4. Data Flow Diagrams:**
- Trace data from inputs through processing to outputs
- Show data transformation and validation steps
- Highlight synchronization and buffering points
- Include feedback and monitoring loops

**5. Process Flow Diagrams:**
- Map task execution sequences and dependencies
- Show inter-task communication and synchronization
- Document timing relationships and constraints
- Include initialization and shutdown procedures

---

## DSD Creation Process and Best Practices

### Prerequisites and Validation

#### Requirement Status Validation (MANDATORY)
**CRITICAL**: Before starting DSD creation, verify the requirement document status.

1. **Locate Requirement Document**: Find the component's requirement document in `doc/req-as-code/*_Req.md`
2. **Check Status Field**: Search for `:status:` field in the requirement document
3. **Validate Status**: 
   - ✅ **PROCEED** if status is: `reviewed`, `approved`, `baseline`, or `accepted`
   - ❌ **STOP** if status is: `new`, `draft`, or `in-progress`

**Action Required for "new" Status**:
```
If :status: new is found in the *_Req.md file:
→ INFORM the developer: "Requirements document has status 'new' and must be reviewed first."
→ REQUEST: "Please get the requirements reviewed and approved before proceeding with DSD creation."
→ DO NOT proceed with DSD creation until requirements are in reviewed/approved state.
```

**Rationale**: DSD documents are based on stable, reviewed requirements. Creating design documentation from unreviewed requirements leads to rework and inconsistencies.

---

### Development Workflow and Methodology

#### Phase 1: Foundation and Requirements Analysis
1. **Validate Requirements Status**: Verify requirement document is reviewed/approved (see Prerequisites above)
2. **Start with Architecture Overview**: Establish component boundaries, responsibilities, and system context
3. **Requirements Traceability**: Create comprehensive mapping between requirements and design elements  
4. **Component Scanning**: Systematically analyze source structure (excluding `tst/` directories)
5. **Interface Identification**: Extract all public APIs and message exchange patterns

#### Phase 2: Core Design Documentation  
1. **Data Model Documentation**: Central data structures and access patterns (highest priority for implementers)
2. **Interface Specifications**: Complete API contracts with message exchange protocols
3. **Process and Timing Design**: Task scheduling, synchronization, and real-time constraints
4. **Safety Architecture**: Critical monitoring functions and fault handling strategies

#### Phase 3: Implementation Guidance and Validation
1. **Algorithm Documentation**: Detailed behavioral descriptions with flow diagrams
2. **Hardware Abstraction**: Driver interfaces and physical layer dependencies
3. **Configuration Management**: Parameter handling and calibration procedures
4. **Testing and Observability**: Test hooks and diagnostic interfaces

### Documentation Best Practices

#### Visual Design Guidelines
- **Focused Diagrams**: Create separate diagrams for each major behavior (actuation, monitoring, safety, communication)
- **Layered Architecture**: Show abstraction levels from hardware to application interfaces
- **Message Flow Emphasis**: Highlight inter-component communication and data exchange patterns
- **State-Based Modeling**: Use state machines for complex behavioral documentation

#### Technical Writing Standards
- **Explicit Specifications**: Provide complete pre/post conditions and side effects for all public APIs
- **Cross-Reference Integration**: Link design elements to source files using relative paths from workspace root
- **Concurrent Access Documentation**: Clearly specify thread safety and synchronization requirements
- **Error Handling Coverage**: Document all failure modes and recovery strategies

#### Version Control and Maintenance
- **Repository Integration**: Store DSD files in component `design/` directories alongside source code
- **Change Tracking**: Maintain detailed revision history with rationale for design decisions
- **Living Documentation**: Update DSD concurrently with implementation changes
- **Review Integration**: Include DSD updates in code review processes

---

## Content Templates and Examples

### Interface Documentation Template
```markdown
#### [COMPONENT]_FunctionName API Specification

| Attribute | Value |
|-----------|-------|
| **Symbol** | `[COMPONENT]_FunctionName` |
| **Location** | `api/hsw/[COMPONENT]_Interface.h` |
| **Purpose** | [Detailed description of function behavior] |
| **Message Type** | Command/Query/Event/Status |
| **Direction** | Inbound/Outbound/Bidirectional |
| **Thread Context** | 1ms task/X1 task/Any/Interrupt |
| **Timing Constraint** | [Maximum execution time or deadline] |

**Parameters:**
- `param1` (Input): [Type, range, units, validation rules]
- `param2` (Output): [Type, modification behavior, validity]

**Returns:**
- Success: [Success condition and return value]
- Error: [Error codes and failure conditions]

**Preconditions:**
- [System state requirements]
- [Parameter validity requirements]

**Postconditions:** 
- [System state changes]
- [Side effects and notifications]

**Message Exchange Pattern:**
```
Caller → Validation → Processing → Response
   ↓         ↓           ↓          ↓
Error ←   Invalid ←  Algorithm ← Success
```

**Usage Example:**
```c
ReturnType_t result = [COMPONENT]_FunctionName(validInput);
if (result == [COMPONENT]_SUCCESS) {
    // Process successful result
} else {
    // Handle error condition
}
```
```

### Process Documentation Template
```markdown
#### [COMPONENT]_PRC_ProcessName Task Specification

| Attribute | Value |
|-----------|-------|
| **Process Name** | `[COMPONENT]_PRC_ProcessName_[Rate]` |
| **SPG Assignment** | `SPG_[COMPONENT]_[Category]_[Rate]` |  
| **Execution Rate** | [1ms/X1/Init/Background] |
| **WCET** | [Worst-case execution time in μs] |
| **Stack Usage** | [Maximum stack depth in bytes] |
| **Priority** | [Task priority level] |

**Responsibilities:**
- [Primary function description]
- [Data processing responsibilities]  
- [Output generation tasks]

**Input Dependencies:**
- [Required input data and sources]
- [Synchronization requirements]
- [Timing constraints]

**Output Products:**
- [Generated data and destinations]
- [State changes and notifications]
- [External interface updates]

**Error Handling:**
- [Fault detection mechanisms]
- [Recovery procedures]
- [Diagnostic event generation]

**Execution Flow:**
```
Input Acquisition → Validation → Algorithm → Output → Monitoring
       ↓               ↓           ↓         ↓        ↓
Error Handling ←  Parameter ←  Processing ← Update ← Status
                    Check       Logic     DataModel  Check
```
```

### Message Exchange Documentation Template
```markdown
#### [SOURCE]_to_[TARGET] Communication Protocol

**Communication Pattern:** [Synchronous/Asynchronous/Event-driven/Periodic]

**Message Categories:**
1. **Command Messages**: Control requests and actuation commands
   - Format: `CommandType_t { commandId, parameters, timestamp }`
   - Direction: Application → Component
   - Timing: Response required within [X] ms

2. **Status Messages**: Feedback and monitoring data
   - Format: `StatusType_t { statusId, values, validity }`  
   - Direction: Component → Application
   - Timing: Updated every [X] ms

3. **Event Messages**: Diagnostic events and state changes
   - Format: `EventType_t { eventId, severity, data }`
   - Direction: Component → Diagnostic Manager
   - Timing: Immediate notification required

**Protocol Sequence:**
```
Message Sender                    Message Receiver
      |                                 |
   Prepare -------- Message --------→ Validate
      |                                 |
   Wait Reply ←----- Response -------- Process  
      |                                 |
   Confirm -------- Ack/Nak --------→ Complete
```

**Error Handling:**
- **Timeout**: [Timeout duration] and recovery action
- **Invalid Message**: Rejection and error notification  
- **Resource Unavailable**: Retry mechanism and limits
- **Protocol Error**: Reset and re-initialization procedure
```

---

## Agent Memory — Continuous Learning

The agent maintains a memory file at `.github/memory/dsdLearnings.memory.md` to persist learnings across sessions.

### What to Record
- Corrections or feedback from the user that contradict or extend the instruction files
- Unexpected patterns, conventions, or naming deviations discovered in the codebase
- User preferences for DSD formatting, structure, or content not covered by instructions
- Pitfalls encountered during DSD creation or review (e.g., missing stubs, unusual feature switches)

### What NOT to Record
- Information already present in instruction files or source code
- Pre-filled summaries of the workspace structure or known patterns
- Routine actions or status updates

### When to Read
- **Always** read `dsdLearnings.memory.md` at the start of any DSD creation or review session, before beginning work.

### When to Write
- **Only** when the user explicitly requests a learning to be recorded. Do **not** write autonomously.
- Use the format:
  ```markdown
  ### YYYY-MM-DD — Short title
  What was learned and why it matters.
  ```


