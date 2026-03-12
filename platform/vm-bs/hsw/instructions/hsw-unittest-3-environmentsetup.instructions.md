---
applyTo: "**/tst/**/cfg/*.bcfg,**/tst/**/*Adaptor*.c,**/tst/**/*Adaptor*.h,**/tst/**/*Adapter*.c,**/tst/**/*Adapter*.h,**/tst/**/stub/**/*.c,**/tst/**/stub/**/*.h,**/tst/**/stubs/**/*.c,**/tst/**/stubs/**/*.h,**/tst/**/Stub/**/*.c,**/tst/**/Stub/**/*.h"
description: "HSW Unit Test environment preparation — creates bcfg, Adaptor.c/h, and stub files in one workflow"
---

# HSW Unit Test Environment Setup Guidelines

## Purpose

This instruction covers the **end-to-end preparation** of a new Unit Test (UT) environment for one HSW component feature.  
A complete UT environment consists of **three artefacts that must always be created together**:

| Artefact | Location | Covered by |
|----------|----------|------------|
| Build configuration (`.bcfg`) | `…/tst/…/<SubFeature>/cfg/T<COMPONENT><Feature>_BuildConfig.bcfg` | Section 2 |
| Adaptor (`.c` / `.h`) | `…/tst/…/<SubFeature>/T<COMPONENT>_<Feature>Adaptor.c/.h` | Section 3 |
| Stubs (`.c` / `.h`) | `…/tst/…/<SubFeature>/stubs/` and/or `…/tst/stub/` | Section 4 |

> **Rule:** Never generate one artefact in isolation. If only one file is explicitly requested, generate a minimal skeleton for the others as well so the build remains self-consistent.

> **Critical — Scan Before You Create:**  
> Folder layouts, naming conventions, adaptor prefix styles, stub directory names, and DEM stub styles **vary significantly** across HSW components. Before creating any file, you **must** scan the target component's existing `tst/` directory tree and read at least one existing `.bcfg`, adaptor, and stub file from the same component (or a sibling feature). Every new file must mirror the conventions already established in that component — never assume a fixed template. See **Step 0** in Section 5 for the full discovery procedure.

---

## 1. Folder Layout

### 1.1 Primary layout (ucbase modules: RBECM, RBTaskMon, RBADC, RBCDI)

```
<component>/tst/unit/<SubFeature>/
  cfg/
    T<COMPONENT><Feature>_BuildConfig.bcfg
  stubs/                                       ← feature-specific stubs
    T<COMPONENT>_<Dep>Stub.c
    T<COMPONENT>_<Dep>Stub.h
  T<COMPONENT>_<Feature>Adaptor.c
  T<COMPONENT>_<Feature>Adaptor.h

<component>/tst/unit/stubs/                    ← shared stubs (reused across features)
  T<COMPONENT>_ConfigStub.h
  T<COMPONENT>_ConfigElementsStub.h
  T<COMPONENT>_DEMStub.c
  T<COMPONENT>_DEMStub.h
```

**Real examples:**
- `rbecm/tst/unit/FailureReporting/cfg/TRBECMFailureReporting_BuildConfig.bcfg`
- `rbecm/tst/unit/SWTests/cfg/TRBECMSWTests_BuildConfig.bcfg`
- `rbtaskmon/tst/unit/TaskExecutionMonitor/cfg/TRBTaskMonExecutionMonitor_BuildConfig.bcfg`
- `rbcdi/tst/unit/TriggerAndSignalsHandling/cfg/TRBCDITriggerAndSignalsHandling_BuildConfig.bcfg`
- `rbadc/tst/unit/unit_TestConversion/cfg/TRBADC_TestConversion_BuildConfig.bcfg`

### 1.2 Alternate layout (application modules: RBEVP, RBWSS, RBePedal, RBHYDR, RBPTS, RBLIPS)

```
<component>/tst/unit_<Feature>/
  cfg/
    T<COMPONENT>_<Feature>_BuildConfig.bcfg    ← or T<COMPONENT>_<Feature>.bcfg
  stub/                                        ← feature-specific stubs (sometimes "Stub/")
    …
  T<COMPONENT>_<Feature>Adaptor.c              ← or T<COMPONENT>_<Feature>Adapter.c
  T<COMPONENT>_<Feature>Adaptor.h              ← or T<COMPONENT>_<Feature>Adapter.h

<component>/tst/stub/                          ← shared stubs (DEM, config, etc.)
  T<COMPONENT>_DEMStub.c
  T<COMPONENT>_DEMStub.h
  TDEMStub.c / TDEMStub.h                     ← generic DEM stub (RBePedal, RBPTS)
```

