# OBD on UDS Services - CT Instructions

##  ESSENTIALS

**Protocol:** ISO 14229-1 + SAE J1979 (OBD on UDS)  
**Channel:** OBD with UDS addressing  
**Activation:** DID 0xFD1B = 0x01 (OBD on UDS mode)  
**DID Ranges:** 0xF4xx (PIDs), 0xF8xx (InfoTypes)  
**Services:** UDS 0x22, 0x14, 0x19  
** Patterns:** [ct00-base-common.instructions.md](./ct00-base-common.instructions.md)

> ** TEMPLATE:** All PID/DID mappings, signals, responses are examples. Replace with actual implementation.

---

##  OBD ON UDS MODE ACTIVATION

**CRITICAL**: Must activate OBD on UDS mode before tests!

```c
//Start: OBDonUDS_Communication_Standard
uint8 seed[8] = {0};
SWT_RunSystemMS(10000);

/* Extended Session + Security */
SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
SWT_RunSystemMS(3750);

SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed"));
SWT_RunSystemMS(1000);
SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
calculate_key(seed, 1);
SWT_RunSystemMS(1000);
SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 02", key, 2, "Unlock Security"));
SWT_RunSystemMS(1500);
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "67 02", 2));
SWT_RunSystemMS(100);

/* Write OBD Communication Standard to OBDonUDS */
SWT_Eval(HSWFT_DiagSendRequest("UDS", "2E FD 1B 01", "Write OBD Comm Std to OBDonUDS"));
SWT_RunSystemMS(1000);
SWT_Eval(HSWFT_DiagEvalResponse("UDS", "6E FD 1B", 3));

/* Switch to next Power Cycle */
SWT_SoftwareReset();
//End  : OBDonUDS_Communication_Standard

SWT_RunSystemMS(500);
```

---

##  SERVICE MAPPING

OBD on UDS uses UDS Service 22 (ReadDataByIdentifier) with special DID ranges:

### **PIDs (OBD Service 01  UDS Service 22)**
```
OBD Service 01, PID 0x0C  UDS Service 22, DID 0xF40C
Request:  22 F4 0C (Read Engine RPM)
Response: 62 F4 0C [Data]
```

### InfoTypes (OBD Service 09  UDS Service 22)
```
OBD Service 09, InfoType 0x02  UDS Service 22, DID 0xF802
Request:  22 F8 02 (Read VIN)
Response: 62 F8 02 [VIN Data]
```

### DTC Services
- **Service 14**: Clear DTCs (same as UDS)
- **Service 19**: Read DTCs (same as UDS)

---

## Test Pattern for OBD on UDS PIDs

```c
SWTEST void TC_22_F4<PID>_01(void)
{
    RBMESG_DefineMESGDef(<OBD_Signal>);
    
    //Start: OBDonUDS_Communication_Standard
    [Activation code as shown above]
    //End  : OBDonUDS_Communication_Standard
    
    SWT_RunSystemMS(500);
    
    /* Set signal value */
    l_<OBD_Signal>.Qualifier = 0x01;
    l_<OBD_Signal>.Value = <TestValue>;
    RBMESG_SendMESGDef(<OBD_Signal>);
    
    /* Read via OBD channel using UDS Service 22 */
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "22 F4 <PID>", "Read PID via OBDonUDS"));
    SWT_Eval(HSWFT_DiagEvalResponse("OBD", "62 F4 <PID> <Data>", <Length>));
    
    /* Also test via functional addressing */
    SWT_Eval(HSWFT_DiagSendRequest("OBD_FUNC", "22 F4 <PID>", "Read PID Functional"));
    SWT_Eval(HSWFT_DiagEvalResponse("OBD_FUNC", "62 F4 <PID> <Data>", <Length>));
}
```

---

##  COMMON OBD ON UDS DIDS

### **PIDs (0xF400-0xF4FF)**
| DID    | OBD PID | Description             | Data Bytes |
|-----|---------|-------------|------------|
| 0xF40C | 0x0C | Engine RPM | 2 |
| 0xF40D | 0x0D | Vehicle Speed | 1 |
| 0xF405 | 0x05 | Coolant Temperature | 1 |
| 0xF40F | 0x0F | Intake Air Temperature | 1 |
| 0xF411 | 0x11 | Throttle Position | 1 |
| 0xF42F | 0x2F | Fuel Tank Level | 1 |

