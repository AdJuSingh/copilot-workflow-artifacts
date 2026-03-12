# DCOMSIM Component Test Implementation Guide

## Service Identification (How to Map Requests)

**DID 0xFxxx**  Service 0x22 (Read) or 0x2E (Write)
**RID 0xFxxx**  Service 0x31 (Routine)
**PID 0xnn**  OBD Classic or OBD on UDS
**"Session control"**  Service 0x10
**"Security access"**  Service 0x27
**"DTC clear/read"**  Service 0x14/0x19

## Instruction Loading Sequence

1. **Read Base Instructions**: `.github/instructions/CT/ct00-base-common.instructions.md`
2. **Review Index**: `.github/instructions/CT/ct-index.instructions.md`
3. **Read Test Generation Guide**: `.github/instructions/CT/ct-test-generation.instructions.md`
4. **Read Service-Specific Instructions** based on service type:
   - **Service 0x10**: `.github/instructions/CT/ct-service-10-diagnostic-session-control.instructions.md`
   - **Service 0x14**: `.github/instructions/CT/ct-service-14-clear-dtc.instructions.md`
   - **Service 0x19**: `.github/instructions/CT/ct-service-19-read-dtc.instructions.md`
   - **Service 0x22**: `.github/instructions/CT/ct-service-22-read-data.instructions.md`
   - **Service 0x27**: `.github/instructions/CT/ct-service-27-security-access.instructions.md`
   - **Service 0x28**: `.github/instructions/CT/ct-service-28-communication-control.instructions.md`
   - **Service 0x2E**: `.github/instructions/CT/ct-service-2e-write-data.instructions.md`
   - **Service 0x31**: `.github/instructions/CT/ct-service-31-routine-control.instructions.md`
   - **OBD Classic**: `.github/instructions/CT/ct-obd-classic.instructions.md`
   - **OBD on UDS**: `.github/instructions/CT/ct-obd-on-uds.instructions.md`
5. **Reference this quality guide** for final validation

## File Structure & Naming

