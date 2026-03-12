# Instruction 00: Build Software (Software Build Execution)

## CRITICAL: BUILD SOFTWARE FORMAT & STANDARDS

- Software build must be executed based on the build configurations defined in `Cfg_Configurations.xml`.
- The build system uses MTC (MBuild Tool Chain) for all builds.
- Build configurations are categorized by product variant, build type, and target hardware.
- Do not create any additional build configuration files unless explicitly requested.
- **The accepted workflow is to immediately parse configurations and present the full list to the user for selection**.
- **CRITICAL FILE REFERENCE**: All build configurations are maintained in `Cfg_Configurations.xml` in the project root directory.
- **SPEED REQUIREMENT**: Do not take excessive time for configuration selection - fetch and display builds immediately when prompted.
- **PERFORMANCE TARGET**: Complete configuration discovery and display within 15 seconds maximum.
- **IMMEDIATE ACTION REQUIRED**: When user specifies a build category (e.g., "DCOMSIM"), show only relevant configurations first, then optionally show others if requested.

## BUILD CONFIGURATION DISCOVERY

- **IMMEDIATE ACTION**: Read and parse all build configurations from `Cfg_Configurations.xml` as soon as prompted
- **PERFORMANCE REQUIREMENT**: Complete configuration parsing and display within 15 seconds
- **SMART FILTERING**: If user specifies a build type (e.g., "DCOMSIM", "CSW", "BSW"), show only relevant configurations first
- Extract the following information for each configuration without delay:
  - `<ConfigurationName>`: The unique name identifier for the build configuration
  - `<BBNo>`: The baseline/project number
  - `<ConfigurationNo>`: The hexadecimal configuration number
  - `<ConfigurationType>`: Build type (DEVELOP, RELEASE, etc.)
  - `<Comment>`: Description of the build configuration
  - `<BuildIdPrefix>`: Build identifier prefix (if applicable)
  - `<UsedHexBlocks>`: Dependent hex blocks for composite builds (if applicable)
- Group configurations by BB number and product variant for easier selection
- Display configurations in a structured format for user selection immediately
- **OPTIMIZATION**: Use targeted file reading instead of full file parsing when specific build types are requested
- **DO NOT WAIT**: Present the relevant configurations to the user right away

## BUILD CATEGORIES

The build configurations are organized into categories based on the project structure. Common categories include:

- **CSW (Customer Software) Area**: Customer-facing software builds
- **BSW (Basic Software) Area**: Basic software simulation builds
- **DCOM SIM Area**: Diagnostic communication simulation builds
- **Soft ECU Area**: Software-in-the-loop (SIL) testing builds
- **Simulation Area**: Application and basic software simulation configurations
- **Bootloader Area**: Bootloader and boot manager builds
- **Product Variants**: Product-specific build configurations
- **Test Builds**: DVT (Design Verification Test), EMC, and validation builds

## INTERACTIVE BUILD SELECTION WORKFLOW

1. **Display Available Build Configurations**:

   - **SPEED OPTIMIZATION**: If user mentions specific build type (DCOMSIM, CSW, BSW, etc.), use targeted search to show only relevant configurations first
   - Parse `Cfg_Configurations.xml` with targeted reading for faster response (within 15 seconds)
   - Group configurations by BB number and category
   - Show configuration name, BB number, and description
   - Format: `[Index] ConfigurationName (BBNo: BBXXXXX) - Description`
   - **PERFORMANCE TARGET**: Display relevant configurations within 15 seconds maximum
   - **SMART DISPLAY**: Show most likely configurations based on user request, offer to show others if needed
2. **User Selects Build Configuration**:

   - User provides the index number or configuration name
   - Confirm the selection with the user before proceeding
