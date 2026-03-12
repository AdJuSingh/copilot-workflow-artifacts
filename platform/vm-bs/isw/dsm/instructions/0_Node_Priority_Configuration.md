# Node Configuration and Priority Management

## Node Definition
A **Node** is a logical grouping of similar failures that share common characteristics or system components. Each Node contains multiple failures that are related in terms of functionality, location, or system impact.

## Node Priority Management

### Priority Concept
- Each failure within a Node has an assigned **Priority** value
- **Higher number = Higher priority** (e.g., Priority 3 > Priority 2 > Priority 1)
- When multiple failures within the same Node are active simultaneously, the failure with the highest priority takes precedence
- Lower priority failures are **suppressed** when higher priority failures are active

### Priority Behavior
```
Example: Node_VoltageHandler1 contains 3 failures:
- Failure_A (Priority: 3) - Highest priority
- Failure_B (Priority: 2) - Medium priority  
- Failure_C (Priority: 1) - Lowest priority

If all 3 failures occur simultaneously:
- Only Failure_A (Priority 3) will be logged to memory
- Failure_B and Failure_C will be suppressed
```

## Node Structure Requirements

### Essential Node Information
For implementation purposes, the following must be defined for each Node:

#### Node Identification
- **Node Name**: Unique identifier for the node
- **Parent Node**: Hierarchical reference (if applicable)
- **Node Description**: Brief description of node purpose/scope

#### Failure Mapping
- **Failure List**: All failures belonging to this node
- **Priority Assignment**: Priority value for each failure
- **Priority Justification**: Reason for priority assignment

### Node Configuration Template
```markdown
## Node: <Node_Name>

### Node Information
| Parameter | Value |
|-----------|--------|
| **Node Name** | <Unique_Node_Identifier> |
| **System Strategy** | <System_Strategy_for_Node> |
| **Parent Node** | <Parent_Node_Reference> |

### Failure Priority Mapping
| Failure Name | Priority | Source |
|--------------|----------|--------|
| <Failure_1> | <Priority_Number> | <From_Requirements.csv_or_User_Input> |
| <Failure_2> | <Priority_Number> | <From_Requirements.csv_or_User_Input> |
| <Failure_3> | <Priority_Number> | <From_Requirements.csv_or_User_Input> |

### Priority Behavior
- **Highest Priority Failure**: <Failure_Name> (Priority: <Number_from_requirements_or_user>)
- **Suppression Logic**: When multiple failures active, only highest priority logged
- **Implementation Impact**: Priority-based failure logging and suppression

...then individual failure details...
```

## Priority Assignment Guidelines

### Priority Information Source
- **Primary Source**: Extract priority values from Requirements.csv file
- **DO NOT determine priorities**: Copilot must not assign or suggest priority values
- **DO NOT provide priority justification**: Copilot must not create reasoning for priorities
- **Only extract or request**: Either extract from requirements or request from user

## Information Sources

### From Requirements.csv
- **Node Name**: Extract from "Node name" field
- **Parent Node**: Extract from "Parent Node" field
- **Failure Name**: Extract from "Failure name" field
- **Priority**: Look for "Priority" or similar field for each failure
- **System Strategy**: Extract from "System strategy" field for each failure

### System Strategy Validation
**CRITICAL**: All failures within the same Node must have identical System Strategy
- **Check all failures** in the same Node for System Strategy consistency
- **If different System Strategies found**: Request user to fix in Requirements.csv
- **Never assume or change System Strategy**: Always request user to update Requirements.csv

### Request from User (if issues found)
- **Priority Assignment**: "Priority value not found for [Failure_Name] in Requirements.csv. Please provide priority value (higher number = higher priority)"
- **System Strategy Mismatch**: "System Strategy mismatch detected in Node [Node_Name]. Found: [Strategy1] and [Strategy2]. Please update Requirements.csv so all failures in this Node have the same System Strategy."
- **Missing System Strategy**: "System Strategy not found for failure [Failure_Name] in Requirements.csv. Please add System Strategy field."

### CRITICAL: What Copilot Must NOT Do
- **DO NOT assign priority values**
- **DO NOT create priority justifications**
- **DO NOT determine priority based on failure characteristics**
- **DO NOT suggest priority ranges or guidelines**
- **DO NOT assume or change System Strategy for consistency**
- **DO NOT fix System Strategy mismatches automatically**

## Implementation Requirements

### Node Analysis Output
For each identified Node, the analysis must include:
1. **Complete Failure Inventory**: All failures within the node
2. **Priority Matrix**: Clear priority assignments and rankings
3. **Suppression Logic**: Which failures suppress which others
4. **Missing Information**: Clear requests for missing priority data

### No Assumptions Rule
- **Never assign priority values** - only extract from Requirements.csv or request from user
- **Never create priority justifications** - do not explain why a priority was assigned
- **Never assume node groupings** - only use failures explicitly listed in requirements
- **Never suggest priority ranges** - only work with actual values provided

## Validation Checklist
- [ ] Node name extracted from Requirements.csv
- [ ] All failures mapped to correct nodes
- [ ] System Strategy consistency validated across all failures in each Node
- [ ] System Strategy mismatches flagged for user correction (if found)
- [ ] Priority values extracted from Requirements.csv OR requested from user (if missing)
- [ ] NO priority justifications created by Copilot
- [ ] NO priority assignments made by Copilot
- [ ] NO System Strategy assumptions or automatic fixes by Copilot
- [ ] Suppression behavior defined based on actual priority values
- [ ] Complete failure inventory for each node
- [ ] Priority source clearly documented (Requirements.csv vs User Input)

## Integration with Main Analysis
This Node configuration should be integrated into the main DEM failure analysis as an additional section:

```markdown
#### Node Priority Configuration
| Parameter | Value |
|-----------|--------|
| **Node Priority Mapping** | <List_all_failures_with_priorities> |
| **Suppression Logic** | <Describe_which_failures_suppress_others> |
| **Missing Priority Info** | <Request_user_input_for_missing_priorities> |
```