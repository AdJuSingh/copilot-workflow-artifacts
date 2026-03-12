Generate DSM Component Test specifications and scripts using DSM_CT_Genarator_CLI.exe.

Steps (automated-friendly)
1. Auto-discover CSVs:
   - Scan `rb\as\mb\ipb\dsmpr\tst\ct_generator` folder for all CSV files.
   - Classify CSVs: files starting with "Gen" are mainpath files, all others are project files.
   - Use ALL CSV files found (no user selection).
2. Auto-discover CP_Status columns:
   - Read CSV headers (first line) from all discovered CSVs.
   - Filter header names containing `CP_Status`.
   - Present deduplicated numbered list (no descriptions).
3. Ask user for CP column selection (number or exact name) and test type (all/node/dtc-enco/stm).
4. Construct CLI command:
   .\DSM_CT_Generator.exe --project-files [non-Gen files] --mainpath-files [Gen* files] --cp-column "ColumnName" --all
5. Directly execute the CLI command in the tool folder (cd to rb\as\mb\ipb\dsmpr\tst\ct_generator) and monitor output.
6. Validate generated .xlsx files in output_temp and summarize counts.

Requirements:
- Must read CSV headers to find CP columns; only show header names containing `CP_Status`.
- Present minimal output (numbered lists, commands).
- Once user provides CP column selection and test type, directly execute the command without confirmation.

Success: `.xlsx` test specification files generated in output_temp folder and summary presented.
