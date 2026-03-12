# GHCP Orchestrated Workflow
This repository contains the VM organization structure with agentic artifacts for platform and project specific.

## Overview

This project provides a standardized framework for organizing VM structures with agentic artifacts that support VM platform development and project management workflows.

## Repository Structure

- **`generic/`** - Contains VM-specific configurations and prompts organized by vehicle domains:
  - `vm-bs/` - Brake System artifacts
  - `vm-oss/` - Occupant Safety System artifacts  
  - `vm-st/` - Steering System artifacts

- **`docs/`** - Project documentation including VM organization structure and onboarding materials

- **`projects/`** - Example projects and project templates for new implementations

- **`tests/`** - Test configurations and validation scripts  


## VM Organization Structure

### Generic Configurations

#### Brake Systems (vm-bs)
- **ASW (Application Software)**
- **HSW (Hardware Related Software)**
- **ISW (Infrastructure Software)**: 
  - DCOM: Diag Communication related
  - DSM: Diag software related
  - NET: Network configuration prompts

#### Occupant Safety Systems (vm-oss)
- **Follows the same folder structure as VM-BS**

#### Steering Systems (vm-st)  
- ***Follows the same folder structure as VM-BS**

## Contact
