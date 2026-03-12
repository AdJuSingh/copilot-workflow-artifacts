
# DTC Configuration and Failure Mapping

<!-- Purpose: Guide agents to extract and structure DTC configuration from Requirements.csv -->
<!-- Version: 1.1 | Last Updated: 2025-11-24 -->

---

## Overview

### DTC Definition

A **DTC (Diagnostic Trouble Code)** is a standardized code used to identify and report specific failures detected by the ECU. Multiple failures can share the same DTC code when they represent similar diagnostic conditions.

---

## DTC Grouping Concept

### DTC Mapping Behavior

- Multiple failures can be mapped to the **same DTC code**
- Each DTC has associated configuration parameters that apply to all mapped failures
- DTC Attributes define common behavior for groups of DTCs (freeze frame, aging, priority, etc.)

### DTC Mapping Example

```text
DTC: 0x123456 ("Hydraulic undervoltage failure")
Mapped Failures:
  - FW_HydraulicUndervoltage1 (9.6V threshold)
  - FW_HydraulicUndervoltage2 (8.6V threshold)
  - FW_HydraulicUndervoltage3 (7.6V threshold)

All three failures report the same DTC but have different detection thresholds
```

---

## DTC Information Extraction

### Information Sources

#### From Failure Requirements (SWFS_*)

Extract the following DTC parameters from each failure requirement in `Requirements.csv`:

> **IMPORTANT**: These fields appear within the same SWFS_* requirement text block as the failure definition. Look for them in the multi-line CSV cell content.

| Parameter | Field Name in CSV | Description | Location |
|-----------|------------------|-------------|----------|
| **DTC** | `DTC` | Diagnostic Trouble Code (hex format: 0x123456) | Within SWFS_* requirement text |
| **DTC Name** | `DTC name` | Human-readable description of the DTC | Within SWFS_* requirement text |
| **Warning Bit Indicator** | `Warning bit indicator` | Boolean flag (True/False) | Within SWFS_* requirement text |
| **DTC Attribute** | `DTC Attribute:` or `DTC Attribute` | Reference to DTC attribute configuration (e.g., DTCAttribute_CHR_NonOBD) | Within SWFS_* requirement text (may appear in any SWFS_* for the same DTC) |
| **DTC Severity** | `DTC severity` | Severity level (e.g., Immediately, Deferred, etc.) | Within SWFS_* requirement text |

#### Field Variations

- Field names may use different capitalization: `DTC severity`, `DTC Severity`, etc.
- Look for colon separator: `DTC Attribute:` or just spaces `DTC Attribute`
- DTC Attribute may only appear in one SWFS_* even if multiple failures share the same DTC

#### From DTC Attribute Requirements (SWCS_*)

Look for requirements starting with **"General Requirements to Configure DTCAttribute_<ATTRIBUTE_NAME>"**.

These appear as separate entries in `Requirements.csv` (e.g., `SWCS_1`, `SWCS_2`, etc.).

Extract the following configuration parameters:

| Parameter | Field Name in CSV | Description | Example Value |
|-----------|------------------|-------------|---------------|
| **DTC Kind** | `DTC kind:` | Type of DTCs covered | "All DTCs", "OBD DTCs", "Non-OBD DTCs" |
| **Freeze Frame Class** | `Freeze Frame Class:` | Freeze frame configuration class | DemFreezeFrameClass_RBAPLCUST |
| **Extended Data Class** | `Extended Data Class:` | Extended data configuration class | DemExtendedDataClass_RB |
| **Number of Freeze Frame Records** | `Number of freeze frame records:` | Count of freeze frame snapshots to store | 2 |
| **Failure Cycle Counter Threshold** | `Failure cycle counter threshold:` | Cycles before failure is confirmed | 1 |
| **Aging Cycle Counter Threshold** | `Aging cycle counter threshold:` | Cycles before failure ages out | 40 |
| **DEM DTC Priority** | `Dem DTC Priority:` | Priority value for DEM (0-255, where 1 is highest) | 255 |
| **DTC Event Destination** | `DTC event destination:` | Memory location | "Primary memory", "Secondary memory", "Mirror memory" |

> **Note**: All 8 parameters must be present in SWCS_* requirement for complete DTC Attribute configuration.

---

### Extraction Workflow

#### Step 1: Parse all SWFS_* requirements

- Collect DTC codes from each failure requirement
- Extract DTC name, DTC severity, Warning bit indicator from each SWFS_*
- Look for DTC Attribute reference in any SWFS_* (may appear in only one failure for shared DTC)

#### Step 2: Group failures by DTC code

- Identify which failures share the same DTC (e.g., 0x123456)
- Create "Failures Mapped" list for each unique DTC

