# Service 22: ReadDataByIdentifier - CT Instructions

> ** IMPORTANT: This document is a REFERENCE TEMPLATE**  
> All specific examples (DIDs, signals, values) are **illustrative only**.  
> Replace `<DID>`, `<DIDName>`, signal names, and test values with your actual implementation details.

## Overview

Service 22 (ReadDataByIdentifier) is used to read data from the ECU using Data Identifiers (DIDs).

**Standard:** ISO 14229-1 (UDS)  
**Service ID:** 0x22  
**Response ID:** 0x62

---

## Key Concepts

### Data Identifiers (DIDs)
- **0xF000-0xF0FF**: Network configuration
- **0xF100-0xF18F**: Vehicle manufacturer specific
- **0xF190-0xF19F**: Vehicle information (VIN, etc.)
- **0xF1A0-0xF1EF**: Vehicle manufacturer specific
- **0xF1F0-0xF1FF**: System supplier specific
- **0xFD00-0xFDFF**: Custom application data

### Data Format
- Data may require signal validity checks
- Invalid data typically represented as 0xFFFF or 0xFF
- Resolution and scaling defined per DID
- Byte order (MSB/LSB) defined per DID

---

## Standard Request/Response Format

### Request Format
```
[Service ID] [DID High] [DID Low]
Example: 22 <DID_High> <DID_Low> (e.g., "22 FD 00" for DID 0xFD00)
```

### Positive Response Format
```
[Response ID] [DID High] [DID Low] [Data Bytes...]
Example: 62 <DID_High> <DID_Low> <Data_Byte_1> <Data_Byte_2> ...
         (e.g., "62 FD 00 19 00 19 00 19 00 19 00" for 8 bytes of data)
```

### Common Negative Response Codes (NRCs)
- **0x13**: IncorrectMessageLengthOrInvalidFormat
- **0x31**: RequestOutOfRange - DID not supported
- **0x33**: SecurityAccessDenied - Security level required
- **0x7F**: ServiceNotSupportedInActiveSession

---

## Test Scenarios

> ** NOTE:** All code examples below use **DID 0xFD00 (Wheel Speed)** as a reference.  
> Replace signal names (`RBSSPWSS_WheelSpeed_*`), DIDs, values, and requirement IDs with your specific implementation.

### 1. Positive Scenarios

#### TC_22_<DID>_01: Read Valid Data in Default Session
```c
/*
  @testlists Service22_<DIDName>
  TC_22_<XXXX>_01: Read <your data description> with valid values
  Tests SWCS_$22_XX, SWCS_$22_YY [Replace with actual requirement IDs]
  
  EXAMPLE USES: DID 0xFD00, Wheel Speed signals - REPLACE WITH YOUR DID/SIGNALS
*/
SWTEST void TC_22_<XXXX>_01(void)  /* Replace <XXXX> with your DID */
{
    /* Setup signal values - EXAMPLE: Replace with your actual signals */
    RBMESG_DefineMESGDef(<YourSignal_1>);  /* Define all required input signals */
    RBMESG_DefineMESGDef(<YourSignal_2>);
    /* ... define all signals needed for your DID ... */
    
    l_<YourSignal_1>.<Field1> = <ValidValue1>;  /* Set to valid test values */
    l_<YourSignal_1>.<Field2> = <ValidValue2>;  /* e.g., Qualifier = 0x00 for valid */
    l_<YourSignal_2>.<Field1> = <ValidValue1>;
    /* ... set all signal fields ... */
    
    RBMESG_SendMESGDef(<YourSignal_1>);  /* Send all defined signals */
    RBMESG_SendMESGDef(<YourSignal_2>);
    /* ... send all signals ... */
    
    SWT_RunSystemMS(10000);  /* Allow system stabilization */
    
    /* Enter Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Read DID - Replace with your DID and expected response */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID_High> <DID_Low>", "Read <YourDataName>"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID_High> <DID_Low> <ExpectedData>", <Length>));
}
```

