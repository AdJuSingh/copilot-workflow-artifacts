---
description: 'Standards and templates for automotive requirements analysis documentation'
applyTo: 'doc/requirements/**/*.md'
usedBy: '.github/prompts/0-create-requirements-analysis.prompt.md'
---
# Requirements Analysis Documentation Standards

**NOTE:** This instruction file is referenced by `.github/prompts/0-create-requirements-analysis.prompt.md` which provides the workflow and execution steps for the requirements analysis agent. This file contains the detailed standards, templates, and quality guidelines.

---

Guidelines for creating high-quality requirements analysis documentation for automotive diagnostic services following ISO 26262, ISO 14229-1, and IREB standards.

## Purpose

This instruction file defines standards for creating requirements analysis documentation that:

1. **Ensures Traceability** - Maintains complete bidirectional traceability between requirements and implementation
2. **Supports Functional Safety** - Aligns with ISO 26262 and ASIL requirements for automotive safety
3. **Facilitates Verification** - Provides clear, testable requirements that enable validation
4. **Enables Compliance** - Documents conformance to ISO 14229-1 UDS protocol and MISRA C/AUTOSAR coding standards
5. **Maintains Consistency** - Establishes templates that ensure uniform documentation across all requirements

**Target Users:** Requirements engineers, software architects, safety engineers, developers, and testers working on automotive diagnostic systems.

**Scope:** This instruction applies to all requirements analysis documents in `doc/requirements/` that analyze UDS diagnostic services, DIDs (Data Identifiers), and related functionality.

**Relationship to Detailed Software Design:** Requirements analysis documents provide the foundation for Detailed Software Design (DSD) by establishing clear, traceable requirements. The analysis ensures that all design decisions in DSD documents are properly justified and linked back to verified requirements. This supports design review, component specification, architecture definition, and interface contracts documentation.

## Design Principles

All requirements analysis documentation must follow these core principles:

### 1. Source-Driven Analysis

- **Principle:** Base ALL analysis exclusively on `doc/requirements.csv`
- **Rationale:** Ensures single source of truth and prevents speculation
- **Implementation:** Never reference implementation files, test files, or design documents in requirements analysis

### 2. Functional Grouping

- **Principle:** Group related requirements by function, not by ID
- **Rationale:** Improves readability and reduces documentation redundancy
- **Implementation:** Combine session/security/addressing requirements into "Service Configuration" sections

### 3. Standards Compliance

- **Principle:** Ensure compliance with automotive standards
- **Standards:**
  - **ISO 26262** - Functional safety (ASIL levels, safety requirements)
  - **ISO 14229-1** - UDS protocol specification
  - **MISRA C** - C coding guidelines for safety-critical systems
  - **AUTOSAR** - Automotive software architecture standards
  - **Bosch** - Company-specific coding and documentation standards
  - **IREB** - Requirements engineering best practices

### 4. Error Handling by Evidence

- **Principle:** Document error handling ONLY when explicitly specified in requirements
- **Rationale:** Prevents assumption-based analysis and maintains requirements fidelity
- **Implementation:** Include NRC codes only if mentioned in requirements.csv text

### 5. Template Consistency

- **Principle:** Use standardized templates for all requirement types
- **Rationale:** Ensures predictable structure and reduces review time
- **Implementation:** Follow Template 0-5 patterns for different requirement categories

## Project Context

- **Domain:** Automotive diagnostic services (UDS protocol)
- **Safety Standards:**
  - ISO 26262 functional safety (ASIL-B through ASIL-D requirements)
  - Functional safety architecture and safety mechanisms
- **Technical Standards:**
  - ISO 14229-1 UDS specification
  - IREB requirements engineering methodology
- **Coding Standards:**
  - MISRA C:2012 for safety-critical embedded C code
  - AUTOSAR architecture and naming conventions
  - Bosch coding guidelines and best practices
- **Source:** All requirements sourced from `doc/requirements.csv`
- **Output:** Structured markdown documentation in `doc/requirements/`
- **Target Audience:** Software architects, developers, safety engineers, testers, requirements engineers

## Guidelines

### Core Instructions

**Instructions:** Follow these core guidelines when creating [REQUIREMENTS_ANALYSIS_DOCUMENTS]. Each guideline ensures consistency, traceability, and compliance with [AUTOMOTIVE_STANDARDS].

- **Document** ALL analysis exclusively based on [REQUIREMENTS_CSV] at `doc/requirements.csv`
- **Never** reference [IMPLEMENTATION_FILES], [TEST_FILES], or [DESIGN_DOCUMENTS] in analysis
- **Use** structured [TEMPLATES] for consistency across all [REQUIREMENTS_DOCUMENTS]
- **Maintain** complete [TRACEABILITY] with [PARENT_REQUIREMENTS] and [CHILD_REQUIREMENTS]
- **Group** related [REQUIREMENTS] by [FUNCTION] for clarity and efficiency
- **Include** [FEATURE_SUMMARY] section at start of each [FEATURE_ANALYSIS]
- **Define** descriptive [SECTION_HEADERS] (e.g., "Service Configuration") without [REQUIREMENT_IDS]
- **List** combined [REQUIREMENT_IDS] in the "Requirements:" field within each [SECTION]
- **Create** [SUBFUNCTION_ANALYSIS] ONLY if [REQUIREMENTS] exist in [REQUIREMENTS_CSV] - Do not create speculative analysis
- **Include** [NRC_ERROR_HANDLING] ONLY if explicitly mentioned in [REQUIREMENTS_CSV] - Never infer or assume [NRC_CODES]

### Error Handling Guidelines

**Instructions:** Follow these error handling guidelines to ensure [REQUIREMENTS_ANALYSIS] robustness. Define how to handle [PREREQUISITES], [MISSING_DATA], and [INVALID_INPUTS].

