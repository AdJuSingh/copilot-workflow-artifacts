# Service 14: ClearDiagnosticInformation - CT Instructions

##  ESSENTIALS

**Service:** 0x14 ClearDiagnosticInformation | **Response:** 0x54  
**Standard:** ISO 14229-1 (UDS)  
**Group:** 0xFFFFFF (clear all DTCs)  
**Critical:**  10 second delay for NvM write  
** Patterns:** [ct00-base-common.instructions.md - Section 7.5](./ct00-base-common.instructions.md#75-dtc-management-pattern)

> ** TEMPLATE:** Replace DTC groups and timing with actual specs.

---

##  REQUEST/RESPONSE FORMAT

### **Request**
```
[0x14] [Group High] [Group Mid] [Group Low]
14 FF FF FF  - Clear all DTCs
```

### **Positive Response**
```
[0x54]
54  - Success
```

### **Common NRCs**
- **0x13** - IncorrectMessageLengthOrInvalidFormat
- **0x31** - RequestOutOfRange (invalid DTC group)

---

##  KEY TEST PATTERN

```c
SWTEST void TC_14_01(void)
{
    SWT_RunSystemMS(10000);
    
    /* Report some DTCs */
    Dem_ReportErrorStatus(DemConf_DemEventParameter_TestDTC1, DEM_EVENT_STATUS_FAILED);
    Dem_ReportErrorStatus(DemConf_DemEventParameter_TestDTC2, DEM_EVENT_STATUS_FAILED);
    SWT_RunSystemMS(500);
    
    /* Enter Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Verify DTCs exist */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "19 01 05", "Count DTCs"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "59 01 FF 01 00 02", 6));  /* 2 DTCs */
    
    /* Clear all DTCs */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "14 FF FF FF", "Clear all DTC"));
    SWT_RunSystemMS(10000);  /* Important: Wait for NvM write */
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "54", 1));
    
    /* Verify DTCs cleared */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "19 01 05", "Count DTCs"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "59 01 FF 01 00 00", 6));  /* 0 DTCs */
}
```

---

##  TEST COVERAGE CHECKLIST

- [ ] Positive: Clear all DTCs (0xFFFFFF)
- [ ] Verification: DTC count before/after
- [ ] Sessions: Default and Extended
- [ ] NRC 0x31: Invalid DTC group
- [ ] NRC 0x13: Wrong message length
- [ ] Persistence: Verify after power cycle

---

##  CRITICAL REQUIREMENTS

**Timing:**
-  **10 second delay** after clear (NvM write time)
- Allow DEM to process before verification

**Verification:**
- Use Service 0x19 before and after
- Report test DTCs using `Dem_ReportErrorStatus()`
- Verify count returns to 0

**Session:**
- Works in Default Session (no Extended required)
- Group 0xFFFFFF clears all DTCs

See [Base Instructions](./ct00-base-common.instructions.md) for common patterns.

**END OF SERVICE 14 INSTRUCTIONS**
