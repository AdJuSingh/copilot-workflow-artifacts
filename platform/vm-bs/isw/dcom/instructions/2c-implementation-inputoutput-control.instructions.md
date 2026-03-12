# Instruction 2c: Input/Output Control Implementation Guidelines

##  ESSENTIALS

**Service:** UDS 0x2F - InputOutputControlByIdentifier (IOCBI)
**Naming:** `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_IOC_{ActuatorName}.c`
**Input:** Design from `doc/design/{DIDID}_{DIDName}_DetailedDesign.uml`
**Standards:** ISO 14229-1 Service 0x2F, AUTOSAR UDS patterns
**Header:** `RBAPLCUST_Global.h` (global declarations), `RBAPLCUST_InputOutputControl.h` (macros/control masks)

---

##  PREREQUISITE: Design File Must Exist

**BEFORE implementation**: Verify `doc/design/{DIDID}_{DIDName}_DetailedDesign.uml` exists
- **If missing**: STOP and prompt user to create design first
- **If exists**: Proceed with implementation

---

##  7-STEP EXECUTION WORKFLOW

### **STEP 1: ANALYZE COMMON FILES**

**Study reusable components:**
1. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_InputOutputControl.h` - Macros, control mask definitions, degradation APIs
2. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_IOC_*.c` - Similar IOC implementations for patterns
3. `RBAPLCUST_Global.h` - Existing degradation requesters (reuse or add new)
4. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_GeneralFunctions.c` - Helper functions and utilities
5. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_DiagnosticSessionControl.c` - Session management
6. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_DiagnosisDegradationProcess.c` - Degradation coordination

** Gate:** Common patterns identified, reusable components catalogued

### **STEP 2: IDENTIFY REFERENCE IOC**

**Search:** Find most similar IOC in `src/RBAPLCUST_IOC_*.c` based on actuator type
**Compare:** Control mask type (1-byte/2-byte/none), actuator category (valve/motor/plunger), degradation pattern
** Gate:** Reference IOC selected, implementation pattern understood

### **STEP 3: DEFINE STRUCTURE**

**Mandatory Functions:**
- `{ActuatorName}_ShortTerm()` - Short-term adjustment handler (starts actuation)
- `{ActuatorName}_ReturnToEcu()` - Return control to ECU handler (stops actuation)
- `{ActuatorName}_ResetToDefault()` - Reset to default handler
- `{ActuatorName}_ReadFnc()` - Read current actuation state

**Helper Functions:**
- `{ActuatorName}_Process()` - Cyclic processing for degradation monitoring
- `{ActuatorName}_ExtendedSessionLossHandler_()` - Session loss handling
- `{ActuatorName}_GeneralRejectHandler_()` - General reject handling
- `{ActuatorName}_Actuate()` - Actual actuation/deactuation logic
- `{ActuatorName}_ConditionCheckFailed()` - Precondition validation (optional)

**State Machine:**
- Static state variable: `RBAPLCUST_DegradationState_IOC_{ActuatorName}`
- Static control mask: `g_ControlMask{Suffix}` (uint8 or uint16)
- States: IDLE  WAITFORDEGRADATION  DEGRADED

**File Structure Template:**

```c
/*
 * ============================================================================
 * INPUT/OUTPUT CONTROL IMPLEMENTATION - {ActuatorName}
 * ============================================================================
 * Service: UDS 0x2F - InputOutputControlByIdentifier (IOCBI)
 * Standards: ISO 14229-1, AUTOSAR
 * Design: doc/design/{DIDID}_{DIDName}_DetailedDesign.uml
 * ============================================================================
 */

/* Includes */
#include "RBAPLCUST_InputOutputControl.h"
#include "RBAPLCUST_Global.h"
#include "RBAPLEOL_Interface.h"
#include "RBAPLHELP_SessionHandler.h"
/* Additional includes based on feature switches */

/* Feature Switch Validation */
RB_ASSERT_SWITCH_SETTINGS(RBFS_RBAPLCustIOControlXxx, ON, OFF)

/* Local Types and Definitions */
static RBAPLCUST_DegradationState_t RBAPLCUST_DegradationState_IOC_{ActuatorName} = RBAPLCUST_DegradationState_IDLE;
static uint8 g_ControlMask{Suffix} = 0x00; // or uint16 for 2-byte control mask