### **InfoTypes (0xF800-0xF8FF)**
| DID    | OBD InfoType | Description     |
|-----|--------------|-------------|
| 0xF802 | 0x02 | VIN |
| 0xF804 | 0x04 | Calibration ID |
| 0xF806 | 0x06 | CVN |

---

## Test Pattern for DTC Services

### Service 14: Clear DTCs
```c
SWTEST void TC_14_OBDonUDS_01(void)
{
    [OBD on UDS activation]
    
    /* Report test DTC */
    Dem_ReportErrorStatus(DemConf_DemEventParameter_OBD_DTC, DEM_EVENT_STATUS_FAILED);
    SWT_RunSystemMS(500);
    
    /* Clear via OBD channel */
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "14 FF FF FF", "Clear DTCs via OBDonUDS"));
    SWT_RunSystemMS(10000);
    SWT_Eval(HSWFT_DiagEvalResponse("OBD", "54", 1));
}
```

### Service 19: Read DTCs
```c
SWTEST void TC_19_OBDonUDS_01(void)
{
    [OBD on UDS activation]
    
    /* Report test DTC */
    Dem_ReportErrorStatus(DemConf_DemEventParameter_OBD_DTC, DEM_EVENT_STATUS_FAILED);
    SWT_RunSystemMS(500);
    
    /* Read via OBD channel */
    SWT_Eval(HSWFT_DiagSendRequest("OBD", "19 02 FF", "Read DTCs via OBDonUDS"));
    /* Response: 59 02 FF [Status] [DTC bytes...] */
}
```

---

## Test File Template

```c
/********************************************************************************
 * COMPONENT TEST - OBD on UDS - <Service/DID Description>
 * FILE: DCOM_SWT_OBDonUDS_<Name>.c
 * 
 * TEST SCENARIOS COVERED:
 * ========================
 * 1. OBD on UDS Mode Activation:
 *    - Write DID 0xFD1B = 0x01 (OBD on UDS mode)
 *    - Power cycle to activate
 * 
 * 2. Positive Scenarios:
 *    - Read PIDs via Service 22 (DID 0xF4xx)
 *    - Physical and Functional addressing
 * 
 * 3. DTC Services:
 *    - Service 14: Clear DTCs
 *    - Service 19: Read DTCs
 * 
 * Requirements Traceability:
 *   SWCS_$OBDonUDS_XX: [Requirements]
 ********************************************************************************/

#include "SwTest_Global.h"
#include "TestEnvironment_Base.h"
#include "Platform_Types.h"
#include "Compiler.h"
#include "Std_Types.h"

#if defined RBFS_RBLIBOBDOBDONUDS \ 
    && defined RBFS_RBLIBOBDOBDONUDS_ON
#if ((RBFS_RBLIBOBDOBDONUDS == RBFS_RBLIBOBDOBDONUDS_ON))

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
-  **MUST activate OBD on UDS mode** via DID 0xFD1B = 0x01
-  **Requires power cycle** after mode activation
- Uses UDS services (22, 14, 19) with OBD DIDs

**DID Mapping:**
- **0xF400-0xF4FF** - PIDs (Service 01 equivalent)
- **0xF800-0xF8FF** - InfoTypes (Service 09 equivalent)
- Physical and Functional addressing supported

**Feature Switch:**
```c
#if defined RBFS_RBLIBOBDOBDONUDS \
    && defined RBFS_RBLIBOBDOBDONUDS_ON
#if ((RBFS_RBLIBOBDOBDONUDS == RBFS_RBLIBOBDOBDONUDS_ON))
/* Test cases */
#endif
#endif
```

---

##  DIFFERENCES FROM OBD CLASSIC

| Aspect          | OBD Classic      | OBD on UDS         |
| --------------- | ---------------- | ------------------ |
|--------|-------------|------------|
| Protocol | SAE J1979 | ISO 14229 + J1979 |
| Request Format | `01 0C` | `22 F4 0C` |
| Response Format | `41 0C [Data]` | `62 F4 0C [Data]` |
| DID 0xFD1B Value | 0x00 | 0x01 |
| Feature Switch | RBFS_RBLIBOBDOBDCLASSIC | RBFS_RBLIBOBDOBDONUDS |

---

## Related Instructions

- [OBD Classic](./ct-obd-classic.instructions.md)
- [Service 22: ReadData](./ct-service-22-read-data.instructions.md)
- [Base Instructions](./ct00-base-common.instructions.md)
- [Master Index](./ct-index.instructions.md)

---

**END OF OBD ON UDS INSTRUCTIONS**
