# Component Test (CT) Instructions - Master Index

##  DCOM Test Script Generation Guide

> ** TEMPLATE LIBRARY:** All code examples, values, signals are illustrative. Replace with actual project details.

---

##  QUICK START

**New to CT testing?**
1. **Start:** [Base Common Instructions](./ct00-base-common.instructions.md) - Pattern library
2. **Choose:** Your service from tables below
3. **Follow:** Service-specific template
4. **Reference:** [Comprehensive Guide](./ct-test-generation.instructions.md) for deep dives

** Example Tests:** `rb\as\ms\core\app\dcom\RBDcmSim\DCOMSIM\CT_Generator\tst\TestScripts\Platform_Testscript\`

---

##  INSTRUCTION DOCUMENTS

### **Foundation**

| Document                                                               | Purpose                           | Use When                |
| ---------------------------------------------------------------------- | --------------------------------- | ----------------------- |
| **[ct00-base-common.instructions.md](./ct00-base-common.instructions.md)** | Pattern library (headers, timing, signals) | **Start here** - All services |
| **[ct-test-generation.instructions.md](./ct-test-generation.instructions.md)** | Comprehensive reference guide | Need deep context       |

---

### **UDS Services (ISO 14229-1)**

| Service  | Document                                                               | Description                        |
| -------- | ---------------------------------------------------------------------- | ---------------------------------- |
| **0x10** | **[Service 10](./ct-service-10-diagnostic-session-control.instructions.md)**         | Session management                 |
| **0x14** | **[Service 14](./ct-service-14-clear-dtc.instructions.md)**                         | Clear DTCs                         |
| **0x19** | **[Service 19](./ct-service-19-read-dtc.instructions.md)**                          | Read DTC information               |
| **0x22** | **[Service 22](./ct-service-22-read-data.instructions.md)**                         | Read data by identifier            |
| **0x27** | **[Service 27](./ct-service-27-security-access.instructions.md)**                   | Security access (seed-key)         |
| **0x28** | **[Service 28](./ct-service-28-communication-control.instructions.md)**             | Communication control              |
| **0x2E** | **[Service 2E](./ct-service-2e-write-data.instructions.md)**                        | Write data by identifier           |
| **0x31** | **[Service 31](./ct-service-31-routine-control.instructions.md)**                   | Routine control                    |

---

### **OBD Services (SAE J1979)**

| Category         | Document                                               | Description                   |
| ---------------- | ------------------------------------------------------ | ----------------------------- |
| **OBD Classic**  | **[OBD Classic](./ct-obd-classic.instructions.md)**    | Traditional OBD-II (Services 01-09) |
| **OBD on UDS**   | **[OBD on UDS](./ct-obd-on-uds.instructions.md)**       | OBD via UDS (Service 22 + DIDs) |

---

##  QUICK LOOKUP BY USE CASE

**Session Management**  [Service 10](./ct-service-10-diagnostic-session-control.instructions.md)  
**Security/Access**  [Service 27](./ct-service-27-security-access.instructions.md)  
**Read ECU Data**  [Service 22](./ct-service-22-read-data.instructions.md) | [OBD Classic](./ct-obd-classic.instructions.md) | [OBD on UDS](./ct-obd-on-uds.instructions.md)  
**Write ECU Data**  [Service 2E](./ct-service-2e-write-data.instructions.md)  
**DTC Management**  [Service 14](./ct-service-14-clear-dtc.instructions.md) | [Service 19](./ct-service-19-read-dtc.instructions.md)  
**Routine Execution**  [Service 31](./ct-service-31-routine-control.instructions.md)  
**Network Control**  [Service 28](./ct-service-28-communication-control.instructions.md)

---

##  STANDARD TEST COVERAGE

**Target:** 15-20+ test cases per service/DID/RID/PID

### **Positive Scenarios (5+)**
- [ ] Valid operation in correct session
- [ ] Valid operation in alternate session (if supported)
- [ ] Multiple sequential operations
- [ ] Typical use case scenarios
- [ ] Expected data format verification

###  Negative Scenarios (6+)
- [ ] NRC 0x13: IncorrectMessageLengthOrInvalidFormat (too short, too long)
- [ ] NRC 0x31: RequestOutOfRange (invalid parameters)
- [ ] NRC 0x33: SecurityAccessDenied (if security required)
- [ ] NRC 0x7F: ServiceNotSupportedInActiveSession (wrong session)
- [ ] NRC 0x24: RequestSequenceError (if sequence matters)
- [ ] Service-specific NRCs (0x35, 0x37, etc..)

###  Session Management (3+)
- [ ] Correct session requirement verification
- [ ] Session transition handling
- [ ] Session timeout behavior (if applicable)

###  Boundary & Edge Cases (3+)
- [ ] Minimum valid value
- [ ] Maximum valid value
- [ ] Invalid/Not Available indicator (0xFFFF, etc.)

###  Additional (if applicable)
- [ ] Signal qualifier testing (valid vs. invalid)
- [ ] Timing requirements (P2, S3, power-on delays)
- [ ] Data persistence (power cycle)
- [ ] Security level requirements
- [ ] Prerequisite conditions

### **Negative Scenarios (8+)**
- [ ] NRC 0x13: Incorrect message length
- [ ] NRC 0x31: Request out of range
- [ ] NRC 0x33: Security access denied
- [ ] NRC 0x7F: Service not supported in session
- [ ] NRC 0x24: Request sequence error
- [ ] Additional service-specific NRCs

### **Boundary & Edge Cases (3+)**
- [ ] Minimum valid values
- [ ] Maximum valid values
- [ ] Invalid/not available data

### **Session & Timing (2+)**
- [ ] Session timeout behavior
- [ ] Sequential operations

---

##  NAMING CONVENTIONS

### **File Names**
```
DCOM_SWT_<ServiceCategory>_<ServiceName>_<Identifier>.c
```

**Examples:**
- `DCOM_SWT_Service22_WheelSpeedInformation.c`
- `DCOM_SWT_Service31_Dynamictest_F003.c`
- `DCOM_SWT_OBDclassic_Service01_EngineRPM_PID0C.c`

### **Test Case Names**
```c
TC_<Service>_<ID>_<SequenceNumber>
```

**Examples:**
- `TC_22_FD00_01` - Service 22, DID 0xFD00, test #1
- `TC_31_F003_01` - Service 31, RID 0xF003, test #1
- `TC_01_0C_01` - OBD Service 01, PID 0x0C, test #1

---

##  QUICK PATTERN REFERENCE

> ** Complete patterns:** [ct00-base-common.instructions.md - Section 7](./ct00-base-common.instructions.md#7-code-patterns)

**Session:**
- `10 01` (Default)  `50 01 00 32 01 F4`
- `10 03` (Extended)  `50 03 00 32 01 F4`

**Security:**
- `27 01` (Seed)  Calculate  `27 02` (Key)  `67 02`

**Signal:**
- Define  Set fields  Send  Wait 10000ms

**Read:**
- `22 <DID>`  `62 <DID> <Data>`

**Write:**
- `2E <DID> <Data>`  `6E <DID>`

**Routine:**
- `31 01 <RID>` (Start)  `31 03 <RID>` (Results)  `31 02 <RID>` (Stop)

---

##  TOOL INFORMATION

**CT Generator Tool:**
- Automates test script generation
- Location: `rb\as\ms\core\app\dcom\RBDcmSim\DCOMSIM\CT_Generator\`

**Test Execution:**
- Framework: SwTest (HSWFT)
- Environment: DCOMSim or actual ECU
- Test Lists: `testlist.txt`

---

##  TIMING REFERENCE

> ** Complete details:** [ct00-base-common.instructions.md - Appendix D](./ct00-base-common.instructions.md#appendix-d-typical-timing-values)

**Key Values:**
- Init: 10000ms
- Session timeout: 5000ms
- DTC clear wait: 10000ms
- Delays: 250/1000ms

---

##  QUICK NRC REFERENCE

> ** Complete list:** [ct00-base-common.instructions.md - Appendix B](./ct00-base-common.instructions.md#appendix-b-standard-nrc-codes)

| NRC  | Name                    | Common Cause          |
| ---- | ----------------------- | --------------------- |
| 0x13 | IncorrectLength         | Wrong message length  |
| 0x24 | RequestSequenceError    | Wrong sequence        |
| 0x31 | RequestOutOfRange       | Invalid parameter     |
| 0x33 | SecurityAccessDenied    | Security not unlocked |
| 0x7F | ServiceNotSupported     | Wrong session         |

---

##  BEST PRACTICES

**DO:**
- Start with base instructions
- Use 10000ms stabilization
- Verify session state
- Test positive + negative
- Include boundary testing
- Read-back after write
- Wait 10000ms after DTC clear
- Proper MESG signal setup
- Document requirements
- Group related tests

**DON'T:**
- Skip stabilization time
- Forget security unlock
- Assume session state
- Ignore timing
- Test only happy paths
- Use hardcoded seeds
- Skip power-on delays
- Forget NRC testing
- Leave tests uncommented

---

##  RELATED DOCUMENTATION

**Requirements:**
- `doc/requirements/requirements.csv`
- `doc/requirements/DEM_Requirements.md`

**Design:**
- `doc/design/` - Design files
- `Diamant__FW__Generated.xml`

**Configuration:**
- `Cfg_Build_Master.bcfg`
- `Cfg_Configurations.xml`
- `_metadata/mic/`

---

##  DOCUMENT NAVIGATION

**Foundation:**
- [Base Common Instructions](./ct00-base-common.instructions.md)
- [Comprehensive Guide](./ct-test-generation.instructions.md)

**UDS Services:**
- [Service 10: SessionControl](./ct-service-10-diagnostic-session-control.instructions.md)
- [Service 14: ClearDTC](./ct-service-14-clear-dtc.instructions.md)
- [Service 19: ReadDTC](./ct-service-19-read-dtc.instructions.md)
- [Service 22: ReadData](./ct-service-22-read-data.instructions.md)
- [Service 27: SecurityAccess](./ct-service-27-security-access.instructions.md)
- [Service 28: CommunicationControl](./ct-service-28-communication-control.instructions.md)
- [Service 2E: WriteData](./ct-service-2e-write-data.instructions.md)
- [Service 31: RoutineControl](./ct-service-31-routine-control.instructions.md)

**OBD Services:**
- [OBD Classic](./ct-obd-classic.instructions.md)
- [OBD on UDS](./ct-obd-on-uds.instructions.md)

---

** You are here: ct-index.instructions.md (Master Index)**

---

**END OF MASTER INDEX**