**Real examples:**
- `rbevp/tst/unit_UndervoltageMonitor/cfg/TRBEVP_Undervoltagemonitor.bcfg`
- `rbwss/tst/Unit_WSSTestApbAsic/cfg/TRBWSSTestApbAsic_BuildConfig.bcfg`
- `rbhydr/tst/unit_RfpecAdapter/cfg/TRBHYDR_RfpecAdapter_BuildConfig.bcfg`
- `rbepedal/tst/unit_ePedalSupplyMonitoring/cfg/TRBePedal_SupplyMonitoring_BuildConfig.bcfg`

### 1.3 Naming Patterns Summary

| Element | Convention | Real examples |
|---------|-----------|---------------|
| Top-level folder | `unit/<Feature>` or `unit_<Feature>` or `Unit_<Feature>` | `unit/FailureReporting`, `unit_SwitchingRelay`, `Unit_WSSTestApbAsic` |
| BCFG file name | `T<COMPONENT><Feature>_BuildConfig.bcfg` | `TRBECMSWTests_BuildConfig.bcfg`, `TRBPTS_PWM_BuildConfig.bcfg` |
| Adaptor `.c` | `T<COMPONENT>_<Feature>Adaptor.c` or `…_Adapter.c` | `TRBECM_FailureReporting_Adaptor.c`, `TRBePedal_SupplyMonitoringAdapter.c` |
| Stub folder | `stubs/` or `stub/` or `Stub/` | Varies by module — match existing convention |

---

## 2. Build Configuration File (`.bcfg`)

### 2.1 Mandatory Three-Module Structure

Every `.bcfg` must define exactly **three** sub-modules inside a top-level module. The sub-module names must be `UnitUnderTest`, `TestCase`, and `Stub`.

```
module "T<COMPONENT><Feature>"
{
  module "UnitUnderTest" {
    export {
      "/rb/as/<domain>/<component>/api/**";
    }
    files {
      c {
        "/rb/as/<domain>/<component>/tst/…/<SubFeature>/T<COMPONENT>_<Feature>Adaptor.c";
      }
    }
  } // UnitUnderTest

  module "TestCase" {
    files {
      c {
        "/rb/as/<domain>/<component>/tst/…/<SubFeature>/T<COMPONENT>_<Feature>.c";
      }
    }
  } // TestCase

  module "Stub" {
    export {
      "/rb/as/<domain>/<component>/tst/unit/stubs/**";
      "/rb/as/<domain>/<component>/tst/…/<SubFeature>/stubs/**";

      /** stub "RealHeader.h"   with "T<COMPONENT>_<Dep>Stub.h" */
    }
    files {
      c {
        "/rb/as/<domain>/<component>/tst/unit/stubs/*.c";
        "/rb/as/<domain>/<component>/tst/…/<SubFeature>/stubs/*.c";
      }
    }
  } // Stub

} // T<COMPONENT><Feature>
```

### 2.2 Real `.bcfg` Examples

**RBECM — FailureReporting** (`TRBECMFailureReporting_BuildConfig.bcfg`):
```
module "TRBECMFailureReporting"
{
  module "TestCase" {
    files {
      c {
        "/rb/as/core/hwp/hsw/ucbase/safety/rbecm/tst/unit/FailureReporting/TRBECM_FailureReporting.c";
      }
    }
  } // TestCase

  module "UnitUnderTest" {
    export {
      "/rb/as/core/hwp/hsw/ucbase/safety/rbecm/api/**";
    }
    files {
      c {
        "/rb/as/core/hwp/hsw/ucbase/safety/rbecm/tst/unit/FailureReporting/TRBECM_FailureReporting_Adaptor.c";
      }
    }
  } // UnitUnderTest

  module "Stub" {
    export {
      "/rb/as/core/hwp/hsw/ucbase/safety/rbecm/tst/unit/stubs/**";
      "/rb/as/core/hwp/hsw/ucbase/safety/rbecm/tst/unit/FailureReporting/stubs/**";

      /** stub "RBCMHSW_Locks.h"             with   "TRBECM_RBCMHSW_Stub.h" */
      /** stub "RBECM_Config.h"              with   "TRBECM_ConfigStub.h" */
      /** stub "RBSYS_RH850Regs.h"           with   "TRBECM_RBSYS_Stub.h" */
      /** stub "Dem.h"                       with   "TRBECM_Dem_Stub.h" */
      /** stub "RBHSWDEM_Facade.h"           with   "TRBECM_Dem_Stub.h" */
      /** stub "RBSYS_CpuInfo.h"             with   "TRBECM_RBSYS_Stub.h" */
    }
    files {
      c {
        "/rb/as/core/hwp/hsw/ucbase/safety/rbecm/tst/unit/FailureReporting/stubs/*.c";
      }
    }
  } // Stub
} // TRBECMFailureReporting
```

