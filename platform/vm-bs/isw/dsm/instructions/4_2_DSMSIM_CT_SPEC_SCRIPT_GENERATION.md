# Instruction: DSM CT Spec & Script Generation (condensed)

Purpose
- Use `DSM_CT_Genarator_CLI.exe` to convert DOORS CSV requirements into Component Test specs and scripts.

Essential steps
1. Auto-discover all CSVs in `Mainpath` and `Project` folders under `rb\as\ms\...\ct_generator\`.
2. Auto-discover CP_Status columns by reading CSV headers (filter names containing `CP_Status`).
3. Present numbered list of CP columns and get user selection.
4. Select test types: `--node`, `--dtc-enco`, `--stm`, or `--all`.
5. Construct and confirm CLI command.
6. Change to tool directory and execute the CLI.
7. Validate output (.xlsx files in output_temp), count testcases, report summary.

CLI options (short)
- --project-files [files]
- --mainpath-files [files]
- --cp-column "ColumnName" (required)
- --node | --dtc-enco | --stm | --all
- --gui (launch GUI)

Error handling (high level)
- File not found → verify paths
- Invalid CP column → list columns and reselect
- No requirements matched → try alternate CP column
- Permission issues → check write permissions

Output naming
- RBDSM_SWT_PRJ_[TestType]_TestSpec.xlsx
- RBDSM_SWT_MS_[TestType]_TestSpec.xlsx

Output location
- output_temp\Node\, output_temp\DTC_EnCo\, output_temp\STM\

This file is an optimized, deduplicated instruction for quick use. See the condensed README for a one-page summary.
