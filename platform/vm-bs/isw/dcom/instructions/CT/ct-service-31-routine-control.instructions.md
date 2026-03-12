# Service 31: RoutineControl - CT Instructions

##  ESSENTIALS

**Service:** 0x31 RoutineControl | **Response:** 0x71  
**Standard:** ISO 14229-1 (UDS)  
**Subfunctions:** 0x01 (Start), 0x02 (Stop), 0x03 (Request Results)  
**Requirements:** Extended Session + Security (usually)  
**Sequence:** Start  Results  Stop  
** Patterns:** [ct00-base-common.instructions.md](./ct00-base-common.instructions.md)

> ** TEMPLATE:** Replace RIDs, parameters, responses with actual routine specs.

---

##  SUBFUNCTIONS

**Routine Operations:**
- **0x01** - Start Routine (begin execution)
- **0x02** - Stop Routine (halt execution)
- **0x03** - Request Routine Results (get status/data)

**Typical Flow:**
```
1. Start (0x01)  Begin routine
2. Wait  Allow execution time
3. Results (0x03)  Check status/data
4. Stop (0x02)  Terminate routine
```

---

##  REQUEST/RESPONSE FORMAT

### **Start Routine (0x01)**
```
[0x31] [0x01] [RID High] [RID Low] [Option Bytes...]
31 01 F0 03 01  - Start RID 0xF003 with param 0x01

Response: 71 01 F0 03 [Status]
```

### **Request Results (0x03)**
```
[0x31] [0x03] [RID High] [RID Low]
31 03 F0 03  - Get results for RID 0xF003

Response: 71 03 F0 03 [Result Data]
```

### **Stop Routine (0x02)**
```
[0x31] [0x02] [RID High] [RID Low]
31 02 F0 03  - Stop RID 0xF003

Response: 71 02 F0 03
```

### **Common NRCs**
- **0x13** - IncorrectMessageLengthOrInvalidFormat
- **0x24** - RequestSequenceError (wrong sequence)
- **0x31** - RequestOutOfRange (invalid RID/parameters)
- **0x33** - SecurityAccessDenied
- **0x7F** - ServiceNotSupportedInActiveSession

---

##  KEY TEST PATTERN

```c
SWTEST void TC_31_<RID>_01(void)
{
    uint8 seed[8] = {0};
    
    /* Setup MESG signals if needed */
    RBMESG_DefineMESGDef(<RequiredSignals>);
    l_<Signal>.Qualifier = 0x00;
    l_<Signal>.Value = <Value>;
    RBMESG_SendMESGDef(<Signal>);
    
    SWT_RunSystemMS(10000);
    
    /* Extended session + Security */
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
    SWT_RunSystemMS(100);
    
    /* Start Routine */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 01 F0 03 01", "Start Routine"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "71 01 F0 03 00", 5));
    
    SWT_RunSystemMS(5000);  /* Allow routine to execute */
    
    /* Request Results */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 03 F0 03", "Request Results"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "71 03 F0 03 [Result Bytes]", Length));
    
    /* Stop Routine */
    SWT_Eval(HSWFT_DiagSendRequest("UDS", "31 02 F0 03", "Stop Routine"));
    SWT_Eval(HSWFT_DiagEvalResponse("UDS", "71 02 F0 03", 4));
}
```

---

##  TEST COVERAGE CHECKLIST

- [ ] Positive: Complete sequence (Start  Results  Stop)
- [ ] NRC 0x24: Stop without start
- [ ] NRC 0x24: Results without start
- [ ] NRC 0x31: Invalid RID
- [ ] NRC 0x31: Invalid parameters
- [ ] NRC 0x13: Wrong message length
- [ ] Conditions: Prerequisite signals/states
- [ ] Timing: Execution delay between start and results

---

##  CRITICAL REQUIREMENTS

**Sequence Control:**
-  Correct: Start  Wait  Results  Stop
-  NRC 0x24: Stop before start
-  NRC 0x24: Results before start
- Test all invalid sequences

**Prerequisites:**
- Extended Session required
- Security Access required (usually)
- Setup prerequisite signals using MESG
- Verify conditions before routine start

**Timing:**
- Allow execution time after start (5000ms typical)
- Poll results multiple times if needed
- Some routines may be long-running

See [Base Instructions](./ct00-base-common.instructions.md) for common patterns.

**END OF SERVICE 31 INSTRUCTIONS**
