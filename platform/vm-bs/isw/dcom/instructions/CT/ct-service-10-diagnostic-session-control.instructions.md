# Service 10: Diagnostic Session Control - CT Instructions

##  ESSENTIALS

**Service:** 0x10 DiagnosticSessionControl | **Response:** 0x50  
**Standard:** ISO 14229-1 (UDS)  
**Sessions:** 0x01 (Default), 0x03 (Extended), 0x02 (Programming)  
**Timing:** P2=50ms, P2*=5000ms, S3 timeout=5000ms  
** Patterns:** [ct00-base-common.instructions.md - Section 7.1](./ct00-base-common.instructions.md#71-session-management-patterns)

> ** TEMPLATE:** Replace session types, timing values, conditions with actual specs.

---

##  SESSION BEHAVIOR

**Session Types:**
- **0x01** - Default Session (diagnostic default)
- **0x02** - Programming Session (ECU programming)
- **0x03** - Extended Session (advanced diagnostics)
- **0x04-0x7F** - OEM-specific

**Key Behaviors:**
- Auto-revert to Default after S3 timeout (5000ms)
- Tester Present (0x3E) keeps session alive
- Vehicle speed interlocks may apply
- Security access lost on transitions

---

##  REQUEST/RESPONSE FORMAT

### **Request**
```
[Service ID] [Session Type]
10 01  - Default Session
10 03  - Extended Session
```

### **Positive Response**
```
[Response ID] [Session] [P2 High] [P2 Low] [P2* High] [P2* Low]
50 01 00 32 01 F4  - Default, P2=50ms, P2*=500ms
```

### **Common NRCs**
- **0x12** - SubFunctionNotSupported (invalid session type)
- **0x13** - IncorrectMessageLengthOrInvalidFormat
- **0x22** - ConditionsNotCorrect (vehicle conditions not met)
- **0x7F** - ServiceNotSupportedInActiveSession

---

##  TEST SCENARIOS

### **1. Positive Scenarios**

#### TC_10_01: Enter Default Session
```c
/*
  @testlists Service10_DiagnosticSessionControl
  TC_10_01: Enter Default Session and verify response with timing parameters
  Tests SWCS_$10_01, SWCS_$10_02
*/
SWTEST void TC_10_01(void)
{
    SWT_RunSystemMS(10000);
    
    /* Enter Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Verify session via DID F186 */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Read Active Diagnostics Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 01", 4));
}
```

#### TC_10_02: Enter Extended Session
```c
/*
  @testlists Service10_DiagnosticSessionControl
  TC_10_02: Enter Extended Session and verify response
  Tests SWCS_$10_01, SWCS_$10_03
*/
SWTEST void TC_10_02(void)
{
    SWT_RunSystemMS(10000);
    
    /* Enter Default Session first */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Enter Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Verify session via DID F186 */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Read Active Diagnostics Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 03", 4));
}
```

### 2. Session Transition Tests

#### TC_10_03: Transition Between Sessions
```c
/*
  @testlists Service10_DiagnosticSessionControl
  TC_10_03: Test transition from Default to Extended and back to Default
  Tests SWCS_$10_04, SWCS_$10_05
*/
SWTEST void TC_10_03(void)
{
    SWT_RunSystemMS(10000);
    
    /* Start in Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 01", 4));
    
    /* Transition to Extended */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Enter Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 03", 4));
    
    /* Return to Default */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Return to Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 01", 4));
}
```

### 3. Session Timeout Tests

#### TC_10_04: Extended Session Timeout
```c
/*
  @testlists Service10_DiagnosticSessionControl
  TC_10_04: Verify Extended Session times out to Default after S3 period
  Tests SWCS_$10_06, SWCS_$10_07
*/
SWTEST void TC_10_04(void)
{
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Enter Extended Session"));
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

#### TC_10_05: Tester Present Prevents Timeout
```c
/*
  @testlists Service10_DiagnosticSessionControl
  TC_10_05: Verify Tester Present keeps Extended Session active beyond S3 timeout
  Tests SWCS_$10_08, SWCS_$10_09
*/
SWTEST void TC_10_05(void)
{
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Enter Extended Session"));
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

### 4. Negative Scenarios

#### TC_10_06: NRC 0x12 - Invalid Session Type
```c
/*
  @testlists Service10_DiagnosticSessionControl
  TC_10_06: Request unsupported session type
  Tests SWCS_$10_10 - NRC 0x12: SubFunctionNotSupported
*/
SWTEST void TC_10_06(void)
{
    SWT_RunSystemMS(10000);
    
    /* Enter Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Request invalid session type */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 05", "Request Invalid Session Type"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 10 12", 3));
}
```

#### TC_10_07: NRC 0x13 - Incorrect Message Length
```c
/*
  @testlists Service10_DiagnosticSessionControl
  TC_10_07: Send request with incorrect message length
  Tests SWCS_$10_11 - NRC 0x13: IncorrectMessageLengthOrInvalidFormat
*/
SWTEST void TC_10_07(void)
{
    SWT_RunSystemMS(10000);
    
    /* Too short */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10", "Session Control - Too short"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 10 13", 3));
    
    /* Too long */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01 00", "Session Control - Too long"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 10 13", 3));
}
```

### 5. Sequential Operations

#### TC_10_08: Multiple Sequential Session Changes
```c
/*
  @testlists Service10_DiagnosticSessionControl
  TC_10_08: Test multiple sequential session changes without delay
  Tests SWCS_$10_12
*/
SWTEST void TC_10_08(void)
{
    SWT_RunSystemMS(10000);
    
    /* First session change */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session #1"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(100);
    
    /* Second session change */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Enter Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(100);
    
    /* Third session change */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Enter Default Session #2"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(100);
    
    /* Verify final session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 01", 4));
}
```

---

## Test File Template

```c
/********************************************************************************
 * COMPONENT TEST - Service 10 - Diagnostic Session Control
 * FILE: DCOM_SWT_Service10_DiagnosticSessionControl.c
 * 
 * TEST SCENARIOS COVERED:
 * ========================
 * 1. Positive Scenarios:
 *    - Enter Default Session with timing parameters
 *    - Enter Extended Session with timing parameters
 *    - Session transition verification
 * 
 * 2. Negative Scenarios:
 *    - NRC 0x12: SubFunctionNotSupported (invalid session type)
 *    - NRC 0x13: IncorrectMessageLengthOrInvalidFormat
 * 
 * 3. Session Management:
 *    - Session timeout behavior
 *    - Tester Present functionality
 *    - Multiple sequential session changes
 * 
 * Requirements Traceability:
 *   SWCS_$10_01: Default Session support
 *   SWCS_$10_02: Extended Session support
 *   SWCS_$10_03: Session transition handling
 *   SWCS_$10_04: S3 timeout implementation
 ********************************************************************************/

#include "SwTest_Global.h"
#include "TestEnvironment_Base.h"
#include "Platform_Types.h"
#include "Compiler.h"
#include "Std_Types.h"
#include "RBAPLCUST_Global.h"
#include "RBAPLCUST_Config.h"
#include "RBAPLCUST_Interface.h"

/* Test cases implementation here */
```

---

## Key Points

1. **Always start with Default Session** - Good practice to establish known state
2. **Verify session after change** - Use DID 0xF186 to confirm active session
3. **Respect timing** - Allow 250ms after session changes before next operation
4. **Test timeout behavior** - Verify S3 timeout works correctly
5. **Test Tester Present** - Ensure session keep-alive mechanism works
6. **Check NRCs** - Test all applicable negative response codes
7. **Sequential operations** - Test rapid session changes

---

## Common Mistakes to Avoid

 **Not allowing stabilization time after session change**
```c
SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed")); // Too fast!
```

 **Correct approach with delay**
```c
SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
SWT_RunSystemMS(250); // Allow session to stabilize
SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed"));
```

 **Not verifying session state**
```c
SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
// No verification - assume it worked
```

 **Verify session state**
```c
SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 F1 86", "Check Session"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 F1 86 03", 4));
```

---

## Related Services

- **Service 0x3E**: TesterPresent - Keeps session active
- **Service 0x22**: ReadDataByIdentifier (DID 0xF186) - Read active session
- **Service 0x27**: SecurityAccess - Security may reset on session change

---

## References

- ISO 14229-1: Unified Diagnostic Services (UDS)
- [Base Common Instructions](./ct00-base-common.instructions.md)
- [Master Index](./ct-index.instructions.md)

---

**END OF SERVICE 10 INSTRUCTIONS**
