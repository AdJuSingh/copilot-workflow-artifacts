# Component Test (CT) Generation Instructions for DCOM Test Scripts
## Version 2.0 - Comprehensive Reference Guide

> ** IMPORTANT: This document is a COMPREHENSIVE REFERENCE**  
> All code examples, values, signals, and patterns are **illustrative templates only**.  
> Replace placeholders like `<Service>`, `<DID>`, `<SignalName>`, timing values, etc. with your actual implementation details.

** This is the detailed reference guide. For quick start, see:**
- **[ct-index.instructions.md](./ct-index.instructions.md)** - Quick navigation and lookup
- **[ct00-base-common.instructions.md](./ct00-base-common.instructions.md)** - Common patterns (avoid duplication by referencing this)
- Service-specific instructions (CT_Service_XX files)

---

## Table of Contents
1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Header Section](#header-section)
4. [Include Directives](#include-directives)
5. [Helper Functions](#helper-functions)
6. [Test Case Structure](#test-case-structure)
7. [Test Scenarios](#test-scenarios)
8. [Code Patterns](#code-patterns)
9. [Requirements Traceability](#requirements-traceability)
10. [Service-Specific Guidelines](#service-specific-guidelines)
11. [Best Practices](#best-practices)

---

## 1. Overview

> ** AVOID DUPLICATION:** Common patterns (session setup, security access, signal configuration, timing) are defined in  
> **[ct00-base-common.instructions.md](./ct00-base-common.instructions.md)**.  
> This document provides comprehensive examples and service-specific details. Reference the base file instead of duplicating patterns.

Component Test (CT) scripts are C-based test files for DCOM (Diagnostic Communication) services validation using the CT Generator framework. These tests validate UDS (Unified Diagnostic Services), OBD Classic, OBD on UDS, and ZEV on UDS protocols.

### Purpose
- Validate diagnostic service implementations
- Ensure compliance with ISO 14229 (UDS) and SAE J1979 (OBD)
- Provide comprehensive test coverage (positive, negative, boundary, edge cases)
- Support requirements traceability
- Enable automated test execution

** Quick Navigation**:
- **Index & Lookup**  [ct-index.instructions.md](./ct-index.instructions.md)
- **Common Patterns**  [ct00-base-common.instructions.md](./ct00-base-common.instructions.md) (Use this to avoid duplication!)
- **Service-Specific**  Service files (CT_Service_XX.md)

---

## 2-6. File Structure, Headers, Includes, Helpers & Test Structure

> ** FULL DETAILS IN:** [ct00-base-common.instructions.md - Sections 2-6](./ct00-base-common.instructions.md)

**Quick Reference:**
- **File Naming:** `DCOM_SWT_<ServiceCategory>_<ServiceName>_<Identifier>.c`
- **Headers:** Include test scenarios, requirements traceability, design references
- **Includes:** Mandatory (SwTest_Global.h, Platform_Types.h) + Service-specific (RBAPLCUST_*, Dem.h, etc.)
- **Helpers:** `calculate_key()` for security access
- **Test Template:** `SWTEST void TC_<Service>_<ID>_<Num>(void)`

**Directory:** `TestScripts/Platform_Testscript/DCOM_SWT_Service*.c`

See the base file for complete templates and examples.

---

## 7. Test Scenarios

** For quick coverage checklist**: See [5-dcomsim-component-test-ct-file.instructions.md](./5-dcomsim-component-test-ct-file.instructions.md)

### 7.1 Positive Test Scenarios

#### Standard Read Operation (Service 22)
```c
SWTEST void TC_22_<DID>_01(void)
{
    /* Setup signals with valid values */
    RBMESG_DefineMESGDef(<SignalName>);
    l_<SignalName>.Qualifier = 0x00;  /* Valid */
    l_<SignalName>.<Value> = <ValidValue>;
    RBMESG_SendMESGDef(<SignalName>);
    
    SWT_RunSystemMS(10000);
    
    /* Enter Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Read DID */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID_HI> <DID_LO>", "Read <Description>"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID_HI> <DID_LO> <ExpectedData>", <Length>));
}
```

#### Standard Write Operation (Service 2E)
```c
SWTEST void TC_2E_<DID>_01(void)
{
    uint8 seed[8] = {0};
    
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    HSWFT_DiagDelayMS("UDS", 3750);
    
    /* Security unlock if required */
    [Security access code if needed]
    
    /* Write DID */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "2E <DID_HI> <DID_LO> <Data>", "Write <Description>"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "6E <DID_HI> <DID_LO>", 3));
    
    /* Read back to verify */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID_HI> <DID_LO>", "Read <Description>"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID_HI> <DID_LO> <ExpectedData>", <Length>));
}
```

#### Routine Control (Service 31)
```c
SWTEST void TC_31_<RID>_01(void)
{
    uint8 seed[8] = {0};
    
    /* Setup MESG signals */
    RBMESG_DefineMESGDef(<RequiredSignals>);
    
    SWT_RunSystemMS(10000);
    
    /* Extended session + Security */
    [Session and security setup]
    
    /* Start Routine */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 01 <RID_HI> <RID_LO> <Params>", "Start Routine"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "71 01 <RID_HI> <RID_LO> <Status>", <Length>));
    
    SWT_RunSystemMS(<ExecutionTime>);
    
    /* Request Results */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 03 <RID_HI> <RID_LO>", "Request Routine Results"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "71 03 <RID_HI> <RID_LO> <Results>", <Length>));
    
    /* Stop Routine */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 02 <RID_HI> <RID_LO>", "Stop Routine"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "71 02 <RID_HI> <RID_LO>", <Length>));
}
```

### 7.2 Negative Test Scenarios

#### NRC 0x13: Incorrect Message Length
```c
SWTEST void TC_<Service>_<ID>_<Num>(void)
{
    [Setup session]
    
    /* Too short */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "<Service> <Incomplete>", "NRC 13 - Too short"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F <Service> 13", 3));
    
    /* Too long */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "<Service> <Valid> <Extra>", "NRC 13 - Too long"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F <Service> 13", 3));
}
```

#### NRC 0x31: Request Out of Range
```c
SWTEST void TC_<Service>_<ID>_<Num>(void)
{
    [Setup session]
    
    /* Invalid parameter value */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "<Service> <ID> <InvalidValue>", "NRC 31 - Out of range"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F <Service> 31", 3));
}
```

#### NRC 0x7F: Service Not Supported in Active Session
```c
SWTEST void TC_<Service>_<ID>_<Num>(void)
{
    SWT_RunSystemMS(10000);
    
    /* Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Try service not allowed in default session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "<Service> <Params>", "NRC 7F - Not in session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F <Service> 7F", 3));
}
```

#### NRC 0x33: Security Access Denied
```c
SWTEST void TC_<Service>_<ID>_<Num>(void)
{
    /* Extended session without security unlock */
    SWT_RunSystemMS(10000);
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    HSWFT_DiagDelayMS("UDS", 3750);
    
    /* Try service requiring security */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "<Service> <Params>", "NRC 33 - Security denied"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F <Service> 33", 3));
}
```

#### NRC 0x24: Request Sequence Error
```c
SWTEST void TC_31_<RID>_<Num>(void)
{
    [Setup session and security]
    
    /* Try to stop routine before starting */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 02 <RID>", "Stop without start"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 31 24", 3));
    
    /* Try to get results before starting */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 03 <RID>", "Results without start"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 31 24", 3));
}
```

#### NRC 0x37: Required Time Delay Not Expired
```c
SWTEST void TC_27_01_<Num>(void)
{
    SWT_RunSystemMS(1000);  /* Only 1 second after power-on */
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    
    /* Security access before 5-second delay */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed - Too early"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 27 37", 3));
    
    SWT_RunSystemMS(4500);  /* Wait for remaining time */
    
    /* Now should work */
    uint8 seed[8] = {0};
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed - OK"));
    SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
}
```

### 7.3 Session Management Tests

#### Session Transitions
```c
SWTEST void TC_10_01_<Num>(void)
{
    SWT_RunSystemMS(10000);
    
    /* Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 01", 4));
    
    /* Transition to Extended */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 03", 4));
}
```

#### Session Timeout
```c
SWTEST void TC_10_01_<Num>(void)
{
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 03", 4));
    
    /* Wait for timeout (5000ms + margin) */
    HSWFT_DiagDelayMS("UDS", 6000);
    
    /* Should be back in default session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session After Timeout"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 01", 4));
}
```

#### Tester Present
```c
SWTEST void TC_10_01_<Num>(void)
{
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    
    /* Activate Tester Present */
    HSWFT_DiagActivateTesterPresent(5000);
    
    /* Wait longer than timeout */
    HSWFT_DiagDelayMS("UDS", 5010);
    
    /* Should still be in extended session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 03", 4));
    
    /* Deactivate Tester Present */
    HSWFT_DiagDeactivateTesterPresent();
    
    /* Now it will timeout */
    HSWFT_DiagDelayMS("UDS", 5010);
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session After TP Off"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 01", 4));
}
```

### 7.4 Boundary & Edge Cases

#### Minimum/Maximum Values
```c
SWTEST void TC_22_<DID>_<Num>(void)
{
    RBMESG_DefineMESGDef(<SignalName>);
    
    /* Test minimum value */
    l_<SignalName>.Qualifier = 0x00;
    l_<SignalName>.<Value> = <MinValue>;  /* e.g., 0x0000 */
    RBMESG_SendMESGDef(<SignalName>);
    
    SWT_RunSystemMS(10000);
    [Session setup]
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read at Min"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <MinData>", <Len>));
}

SWTEST void TC_22_<DID>_<Num+1>(void)
{
    RBMESG_DefineMESGDef(<SignalName>);
    
    /* Test maximum value */
    l_<SignalName>.Qualifier = 0x00;
    l_<SignalName>.<Value> = <MaxValue>;  /* e.g., 0xFFFE or 0x3200 */
    RBMESG_SendMESGDef(<SignalName>);
    
    SWT_RunSystemMS(10000);
    [Session setup]
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read at Max"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <MaxData>", <Len>));
}
```

#### Invalid/Not Available Values
```c
SWTEST void TC_22_<DID>_<Num>(void)
{
    RBMESG_DefineMESGDef(<SignalName>);
    
    /* Invalid qualifier */
    l_<SignalName>.Qualifier = 0x00;  /* Invalid */
    l_<SignalName>.<Value> = 0x1234;
    RBMESG_SendMESGDef(<SignalName>);
    
    SWT_RunSystemMS(10000);
    [Session setup]
    
    /* Expect invalid indicator (0xFFFF or similar) */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read Invalid"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> FF FF", <Len>));
}
```

#### Multiple Sequential Operations
```c
SWTEST void TC_22_<DID>_<Num>(void)
{
    [Setup signals and session]
    
    /* First read */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read #1"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <Data>", <Len>));
    SWT_RunSystemMS(100);
    
    /* Second read */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read #2"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <Data>", <Len>));
    SWT_RunSystemMS(100);
    
    /* Third read */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read #3"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <Data>", <Len>));
}
```

### 7.5 OBD-Specific Tests

#### OBD Classic Setup Pattern
```c
SWTEST void TC_01_<PID>_<Num>(void)
{
    RBMESG_DefineMESGDef(<OBD_Signal>);
    
    //Start: OBDclassic_Communication_Standard
    uint8 seed[8] = {0};
    SWT_RunSystemMS(10000);
    
    /* Enter Extended session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Read Active Diagnostics Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 01", 4));
    SWT_RunSystemMS(250);
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(3750);
    
    /* Unlock Security */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed"));
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
    calculate_key(seed, 1);
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 02", key, 2, "Unlock Security"));
    SWT_RunSystemMS(1500);
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "67 02", 2));
    SWT_RunSystemMS(100);
    
    /* Write OBD Communication Standard to OBDclassic */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "2E FD 1B 00", "Write OBD Communication Standard to OBDclassic"));
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "6E FD 1B", 3));
    
    /* Switch to next Power Cycle */
    SWT_SoftwareReset();
    //End  : OBDclassic_Communication_Standard
    
    SWT_RunSystemMS(1000);
    
    /* Set signal value */
    l_<OBD_Signal>.Qualifier = 0x01;
    l_<OBD_Signal>.Value = <TestValue>;
    RBMESG_SendMESGDef(<OBD_Signal>);
    
    /* OBD Request - Physical Addressing */
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "01 <PID>", "PID <PID> in Physical Addressing"));
    SWT_Eval(HSWFT_DiagEvalResponse("OBD", "41 <PID> <Data>", <Len>));
}
```

#### OBD on UDS Setup Pattern
```c
SWTEST void TC_<Service>_<ID>_<Num>(void)
{
    //Start: OBDonUDS_Communication_Standard
    uint8 seed[8] = {0};
    SWT_RunSystemMS(10000);
    
    /* Extended session + Security */
    [Standard UDS session and security setup]
    
    /* Write OBD Communication Standard to OBDonUDS */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "2E FD 1B 01", "Write OBD Communication Standard to OBDonUDS"));
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "6E FD 1B", 3));
    
    /* Switch to next Power Cycle */
    SWT_SoftwareReset();
    //End  : OBDonUDS_Communication_Standard
    
    SWT_RunSystemMS(500);
    
    /* Test execution using OBD channel */
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "<Service> <Sub> <Params>", "Description"));
    SWT_Eval(HSWFT_DiagEvalResponse("OBD", "<Response>", <Len>));
}
```

#### Physical vs Functional Addressing
```c
/* Physical Addressing */
SWT_Eval(HSWFT_DiagSendRequest("OBD", "01 <PID>", "PID in Physical"));
SWT_Eval(HSWFT_DiagEvalResponse("OBD", "41 <PID> <Data>", <Len>));

/* Functional Addressing */
SWT_Eval(HSWFT_DiagSendRequest("OBD_FUNC", "01 <PID>", "PID in Functional"));
SWT_Eval(HSWFT_DiagEvalResponse("OBD_FUNC", "41 <PID> <Data>", <Len>));
```

---

## 8. Code Patterns

> ** FULL PATTERNS IN:** [ct00-base-common.instructions.md - Section 7](./ct00-base-common.instructions.md#7-code-patterns)  
> This section is **condensed**. See the base file for complete code examples and variations.

**Standard Patterns:**
- **Session Setup:** Default (10 01), Extended (10 03) - includes verification with DID F186
- **Security Access:** Seed request (27 01/03)  Calculate key  Send key (27 02/04)
- **Signal Setup:** Define  Set values  Send  Wait 10000ms
- **Timing:** Init=10000ms, Delay=250ms, Timeout=3750ms/6000ms
- **DTC Management:** Report  Clear (14 FF FF FF + 10000ms wait)  Read (19 01/02)

See base file for full code templates.

---

## 9. Requirements Traceability

### Format in Header
```c
 * Requirements Traceability:
 *   SWCS_$<Service>_<ID>: <Description>
 *   SWCS_$<Service>_<ID+1>: <Description>
 *   ...
```

### Examples

#### Service 22 (ReadDataByIdentifier)
```c
 * Requirements Traceability:
 *   SWCS_$22_12: Parent requirement - DID 0xFD00 Wheel Speed Information
 *   SWCS_$22_13: Description section
 *   SWCS_$22_14: Core functional behavior - 4 wheels with validity check
 *   SWCS_$22_15: Diagnostic sessions - Default/Extended (DCM enforced)
 *   SWCS_$22_16: Security level - None required
 *   SWCS_$22_17: Addressing mode - Physical only (DCM enforced)
 *   SWCS_$22_18: Request format - 0x22 + 0xFD00 (DCM parsed)
 *   SWCS_$22_19: Response format - 0x62 + 0xFD00 + 8 bytes data
 *   SWCS_$22_20: Data format - 1/128 m/s resolution, 0xFFFF invalid
 *   SWCS_$22_21: Behavior section
 *   SWCS_$22_22: Message-Concept data sources - RBSSPWSS_WheelSpeed_FL/FR/RL/RR
```

### Test Case Comments
```c
/*
  @testlists Service22_WheelSpeedInformation
  TC_22_FD00_01: Read wheel speed information in Default Session with all valid speeds
  Tests SWCS_$22_14, SWCS_$22_15, SWCS_$22_19, SWCS_$22_20, SWCS_$22_22
*/
```

---

## 10. Service-Specific Guidelines

### Service 10: Diagnostic Session Control

**Key Points:**
- Test all session types (Default=0x01, Extended=0x03, Programming=0x02)
- Verify session timeout behavior (5 seconds typical)
- Test tester present functionality
- Verify session transitions
- Check vehicle speed interlocks

**Standard Response:**
```
Request:  10 01
Response: 50 01 00 32 01 F4
         [Service] [Session] [P2 High] [P2 Low] [P2* High] [P2* Low]
```

### Service 14: ClearDiagnosticInformation

**Key Points:**
- Test in Default and Extended sessions
- Test with DTC group numbers (0xFFFFFF for all)
- Verify NRC 0x13 (length), NRC 0x31 (invalid group)
- Allow 10-second delay for NvM write operations
- Verify DTCs are actually cleared

**Standard Flow:**
```c
SWT_Eval(HSWFT_DiagSendRequest("UDS", "14 FF FF FF", "Clear all DTC"));
SWT_RunSystemMS(10000);  /* Important: Wait for NvM */
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "54", 1));
```

### Service 19: Read DTC Information

**Key Points:**
- Multiple subfunctions (0x01-0x1A, 0x42, 0x55, 0x56)
- Test physical and functional addressing
- Verify DTC status masks
- Test freeze frame data
- Extended data records

**Common Subfunctions:**
- 0x01: Number of DTCs by status mask
- 0x02: DTC by status mask
- 0x04: Freeze frame data
- 0x06: Extended data record
- 0x1A: Supported DTC extended data records

### Service 22: ReadDataByIdentifier

**Key Points:**
- Test in allowed sessions
- Verify data format (byte order, resolution, scaling)
- Test with valid/invalid signal qualifiers
- Test minimum/maximum/invalid values
- Verify 0xFFFF or similar for invalid data
- Test multiple DIDs in single request (if supported)

**Standard Pattern:**
```
Request:  22 FD 00
Response: 62 FD 00 [Data Bytes...]
```

### Service 27: SecurityAccess

**Key Points:**
- Test power-on delay (typically 5 seconds)
- Test in Extended session only
- Verify seed generation (must be non-zero)
- Test correct and incorrect key
- Test level 1 (EOL) and level 2 (Service)
- Test seed timeout

**Standard Flow:**
```c
SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed"));
SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
calculate_key(seed, 1);
SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 02", key, 2, "Send Key"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "67 02", 2));
```

### Service 28: CommunicationControl

**Key Points:**
- Test in Extended session only
- Requires security access
- Test subfunctions: 0x00 (EnableRx/EnableTx), 0x01 (EnableRx/DisableTx), etc.
- Test communication types: 0x01 (Normal), 0x02 (Network Management), 0x03 (Both)
- Verify NRC 0x7F (service not supported in active session)

### Service 2E: WriteDataByIdentifier

**Key Points:**
- Test in Extended session
- May require security access
- Verify write followed by read-back
- Test NRC 0x31 (request out of range)
- Test NRC 0x13 (incorrect message length)
- Test session persistence after write

**Standard Pattern:**
```c
SWT_Eval(HSWFT_DiagSendRequest("UDS", "2E FD 1A 01", "Write Value"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "6E FD 1A", 3));
SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 FD 1A", "Read Back"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 FD 1A 01", 4));
```

### Service 31: RoutineControl

**Key Points:**
- Test subfunctions: 0x01 (Start), 0x02 (Stop), 0x03 (RequestResults)
- Test sequence: Start  Results  Stop
- Test NRC 0x24 (request sequence error)
- Test input parameter validation
- Requires Extended session and security
- Test routine timeout behavior

**Standard Pattern:**
```c
/* Start */
SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 01 F0 03 [Params]", "Start Routine"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "71 01 F0 03 [Status]", Length));

/* Get Results */
SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 03 F0 03", "Request Results"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "71 03 F0 03 [Results]", Length));

/* Stop */
SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 02 F0 03", "Stop Routine"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "71 02 F0 03", Length));
```

### OBD Services

**OBD Classic (Service 01, 02, 03, 04, 07, 09, 0A):**
- Requires OBD mode activation via DID 0xFD1B write
- Requires power cycle after mode switch
- Test physical and functional addressing
- Response format: Request + 0x40

**OBD on UDS (Service 14, 19, 22):**
- Similar to OBD Classic setup
- Uses UDS services with OBD-specific DIDs
- DID range: 0xF400-0xF4FF (PIDs), 0xF800-0xF8FF (InfoTypes)

---

## 11. Best Practices

** For quality checklist and common mistakes**: See [5-dcomsim-component-test-ct-file.instructions.md](./5-dcomsim-component-test-ct-file.instructions.md)

### 11.1 Code Quality

1. **Consistent Formatting**
   - Use consistent indentation (tabs or spaces)
   - Align similar statements
   - Keep line length reasonable (< 100 characters)

2. **Clear Comments**
   - Explain test purpose at function level
   - Comment complex logic
   - Use section markers for test phases

3. **Meaningful Names**
   - Use descriptive test case numbers
   - Clear description strings in diagnostic commands
   - Consistent naming across similar tests

### 11.2 Test Design

1. **Comprehensive Coverage**
   - Positive scenarios (happy path)
   - Negative scenarios (all applicable NRCs)
   - Boundary conditions (min/max values)
   - Edge cases (invalid, not available)
   - Session management
   - Timing requirements

2. **Independent Tests**
   - Each test should be self-contained
   - Initialize all required state
   - Don't rely on execution order
   - Clean up if needed (though framework usually handles this)

3. **Proper Timing**
   ```c
   SWT_RunSystemMS(10000);  /* System initialization */
   SWT_RunSystemMS(250);    /* Between commands */
   SWT_RunSystemMS(3750);   /* Before session timeout */
   SWT_RunSystemMS(10000);  /* For NvM operations */
   ```

4. **Signal Handling**
   - Always define MESG before use
   - Set qualifier appropriately
   - Send signals before reading
   - Allow stabilization time (10000ms typical)

### 11.3 Error Handling

1. **Expected NRCs**
   ```c
   /* Always test expected negative responses */
   SWT_Eval(HSWFT_DiagSendRequest("UDS", "<Invalid>", "Description"));
   SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F <Service> <NRC>", 3));
   ```

2. **Common NRCs to Test**
   - 0x13: incorrectMessageLengthOrInvalidFormat
   - 0x24: requestSequenceError
   - 0x31: requestOutOfRange
   - 0x33: securityAccessDenied
   - 0x37: requiredTimeDelayNotExpired
   - 0x7F: serviceNotSupportedInActiveSession

### 11.4 Documentation

1. **Test Case Documentation**
   ```c
   /*
     @testlists <Category>
     <Clear description of what is being tested>
     <Which requirements are covered>
   */
   ```

2. **Inline Comments**
   - Explain setup steps
   - Clarify expected behavior
   - Note timing requirements
   - Document special conditions

3. **Header Documentation**
   - List all test scenarios
   - Reference requirements
   - Include design documents
   - Note tool version if auto-generated

### 11.5 Maintenance

1. **Version Control**
   - Include tool version in header
   - Date stamp generation
   - Track requirement versions

2. **Modularity**
   - Reuse helper functions
   - Consistent patterns across tests
   - Feature switches for variants

3. **Readability**
   - Group related tests
   - Use section comments
   - Consistent ordering (positive first, then negative)

---

## Appendix A: Common Diagnostic Channels

```c
"UDS"       - Standard UDS channel (physical addressing)
"OBD"       - OBD channel (physical addressing)
"OBD_FUNC"  - OBD channel (functional addressing)
```

## Appendix B: Standard NRC Codes

| NRC  | Name | Description |
|------|------|-------------|
| 0x10 | generalReject | General reject |
| 0x11 | serviceNotSupported | Service not supported |
| 0x12 | subfunctionNotSupported | Subfunction not supported |
| 0x13 | incorrectMessageLengthOrInvalidFormat | Length or format error |
| 0x14 | responseTooLong | Response too long |
| 0x21 | busyRepeatRequest | Server busy |
| 0x22 | conditionsNotCorrect | Conditions not correct |
| 0x24 | requestSequenceError | Wrong sequence |
| 0x31 | requestOutOfRange | Parameter out of range |
| 0x33 | securityAccessDenied | Security not unlocked |
| 0x35 | invalidKey | Wrong security key |
| 0x36 | exceedNumberOfAttempts | Too many key attempts |
| 0x37 | requiredTimeDelayNotExpired | Wait time not expired |
| 0x7E | subfunctionNotSupportedInActiveSession | Subfunction blocked in session |
| 0x7F | serviceNotSupportedInActiveSession | Service blocked in session |

## Appendix C: Standard UDS Services

| Service | Name | Description |
|---------|------|-------------|
| 0x10 | DiagnosticSessionControl | Change diagnostic session |
| 0x11 | ECUReset | Reset ECU |
| 0x14 | ClearDiagnosticInformation | Clear DTCs |
| 0x19 | ReadDTCInformation | Read DTC status |
| 0x22 | ReadDataByIdentifier | Read data by DID |
| 0x27 | SecurityAccess | Unlock security level |
| 0x28 | CommunicationControl | Control communication |
| 0x2E | WriteDataByIdentifier | Write data by DID |
| 0x2F | InputOutputControlByIdentifier | Control I/O |
| 0x31 | RoutineControl | Execute routine |
| 0x3E | TesterPresent | Keep session alive |
| 0x85 | ControlDTCSetting | Enable/disable DTC setting |

## Appendix D: Typical Timing Values

```c
/* System initialization */
10000 ms  - Initial system stabilization

/* Session management */
50 ms     - P2 timeout (standard)
5000 ms   - P2* extended timeout
5000 ms   - Session timeout (S3)
250 ms    - Delay after session change

/* Security access */
5000 ms   - Power-on delay before security access
1000 ms   - Between seed request and key send

/* DTC operations */
10000 ms  - After clear DTC (NvM write time)
500 ms    - After DTC report

/* General */
100 ms    - Between diagnostic commands
3750 ms   - Wait time to test timeout (just before 5s)
6000 ms   - Wait time to ensure timeout occurred
```

---

## Quick Reference Summary

> ** REMEMBER:** All examples in this document are **reference templates only**. Always replace placeholder values with actual project-specific details.

**Avoid Duplication - Use These References:**
-  **Common Patterns**  [ct00-base-common.instructions.md](./ct00-base-common.instructions.md) (Session, security, signals, timing)
-  **Quick Lookup**  [ct-index.instructions.md](./ct-index.instructions.md) (Navigation and cross-reference)
-  **Service-Specific**  Service instruction files (CT_Service_XX.md)

**Getting Started:**
-  Navigation hub: [ct-index.instructions.md](./ct-index.instructions.md)
-  Example files: `rb\as\ms\core\app\dcom\RBDcmSim\DCOMSIM\CT_Generator\tst\TestScripts`
-  File pattern: `DCOM_SWT_Service<Hex>_<Name>.c`

**Key Sections:**
- Section 7: Complete test scenario patterns with code examples (see also Base file Section 7)
- Section 8: Code patterns (cross-referenced to Base file to avoid duplication)
- Section 8: Reusable code patterns (session, security, signals, timing)
- Section 10: Service-specific implementation guidelines
- Appendix B: All NRC codes reference
- Appendix D: Standard timing values

**Test Coverage:** 15-20+ tests minimum (5+ positive, 6+ negative, 3+ session, 3+ boundary)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0 | 2025-11-16 | GitHub Copilot | Optimized as reference guide with cross-references to avoid duplication |
| 2.0 | 2025-11-12 | GitHub Copilot | Comprehensive instruction set created from pattern analysis |
| 1.4.9 | 2024-11-07 | CT Generator | Last tool version reference found |

---

## Contact & Support

For questions or issues with these instructions:
1. Start with [ct-index.instructions.md](./ct-index.instructions.md) for navigation
2. Reference [ct00-base-common.instructions.md](./ct00-base-common.instructions.md) for common patterns
3. Review existing test files in Platform_Testscript folder

---

**END OF COMPREHENSIVE REFERENCE GUIDE**

> **Remember:** This is a reference document with example templates. Always adapt examples to your specific requirements.
3. Check tool documentation for CT Generator
4. Consult requirements documents in doc/requirements/
5. Review design documents in doc/design/

---

**END OF INSTRUCTIONS**
