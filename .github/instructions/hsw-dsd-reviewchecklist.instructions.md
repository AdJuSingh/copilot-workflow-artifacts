---
applyTo: "**/doc/**/*.md"
description: "HSW Detailed Software Design (DSD) Review Checklist"
---

# Generic HSW Module Detailed Software Design (DSD) Review Checklist

## Purpose
This instruction file provides the review checklists and quality gate criteria for evaluating Detailed Software Design (DSD) documents for HSW (Hardware related Software) modules.

---

## Design Review and Quality Assurance

### Technical Review Checklist
**Architecture Review:**
- [ ] Component responsibilities clearly defined and bounded
- [ ] Interface contracts completely specified with pre/post conditions  
- [ ] Message exchange patterns documented with flow diagrams
- [ ] Task scheduling and timing constraints properly defined
- [ ] Memory and resource usage within acceptable limits

**Safety and Compliance Review:**
- [ ] All safety requirements mapped to implementation
- [ ] Diagnostic coverage adequate for ASIL requirements
- [ ] Fault reaction strategies defined and implemented
- [ ] MISRA C compliance verified and exceptions documented
- [ ] Hardware abstraction properly isolates platform dependencies

**Interface and Integration Review:**
- [ ] Public APIs have complete interface specifications
- [ ] Header dependencies analyzed and circular references avoided
- [ ] Inter-component communication protocols defined
- [ ] Data ownership and synchronization rules established
- [ ] Test interfaces and observability adequate

### Quality Gates and Approval Criteria
**Review Approval Requirements:**
- **Technical Architect**: Design consistency and architecture compliance
- **Safety Engineer**: Safety requirement coverage and ASIL compliance  
- **Integration Lead**: Interface compatibility and system integration
- **Test Engineer**: Testability and verification approach adequacy

---

## Technical Review Checklist

#### Architecture and Design Compliance
- [ ] **Component Scope**: Responsibilities clearly defined with appropriate boundaries
- [ ] **Interface Completeness**: All public APIs documented with complete contracts
- [ ] **Message Protocols**: Inter-component communication patterns fully specified
- [ ] **Data Model**: Central data management documented with ownership rules
- [ ] **Task Architecture**: Process scheduling and timing constraints properly defined

#### Safety and Reliability Standards  
- [ ] **Safety Requirements**: All ASIL-rated requirements mapped to implementation
- [ ] **Fault Handling**: Comprehensive fault detection and reaction strategies
- [ ] **Diagnostic Coverage**: Adequate monitoring and diagnostic event generation
- [ ] **Recovery Procedures**: Safe states and recovery mechanisms documented
- [ ] **Hardware Dependencies**: Abstraction layers and failure isolation adequate

#### Implementation and Integration Readiness
- [ ] **Coding Standards**: MISRA C compliance and Bosch conventions followed
- [ ] **Header Dependencies**: Include hierarchy analyzed with circular references resolved  
- [ ] **Concurrency Safety**: Thread safety and synchronization mechanisms specified
- [ ] **Resource Management**: Memory and performance constraints documented
- [ ] **Testability**: Test interfaces and observability mechanisms adequate

#### Documentation Quality and Maintenance
- [ ] **Traceability**: Requirements-to-implementation mapping complete and verifiable
- [ ] **Visual Clarity**: Appropriate diagrams for architecture, flow, and state behavior
- [ ] **Technical Accuracy**: Content verified against requirements and design decisions
- [ ] **Maintainability**: Documentation structure supports ongoing updates and changes
- [ ] **Completeness**: All required sections present with adequate detail level