**Prerequisite Validation:**

- **Check** that [REQUIREMENTS_CSV] exists at `doc/requirements.csv` before starting [ANALYSIS]
- **Verify** [CSV_FILE] is properly formatted and readable
- **Validate** that requested [REQUIREMENT_IDS] exist in the [CSV]
- **If prerequisite fails:** Document the [FAILURE] and request user to provide correct [ARTIFACTS]

**Missing Information Handling:**

- **If** [REQUIREMENT_TEXT] is incomplete → State "Not specified in requirements" explicitly
- **If** [TRACEABILITY_FIELDS] are empty → Document as "No parent/child requirements specified"
- **If** [NRC_CODES] are ambiguous → Do NOT assume standard [NRC_CODES]; document ambiguity
- **If** [DID_DETAILS] or [SERVICE_DETAILS] are missing → Request clarification rather than inferring from [IMPLEMENTATION]
- **Never** supplement missing information from [IMPLEMENTATION_FILES] or [ASSUMPTIONS]

**Invalid Data Recovery:**

- **If** [REQUIREMENT_ID] format is invalid → Report validation error with correct [FORMAT]
- **If** [CSV_DATA] is malformed → Skip affected rows and document [PARSING_ERRORS]
- **If** [CROSS_REFERENCES] are broken → Report broken links and suggest [CORRECTIONS]

**Fallback Strategies:**

- When partial [INFORMATION] is available, document what exists and clearly mark what is [MISSING]
- Provide [TEMPLATES] for missing [SECTIONS] but do not populate with assumed [DATA]
- Reference relevant [ISO_STANDARDS] (14229-1, 26262) for [DOMAIN_CONTEXT] only, not for filling [GAPS]

## Document Structure Standards

### Placeholder Reference Guide

**Instructions:** When creating templates or examples, you must use generic placeholders that can be replaced with actual values. This guideline defines standard placeholders for common elements.

**Generic Placeholders:**

- `[X]` - Generic numeric value or index (e.g., byte X, field X)
- `[Y]` - Secondary numeric value or index
- `[Name]` - Generic name placeholder (e.g., [ComponentName], [FunctionName])
- `[Component]` - Software component identifier
- `[Author]` - Document author name
- `[Date]` - Date timestamp (ISO 8601 format: YYYY-MM-DD)
- `[filename]` - File path or name
- `[Rate]` - Frequency or rate value (Hz, ms, etc.)
- `[TaskRate]` - Task execution rate

**Usage Example:**

```markdown
Created by [Author] on [Date]
Component: [Component]
Function: [FunctionName] executed at [TaskRate]Hz
```

**How to Use This Template:**

1. **Identify** the placeholder type needed for your context
2. **Replace** the placeholder with the actual value from requirements.csv
3. **Verify** that all placeholders have been replaced before finalizing

### Overall Organization

Each requirements analysis document follows this structure:

```markdown
# Requirements Analysis: [Document Title]

## Feature: [DID/Feature Name]

### Feature Summary
[Overview section]

---

## Service Configuration
[Configuration analysis]

---

## Request/Response Messages
[Message format analysis]

---

## Behavioral Implementation
[Behavioral analysis]

---
```

**Note:** Section headers use descriptive titles only. Requirement IDs are listed in the "Requirements:" field within each section, not in the header.

### File Naming Convention

**Instructions:** Name [REQUIREMENTS_ANALYSIS] files using the standardized format below. Replace [DID] with the  actual Data Identifier value.

- **Format:** `DCOM_<[DID]>_Requirements.md`
- **Examples:** `DCOM_0x2046_Requirements.md`, `DCOM_0xF190_Requirements.md`
- **Location:** `doc/requirements/`
- **Rule:** One file per [DID] or [FEATURE]

## Requirements Grouping Best Practices

**Instructions:** Group related [REQUIREMENTS] into logical [SECTIONS] to improve readability and reduce redundancy. Use the following grouping patterns for common [REQUIREMENT_CATEGORIES].

### Group 1: Service Configuration

**Instructions:** Combine all [SERVICE_CONFIGURATION] requirements into a single section.

**Combine into single section:**

- [DIAGNOSTIC_SESSION] requirements
- [SECURITY_LEVEL] requirements
- [ADDRESSING_MODE] requirements
- [SERVICE_AVAILABILITY] requirements

**Section Header:** Service Configuration

**Requirements Field:** `[SWCS_XX_1], [SWCS_XX_2], [SWCS_XX_3]` (combined [IDS] listed in Requirements: field)

### Group 2: Request & Response Messages

**Instructions:** Combine all [MESSAGE_FORMAT] requirements into a single section covering both [REQUEST] and [RESPONSE] structures.

**Combine into single section:**

- [REQUEST_MESSAGE_FORMAT] requirements
- [RESPONSE_MESSAGE_FORMAT] requirements
- [MESSAGE_STRUCTURE] specifications

**Section Header:** Request/Response Messages

**Requirements Field:** `[SWCS_XX_6], [SWCS_XX_7], [SWCS_XX_8]` (combined [IDS] listed in Requirements: field)

### Group 3: Behavioral Implementation

**Instructions:** Combine all [BEHAVIORAL] and [IMPLEMENTATION_LOGIC] requirements into a single section.

**Combine into single section:**

- [BEHAVIORAL_LOGIC] requirements
- [DATA_SOURCE_MAPPING] requirements
- [VARIABLE_MAPPING] requirements
- [STATE_MANAGEMENT] requirements

**Section Header:** Behavioral Implementation

**Requirements Field:** `[SWCS_XX_10], [SWCS_XX_11]` (combined [IDS] listed in Requirements: field)

## Template Patterns

**Instructions:** Use the following templates to structure your requirements analysis. Replace placeholders [LIKE_THIS] with actual content from requirements.csv. Each template provides a consistent framework for documenting specific requirement categories.