- Filename: `DCOM_SWT_Service<ServiceHex>_<DIDName>.c` in `rb\as\ms\core\app\dcom\RBDcmSim\DCOMSIM\CT_Generator\tst\TestScripts\`
- Include: `SwTest_Global.h`, `TestEnvironment_Base.h`, `ASWIF_CommonConfig.h`, `Platform_Types.h`, `Compiler.h`, `Std_Types.h`
- Header: TEST SCENARIOS section, SWCS_xx references, generation metadata

## Test Script Core Components (How to Structure)

1. Test header with requirements traceability
2. Standard includes from instruction patterns
3. Precondition setup (session, security, timing)
4. Positive test cases (valid scenarios)
5. Negative test cases (invalid scenarios, NRC verification)
6. Timing validation (P2/P3 timeouts)
7. Post-condition validation
8. Signal setup/teardown

## Test Coverage (15-20 cases minimum)

- **Positive (5+)**: Valid requests, all data combinations, sequential operations
- **Negative/NRC (6-8+)**: 0x13 (length), 0x22 (conditions), 0x31 (range), 0x33 (security), 0x7F (session)
- **Session (3-4+)**: DefaultExtended transitions, timeouts, availability per session
- **Boundary (3-4+)**: Min (0x00), max (0xFF/0xFFFF), mid-range, bit patterns
- **Timing (2+)**: P2/P2* compliance, rapid sequential requests

## Response Length (CRITICAL)

- Source: `doc/requirements/DCOM_DID_Requirements.md` ONLY
- Formula: `1 (SID) + 2 (DID) + N (data) = Total` with comment in EVERY test
- Negative responses: 3 bytes (`7F <Service> <NRC>`)
- NO placeholders without verification

## UDS Protocol

- Format: Space-separated uppercase hex (no 0x prefix)
- Sessions: `10 01` (Default), `10 03` (Extended)
- Verify all service IDs, NRCs, request/response formats against UDS standard

## Service-Specific Test Requirements (How to Test Each Service)

**UDS Services:**

- **0x10**: Session transitions, timeout validation, persistence
- **0x14**: DTC clearing, memory verification
- **0x19**: DTC reading, status, freeze frames
- **0x22**: DID reading, session/security dependencies
- **0x27**: Seed/key validation, security unlock
- **0x28**: Communication control, subnet validation
- **0x2E**: DID writing, NVM persistence, validation
- **0x31**: Routine start/stop/results, execution status

**OBD Services:**

- **Classic (0x00)**: Physical (0x7E0) / Functional (0x7DF) addressing, DID 0xFD1B=0x00
- **On UDS (0x01)**: Service 0x22 with PIDs (0xF4xx/0xF8xx), DID 0xFD1B=0x01

## Implementation File Reference (How to Use Source Code)

 **Extract:** Headers, interfaces, data types, constants
 **Forbidden:** Implementation logic, function bodies, test patterns

## Code Quality (How to Write Code)

- Function naming: `TC_<ServiceHex>_<DIDHex>_<NN>` with `@testlists` annotation
- Framework: `SWT_Eval()`, `HSWFT_DiagSendRequest()`, `HSWFT_DiagEvalResponse()`, `HSWFT_DiagDelayMS()`
- Stabilization: `SWT_RunSystemMS(10000)` after message setup
- Messages: `DefineMESGDef()`, `SendMESGDef()`, `l_<MessageName>.<Field>` assignments

## Documentation & Traceability

- Comments: Test purpose, expected behavior, success criteria
- TEST SCENARIOS: List all positive/negative/session/boundary/timing scenarios
- Requirements: SWCS_xx references, design link (`doc/design/DCOM_DID_<Number>_<Name>.uml`)

## TestSpec Excel File (Generate Only If User Requests)

**IMPORTANT**: TestSpec Excel file generation is OPTIONAL and depends on user preference. Always ask the user before starting:
- "What would you like me to generate?"
  - Option 1: Both C test file and TestSpec Excel file
  - Option 2: C test file only
  - Option 3: TestSpec Excel file only (requires existing C file)

If user requests Excel file (Option 1 or 3), generate it DIRECTLY using Python code execution with openpyxl. **DO NOT create a standalone .py script file**.

### File Naming & Location

- Filename: `CT_{ServiceName}_{Identifier}_TestSpec.xlsx`
- Location: Same directory as the .c file: `rb\as\ms\core\app\dcom\RBDcmSim\DCOMSIM\CT_Generator\tst\TestScripts\`
- Sheet name: `CT_Function_Proxi` (must match template exactly)
- Template source: `doc\CT_TestSpec_Template.xlsx`

### Template Row Preservation (CRITICAL)

- **Row 1** (header row, height=30, dark-blue fill `1F4E79`, bold white Calibri 11): Copy verbatim — Test Name, Status, RB_DoorsLink, Description, RB_Stimulation, RB_Expected_Result, RB_TestEnvironment, RB_Comments, Designer, RB_TEST_TYPE, RB_AutomationScript, RB_Script_Status, RB_Variant, RB_FNID, QC_Link
- **Row 2** (guidance row, height=120, sky-blue fill `00B0F0`): Copy verbatim with all per-column guidance text and formatting
- **Rows 3+**: One new row per test case derived from the .c file
- Preserve all column widths from template (A=14, B=12, C=40, D=65, E=55, F=65, G=20, H=20, I=14, J=20, K=30, L=20, M=16, N=14, O=28)
- Freeze panes at A3 (rows 1–2 always visible)

### Column Mapping (Columns A–O per test case row)

| Col | Header (standardised) | Content |
|-----|-----------------------|---------|
| A | Test Name | Sequential identifier: TC1, TC2, TC3, … |
| B | Status | `"reviewed"` |
| C | RB_DoorsLink | Semicolon-separated SWCS requirement IDs from `@testlists` / `@req` / `@swcs` annotations (format: `000000_SWFS_SWCS_<ID>;`) |
| D | Description | Purpose — one sentence describing what is validated |
| E | RB_Stimulation | Numbered list of UDS request steps (e.g. `1. 10 03\n2. 22 FD 0B`) — uppercase hex, no 0x prefix |
| F | RB_Expected_Result | Numbered list of expected UDS responses (e.g. `1. 50 03 00 32 01 F4\n2. 62 FD 0B ...`) |
| G | RB_TestEnvironment | `"CCSiL"` |
| H | RB_Comments | Leave empty unless specific notes apply |
| I | Designer | `"DCOM"` |
| J | RB_TEST_TYPE | `"Component Test"` |
| K | RB_AutomationScript | Filename of the generated .c test script |
| L | RB_Script_Status | `"PASS"` |
| M | RB_Variant | Leave empty |
| N | RB_FNID | Leave empty |
| O | QC_Link | Leave empty |

### Generation Approach

**CRITICAL**: Generate Excel file DIRECTLY using Python code execution, NOT by creating a separate .py script file.

Use inline Python with `openpyxl` to generate the file directly:

```python
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
import copy

