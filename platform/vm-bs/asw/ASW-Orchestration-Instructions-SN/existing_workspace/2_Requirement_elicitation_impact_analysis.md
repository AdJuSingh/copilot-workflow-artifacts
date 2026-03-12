# Requirement Elicitation

Prompt the user to give the updated requirements ={updated_requirements}

Perform requirement elicitation and make sure that the requirements follow a structure and are not ambiguous, since an ambiguous requirement could cause further issues down the process. [Make sure the user-provided requirements have a clear Actor/Subject, Action Verb, Specific Function/Behaviour, Conditions and Triggers, ASIL safety, Performance Criteria, Constraints and Boundaries, classification explicitly provided, Interface specifications if any, Diagnostic Requirements.] If any of these are not present, query the user for input regarding these. Also give the user an option to continue the modification without these. Store the Requirement id in {requirement_id}

Note: The requirements in DOORS .csv's don't correspond to user-given {updated_requirements}. The {updated_requirements}
acts as an update to existing DOORS requirements. Wait for user input after requirement elicitation, then only move to impact analysis.


# Instructions for Impact Analysis


Given {updated_requirements} with respect to the workspace, perform impact analysis.
Workspace is {codebase_for_edit}.
Don't hallucinate or do any guesswork without solid proof from the workspace or Knowledge Graph. You are the one tasked with doing a workspace-level impact analysis for the updated requirements in the existing workspace with the context of the Knowledge Graph (.jsonld) and {codebase_for_edit}.

Workspace structure is
project/
├── .vscode/
│ └── project_snippet.code-snippets [Reference for code/test patterns]
│
├── api/
│ ├── XXXX.h [External interface headers]
│ └── XXXX.hpp [Check for corresponding test: tst/gtest/*/test_XXXX.cpp]
│
├── cfg/
│ └── {component_name}_parameters.pdl [Configuration parameters for source/test files]
│
├── src/
│ ├── */XXXX.hpp [Main source headers]
│ ├── */XXXX.cpp [Main source implementations]
│ ├── onesensor/ [Plausibility check components]
│ ├── twosensor/ [Plausibility check components]
│ ├── actuation/ [Plausibility check components]
│ └── modulation/ [Plausibility check components]
│
├── tst/
│ └── gtest/
│ └── */test_XXXX.cpp [Unit tests - corresponds to api/XXXX.h(pp)]
│
└── Gen/
└── * [Build files for unit testing, CTTCodeCoverage]
[Critical for test execution]

## Key Relationships
- `api/XXXX.h(pp)` ↔ `tst/gtest/*/test_XXXX.cpp` (interface-test pairing)
- `cfg/{component}_parameters.pdl` → `src/` and `tst/` (configuration dependency)
- `Gen/*` → test execution (build dependency)


Impact Analysis checklist is:
1) .hpp, .cpp, and test files affected
2) What classes, methods, and functions are affected
3) Check ALL existing test files for compilation impacts before making changes
3) Is a safety requirement affected? (Check safety requirement on related signals & contact FSM)
4) Will software variants other than CSW be affected?

Evaluate if the requirement involves:
- Cross-cutting concerns (functionality used across multiple variants/components)
- Complex conditional logic that should be extracted into utility functions
- Repeated patterns that violate DRY principle

If identified, plan for:
- Utility function/class creation in src/ root directory
- Dedicated test files for new utilities
- Clean separation of concerns

## Architectural Impact Analysis Checklist

Beyond standard impact analysis, evaluate:

### Code Architecture Impact:
1) **Cross-Variant Functionality**: Will this requirement apply to multiple variants (actuation, modulation, actandmod)?
   - If YES: Plan utility function/class creation in src/ root
   - Extract common logic to avoid duplication

2) **Complexity Analysis**: Does the requirement involve complex conditional logic (>3 conditions)?
   - If YES: Plan function extraction for readability
   - Use meaningful function names (e.g., isSystemDegraded vs inline checks)

3) **File Creation Requirements**:
   - New utility files: src/rbc_arbextern_{functionality}.{hpp|cpp}
   - Dedicated test files: tst/gtest/ut/test_rbc_arbextern_{functionality}.cpp
   - Build configuration updates: BCfg file modifications

4) **Reusability Assessment**: Can the implementation be reused for similar future requirements?
   - If YES: Design for extensibility and parameterization

Example:
    Ideally, the requirement elicitation & impact analysis should be like

    For the requirement: Driver's request to change the VDMS (Vehicle Dynamic Mode Selection) operating mode shall be checked against conditions like if mode change is allowed, passive mode is allowed, and if ESP is requested for the reactivation along with if handbag failure is detected by the system.
    Additional requirement: Check the vehicle speed by creating an Elicitation for the same and add three modes: low-speed, medium-speed, and high-speed. No mode change is allowed if the vehicle speed is high.


    Requirement Elicitation response:
    Actor/Subject: ✅ The VDMS system
    Action Verb: ✅ "shall be checked"
    Function/Behaviour: ✅ Check vehicle speed and prevent mode changes at high speed
    Conditions/Triggers: ✅ Driver request + speed conditions
    Classification: ✅ Functional requirement

    ---Waits for developer's input

    Impact Analysis Response

    1. Files Affected
    Header Files (.hpp):

    ✅ rbc_vdms_core-espmode-arbitration.hpp - Add vehicle speed parameter to sendVDMSmode function
    ✅ rbc_vdms_enums.h - Add new VehicleSpeedCategory enum
    Implementation Files (.cpp):

    ✅ rbc_vdms_core-espmode-arbitration.cpp - Update arbitration logic with speed checks
    Test Files:

    ✅ test_rbc_vdms_core-espmode-arbitration.cpp - Add speed category test cases
    2. Classes, Methods & Functions Affected
    Functions:

    ✅ MODIFIED: sendVDMSmode() - Add vehicleSpeedCategory parameter
    ✅ NEW: categorizeVehicleSpeed() - Convert speed value to enumeration
    Enumerations:
    ✅ NEW: VehicleSpeedCategory enum {LOW_SPEED, MEDIUM_SPEED, HIGH_SPEED}

    3. Safety Requirements
    ✅ Enhanced Safety: Speed-based mode change prevention at high speeds
    ✅ Interface Safety: Vehicle speed signal already exists (vehicleSpeedALC)
    ✅ Diagnostic: Existing vehicle speed handling in place

    4. Software Variants
    ✅ VDMS_Base: Affected - Core arbitration logic modified
    ✅ VDMS_HadHap: Affected - Same core arbitration logic used


# Next Step

After the requirement elicitation & impact analysis is complete, ask for user verification and feedback, then load the 2.5_Memory.md and fetch the relevant context from the memory.md file and store it in {memory_context} escpecially check the user_feedback section in all the indexes, show the fetched memory context to the user, then load the 3_Implementation_plan and continue.
