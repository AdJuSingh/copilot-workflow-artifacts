# Instruction 2b: Routine Control Implementation Guidelines

##  ESSENTIALS

**Service:** UDS 0x31 - RoutineControl
**Naming:** `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_RoutineControl_{RoutineName}.c`
**Input:** Design from `doc/design/{RoutineID}_{RoutineName}_DetailedDesign.uml`
**Standards:** ISO 14229-1 Service 0x31, AUTOSAR UDS patterns
**Header:** `RBAPLCUST_Global.h` (global declarations), `RBAPLCUST_RoutineControl.h` (macros/status codes)

---

##  PREREQUISITE: Design File Must Exist

**BEFORE implementation**: Verify `doc/design/{RoutineID}_{RoutineName}_DetailedDesign.uml` exists
- **If missing**: STOP and prompt user to create design first
- **If exists**: Proceed with implementation

---

##  7-STEP EXECUTION WORKFLOW

### **STEP 1: ANALYZE COMMON FILES**

**Study reusable components:**
1. `rb/as/ms/core/app/dcom/RBAPLCust/api/RBAPLCUST_RoutineControl.h` - Macros, APIs, patterns
2. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_RoutineControl.c` - Common implementations
3. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_RoutineControl_IPB*.c` - Similar routines for degradation patterns
4. `RBAPLCUST_Global.h` - Existing degradation requesters (reuse or add new)
5. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_GeneralFunctions.c` - Helper functions and utilities
6. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_DiagnosticSessionControl.c` - Session management
7. `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_DiagnosisDegradationProcess.c` - Degradation coordination

** Gate:** Common patterns identified, reusable components catalogued

### **STEP 2: IDENTIFY REFERENCE ROUTINE**

**Search:** Find most similar routine in `src/RBAPLCUST_RoutineControl_IPB*.c`
**Compare:** Parameters, degradation pattern, feature switches, error handling
** Gate:** Reference routine selected, implementation pattern understood

### **STEP 3: DEFINE STRUCTURE**

**Mandatory Functions:**
- `{RoutineName}_start()` - Start routine handler
- `{RoutineName}_stop()` - Stop routine handler
- `{RoutineName}_RequestResult()` - Results retrieval handler

**Helper Functions:**
- `{RoutineName}_Process()` - Main processing logic
- `{RoutineName}_ExtendedSessionLossHandler_()` - Session loss handling
- `{RoutineName}_GeneralRejectHandler_()` - General reject handling

**State Machine:**
- Static state variable
- Switch-case: IDLE  WAITFORDEGRADATION  DEGRADED

**File Structure Template:**

```c
/*
 * ============================================================================
 * ROUTINE CONTROL IMPLEMENTATION - {RoutineName}
 * ============================================================================
 * Service: UDS 0x31 - RoutineControl
 * Standards: ISO 14229-1, AUTOSAR
 * Design: doc/design/{RoutineID}_{RoutineName}_DetailedDesign.uml
 * ============================================================================
 */

/* Includes */
#include "RBAPLCUST_RoutineControl.h"
#include "RBAPLCUST_Global.h"
/* Additional includes */

/* Feature Switch Validation */
RB_ASSERT_SWITCH_SETTINGS(RBFS_RBAPLEOLXxx, OFF)

/* Local Types and Definitions */
typedef enum {
    RBAPLCUST_DegradationState_IDLE,
    RBAPLCUST_DegradationState_WAITFORDEGRADATION,
    RBAPLCUST_DegradationState_DEGRADED
} {RoutineName}_DegradationState_ten;

/* Static Variables */
static {RoutineName}_DegradationState_ten {RoutineName}_DegradationState_en = RBAPLCUST_DegradationState_IDLE;

/* Forward Declarations */
static Std_ReturnType {RoutineName}_Process(void);
static void {RoutineName}_ExtendedSessionLossHandler_(void);
static void {RoutineName}_GeneralRejectHandler_(void);

/* ============================================================================
 * PUBLIC FUNCTIONS
 * ============================================================================
 */

Std_ReturnType RBAPLCUST_{RoutineName}_start(
    const uint8* dataIn_pcu8,
    Dcm_OpStatusType OpStatus,
    uint8* dataOut_pu8,
    uint16* currentDataLength_pu16,
    Dcm_NegativeResponseCodeType* ErrorCode
) {
    /* Implementation */
}

Std_ReturnType RBAPLCUST_{RoutineName}_stop(
    const uint8* dataIn_pcu8,
    Dcm_OpStatusType OpStatus,
    uint8* dataOut_pu8,
    uint16* currentDataLength_pu16,
    Dcm_NegativeResponseCodeType* ErrorCode
) {
    /* Implementation */
}

Std_ReturnType RBAPLCUST_{RoutineName}_RequestResult(
    Dcm_OpStatusType OpStatus,
    uint8* dataOut_pu8,
    uint16* currentDataLength_pu16,
    Dcm_NegativeResponseCodeType* ErrorCode
) {
    /* Implementation */
}

/* ============================================================================
 * PRIVATE FUNCTIONS
 * ============================================================================
 */

static Std_ReturnType {RoutineName}_Process(void) {
    /* State machine implementation */
}

static void {RoutineName}_ExtendedSessionLossHandler_(void) {
    /* Session loss handling */
}

static void {RoutineName}_GeneralRejectHandler_(void) {
    /* General reject handling */
}
```