**RBTaskMon — TaskExecutionMonitor** (`TRBTaskMonExecutionMonitor_BuildConfig.bcfg`):
```
module "TRBTaskMonExecutionMonitor"
{
  module "TestCase" {
    files {
      c {
        "/rb/as/core/hwp/hsw/ucbase/safety/rbtaskmon/tst/unit/TaskExecutionMonitor/TRBTaskMon_TaskExecutionMonitor.c";
      }
    }
  } // TestCase

  module "UnitUnderTest" {
    export {
      "/rb/as/core/hwp/hsw/ucbase/safety/rbtaskmon/**/api/**";
      "/rb/as/core/hwp/hsw/ucbase/safety/rbtaskmon/src/";
    }
    files {
      c {
        "/rb/as/core/hwp/hsw/ucbase/safety/rbtaskmon/tst/unit/TaskExecutionMonitor/TRBTaskMon_TaskExecutionMonitorAdaptor.c"
      }
    }
  } // UnitUnderTest

  module "Stub" {
    export {
      "/rb/as/core/hwp/hsw/ucbase/safety/rbtaskmon/tst/unit/TaskExecutionMonitor/**";
      "/rb/as/core/hwp/hsw/ucbase/safety/rbtaskmon/tst/unit/stubs/**";

      /** Configure "TRBTaskMon_ConfigStub.h" from "TRBTaskMon_ConfigElementsStub.h": RBFS_Task0p5ms, RBFS_MCORE, RBFS_BUILDTYPE */
      /** stub "RBTaskMon_Config.h"   with "TRBTaskMon_ConfigStub.h" */
      /** stub "RBSYS_CpuInfo.h"      with "TRBTaskMon_RBSYS_CpuInfoStub.h" */
    }
    files {
      c {
        "/rb/as/core/hwp/hsw/ucbase/safety/rbtaskmon/tst/unit/stubs/*.c";
        "/rb/as/core/hwp/hsw/ucbase/safety/rbtaskmon/tst/unit/TaskExecutionMonitor/stubs/*.c";
      }
    }
  } // Stub
} // TRBTaskExecutionMonitor
```

> **No-adaptor variant (RBHYDR):** When the unit has external linkage only, put the production `.c` directly in `UnitUnderTest.files` — no adaptor needed. See Section 3.7.

### 2.3 Stub Mapping Syntax

Inside `Stub { export { … } }`, declare header replacements using TListGen comment syntax:

```
/** stub "RealHeader.h"         with "T<COMPONENT>_<Dep>Stub.h" */
```

**Rules:**
- One `/** stub … */` line per replaced header.
- Multiple real headers may map to the same stub header.
- `RBHSWDEM_Facade.h` and `Dem.h` must **always** be stubbed.
- When using feature switches, use the `/** Configure … from … */` directive:
  ```
  /** Configure "T<COMPONENT>_ConfigStub.h" from "T<COMPONENT>_ConfigElementsStub.h": RBFS_FeatureA, RBFS_FeatureB */
  /** stub "<COMPONENT>_Config.h"  with "T<COMPONENT>_ConfigStub.h" */
  ```

### 2.4 `UnitUnderTest` — Export Variations

The `export` block in `UnitUnderTest` may include multiple paths depending on the module structure:

| Pattern | When to use | Example module |
|---------|-------------|----------------|
| `api/**` only | Component has a flat API layer | RBECM, RBCDI |
| `api/**` + `src/` | Tests need internal headers from `src/` | RBTaskMon |
| `api/**` + `src/<sub>/` | Nested source sub-modules | RBHYDR |
| `src/**` + `api/**` | Tests access both source and API internals | RBEVP |

### 2.5 Module Order

Both orderings are observed in the codebase (either `UnitUnderTest` → `TestCase` → `Stub` or `TestCase` → `UnitUnderTest` → `Stub`). Follow the convention of the **existing tests in the same component**. When starting a new component, prefer `UnitUnderTest` → `TestCase` → `Stub`.

---

## 3. Adaptor Files

The adaptor gives tests white-box access to private (`static`) symbols.  
**The adaptor `.c` file must `#include` the production `.c` file directly.**

### 3.1 `T<COMPONENT>_<Feature>Adaptor.c`

```c
#include "T<COMPONENT>_<Feature>Adaptor.h"

#include "../src/<COMPONENT>_<Feature>.c"   /* grants access to all static symbols */

ReturnType CallPrivate_<COMPONENT>_<PrivateFunction>(ArgType arg)
{
  return <COMPONENT>_<PrivateFunction>(arg);
}

StateType GetPrivate_<COMPONENT>_<StateVar>(void)
{
  return <COMPONENT>_<StateVar>;
}

void SetPrivate_<COMPONENT>_<StateVar>(StateType value)
{
  <COMPONENT>_<StateVar> = value;
}
```

