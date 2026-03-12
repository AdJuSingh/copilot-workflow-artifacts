# Debouncer Type Selection and Configuration

## Debouncer Type Determination

### Primary Rule
The debouncer type should be explicitly specified in the `Requirements.csv` file:
- Look for field: `Debouncer Type` or `DebouncerType`
- Expected values: `Counter based` or `MonitoringInternal`

### If Debouncer Type is Missing
If the debouncer type is not specified in Requirements.csv:
- **Request user input**: "Debouncer type not specified in requirements. Please provide: CounterBased or MonitoringInternal"
- **Do not assume** or select debouncer type based on available timing parameters

## Counter-Based Debouncer Configuration

### Required Parameters for Counter-Based
When debouncer type is `Counter based`, extract/calculate the following:

| Parameter | Source/Calculation |
|-----------|-------------------|
| **Task Cycle** | From Requirements.csv `TASK_REF` field |
| **Detection Time** | From Requirements.csv `Detection Time` field |
| **Recovery Time** | From Requirements.csv `Recovery Time` field |

### Threshold Calculations
```
DebouncecounterFailedthreshold = -(Detection Time / Task Cycle) [rounded to nearest integer]
DebouncecounterFailedthreshold = +(Detection Time / Task Cycle) [rounded to nearest integer]
DebouncecounterPassedthreshold = -(Recovery Time / Task Cycle) [rounded to nearest integer]
DebouncecounterIncrementstepsize = 1 (default)
DebouncecounterDecrementstepsize = 1 (default)
```

### Jump Values
- **Jump Up Value**: Default = 0 (unless specified in requirements)
- **Jump Down Value**: Default = 0 (unless specified in requirements)
- **Jump Up enabled**: Default = True (unless specified otherwise)
- **Jump Down enabled**: Default = True (unless specified otherwise)


### Missing Information Handling
If any required timing parameter is missing for Counter-Based debouncer:
- **Request from user**: "Counter-based debouncer requires Task Cycle, Detection Time, and Recovery Time. Please provide missing values."

## MonitoringInternal Debouncer

### Configuration
When debouncer type is `MonitoringInternal`:
- No threshold calculations required
- Algorithm handles timing internally
- Document as: `DebouncerType: MonitoringInternal`

## Documentation Format

### Counter-Based Example (sign convention)
```
Debouncer Type: CounterBased
- Failed Threshold: 10 (1000ms / 100ms)    # POSITIVE when failure condition is counted toward triggering
- Passed Threshold: -5 (500ms / 100ms)     # NEGATIVE when recovery lowers the counter back toward clear
- Increment Step: 1
- Decrement Step: 1
- Jump Up value: 0
- Jump Down value: 0
- Jump Up enabled: True
- Jump Down enabled: True
```

### MonitoringInternal Example:
```
Debouncer Type: MonitoringInternal
- Internal algorithm manages timing and thresholds
```

## Validation Rules
- [ ] Debouncer type explicitly specified in requirements or requested from user
- [ ] For Counter-Based: All timing parameters available or requested
- [ ] Threshold calculations performed correctly
- [ ] No assumptions made about debouncer type based on available timing data