TEMPLATE = r"doc\CT_TestSpec_Template.xlsx"
OUTPUT   = r"rb\as\ms\core\app\dcom\RBDcmSim\DCOMSIM\CT_Generator\tst\TestScripts\CT_{ServiceName}_{Identifier}_TestSpec.xlsx"

# ── Auto-fit helpers ──────────────────────────────────────────────────────────
CHAR_WIDTH  = 1.2   # approximate character-to-column-width ratio
LINE_HEIGHT = 15.0  # approximate height per line of text (points)
MIN_COL_WIDTH  = 10
MAX_COL_WIDTH  = 80   # cap wide columns (E, F) to keep sheet readable
MIN_ROW_HEIGHT = 15
MAX_ROW_HEIGHT = 400

def cell_line_count(value):
    """Count the number of display lines in a cell value."""
    if value is None:
        return 1
    return max(1, str(value).count('\n') + 1)

def cell_max_line_width(value):
    """Return the longest single line width (chars) in a cell value."""
    if value is None:
        return 0
    return max((len(line) for line in str(value).split('\n')), default=0)

def autofit_columns(ws, skip_rows=2):
    """Set column widths to fit data content, respecting MIN/MAX bounds."""
    col_widths = {}
    for row in ws.iter_rows(min_row=skip_rows + 1):
        for cell in row:
            if cell.value is None:
                continue
            col_letter = get_column_letter(cell.column)
            w = cell_max_line_width(cell.value) * CHAR_WIDTH
            col_widths[col_letter] = max(col_widths.get(col_letter, MIN_COL_WIDTH), w)
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = max(MIN_COL_WIDTH, min(MAX_COL_WIDTH, width))

def autofit_rows(ws, skip_rows=2):
    """Set row heights to fit multi-line cell content, respecting MIN/MAX bounds."""
    for row in ws.iter_rows(min_row=skip_rows + 1):
        max_lines = 1
        for cell in row:
            max_lines = max(max_lines, cell_line_count(cell.value))
        row_num = row[0].row
        ws.row_dimensions[row_num].height = max(
            MIN_ROW_HEIGHT,
            min(MAX_ROW_HEIGHT, max_lines * LINE_HEIGHT)
        )
# ─────────────────────────────────────────────────────────────────────────────

wb = load_workbook(TEMPLATE)
ws = wb.active  # CT_Function_Proxi

# Delete all rows from row 3 downward (keep rows 1-2 intact)
for _ in range(ws.max_row, 2, -1):
    ws.delete_rows(_)