### Template 0: Feature Summary

**Purpose:** Define the scope and components involved for a [DID] or [FEATURE].

**Instructions:** Create this section at the beginning of each requirements analysis document. Specify the [DID_IDENTIFIER], [FEATURE_NAME], high-level [SCOPE_DESCRIPTION], and list all involved [COMPONENT_NAMES].

```markdown
## Feature: [DID_IDENTIFIER] - [FEATURE_NAME]

### Feature Summary

**Scope:** [High-level description of feature coverage]

**Involved Components:** [COMPONENT_1], [COMPONENT_2], [COMPONENT_3] (e.g., DCOM, Dcm, DiagnosticMonitor)

---
```

### Template 1: Service Configuration Group

**Purpose:** Document configuration requirements for [SESSION_SUPPORT], [SECURITY_LEVEL], and [ADDRESSING_MODE].

**Instructions:** Combine all service configuration requirements (session, security, addressing) into a single section. List all [REQUIREMENT_IDS] in the Requirements field. Quote the complete [REQUIREMENT_TEXT] from requirements.csv.

```markdown
## Service Configuration

**Requirements:**

[REQ_ID_1], [REQ_ID_2], [REQ_ID_3]

**Requirement Text:**
> [Complete requirement text from CSV]

**Short Explanation:** [1-2 sentences explaining configuration purpose]

**Dependencies:**
- [List dependencies - e.g., UDS ISO 14229-1, ASIL requirements, etc.]

---
```

### Template 2: Request/Response Messages Group

**Purpose:** Specify message formats for [SERVICE_ID], [DID], [REQUEST_STRUCTURE], and [RESPONSE_STRUCTURE].

**Instructions:** Define byte-by-byte message layouts. Include [DATA_TYPES], [VALUE_RANGES], [BIT_FIELDS], and [CONVERSION_FORMULAS] as specified in requirements.csv.

```markdown
## Request/Response Messages

**Requirements:** 

[REQ_ID_1], [REQ_ID_2], [REQ_ID_3]

**Requirement Text:**
> [Complete requirement text from CSV]

**Short Explanation:** [1-2 sentences explaining message format purpose]

**Dependencies:**
- [UDS ISO 14229-1 service specification]

**API Details:**

**Request Message:**
- **Message Structure:**
  - Byte 0: Service ID = 0x[XX] ([Service Name])
  - Bytes 1-2: Data Identifier = 0x[XXXX] (big-endian)
- **Data Types:**
  - Service ID: uint8
  - Data Identifier: uint16 (big-endian)
- **Message Length:** [X bytes total]
- **Value Ranges:**
  - Service ID: 0x[XX] (fixed)
  - Data Identifier: 0x[XXXX] (fixed)

**Response Message:**
- **Message Structure:**
  - Byte 0: Service ID = 0x[XX] (positive response: 0x[Request] + 0x40)
  - Bytes 1-2: Data Identifier = 0x[XXXX] (echo, big-endian)
  - [Additional bytes with bit field breakdowns]
- **Data Types:**
  - [List all data types]
- **Bit Field Encoding:** (if applicable)
  - Bit 0: [Description] (0 = [meaning], 1 = [meaning])
  - [Continue for all bits]
- **Value Ranges:**
  - [Field name] (raw): 0x[XX] to 0x[YY]
  - [Field name] (physical): [min] to [max] [units]
- **Conversion Formulas:**
  - [Field]: Physical = ([scale] × raw) + [offset] [units]
- **Message Length:** [Y bytes total]

---
```

### Template 3: Behavioral Implementation Group

**Purpose:** Document [BEHAVIORAL_LOGIC], [DATA_SOURCE_MAPPING], [PROCESSING_ALGORITHMS], and [STATE_MANAGEMENT] for the [SERVICE] or [DID].

**Instructions:** Describe how the [COMPONENT] implements the functional behavior. Map each [OUTPUT_FIELD] to its [DATA_SOURCE]. Define [CALCULATIONS], [BIT_MANIPULATIONS], and [STATE_TRANSITIONS] as specified in requirements.csv.

```markdown
## Behavioral Implementation

**Requirements:**

[REQ_ID_1], [REQ_ID_2], [REQ_ID_3]

**Requirement Text:**
> [Complete behavioral specification from CSV]

**Short Explanation:** [1-2 sentences explaining behavioral purpose]

**Dependencies:**
- [Message format requirement IDs]
- [Service configuration requirement IDs]
- Global variables: [list]
- External systems: [list]

**Functional Behavior:**

1. **Data Source Mapping:**
   - [Detailed mapping of each output byte/field to data source]
   - [Variable-to-field mappings]

2. **Data Processing:**
   - [Transformation algorithms, calculations]
   - [Bit manipulation operations]
   - [Data validation rules]

3. **State Management:**
   - [How state variables are maintained]
   - [Who updates variables]
   - [State tracking and transitions]

4. **Business Logic:** (if applicable)
   - [Algorithm descriptions]
   - [Decision flow]

5. **Timing Constraints:** (if applicable)
   - [Response time requirements]
   - [UDS timing constraints]

**Error Handling:** (if NRC codes are explicitly mentioned in requirements.csv)

**NRC Priority Order (ISO 14229-1):**
- [List ONLY the NRC codes that are explicitly mentioned in requirements.csv]
- [Do NOT infer, assume, or add NRC codes that are not in the requirement text]
- [If NO NRC codes are mentioned in requirements.csv, OMIT this entire Error Handling section]

---
```

## Mandatory Analysis Fields

### Universal Fields (All Requirements)

1. **Requirement ID & Text** - From requirements.csv
2. **Short Explanation** - 1-2 sentences explaining purpose
3. **Component** - Owner component
4. **Dependencies** - Related standards, requirements, variables
5. **Traceability** - Parent (traces to) and child (traced by) requirements