#### TC_22_<DID>_02: Read in Extended Session
```c
/*
  @testlists Service22_<DIDName>
  TC_22_<XXXX>_02: Read <your data> in Extended Session
  Tests SWCS_$22_XX [Replace with actual requirement ID]
  
  PATTERN: Use this when DID is accessible in Extended Diagnostic Session
*/
SWTEST void TC_22_<XXXX>_02(void)  /* Replace <XXXX> with your DID */
{
    /* Setup signals - Same pattern as TC_01, different test values */
    RBMESG_DefineMESGDef(<YourSignal_1>);
    /* ... define your signals ... */
    
    l_<YourSignal_1>.<Field> = <TestValue>;  /* Use different values than TC_01 */
    /* ... set signal values ... */
    
    RBMESG_SendMESGDef(<YourSignal_1>);
    /* ... send signals ... */
    
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    HSWFT_DiagDelayMS("UDS", 3750);  /* Session timing per requirements */
    
    /* Read DID - Replace with your DID and expected response */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID_High> <DID_Low>", "Read <YourData>"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID_High> <DID_Low> <ExpectedData>", <Length>));
}
```

### 2. Boundary & Edge Cases

#### TC_22_<DID>_03: Minimum Value
```c
/*
  @testlists Service22_<DIDName>
  TC_22_<XXXX>_03: Read <your data> at minimum valid value
  Tests SWCS_$22_XX [Replace with actual requirement ID]
  
  PATTERN: Test lower boundary of data range
*/
SWTEST void TC_22_<XXXX>_03(void)  /* Replace <XXXX> with your DID */
{
    /* Define and setup signals with MINIMUM valid values */
    RBMESG_DefineMESGDef(<YourSignal>);
    /* ... define signals ... */
    
    l_<YourSignal>.<ValidityField> = <ValidIndicator>;  /* e.g., 0x00 = valid */
    l_<YourSignal>.<DataField> = <MinimumValue>;  /* Set to minimum per spec */
    /* ... set to minimum values ... */
    
    RBMESG_SendMESGDef(<YourSignal>);
    /* ... send signals ... */
    
    SWT_RunSystemMS(10000);
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read <Data> - Min"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <MinExpectedBytes>", <Len>));
}
```

#### TC_22_<DID>_04: Maximum Value
```c
/*
  @testlists Service22_<DIDName>
  TC_22_<XXXX>_04: Read <your data> at maximum valid value
  Tests SWCS_$22_XX [Replace with actual requirement ID]
  
  PATTERN: Test upper boundary of data range (often 0xFFFE, 0xFFFF reserved for invalid)
*/
SWTEST void TC_22_<XXXX>_04(void)  /* Replace <XXXX> with your DID */
{
    /* Define and setup signals with MAXIMUM valid values */
    RBMESG_DefineMESGDef(<YourSignal>);
    /* ... define signals ... */
    
    l_<YourSignal>.<ValidityField> = <ValidIndicator>;  /* Valid qualifier */
    l_<YourSignal>.<DataField> = <MaximumValue>;  /* Max per spec (often 0xFFFE) */
    /* ... set to maximum valid values ... */
    
    RBMESG_SendMESGDef(<YourSignal>);
    /* ... send signals ... */
    
    SWT_RunSystemMS(10000);
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read <Data> - Max"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <MaxExpectedBytes>", <Len>));
}
```

