
# This instruction file deals with running of Unit test, CTT code coverage and Memory Management with SWDM Compliance

## Initial Checks for successful execution
1) Before initiating, if the "Gen" Folder exists Delete the Gen Folder or ask the user to delete the "Gen" Folder - Because if the Gen Folder exists it may cause errors in UTB Build. The Gen Folder is to be created after testing

2) Make sure the full directory structure doesn't have any whitespaces, if yes raise a warning to the user and continue

3) Executable path: Bin_{Component_workspace}_UnitTest_TDM.exe
  Compiler: GCC_MINGW64_X86_WIN_V10_4 environment required
  Test framework: Google Test integrated

## Pre-Test SWDM Compliance Validation

**Step 0: SWDM Format Validation**
Before running any tests, validate that all unit test files comply with SWDM standards:

1. **Unit Test File Structure Validation:**
   - Check that test files are located in `tst/*/gtest/*/ut/` directory,
   - Verify test file naming follows pattern: `test_<component>_<module>.cpp`
   - Ensure test class naming follows pattern: `<Component><Module>Test` (PascalCase)

2. **Documentation Block Validation:**
   - Verify each test file contains proper `@addtogroup` structure:
     ```cpp
     /// @addtogroup rbc_vdms_{UNIT_NAMESPACE}_{UNIT_FILENAME}
     /// @{
     /// @unitspec{SPECIFIC_TEST_DESCRIPTION}
     /// @derives{REQUIREMENT_REFERENCE}
     ///   FUNCTIONAL_DESCRIPTION_FOR_THIS_TEST
     ///   
     ///   ALGORITHM_OR_CONDITION_BEING_TESTED
     ///   EXPECTED_BEHAVIOR_OR_STATE_TRANSITION
     /// @endunitspec
     /// @}
     ```
   - Each TEST_F or TEST function must have individual test documentation with:
     - `@par Scope / Purpose / Design:` description
     - Proper GIVEN/WHEN/THEN structure in comments

3. **Stub Parameter Usage Validation:**
   - Check that all parameter access uses proper stub functions:
     - `RB_setParam_<ParameterName>(value)` for setting parameters
     - `RB_getParam_<ParameterName>()` for getting raw parameters  
     - `RB_getParamPhys_<ParameterName>()` for physical parameters
     - `RB_getParamPhysEffective_<ParameterName>()` for effective physical parameters
   - Verify no direct parameter assignments (e.g., `param = value;`)
   - Confirm parameter reset function usage: `RB_reset_all_parameters_from_<component>_to_defaults()`

4. **Test Structure Validation:**
   - Verify proper GTEST framework usage (TEST, TEST_F, EXPECT_EQ, ASSERT_*)
   - Check that test inputs are declared as `constexpr const` where applicable
   - Ensure expected outputs are clearly defined before WHEN section
   - Validate proper variable naming conventions (camelCase for variables)

**If validation fails:** Report specific non-compliance issues to user and request permission to fix before proceeding.

  The unit testing workflow operates through a structured configuration system where Cfg_UTB.xml defines three test configurations (standard TDM, coverage analysis, and static analysis Bauhaus) that utilize different compilers and build targets. The utb.bcfg build configuration includes source files, Google Test framework components, and test stubs while excluding production-only elements. The UTB (Unit Test Builder) framework generates separate build environments in UTB directories for each configuration, creating object files, executables, and reports. Test stubs in stubs provide mock interfaces for dependencies, enabling isolated unit testing. 
  The UTB framework generates isolated build environments per test configuration in UTB. Each configuration (VDMS_UnitTest_TDM, VDMS_UnitTest_TDM_Coverage) contains tmp/ for preprocessed files, obj/ for compiled objects, and out/ for executables and logs
  When the testing has been done. Access the results in Gen/UTB/Runtime.txt or Gen/UTB/_Log_UTBOutput.prt


## Workflow
### Critical: Don't Make up results only show results when the termianl run task is complete and valid using the output in Gen folder - since it is not possible to access terminal run tasks for this case. 
**Step 1: Execute Unit Test Build with Exit Code Monitoring**
- Run build task 
- Monitor task execution and capture the status from Gen/UTB/Runtime.txt. It should update BuildResult as False/True.
- It will take close to 1-2 minutes for UTB status to get updated
- Make sure you take the Runtime.txt for latest runtime. Not for the previous one.

  Build Status Verification:
  Check Gen/*/Runtime.txt for configuration success/failure before execution
  Verify executable exists in BinaryList_Cfg_UTB_xml.txt
  Check _Log_UTBOutput_*.prt for detailed compilation errors if build fails
  
  Note: Do not run commands in the terminal that might interfere with the current executing command - get build status for both UTB & CTTCodeCoverage from the files in Gen

**Step 2: Execute CTTCodeCoverage with Exit Code Monitoring**
- Run CTTCodeCoverage task 
-  It will take close to 1-5 minutes for CTT status to get updated
- The task execution output will be updated in Gen/CTT_Results.txt


## Enhanced Failure Condition Handling

**If Unit Test Build Fails (Exit Code != 0):**
1. **Error Analysis:** Parse build output for specific error types:
   - Compilation errors (syntax, missing includes)
   - Linking errors (undefined references)
   - SWDM format violations
   - Stub parameter access errors

2. **Failure Root Cause Identification:**
   - Check for missing files in Gen folder
   - Validate stub parameter usage against generated stubs
   - Verify requirement traceability format
   - Check @unitspec documentation completeness

3. **User Interaction:**
   - Present specific error details with line numbers
   - Suggest targeted fixes for implementation, design document, and test files
   - Request user permission before modifying any code files
   - Provide options: fix automatically, fix with guidance, or manual fix

4. **Recovery Actions:**
   - Rerun "Update SWDM Workspace" task if workspace issues detected
   - Regenerate parameter stubs if PDL-related errors found
   - Re-execute validation steps after fixes applied

**If CTTCodeCoverage Fails (Exit Code != 0):**
1. **Coverage Analysis Failure:** Check for coverage tool configuration issues
2. **Missing Dependencies:** Verify all required build artifacts exist

**Post-Failure Recovery:**
- After storing the Task failure reason in your memory - Delete Gen folder to start fresh.
- After implementing fixes, re-run Step 0 (SWDM Validation)
- Re-execute failed tasks and monitor Gen folder output

Note: Code file modifications require explicit user permission. Always explain the specific SWDM compliance issue before requesting permission to fix.

# End of Workflow Orchestration
