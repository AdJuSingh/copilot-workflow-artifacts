---
applyTo: "**"
---


# Copilot Instructions for HSW Unit Testing

## Project Overview

This codebase contains embedded automotive software components following HSW (Hardware Software) architecture. Components are structured with standardized directories including:
- `api/` – Public header files defining interfaces and configuration structures.
- `src/` – Source code, organized by hardware platform.
- `cfg/` – XML configuration files for build/test variants.
- `tst/` – Unit and integration test definitions, including XML test lists and stub implementations.
- `scripts/` – Build/test automation scripts, including batch files and ARXML parameter definitions.
- `doc/` – Documentation, design files, and changelogs.

## Build & Test Workflow

### Unit Test Execution

To run unit tests for any component, follow these steps:

1. **Locate Component Test Configuration**: Each component has unit test XML files in its directory structure, typically in:
   - `<component_path>/tst/<component>_unittests.xml`

2. **Run Unit Tests**: Use the following command pattern from the root directory:
   ```cmd
   libu\LightlyBuild.cmd --gendir=Gen --config=<TEST_CONFIG_NAME> --test --clean-first --not-parallel --simplexmlconfig_file=<PATH_TO_UNITTEST_XML>
   ```

### Example Usage

When a user specifies:
- Component: `RBEVP` 
- Test Config: `TRBEVPCOORandACTHandler`

The command would be:
```cmd
rb\as\core\tools\libu\LightlyBuild.cmd --gendir=Gen --config=TRBEVPCOORandACTHandler --test --clean-first --not-parallel --simplexmlconfig_file=rb/as/core/hwp/hsw/rbevp/tst/rbevp_unittests.xml
```

### How to Help Users

1. **Identify Root Directory**: Look for the folder containing `rb/` subdirectory
2. **Find Test XML**: Search the component's directory tree for `*_unittests.xml` files
3. **Extract Config Names**: Parse the XML file to find available test configuration names
4. **Generate Command**: Construct the LightlyBuild command with the correct paths


## Key Patterns & Conventions


### Component Architecture
- **Hardware Variants**: Code organized by target hardware (EV7135, EV7021, EV8000, etc.)
- **AUTOSAR Compliance**: Follows automotive software architecture standards
- **MISRA C 2012**: Safety-critical C development standards enforced

### Directory Structure
- **api/**: Public header files and interfaces
- **src/**: Source code organized by hardware platform/variant
- **cfg/**: XML configuration files for build/test variants  
- **tst/**: Unit and integration tests with XML definitions
- **Gen/**: Generated build outputs and temporary files
- **rb/as/core/**: Core HSW framework and tools

### Test Configuration Patterns
- **XML Test Definitions**: `*_unittests.xml` files define test cases and configurations
- **Build Configuration Files**: `.bcfg` files specify compilation settings
- **Stub Dependencies**: Hardware abstraction stubs in `tst/stub/` directories


## Troubleshooting

### Common Issues
- **Build Failures**: Check XML configuration files for syntax errors and path validity
- **Missing Dependencies**: Verify all required tools are in PATH (MTC, GCC, PowerShell)
- **Path Issues**: Ensure forward slashes in XML paths, backslashes in Windows commands
- **Configuration Mismatch**: Verify test config name matches XML definitions exactly

### Build System Requirements
- **MTC Tools**: Versions 10.8-10.13 required in `C:/MTC10Base/`
- **VS Code Extensions**: C/C++ extension recommended for IntelliSense
- **PowerShell**: Version 5.1+ for build script execution
- **Python**: Required for some build automation scripts

### File Locations to Check
- **Root Detection**: Look for `rb/` directory to find project root
- **Test XMLs**: Usually in `<component>/tst/*_unittests.xml`
- **Build Configs**: `.bcfg` files and `Cfg_Configurations.xml`
- **Generated Files**: Check `Gen/` directory for build outputs and errors

## Workflow Examples

### Adding a New Test Case
1. Locate component's test XML file (e.g., `rb/as/core/hwp/hsw/<component>/tst/<component>_unittests.xml`)
2. Add new test configuration entry with unique `ConfigurationName`
3. Implement test source code in appropriate `tst/` subdirectory
4. Update or create stubs if needed for hardware dependencies
5. Run unit test using the command pattern shown above

### Component Analysis Workflow
When user mentions a component:
1. **Search for Component**: Use file system search to locate component directory
2. **Find Test Configs**: Parse XML files to extract available configurations
3. **Identify Dependencies**: Check include paths and stub requirements
4. **Generate Command**: Create proper LightlyBuild command with correct paths

### Running Tests for Different Components
```cmd
# For RBPRESSSENT component with TRBPRESSSENTCalcGradient config
rb\as\core\tools\libu\LightlyBuild.cmd --gendir=Gen --config=TRBPRESSSENTCalcGradient --test --clean-first --not-parallel --simplexmlconfig_file=rb/as/core/hwp/hsw/rbpress/rbpresssent/tst/rbpresssent_unittests.xml

# For RBLIPS component with TRBLiPSSENTMonitorings config  
rb\as\core\tools\libu\LightlyBuild.cmd --gendir=Gen --config=TRBLiPSSENTMonitorings --test --clean-first --not-parallel --simplexmlconfig_file=rb/as/core/hwp/hsw/rblips/tst/rblips_unittests.xml
```

---

**AI Assistant Guidelines:**
When users request unit testing for a component:
1. **Auto-detect root directory**: Find the folder containing `rb/` subdirectory
2. **Component discovery**: Search for the component in the directory structure
3. **XML parsing**: Locate and parse `*_unittests.xml` to find available configurations
4. **Command generation**: Build the complete LightlyBuild command with proper paths
5. **Execution guidance**: Provide the exact command to run from the root directory

**Key Tools and Extensions:**
- Use `file_search` to locate components and XML files
- Use `read_file` to parse XML configurations  
- Use `semantic_search` to understand component relationships
- Use `run_in_terminal` to execute build commands when requested