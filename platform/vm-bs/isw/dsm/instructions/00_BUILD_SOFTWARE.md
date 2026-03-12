# Instruction 00: Build Software (Software Build Execution)

## CRITICAL: BUILD SOFTWARE FORMAT & STANDARDS

- Software build must be executed based on the build configurations defined in `Cfg_Configurations.xml`.
- The build system uses MTC (MBuild Tool Chain) version 10.12 for all builds.
- Build configurations are categorized by product variant, build type, and target hardware.
- Do not create any additional build configuration files unless explicitly requested.
- **The accepted workflow is to select a build configuration from the available list and execute the corresponding build command**.
- **CRITICAL FILE REFERENCE**: All build configurations are maintained in `Cfg_Configurations.xml` in the project root directory.

## BUILD CONFIGURATION DISCOVERY

- Read and parse all build configurations from `Cfg_Configurations.xml`.
- Extract the following information for each configuration:
  - `<ConfigurationName>`: The unique name identifier for the build configuration
  - `<BBNo>`: The baseline/project number (e.g., BB84030, BB89210, BB53514, BB53355)
  - `<ConfigurationNo>`: The hexadecimal configuration number
  - `<ConfigurationType>`: Build type (DEVELOP, RELEASE, etc.)
  - `<Comment>`: Description of the build configuration
  - `<BuildIdPrefix>`: Build identifier prefix (if applicable)
  - `<UsedHexBlocks>`: Dependent hex blocks for composite builds (if applicable)
- Group configurations by BB number and product variant for easier selection.
- Display configurations in a structured format for user selection.

## BUILD CATEGORIES

The build configurations are organized into the following categories:

### 1. **IPB CSW Area** (BB84030)

- Mainstream IPB product CSW builds
- Includes internal CAN transceiver variants, RTE builds, and finalization builds

### 2. **IPB BSW Area** (BB84030)

- BSW simulation builds for IPB product
- BSWSIM configurations for DCM, Network, and FlexRay

### 3. **IPB DCOM SIM Area** (BB84030)

- DCOMSIM configurations for IPB 2.0 product
- Component testing and diagnostic communication simulation

### 4. **IPB Soft ECU Area** (BB84030, BB89210, BB89577)

- Soft ECU builds for SIL testing
- Multiple variants for different product configurations

### 5. **Simulation Area** (BB84030)

- ASW simulation configurations (Sfun4ASWOnlySim)
- BSW simulation for Network and DCM components

### 6. **IPB BLDR/BMGR/HSM Build Area** (BB84030, BB89210, BB89577)

- Bootloader builds (RBBLDR, BMGR)
- Hardware Security Module (HSM) enabled builds
- Combined boot-in-one configurations

### 7. **RoPP41 Builds** (BB89210 - Main, BB89577 - Sub)

- Main system builds (AC0, C1 layouts)
- Sub system builds (AC0, C1 layouts)
- iPace variants with HSM support
- EMC, Dry Labcar, and Finalize builds

### 8. **IPB EP8000 Build Area** (BB84030)

- EP8000 CSW builds
- DVT (Design Verification Test) builds
- TCSW (Test CSW) builds
- EMC and finalization builds

### 9. **HAD (Highly Automated Driving) Builds** (BB84030)

- HAD variant builds for iPACE
- Soft ECU and Dry Labcar configurations

### 10. **JLR iPACE Builds** (BB84030)

- CANFD enabled builds
- B3, B4 sample builds
- Soft ECU and finalization builds

### 11. **Chrysler IPB ICE Variant** (BB53514)

- XPASS, PSW, HSWSim builds
- ECA, ECC builds (application finalized/not finalized)
- ECD builds (customer builds)
- BLDR, RBBLDR, RBMGR configurations
- DCOMSIM, BSWSimDCOM, DSMSim builds
- BLU (Bootloader Update) builds

### 12. **Chrysler IPB PHEV Variant** (BB53355)

- Similar configuration set as ICE variant
- PHEV-specific builds and variants

## INTERACTIVE BUILD SELECTION WORKFLOW

