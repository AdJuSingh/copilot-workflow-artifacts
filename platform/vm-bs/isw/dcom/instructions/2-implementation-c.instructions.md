# Instruction 2: C Code Implementation

##  ESSENTIALS

**File:** `RBAPLCUST_{ServiceType}_{DIDNumber}_{DIDName}.c`
**Input:** Design from `doc/design/DCOM_DID_{Number}_{Name}_DetailedDesign.uml`
**Header:** `RBAPLCUST_Global.h` (NEVER create separate headers per DID)
**Standards:** ISO 14229 (UDS), AUTOSAR 4.x, MISRA C
**Reference:** Study patterns in `rb/as/ms/core/app/dcom/RBAPLCust/src/`

---

##  PREREQUISITE: Design File Must Exist

**BEFORE implementation:** Verify `doc/design/DCOM_DID_{Number}_{Name}_DetailedDesign.uml` exists
- **If missing:** STOP and prompt user to create design first
- **If exists:** Proceed with implementation

**Service-Specific Instructions:**
- For Routine Control (0x31)  Use **[2b-implementation-routine-control.instructions.md](2b-implementation-routine-control.instructions.md)**
- For Input Output Control (0x2F)  Use **[2c-implementation-inputoutput-control.instructions.md](2c-implementation-inputoutput-control.instructions.md)**

---

##  6-STEP EXECUTION WORKFLOW

### **STEP 1: ANALYZE DESIGN**

**Review:** `.uml` file for API signatures, error handling, state machines, NVM integration
**Confirm:** Service type (0x22 RDBI, 0x2E WDBI, 0x2F IOC, 0x31 Routine, 0x27 Security)
**Extract:** Function names, parameters, return types, error codes, integration points
** Gate:** Complete understanding of design requirements

### **STEP 2: STUDY REFERENCE PATTERNS**

**Search:** `rb/as/ms/core/app/dcom/RBAPLCust/src/RBAPLCUST_{ServiceType}_*.c`
**Identify:** Naming conventions, buffer access patterns, error handling, NVM callbacks, thread safety
**Document:** Pattern deviations if required by design
** Gate:** Implementation approach defined

### **STEP 3: IMPLEMENT MAIN FUNCTION**

**Structure:**
- Requirements traceability header
- Standard includes (`Dcm.h`, `Std_Types.h`, `RBAPLCUST_Global.h`, `RBSYS.h`)
- Main service handler function
- Input validation (length, range)
- UDS error codes (0x13 Incorrect Length, 0x31 Out Of Range, 0x22 Conditions Not Correct)
- Data processing logic from design
- Return `E_OK` or `E_NOT_OK`

** Gate:** Main function complete with all error paths

### **STEP 4: ADD BACKGROUND PROCESSES (If Required)**

**For WDBI (0x2E) with NVM:**
- `PRC_DCOM_{Name}Status()` - State machine (IDLE  PENDING  SUCCESS/FAILED)
- `PRC_DCOM_{Name}withKeycycle_NMHandling()` - Network management monitoring
- Thread safety with `RBSYS_EnterCommonLock()` / `RBSYS_ExitCommonLock()`
- DEM event reporting on errors

** Gate:** Background processes implemented if design requires

### **STEP 5: ADD NVM CALLBACKS (If Required)**

**For WDBI (0x2E) with NVM persistence:**
- `RBAPLCUST_ReadCallback_{DID}_{Name}()` - NVM read completion
- `RBAPLCUST_WriteCallback_{DID}_{Name}()` - NVM write completion  
- `RBAPLCUST_ResultCallback_{DID}_{Name}()` - Operation result handling
- Static assertions for data structure validation
- Retry logic for failed operations

** Gate:** NVM integration complete if design requires

### **STEP 6: QUALITY GATE**

**Code Quality:**
- [ ] All functions in single `.c` file
- [ ] AUTOSAR macros used (`FUNC()`, `P2VAR()`, `P2CONST()`)
- [ ] Standard types (`uint8_t`, `Std_ReturnType`, `E_OK`, `E_NOT_OK`)
- [ ] Direct buffer access (`Data[0]`, `Data[1]`)
- [ ] Requirements traceability header present
- [ ] Zero compilation errors/warnings
- [ ] No hardcoded credentials or magic numbers
- [ ] Bounds checking on all array access
- [ ] Thread safety for shared globals

**Design Coverage:**
- [ ] 95-100% design element coverage
- [ ] All error paths implemented
- [ ] All state transitions handled
- [ ] UDS compliance verified

**Integration:**
- [ ] `RBAPLCUST_Global.h` updated if needed
- [ ] DCM compatibility verified
- [ ] Session transitions tested
- [ ] System APIs used correctly

** Final:** Ready for build and unit testing

---

##  CODE STYLE & CONVENTIONS

### **AUTOSAR Compliance**

```c
/* Function definition */
FUNC(Std_ReturnType, DCM_CODE) RBAPLCUST_RDBI_DID_F123_ExampleService(
    P2VAR(uint8, AUTOMATIC, DCM_VAR) Data)
{
    /* Standard types */
    uint8_t l_dataIndex = 0u;
    uint16_t l_valueBuffer = 0u;
    Std_ReturnType l_returnValue = E_OK;
    
    /* Implementation */
    
    return l_returnValue;
}
```

### **Naming Conventions**