#### TC_22_<DID>_05: Invalid/Not Available Data
```c
/*
  @testlists Service22_<DIDName>
  TC_22_<XXXX>_05: Read <your data> with invalid qualifier/status
  Tests SWCS_$22_XX [Replace with actual requirement ID]
  
  PATTERN: Test how DID responds when input signals are invalid/unavailable
  Expected: Often returns 0xFFFF or 0xFF per signal to indicate "not available"
*/
SWTEST void TC_22_<XXXX>_05(void)  /* Replace <XXXX> with your DID */
{
    /* Define signals and set to INVALID state */
    RBMESG_DefineMESGDef(<YourSignal>);
    /* ... define signals ... */
    
    l_<YourSignal>.<ValidityField> = <InvalidIndicator>;  /* e.g., 0x01 = invalid */
    l_<YourSignal>.<DataField> = <AnyValue>;  /* Data value doesn't matter if invalid */
    /* ... set validity to invalid ... */
    
    RBMESG_SendMESGDef(<YourSignal>);
    /* ... send signals ... */
    
    SWT_RunSystemMS(10000);
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Expect invalid indicator per spec (commonly 0xFFFF or 0xFF per field) */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read <Data> - Invalid"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <InvalidBytes>", <Len>));
}
```

### 3. Negative Scenarios

#### TC_22_<DID>_06: NRC 0x31 - Unsupported DID
```c
/*
  @testlists Service22_<DIDName>
  TC_22_<XXXX>_06: Request unsupported/invalid DID
  Tests NRC 0x31: RequestOutOfRange
  
  PATTERN: Verify proper negative response for non-existent DIDs
*/
SWTEST void TC_22_<XXXX>_06(void)  /* Use a base test case number */
{
    SWT_RunSystemMS(10000);
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Request unsupported DID - Choose a DID known to NOT be implemented */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <Unsupported_DID>", "Read Unsupported DID"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 22 31", 3));  /* NRC 0x31 */
}
```

#### TC_22_<DID>_07: NRC 0x13 - Incorrect Message Length
```c
/*
  @testlists Service22_<DIDName>
  TC_22_<XXXX>_07: Send request with incorrect message length
  Tests NRC 0x13: IncorrectMessageLengthOrInvalidFormat
  
  PATTERN: Standard Service 22 request = 3 bytes [22][DID_High][DID_Low]
*/
SWTEST void TC_22_<XXXX>_07(void)
{
    SWT_RunSystemMS(10000);
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Too short - Missing DID low byte */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID_High>", "Read DID - Too short"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 22 13", 3));  /* NRC 0x13 */
    
    /* Too long - Extra bytes after DID */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID_High> <DID_Low> 00", "Read DID - Too long"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 22 13", 3));  /* NRC 0x13 */
}
```

#### TC_22_<DID>_08: NRC 0x7F - Wrong Session
```c
/*
  @testlists Service22_<DIDName>
  TC_22_<XXXX>_08: Read DID only available in specific session while in wrong session
  Tests NRC 0x7F: ServiceNotSupportedInActiveSession
  
  PATTERN: Use when DID is restricted to Extended/Programming session only
  NOTE: Skip this test if your DID is available in all sessions
*/
SWTEST void TC_22_<XXXX>_08(void)
{
    SWT_RunSystemMS(10000);
    
    /* Stay in Default Session (or use different session than required) */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Try to read DID requiring different session (e.g., Extended) */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read DID in wrong session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 22 7F", 3));  /* NRC 0x7F */
}
```

### 4. Sequential Operations

#### TC_22_<DID>_09: Multiple Sequential Reads
```c
/*
  @testlists Service22_<DIDName>
  TC_22_<XXXX>_09: Multiple sequential reads of the same DID
  Tests SWCS_$22_XX [Replace with actual requirement ID]
  
  PATTERN: Verify repeated reads return consistent results
*/
SWTEST void TC_22_<XXXX>_09(void)  /* Replace <XXXX> with your DID */
{
    /* Setup signals with stable values */
    RBMESG_DefineMESGDef(<YourSignal>);
    /* ... define signals ... */
    
    l_<YourSignal>.<Field> = <StableValue>;  /* Use consistent value */
    /* ... set signal values ... */
    
    RBMESG_SendMESGDef(<YourSignal>);
    /* ... send signals ... */
    
    SWT_RunSystemMS(10000);
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* First read */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read #1"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <ExpectedData>", <Len>));
    SWT_RunSystemMS(100);
    
    /* Second read - Should return same data */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read #2"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <ExpectedData>", <Len>));
    SWT_RunSystemMS(100);
    
    /* Third read - Verify consistency */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 <DID>", "Read #3"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 <DID> <ExpectedData>", <Len>));
}
```

