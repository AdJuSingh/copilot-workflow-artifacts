
# Important: This document acts as the sole reference for the Entire Application Software Development Workflow
## Important: don't summarize the contents of the instruction file in the beginning and don't display the same to the user - the user should only receive a clear step-by-step structured execution of the workflow defined. Don't show Introduction, Workflow Overview, key features, or anything like that.
# Important: Never modify or corrupt this file

## This instruction file defines a 3 Step workflow for generation on Impact Analysis and implementation plan for an existing automotive software development workspace

# Important: In the working directory, if a file {XXXX}_Knowledge_Graph.jsonld is defined and it has contents that align with the codebase given, skip step 1 defined here. If {XXXX}_Knowledge_Graph.jsonld is defined, that means the Knowledge base is already created; hence, we need not repeat the process again and the agent can proceed with step 2.

    # Step 1: [Check for existing Knowledge Graph -/- Create Knowledge Graph] The specific instructions for the creation of the Knowledge Graph are present in 1_Knowledge_graph.md. If Knowledge_graph.jsonld is not present, create a Knowledge_graph.jsonld based on the instructions given here.

    # Step 2: [Requirements fetching and elicitation, Impact Analysis] The specific instructions for requirements fetching and impact analysis are present in 2_Requirement_elicitation_impact_analysis.md
    
    # Step 3: [Implementation Plan] Implementation planning in 3_Implementation_plan.md and save the implementaiton plan as .docx