**Variables:** `l_` (local), `g_` (global)
**Functions:** `RBAPLCUST_{ServiceName}_{Operation}`
**Messages:** `DefineMESGDef()`, `RcvMESGDef()`, `SendMESGDef()`

### **Buffer Access**

```c
/* Direct access - DCM handles service ID/DID */
Data[0] = highByte;
Data[1] = lowByte;

/* NO pointer arithmetic outside AUTOSAR macros */
```

### **Thread Safety**

```c
/* Critical section for shared globals */
RBSYS_EnterCommonLock();
g_SharedVariable = newValue;
RBSYS_ExitCommonLock();
```

### **Documentation**

```c
/**
 * @brief Read Data By Identifier - DID 0xF123 Example Service
 * @details Implements SWCS_DCOM_12345 through SWCS_DCOM_12350
 * @param[out] Data - Response buffer (DCM managed)
 * @return E_OK - Success | E_NOT_OK - Error (NRC set by DCM)
 * @requirements SWCS_DCOM_12345, SWCS_DCOM_12346
 */
FUNC(Std_ReturnType, DCM_CODE) RBAPLCUST_RDBI_DID_F123_ExampleService(
    P2VAR(uint8, AUTOMATIC, DCM_VAR) Data)
```

---

##  WDBI NVM INTEGRATION TEMPLATE

### **Main Handler with NVM**

```c
FUNC(Std_ReturnType, DCM_CODE) RBAPLCUST_WDBI_DID_F123_ExampleConfig(
    P2CONST(uint8, AUTOMATIC, DCM_VAR) Data,
    Dcm_OpStatusType OpStatus,
    P2VAR(Dcm_NegativeResponseCodeType, AUTOMATIC, DCM_VAR) ErrorCode)
{
    Std_ReturnType l_returnValue = E_NOT_OK;
    
    /* Input validation */
    if (Data[0] > MAX_VALUE) {
        *ErrorCode = DCM_E_REQUESTOUTOFRANGE; /* NRC 0x31 */
        return E_NOT_OK;
    }
    
    /* Store data globally for NVM write */
    RBSYS_EnterCommonLock();
    g_ConfigData = Data[0];
    g_WriteStatus = WRITE_PENDING;
    RBSYS_ExitCommonLock();
    
    /* Trigger NVM write */
    if (NvM_WriteBlock(NVM_BLOCK_ID, &g_ConfigData) == E_OK) {
        l_returnValue = E_OK;
    }
    
    return l_returnValue;
}
```

### **Background State Machine**

```c
FUNC(void, DCM_CODE) PRC_DCOM_ExampleConfigStatus(void)
{
    static uint8 l_retryCount = 0u;
    
    switch (g_WriteStatus) {
        case WRITE_PENDING:
            /* Wait for callback */
            break;
            
        case WRITE_SUCCESS:
            /* Reset state */
            g_WriteStatus = WRITE_IDLE;
            l_retryCount = 0u;
            break;
            
        case WRITE_FAILED:
            if (l_retryCount < MAX_RETRIES) {
                NvM_WriteBlock(NVM_BLOCK_ID, &g_ConfigData);
                l_retryCount++;
            } else {
                Dem_ReportErrorStatus(DEM_EVENT_ID, DEM_EVENT_STATUS_FAILED);
                g_WriteStatus = WRITE_IDLE;
                l_retryCount = 0u;
            }
            break;
    }
}
```

### **NVM Callbacks**

```c
FUNC(Std_ReturnType, NVM_CODE) RBAPLCUST_WriteCallback_DID_F123_ExampleConfig(
    NvM_ServiceIdType ServiceId,
    NvM_RequestResultType JobResult)
{
    RBSYS_EnterCommonLock();
    if (JobResult == NVM_REQ_OK) {
        g_WriteStatus = WRITE_SUCCESS;
    } else {
        g_WriteStatus = WRITE_FAILED;
    }
    RBSYS_ExitCommonLock();
    
    return E_OK;
}
```

---

##  IMPLEMENTATION RULES

### **DO:**
- Follow existing code style exactly
- Study reference implementations first
- Implement ALL functions in single `.c` file
- Use `RBAPLCUST_Global.h` for declarations
- Include requirements traceability
- Complete UDS error handling
- Bounds checking on all arrays
- Thread safety for shared data

### **DON'T:**
- Create separate header files per DID
- Over-document (minimal inline comments)
- Create test/make files (maintained separately)
- Add single-use helper functions
- Use placeholder comments like `/* TODO */`
- Hardcode credentials or magic numbers
- Use pointer arithmetic outside AUTOSAR macros

---

##  COMMON MISTAKES

**Standards:** Missing AUTOSAR macros, wrong types, unsafe pointers
**Naming:** Wrong conventions, separate headers per DID
**Buffer Access:** Pointer arithmetic, incorrect indexing
**Thread Safety:** Missing locks on shared globals
**Error Handling:** Incomplete UDS codes, missing NRC scenarios
**NVM Integration:** Missing callbacks, no retry logic, no static assertions
**Documentation:** Over-documenting, missing traceability, no rationale for deviations

---

##  REFERENCES

**ISO 14229-1:** UDS Services | **AUTOSAR 4.x:** Architecture & APIs | **MISRA C:** Safe Coding Standards
**Vector DaVinci:** Build System | **DCM Module:** Diagnostic Communication Manager