#### Step 3: Extract DTC Attribute references

- Check all SWFS_* requirements for DTC Attribute field
- Note: DTC Attribute may only be specified in one SWFS_* even if multiple failures share the DTC
- Use the DTC Attribute value found in any SWFS_* for all failures with that DTC

#### Step 4: Parse SWCS_* requirements

- Search for "General Requirements to Configure DTCAttribute_<NAME>"
- Extract all 8 DTC Attribute configuration parameters
- Match SWCS requirement ID to DTC Attribute name

#### Step 5: Match and merge

- Combine failure-level DTC info (from SWFS_*) with DTC Attribute configuration (from SWCS_*)
- Validate all 8 parameters extracted from SWCS_*
- Flag missing information if any parameter not found

---

### CRITICAL: What Copilot Must Do and Must NOT Do

#### ✅ MUST DO

- **Extract DTC information from SWFS_* text**: DTC code, name, severity, warning bit indicator are within the same requirement
- **Search ALL SWFS_* for DTC Attribute**: May appear in only one failure even if multiple failures share the DTC
- **Parse SWCS_* requirements separately**: Look for SWCS_1, SWCS_2, etc. in separate CSV entries
- **Extract all 8 DTC Attribute parameters**: Validate complete configuration from SWCS_*
- **Use exact values from Requirements.csv**: No normalization except as specified in other instructions

#### ❌ MUST NOT DO

- **DO NOT assign DTC codes** - only extract from Requirements.csv SWFS_* text
- **DO NOT create DTC attributes** - only extract from Requirements.csv
- **DO NOT assume DTC attribute values** - if SWCS_* missing, request from user
- **DO NOT modify DTC configurations** - use exactly as specified in requirements
- **DO NOT assume DTC Attribute is missing** - check ALL SWFS_* entries before requesting from user

---

## DTC Configuration Template

### DTC Summary Section Format

This section should appear in `DEM_Requirements.md` after all Node and Failure sections:

---

```markdown
---

## DTC Configuration Summary

### DTC: <DTC_Code>

#### DTC Information
| Parameter | Value |
|-----------|--------|
| **DTC Code** | <DTC_hex_code> |
| **DTC Name** | <DTC_description> |
| **Failures Mapped** | <Failure_1>, <Failure_2>, <Failure_3>, ... |
| **Warning Bit Indicator** | <True_or_False> |
| **DTC Attribute** | <DTCAttribute_Reference> |
| **DTC Severity** | <Severity_level> |

#### DTC Attribute Configuration: <DTCAttribute_Name>
| Parameter | Value |
|-----------|--------|
| **DTC Kind** | <All_DTCs_or_specific> |
| **Freeze Frame Class** | <FreezeFrame_class_name> |
| **Extended Data Class** | <ExtendedData_class_name> |
| **Number of Freeze Frame Records** | <Record_count> |
| **Failure Cycle Counter Threshold** | <Cycle_count> |
| **Aging Cycle Counter Threshold** | <Aging_cycles> |
| **DEM DTC Priority** | <Priority_0_to_255> |
| **DTC Event Destination** | <Memory_location> |

...repeat for each unique DTC...
```

### Complete Example
```markdown
## DTC Configuration Summary

### DTC: 0x123456

#### DTC Information
| Parameter | Value |
|-----------|--------|
| **DTC Code** | 0x123456 |
| **DTC Name** | Hydraulic undervoltage failure |
| **Failures Mapped** | FW_HydraulicUndervoltage1, FW_HydraulicUndervoltage2, FW_HydraulicUndervoltage3 |
| **Warning Bit Indicator** | True |
| **DTC Attribute** | DTCAttribute_CHR_NonOBD |
| **DTC Severity** | Immediately |

#### DTC Attribute Configuration: DTCAttribute_CHR_NonOBD
| Parameter | Value |
|-----------|--------|
| **DTC Kind** | All DTCs |
| **Freeze Frame Class** | DemFreezeFrameClass_RBAPLCUST |
| **Extended Data Class** | DemExtendedDataClass_RB |
| **Number of Freeze Frame Records** | 2 |
| **Failure Cycle Counter Threshold** | 1 |
| **Aging Cycle Counter Threshold** | 40 |
| **DEM DTC Priority** | 255 |
| **DTC Event Destination** | Primary memory |
```

---

## Missing Information Handling

### If DTC Information is Missing

**Request from user**:

```text
DTC code not found for failure [Failure_Name] in Requirements.csv. 
Please provide DTC code (hex format: 0xXXXXXX)
```

**Request DTC Attribute**:

```text
DTC Attribute not specified for failure [Failure_Name]. 
Please provide DTC Attribute reference (e.g., DTCAttribute_CHR_NonOBD)
```

