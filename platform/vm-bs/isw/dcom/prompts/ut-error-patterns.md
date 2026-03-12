# Common Error Patterns & Solutions

## Error Type Classification

### Type 1: Missing Header File

**Error Pattern:**
```
Error: RBAPLCUST_Config.h: No such file or directory
```

**Solution:** Create minimal stub header
```c
#ifndef RBAPLCUST_CONFIG_H__
#define RBAPLCUST_CONFIG_H__

#include <stdint.h>

#endif /* RBAPLCUST_CONFIG_H__ */
```

---

### Type 2: Undeclared Type/Typedef

**Error Pattern:**
```
Error: 'Dcm_SesCtrlType' undeclared
Error: unknown type name 'NvM_BlockIdType'
```

**Solution:** Add typedef to appropriate stub header

Apply type inference rules from `stub_templates.md`:
```c
/* In Dcm.h stub */
typedef uint8_t Dcm_SesCtrlType;
typedef uint8_t Dcm_OpStatusType;

/* In NvM.h stub */
typedef uint16_t NvM_BlockIdType;
typedef uint8_t NvM_RequestResultType;
```

---

### Type 3: Undeclared Function

**Error Pattern:**
```
Error: implicit declaration of function 'NvM_WriteBlock'
```

**Solution:** Add function declaration

1. Search source file for function usage
2. Infer signature from call site
3. Add declaration to stub

```c
/* Example: NvM_WriteBlock(Block_Id, Data) == E_OK */

/* In NvM.h stub */
Std_ReturnType NvM_WriteBlock(uint16_t BlockId, const uint8_t* NvMDataPtr);
```

---

### Type 4: Undeclared Macro/Constant

**Error Pattern:**
```
Error: 'DCM_DEFAULT_SESSION' undeclared
Error: 'C_InitWriteByPdm' undeclared
```

**Solution:** Add macro definition

```c
/* In Dcm.h */
#define DCM_DEFAULT_SESSION              0x01
#define DCM_PROGRAMMING_SESSION          0x02
#define DCM_EXTENDED_DIAGNOSTIC_SESSION  0x03

/* In DCOM_Types.h */
#define C_InitWriteByPdm        0x00
#define C_ProcessingWriteByPdm  0x01
#define C_DoneWriteByPdm        0x02
#define C_ErrorWriteByPdm       0xFF
```

---

### Type 5: Undeclared Enum

**Error Pattern:**
```
Error: 'DCOM_WriteNvmState_N' undeclared
```

**Solution:** Add enum definition

Search source for usage, infer enum values:
```c
/* Found: DCOM_WriteNvmState_N EepromState = C_InitWriteByPdm; */

typedef enum {
    C_InitWriteByPdm = 0,
    C_ProcessingWriteByPdm,
    C_DoneWriteByPdm,
    C_ErrorWriteByPdm
} DCOM_WriteNvmState_N;
```

---

### Type 6: Undeclared Struct/Union

**Error Pattern:**
```
Error: storage size of 'l_NMSG_VehicleSpeed_KMH_ST' isn't known
```

**Solution:** Add struct definition

Search for member access, infer structure:
```c
/* Found: l_NMSG_VehicleSpeed_KMH_ST.VehicleSpeed_UW == 0x0000 */

typedef struct {
    uint16_t VehicleSpeed_UW;
} NMSG_VehicleSpeed_KMH_ST;
```

---

## Complex Scenarios

### Scenario 1: Cascading Missing Headers

**Problem:** Header A includes Header B, causing chain

**Symptom:**
```
Error: RBAPLCUST_Global.h: No such file
[After creating stub]
Error: CM_Basetypes_COMMON.h: No such file
```

**Solution:** Create chain of stubs
```c
/* RBAPLCUST_Global.h stub */
#ifndef RBAPLCUST_GLOBAL_H__
#define RBAPLCUST_GLOBAL_H__

#include <stdint.h>
#include "CM_Basetypes_COMMON.h"  /* Include dependency */

/* Content */

#endif
```

---

### Scenario 2: Circular Dependencies