### 3.2 Real Adaptor Examples

**RBECM — FailureReporting** (`TRBECM_FailureReporting_Adaptor.c`):
```c
#include "TRBECM_FailureReporting_Adaptor.h"

#include "../src/RBECM_FailureReporting.c"

boolean GetPrivate_RBECM_isuCSafetyLogicFaultFailedReported(void)
{
  return RBECM_isuCSafetyLogicFaultFailedReported;
}

void SetPrivate_RBECM_isuCSafetyLogicFaultFailedReported(boolean status)
{
  RBECM_isuCSafetyLogicFaultFailedReported = status;
}

void CallPrivate_RBECM_uCSafetyLogicFaultGoodcheckHandler(void)
{
  RBECM_uCSafetyLogicFaultGoodcheckHandler();
}
```

**RBEVP — UndervoltageMonitor** (config-guard technique — pre-define include guard to intercept config header):
```c
// prevent original config header to be loaded
#define RBEVP_CONFIG_H__

#include "TRBEVP_Config.h"
#include "TRBEVP_ConfigElements.h"
#include "RBHSWDEM_Facade.h"
#include "TRBEVP_UndervoltageMonitorAdaptor.h"

#include "../../src/RBEVP_UndervoltageMonitor.c"

#if( RBFS_ElectronicVacuumPump == RBFS_ElectronicVacuumPump_TwoRelay )
uint8_t CallPrivate_ls_RBEVPUnderVoltcnt(void)
{
  return ls_RBEVPUnderVoltcnt;
}
#endif
```

> **Other naming conventions** (see Section 3.4 and Appendix A): RBCDI uses `CP_` prefix with `#if` wrappers; RBePedal uses `TRBePedal_set_`/`TRBePedal_get_` style; RBTaskMon mixes `CallPrivate_` with `TRBTaskMon_Set` wrappers.

### 3.3 `T<COMPONENT>_<Feature>Adaptor.h`

```c
#ifndef T<COMPONENT>_<FEATURE>ADAPTOR_H__
#define T<COMPONENT>_<FEATURE>ADAPTOR_H__

#include "Std_Types.h"
#include "<COMPONENT>_<Feature>.h"   /* public types needed by declarations */

/* Private function wrapper declarations */
extern ReturnType CallPrivate_<COMPONENT>_<PrivateFunction>(ArgType arg);

/* Internal state accessor declarations */
extern StateType GetPrivate_<COMPONENT>_<StateVar>(void);
extern void      SetPrivate_<COMPONENT>_<StateVar>(StateType value);

#endif /* T<COMPONENT>_<FEATURE>ADAPTOR_H__ */
```

**Real header examples:**

```c
/* TRBECM_FailureReporting_Adaptor.h */
#ifndef TRBECM_FAILUREREPORTING_ADAPTOR_H__
#define TRBECM_FAILUREREPORTING_ADAPTOR_H__

#include "Std_Types.h"
#include "TRBECM_RegisterDefines.h"

extern boolean GetPrivate_RBECM_isuCSafetyLogicFaultFailedReported(void);
extern void SetPrivate_RBECM_isuCSafetyLogicFaultFailedReported(boolean status);
extern void CallPrivate_RBECM_uCSafetyLogicFaultGoodcheckHandler(void);

#endif
```

### 3.4 Adaptor Naming Rules

Three naming conventions coexist in the codebase. Use whichever is already established in the component; for new components, prefer PascalCase prefixes.

| Access type | PascalCase prefix (preferred) | Alt: `T<COMPONENT>_set/get` style | Alt: `CP_` prefix |
|-------------|-------------------------------|------------------------------------|--------------------|
| Wrap `static` function | `CallPrivate_<COMPONENT>_<Func>` | — | `CP_<COMPONENT>_<Func>` |
| Read private variable | `GetPrivate_<COMPONENT>_<Var>` | `T<COMPONENT>_get<Var>` | `GP_<COMPONENT>_<Var>` |
| Write private variable | `SetPrivate_<COMPONENT>_<Var>` | `T<COMPONENT>_set<Var>` | — |

See Appendix A for per-module prefix examples.

### 3.5 Adaptor `.c` include path

The relative path from adaptor to production source varies by folder depth. Match the existing component convention:

| Layout | Include path from adaptor | Example module |
|--------|--------------------------|----------------|
| `tst/unit/<Feature>/` | `#include "../src/<File>.c"` | RBECM (1-level deep) |
| `tst/unit/<Feature>/` | `#include "../../../src/<File>.c"` | RBCDI (3-level deep) |
| `tst/unit_<Feature>/` | `#include "../../src/<File>.c"` | RBePedal, RBEVP |