3. **Prompt for Build Type Selection**:

   - **CRITICAL**: After confirming the build configuration, ask the user to select the build type:
     - **Option 1: Full Build (RebuildAll)** - Complete rebuild of all components from scratch
     - **Option 2: Incremental Build** - Build only changed components (faster)
   - User must select either option 1 or 2
   - Display the selection prompt clearly:
     ```
     Select Build Type:
     1. Full Build (RebuildAll) - Complete rebuild from scratch
     2. Incremental Build - Build only changed components

     Enter your choice (1 or 2):
     ```
4. **Generate MTC Build Command**:

   - **CRITICAL**: Use the MTC (MBuild Tool Chain) PowerShell command format
   - Extract the workspace root directory (parent directory of `Cfg_Configurations.xml`)
   - **For Full Build (Option 1)**, generate command in this format:

     ```powershell
     powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File <MTC_INSTALLATION_PATH>\StartMTC\Start-MTC.ps1 -RootDir "<WorkspaceRoot>" -Config <ConfigurationName> -GenerateMakeFile -BuildTarget BUILD
     ```
   - **For Incremental Build (Option 2)**, generate command in this format:

     ```powershell
     powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File <MTC_INSTALLATION_PATH>\StartMTC\Start-MTC.ps1 -RootDir "<WorkspaceRoot>" -Config <ConfigurationName> -BuildTarget BUILD -ImprovedIncrementalBuild
     ```
   - **Command Parameters**:

     - `<MTC_INSTALLATION_PATH>`: Path to MTC installation (e.g., C:\MTC10Base)
     - `<WorkspaceRoot>`: Absolute path to workspace (parent of Cfg_Configurations.xml)
     - `<ConfigurationName>`: The selected configuration name
     - `-GenerateMakeFile`: Only for Full Build - generates makefiles from scratch
     - `-ImprovedIncrementalBuild`: Only for Incremental Build - builds only changed components
     - `-BuildTarget BUILD`: Standard build target for all builds
5. **Execute Build**:

   - Display the generated command to the user for confirmation
   - Execute the MTC PowerShell command in the terminal
   - Monitor build progress and capture output
   - ** CRITICAL WARNING**: Once the build has started, DO NOT push any additional commands in the same terminal. The MTC build process is sensitive to interruptions and additional terminal input can cause build failures or corruption. Wait for the build to complete before issuing any new commands.
6. **Build Verification**:

   - Check build log for errors and warnings
   - Verify output files in `Gen/<ConfigurationName>/` directory
   - Report build status to user

## MTC BUILD COMMAND PATTERNS

### MTC PowerShell Command Format (CURRENT STANDARD):

**Full Build Command:**

```powershell
powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File <MTC_INSTALLATION_PATH>\StartMTC\Start-MTC.ps1 -RootDir "<WorkspaceRoot>" -Config <ConfigurationName> -GenerateMakeFile -BuildTarget BUILD
```

**Incremental Build Command:**

```powershell
powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File <MTC_INSTALLATION_PATH>\StartMTC\Start-MTC.ps1 -RootDir "<WorkspaceRoot>" -Config <ConfigurationName> -BuildTarget BUILD -ImprovedIncrementalBuild
```

**Command Parameters Explained:**

- `-ExecutionPolicy Bypass`: Bypasses PowerShell execution policy
- `-NoLogo -NonInteractive -NoProfile`: Suppress output and run without user interaction
- `-File <MTC_INSTALLATION_PATH>\StartMTC\Start-MTC.ps1`: MTC build orchestration script
- `-RootDir "<WorkspaceRoot>"`: Absolute path to workspace (parent of Cfg_Configurations.xml)
- `-Config <ConfigurationName>`: Build configuration name from XML
- `-GenerateMakeFile`: Generate makefiles from scratch (Full Build only)
- `-BuildTarget BUILD`: Standard build target
- `-ImprovedIncrementalBuild`: Build only changed components (Incremental Build only)

**Example Commands:**

For Full Build:

```powershell
powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File C:\MTC10Base\StartMTC\Start-MTC.ps1 -RootDir "C:\Workspace\ProjectName" -Config ConfigurationName -GenerateMakeFile -BuildTarget BUILD
```