# Append test case rows starting at row 3
for row_data in test_cases:  # list of dicts with keys matching columns A-O
    ws.append([
        row_data['test_name'],       # A: TCx
        row_data['status'],          # B: reviewed
        row_data['rb_doors_link'],   # C: SWCS refs
        row_data['description'],     # D: purpose
        row_data['rb_stimulation'],  # E: UDS requests
        row_data['rb_expected'],     # F: UDS responses
        row_data['rb_env'],          # G: CCSiL
        row_data.get('comments',''), # H
        row_data['designer'],        # I: DCOM
        row_data['test_type'],       # J: Component Test
        row_data['script'],          # K: filename
        row_data['script_status'],   # L: PASS
        '',                          # M
        '',                          # N
        '',                          # O
    ])
    # Apply wrap_text + top alignment to all data cells in the new row
    r = ws.max_row
    for col in range(1, 16):  # columns A–O
        cell = ws.cell(row=r, column=col)
        cell.alignment = Alignment(wrap_text=True, vertical='top')

# Auto-fit column widths and row heights for data rows (rows 3+)
autofit_columns(ws, skip_rows=2)
autofit_rows(ws, skip_rows=2)

wb.save(OUTPUT)
```

### Validation Rules

- Number of data rows must equal number of test cases in the .c file
- Column C (RB_DoorsLink): At least one SWCS reference per row; use `000000_SWFS_SWCS_<RequirementID>;` format
- Column E (RB_Stimulation): Must start with `1.` and list numbered steps; each UDS message on its own numbered line
- Column F (RB_Expected_Result): Must have matching numbered steps for each stimulus step
- Column header names must exactly match the standardised template: `RB_Expected_Result`, `QC_Link` (underscores, not spaces)
- Confirm file was written by checking file exists and row count = 2 + len(test_cases)

### File Cleanup (MANDATORY)

**CRITICAL**: After Excel file generation is complete, ensure workspace cleanliness:

- **Final Deliverables**: ONLY `.c` (test file) and `.xlsx` (TestSpec) files should remain in the TestScripts directory
- **Temporary Files**: If ANY Python script files (`.py`) were created during the Excel generation process (e.g., `generate_testspec_*.py`, helper scripts, or any other .py files), they MUST be deleted immediately after successful Excel generation
- **Verification**: After completion, verify that NO `.py` files exist in `rb\as\ms\core\app\dcom\RBDcmSim\DCOMSIM\CT_Generator\tst\TestScripts\` directory related to this test generation
- **Cleanup Command**: Use PowerShell `Remove-Item` or Python `os.remove()` to delete any temporary .py scripts created during the workflow

**Example cleanup verification:**
```powershell
# Check for any .py files in TestScripts directory
Get-ChildItem "rb\as\ms\core\app\dcom\RBDcmSim\DCOMSIM\CT_Generator\tst\TestScripts\" -Filter *.py

# Delete any test generation .py scripts
Remove-Item "rb\as\ms\core\app\dcom\RBDcmSim\DCOMSIM\CT_Generator\tst\TestScripts\generate_*.py" -ErrorAction SilentlyContinue
```

**Rationale**: The instruction emphasizes generating Excel files DIRECTLY using inline Python code execution. However, if any temporary .py scripts are accidentally created or used for debugging purposes, they must be cleaned up to maintain a clean workspace with only production deliverables (.c and .xlsx files).

## Operator Interaction

- When fixing code: Explain problems found first
- When generating tests: Explain what tests will be created first
- For multiple changes: Provide step-by-step overview first

## Security & Best Practices

- Check for vulnerabilities, avoid hardcoded credentials/API keys, validate inputs
- Follow project code style, add type hints/docstrings, comment complex logic
- Use `.env` for variables, document in `README.md`, provide `.env.example`

## Version Control & Change Logging

- Atomic commits with conventional commit format, update `.gitignore`
- Log changes in `changelog.md`: files modified/added/deleted, semantic versioning, date/description

## Testing & Python Specifics

- Unit tests for new functionality, 80%+ coverage, integration tests for APIs
- Python: Use venv (create if missing), `python3 -m flask run`, update `requirements.txt`, PEP 8/484