### 3.6 Advanced: Config-Guard Technique

When the production source includes a config header that must be intercepted _before_ the `.c` inclusion, pre-define its include guard to prevent loading the real header. See the **RBEVP example** in Section 3.2 for a complete demonstration.

### 3.7 When the Adaptor Is Not Needed

If the function under test has **external linkage** and no internal state access is required (e.g. RBHYDR), the production `.c` goes directly in the `UnitUnderTest` module of the `.bcfg` — no adaptor file is created.

---

## 4. Stub Files

### 4.1 Stub Directory Organisation

Two models are observed across the codebase:

**Centralised model** (RBECM, RBTaskMon, RBCDI):
```
tst/unit/stubs/              ← shared stubs (DEM, config, RBSYS)
tst/unit/<Feature>/stubs/    ← feature-specific stubs
```

**Distributed model** (RBADC, RBWSS):
```
tst/unit/stub/               ← shared stubs
tst/unit/stub/genCfg/        ← generated configuration stubs
tst/unit/stub/intern/        ← internal stubs
tst/unit/stub/RbConfig/      ← project config stubs
tst/unit/unit_<Feature>/stub/ ← per-feature stubs
```

**Flat model** (RBEVP, RBePedal, RBHYDR):
```
tst/stub/                    ← single shared stub folder for all features
```

Match the existing stub directory structure of the component.

### 4.2 Per-Dependency Stub Pattern

#### Header `T<COMPONENT>_<Dep>Stub.h`:

```c
#ifndef T<COMPONENT>_<DEP>STUB_H__
#define T<COMPONENT>_<DEP>STUB_H__

#include "Std_Types.h"

/* Return value controllable by the test */
extern ReturnType  tstub_ret_<Dep>_<Function>;
/* Captured input argument */
extern InputType   tstub_par_<Dep>_<Function>_arg1;
/* Call counter */
extern uint32      tstub_call_<Dep>_<Function>;

#endif /* T<COMPONENT>_<DEP>STUB_H__ */
```

#### Implementation `T<COMPONENT>_<Dep>Stub.c`:

```c
#include "T<COMPONENT>_<Dep>Stub.h"

ReturnType  tstub_ret_<Dep>_<Function>          = E_OK;
InputType   tstub_par_<Dep>_<Function>_arg1     = 0;
uint32      tstub_call_<Dep>_<Function>         = 0u;

ReturnType <Dep>_<Function>(InputType arg1)
{
  tstub_par_<Dep>_<Function>_arg1 = arg1;
  tstub_call_<Dep>_<Function>++;
  return tstub_ret_<Dep>_<Function>;
}
```

**Real examples:**

```c
/* TRBECM_RBSYS_Stub.c */
#include "TRBECM_RBSYS_Stub.h"

uint32 TRBECM_CoreID = RBSYS_CORE_ID_0;
unsigned int RBSYS_getCoreID(void)
{
  return TRBECM_CoreID;
}

void TRBSYS_SetCoreID(unsigned int coreID)
{
  TRBECM_CoreID = coreID;
}
```

```c
/* TRBECM_RBECM_Stub.c */
#include "RBECM_ErrorPin.h"

boolean TRBECM_ErrorPinActiveAndLocked = FALSE;
void RBECM_ActivateAndLockErrorPin(void)
{
  TRBECM_ErrorPinActiveAndLocked = TRUE;
}
```

#### Control-variable naming

| Purpose | Prefix | Real examples |
|---------|--------|--------------|
| Configured return value | `tstub_ret_` | `tstub_ret_RBADC_ReadFluid` |
| Captured parameter | `tstub_par_` | `tstub_par_Dem_Report_EventId` |
| Call counter | `tstub_call_` | `tstub_call_Dem_ReportStatus` |
| Direct state variable | `T<COMPONENT>_<VarName>` | `TRBECM_CoreID`, `TRBECM_ErrorPinActiveAndLocked` |

### 4.3 Config Stub Pattern

Many modules use a two-file config stub pair to control feature switches at test time:

**`T<COMPONENT>_ConfigElementsStub.h`** — defines all possible feature-switch values:
```c
#ifndef T<COMPONENT>_CONFIGELEMENTSSTUB_H__
#define T<COMPONENT>_CONFIGELEMENTSSTUB_H__

#define RBFS_MCORE_OFF 0x1
#define RBFS_MCORE_ON  0x2

#define RBFS_Task0p5ms_OFF 0x1
#define RBFS_Task0p5ms_ON  0x2

#endif
```

