Prompt 0: Generate Requirements Analysis (`DEM_Requirements.md`)
Create a markdown file (`GenFromCopilot/requirements/DEM_Requirements.md`) that analyzes and explains each requirement from `GenFromCoPilot/requirements/Requirements.csv`.

## Usage Modes

**Mode 1 - Complete Document Analysis (Default)**:
- Prompt: "Follow instructions in 0_create_requirements_analysis.prompt.md"
- Behavior: Analyzes ALL failures in Requirements.csv
- Filters out non-failure content (headers, reviews, signals without failures)
- Validates all mandatory fields for all failures

**Mode 2 - Specific Failure Analysis**:
- Prompt: "Follow instructions in 0_create_requirements_analysis.prompt.md. [FailureName1] [FailureName2]"
- Example: "Follow instructions in 0_create_requirements_analysis.prompt.md. FW_RBNet_Scl_CBC_PT1_IGN_OFF_TIME_LNG_Invalid"
- Behavior: Analyzes ONLY the specified failure(s)
- Validates mandatory fields for specified failures only

## Critical Rules
- Strictly Refer "0_CREATE_SWFS_REQUIREMENTS_ANALYSIS" instruction file for generating the output
- **ALWAYS GENERATE DEM_Requirements.md**: Even if mandatory fields are missing, generate the file with missing information documented at the end of each failure
- **Document ONLY Failure Information**: Ignore non-failure content (headers, reviews, signals without failures)
- **Group by Node**: Organize all failures by their Node hierarchy
- NO ASSUMPTIONS: Extract ONLY information present in Requirements.csv (no elaboration)
- Missing mandatory fields are reported at the end of each individual failure (not in a separate upfront section)

## Expected Output
- **DEM_Requirements.md is ALWAYS generated** with:
  - Failures grouped by Node
  - Complete failure analysis for each failure
  - ⚠️ WARNING indicators in failure heading for those with missing mandatory fields
  - Missing fields documented at end of each failure in "⚠️ Missing Mandatory Fields" section
  - ✅ READY / ❌ BLOCKED status for each failure
  - "⚠️ Configuration Warnings" section at the end (customer defaults, DTC inconsistencies)
