# Service 2E: WriteDataByIdentifier - CT Instructions

> ** REFERENCE TEMPLATE:** Replace DIDs, data values, and verification steps with your actual write specifications.

## Overview

Service 2E (WriteDataByIdentifier) writes data to the ECU using Data Identifiers (DIDs).

**Standard:** ISO 14229-1 | **Service ID:** 0x2E | **Response ID:** 0x6E  
** Base Patterns:** [ct00-base-common.instructions.md](./ct00-base-common.instructions.md)

**Standard:** ISO 14229-1 (UDS)  
**Service ID:** 0x2E  
**Response ID:** 0x6E

---

## Standard Format

### Request
```
[0x2E] [DID High] [DID Low] [Data Bytes...]
Example: 2E FD 1A 01 (Write value 0x01 to DID 0xFD1A)
```

### Positive Response
```
[0x6E] [DID High] [DID Low]
Example: 6E FD 1A
```

### Common NRCs
- **0x13**: IncorrectMessageLengthOrInvalidFormat
- **0x31**: RequestOutOfRange - Invalid DID or data
- **0x33**: SecurityAccessDenied - Security required
- **0x7F**: ServiceNotSupportedInActiveSession - Wrong session

---

##  KEY TEST PATTERN

```c
SWTEST void TC_2E_<DID>_01(void)
{
    uint8 seed[8] = {0};
    
    SWT_RunSystemMS(10000);
    
    /* Enter Extended Session */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    HSWFT_DiagDelayMS("UDS", 3750);
    
    /* Unlock security if required */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed"));
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
    calculate_key(seed, 1);
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 02", key, 2, "Unlock Security"));
    SWT_RunSystemMS(1500);
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "67 02", 2));
    SWT_RunSystemMS(100);
    
    /* Write DID */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "2E FD 1A 01", "Write Value"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "6E FD 1A", 3));
    
    /* Read back to verify */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "22 FD 1A", "Read Back"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "62 FD 1A 01", 4));
}
```

---

##  TEST COVERAGE CHECKLIST

- [ ] Positive: Write and read-back verification
- [ ] Session: Extended session required
- [ ] Security: NRC 0x33 without security
- [ ] NRC 0x31: Invalid data values (out of range)
- [ ] NRC 0x13: Wrong message length
- [ ] Persistence: Value persists after power cycle (if applicable)
- [ ] Boundary: Test min/max values
- [ ] Default: Return to Default session behavior

---

##  CRITICAL REQUIREMENTS

**Session & Security:**
- Extended Session required (NRC 0x7F in Default)
- Security unlock usually required (NRC 0x33 without)
- Some DIDs may work in Default session

**Verification:**
- Always read back with Service 0x22
- Verify written value matches
- Test persistence after power cycle (if NvM)

**Data Validation:**
- Test min/max boundaries
- Test invalid values (NRC 0x31)
- Test wrong data length (NRC 0x13)

See [Base Instructions](./ct00-base-common.instructions.md) for common patterns.

**END OF SERVICE 2E INSTRUCTIONS**
