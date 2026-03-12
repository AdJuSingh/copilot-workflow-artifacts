# Instruction 06: CT SIM Execution

Changelog
---------
- 2025-11-11: Added CRITICAL directive to avoid extra analysis after prompt invocation - proceed directly with workflow steps only.
- 2025-11-11: Updated to use `.\Bin_<SelectedFolder>.exe SwTest -Testlist=?` command to list available test cases directly from the simulation binary instead of parsing header files. Added alternative method using header file parsing.
- 2025-11-11: Consolidated duplicate guidance; added explicit verification and changelog header. The prompt file (`.github/prompts/6_create_ct_sim_execution.prompt.md`) is intentionally concise and points to this file for full details.

CRITICAL: CT SIM EXECUTION FORMAT & STANDARDS

- This workflow executes Component Test (CT) simulations on generated build outputs. Only folders under `Gen` are valid targets. Do not modify or delete files in the selected folder.
- **IMPORTANT**: Once this prompt is invoked, proceed directly with the workflow steps. Do NOT perform any extra analysis, suggestions, or additional actions unless explicitly requested by the user.

Prerequisites
-------------
- The selected build must be produced by a completed build process.
- The `Gen` directory must contain at least one build folder with an `out` subfolder containing the simulation binary.

Step-by-step process
--------------------
1. Fetch available simulation targets
  - Enumerate directories directly under `Gen` (ignore files).
  - Present them indexed for the user.
2. User selects a simulation target
  - Accept either the index or the exact folder name (case-sensitive match preferred).
  - Ask the user to confirm the selection before proceeding.
3. Prepare the simulation environment
  - Validate existence of the `out` directory and an executable named `Bin_<SelectedFolder>.exe`.
  - List available test lists by running the simulation binary with the help flag:

    cd Gen\<SelectedFolder>\out; .\Bin_<SelectedFolder>.exe SwTest -Testlist=?

    This command will display all available test lists indexed from 0 to N.
  - Parse the output and present the test lists indexed for user selection.
  - Alternative: If needed, validate presence of the test-list header at: `<SelectedFolder>/src_out/cgen/SwTest_GeneratedTestLists.h` and extract test list identifiers using the regex:

    pattern = r'extern\s+TestCaseDefinition\s+(\w+)\[\];'

  - If any required artifact is missing, stop and report the missing path(s). Do not continue.
4. Execute simulation
  - After the user chooses a test list and confirms, run the command from the `out` directory:

    powershell: cd C:\TSDE_Workarea\LNG1COB\IPB_CHY\CHRYSLER_IPB\Gen\<SelectedFolder>\out; .\Bin_<SelectedFolder>.exe SwTest -Testlist=<SelectedTestList>

  - Capture stdout/stderr and the exit code.
5. Verification & reporting
  - Verify exit code (0 == success). Collect any output files produced in `out`.
  - Create a concise test summary `.txt` in the `out` directory with these required fields:
    - Test Name
    - Total Test Cases / range
    - Total Test Steps
    - Passed / Failed counts and %
    - Warnings
    - Runtime (real / simulated)
    - Exit Code
    - Report filename(s) (CSV)
    - Top failure patterns (short list)

  - Log file locations and a short execution report should be returned to the user.

Display template
----------------
AVAILABLE SIMULATION TARGETS
[1] DCOMsimxCHRxIPBxICE
[2] CHRxIPB2xICExEP800102xECA

Select a simulation target by entering the index number or folder name:

Quality checklist (minimum)
--------------------------
- Confirmed selection before execution.
- Executable `Bin_<SelectedFolder>.exe` present in `out`.
- `SwTest_GeneratedTestLists.h` present and parsed or explicit error reported.
- Captured stdout/stderr and exit code.
- Test summary `.txt` written in `out`.

Common mistakes to avoid
-----------------------
- Not listing all folders under `Gen` (ensure directories only).
- Running without user confirmation.
- Not validating required files before execution.
- Not reporting missing files or errors clearly.

Iterative improvement
---------------------
- Keep this file canonical for CT simulation execution rules. Update as simulation tooling or output formats change.