---

## Test File Template

```c
/********************************************************************************
 * COMPONENT TEST - Service 22 - ReadDataByIdentifier - DID 0x<XXXX>
 * FILE: DCOM_SWT_Service22_<DIDName>.c
 * 
 * REPLACE PLACEHOLDERS:
 * - <XXXX>: Your DID hex value (e.g., FD00, F190)
 * - <DIDName>: Descriptive name (e.g., WheelSpeed, VehicleVIN)
 * - <DataName>: Data identifier name for include file
 * 
 * TEST SCENARIOS COVERED:
 * ========================
 * 1. Positive Scenarios:
 *    - Read valid data in Default Session (if supported)
 *    - Read valid data in Extended Session (if supported)
 *    - Multiple sequential reads (verify consistency)
 * 
 * 2. Negative Scenarios:
 *    - NRC 0x13: IncorrectMessageLengthOrInvalidFormat
 *    - NRC 0x31: RequestOutOfRange (unsupported DID)
 *    - NRC 0x7F: ServiceNotSupportedInActiveSession (if session-specific)
 *    - NRC 0x33: SecurityAccessDenied (if security required)
 * 
 * 3. Boundary & Edge Cases:
 *    - Minimum value (lower boundary per spec)
 *    - Maximum value (upper boundary, often 0xFFFE)
 *    - Invalid/Not Available data (typically 0xFFFF or 0xFF)
 * 
 * 4. Data Format Validation:
 *    - Byte order verification (MSB/LSB per spec)
 *    - Resolution and scaling (per DID definition)
 *    - Qualifier handling (valid vs. invalid indicators)
 * 
 * Requirements Traceability:
 *   SWCS_$22_XX: Parent requirement - DID 0x<XXXX> <Description>
 *   [List all requirements covered by this test file]
 ********************************************************************************/

#include "SwTest_Global.h"
#include "TestEnvironment_Base.h"
#include "Platform_Types.h"
#include "Compiler.h"
#include "Std_Types.h"
#include "RBAPLCUST_Global.h"
#include "RBAPLCUST_Config.h"
#include "RBAPLCUST_Interface.h"
#include "RBAPLCUST_RDBI_<DataName>.h"  /* Replace <DataName> with actual header */

/* ===== Test cases implementation here ===== */
/* Use patterns from sections above, replacing all placeholders */
```

---

## Key Implementation Guidelines

1. **Signal Setup** - Always use MESG framework to define and send input signals before reading DID
2. **Stabilization Time** - Allow 10000ms after signal setup for system stabilization (adjust per requirements)
3. **Boundary Testing** - Test minimum, maximum, and invalid values per your DID specification
4. **Data Format Verification** - Check byte order (MSB/LSB), resolution, and scaling per DID definition
5. **Qualifier Handling** - Test both valid and invalid signal qualifiers/status indicators
6. **Session Requirements** - Verify DID accessibility in Default/Extended/Programming sessions per spec
7. **Sequential Reads** - Test multiple reads to verify consistent and repeatable responses
8. **Expected Values** - Calculate expected response bytes based on signal values and DID encoding rules

> **Remember:** All numeric values (DIDs, data values, timing) shown in examples are references only.  
> Consult your project's DID specification document for actual values.

---

## Related Services

- **Service 0x2E**: WriteDataByIdentifier - Write DIDs
- **Service 0x10**: DiagnosticSessionControl - Session management
- **Service 0x27**: SecurityAccess - Some DIDs require security

---

## References

- [Base Common Instructions](./ct00-base-common.instructions.md)
- [Master Index](./ct-index.instructions.md)

---

**END OF SERVICE 22 INSTRUCTIONS**
