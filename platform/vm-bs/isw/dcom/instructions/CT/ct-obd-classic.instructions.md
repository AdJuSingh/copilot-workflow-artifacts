# OBD Classic Services - CT Instructions

##  ESSENTIALS

**Protocol:** SAE J1979 (OBD-II)  
**Channel:** OBD (physical), OBD_FUNC (functional)  
**Activation:** DID 0xFD1B = 0x00 (OBD Classic mode)  
**Services:** 0x01, 0x02, 0x03, 0x04, 0x07, 0x09, 0x0A  
** Patterns:** [ct00-base-common.instructions.md](./ct00-base-common.instructions.md)

> ** TEMPLATE:** All PID values, signals, responses are examples. Replace with actual implementation.

---

##  OBD CLASSIC SERVICES

**Available Services:**
- **Service 01** - Request Current Powertrain Diagnostic Data (PIDs)
- **Service 02** - Request Powertrain Freeze Frame Data
- **Service 03** - Request Emission-Related DTCs
- **Service 04** - Clear/Reset Emission-Related Diagnostic Information
- **Service 07** - Request Emission-Related DTCs (Current/Last Cycle)
- **Service 09** - Request Vehicle Information (InfoTypes)
- **Service 0A** - Request Permanent DTCs

---

##  OBD MODE ACTIVATION

**CRITICAL:** Must activate OBD Classic mode before all tests!

```c
//Start: OBDclassic_Communication_Standard
uint8 seed[8] = {0};
SWT_RunSystemMS(10000);

/* Enter Extended session */
SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
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
SWT_Eval(HSWFT_DiagSendRequest("UDS", "2E FD 1B 00", "Write OBD Comm Std to OBDclassic"));
SWT_RunSystemMS(1000);
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "6E FD 1B", 3));

/* Switch to next Power Cycle */
SWT_SoftwareReset();
//End  : OBDclassic_Communication_Standard

SWT_RunSystemMS(1000);
```

---

##  SERVICE 01: CURRENT POWERTRAIN DATA

### **Request Format**
```
[0x01] [PID]
Example: 01 0C (Engine RPM - PID 0x0C)
```

### Response Format
```
[0x41] [PID] [Data Bytes...]
Example: 41 0C 1A F8 (Engine RPM = 6910 rpm)
```

### Test Pattern for Service 01

```c
SWTEST void TC_01_<PID>_01(void)
{
    RBMESG_DefineMESGDef(<OBD_Signal>);
    
    //Start: OBDclassic_Communication_Standard
    [Activation code as shown above]
    //End  : OBDclassic_Communication_Standard
    
    SWT_RunSystemMS(1000);
    
    /* Set signal value */
    l_<OBD_Signal>.Qualifier = 0x01;  /* Valid for OBD */
    l_<OBD_Signal>.Value = <TestValue>;
    RBMESG_SendMESGDef(<OBD_Signal>);
    
    /* Physical Addressing */
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "01 <PID>", "PID <PID> Physical"));
    SWT_Eval(HSWFT_DiagEvalResponse("OBD", "41 <PID> <Data>", <Length>));
    
    /* Functional Addressing */
    SWT_Eval(HSWFT_DiagSendRequest("OBD_FUNC", "01 <PID>", "PID <PID> Functional"));
    SWT_Eval(HSWFT_DiagEvalResponse("OBD_FUNC", "41 <PID> <Data>", <Length>));
}
```

---

##  COMMON PIDS

| PID  | Description             | Bytes | Formula         |
| ---- | ----------------------- | ----- | --------------- |
| 0x0C | Engine RPM | 2 | (256*A+B)/4 |
| 0x0D | Vehicle Speed | 1 | A km/h |
| 0x05 | Coolant Temperature | 1 | A-40 C |
| 0x0F | Intake Air Temperature | 1 | A-40 C |
| 0x11 | Throttle Position | 1 | A*100/255 % |
| 0x2F | Fuel Tank Level | 1 | A*100/255 % |

---

## Service 03: Request Emission-Related DTCs

### Request
```
[0x03]
```

### Response
```
[0x43] [DTC Count] [DTC1 High] [DTC1 Low] [DTC2 High] [DTC2 Low] ...
```

### Test Pattern