**`T<COMPONENT>_ConfigStub.h`** — selects the active configuration:
```c
#ifndef T<COMPONENT>_CONFIGSTUB_H__
#define T<COMPONENT>_CONFIGSTUB_H__

#include "T<COMPONENT>_ConfigElementsStub.h"

#define RBFS_MCORE     RBFS_MCORE_ON
#define RBFS_Task0p5ms RBFS_Task0p5ms_ON

#endif
```

Wire this pair in the `.bcfg` via `/** Configure … from … */` + `/** stub … with … */` directives (see Section 2.3).

**Real examples:** `TRBTaskMon_ConfigStub.h`, `TRBECM_ConfigStub.h`, `TRBCDI_RBHSW_Config.h`, `TRBEVP_Config.h`

### 4.4 DEM Stub — Always Mandatory

The DEM stub is **required for every UT environment**. Three DEM stub styles are observed:

#### Style A — Structured with system-status tracking (RBADC pattern, recommended for new code)

```c
/* T<COMPONENT>_DEM.h */
#ifndef T<COMPONENT>_DEM_H__
#define T<COMPONENT>_DEM_H__

#include "Std_Types.h"

typedef enum { DemConf_DemEventParameter_None, … } Dem_EventIdType;
typedef Dem_EventIdType RBHSWDEM_EventId_t;
typedef enum { DEM_EVENT_STATUS_NONE, DEM_EVENT_STATUS_FAILED, DEM_EVENT_STATUS_PASSED, … } RBHSWDEM_EventStatus_t;

typedef enum { DEM_SYSTEM_FAIL_FREE, DEM_SYSTEM_FAILED, DEM_SYSTEM_HEALED } T<COMPONENT>_DEM_SystemStatus_t;

typedef struct {
  RBHSWDEM_EventId_t     id;
  RBHSWDEM_EventStatus_t status;
  uint32                 debug0;
  uint32                 debug1;
} T<COMPONENT>_DEM_Fail_Entry_t;

extern void                            T<COMPONENT>_DEM_ResetAll(void);
extern T<COMPONENT>_DEM_SystemStatus_t T<COMPONENT>_DEM_GetSystemStatus(void);
extern T<COMPONENT>_DEM_Fail_Entry_t   T<COMPONENT>_DEM_GetFailEntry(void);

#endif
```

```c
/* T<COMPONENT>_DEM.c */
#include "T<COMPONENT>_DEM.h"

static T<COMPONENT>_DEM_Fail_Entry_t   failEntry    = { DemConf_DemEventParameter_None, DEM_EVENT_STATUS_NONE, 0, 0 };
static T<COMPONENT>_DEM_SystemStatus_t systemStatus = DEM_SYSTEM_FAIL_FREE;

void RBHSWDEM_ReportErrorStatusWithEnvData(RBHSWDEM_EventId_t id,
                                           RBHSWDEM_EventStatus_t status,
                                           uint32 debug0, uint32 debug1)
{
  failEntry.id     = id;
  failEntry.status = status;
  failEntry.debug0 = debug0;
  failEntry.debug1 = debug1;

  if ((status == DEM_EVENT_STATUS_FAILED) || (status == DEM_EVENT_STATUS_PREFAILED))
    systemStatus = DEM_SYSTEM_FAILED;
  else if ((status == DEM_EVENT_STATUS_PASSED) && (systemStatus == DEM_SYSTEM_FAILED))
    systemStatus = DEM_SYSTEM_HEALED;
}

void T<COMPONENT>_DEM_ResetAll(void)        { /* reset failEntry fields + systemStatus to defaults */ }
T<COMPONENT>_DEM_SystemStatus_t T<COMPONENT>_DEM_GetSystemStatus(void) { return systemStatus; }
T<COMPONENT>_DEM_Fail_Entry_t   T<COMPONENT>_DEM_GetFailEntry(void)    { return failEntry; }
```

#### Style B — Indexed array (RBECM pattern — tracks multiple sequential DEM calls)

```c
/* TRBECM_DEMStub.h */
typedef struct {
  uint32 TestFailed;
  uint32 TestComplete;
  uint32 EventIdType;
  uint32 Debug0;
  uint32 Debug1;
} demStub_t;

extern demStub_t demStub[];
```

#### Style C — Per-event flags (RBEVP pattern — tests `Dem_IsInitMonitorForEventRequested`)

```c
/* TRBEVP_DEMStub.h */
extern boolean Dem_IsInitMonitorForEventRequested_flag_RBEvpUndervoltage_N;
extern demStub_st DemStubFailureList[RBEVP_LastFailureEntry];
```

When starting a **new** component, use **Style A** unless the component already has a DEM stub in its shared `stubs/` or `stub/` folder.