** Gate:** Function signatures defined, state machine structure planned

### **STEP 4: IMPLEMENT COMMON COMPONENTS**

**Reuse Macros:**
- `RBAPLCUST_RC_STARTROUTINE`, `RBAPLCUST_RC_STOPROUTINE`, `RBAPLCUST_RC_REQUESTRESULTS`
- Status codes: `ROUTINE_SUCCESSFULLY_STOPPED`, `ROUTINE_SUCCESSFULLY_COMPLETED`, `RBAPLCUST_OK`

**Reuse APIs:**
- `RBAPLHELP_RequestDegradation()`, `RBAPLHELP_IsDegraded()`
- `RBAPLCUST_StartDiagnosisDegradationProcess()`, `RBAPLCUST_StopDiagnosisDegradationProcess()`
- `RBAPLEOL_ReadyToStartRoutine()`, `RBAPLCUST_StopAplEolRoutine()`

**Feature Switches:**
- Reuse existing `RBFS_RBAPLEOLXxx` switches from similar routines
- Add `RB_ASSERT_SWITCH_SETTINGS()` with OFF check returning `DCM_E_REQUESTOUTOFRANGE`

**Degradation States:**
- `RBAPLCUST_DegradationState_IDLE`
- `RBAPLCUST_DegradationState_WAITFORDEGRADATION`
- `RBAPLCUST_DegradationState_DEGRADED`

** Gate:** Common components integrated, feature switches configured

### **STEP 5: IMPLEMENT ROUTINE LOGIC**

**Start Flow:**
1. Check `RBAPLEOL_ReadyToStartRoutine()`
2. Validate input parameters
3. Request degradation via `RBAPLHELP_RequestDegradation()`
4. Wait for degradation state
5. Start routine execution
6. Return `RBAPLCUST_OK` or error code

**Stop Flow:**
1. Validate current state
2. Stop degradation process
3. Call `RBAPLCUST_StopAplEolRoutine()`
4. Return status code

**Results Flow:**
1. Check execution state
2. Populate output parameters
3. Return results with status

** Gate:** All three handlers implemented with correct flow

### **STEP 6: IMPLEMENT ERROR HANDLING**

**Return Codes:**
- `E_OK` - Success
- `E_NOT_OK` - Failure
- `DCM_E_PENDING` - Operation in progress

**Error Codes:**
- `DCM_E_REQUESTOUTOFRANGE` - Invalid parameters
- `DCM_E_CONDITIONSNOTCORRECT` - Preconditions not met
- `DCM_E_REQUESTSEQUENCEERROR` - Invalid state for operation
- `DCM_E_GENERALREJECT` - General failure

**Ready States:**
- `RBAPLEOL_RoutineStartPossible` - Can start routine
- `RBAPLEOL_RoutineRunningAlready` - Already executing

** Gate:** Error handling complete, all scenarios covered

### **STEP 7: QUALITY GATE**

**Code Structure:**
- [ ] Three mandatory functions with AUTOSAR signatures
- [ ] Three helper functions following naming conventions
- [ ] State machine implemented correctly
- [ ] Follows reference routine pattern

**Reusability:**
- [ ] Uses common macros and APIs
- [ ] Reuses existing feature switches
- [ ] Reuses degradation requesters from `RBAPLCUST_Global.h`
- [ ] No duplicate code

**Error Handling:**
- [ ] All error paths implemented
- [ ] Correct NRC codes returned
- [ ] State validation in all handlers

**Standards Compliance:**
- [ ] ISO 14229-1 Service 0x31 compliant
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

**Structure:** Missing helper functions, incorrect function signatures, no state machine
**Reusability:** Creating new macros instead of reusing, not checking for existing degradation requesters, duplicate code
**Error Handling:** Missing error paths, incorrect NRC codes, no state validation
**Standards:** Not following AUTOSAR patterns, wrong naming conventions, missing feature switches
**Process:** Skipping analysis of common files, not using reference routine, over-engineering simple flows

---

##  REFERENCES

**ISO 14229-1:** UDS Service 0x31 - RoutineControl
**AUTOSAR:** Classic Platform Diagnostic Communication Manager
**Headers:** `RBAPLCUST_RoutineControl.h`, `RBAPLCUST_Global.h`
**Reference:** `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_RoutineControl_IPB*.c`