**Problem:** Header A includes B, B includes A

**Symptom:**
```
Error: Redefinition of 'Type_t'
Error: Multiple definitions
```

**Solution:** Use forward declarations
```c
/* In Header A stub */
typedef struct StructB_tag StructB_t;  /* Forward declaration */

typedef struct {
    StructB_t* ptr;  /* Pointer usage OK */
} StructA_t;

/* In Header B stub */
typedef struct StructA_tag StructA_t;  /* Forward declaration */

typedef struct StructB_tag {
    StructA_t* ptr;
} StructB_t;
```

---

### Scenario 3: Complex Macro Definitions

**Problem:** Source uses macros with arguments

**Symptom:**
```
Error: 'RB_ASSERT_SWITCH_SETTINGS' undeclared
```

**Solution:** Create empty macro for compilation
```c
#define RB_ASSERT_SWITCH_SETTINGS(name, val1, val2)  /* Empty */
#define RBMESG_DefineMESGDef(msg)                    /* Empty */
```

**Note:** These macros often do static analysis/assertions not needed for compilation.

---

### Scenario 4: Conditional Compilation

**Problem:** Source uses `#if`, `#ifdef` directives

**Symptom:**
```
Error: 'RBFS_RBAPLCUSTEcuReset' undeclared
```

**Source:**
```c
#if(RBFS_RBAPLCUSTEcuReset == RBFS_RBAPLCUSTEcuReset_OneBoxMainSystem)
    #include "RBMIC_InterCom_IswInterface.h"
#endif
```

**Solution:** Define configuration macros
```c
#define RBFS_RBAPLCUSTEcuReset                     1
#define RBFS_RBAPLCUSTEcuReset_ON                  1
#define RBFS_RBAPLCUSTEcuReset_OneBoxMainSystem    2

/* Set default to enable compilation */
#define RBFS_RBAPLCUSTEcuReset  RBFS_RBAPLCUSTEcuReset_ON
```

---

### Scenario 5: AUTOSAR RTE Types

**Problem:** AUTOSAR Runtime Environment types

**Symptom:**
```
Error: 'VAR' undeclared
Error: 'FUNC' undeclared
Error: 'CONSTP2VAR' undeclared
```

**Solution:** Define AUTOSAR memory class macros (see `stub_templates.md` Compiler.h)

**Usage:**
```c
/* Source: */
FUNC(Std_ReturnType, DCM_APPL_CODE) MyFunction(
    VAR(uint8, AUTOMATIC) param,
    CONSTP2VAR(uint8, AUTOMATIC, DCM_APPL_DATA) dataOut
)

/* Expands to: */
Std_ReturnType MyFunction(uint8 param, uint8 * const dataOut)
```

---

### Scenario 6: Measurement/Calibration Blocks

**Problem:** Measurement block comments

**Symptom:**
```
/*[[MEASUREMENT*/
/*NAME=VariableName*/
/*DATA_TYPE=UBYTE*/
/*]]MEASUREMENT*/
```

**Solution:** NO ACTION - These are comments, ignore them

---

## Troubleshooting

### Issue: Same Error Repeats 3+ Times

**Diagnosis:**
- Stub file not saved correctly
- Stub file not in include path
- Wrong header file chosen
- Typo in type names

**Solution:**
1. Verify stub location: `UT_xxx\api\stubs\`
2. Check batch file includes: `-Iapi\stubs`
3. Verify header guard matches filename
4. Check for typos in declarations

---

### Issue: Too Many Errors (>50)

**Diagnosis:**
- Source file very complex
- Many AUTOSAR dependencies

**Solution:**
1. Create common AUTOSAR stubs first:
   - `Platform_Types.h`
   - `Compiler.h`
   - `Std_Types.h`
2. Batch create stubs for all includes
3. Add content iteratively

---

### Issue: Linking Errors

**Symptom:**
```
Error: undefined reference to 'FunctionName'
```

**Diagnosis:**
- Compilation succeeded
- Linking failed (out of scope)

**Solution:**
- Add function declaration to stub header
- NO implementation needed (linking is later phase)