### 4.5 What to Stub

Create a stub for any header the production code includes that is **not** the unit under test:

| Category | Real headers observed | Stub-target examples |
|----------|-----------------------|---------------------|
| DEM / error reporting | `RBHSWDEM_Facade.h`, `Dem.h`, `Dem_Ext.h` | `T<COMPONENT>_DEM.h`, `T<COMPONENT>_DEMStub.h`, `TDEMStub.h` |
| RBSYS system services | `RBSYS_SystemTimer.h`, `RBSYS_CpuInfo.h`, `RBSYS_TaskInfo.h`, `RBSYS_RH850Regs.h` | `T<COMPONENT>_RBSYS_Stub.h`, `T<COMPONENT>_RBSYS_CpuInfoStub.h` |
| Component config | `<COMPONENT>_Config.h`, `RBHSW_Config.h` | `T<COMPONENT>_ConfigStub.h`, `T<COMPONENT>_RBHSW_Config.h` |
| CMHSW / safety framework | `RBCMHSW_Locks.h`, `RBCMHSW_uCSafety.h`, `RBCMHSW_FlashSettings.h` | `T<COMPONENT>_RBCMHSW_Stub.h` |
| HSW ESR | `RBHSWESR_FailureHandling.h` | `T<COMPONENT>_HswESR_Stub.h` |
| AUTOSAR BSW | `Adc.h`, `NvM.h`, `Com.h` | `T<COMPONENT>_AllStub.h` |
| MCAL / HW drivers | `RBADC_HWAccessAPI.h`, `RBDIO_Dio.h`, `RBMICSYS_Wheelspeed.h` | per-dependency stub |
| Generated config headers | `RBADC_GenCfg.h`, `RBADC_GenCfgSets.h` | `T<COMPONENT>_GenCfg.h` |
| Project config / feature flags | `RB_Config.h`, `RB_Prj_ConfigSettings.h` | `T<COMPONENT>_ConfigStub.h` |
| Inter-component interfaces | `RBRFPEC_RBHYDR_Interfaces.h`, `RBMICB6_Interface.h` | per-dependency stub |
| Task scheme add-ons | `RBCMHSW_TaskSchemeAddOn.h` | `T<COMPONENT>_RBCMHSW_TaskSchemeAddOn_Stub.h` |

---

## 5. Step-by-Step Workflow

When asked to **set up a UT environment** for `<COMPONENT>_<Feature>`, follow this sequence:

### Step 0 — Survey existing component structure (MANDATORY)

> **This step is non-negotiable.** Conventions differ between components — do not skip it.

Perform the following discovery before creating any file:

1. **List the component's `tst/` directory tree** to determine the folder layout:
   - `tst/unit/<Feature>/` vs `tst/unit_<Feature>/` vs `tst/Unit_<Feature>/`
   - Presence and capitalisation of stub directories: `stubs/`, `stub/`, `Stub/`
   - Whether `cfg/` sits inside each feature folder or elsewhere
2. **Read at least one existing `.bcfg`** from a sibling feature in the same component:
   - Note the module naming pattern (e.g. `T<COMPONENT><Feature>` vs `T<COMPONENT>_<Feature>`)
   - Note the sub-module ordering (`UnitUnderTest` → `TestCase` → `Stub` or vice-versa)
   - Note how export paths and file globs are written
   - Note the `/** stub … with … */` naming style and any `/** Configure … from … */` directives
3. **Read at least one existing adaptor** (`.c` and `.h`) from the same component:
   - Note the accessor prefix convention (`CallPrivate_`/`GetPrivate_`/`SetPrivate_`, `CP_`/`GP_`, `T<COMPONENT>_set/get`, or custom)
   - Note the `#include` relative path depth from adaptor to production `.c` (e.g. `../src/`, `../../src/`, `../../../src/`)
   - Note whether a config-guard technique is used (pre-defining include guards)
4. **Locate the shared DEM stub** (if any) in `tst/unit/stubs/`, `tst/stub/`, or similar:
   - Identify the DEM stub style (Style A, B, or C — see Section 4.4)
   - If a shared DEM stub exists, reuse it — do not create a duplicate
5. **Check for config stub pairs** (`ConfigStub.h` + `ConfigElementsStub.h`) already in the shared stubs folder:
   - If they exist, reuse and extend them rather than creating new ones
6. **Record your findings** before proceeding — the conventions discovered here dictate every file you create in Steps 1–4.

### Step 1 — Identify dependencies

Two input options are supported. Use whichever matches the available artefacts:

