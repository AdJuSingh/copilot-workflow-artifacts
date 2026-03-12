# Bosch Failure Memory (BFM) Category Reference

## Category Reference Table
| ID | Category | Typical Use / Scope | Priority Weight (relative order) | Rationale / Example |
|----|----------|---------------------|----------------------------------|---------------------|
| 1 | EcuInternal | PCB level electronic faults | 1 | Component or solder joint failure on ECU PCB |
| 2 | AttachedEcu | Failure in ECU but not PCB | 2 | Valve coil connection issue |
| 10 | HydraulicAggregate* | Sensor/actuator inside hydraulic block (ambiguous vs PCB) | 3 | Pressure sensor inside hydraulic unit |
| 5 | WssFault | Wheel speed sensor faults | 5 | Broken wheel speed sensor wiring |
| 11 | ExternalFaultWithHigherPrio* | External sensor/actuator (NOT network) higher visibility | 6 | External actuator fault that must not be hidden by many network faults |
| 6 | ApbFault | Parking brake motor / connection | 7 | Open circuit / overcurrent PB motor |
| 4 | ApbMssFault | Parking brake motor speed sensor / connection | 8 | PB motor speed signal missing |
| 8 | Rfp_ext | Motor malfunction triggered by external condition | 9 | High resistance supply line |
| 7 | ExternalFault | Generic external (default for customer monitorings incl. network) | 10 | CAN / FlexRay signal invalid (default if no better fit) |
| 9 | TransientFaultState | Transient external fluctuation | 11 | Supply voltage dip |
| 3 | AttachedDevice | Sensor attached to hydraulic block (external connection style varies) | 4 | Linear Position Sensor malfunction |

## Category Selection Guidelines

### Important Notes:
1. Do NOT use ExternalFaultWithHigherPrio for network (bus / signal) failures—use ExternalFault instead.
2. Network signal plausibility / availability issues (e.g. NET_* signals) normally map to ExternalFault.
3. If evidence shows sensor internal defect vs wiring vs PCB ambiguity, evaluate HydraulicAggregate vs AttachedDevice vs ExternalFault.
4. Mark categories with * if they have special escalation or replacement implications (HydraulicAggregate causes component replacement strategy).
5. **DEFAULT RULE**: If, after analysis, none of the defined categories clearly matches, select ExternalFault as the default and document the reasoning ("No specific category criteria met; defaulting per instruction rule").

### Selection Workflow
1. Parse requirement text for clues: keywords like "NET_", "signal", "CAN", "FlexRay" → candidate ExternalFault.
2. Look for physical component references (motor, coil, sensor) and location context (inside hydraulic block, parking brake) to narrow to specific categories (ApbFault, ApbMssFault, HydraulicAggregate, AttachedDevice).
3. If internal ECU electronics (logic, ASIC, PCB temperature) → EcuInternal.
4. If sensor/actuator external but not network and needs higher visibility over network noise → ExternalFaultWithHigherPrio (validate justification).
5. If short-lived transient condition (voltage dip, transient comm glitch with auto-recovery) → TransientFaultState.
6. If none of the above decision points apply decisively → assign ExternalFault (default) and record justification.

### Documentation Requirements in Analysis File
For each SWFS / SWCS diagnostic requirement:
```
Failure Category: <CategoryName> (Justification: <concise reasoning referencing requirement text>)
```
If ambiguous:
```
Failure Category: TBD (Candidates: ExternalFault | ExternalFaultWithHigherPrio) - Reason: <explain missing clarity>
Action: Clarify with system architect / HSW Twiki reference.
```

### Validation Checklist
- [ ] Category selected matches definition and examples.
- [ ] Not using ExternalFaultWithHigherPrio for network failure.
- [ ] Justification present and traceable to requirement wording.
- [ ] Ambiguities explicitly flagged with action.

### Handling Changes
If category changes after review, update:
1. Requirements analysis section (adjust justification)
2. Change History block (log rationale)
3. Any generated Failure Word XML (update <CATEGORY> element)

### Tooling Suggestion (Future Enhancement)
Implement a lightweight lint step to flag suspicious mappings (e.g., NET_ prefix categorized as ExternalFaultWithHigherPrio) for manual review.