### Type-Specific Fields

**Instructions:** Include additional fields based on requirement type. Determine the [REQUIREMENT_TYPE] from the requirements.csv and select the appropriate field set below.

**For SWFS (Software Feature Specification):**

- Purpose: [High-level functional goal]
- Functional Behavior: [Expected system behavior]

**For SWCS (Software Component Specification):**

- Purpose: [Specific technical objective]
- Error Handling: NRC codes per ISO 14229-1 (ONLY in Behavioral Implementation section, ONLY if [NRC_CODES] are explicitly mentioned in requirements.csv)
- API Details: ONLY for [MESSAGE_FORMAT] requirements

## API Details Guidelines

**Instructions:** Define API details ONLY when documenting [REQUEST_MESSAGE] or [RESPONSE_MESSAGE] format requirements. Specify [DATA_TYPES], [VALUE_RANGES], [MESSAGE_LENGTH], and [BIT_ENCODINGS] as found in requirements.csv.

### When to Include API Details

**Instructions:** Use this guideline to determine when [API_DETAILS] should be included in [REQUIREMENTS_ANALYSIS]. Evaluate each [REQUIREMENT] against these criteria.

**Include ONLY for:**

- Requirements defining [REQUEST_MESSAGE] structures
- Requirements defining [RESPONSE_MESSAGE] structures

**DO NOT include for:**

- [SESSION_SUPPORT] requirements
- [SECURITY_LEVEL] requirements
- [ADDRESSING_MODE] requirements
- General [BEHAVIOR_DESCRIPTIONS]

### API Details Components

**Instructions:** Document [API_DETAILS] using the component patterns below. Specify all [FIELD_NAMES], [DATA_TYPES], and [VALUE_RANGES] as defined in requirements.csv.

**Request Message API Details:**

- Message structure ([BYTE_LAYOUT] - byte-by-byte layout)
- Data types ([X] uint8, [Y] uint16, big-endian/little-endian)
- Value ranges (valid ranges for each [FIELD])
- [SERVICE_ID] (UDS service identifier)
- Data Identifier ([DID]/[PID]/[PARAMETER] identifier)
- Message length (total [BYTE_COUNT])

**Response Message API Details:**

- Message structure ([BYTE_LAYOUT] - byte-by-byte layout)
- Data types (including [BIT_FIELDS])
- Value ranges ([RAW_VALUES] and [PHYSICAL_VALUES])
- Conversion formulas ([FORMULA]: Physical = [SCALE] × raw + [OFFSET])
- Bit field encoding ([BIT_LEVEL] definitions)
- [SERVICE_ID] (response identifier)
- Echo fields ([DID]/[PARAMETER] echoed in response)
- Message length (total [BYTE_COUNT])

## Error Handling Standards

### NRC Code Documentation

**CRITICAL RULE:** Include error handling section ONLY in the Behavioral Implementation section, and ONLY if NRC codes are explicitly mentioned in the requirement text from requirements.csv.

**Do NOT:**

- Infer or assume NRC codes based on service type
- Add "standard" or "typical" NRC codes not in requirements
- Add error handling to Service Configuration or Request/Response Messages sections
- Add error handling section if requirements.csv does not mention NRC codes

**Do ONLY:**

- Include ONLY the specific NRC codes explicitly stated in requirements.csv
- Reference ISO 14229-1 for NRC code definitions when NRC codes are mentioned:

**Common NRC Categories:**

- Session-related errors (e.g., serviceNotSupportedInActiveSession - 0x7F)
- Security-related errors (e.g., securityAccessDenied - 0x33)
- Addressing-related errors (e.g., subFunctionNotSupported - 0x12)
- Service-specific error conditions per ISO 14229-1

**ISO 14229-1 Compliance Requirements:**

- All NRC codes MUST match ISO 14229-1 specification
- NRC values (hex codes) MUST be correct per ISO 14229-1 Table A.1
- NRC priority order MUST follow ISO 14229-1 standard (Annex A, prioritization rules)
- NRC descriptions MUST use official ISO 14229-1 terminology
- Service-specific NRCs MUST be applicable to the specific UDS service
- Only include NRCs that are defined for the specific service in ISO 14229-1 service specification
- Validate each NRC against the service's negative response behavior table in ISO 14229-1

### Error Handling Pattern

```markdown
**Error Handling:**

**NRC Priority Order (ISO 14229-1):**
1. NRC 0x7F: serviceNotSupportedInActiveSession (highest priority)
2. NRC 0x33: securityAccessDenied
3. NRC 0x13: incorrectMessageLengthOrInvalidFormat
4. NRC 0x31: requestOutOfRange
```

## Traceability Standards

### Service-Specific NRC Applicability

When documenting error handling, ensure NRC codes are appropriate for the specific UDS service:

**Service 0x22 (ReadDataByIdentifier):**

- Applicable: 0x7F, 0x33, 0x13, 0x31, 0x22
- NOT applicable: 0x12 (no sub-functions), 0x24 (not stateful), 0x72 (not programming)

**Service 0x2E (WriteDataByIdentifier):**

- Applicable: 0x7F, 0x33, 0x13, 0x31, 0x22, 0x72
- NOT applicable: 0x12 (no sub-functions), 0x24 (not stateful)

**Service 0x19 (ReadDTCInformation):**

- Applicable: 0x7F, 0x12, 0x13, 0x31
- NOT applicable: 0x33 (typically no security), 0x24 (not stateful), 0x72 (not programming)

**Service 0x2F (InputOutputControlByIdentifier):**

- Applicable: 0x7F, 0x33, 0x13, 0x31, 0x22
- NOT applicable: 0x12 (no sub-functions), 0x24 (not stateful), 0x72 (not programming)