/* MESG Definitions */
RBMESG_DefineMESGDef(RBMESG_RBAPLEOL_ProcessSelection);
RBMESG_DefineMESGDef(RBMESG_RBDHP_DiagnosisProtectionState);

/* Forward Declarations */
static Std_ReturnType {ActuatorName}_Actuate(boolean Activate, const uint8* ControlStateInfo);
static void {ActuatorName}_Process(void);
static void {ActuatorName}_ExtendedSessionLossHandler_(void);
static void {ActuatorName}_GeneralRejectHandler_(uint8 Subfunction);

/* ============================================================================
 * PUBLIC FUNCTIONS
 * ============================================================================
 */

Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ShortTerm(
    const uint8* ControlStateInfo,
    Dcm_OpStatusType OpStatus,
    uint8 controlMask, // uint16 for 2-byte, omit for single actuator
    Dcm_NegativeResponseCodeType* ErrorCode
) {
    /* State machine implementation: IDLE -> WAITFORDEGRADATION -> DEGRADED */
}

Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ReturnToEcu(
    uint8 controlMask, // uint16 for 2-byte, omit for single actuator
    Dcm_NegativeResponseCodeType* ErrorCode
) {
    /* Deactivation and cleanup logic */
}

Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ResetToDefault(
    Dcm_OpStatusType OpStatus,
    uint8 controlMask, // uint16 for 2-byte, omit for single actuator
    Dcm_NegativeResponseCodeType* ErrorCode
) {
    /* Typically calls ReturnToEcu */
}

Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ReadFnc(
    Dcm_OpStatusType OpStatus,
    uint8* Data
) {
    /* Read current actuation state */
}

/* ============================================================================
 * PRIVATE FUNCTIONS
 * ============================================================================
 */

static Std_ReturnType {ActuatorName}_Actuate(boolean Activate, const uint8* ControlStateInfo) {
    /* Actual actuation logic */
}

void RBAPLCUST_IOC_{ActuatorName}_Process(void) {
    /* Cyclic monitoring in DEGRADED state */
}

static void {ActuatorName}_ExtendedSessionLossHandler_(void) {
    /* Cleanup on session loss */
}

static void {ActuatorName}_GeneralRejectHandler_(uint8 Subfunction) {
    /* Handle general reject conditions */
}
```

### Function Signatures Reference

**ShortTerm with 1-byte control mask:**
```c
Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ShortTerm(
    const uint8* ControlStateInfo,
    Dcm_OpStatusType OpStatus,
    uint8 controlMask,
    Dcm_NegativeResponseCodeType* ErrorCode)
```

**ShortTerm with 2-byte control mask:**
```c
Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ShortTerm(
    const uint8* ControlStateInfo,
    Dcm_OpStatusType OpStatus,
    uint16 controlMask,
    Dcm_NegativeResponseCodeType* ErrorCode)
```

**ShortTerm without control mask (single actuator):**
```c
Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ShortTerm(
    const uint8* ControlStateInfo,
    Dcm_OpStatusType OpStatus,
    Dcm_NegativeResponseCodeType* ErrorCode)
```

**ReturnToEcu:**
```c
Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ReturnToEcu(
    uint8/uint16 controlMask,  // omit if single actuator
    Dcm_NegativeResponseCodeType* ErrorCode)
```

**ResetToDefault:**
```c
Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ResetToDefault(
    Dcm_OpStatusType OpStatus,
    uint8/uint16 controlMask,  // omit if single actuator
    Dcm_NegativeResponseCodeType* ErrorCode)
```

**ReadFnc:**
```c
Std_ReturnType RBAPLCUST_IOC_{ActuatorName}_ReadFnc(
    Dcm_OpStatusType OpStatus,
    uint8* Data)
