# Service 28: CommunicationControl - CT Instructions

##  ESSENTIALS

**Service:** 0x28 CommunicationControl | **Response:** 0x68  
**Standard:** ISO 14229-1 (UDS)  
**Requirements:** Extended Session + Security Access  
**Control Types:** 0x00-0x03 (Enable/Disable RX/TX)  
**Comm Types:** 0x01 (Normal), 0x02 (NM), 0x03 (Both)  
** Patterns:** [ct00-base-common.instructions.md](./ct00-base-common.instructions.md)

> ** TEMPLATE:** Replace control/communication types with actual network config.

---

##  CONTROL TYPES

**Subfunctions:**
- **0x00** - EnableRxAndTx
- **0x01** - EnableRxAndDisableTx
- **0x02** - DisableRxAndEnableTx
- **0x03** - DisableRxAndTx

**Communication Types:**
- **0x01** - Normal communication messages
- **0x02** - Network management messages
- **0x03** - Both normal and network management

---

##  REQUEST/RESPONSE FORMAT

### **Request**
```
[0x28] [Control Type] [Communication Type]
28 00 01  - Enable RX/TX for normal messages
28 03 03  - Disable RX/TX for all
```

### **Positive Response**
```
[0x68] [Control Type]
68 00  - Success
```

### **Common NRCs**
- **0x13** - IncorrectMessageLengthOrInvalidFormat
- **0x31** - RequestOutOfRange (invalid control/comm type)
- **0x33** - SecurityAccessDenied (security required)
- **0x7F** - ServiceNotSupportedInActiveSession

---

##  KEY TEST PATTERN

```c
SWTEST void TC_28_01(void)
{
    uint8 seed[8] = {0};
    
    SWT_RunSystemMS(10000);
    
    /* Extended Session + Security */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 01", "Default Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 01 00 32 01 F4", 6));
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "10 03", "Extended Session"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "50 03 00 32 01 F4", 6));
    HSWFT_DiagDelayMS("UDS", 3750);
    
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "27 01", "Request Seed"));
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagReadSecurityResponse("UDS", "67 01", seed, 2));
    calculate_key(seed, 1);
    SWT_RunSystemMS(1000);
    SWT_Eval(HSWFT_DiagSendSecurityUnlock("UDS", "27 02", key, 2, "Unlock"));
    SWT_RunSystemMS(1500);
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "67 02", 2));
    
    /* Enable RX and TX */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "28 00 01", "Enable RX/TX - Normal"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "68 00", 2));
}
```

---

##  TEST COVERAGE CHECKLIST

- [ ] Positive: All control types (0x00-0x03)
- [ ] Communication types: 0x01 (Normal), 0x02 (NM), 0x03 (Both)
- [ ] Security: NRC 0x33 without security
- [ ] Session: NRC 0x7F in Default session
- [ ] NRC 0x31: Invalid control/comm type
- [ ] NRC 0x13: Wrong message length
- [ ] Restore: Re-enable communication after test

---

##  CRITICAL REQUIREMENTS

**Prerequisites:**
- Extended Session required (NRC 0x7F in Default)
- Security Access required (NRC 0x33 without unlock)
- Test both requirements independently

**Test Matrix:**
- Test all 4 control types (0x00-0x03)
- Test all 3 communication types (0x01-0x03)
- Verify network behavior changes

**Cleanup:**
- Always restore communication (0x28 0x00 0x03)
- Verify network functional after test

See [Base Instructions](./ct00-base-common.instructions.md) for common patterns.

**END OF SERVICE 28 INSTRUCTIONS**