**Service 0x31 (RoutineControl):**

- Applicable: 0x7F, 0x12, 0x33, 0x13, 0x24, 0x31, 0x22, 0x72
- All common NRCs may apply due to sub-functions and stateful nature

**Validation Rule:** Always verify each NRC against the specific service's negative response behavior table in ISO 14229-1 service specification.

## Common Patterns

**IMPORTANT NOTE:** The "Error Handling" sections shown in these patterns are REFERENCE EXAMPLES ONLY. These are NOT to be copied into your analysis unless the specific NRC codes are explicitly mentioned in requirements.csv. Do not assume or infer error handling - only include if explicitly stated in the requirement text.

### Pattern 1: DID Read Service (0x22)

Typical structure for ReadDataByIdentifier service:

1. Service Configuration (sessions, security, addressing)
2. Request/Response Messages (3-byte request, N-byte response)
3. Behavioral Implementation (data source mapping)

**ISO 14229-1 Reference:** Service 0x22 - ReadDataByIdentifier
**AUTOSAR Reference:** Dcm module, DcmDspDidRead configuration

**Request Structure:**

- Byte 0: Service ID = 0x22
- Bytes 1-2: Data Identifier = 0x[XXXX] (big-endian)
- **Message Length:** 3 bytes total

**Response Structure:**

- Byte 0: Service ID = 0x62 (positive response: 0x22 + 0x40)
- Bytes 1-2: Data Identifier = 0x[XXXX] (echo, big-endian)
- Bytes 3+: dataRecord (DID-specific data)
- **Message Length:** 3 + N bytes (N = data record length)

**Behavioral Considerations:**

- Data source mapping from internal variables to response bytes
- Real-time data reading vs cached values
- Data consistency and snapshot timing
- Endianness handling (big-endian for multi-byte values)
- Physical vs raw value conversion
- Periodic/event-triggered data updates

**Error Handling:**

**NRC Priority Order (ISO 14229-1):**

1. NRC 0x7F: serviceNotSupportedInActiveSession (highest priority)
2. NRC 0x33: securityAccessDenied
3. NRC 0x13: incorrectMessageLengthOrInvalidFormat
4. NRC 0x31: requestOutOfRange (unsupported DID)
5. NRC 0x22: conditionsNotCorrect (data not available)

**Service 0x22 Note:** Does not use NRC 0x12 (no sub-functions), 0x24 (not stateful), or 0x72 (not a programming service).

### Pattern 2: DID Write Service (0x2E)

Typical structure for WriteDataByIdentifier service:

1. Service Configuration (sessions, security, addressing)
2. Request/Response Messages (multi-byte request, 3-byte response)
3. Behavioral Implementation (validation, storage, effects)

**ISO 14229-1 Reference:** Service 0x2E - WriteDataByIdentifier
**AUTOSAR Reference:** Dcm module, DcmDspDidWrite configuration

**Request Structure:**

- Byte 0: Service ID = 0x2E
- Bytes 1-2: Data Identifier = 0x[XXXX] (big-endian)
- Bytes 3+: dataRecord (data to write, DID-specific)
- **Message Length:** 3 + N bytes (N = data record length)

**Response Structure:**

- Byte 0: Service ID = 0x6E (positive response: 0x2E + 0x40)
- Bytes 1-2: Data Identifier = 0x[XXXX] (echo, big-endian)
- **Message Length:** 3 bytes total

**Behavioral Considerations:**

- Input data validation (range, format, checksum)
- Physical vs raw value conversion
- Data persistence (volatile vs non-volatile storage)
- Write protection and authorization checks
- Side effects and system state changes
- Atomic write operations
- Write confirmation and verification
- EEPROM/NVM write cycle management

**Error Handling:**

**NRC Priority Order (ISO 14229-1):**

1. NRC 0x7F: serviceNotSupportedInActiveSession (highest priority)
2. NRC 0x33: securityAccessDenied
3. NRC 0x13: incorrectMessageLengthOrInvalidFormat
4. NRC 0x31: requestOutOfRange (invalid data value or unsupported DID)
5. NRC 0x22: conditionsNotCorrect (write preconditions not met)
6. NRC 0x72: generalProgrammingFailure (write operation failed)

**Service 0x2E Note:** Includes NRC 0x72 for write failures. Does not use NRC 0x12 (no sub-functions) or 0x24 (not stateful).

### Pattern 3: Read DTC Information Service (0x19)

Typical structure for ReadDTCInformation service:

1. Service Configuration (sessions, security, addressing)
2. Request/Response Messages (variable length based on sub-function)
3. Behavioral Implementation (DTC retrieval, filtering, snapshot/extended data)

**ISO 14229-1 Reference:** Service 0x19 - ReadDTCInformation

**Common Sub-Functions:**

- 0x01: reportNumberOfDTCByStatusMask
- 0x02: reportDTCByStatusMask
- 0x04: reportDTCSnapshotRecordByDTCNumber
- 0x06: reportDTCExtendedDataRecordByDTCNumber
- 0x0A: reportSupportedDTC

**Request Structure:**

- Byte 0: Service ID = 0x19
- Byte 1: Sub-function (reportType)
- Bytes 2+: Sub-function specific parameters (status mask, DTC number, record number)

**Response Structure:**

- Byte 0: Service ID = 0x59 (positive response)
- Byte 1: Sub-function (echo)
- Bytes 2+: Sub-function specific data (DTC count, DTC records, status availability mask, snapshot/extended data)

**AUTOSAR Reference:** Dcm module with Dem (Diagnostic Event Manager) interface

**Behavioral Considerations:**

- DTC status mask filtering (ISO 14229-1 Annex D.1)
- DTC format: 3-byte value (ISO 14229-1 Annex D.2)
- Snapshot/Extended data record numbering
- Status availability mask handling
- Memory selection (primary/user-defined/mirror memory)

