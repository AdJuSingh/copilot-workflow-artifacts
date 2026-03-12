# Requirement Elicitation

Prompt the user to give the updated requirements ={updated_requirements}

Perform requirement elicitation and make sure that the requirements follow a structure and are not ambiguous, since an ambiguous requirement could cause further issues down the process. [Make sure the user-provided requirements have a clear Actor/Subject, Action Verb, Specific Function/Behaviour, Conditions and Triggers, ASIL safety, Performance Criteria, Constraints and Boundaries, classification explicitly provided, Interface specifications if any, Diagnostic Requirements.] If any of these are not present, query the user for input regarding these. Also give the user an option to continue the modification without these.

Note: The requirements in DOORS .csv's don't correspond to user-given {updated_requirements}. The {updated_requirements}
acts as an update to existing DOORS requirements. Wait for user input after requirement elicitation, then only move to impact analysis.

Do's
Only move to Impact Analysis with Developer consent

Important: Perform an alignment check to verify to what percentage does the user given {updated_requirements} align with the workspace and Knowledge_Graph.JSONLD and proved the output, raise concern if the requirement does not completly align with the workspace

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
3) Is a safety requirement affected? (Check safety requirement on related signals & contact FSM)
4) Will software variants other than CSW be affected?

Example:
    Ideally, the requirement elicitation & impact analysis should be like

    For the requirement: Driver's request to change the VDMS (Vehicle Dynamic Mode Selection) operating mode shall be checked against conditions like if mode change is allowed, passive mode is allowed, and if ESP is requested for the reactivation along with if handbag failure is detected by the system.
    Additional requirement: Check the vehicle speed by creating an Elicitation for the same and add three modes: low-speed, medium-speed, and high-speed. No mode change is allowed if the vehicle speed is high.


    Requirement Elicitation response:

    Actor/Subject: The VDMS system
    Action Verb: "shall be checked"
    Function/Behaviour: Check vehicle speed and prevent mode changes at high speed
    Conditions/Triggers: Driver request + speed conditions
    Classification: Functional requirement

    ---Waits for developer's input

    Impact Analysis Response

    1. Files Affected
    Header Files (.hpp):

    rbc_vdms_core-espmode-arbitration.hpp - Add vehicle speed parameter to sendVDMSmode function
    rbc_vdms_enums.h - Add new VehicleSpeedCategory enum
    Implementation Files (.cpp):

    rbc_vdms_core-espmode-arbitration.cpp - Update arbitration logic with speed checks
    Test Files:

    test_rbc_vdms_core-espmode-arbitration.cpp - Add speed category test cases
    2. Classes, Methods & Functions Affected
    Functions:

    MODIFIED: sendVDMSmode() - Add vehicleSpeedCategory parameter
    NEW: categorizeVehicleSpeed() - Convert speed value to enumeration
    Enumerations:
    NEW: VehicleSpeedCategory enum {LOW_SPEED, MEDIUM_SPEED, HIGH_SPEED}

    3. Safety Requirements
    Enhanced Safety: Speed-based mode change prevention at high speeds
    Interface Safety: Vehicle speed signal already exists (vehicleSpeedALC)
    Diagnostic: Existing vehicle speed handling in place

    4. Software Variants
    VDMS_Base: Affected - Core arbitration logic modified
    VDMS_HadHap: Affected - Same core arbitration logic used


# Next Step

After the requirement elicitation & impact analysis is complete, ask for user verification and feedback, then load the 3_Implementation_plan and continue.
