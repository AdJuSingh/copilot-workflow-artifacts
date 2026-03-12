# Service 19: ReadDTCInformation - CT Instructions

##  ESSENTIALS

**Service:** 0x19 ReadDTCInformation | **Response:** 0x59  
**Standard:** ISO 14229-1 (UDS)  
**Subfunctions:** 0x01 (count), 0x02 (read), 0x04 (snapshot), 0x06 (extended), 0x1A (supported)  
** Patterns:** [ct00-base-common.instructions.md - Section 7.5](./ct00-base-common.instructions.md#75-dtc-management-pattern)

> ** TEMPLATE:** Replace subfunctions, status masks, DTCs with actual config.

---

##  COMMON SUBFUNCTIONS

**Read Operations:**
- **0x01** - ReportNumberOfDTCByStatusMask (count)
- **0x02** - ReportDTCByStatusMask (retrieve all)
- **0x04** - ReportDTCSnapshotRecordByDTCNumber
- **0x06** - ReportDTCExtendedDataRecordByDTCNumber
- **0x1A** - ReportSupportedDTCExtDataRecord

---

##  REQUEST/RESPONSE FORMAT

### **Report Number (0x01)**
```
Request:  19 01 [Status Mask]
19 01 05  - Count active DTCs

Response: 59 01 FF 01 00 02  - 2 DTCs available
```

### **Report DTCs (0x02)**
```
Request:  19 02 [Status Mask]
19 02 FF  - Get all DTCs

Response: 59 02 FF [Status] [DTC1] [DTC1 Status] [DTC2] [DTC2 Status]...
```

### **Common NRCs**
- **0x13** - IncorrectMessageLengthOrInvalidFormat
- **0x31** - RequestOutOfRange (invalid subfunction)
- **0x7F** - ServiceNotSupportedInActiveSession

---

##  KEY TEST PATTERN

```c
SWTEST void TC_19_01(void)
{
    SWT_RunSystemMS(10000);
    
    /* Report test DTCs */
    Dem_ReportErrorStatus(DemConf_DemEventParameter_TestDTC1, DEM_EVENT_STATUS_FAILED);
    Dem_ReportErrorStatus(DemConf_DemEventParameter_TestDTC2, DEM_EVENT_STATUS_FAILED);
    SWT_RunSystemMS(500);
    
    /* Enter Default Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_RunSystemMS(250);
    
    /* Count active DTCs */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "19 01 05", "Count Active DTCs"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "59 01 FF 01 00 02", 6));  /* 2 DTCs */
    
    /* Retrieve active DTCs */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "19 02 FF", "Retrieve All DTCs"));
    /* Response varies based on actual DTCs */
    /* Format: 59 02 FF [Status] [DTC bytes...] */
}
```

---

##  TEST COVERAGE CHECKLIST

- [ ] Subfunction 0x01: Count DTCs by status
- [ ] Subfunction 0x02: Retrieve DTCs by status
- [ ] Physical vs Functional addressing
- [ ] NRC 0x31: Invalid subfunction
- [ ] NRC 0x13: Wrong message length
- [ ] Empty case: No DTCs stored
- [ ] Multiple DTCs: Verify all reported
- [ ] Status masks: Test different masks

---

##  CRITICAL REQUIREMENTS

**DTC Setup:**
- Report DTCs using `Dem_ReportErrorStatus()`
- Allow 500ms after reporting
- Test with 0, 1, and multiple DTCs

**Addressing:**
- Test Physical ("UDS") and Functional addressing
- Both should return same DTC data

**Verification:**
- Count (0x01) should match retrieve (0x02)
- Status masks filter correctly
- DTC format: 3 bytes [High][Mid][Low]

See [Base Instructions](./ct00-base-common.instructions.md) for common patterns.

**END OF SERVICE 19 INSTRUCTIONS**