**Error Handling:**

**NRC Priority Order (ISO 14229-1):**

1. NRC 0x7F: serviceNotSupportedInActiveSession (highest priority)
2. NRC 0x12: subFunctionNotSupported
3. NRC 0x13: incorrectMessageLengthOrInvalidFormat
4. NRC 0x31: requestOutOfRange (invalid DTC, record number)

**Service 0x19 Note:** Uses NRC 0x12 due to sub-functions. Typically does not require security (0x33), is not stateful (0x24), or programming-related (0x72).

### Pattern 4: Input/Output Control Service (0x2F)

Typical structure for InputOutputControlByIdentifier service:

1. Service Configuration (sessions, security, addressing)
2. Request/Response Messages (variable length based on control parameters)
3. Behavioral Implementation (I/O control logic, state management, safety checks)

**ISO 14229-1 Reference:** Service 0x2F - InputOutputControlByIdentifier
**AUTOSAR Reference:** Dcm module, DcmDspDidControlAccess configuration

**Control Options (controlParameter):**

- 0x00: returnControlToECU (release control back to ECU)
- 0x01: resetToDefault (set to default value)
- 0x02: freezeCurrentState (maintain current state)
- 0x03: shortTermAdjustment (apply specific control value)

**Request Structure:**

- Byte 0: Service ID = 0x2F
- Bytes 1-2: Data Identifier = 0x[XXXX] (big-endian)
- Byte 3: controlParameter (controlOption)
- Bytes 4+: controlOptionRecord (control state/mask/values, if applicable)

**Response Structure:**

- Byte 0: Service ID = 0x6F (positive response)
- Bytes 1-2: Data Identifier = 0x[XXXX] (echo, big-endian)
- Byte 3: controlParameter (echo)
- Bytes 4+: controlStatusRecord (current status of controlled parameter)

**Behavioral Considerations:**

- Control state machine (active control vs ECU control)
- Safety interlocks and precondition checks
- Control persistence across diagnostic sessions
- Concurrent control request handling
- Hardware/software control arbitration
- Control value validation and range checking

**Error Handling:**

**NRC Priority Order (ISO 14229-1):**

1. NRC 0x7F: serviceNotSupportedInActiveSession (highest priority)
2. NRC 0x33: securityAccessDenied
3. NRC 0x13: incorrectMessageLengthOrInvalidFormat
4. NRC 0x31: requestOutOfRange (invalid control parameter or values)
5. NRC 0x22: conditionsNotCorrect (preconditions not met, safety checks failed)

**Service 0x2F Note:** Does not use NRC 0x12 (no sub-functions), 0x24 (not stateful), or 0x72 (not programming).

### Pattern 5: Routine Control Service (0x31)

Typical structure for RoutineControl service:

1. Service Configuration (sessions, security, addressing)
2. Request/Response Messages (variable length)
3. Behavioral Implementation (routine execution, state machine)

**ISO 14229-1 Reference:** Service 0x31 - RoutineControl
**AUTOSAR Reference:** Dcm module, DcmDspRoutine configuration

**Sub-Functions (routineControlType):**

- 0x01: startRoutine (initiate routine execution)
- 0x02: stopRoutine (terminate routine execution)
- 0x03: requestRoutineResults (retrieve routine results)

**Request Structure:**

- Byte 0: Service ID = 0x31
- Byte 1: Sub-function (routineControlType)
- Bytes 2-3: Routine Identifier = 0x[XXXX] (big-endian)
- Bytes 4+: routineControlOptionRecord (optional parameters)

**Response Structure:**

- Byte 0: Service ID = 0x71 (positive response: 0x31 + 0x40)
- Byte 1: Sub-function (echo)
- Bytes 2-3: Routine Identifier = 0x[XXXX] (echo, big-endian)
- Bytes 4+: routineStatusRecord (status info, results, or confirmation)

**Behavioral Considerations:**

- Routine execution state machine (idle/running/completed/failed)
- Synchronous vs asynchronous routine execution
- Routine pre-conditions and post-conditions
- Routine execution time limits and timeouts
- Concurrent routine request handling
- Routine result persistence and lifetime
- Hardware/software resource allocation
- Safety-critical routine interlocks

**Error Handling:**

**NRC Priority Order (ISO 14229-1):**

1. NRC 0x7F: serviceNotSupportedInActiveSession (highest priority)
2. NRC 0x12: subFunctionNotSupported
3. NRC 0x33: securityAccessDenied
4. NRC 0x13: incorrectMessageLengthOrInvalidFormat
5. NRC 0x24: requestSequenceError (routine already running/not started)
6. NRC 0x31: requestOutOfRange (unsupported routine ID or invalid parameters)
7. NRC 0x22: conditionsNotCorrect (preconditions not met)
8. NRC 0x72: generalProgrammingFailure (routine execution failed)

**Service 0x31 Note:** Uses comprehensive NRC set including 0x12 (sub-functions), 0x24 (stateful execution), and 0x72 (execution failures).

## Quality Standards

### Document Quality Checklist

✅ Feature Summary section present
✅ All requested requirements analyzed (no scope expansion)
✅ Requirements properly grouped by function
✅ Section headers use descriptive titles only (no requirement IDs)
✅ Combined requirement IDs listed in Requirements: field
✅ Complete traceability documented
✅ API details for message format requirements
✅ Error handling with NRC codes ONLY in Behavioral Implementation section
✅ Error handling included ONLY if NRC codes are explicitly mentioned in requirements.csv
✅ NO inferred or assumed NRC codes - only those stated in requirement text
✅ NRC codes verified against ISO 14229-1 Table A.1 (when present in requirements)
✅ NRC priority order matches ISO 14229-1 (clause 7.1, Annex A) when present in requirements
✅ No forbidden file references
✅ Proper markdown formatting
✅ Change summary if updating existing document
✅ Subfunction analysis created only for requirements present in CSV

