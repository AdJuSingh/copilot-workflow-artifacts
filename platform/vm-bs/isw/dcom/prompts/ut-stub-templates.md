# Stub Templates & Header Patterns

## Minimal Header Stub Template

```c
/**
 * Auto-generated stub for: [HeaderName].h
 * Purpose: Enable compilation of [CFileName].c
 * Agent: BSW Compilation Agent
 * Date: [Current Date]
 */

#ifndef [HEADER_GUARD]
#define [HEADER_GUARD]

#include <stdint.h>
#include <stdbool.h>

/* Placeholder - will be populated based on compilation errors */

#endif /* [HEADER_GUARD] */
```

## Stub Organization Structure

```c
#ifndef HEADER_GUARD
#define HEADER_GUARD

/* Includes */
#include <stdint.h>

/* Typedefs */
typedef uint8_t ModuleName_TypeName;

/* Macros */
#define MODULE_CONSTANT  0x00

/* Enums */
typedef enum {
    EnumValue1 = 0,
    EnumValue2
} EnumName_t;

/* Structs */
typedef struct {
    uint16_t member1;
} StructName_t;

/* Function Declarations */
Std_ReturnType ModuleName_FunctionName(uint16_t param);

#endif /* HEADER_GUARD */
```

## Type Inference Rules

| Source Pattern | Inferred Type | Rationale |
|----------------|---------------|-----------|
| `if (func() == E_OK)` | `Std_ReturnType` | AUTOSAR standard return |
| `Type var = 0x01;` | `uint8_t` | Small hex value |
| `Type var = 0x1234;` | `uint16_t` | 16-bit hex value |
| `Type var = 0x12345678;` | `uint32_t` | 32-bit hex value |
| `Type_t* ptr;` | `typedef ... Type_t;` | Pointer usage |
| `struct.member == 0` | `uint16_t member;` | Member access in struct |
| Name contains "Type", "_t" | `typedef uint8_t [TypeName];` | Default to uint8_t |
| Name contains "16", "Word" | `typedef uint16_t [TypeName];` | 16-bit type |
| Name contains "32", "Long" | `typedef uint32_t [TypeName];` | 32-bit type |
| Name contains "Status", "Result" | `typedef uint8_t [TypeName];` | Status/Result type |
| Name contains "Ptr", "*" | `typedef void* [TypeName];` | Pointer type |

## AUTOSAR Standard Headers

### Platform_Types.h

```c
#ifndef PLATFORM_TYPES_H
#define PLATFORM_TYPES_H

typedef unsigned char       boolean;
typedef signed char         sint8;
typedef unsigned char       uint8;
typedef signed short        sint16;
typedef unsigned short      uint16;
typedef signed long         sint32;
typedef unsigned long       uint32;
typedef float               float32;
typedef double              float64;

typedef uint8               uint8_least;
typedef uint16              uint16_least;
typedef uint32              uint32_least;
typedef sint8               sint8_least;
typedef sint16              sint16_least;
typedef sint32              sint32_least;

#ifndef TRUE
#define TRUE    1
#endif

#ifndef FALSE
#define FALSE   0
#endif

#endif /* PLATFORM_TYPES_H */
```

### Std_Types.h

```c
#ifndef STD_TYPES_H
#define STD_TYPES_H

#include "Platform_Types.h"

typedef uint8 Std_ReturnType;

#define E_OK        ((Std_ReturnType)0x00)
#define E_NOT_OK    ((Std_ReturnType)0x01)

#define STD_HIGH    0x01
#define STD_LOW     0x00

#define STD_ACTIVE  0x01
#define STD_IDLE    0x00

#define STD_ON      0x01
#define STD_OFF     0x00

#endif /* STD_TYPES_H */
```

### Compiler.h

```c
#ifndef COMPILER_H
#define COMPILER_H

/* Memory class macros */
#define AUTOMATIC
#define TYPEDEF
#define STATIC static
#define INLINE inline

/* Pointer classes */
#define P2VAR(ptrtype, memclass, ptrclass)          ptrtype *
#define P2CONST(ptrtype, memclass, ptrclass)        const ptrtype *
#define CONSTP2VAR(ptrtype, memclass, ptrclass)     ptrtype * const
#define CONSTP2CONST(ptrtype, memclass, ptrclass)   const ptrtype * const
#define P2FUNC(rettype, ptrclass, fctname)          rettype (*fctname)

/* Function and variable qualifiers */
#define FUNC(rettype, memclass)                     rettype
#define VAR(vartype, memclass)                      vartype
#define CONST(consttype, memclass)                  const consttype

/* AUTOSAR memory classes */
#define DCM_APPL_CODE
#define DCM_APPL_DATA
#define DCM_INTERN_DATA

#endif /* COMPILER_H */
```