For Incremental Build:

```powershell
powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File C:\MTC10Base\StartMTC\Start-MTC.ps1 -RootDir "C:\Workspace\ProjectName" -Config ConfigurationName -BuildTarget BUILD -ImprovedIncrementalBuild
```

### Legacy Build Scripts (DEPRECATED - For Reference Only):

Legacy batch file scripts may be present in the workspace but should NOT be used. Always use the MTC PowerShell command format shown above.

## BUILD OUTPUT VERIFICATION

After build completion, verify:

1. **Build Artifacts**:

   - Check `Gen/<ConfigurationName>/` directory for output files
   - Verify hex files, map files, and binaries are generated
   - Check build timestamp in `Build_<timestamp>/` subdirectory
2. **Build Logs**:

   - Review `Gen/<ConfigurationName>/make/_Log_GenMake_<ConfigurationName>.prt`
   - Check for compilation errors and warnings
   - Verify all modules compiled successfully
3. **Build Status**:

   - Confirm exit code is 0 (success)
   - Report any build failures with error details
   - Document build completion time

## CONFIGURATION SELECTION TEMPLATE

Display configurations in this format:

```
AVAILABLE BUILD CONFIGURATIONS

--- CSW Area (BBXXXXX) ---
[1] ConfigurationName1 (BBXXXXX)
    Description of build configuration 1

[2] ConfigurationName2 (BBXXXXX)
    Description of build configuration 2

--- BSW Simulation Area (BBXXXXX) ---
[3] ConfigurationName3 (BBXXXXX)
    Description of build configuration 3

--- Product Variant Area (BBYYYYY) ---
[50] ConfigurationName50 (BBYYYYY)
     Description of build configuration 50

[51] ConfigurationName51 (BBYYYYY)
     Description of build configuration 51

=============================================================================
Select a build configuration by entering the index number or name:
```

## Quality Checklist

- [ ] All configurations from Cfg_Configurations.xml are parsed and displayed
- [ ] Configurations are grouped by BB number and category
- [ ] User selection is confirmed before build execution
- [ ] Correct build script is identified based on configuration
- [ ] Build command is executed in the correct directory
- [ ] Build output is verified and reported
- [ ] Build logs are checked for errors and warnings
- [ ] Build artifacts are verified in the output directory

### Copilot Self-Review Checklist:

- [ ]  All configurations from XML are accurately extracted
- [ ]  Configuration names and BB numbers are correctly displayed
- [ ]  Build categories are logically organized
- [ ]  User selection workflow is clear and interactive
- [ ]  Build command mapping is accurate
- [ ]  Build verification steps are comprehensive
- [ ]  Error handling for build failures is in place
- [ ]  Build output location is correctly identified

### Common Mistakes to Avoid:

- Executing build without user confirmation
- Not verifying the build script exists before execution
- Ignoring build log errors and warnings
- Not checking build output directory for artifacts
- Using wrong build script for the selected configuration
- Not providing clear feedback on build status
- Failing to handle build errors gracefully
- ** CRITICAL: Pushing additional commands to the terminal while a build is running (this will cause build failures or corruption)**

## Consistency

- If any previous build execution exists, the new build should follow the same pattern and verification steps.
- Build logs and output verification should be consistent across all build types.

## Next Step

- After successful build, the output artifacts are ready for:
  - Flashing to target hardware
  - SIL/HIL testing
  - Component testing (DCOMSIM, BSWSim)
  - Integration testing

## Iterative Improvement Requirement

- Before executing any build, verify:
  - Build configuration exists in Cfg_Configurations.xml
  - Required build script is available
  - Previous build artifacts are backed up (if needed)
  - Build environment is properly configured
- After build execution:
  - Verify all expected output files are generated
  - Check build logs for any warnings or errors
  - Document build results and any issues encountered