### Avoid These Issues

❌ Analyzing requirements not requested
❌ Referencing implementation files (.c, .h, .cpp)
❌ Referencing test files or design documents
❌ Separating related requirements (should be grouped)
❌ Missing Feature Summary section
❌ Including requirement IDs in section headers (use descriptive titles only)
❌ Not listing combined requirement IDs in Requirements: field
❌ Incomplete API details for message formats
❌ Adding error handling to Service Configuration or Request/Response Messages sections
❌ Including error handling when NRC codes are not mentioned in requirements.csv
❌ Inferring or assuming NRC codes not explicitly stated in requirement text
❌ Adding "typical" or "standard" NRC codes not in requirements.csv
❌ Incorrect NRC codes not matching ISO 14229-1 Table A.1
❌ Wrong NRC priority order violating ISO 14229-1 (clause 7.1, Annex A prioritization)
❌ Incomplete traceability information
❌ Creating subfunction analysis when requirements are not in CSV

## Markdown Formatting

### Code Blocks

Use fenced code blocks with language identifiers:

````markdown
```c
// C code example
uint8_t data[4];
```
````

### Tables

Use markdown tables for structured data:

```markdown
| Field | Byte | Type | Range |
|-------|------|------|-------|
| SID   | 0    | uint8| 0x22  |
| DID   | 1-2  | uint16| 0x0000-0xFFFF |
```

### Lists

Use consistent list formatting:

```markdown
**Dependencies:**
- ISO 14229-1: Unified Diagnostic Services
- ISO 26262: Functional Safety
- Global variable: g_TestModeStatus
```

### Emphasis

Use standard markdown emphasis:

- **Bold** for field names and labels
- *Italic* for emphasis (use sparingly)
- `Code` for identifiers, values, variables

## Validation Guidelines

### Source Validation

- Verify all information comes from `doc/requirements.csv`
- Do not reference code implementation
- Do not reference test files
- Do not reference design documents
- State "Not specified in requirements" if information is missing
- Create subfunction/service analysis only if requirements are present in CSV

### Completeness Validation

- All requested requirements analyzed
- All mandatory fields present
- Type-specific fields included where required
- Traceability documented
- Error handling documented (if and only if NRC codes are explicitly mentioned in requirements.csv)

### Format Validation

- Proper markdown syntax
- Consistent template usage
- Correct file naming
- Proper section headers
- Valid requirement ID references

### NRC Code Validation

**Apply only when NRC codes are explicitly mentioned in requirements.csv:**