### Dcm.h (Diagnostic Communication Manager)

```c
#ifndef DCM_H
#define DCM_H

#include <stdint.h>

typedef uint8_t Std_ReturnType;
typedef uint8_t Dcm_SesCtrlType;
typedef uint8_t Dcm_OpStatusType;
typedef uint8_t Dcm_NegativeResponseCodeType;
typedef uint8_t Dcm_ProtocolType;
typedef uint8_t Dcm_SecLevelType;

/* Session types */
#define DCM_DEFAULT_SESSION             0x01
#define DCM_PROGRAMMING_SESSION         0x02
#define DCM_EXTENDED_DIAGNOSTIC_SESSION 0x03

/* Return codes */
#define E_OK                0x00
#define E_NOT_OK            0x01
#define DCM_E_PENDING       0x10

/* Negative response codes */
#define DCM_E_GENERALREJECT                         0x10
#define DCM_E_SERVICENOTSUPPORTED                   0x11
#define DCM_E_SUBFUNCTIONNOTSUPPORTED               0x12
#define DCM_E_INCORRECTMESSAGELENGTHORINVALIDFORMAT 0x13
#define DCM_E_CONDITIONSNOTCORRECT                  0x22
#define DCM_E_REQUESTOUTOFRANGE                     0x31
#define DCM_E_SECURITYACCESSDENIED                  0x33

/* Function declarations */
Std_ReturnType Dcm_GetSesCtrlType(Dcm_SesCtrlType* SesCtrlType);
Std_ReturnType Dcm_GetSecurityLevel(Dcm_SecLevelType* SecLevel);

#endif /* DCM_H */
```

### NvM.h (Non-volatile Memory Manager)

```c
#ifndef NVM_H
#define NVM_H

#include <stdint.h>

typedef uint8_t Std_ReturnType;
typedef uint16_t NvM_BlockIdType;
typedef uint8_t NvM_RequestResultType;

/* Return codes */
#define E_OK        0x00
#define E_NOT_OK    0x01

/* Request results */
#define NVM_REQ_OK              0x00
#define NVM_REQ_NOT_OK          0x01
#define NVM_REQ_PENDING         0x02
#define NVM_REQ_BLOCK_SKIPPED   0x03
#define NVM_REQ_NV_INVALIDATED  0x04
#define NVM_REQ_CANCELED        0x05
#define NVM_REQ_REDUNDANCY_FAILED 0x06
#define NVM_REQ_RESTORED_FROM_ROM 0x07

/* Function declarations */
Std_ReturnType NvM_ReadBlock(NvM_BlockIdType BlockId, void* NvM_DstPtr);
Std_ReturnType NvM_WriteBlock(NvM_BlockIdType BlockId, const void* NvM_SrcPtr);
Std_ReturnType NvM_GetErrorStatus(NvM_BlockIdType BlockId, NvM_RequestResultType* RequestResultPtr);
Std_ReturnType NvM_SetRamBlockStatus(NvM_BlockIdType BlockId, boolean BlockChanged);

#endif /* NVM_H */
```

## Macro Value Defaults

| Macro Pattern | Default Values |
|---------------|----------------|
| State/Status macros | Sequential: 0x00, 0x01, 0x02, ... |
| Error codes | High values: 0xFF, 0xFE, 0xFD, ... |
| Boolean flags | 0x00 (false), 0x01 (true) |
| Session IDs | Standard: 0x01, 0x02, 0x03, ... |

## Function Signature Inference

### AUTOSAR Standard Patterns

```c
/* Return types */
typedef uint8_t Std_ReturnType;
#define E_OK     0x00
#define E_NOT_OK 0x01

/* Common function patterns */
Std_ReturnType [Module]_Init(void);
Std_ReturnType [Module]_Write[Something]([IdType] Id, const [DataType]* Data);
Std_ReturnType [Module]_Read[Something]([IdType] Id, [DataType]* Data);
[StatusType] [Module]_GetStatus([IdType] Id);
```

### Pattern Matching for Headers

```
Type name pattern: [Prefix]_[Name]Type
→ Likely defined in: [Prefix].h or [Prefix]_Types.h

Examples:
- Dcm_SesCtrlType → Dcm.h or Dcm_Types.h
- NvM_BlockIdType → NvM.h or NvM_Types.h
- RBAPLCUST_StateType → RBAPLCUST_Global.h
```