```c
SWTEST void TC_03_01(void)
{
    [OBD Classic activation]
    
    /* Report test DTC */
    Dem_ReportErrorStatus(DemConf_DemEventParameter_OBD_DTC, DEM_EVENT_STATUS_FAILED);
    SWT_RunSystemMS(500);
    
    /* Request DTCs */
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "03", "Request Emission DTCs"));
    /* Response format: 43 [Count] [DTC bytes...] */
}
```

---

## Service 04: Clear Emission DTCs

### Request
```
[0x04]
```

### Response
```
[0x44]
```

### Test Pattern

```c
SWTEST void TC_04_01(void)
{
    [OBD Classic activation]
    
    /* Report and verify DTC */
    Dem_ReportErrorStatus(DemConf_DemEventParameter_OBD_DTC, DEM_EVENT_STATUS_FAILED);
    SWT_RunSystemMS(500);
    
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "03", "Check DTCs"));
    /* Verify DTC present */
    
    /* Clear DTCs */
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "04", "Clear DTCs"));
    SWT_RunSystemMS(10000);  /* Wait for NvM */
    SWT_Eval(HSWFT_DiagEvalResponse("OBD", "44", 1));
    
    /* Verify cleared */
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "03", "Check DTCs After Clear"));
    /* Verify no DTCs */
}
```

---

## Service 09: Vehicle Information

### Request Format
```
[0x09] [InfoType]
Example: 09 02 (VIN)
```

### Response Format
```
[0x49] [InfoType] [Data Bytes...]
```

### Common InfoTypes
- **0x02**: VIN (Vehicle Identification Number)
- **0x04**: Calibration ID
- **0x06**: Calibration Verification Numbers

---

## Test File Template

```c
/********************************************************************************
 * COMPONENT TEST - OBD Classic - Service <XX> - <Description>
 * FILE: DCOM_SWT_OBDclassic_Service<XX>_<Name>.c
 * 
 * TEST SCENARIOS COVERED:
 * ========================
 * 1. OBD Mode Activation:
 *    - Write DID 0xFD1B = 0x00 (OBD Classic mode)
 *    - Power cycle to activate
 * 
 * 2. Positive Scenarios:
 *    - Physical addressing
 *    - Functional addressing
 *    - Valid signal values
 * 
 * 3. Boundary Cases:
 *    - Min/max values
 *    - Invalid qualifier
 * 
 * Requirements Traceability:
 *   SWCS_$OBD_XX: [Requirements]
 ********************************************************************************/

#include "SwTest_Global.h"
#include "TestEnvironment_Base.h"
#include "Platform_Types.h"
#include "Compiler.h"
#include "Std_Types.h"

#if defined RBFS_RBLIBOBDOBDCLASSIC \ 
    && defined RBFS_RBLIBOBDOBDCLASSIC_ON
#if ((RBFS_RBLIBOBDOBDCLASSIC == RBFS_RBLIBOBDOBDCLASSIC_ON))

#include "RBAPLOBD_Global.h"
#include "RBAPLOBD_NetworkInterface.h"
#include "RBAPLCUST_Global.h"
#include "RBAPLCUST_Config.h"

static uint8 key[8] = {0};
static void calculate_key(uint8 *seed, uint8 SecLevel_u8) { /* ... */ }

/* Test cases here */

#endif
#endif
```

---

##  KEY REQUIREMENTS

**Prerequisites:**
-  **MUST activate OBD Classic mode** via DID 0xFD1B = 0x00
-  **Requires power cycle** after mode activation
- Test both Physical ("OBD") and Functional ("OBD_FUNC")

**Test Coverage:**
- Test all implemented PIDs
- Use proper MESG signals with correct qualifiers
- Verify response format and data calculations
- Test both addressing modes

**Feature Switch:**
```c
#if defined RBFS_RBLIBOBDOBDCLASSIC \
    && defined RBFS_RBLIBOBDOBDCLASSIC_ON
#if ((RBFS_RBLIBOBDOBDCLASSIC == RBFS_RBLIBOBDOBDCLASSIC_ON))
/* Test cases */
#endif
#endif
```  
 **Feature switch protection** - Wrap in RBFS_RBLIBOBDOBDCLASSIC  
 **Response format**: Service ID + 0x40

---

## Related Instructions

- [OBD on UDS](./ct-obd-on-uds.instructions.md)
- [Base Instructions](./ct00-base-common.instructions.md)
- [Master Index](./ct-index.instructions.md)

---

**END OF OBD CLASSIC INSTRUCTIONS**