- All NRC codes verified against ISO 14229-1 Table A.1
- NRC hex values are correct (e.g., 0x7F, 0x33, 0x13, 0x31, 0x22, 0x12, 0x24, 0x72)
- NRC priority order follows ISO 14229-1 (clause 7.1, Annex A prioritization rules)
- NRC descriptions match official ISO 14229-1 terminology
- Service-specific NRCs are applicable and correct for the UDS service
- Each NRC validated against the specific service's negative response behavior defined in ISO 14229-1
- Only NRCs applicable to the service are included (e.g., don't use 0x24 requestSequenceError for Service 0x22)
- Common NRCs (0x7F, 0x33, 0x13, 0x31, 0x22) verified for service applicability
- Service-specific NRCs (e.g., 0x12 for sub-function services, 0x24 for stateful services, 0x72 for programming services) used appropriately
- No custom or non-standard NRC codes used without justification

## Best Practices

1. **Start with Feature Summary** - Provide context before details
2. **Group Related Requirements** - Combine for clarity and efficiency
3. **Use Descriptive Section Headers** - Header text only, no requirement IDs (e.g., "## Service Configuration")
4. **List Combined IDs in Requirements Field** - Format: "SWCS_$XX_1, SWCS_$XX_2, SWCS_$XX_3"
5. **Be Specific** - Provide concrete details, not abstractions
6. **Maintain Traceability** - Document all relationships
7. **Follow Templates** - Ensure consistency across documents
8. **Reference Standards** - Cite ISO 14229-1, ISO 26262, MISRA C, AUTOSAR, Bosch guidelines
9. **No NRC Code Inference** - Include NRC codes ONLY if explicitly mentioned in requirements.csv text; never infer, assume, or add "standard" NRC codes. When present, verify against ISO 14229-1 Table A.1
10. **CSV-Only Analysis** - Never supplement from other sources
11. **Stay in Scope** - Analyze only what was requested
12. **Verify Requirements Exist** - Create subfunction analysis only when requirements are documented in requirements.csv
13. **Document Safety Aspects** - Include ASIL levels and safety requirements when specified
14. **Follow Coding Standards** - Reference MISRA C rules and AUTOSAR naming conventions for implementation guidance

## Review

### Quality Checklist

Before finalizing any requirements analysis document, verify the following:

**Completeness:**

- [ ] Feature Summary section present and informative
- [ ] All requested requirements analyzed (no scope expansion)
- [ ] Requirements properly grouped by function
- [ ] Complete traceability documented (parent/child requirements)
- [ ] All mandatory analysis fields populated

**Accuracy:**

- [ ] All [REQUIREMENT_IDS] valid and exist in requirements.csv
- [ ] [REQUIREMENT_TEXT] accurately quoted from CSV
- [ ] Cross-references valid and correct
- [ ] [NRC_CODES] (if present) verified against ISO 14229-1 Table A.1
- [ ] NRC priority order matches ISO 14229-1 (clause 7.1, when NRC codes present in requirements)
- [ ] No inferred or assumed information included

**Format:**

- [ ] Section headers use descriptive titles only (no [REQUIREMENT_IDS])
- [ ] Combined [REQUIREMENT_IDS] listed in Requirements: field
- [ ] Proper markdown formatting applied
- [ ] File naming convention followed: `DCOM_<[DID]>_Requirements.md`
- [ ] Templates followed consistently

**Standards Compliance:**

- [ ] ISO 14229-1 UDS specifications referenced correctly for [SERVICE_IDS] and [NRC_CODES]
- [ ] ISO 26262 functional safety considerations documented with [ASIL_LEVEL]
- [ ] [ASIL_LEVEL] levels specified when applicable (ASIL-A, ASIL-B, ASIL-C, ASIL-D)
- [ ] MISRA C coding guidelines referenced for [IMPLEMENTATION_GUIDANCE]
- [ ] AUTOSAR architecture patterns noted where relevant for [COMPONENT_DESIGN]
- [ ] Bosch-specific standards followed

**Error Handling:**

- [ ] Error handling section present ONLY if [NRC_CODES] in requirements.csv
- [ ] NO error handling added to [SERVICE_CONFIGURATION] or [REQUEST_RESPONSE_MESSAGES] sections
- [ ] [NRC_CODES] verified for [SERVICE_TYPE] applicability (e.g., 0x22 ReadDataByIdentifier)
- [ ] NRC priority order follows ISO 14229-1 Annex A prioritization rules

**Traceability:**

- [ ] [PARENT_REQUIREMENTS] (Traces To) documented
- [ ] [CHILD_REQUIREMENTS] (Traced By) documented
- [ ] [COMPONENT_OWNERSHIP] specified
- [ ] [DEPENDENCIES] clearly listed

### Review Process

**Instructions:** Follow this review process to ensure [REQUIREMENTS_ANALYSIS] quality and completeness. Each [REVIEW_TYPE] validates different aspects of the documentation.

**Peer Review:**

1. **Structural Review** - Verify template compliance and formatting for all [SECTIONS]
2. **Technical Review** - Validate [REQUIREMENT_INTERPRETATION] and technical accuracy
3. **Safety Review** - Confirm [ASIL_REQUIREMENTS] and safety mechanisms documented per ISO 26262
4. **Standards Review** - Check ISO 14229-1, MISRA C, AUTOSAR compliance for [COMPONENT_SPECIFICATIONS]

**Validation Criteria:**

- [REQUIREMENTS_ANALYSIS] matches CSV source exactly
- No [IMPLEMENTATION_DETAILS] leaked into requirements analysis
- All [CROSS_REFERENCES] valid
- [TEMPLATES] applied consistently
- [DOCUMENTATION] readable and maintainable

**Sign-off Requirements:**

- [REQUIREMENTS_ENGINEER] approval
- [SAFETY_ENGINEER] approval (for [ASIL_RATED_REQUIREMENTS])
- [TECHNICAL_LEAD] approval

## Documentation

### Maintenance Guidelines

**Instructions:** Follow these guidelines to maintain and update [REQUIREMENTS_ANALYSIS] documents when [REQUIREMENTS_CSV] changes or [STANDARDS] are updated.

**When to Update:**

- [REQUIREMENTS_CSV] changes (new/modified/deleted [REQUIREMENT_IDS])
- ISO 14229-1 standard updates affecting [SERVICE_SPECIFICATIONS]
- Safety requirements changes ([ASIL_LEVEL] modifications per ISO 26262)
- [TEMPLATE] improvements
- Error corrections in [REQUIREMENT_ANALYSIS]

**Update Process:**

1. **Review** [REQUIREMENTS_CSV] for [CHANGES]
2. **Identify** affected [REQUIREMENTS_ANALYSIS_DOCUMENTS]
3. **Update** document [SECTIONS] impacted by [CHANGES]
4. **Verify** [TRACEABILITY] remains intact
5. **Document** [CHANGES] in analysis document
6. **Re-run** validation checklist
7. **Request** peer review for modified [SECTIONS]

**Version Control:**

- Document significant [CHANGES] with change summary section
- Track [REQUIREMENT_ID] additions/deletions
- Note [TEMPLATE_VERSION] updates
- Record [STANDARD_UPDATES] (ISO 14229-1 revisions)

### Template Evolution

**Instructions:** Propose and implement [TEMPLATE_CHANGES] through a structured review process. Ensure [BACKWARD_COMPATIBILITY] when updating [TEMPLATES].

**Template Updates:**

- **Propose** [TEMPLATE_CHANGES] through structured review process
- **Document** rationale for [TEMPLATE_MODIFICATIONS]
- **Update** existing [DOCUMENTS] when [TEMPLATES] change significantly
- **Maintain** [BACKWARD_COMPATIBILITY] when possible

**Standards Updates:**

- Monitor [ISO_26262], [ISO_14229-1], [MISRA_C], [AUTOSAR] standard revisions
- Update [INSTRUCTION_FILE] when [STANDARDS] change
- Identify [REQUIREMENTS_ANALYSIS_DOCUMENTS] requiring updates
- Schedule bulk updates for major [STANDARD_REVISIONS]

### Reference Materials

**Internal Documents:**

- `doc/requirements.csv` - Single source of truth for all requirements
- `.github/prompts/create-req-analysis.prompt.md` - Execution workflow for requirements analysis agent
- Project coding guidelines and naming conventions

**External Standards:**

- ISO 26262:2018 - Road vehicles - Functional safety
- ISO 14229-1:2020 - Unified Diagnostic Services (UDS) specification
- MISRA C:2012 - Guidelines for the use of the C language in critical systems
- AUTOSAR Release 4.x - Classic Platform specifications
- IREB CPRE - Certified Professional for Requirements Engineering
- Bosch coding guidelines (internal reference)

**Tools:**

- Markdown editors with linting support
- CSV validation tools
- Requirements traceability tools
- Standards compliance checkers