### If DTC Attribute Configuration is Missing

**Request configuration requirement**:

```text
DTC Attribute configuration 'DTCAttribute_<NAME>' referenced by failures 
but no SWCS requirement found. Please provide configuration details or 
add SWCS requirement to Requirements.csv
```

### DTC Attribute Consistency Validation

> **CRITICAL**: All failures referencing the same DTC Attribute must use identical configuration

**Validation Rules**:

- **Check all failures** that reference the same DTC Attribute
- **If different DTC Attributes found for same DTC code**: Flag as warning but allow (different failures under same DTC can have different attributes)
- **Never modify DTC Attribute references**: Always use exactly as specified in Requirements.csv

---

## Implementation Requirements

### DTC Analysis Output

For each identified DTC, the analysis must include:

1. **Complete Failure List**: All failures mapped to this DTC code
2. **DTC Configuration**: All DTC-level parameters
3. **DTC Attribute Details**: Complete attribute configuration from SWCS requirements
4. **Missing Information**: Clear requests for missing DTC data

### No Assumptions Rule

> **CRITICAL**: Never make assumptions about missing DTC information

- **Never assign DTC codes** - only extract from Requirements.csv or request from user
- **Never create DTC configurations** - only use values from requirements
- **Never assume DTC attribute values** - request from user if SWCS requirement missing
- **Never modify DTC groupings** - only use failures explicitly mapped to same DTC code

---

## Validation Checklist

### DTC Extraction Validation

- [ ] DTC codes extracted from Requirements.csv for all failures
- [ ] Failures grouped by DTC code correctly
- [ ] DTC Attribute references extracted from failure requirements
- [ ] SWCS requirements parsed for DTC Attribute configurations
- [ ] All DTC Attribute parameters extracted or requested from user

### Quality Assurance

- [ ] No DTC code assignments made by Copilot
- [ ] No DTC attribute assumptions made by Copilot
- [ ] Complete failure mapping for each DTC
- [ ] DTC configuration source clearly documented (Requirements.csv vs User Input)

---

## Integration with Main Analysis

### Placement in DEM_Requirements.md

The DTC Configuration Summary should appear at the end of the document, after all Node and Failure sections:

---

```markdown
# DEM Failure Analysis

## Node: <Node_Name>
### Failure: <Failure_Name>
...

---

## DTC Configuration Summary

### DTC: <DTC_Code>
...

---

## Quality Validation Checklist
...
```

---

### Reference in Individual Failures

Each failure should still include its DTC information in the failure-specific section:

```markdown
#### DTC Configuration
| Parameter | Value | Source |
|-----------|--------|--------|
| **DTC** | <DTC_code> | From Requirements.csv |
| **DTC Name** | <DTC_description> | From Requirements.csv |

#### DTC Extended Information
| Parameter | Value | Source |
|-----------|--------|--------|
| **DTC Severity** | <Severity> | From Requirements.csv |
| **Warning Bit Indicator** | <True_or_False> | From Requirements.csv |
| **DTC Attribute** | <DTCAttribute_reference> | From Requirements.csv (may be in different SWFS_*) |
```

> **Note**: DTC Attribute may be specified in a different SWFS_* requirement than the current failure. The agent should search all SWFS_* with the same DTC code to find the DTC Attribute reference.

---

## Copilot No-Assumption Checklist for DTC Configuration

> **CRITICAL**: Never assume missing DTC information - Always request from user

- [ ] ✅ **DTC Code**: If not in Requirements.csv, request from user - do NOT generate or assume
- [ ] ✅ **DTC Name**: If not in Requirements.csv, request from user
- [ ] ✅ **DTC Attribute**: If not specified in Requirements.csv, request from user - do NOT select default
- [ ] ✅ **DTC Severity**: If not in Requirements.csv, request from user
- [ ] ✅ **Warning Bit Indicator**: If not in Requirements.csv, request from user
- [ ] ✅ **SWCS Requirement**: If referenced DTC Attribute has no SWCS requirement, request user to add it
- [ ] ✅ **DTC Attribute Configuration**: Extract all 8 parameters from SWCS requirement or request from user
- [ ] ✅ **No Default DTC Attributes**: Do not provide default attribute values - always request
- [ ] ✅ **Exact Extraction**: Use DTC attribute names exactly as written in Requirements.csv
- [ ] ✅ **Clear Missing Requests**: "DTC Attribute configuration [DTCAttribute_Name] not found in Requirements.csv. Please add SWCS requirement or provide configuration parameters."
- [ ] ✅ **Status Tracking**: Mark each DTC parameter as either "From Requirements.csv" or "Requested from user"

