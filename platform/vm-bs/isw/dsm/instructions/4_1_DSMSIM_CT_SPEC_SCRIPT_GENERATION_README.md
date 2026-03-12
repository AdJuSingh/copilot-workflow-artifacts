# DSM CT Spec & Script Generation — Quick Reference (condensed)

Purpose
- Generate DSM Component Test (.ct) specs and scripts from DOORS-exported CSVs using DSM_CT_Genarator_CLI.exe.

Key files created
- Instruction: `.github/instructions/1_DSMSIM_CT_SPEC_SCRIPT_GENERATION.md`
- Prompt: `.github/prompts/1_DSMSIM_CT_Spec_Script_Generation.prompt.md`

Tool location
- rb\as\ms\ESP10E_MFA2\dsmpr\tst\ct_generator\DSM_CT_Genarator_CLI.exe

Quick commands
- Show help:
  .\DSM_CT_Genarator_CLI.exe --help
- Generate all tests (example):
  cd "...\ct_generator"
  .\DSM_CT_Genarator_CLI.exe --project-files ".\Project\000000_SWCS_DSM_Node_Config_ESP_Europium.csv" ".\Project\000000_SWCS_DSM_STM_Config_ESP_Europium.csv" --mainpath-files ".\Mainpath\Gen_SWCS_DSM_Node_ConfigMS_ESP.csv" ".\Mainpath\Gen_SWCS_DSM_STM_ConfigMS_ESP.csv" --cp-column "STLA332_BB51408_RB_RS_CP_Status" --all

Workflow (high level)
1. Auto-discover all CSVs in Mainpath/Project folders
2. Auto-discover CP_Status columns from CSV headers (filter names containing 'CP_Status')
3. Present numbered list of CP columns and get user selection
4. Choose test type(s): Node / DTC/EnCo / STM / All
5. Run DSM_CT_Genarator_CLI.exe
6. Validate generated .xlsx files in output_temp and counts

Checklist
- CSVs present and readable
- CP column identified (contains 'CP_Status')
- Output directory writable
- Confirm command before execution

Output
- .xlsx test specification files appear under `output_temp\Node\`, `output_temp\DTC_EnCo\`, and `output_temp\STM\` by default.

Notes
- This README is a concise reference; detailed steps are in the instruction file.