**Option A — Source-based** (production `.c` file exists):
1. Read `<COMPONENT>_<Feature>.c` (production source).
2. List every `#include` that is **not** the unit's own header.
3. Map each include to a stub header (`T<COMPONENT>_<Dep>Stub.h` or `T<COMPONENT>_AllStub.h`).
4. Check if the production source has any `static` functions or variables the tests will need to access → those need adaptor wrappers.
5. Check for `#if (RBFS_…)` conditional compilation → those feature switches need a `ConfigStub.h` / `ConfigElementsStub.h` pair.

**Option B — Forward Engineering / TDD** (DSD document + unit test spec, production `.c` may not yet exist):
1. Read the Detailed Software Design document (`*.md`) for the feature.
2. Read the unit test specification file (`T<COMPONENT>_<Feature>.c`) to understand which functions and variables the tests expect to call.
3. From the DSD, identify all external dependencies (listed in the design's interface / dependency sections) and map each to a stub header.
4. From the DSD, identify all internal (`static`) functions and variables that tests will need white-box access to → those need adaptor wrappers.
5. From the DSD, identify any `RBFS_…` feature switches → those need a `ConfigStub.h` / `ConfigElementsStub.h` pair.

> **Note:** When using Option B, the adaptor's `#include` of the production `.c` must still reference the expected source file path (as specified in the DSD). The adaptor will compile once the production source is created.

### Step 2 — Create the Adaptor

1. Create `T<COMPONENT>_<Feature>Adaptor.c` with the production `.c` `#include` and one wrapper per needed private symbol.
2. Create `T<COMPONENT>_<Feature>Adaptor.h` declaring those wrappers.
3. If the production source does _not_ use `static` functions/variables, skip the adaptor and reference the production `.c` directly in the `.bcfg`.

### Step 3 — Create the Stubs

1. Reuse existing shared DEM stub (`T<COMPONENT>_DEM.c/.h` or `TDEMStub.c/.h`) if one already exists.
2. Create `T<COMPONENT>_DEM.c/.h` if no shared DEM stub exists (always required).
3. For each non-trivial dependency identified in Step 1, create a dedicated `T<COMPONENT>_<Dep>Stub.c/.h`.
4. Consolidate small/trivial dependencies into `T<COMPONENT>_AllStub.c/.h`.
5. If feature switches are needed, create `T<COMPONENT>_ConfigStub.h` + `T<COMPONENT>_ConfigElementsStub.h`.

### Step 4 — Create the Build Config

1. Create `cfg/T<COMPONENT><Feature>_BuildConfig.bcfg`.
2. Add one `/** stub … with … */` line per replaced header.
3. Add `/** Configure … from … */` lines for any config stub pairs.
4. List every stub `.c` file and every stub export path created in Step 3.
5. Reference the adaptor `.c` file in the `UnitUnderTest` module.

### Step 5 — Consistency Check

Verify all items in **Section 6 — Checklist Before Delivering**.

---

## 6. Checklist Before Delivering

- [ ] **Step 0 completed**: Component's existing `tst/` structure scanned; folder layout, naming conventions, adaptor prefix style, DEM stub style, and stub directory names identified and followed.
- [ ] `cfg/T<COMPONENT><Feature>_BuildConfig.bcfg` created with all three sub-modules (`UnitUnderTest`, `TestCase`, `Stub`).
- [ ] `/** stub … */` annotations present for every replaced header, including `RBHSWDEM_Facade.h` and `Dem.h`.
- [ ] `/** Configure … from … */` directive present if any `ConfigStub.h` / `ConfigElementsStub.h` pairs are used.
- [ ] Adaptor `.c` includes the production `.c` via a correct relative path (verified against folder depth).
- [ ] Adaptor `.h` has an include guard formatted as `T<COMPONENT>_<FEATURE>ADAPTOR_H__` (double underscore suffix).
- [ ] Adaptor accessor prefixes match the existing component convention (`CallPrivate_` / `GetPrivate_` / `SetPrivate_` or `T<COMPONENT>_set` / `T<COMPONENT>_get` or `CP_` / `GP_`).
- [ ] DEM stub present — either reused from shared stubs or newly created.
- [ ] Stub control variables follow the established naming pattern (`tstub_ret_`, `tstub_par_`, `tstub_call_` or direct `T<COMPONENT>_<Var>` names).
- [ ] All stub headers have include guards formatted as `T<COMPONENT>_<DEP>STUB_H__` (all caps, double underscore).
- [ ] Stub folder paths (`stubs/`, `stub/`, `Stub/`) are consistent with the component's existing convention.
- [ ] No circular dependencies: adaptor `.c` must not appear in `Stub` or `TestCase` modules.
- [ ] Feature-switch stubs (`ConfigStub.h` + `ConfigElementsStub.h`) created when production code uses `#if (RBFS_…)` guards.