1. **Display Available Build Configurations**:

   - Group configurations by BB number and category
   - Show configuration name, BB number, and description
   - Format: `[Index] ConfigurationName (BBNo: BBXXXXX) - Description`
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

   - **CRITICAL**: Use the MTC (MBuild Tool Chain) PowerShell command format, NOT the batch file scripts
   - Extract the workspace root directory (parent directory of `Cfg_Configurations.xml`)

     - Example: If config file is at `C:\TSDE_Workarea\LNG1COB\IPB_CHY\CHRYSLER_IPB\Cfg_Configurations.xml`
     - Then workspace root is: `C:\TSDE_Workarea\LNG1COB\IPB_CHY\CHRYSLER_IPB`
   - **For Full Build (Option 1)**, generate command in this format:

     ```powershell
     C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File C:\MTC10Base\StartMTC\Start-MTC.ps1 -RootDir "<WorkspaceRoot>" -Config <ConfigurationName> -GenerateMakeFile -BuildTarget BUILD
     ```
   - **For Incremental Build (Option 2)**, generate command in this format:

     ```powershell
     C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File C:\MTC10Base\StartMTC\Start-MTC.ps1 -RootDir "<WorkspaceRoot>" -Config <ConfigurationName> -BuildTarget BUILD -ImprovedIncrementalBuild
     ```
   - **Command Parameters**:

     - `<WorkspaceRoot>`: Absolute path to workspace (parent of Cfg_Configurations.xml)
     - `<ConfigurationName>`: The selected configuration name (e.g., DCOMsimxCHRxIPBxICE, BSWSimDCOMxCHRxIPB2xICE)
     - `-GenerateMakeFile`: Only for Full Build - generates makefiles from scratch
     - `-ImprovedIncrementalBuild`: Only for Incremental Build - builds only changed components
     - `-BuildTarget BUILD`: Standard build target for all builds
5. **Execute Build**:

   - Display the generated command to the user for confirmation
   - Execute the MTC PowerShell command in the terminal
   - Monitor build progress and capture output
   - **⚠️ CRITICAL WARNING**: Once the build has started, DO NOT push any additional commands in the same terminal. The MTC build process is sensitive to interruptions and additional terminal input can cause build failures or corruption. Wait for the build to complete before issuing any new commands.
6. **Build Verification**:

   - Check build log for errors and warnings
   - Verify output files in `Gen/<ConfigurationName>/` directory
   - Report build status to user

## MTC BUILD COMMAND PATTERNS

### MTC PowerShell Command Format (CURRENT STANDARD):

**Full Build Command:**

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File C:\MTC10Base\StartMTC\Start-MTC.ps1 -RootDir "<WorkspaceRoot>" -Config <ConfigurationName> -GenerateMakeFile -BuildTarget BUILD
```

**Incremental Build Command:**

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File C:\MTC10Base\StartMTC\Start-MTC.ps1 -RootDir "<WorkspaceRoot>" -Config <ConfigurationName> -BuildTarget BUILD -ImprovedIncrementalBuild
```

**Command Parameters Explained:**

- `-ExecutionPolicy Bypass`: Bypasses PowerShell execution policy
- `-NoLogo -NonInteractive -NoProfile`: Suppress output and run without user interaction
- `-File C:\MTC10Base\StartMTC\Start-MTC.ps1`: MTC build orchestration script
- `-RootDir "<WorkspaceRoot>"`: Absolute path to workspace (parent of Cfg_Configurations.xml)
- `-Config <ConfigurationName>`: Build configuration name from XML
- `-GenerateMakeFile`: Generate makefiles from scratch (Full Build only)
- `-BuildTarget BUILD`: Standard build target
- `-ImprovedIncrementalBuild`: Build only changed components (Incremental Build only)

**Example Commands:**

For **DCOMsimxCHRxIPBxICE** Full Build:

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File C:\MTC10Base\StartMTC\Start-MTC.ps1 -RootDir "C:\TSDE_Workarea\LNG1COB\IPB_CHY\CHRYSLER_IPB" -Config DCOMsimxCHRxIPBxICE -GenerateMakeFile -BuildTarget BUILD
```

For **DCOMsimxCHRxIPBxICE** Incremental Build:

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File C:\MTC10Base\StartMTC\Start-MTC.ps1 -RootDir "C:\TSDE_Workarea\LNG1COB\IPB_CHY\CHRYSLER_IPB" -Config DCOMsimxCHRxIPBxICE -BuildTarget BUILD -ImprovedIncrementalBuild
```