```

**Process, Handler functions:**
```c
void RBAPLCUST_IOC_{ActuatorName}_Process(void);
void RBAPLCUST_ExtendedSessionLossHandler_IOC_{ActuatorName}(void);
void RBAPLCUST_GeneralRejectHandler_IOC_{ActuatorName}(uint8 Subfunction);
```

### Control Mask Patterns

**Single Byte Control Mask (8 actuators):**
```c
// Used for: StandardValveDrive, WheelBasedCSV_PSVDrive, BrakeCircuitBasedCSV_PSVDrive
static uint8 g_ControlMask{Suffix} = 0x00;
// Bits 7-0 control actuators 1-8
```

**Two Byte Control Mask (16 actuators):**
```c
// Used for: ExtendedValveDrive, RemoteActuation
static uint16 g_ControlMask{Suffix} = 0x0000;
// Bits 15-8 (byte 1) control actuators 1-8
// Bits 7-0 (byte 2) control actuators 9-16
```

**Control Mask Validation:**
```c
// Check for unsupported bits
if ((controlMask & 0x000F) != 0) // Example: bits 3-0 reserved
{
    *ErrorCode = DCM_E_REQUESTOUTOFRANGE;
    retVal = E_NOT_OK;
}
```

### Input Validation Pattern

```c
// Range validation for duty cycle values
for(ControlStateIndex = 0; ControlStateIndex < NumParams; ControlStateIndex++)
{
    if(ControlStateInfo[ControlStateIndex] > RBAPLCUST_STGLTEST_MAXDUTYCTRLVAL)
    {
        l_InputRangeCheckFail = TRUE;
        break;
    }
}
```

### MESG Interface Pattern

```c
/* Receive MESG values */
RBMESG_RcvMESGDef(RBMESG_RBAPLEOL_ProcessSelection);
RBMESG_RcvMESGDef(RBMESG_RBDHP_DiagnosisProtectionState);

/* Check process selection */
if (l_RBMESG_RBAPLEOL_ProcessSelection != RBAPLEOL_NoEOLProcess)
{
    *ErrorCode = DCM_E_CONDITIONSNOTCORRECT;
    retVal = E_NOT_OK;
}

