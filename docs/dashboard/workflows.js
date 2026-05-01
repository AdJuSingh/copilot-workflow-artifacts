// ── Edit this file to add/remove/update workflows and agents ────────────────
// No server needed — this file is loaded as a plain <script> tag.
// After editing, just refresh the browser (F5).
// ─────────────────────────────────────────────────────────────────────────────

// ── Repository metadata — auto-updated by CI and local task ─────────────────
window._META = {
  repo:   "AdJuSingh/copilot-workflow-artifacts",  // GitHub owner/repo
  clones: { count: 0, unique: 0, asOf: "May 2026" }
  // count/unique/asOf are updated automatically -- do not edit by hand
};
window._WORKFLOWS = [
  {
    id:"hsw", domain:"vmbs", title:"HSW", sub:"vm-bs / hsw", status:"live",
    agents:[
      { step:"1",  name:"DSD Generator",           file:"hsw-dsd-generator.prompt.md" },
      { step:"2",  name:"DSD Review Checklist",     file:"hsw-dsd-reviewchecklist.prompt.md" },
      { step:"3",  name:"Implementation Assist",    file:"hsw-implementation-assist.prompt.md" },
      { step:"4",  name:"Unit Test Spec Generator", file:"hsw-unittest-1-spec-generaor.prompt.md" },
      { step:"5",  name:"UT Spec Review Checklist", file:"hsw-unittest-2-spec-reviewchecklist.prompt.md" },
      { step:"6",  name:"UT Environment Setup",       file:"hsw-unittest-3-environmentsetup.prompt.md" },
      { step:"7",  name:"UT Code Implementation",       file:"hsw-unittest-4-codegeneration.prompt.md" },
      { step:"8",  name:"UT Execution",                 file:"hsw-unittest-5-execution.prompt.md" },
      { step:"\u2605", name:"Memory Orchestrator",      file:"hsw-memory-orchestrator.prompt.md" }
    ]
  },
  {
    id:"dcom", domain:"vmbs", title:"ISW \u00b7 DCOM", sub:"vm-bs / isw / dcom \u2014 Diagnostic Communication", status:"live",
    agents:[
      { step:"00", name:"Build Software",           file:"00-build-software.prompt.md" },
      { step:"0",  name:"Requirements Analysis",    file:"0-create-requirements-analysis.prompt.md" },
      { step:"1",  name:"Detailed Software Design", file:"1-create-detailed-software-design.prompt.md" },
      { step:"2",  name:"Create Implementation",    file:"2-create-implementation.prompt.md" },
      { step:"3a", name:"Create Workspace BAT",     file:"3-ut-0-create-workspace-bat.prompt.md" },
      { step:"3b", name:"Compile Source File",      file:"3-ut-1-compile-source-file.prompt.md" },
      { step:"3c", name:"Generate Unit Tests",      file:"3-ut-2-generate-unit-tests.prompt.md" },
      { step:"4a", name:"Build Unit Test",          file:"4-ut-3-build-unit-test.prompt.md" },
      { step:"4b", name:"TPA Report Generation",    file:"4-ut-4-tpa-report-generation.prompt.md" },
      { step:"5",  name:"Create Component Test",    file:"5-create-componenttest.prompt.md" },
      { step:"6",  name:"CT Sim Execution",          file:"6-ct-sim-execution.prompt.md" },
      { step:"7",  name:"Copilot Self-Review",        file:"7-create-copilot-self-review-result.prompt.md" },
      { step:"\u2605", name:"MISRA C Code Review",  file:"c-code-review-misra.prompt.md" }
    ]
  },
  {
    id:"dsm", domain:"vmbs", title:"ISW \u00b7 DSM", sub:"vm-bs / isw / dsm \u2014 Diagnostic SW Manager", status:"pilot",
    agents:[
      { step:"00", name:"Build Software",               file:"00_build_software.prompt.md" },
      { step:"0",  name:"Requirements Analysis",        file:"0_create_requirements_analysis.prompt.md" },
      { step:"1",  name:"Create SWCS Requirements",     file:"1_create_swcs_requirements.prompt.md" },
      { step:"2a", name:"Splitter Input Generation",    file:"2_0_splitter_input_generation.prompt.md" },
      { step:"2b", name:"Update FW Node & Graph Links", file:"2_1_update_fw_node_and_graphlinks.prompt.md" },
      { step:"2c", name:"Update DTC Workflow",          file:"2_2_update_dtc_complete_workflow.prompt.md" },
      { step:"2d", name:"Update STM Database",          file:"2_3_update_stm_database.prompt.md" },
      { step:"3",  name:"Create Review Report",         file:"3_Create_Review_Report.prompt.md" },
      { step:"4",  name:"DSMSIM CT Spec & Script Gen",  file:"4_DSMSIM_CT_Spec_Script_Generation.prompt.md" },
      { step:"5",  name:"DSMSIM Execution",             file:"5_DSMSIM_Execution.prompt.md" }
    ]
  }
];