### Legacy Build Scripts (DEPRECATED - For Reference Only):

```
MB_IPB_BCT_ONLY.cmd
MB_IPB_BSW_IncrementalBuild.cmd
MB_IPB_BSW_RebuildAll.cmd
MB_IPB_BSW_withRTE_IncrementalBuild.cmd
MB_IPB_BSW_withRTE_RebuildAll.cmd
MB_IPB_BSWSim_Dcm_IncrementalBuild.cmd
MB_IPB_BSWSim_Dcm_RebuildAll.cmd
MB_IPB_BSWSim_Net_IncrementalBuild.cmd
MB_IPB_BSWSim_Net_RebuildAll.cmd
MB_IPB_CSW_IncrementalBuild.cmd
MB_IPB_CSW_RebuildAll.cmd
MB_IPB_CSW_withRTE_IncrementalBuild.cmd
MB_IPB_CSW_withRTE_RebuildAll.cmd
MB_IPB_HSWSimDefault_IncrementalBuild.cmd
MB_IPB_HSWSimDefault_RebuildAll.cmd
MB_IPB_Sfun4ASWOnly_BuildNoCodeGen.cmd
MB_IPB_Sfun4ASWOnly_IncrementalBuild.cmd
MB_IPB_Sfun4ASWOnly_Makefile_Only.cmd
MB_IPB_Sfun4ASWOnly_RebuildAll.cmd
MB_IPB_XPASS_IncrementalBuild.cmd
MB_IPB_XPASS_RebuildAll.cmd
```

**Note:** These batch files are still present in the workspace but should NOT be used. Always use the MTC PowerShell command format shown above.

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

--- IPB CSW Area (BB84030) ---
[1] IPBCSWxIntCANTransceiver (BB84030)
    IPB mainstream project CSW configuration using the ASIC Internal Can Transceiver

[2] IPBCSWNonXCPxIntCANTransceiver (BB84030)
    IPB mainstream project CSW configuration for Renesas D4 target device using the ASIC Internal Can Transceiver

[3] IPBCSWwithRTE (BB84030)
    IPB mainstream project CSW configuration with RTE

--- Chrysler IPB ICE Variant (BB53514) ---
[101] CHRxIPB2xICExEP800102xXPASS (BB53514)
      Chrysler IPB ICE Variant, XPASS build

[102] CHRxIPB2xICExEP800102xECA (BB53514)
      Chrysler IPB ICE Variant, CSW build with XCP

[103] DCOMsimxCHRxIPBxICE (BB53514)
      HSWSIM based Chrysler IPB ICE Variant, BSW DCOM Simulation Build

--- Chrysler IPB PHEV Variant (BB53355) ---
[201] CHRxIPB2xPHEVxEP800102xXPASS (BB53355)
      Chrysler IPB PHEV Variant, XPASS build

[202] CHRxIPB2xPHEVxEP800102xECA (BB53355)
      Chrysler IPB PHEV Variant, CSW build with XCP

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

- [ ] ✅ All configurations from XML are accurately extracted
- [ ] ✅ Configuration names and BB numbers are correctly displayed
- [ ] ✅ Build categories are logically organized
- [ ] ✅ User selection workflow is clear and interactive
- [ ] ✅ Build command mapping is accurate
- [ ] ✅ Build verification steps are comprehensive
- [ ] ✅ Error handling for build failures is in place
- [ ] ✅ Build output location is correctly identified

### Common Mistakes to Avoid:

- Executing build without user confirmation
- Not verifying the build script exists before execution
- Ignoring build log errors and warnings
- Not checking build output directory for artifacts
- Using wrong build script for the selected configuration
- Not providing clear feedback on build status
- Failing to handle build errors gracefully
- **⚠️ CRITICAL: Pushing additional commands to the terminal while a build is running (this will cause build failures or corruption)**

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