/* Send MESG values */
RBMESG_SendMESG(RBMESG_RBDHP_PumpMotorRequestFromDiagnosisRPM, l_RequestedRPM);
```

### Actuator-Specific Implementation Patterns

**Valve Actuations (Standard, Extended, CSV/PSV):**
- **Include:** Hydraulic access check: `RB_IsAppHydrAccessPossible()`
- **Include:** Hydraulic protection check: `RBMESG_RBDHP_DiagnosisProtectionState`
- **Input:** Duty cycle values (0-100%)
- **Control Mask:** Bit-by-bit control of which valves to actuate
- **Actuate:** Use control mask to activate/deactivate individual valves

**Motor Drive (Pump Motor):**
- **Input:** RPM value (2 bytes, 0-10000 RPM)
- **Checks:** Motor status, protection state
- **Stop:** `RBAPLEOL_StopPumpMotorActuation()`
- **MESG:** `RBMESG_RBDHP_PumpMotorRequestFromDiagnosisRPM`

**Plunger Actuation:**
- **Input:** Control mode (Position/Torque/Pressure) + control parameters
- **Modes:** `RBAPLCUST_iPBPositionControlMode`, `RBAPLCUST_iPBTorqueControlMode`, `RBAPLCUST_iPBPressureControlMode`
- **Resolution:** Use conversion for scaling values
- **Reset:** `RBAPLEOL_ActuatePlunger_mm(RBAPLEOL_RESET_PLUNGER)`
- **Process:** Start degradation process after successful actuation (different from valves)

**Remote Actuation:**
- **Similar to:** Valve actuation but uses remote ECU interfaces
- **Checks:** Node validity: `Dem_GetComponentRestrictedUsable()`
- **Error Status:** Check remote error status
- **MESG:** Use remote-specific MESG interfaces

** Gate:** Function signatures defined, state machine structure planned

### **STEP 4: IMPLEMENT COMMON COMPONENTS**

**Reuse Macros:**
- IOC subfunctions: `RBAPLCUST_IOCBI_RETURNCONTROLTOECU`, `RBAPLCUST_IOCBI_RESETTODEFAULT`, `RBAPLCUST_IOCBI_SHORTTERMADJUSTMENT`
- Control mask bits: `RBAPLCUST_IOC_CONTROLMASK_BIT0` through `RBAPLCUST_IOC_CONTROLMASK_BIT7` (1-byte)
- Control mask bits: `RBAPLCUST_IOC_CONTROLMASK1_BIT0` through `RBAPLCUST_IOC_CONTROLMASK2_BIT0` (2-byte)
- Max values: `RBAPLCUST_STGLTEST_MAXDUTYCTRLVAL` (100%), `RBAPLCUST_STGLTEST_MAXRPM` (10000 RPM)

**Reuse APIs:**
- `RBAPLHELP_RequestDegradation()`, `RBAPLHELP_IsDegraded()`
- `RBAPLCUST_StartDiagnosisDegradationProcess()`, `RBAPLCUST_StopDiagnosisDegradationProcess()`
- `RB_IsAppHydrAccessPossible()` - For hydraulic access check (valve actuations)

**Feature Switches:**
- Main IOC switch (e.g., `RBFS_RBAPLCustIOControlExtendedValveActuation`)
- Related switches (e.g., `RBFS_RBAPLEOLHydraulicProtectionCheck`, `RBFS_RBAPLEOLValvesActuation`)
- Individual actuator switches (e.g., `RBFS_ValveUSV1`, `RBFS_ValveHSV1`)
- Use `RB_ASSERT_SWITCH_SETTINGS()` with all possible values

**Conditional Includes:**
```c
#if (RBFS_RBAPLEOLHydraulicProtectionCheck == RBFS_RBAPLEOLHydraulicProtectionCheck_ON)
#include "RBDHP_ValveActuationInputDiagnosis.h"
#include "RBDHP_DiagnosisProtectionDisabling.h"
#include "RBDHP_DiagnosisProtectionState.h"
#endif
```

**Degradation States:**
- `RBAPLCUST_DegradationState_IDLE`
- `RBAPLCUST_DegradationState_WAITFORDEGRADATION`
- `RBAPLCUST_DegradationState_DEGRADED`

** Gate:** Common components integrated, feature switches configured

### **STEP 5: IMPLEMENT IOC LOGIC**

**ShortTerm Flow - IDLE State:**
1. Handle `DCM_CANCEL` OpStatus (return E_OK without using pointers)
2. Check no other EOL process running (`RBAPLEOL_ProcessSelection`)
3. Validate input parameters (range checks, control mask validation)
4. Check preconditions (hydraulic protection, system state)
5. Store control mask in global variable
6. Request degradation: `RBAPLHELP_RequestDegradation(TRUE, requester, ErrorCode)`
7. Transition to `WAITFORDEGRADATION`, return `DCM_E_PENDING`

**ShortTerm Flow - WAITFORDEGRADATION State:**
1. Check if degradation achieved: `RBAPLHELP_IsDegraded()`
2. If not degraded: return `DCM_E_PENDING`
3. If degraded:
   - Check diagnosis protection state (if applicable)
   - Call `_Actuate()` function
   - Check hydraulic access: `RB_IsAppHydrAccessPossible()` (for valves)
   - If access check fails: stay in `DEGRADED`, return `DCM_E_PENDING`
   - If successful: transition to `DEGRADED`, return `E_OK`

**ShortTerm Flow - DEGRADED State:**
1. Re-validate input parameters
2. Check hydraulic access (if applicable)
3. Update control mask: `g_ControlMask |= controlMask` (OR to add)
4. Call `_Actuate()` function with new parameters
5. Return `E_OK`, stay in `DEGRADED`

**ReturnToEcu Flow:**
1. **IDLE**: Return E_OK (nothing to stop)
2. **WAITFORDEGRADATION**: Assert error (invalid state)
3. **DEGRADED**:
   - Update control mask: `g_ControlMask &= ~(controlMask)` (AND-NOT to clear)
   - Call `_Actuate()` with FALSE to deactivate
   - If control mask is 0x00 (all released):
     - Stop actuation
     - Stop degradation process
     - Release degradation
     - Transition to IDLE
   - Return E_OK

**ResetToDefault Flow:**
Simply calls `ReturnToEcu()` after checking no other process running

**ReadFnc Flow:**
1. Initialize data buffer to 0x00
2. Read current actuator states from MESG interfaces
3. Populate data buffer with current values
4. Return E_OK or E_NOT_OK

**Process Flow (Cyclic):**
- **IDLE/WAITFORDEGRADATION**: Assert error
- **DEGRADED**:
  1. Check if still degraded: `RBAPLHELP_IsDegraded()`
  2. Check preconditions
  3. If any check fails: stop actuation, release degradation, transition to IDLE

** Gate:** All four handlers and cyclic process implemented with correct flow

### **STEP 6: IMPLEMENT ERROR HANDLING**

**Return Codes:**
- `E_OK` - Operation successful
- `E_NOT_OK` - Operation failed
- `DCM_E_PENDING` - Operation pending (will be called again)

**Error Codes:**
- `DCM_E_REQUESTOUTOFRANGE` - Invalid parameters or feature not enabled
- `DCM_E_CONDITIONSNOTCORRECT` - Preconditions not met
- `DCM_E_REQUESTSEQUENCEERROR` - Wrong sequence of operations
- `NULL_VALUE` - Success (positive response)

**DCM_CANCEL Handling:**
Always check in ShortTerm function:
```c
if (OpStatus == DCM_CANCEL)
{
    // Don't use pointers - they are NULL_PTR!
    retVal = E_OK;
}
```

**Session Loss Handler:**
- **IDLE**: Do nothing
- **WAITFORDEGRADATION**: Release degradation, transition to IDLE
- **DEGRADED**: Stop actuation, stop degradation process, release degradation, reset control mask, transition to IDLE

**General Reject Handler:**
- **ReturnToEcu/ResetToDefault**: Do nothing (allow operation)
- **ShortTermAdjustment**: Same as session loss handler

** Gate:** Error handling complete, all scenarios covered

### **STEP 7: QUALITY GATE**

**Code Structure:**
- [ ] Four mandatory functions with AUTOSAR signatures
- [ ] Three helper functions following naming conventions
- [ ] State machine implemented correctly with control mask management
- [ ] Follows reference IOC pattern

**Reusability:**
- [ ] Uses common macros and APIs
- [ ] Reuses existing feature switches
- [ ] Reuses degradation requesters from `RBAPLCUST_Global.h`
- [ ] No duplicate code

**Actuator-Specific Implementation:**
- [ ] Correct control mask type (1-byte/2-byte/none)
- [ ] Hydraulic access check (for valves)
- [ ] Protection state checks (if applicable)
- [ ] Proper MESG interface usage
- [ ] Input validation (range checks, control mask validation)

**Error Handling:**
- [ ] All error paths implemented
- [ ] Correct NRC codes returned
- [ ] DCM_CANCEL handled properly (no pointer usage)
- [ ] Session loss and general reject handlers implemented

**Standards Compliance:**
- [ ] ISO 14229-1 Service 0x2F compliant
- [ ] AUTOSAR patterns followed
- [ ] Naming conventions adhered to

**Execution Gates:**
- **Gate 1 (Analysis):** Common patterns understood  PASS to planning
- **Gate 2 (Planning):** Structure defined  PASS to implementation
- **Gate 3 (Implementation):** Code complete  PASS to validation
- **Gate 4 (Quality):** All checks passed  PASS to review

** Final:** Ready for code review and testing

---

##  COMMON MISTAKES

**Structure:** Missing helper functions, incorrect function signatures, no state machine, missing control mask management
**Reusability:** Creating new macros instead of reusing, not checking for existing degradation requesters, duplicate code
**Error Handling:** Missing error paths, incorrect NRC codes, using pointers during DCM_CANCEL, no session loss handling
**Actuator-Specific:** Missing hydraulic access check (valves), missing protection state checks, incorrect control mask operations
**State Management:** Not updating control mask correctly (use OR to add, AND-NOT to remove), not checking degradation state before actuation
**Cleanup:** Not releasing degradation on errors, not resetting control mask, not stopping actuation properly
**Validation:** Missing input range checks, not validating unsupported control mask bits, not checking MESG process selection
**Standards:** Not following AUTOSAR patterns, wrong naming conventions, missing feature switches

---

##  REFERENCES

**ISO 14229-1:** UDS Service 0x2F - InputOutputControlByIdentifier
**AUTOSAR:** Classic Platform Diagnostic Communication Manager
**Headers:** `RBAPLCUST_InputOutputControl.h`, `RBAPLCUST_Global.h`, `RBAPLEOL_Interface.h`
**Reference:** `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_IOC_*.c`
