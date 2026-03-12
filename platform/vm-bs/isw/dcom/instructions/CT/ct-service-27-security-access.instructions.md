# Service 27: SecurityAccess - CT Instructions

> ** REFERENCE TEMPLATE:** All examples are templates. Replace security levels, key algorithms, seed/key lengths with your actual implementation.

## Overview

Service 27 (SecurityAccess) is used to unlock protected diagnostic services by providing a seed-key authentication.

**Standard:** ISO 14229-1 (UDS) | **Service ID:** 0x27 | **Response ID:** 0x67  
** Common Patterns:** [ct00-base-common.instructions.md - Section 7.2](./ct00-base-common.instructions.md#72-security-access-pattern)

---

## Key Concepts

### Security Levels
- **Level 1 (0x01/0x02)**: EOL (End-of-Line) - Factory/service level access
- **Level 2 (0x03/0x04)**: Service Level - Advanced diagnostic access
- **Odd numbers**: Request seed
- **Even numbers**: Send key

### Authentication Flow
1. Request seed (0x27 0x01 or 0x27 0x03)
2. ECU responds with seed value
3. Calculate key based on seed
4. Send key (0x27 0x02 or 0x27 0x04)
5. ECU validates and unlocks

### Important Constraints
- **Power-on delay**: Must wait 5 seconds after power-on before first seed request
- **Session requirement**: Only available in Extended Session
- **Seed timeout**: Seed expires after certain time
- **Attempt counter**: Limited failed attempts before lockout

---

## Key Calculation Algorithms

> ** Complete function in:** [ct00-base-common.instructions.md - Section 5](./ct00-base-common.instructions.md#5-helper-functions)

**Example (Replace with your actual algorithm):**
- Level 1 (EOL): `key[1]=seed[0], key[0]=seed[1]` (swap bytes)
- Level 2 (Service): `key[0]=seed[0]^seed[1], key[1]=seed[0]` (XOR operation)

---

## Standard Request/Response Format

### Request Seed Format
```
[Service ID] [Security Level (odd)]
Example: 27 01 (Request seed for Level 1)
         27 03 (Request seed for Level 2)
```

### Seed Response Format
```
[Response ID] [Security Level] [Seed Bytes...]
Example: 67 01 12 34 (Level 1 seed = 0x1234)
```

### Send Key Format
```
[Service ID] [Security Level (even)] [Key Bytes...]
Example: 27 02 34 12 (Send key for Level 1)
```

### Positive Response Format
```
[Response ID] [Security Level]
Example: 67 02 (Level 1 unlocked)
```

### Common Negative Response Codes (NRCs)
- **0x13**: IncorrectMessageLengthOrInvalidFormat
- **0x24**: RequestSequenceError - Key sent without seed request
- **0x35**: InvalidKey - Wrong key provided
- **0x36**: ExceedNumberOfAttempts - Too many failed attempts
- **0x37**: RequiredTimeDelayNotExpired - Power-on delay not met
- **0x7F**: ServiceNotSupportedInActiveSession - Not in Extended session

---

## Test Scenarios

### 1. Positive Scenarios

#### TC_27_01: EOL Level Unlock (Level 1)
```c
/*
  @testlists Service27_SecurityAccess
  TC_27_01: Successful EOL security unlock
  Tests SWCS_$27_01, SWCS_$27_02
*/
SWTEST void TC_27_01(void)
{
    uint8 seed[8] = {0};
    
    SWT_RunSystemMS(10000);  /* Wait > 5 seconds after power-on */
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(3750);
    
    /* Request Seed */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed - Level 1"));
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
    
    /* Calculate and send key */
    calculate_key(seed, 1);
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 02", key, 2, "Send Key - Level 1"));
    SWT_RunSystemMS(1500);
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "67 02", 2));
    SWT_RunSystemMS(100);
}
```

#### TC_27_02: Service Level Unlock (Level 2)
```c
/*
  @testlists Service27_SecurityAccess
  TC_27_02: Successful Service level security unlock
  Tests SWCS_$27_03, SWCS_$27_04
*/
SWTEST void TC_27_02(void)
{
    uint8 seed[8] = {0};
    
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(3750);
    
    /* Request Seed - Level 2 */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 03", "Request Seed - Level 2"));
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 03", seed, 2));
    
    /* Calculate and send key */
    calculate_key(seed, 2);
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 04", key, 2, "Send Key - Level 2"));
    SWT_RunSystemMS(1500);
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "67 04", 2));
    SWT_RunSystemMS(100);
}
```

### 2. Negative Scenarios

#### TC_27_03: NRC 0x37 - Power-On Delay Not Met
```c
/*
  @testlists Service27_SecurityAccess
  TC_27_03: Request seed before 5-second power-on delay
  Tests NRC 0x37: RequiredTimeDelayNotExpired
*/
SWTEST void TC_27_03(void)
{
    SWT_RunSystemMS(1000);  /* Only 1 second after power-on */
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Try to request seed too early */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed - Too early"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 27 37", 3));
    
    /* Wait for remaining time */
    SWT_RunSystemMS(4500);
    
    /* Now should work */
    uint8 seed[8] = {0};
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed - OK"));
    SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
}
```

#### TC_27_04: NRC 0x7F - Wrong Session
```c
/*
  @testlists Service27_SecurityAccess
  TC_27_04: Request seed in Default Session
  Tests NRC 0x7F: ServiceNotSupportedInActiveSession
*/
SWTEST void TC_27_04(void)
{
    SWT_RunSystemMS(10000);
    
    /* Stay in Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Try to request seed in wrong session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed in Default"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 27 7F", 3));
}
```

#### TC_27_05: NRC 0x24 - Send Key Without Seed
```c
/*
  @testlists Service27_SecurityAccess
  TC_27_05: Send key without requesting seed first
  Tests NRC 0x24: RequestSequenceError
*/
SWTEST void TC_27_05(void)
{
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(3750);
    
    /* Send key without seed request */
    SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 02", key, 2, "Send Key without Seed"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 27 24", 3));
}
```

#### TC_27_06: NRC 0x35 - Invalid Key
```c
/*
  @testlists Service27_SecurityAccess
  TC_27_06: Send incorrect key
  Tests NRC 0x35: InvalidKey
*/
SWTEST void TC_27_06(void)
{
    uint8 seed[8] = {0};
    
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(3750);
    
    /* Request Seed */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed"));
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
    
    /* Calculate WRONG key */
    calculate_key(seed, 3);  /* Use fail algorithm */
    SWT_RunSystemMS(1000);
    
    /* Send wrong key */
    SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 02", key, 2, "Send Wrong Key"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 27 35", 3));
}
```

#### TC_27_07: NRC 0x13 - Incorrect Message Length
```c
/*
  @testlists Service27_SecurityAccess
  TC_27_07: Send request with incorrect message length
  Tests NRC 0x13: IncorrectMessageLengthOrInvalidFormat
*/
SWTEST void TC_27_07(void)
{
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(3750);
    
    /* Request seed with extra bytes */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01 00", "Request Seed - Too long"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 27 13", 3));
}
```

### 3. Security Persistence

#### TC_27_08: Security Lost on Session Change
```c
/*
  @testlists Service27_SecurityAccess
  TC_27_08: Verify security is lost when returning to Default Session
  Tests SWCS_$27_10
*/
SWTEST void TC_27_08(void)
{
    uint8 seed[8] = {0};
    
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session and unlock */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(3750);
    
    /* Unlock security */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed"));
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
    calculate_key(seed, 1);
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 02", key, 2, "Unlock Security"));
    SWT_RunSystemMS(1500);
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "67 02", 2));
    
    /* Verify service requiring security works */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "2E FD 1B 00", "Write Protected DID"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "6E FD 1B", 3));
    
    /* Return to Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    
    /* Enter Extended Session again */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Verify security is lost - should get NRC 0x33 */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "2E FD 1B 00", "Write Protected DID"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "7F 2E 33", 3));
}
```

---

## Test File Template

```c
/********************************************************************************
 * COMPONENT TEST - Service 27 - SecurityAccess
 * FILE: DCOM_SWT_Service27_SecurityAccess.c
 * 
 * TEST SCENARIOS COVERED:
 * ========================
 * 1. Positive Scenarios:
 *    - EOL Level (Level 1) unlock
 *    - Service Level (Level 2) unlock
 *    - Seed generation and key validation
 * 
 * 2. Negative Scenarios:
 *    - NRC 0x13: IncorrectMessageLengthOrInvalidFormat
 *    - NRC 0x24: RequestSequenceError (key without seed)
 *    - NRC 0x35: InvalidKey (wrong key)
 *    - NRC 0x37: RequiredTimeDelayNotExpired (power-on delay)
 *    - NRC 0x7F: ServiceNotSupportedInActiveSession
 * 
 * 3. Session Management:
 *    - Security lost on session transition
 *    - Security timeout behavior
 * 
 * Requirements Traceability:
 *   SWCS_$27_01: EOL security level support
 *   SWCS_$27_02: Service security level support
 *   SWCS_$27_03: Power-on delay requirement
 *   SWCS_$27_04: Seed-key algorithm
 ********************************************************************************/

#include "SwTest_Global.h"
#include "TestEnvironment_Base.h"
#include "Platform_Types.h"
#include "Compiler.h"
#include "Std_Types.h"
#include "RBAPLCUST_Global.h"
#include "RBAPLCUST_Config.h"
#include "RBAPLCUST_Interface.h"

static uint8 key[8] = {0};

static void calculate_key(uint8 *seed, uint8 SecLevel_u8)
{
    switch (SecLevel_u8)
    {
        case 1:  /* EOL Level */
            key[1] = seed[0];
            key[0] = seed[1];
            break;
        case 2:  /* Service Level */
            key[0] = seed[0] ^ seed[1];
            key[1] = seed[0];
            break;
        case 3:  /* Fail condition */
            key[0] = 0x0F & seed[0];
            key[1] = 0x0F & seed[1];
            break;
        default:
            break;
    }
}

/* Test cases implementation here */
```

---

## Key Points

1. **Wait for power-on delay** - 5 seconds (use 10000ms to be safe)
2. **Extended session required** - Always enter Extended before security
3. **Proper timing** - 1000ms between seed and key
4. **Seed is random** - Must read actual seed, not hardcoded value
5. **Test both levels** - EOL and Service levels
6. **Test security loss** - Verify on session transitions
7. **Test all NRCs** - Especially 0x35, 0x37, 0x24

---

## Related Services

- **Service 0x10**: DiagnosticSessionControl - Extended session required
- **Service 0x2E**: WriteDataByIdentifier - May require security
- **Service 0x31**: RoutineControl - May require security

---

## References

- [Base Common Instructions](./ct00-base-common.instructions.md)
- [Master Index](./ct-index.instructions.md)

---

**END OF SERVICE 27 INSTRUCTIONS**
